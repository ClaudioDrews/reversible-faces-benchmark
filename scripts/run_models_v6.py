#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Cláudio Drews
"""Round 4 runner (prompt v6): one prompt, a short tool loop, one SVG per model.

Usage:
    export OPENROUTER_API_KEY=...            # never commit keys
    python scripts/run_models_v6.py OUT_DIR prompts/prompt-v6.md deepseek/deepseek-v4.1-flash

Requires: Python 3.9+, Pillow, numpy (for the diagnostics), headless Chrome/Chromium on PATH, and
bubblewrap (`bwrap`) for the code sandbox. Runs ONE model per invocation. Settings used in round 4:
    NOREASON=1 MAXTOK=20000 ...   deepseek/deepseek-v4.1-flash
    EFFORT=medium MAXTOK=32000 .. z-ai/glm-5.3-flash
    EFFORT=low MAXTOK=32000 ..    minimax/minimax-m3.1-flash   (re-run with MAXTOK=64000, see rounds/round-04/SETUP.md)
Note: after the first three round-4 runs (and before the MiniMax re-run) the EVENT/TITLE regular
expressions were widened to accept backticks around the lines (GLM used them). After all runs, only this
docstring and the import path of validate_svg were changed (made relative so the repository copy runs
from any directory); the logic is otherwise unchanged.

Tools offered to the model (OpenAI-style function calling via OpenRouter):
  run_python(code)   sandboxed Python 3 (bubblewrap: no network, private temp dir, 20 s, memory limit)
  render_svg(path|svg) Chrome renders upright (A) and rotated 180 degrees (B); an image of both plus
                     text diagnostics are fed back (every model used here accepts image input).
Limits: MAX_RENDERS=5, MAX_TOOLCALLS=12, MAX_TURNS=16, COST_CAP_USD=0.25 per model.
Environment: OPENROUTER_API_KEY; EFFORT (low|medium|high) or NOREASON=1; MAXTOK (per turn).
Everything is saved under OUT_DIR/<model>/: transcript.jsonl, reasoning.txt, render-N.png,
work/ (the sandbox folder), raw.txt (final answer), <model>.svg, cost-log.json.
"""
import base64, io, json, os, re, shutil, subprocess, sys, tempfile, time, urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path
from PIL import Image

sys.path.insert(0, str(Path(__file__).resolve().parent))
from validate_svg import check as contract_check  # noqa: E402

MAX_RENDERS, MAX_TOOLCALLS, MAX_TURNS = 5, 12, 16
COST_CAP = float(os.environ.get("COST_CAP_USD", "0.25"))
PY_TIMEOUT, PY_OUT = 20, 8000

TOOLS = [
    {"type": "function", "function": {
        "name": "run_python",
        "description": "Run Python 3 (stdlib, numpy, Pillow) in a private temporary folder that persists between calls. "
                       "No network, 20 s limit, 4000 chars of output. Files written here can be passed to render_svg.",
        "parameters": {"type": "object", "properties": {"code": {"type": "string"}}, "required": ["code"]}}},
    {"type": "function", "function": {
        "name": "render_svg",
        "description": "Render an SVG in Chrome upright (A, left) and rotated 180 degrees (B, right). Returns one image "
                       "and diagnostics. Give either `path` (a file in the folder) or `svg` (the SVG text). Max 5 calls.",
        "parameters": {"type": "object", "properties": {"path": {"type": "string"}, "svg": {"type": "string"}}}}},
]


def chrome():
    for n in ("google-chrome", "chromium", "chromium-browser"):
        p = shutil.which(n)
        if p:
            return p
    raise SystemExit("no chrome")


def normalize_svg(text):
    """Used for BOTH the rendered copy and the delivered copy: per-attribute fixes, strip title/desc/metadata."""
    m = re.search(r"<svg\b[^>]*?(/?)>", text, re.S)
    head = m.group(0)
    selfclose = head.endswith("/>")
    inner = head[4:-2] if selfclose else head[4:-1]
    if "xmlns=" not in inner:
        inner += ' xmlns="http://www.w3.org/2000/svg"'
    if not re.search(r"\sviewBox=", " " + inner):
        inner += ' viewBox="0 0 1000 1000"'
    if not re.search(r"\swidth=", " " + inner):
        inner += ' width="1000"'
    if not re.search(r"\sheight=", " " + inner):
        inner += ' height="1000"'
    new = "<svg" + inner + ("/>" if selfclose else ">")
    text = text.replace(head, new, 1)
    return re.sub(r"\s*<(title|desc|metadata)\b.*?</\1>", "", text, flags=re.S)


def chrome_shot(html_path, png, size, extra=()):
    prof = tempfile.mkdtemp(prefix="chrome-prof-")
    try:
        subprocess.run([chrome(), "--headless", "--no-sandbox", "--disable-gpu", "--hide-scrollbars",
                        "--force-device-scale-factor=1",
                        "--virtual-time-budget=3000", "--run-all-compositor-stages-before-draw",
                        '--host-resolver-rules=MAP * ~NOTFOUND',
                        f"--screenshot={png}", f"--window-size={size},{size}", *extra, Path(html_path).resolve().as_uri()],
                       check=True, capture_output=True, timeout=60,
                       env={**os.environ, 'XDG_CONFIG_HOME': prof, 'XDG_CACHE_HOME': prof})
    finally:
        shutil.rmtree(prof, ignore_errors=True)


def render_pair(svg_path, size=500):
    with tempfile.TemporaryDirectory() as tmp:
        html = Path(tmp) / "p.html"
        html.write_text(f'<html><body style="margin:0;background:#fff"><img src="{Path(svg_path).resolve().as_uri()}" '
                        f'width="{size}" height="{size}"></body></html>')
        png = Path(tmp) / "up.png"
        chrome_shot(html, png, size)
        up = Image.open(png).convert("RGB")
    if up.size != (size, size):
        up = up.crop((0, 0, size, size)) if min(up.size) >= size else up.resize((size, size))
    return up, up.rotate(180)


BBOX_JS = """<script>
window.onload=function(){var out=[];var svg=document.querySelector('svg');var sc=1000/svg.getBoundingClientRect().width;
function add(el,label){var r=el.getBoundingClientRect();if(!r.width&&!r.height)return;
 var b=[r.left*sc,r.top*sc,r.right*sc,r.bottom*sc].map(Math.round);out.push({label:label,box:b,area:(b[2]-b[0])*(b[3]-b[1])});}
var kids=[].slice.call(svg.children);var i=0;
kids.forEach(function(k){var t=k.tagName.toLowerCase();i++;
 if(t==='g'){var rot=(k.getAttribute('transform')||'').indexOf('rotate')>=0;var j=0;
   [].slice.call(k.children).forEach(function(c){j++;add(c,'g'+i+(rot?'(rotated)':'')+'/'+c.tagName.toLowerCase()+j)});}
 else add(k,t+i);});
document.title='';var pre=document.createElement('pre');pre.id='bboxes';pre.textContent=JSON.stringify(out);document.body.appendChild(pre);};
</script>"""


def element_table(svg_text):
    """Per-element bounding boxes (page units) and where they land after the half-turn. Measured by Chrome."""
    clean = re.sub(r"<script\b.*?</script>", "", svg_text, flags=re.S)
    clean = re.sub(r"\son\w+\s*=\s*(\"[^\"]*\"|'[^']*')", "", clean)
    clean = re.sub(r"^<\?xml[^>]*\?>", "", clean.strip())
    clean = clean.replace("<svg", '<svg style="width:500px;height:500px;display:block"', 1)
    with tempfile.TemporaryDirectory() as tmp:
        html = Path(tmp) / "b.html"
        html.write_text(f'<html><body style="margin:0">{clean}{BBOX_JS}</body></html>')
        prof = tempfile.mkdtemp(prefix="chrome-prof-")
        try:
            p = subprocess.run([chrome(), "--headless", "--no-sandbox", "--disable-gpu",
                                "--virtual-time-budget=3000", '--host-resolver-rules=MAP * ~NOTFOUND',
                                "--window-size=500,500", "--dump-dom", html.as_uri()],
                               capture_output=True, text=True, timeout=60,
                               env={**os.environ, 'XDG_CONFIG_HOME': prof, 'XDG_CACHE_HOME': prof})
        finally:
            shutil.rmtree(prof, ignore_errors=True)
    m = re.search(r'<pre id="bboxes">(.*?)</pre>', p.stdout, re.S)
    if not m:
        return "(element table unavailable)"
    import html as H
    rows = json.loads(H.unescape(m.group(1)))
    rows.sort(key=lambda r: -r["area"])
    lines = ["largest elements: bbox on the page (x0,y0,x1,y1) -> bbox as it appears in B after the half-turn"]
    for r in rows[:12]:
        x0, y0, x1, y1 = r["box"]
        lines.append(f"  {r['label']}: [{x0},{y0},{x1},{y1}] -> [{1000-x1},{1000-y1},{1000-x0},{1000-y0}]")
    if len(rows) > 12:
        lines.append(f"  (+{len(rows)-12} smaller elements)")
    return "\n".join(lines)


def diagnostics(svg_path, up, rot):
    problems, info = contract_check(svg_path)
    import numpy as np
    g = np.asarray(up.convert("L").resize((200, 200)), dtype=float)
    ink = 255.0 - g
    r = np.rot90(ink, 2)
    rho = float(np.linalg.norm(ink - r) / (np.linalg.norm(ink) + 1e-9))
    nonwhite = g < 200
    frac = float(nonwhite.mean())
    ys, xs = np.where(nonwhite)
    bbox = [int(xs.min() * 5), int(ys.min() * 5), int(xs.max() * 5), int(ys.max() * 5)] if len(xs) else None
    size_kb = round(Path(svg_path).stat().st_size / 1024, 1)
    lines = [f"file: {size_kb} KB",
             "contract problems: " + ("none" if not problems else "; ".join(problems)),
             f"has <title>/<desc>: {info.get('has_title_or_desc')}",
             f"rho (rotational symmetry; 0 = looks identical upside down; only a one-sided alarm): {rho:.3f}",
             f"non-white fraction of the page: {frac:.3f}; bounding box of non-white pixels (x0,y0,x1,y1): {bbox}"]
    if frac > 0.8:
        lines.append("note: the page is almost all non-white, so rho is not informative.")
    elif frac < 0.004:
        lines.append("WARNING: almost nothing is drawn (blank or tiny figure).")
    elif rho < 0.15:
        lines.append("WARNING: very low rho: the figure is nearly rotationally symmetric.")
    try:
        lines.append(element_table(Path(svg_path).read_text()))
    except Exception as e:
        lines.append(f"(element table failed: {e})")
    return "\n".join(lines), rho


def run_python(code, work):
    script = work / "_snippet.py"
    script.write_text(code)
    cmd = ["env", "-i", "PATH=/usr/bin", "HOME=/work", "bwrap", "--unshare-all", "--die-with-parent", "--cap-drop", "ALL",
           "--ro-bind", "/usr", "/usr", "--ro-bind", "/usr/local", "/usr/local", "--symlink", "usr/lib", "/lib",
           "--symlink", "usr/lib64", "/lib64", "--symlink", "usr/bin", "/bin", "--proc", "/proc", "--dev", "/dev",
           "--tmpfs", "/tmp", "--bind", str(work), "/work", "--chdir", "/work",
           "bash", "-c", f"ulimit -v 4000000; ulimit -f 40000; exec timeout {PY_TIMEOUT} python3 _snippet.py"]
    try:
        p = subprocess.run(cmd, capture_output=True, text=True, timeout=PY_TIMEOUT + 10)
        out = (p.stdout or "") + (("\n[stderr]\n" + p.stderr) if p.stderr else "")
        if p.returncode == 124:
            out += f"\n[timed out after {PY_TIMEOUT} s]"
    except subprocess.TimeoutExpired:
        out = f"[timed out after {PY_TIMEOUT} s]"
    if len(out) > PY_OUT:
        out = out[:PY_OUT] + f"\n[output truncated at {PY_OUT} chars]"
    return out or "(no output)"


def api(key, body):
    for attempt in range(3):
        b = dict(body)
        if attempt == 2:
            b["max_tokens"] = min(b.get("max_tokens", 16000), 16000)
        try:
            req = urllib.request.Request("https://openrouter.ai/api/v1/chat/completions", json.dumps(b).encode(),
                                         {"Authorization": "Bearer " + key, "Content-Type": "application/json"})
            r = json.load(urllib.request.urlopen(req, timeout=600))
            if "choices" in r and r["choices"]:
                return r
            print("API returned no choices:", str(r)[:300], flush=True)
        except Exception as e:
            err = str(e)
            if hasattr(e, "read"):
                try:
                    err += " " + e.read().decode()[:500]
                except Exception:
                    pass
            print("API error", attempt, err, flush=True)
        time.sleep(5 * (attempt + 1))
    return None


def png_b64(img):
    b = io.BytesIO()
    img.save(b, "PNG", optimize=True)
    return base64.b64encode(b.getvalue()).decode(), b.getvalue()


HARNESS = "[harness output, not a person] "
DELIVER = ("[harness] Deliver now, without calling a tool, in the final format: an `EVENT:` line, a `TITLE:` line, "
           "then the complete SVG in one ```xml block.")


def main():
    out_root, prompt_file, model = Path(sys.argv[1]), Path(sys.argv[2]), sys.argv[3]
    name = re.sub(r"[^A-Za-z0-9._-]", "_", model.split("/", 1)[1])
    key = os.environ["OPENROUTER_API_KEY"]
    out = out_root / name
    work = out / "work"
    work.mkdir(parents=True, exist_ok=True)
    reasoning = {"enabled": False} if os.environ.get("NOREASON") else {"effort": os.environ.get("EFFORT", "medium")}
    maxtok = int(os.environ.get("MAXTOK", "32000"))
    msgs = [{"role": "user", "content": prompt_file.read_text()}]
    tlog = (out / "transcript.jsonl").open("w")
    rfile = (out / "reasoning.txt").open("w")

    def log(kind, **kw):
        tlog.write(json.dumps({"t": round(time.time()), "kind": kind, **kw}, ensure_ascii=False) + "\n")
        tlog.flush()

    def prune_images(keep=2):
        idx = [i for i, m in enumerate(msgs) if m["role"] == "user" and isinstance(m["content"], list)]
        for i in idx[:-keep]:
            msgs[i] = {"role": "user", "content": HARNESS + "(an older render image was removed to save cost; "
                       "the numbers above remain.)"}

    log("user_prompt", file=str(prompt_file), chars=len(msgs[0]["content"]))
    cost, ptok, ctok, renders, toolcalls, turns = 0.0, 0, 0, 0, 0, 0
    per_turn, final_text, last_svg_text, finish = [], None, None, None
    force, forced_once, providers = False, False, set()
    t0 = time.time()

    def call(force_now):
        body = {"model": model, "messages": msgs, "max_tokens": maxtok, "reasoning": reasoning,
                "usage": {"include": True}}
        if not force_now:
            body["tools"] = TOOLS
            body["tool_choice"] = "auto"
        return api(key, body)

    while turns < MAX_TURNS + 2 and time.time() - t0 < 1800:
        turns += 1
        r = call(force)
        if not r:
            finish = "api_failure"
            break
        ch = r["choices"][0]
        m = ch["message"]
        u = r.get("usage", {})
        c = u.get("cost", 0) or 0
        cost += c
        ptok += u.get("prompt_tokens", 0) or 0
        ctok += u.get("completion_tokens", 0) or 0
        providers.add(str(r.get("provider")))
        det = (u.get("completion_tokens_details") or {})
        per_turn.append({"turn": turns, "prompt_tokens": u.get("prompt_tokens"), "completion_tokens": u.get("completion_tokens"),
                         "reasoning_tokens": det.get("reasoning_tokens"), "cost": c, "finish": ch.get("finish_reason"),
                         "tool_calls": len(m.get("tool_calls") or []), "provider": r.get("provider"), "forced": force})
        reas = m.get("reasoning") or ""
        if reas:
            rfile.write(f"\n===== turn {turns} =====\n{reas}\n")
            rfile.flush()
        log("assistant", turn=turns, content=m.get("content"), tool_calls=m.get("tool_calls"),
            finish=ch.get("finish_reason"), usage=u, provider=r.get("provider"))
        tcs = m.get("tool_calls") or []
        am = {"role": "assistant", "content": m.get("content") if m.get("content") else (None if tcs else "")}
        if tcs:
            am["tool_calls"] = tcs
        if m.get("reasoning_details"):
            am["reasoning_details"] = m["reasoning_details"]
        msgs.append(am)
        if not tcs or force:
            txt = m.get("content") or ""
            if re.search(r"<svg\b.*?</svg>", txt, re.S):
                final_text, finish = txt, ch.get("finish_reason")
                break
            # empty / SVG-less answer: ask once more, forced, with the last rendered SVG available
            if forced_once:
                final_text, finish = txt, (ch.get("finish_reason") or "") + "+no_svg"
                break
            forced_once, force = True, True
            note = HARNESS + "Your reply contained no SVG. " + DELIVER
            if last_svg_text:
                note += "\nThe last SVG you rendered was:\n```xml\n" + last_svg_text + "\n```"
            msgs.append({"role": "user", "content": note})
            log("harness", note="no svg in final; forced")
            continue
        images = []
        for tc in tcs:
            fn = tc["function"]["name"]
            try:
                args = json.loads(tc["function"].get("arguments") or "{}")
            except Exception:
                args = {}
            toolcalls += 1
            if toolcalls > MAX_TOOLCALLS:
                res = "TOOL LIMIT REACHED (12). Deliver now, without calling a tool."
            elif fn == "run_python":
                res = run_python(str(args.get("code", "")), work)
            elif fn == "render_svg":
                if renders >= MAX_RENDERS:
                    res = "RENDER LIMIT REACHED (5). Deliver now, without calling a tool."
                else:
                    renders += 1
                    try:
                        if args.get("svg"):
                            raw_text = args["svg"]
                        else:
                            sp = (work / str(args.get("path", ""))).resolve()
                            if work.resolve() not in sp.parents or not sp.is_file():
                                raise ValueError("path must be a file inside the working folder")
                            raw_text = sp.read_text()
                        norm = normalize_svg(raw_text)
                        rp = work / f"_render_{renders}.svg"
                        rp.write_text(norm)
                        up, rot = render_pair(rp)
                        import numpy as np
                        if (np.asarray(up.convert("L")) > 250).mean() > 0.9999 and "<rect" not in norm and len(norm) > 300:
                            pass
                        txt, rho = diagnostics(rp, up, rot)
                        W = 500
                        comp = Image.new("RGB", (W * 2 + 30, W + 10), "white")
                        comp.paste(up, (5, 5)); comp.paste(rot, (W + 25, 5))
                        b64, raw = png_b64(comp)
                        (out / f"render-{renders}.png").write_bytes(raw)
                        (out / f"render-{renders}.svg").write_text(norm)
                        last_svg_text = norm
                        images.append((renders, b64))
                        res = (f"render {renders}/{MAX_RENDERS}. Left image = A (upright), right image = B (rotated 180°). "
                               f"The image follows in the next message.\n{txt}")
                    except Exception as e:
                        renders -= 1  # a failed render does not use up a render
                        res = f"render failed (not counted): {e}"
            else:
                res = f"unknown tool {fn}"
            log("tool", turn=turns, name=fn, args=args if fn != "run_python" else {"code": args.get("code")}, result=res)
            msgs.append({"role": "tool", "tool_call_id": tc["id"], "content": res})
        if images:
            parts = []
            for n, b64 in images:
                parts.append({"type": "text", "text": HARNESS + f"Image for render {n}: A (upright) on the left, B (rotated 180°) on the right."})
                parts.append({"type": "image_url", "image_url": {"url": "data:image/png;base64," + b64}})
            msgs.append({"role": "user", "content": parts})
            prune_images(2)
        stop_now = None
        if cost >= COST_CAP:
            stop_now = "cost cap reached"
        elif toolcalls >= MAX_TOOLCALLS or (renders >= MAX_RENDERS and toolcalls >= MAX_TOOLCALLS - 2):
            stop_now = "tool budget used"
        elif turns >= MAX_TURNS:
            stop_now = "turn cap reached"
        if stop_now and not force:
            force = True
            note = HARNESS + stop_now.capitalize() + ". " + DELIVER
            if last_svg_text:
                note += "\nThe last SVG you rendered was:\n```xml\n" + last_svg_text + "\n```"
            msgs.append({"role": "user", "content": note})
            log("harness", note=stop_now)
    text = final_text or ""
    (out / "raw.txt").write_text(text)
    ev = re.search(r"^`?EVENT:\s*(.+?)`?$", text, re.M)
    ti = re.search(r"^`?TITLE:\s*(.+?)`?$", text, re.M)
    rec = {"model": model, "reasoning": reasoning, "max_tokens_per_turn": maxtok, "turns": turns,
           "tool_calls": toolcalls, "renders": renders, "prompt_tokens_total": ptok, "completion_tokens_total": ctok,
           "cost_usd": round(cost, 6), "cost_cap_usd": COST_CAP, "finish": finish, "providers": sorted(providers),
           "per_turn": per_turn, "event": ev.group(1).strip() if ev else None, "title": ti.group(1).strip() if ti else None,
           "seconds": round(time.time() - t0)}
    m = re.search(r"<svg\b.*?</svg>", text, re.S)
    if m:
        svg = '<?xml version="1.0" encoding="UTF-8"?>\n' + normalize_svg(m.group(0)) + "\n"
        try:
            ET.fromstring(svg.split("?>", 1)[1]); rec["xml"] = "valid"
        except ET.ParseError as e:
            rec["xml"] = f"INVALID: {e}"
        (out / f"{name}.svg").write_text(svg)
        rec["svg"] = f"{name}.svg"
    else:
        rec["svg"] = None
        if last_svg_text:
            rec["note"] = "no SVG in final answer; last rendered file kept as render-N.svg only (NOT delivered)"
    (out / "cost-log.json").write_text(json.dumps(rec, indent=1, ensure_ascii=False))
    print(name, {k: v for k, v in rec.items() if k != "per_turn"}, flush=True)


if __name__ == "__main__":
    main()
