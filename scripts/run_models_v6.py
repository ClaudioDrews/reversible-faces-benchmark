#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Cláudio Drews
"""Round 4 runner (prompt v6): a SINGLE-ATTEMPT TOOL-AUGMENTED run per model. Not one-shot.

Usage:
    export OPENROUTER_API_KEY=...            # never commit keys
    python scripts/run_models_v6.py [--timestamped|--force] OUT_DIR prompts/prompt-v6.md deepseek/deepseek-v4.1-flash
    python scripts/run_models_v6.py --mock [--mock-svg hostile] OUT_DIR prompts/prompt-v6.md deepseek/deepseek-v4.1-flash   # offline, free

Protocol (see docs/methodology.md): one initial prompt from the human, then a loop in which the model may call
two tools and the HARNESS (not a person) sends tool results and, when a budget is used up, a delivery notice.
One run per model; the first final answer that contains an SVG is the answer.

Requires: Python 3.9+, Pillow, numpy, defusedxml (requirements.txt), headless Chrome/Chromium and bubblewrap
(`bwrap`). Runs ONE model per invocation. Settings used in round 4:
    NOREASON=1 MAXTOK=20000 ...   deepseek/deepseek-v4.1-flash
    EFFORT=medium MAXTOK=32000 .. z-ai/glm-5.3-flash
    EFFORT=low MAXTOK=32000 ..    minimax/minimax-m3.1-flash   (re-run with MAXTOK=64000, see rounds/round-04/SETUP.md)

IMPORTANT: this file is the hardened version (security, budget and logging changes made after round 4). The
round-4 results were produced by the earlier version, commit 6747499 (see docs/security.md and
docs/reproduction.md). Model-output handling changed (sanitizing, sandboxed rendering, original SVG saved
separately). The prompts, the tool set and the numeric limits are the same, but this version can do two things
the old one could not: LOWER max_tokens for a call when the worst-case estimate would not fit the remaining
budget, and stop before a call (cost_precheck_stop). To reproduce round 4 exactly, check out commit 6747499.

Tools offered to the model (OpenAI-style function calling via OpenRouter):
  run_python(code)     sandboxed Python 3 (bubblewrap: no network, private temp dir, 20 s, memory limit)
  render_svg(path|svg) the SVG is sanitized (allowlist), then rendered by Chrome INSIDE a bubblewrap sandbox,
                       upright (A) and rotated 180 degrees (B); an image of both plus text diagnostics are fed
                       back (every model used here accepts image input).

Limits (operational, per model): MAX_RENDERS=5 renders, MAX_TOOLCALLS=12 tool calls, MAX_TURNS=16 turns,
COST_CAP_USD=0.25, 1800 s wall clock (checked between calls).
  * MAX_TURNS counts turns in which the model may use tools. The loop allows MAX_TURNS+2 = 18 API calls in
    total: the 2 extra are RECOVERY turns, namely (1) the forced-delivery turn after a delivery notice (turn,
    tool or cost cap) and (2) one re-ask when a forced or final reply contains no SVG. There is no third.
  * COST_CAP_USD is an APPROXIMATE operational limit, not a guarantee. Before each call the harness estimates
    the worst case (prompt tokens x input price + max_tokens x output price) and lowers max_tokens, or stops,
    if that would exceed the remaining budget; after each call it adds the provider-reported cost. Failed or
    timed-out requests are not reported by the provider and can be billed unseen; a wrong price shifts the
    estimate. If the provider omits usage.cost the cost is derived from the reported tokens and the price (never
    counted as free). Any overrun of the reported cost is written to cost-log.json (cost_overrun_usd).
Environment: OPENROUTER_API_KEY; EFFORT (low|medium|high) or NOREASON=1; MAXTOK (per turn); COST_CAP_USD;
PRICE_IN_PER_MTOK / PRICE_OUT_PER_MTOK (USD per million tokens; otherwise read from OpenRouter's public models
list, otherwise a pessimistic default).
Everything is saved under OUT_DIR/<model>/ (refuses to overwrite a non-empty directory): transcript.jsonl,
api-errors.jsonl (structured log of failed API attempts), reasoning.txt, render-N.png, render-N.svg (what was
rendered: sanitized) and render-N.original.svg (what the model sent, normalized, never rendered unsandboxed),
work/ (the sandbox folder), raw.txt (final answer), <model>.original.svg (the model's SVG, verbatim),
<model>.svg (normalized; the delivered file), <model>.sanitized.svg, cost-log.json (incl. validator report).
"""
import argparse, base64, io, json, os, re, shutil, subprocess, sys, tempfile, time
from pathlib import Path
from PIL import Image

sys.path.insert(0, str(Path(__file__).resolve().parent))
import perceptual  # noqa: E402
import rfb_common as C  # noqa: E402
import safe_render  # noqa: E402
import svg_safety  # noqa: E402
import validate_svg  # noqa: E402

HARNESS_VERSION = "2.1.0 (hardened; round 4 itself ran commit 6747499)"
MAX_RENDERS, MAX_TOOLCALLS, MAX_TURNS = 5, 12, 16
RECOVERY_TURNS = 2
DEFAULT_COST_CAP = 0.25
PY_TIMEOUT, PY_OUT = 20, 8000
MAX_FILE_READ = svg_safety.MAX_BYTES      # 300 KB, same as the file contract and the sanitizer

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


def normalize_svg(text):
    """Used for BOTH the rendered copy and the delivered copy: per-attribute fixes, strip title/desc/metadata.
    (Text-level helper only; it is never a security measure. Safety comes from svg_safety.sanitize().)"""
    text = C.normalize_svg_head(text)
    return re.sub(r"\s*<(title|desc|metadata)\b.*?</\1>", "", text, flags=re.S)


def element_table(svg_text):
    """Per-element bounding boxes (page units) and where they land after the half-turn, measured by Chrome in
    the sandbox on the sanitized SVG."""
    rows = safe_render.element_boxes(svg_text)
    if rows is None:
        return "(element table unavailable)"
    rows.sort(key=lambda r: -r["area"])
    lines = ["largest elements: bbox on the page (x0,y0,x1,y1) -> bbox as it appears in B after the half-turn"]
    for r in rows[:12]:
        x0, y0, x1, y1 = r["box"]
        lines.append(f"  {r['label']}: [{x0},{y0},{x1},{y1}] -> [{1000-x1},{1000-y1},{1000-x0},{1000-y0}]")
    if len(rows) > 12:
        lines.append(f"  (+{len(rows)-12} smaller elements)")
    return "\n".join(lines)


def diagnostics(norm_text, up, findings):
    """Text shown to the model. Structural facts (validator) are kept apart from perceptual hints."""
    errors, warnings, info = validate_svg.check_bytes(norm_text.encode("utf-8"))
    plines, rho = perceptual.lines(up)
    lines = [f"file: {round(len(norm_text.encode('utf-8')) / 1024, 1)} KB",
             "contract problems: " + ("none" if not errors else "; ".join(errors)),
             f"has <title>/<desc>: {info.get('has_title_or_desc')}"]
    other = [w for w in warnings if "<title>" not in w and "<desc>" not in w]
    if other:
        lines.append("warnings: " + "; ".join(other))
    removed = [f for f in findings if f.severity == "error"]
    if removed:
        lines.append("NOTE: the safe renderer removed disallowed parts BEFORE drawing; the picture does not show them: "
                     + "; ".join(f.message for f in removed[:6]))
    lines += plines
    try:
        lines.append(element_table(norm_text))
    except Exception as e:
        lines.append(f"(element table failed: {e})")
    return "\n".join(lines), rho


def run_python(code, work):
    if not shutil.which("bwrap"):
        return "run_python unavailable: bubblewrap is not installed on the host"
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


def png_b64(img):
    b = io.BytesIO()
    img.save(b, "PNG", optimize=True)
    return base64.b64encode(b.getvalue()).decode(), b.getvalue()


HARNESS = "[harness output, not a person] "
DELIVER = ("[harness] Deliver now, without calling a tool, in the final format: an `EVENT:` line, a `TITLE:` line, "
           "then the complete SVG in one ```xml block.")


def parse_args(argv):
    ap = argparse.ArgumentParser(description="Round 4 tool-augmented runner (one model per invocation).")
    ap.add_argument("out_dir")
    ap.add_argument("prompt_file")
    ap.add_argument("model")
    ap.add_argument("--timestamped", action="store_true", help="write into OUT_DIR/<model>/<YYYYmmdd-HHMMSS>")
    ap.add_argument("--force", action="store_true", help="allow writing into a non-empty directory (overwrites)")
    ap.add_argument("--mock", action="store_true",
                    help="offline smoke test: scripted fake API, no network, no key, no cost")
    ap.add_argument("--mock-svg", choices=["benign", "hostile"], default="benign",
                    help="with --mock: the SVG the fake model writes (hostile = scripts, external refs, animation)")
    return ap.parse_args(argv)


def main(argv=None, transport=None):
    args = parse_args(sys.argv[1:] if argv is None else argv)
    out_root, prompt_file, model = Path(args.out_dir), Path(args.prompt_file), args.model
    name = re.sub(r"[^A-Za-z0-9._-]", "_", model.split("/", 1)[-1])
    if args.mock:
        import mock_openrouter as M
        transport = transport or M.MockTransport(M.harness_script(M.hostile_svg() if args.mock_svg == "hostile" else None))
        key = "mock"
    else:
        key = os.environ.get("OPENROUTER_API_KEY")
        if not key:
            sys.exit("Set OPENROUTER_API_KEY in your environment.")
        transport = transport or C.http_transport
    out = C.prepare_out_dir(out_root / name, args.timestamped, args.force)
    work = out / "work"
    work.mkdir(parents=True, exist_ok=True)
    apilog = C.ApiLog(out / "api-errors.jsonl")
    reasoning = {"enabled": False} if os.environ.get("NOREASON") else {"effort": os.environ.get("EFFORT", "medium")}
    maxtok = int(os.environ.get("MAXTOK", "32000"))
    COST_CAP = float(os.environ.get("COST_CAP_USD", DEFAULT_COST_CAP))
    pin, pout, psrc = C.price_for(model, offline=bool(args.mock))
    budget = C.Budget(COST_CAP, pin, pout, psrc, tools=TOOLS)
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

    log("user_prompt", file=str(prompt_file), chars=len(msgs[0]["content"]), harness=HARNESS_VERSION,
        chrome=safe_render.chrome_version() if not args.mock else "mock", price_source=psrc)
    cost, ptok, ctok, renders, toolcalls, turns = 0.0, 0, 0, 0, 0, 0
    per_turn, final_text, last_svg_text, finish = [], None, None, None
    render_rho = []      # advisory symmetry number of each successful render, for the record
    force, forced_once, providers = False, False, set()
    t0 = time.time()

    while turns < MAX_TURNS + RECOVERY_TURNS and time.time() - t0 < 1800:
        mt, est = budget.plan(msgs, maxtok)
        if mt is None:
            finish = "cost_precheck_stop"
            log("harness", note="stopped before the call: even a minimal call could exceed the cost cap",
                estimate_usd=round(est, 6), spent=round(budget.spent, 6))
            break
        turns += 1
        body = {"model": model, "messages": msgs, "max_tokens": mt, "reasoning": reasoning, "usage": {"include": True}}
        if not force:
            body["tools"], body["tool_choice"] = TOOLS, "auto"
        r = C.call_api(key, body, apilog, transport=transport, sleep=0 if args.mock else 5, model=model, turn=turns)
        if not r:
            finish = "api_failure"
            break
        ch = r["choices"][0]
        m = ch["message"]
        u = r.get("usage", {})
        c = budget.record(turns, est, mt, u)     # reported cost; derived from tokens if the provider omits it
        cost += c
        ptok += u.get("prompt_tokens", 0) or 0
        ctok += u.get("completion_tokens", 0) or 0
        providers.add(str(r.get("provider")))
        det = (u.get("completion_tokens_details") or {})
        per_turn.append({"turn": turns, "prompt_tokens": u.get("prompt_tokens"), "completion_tokens": u.get("completion_tokens"),
                         "reasoning_tokens": det.get("reasoning_tokens"), "cost": c, "estimate_before_call": round(est, 6),
                         "max_tokens_used": mt, "finish": ch.get("finish_reason"),
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
            # empty / SVG-less answer: ask once more, forced, with the last rendered SVG available (recovery turn)
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
                targs = json.loads(tc["function"].get("arguments") or "{}")
            except Exception:
                targs = {}
            toolcalls += 1
            if toolcalls > MAX_TOOLCALLS:
                res = "TOOL LIMIT REACHED (12). Deliver now, without calling a tool."
            elif fn == "run_python":
                res = run_python(str(targs.get("code", "")), work)
            elif fn == "render_svg":
                if renders >= MAX_RENDERS:
                    res = "RENDER LIMIT REACHED (5). Deliver now, without calling a tool."
                else:
                    renders += 1
                    try:
                        if targs.get("svg"):
                            raw_text = targs["svg"]
                        else:
                            sp = (work / str(targs.get("path", ""))).resolve()
                            if work.resolve() not in sp.parents or not sp.is_file():
                                raise ValueError("path must be a file inside the working folder")
                            if sp.stat().st_size > MAX_FILE_READ:
                                raise ValueError("file is larger than 300 KB")
                            raw_text = sp.read_text(errors="replace")
                        norm = normalize_svg(raw_text)
                        # sanitize BEFORE any render; render only inside the sandbox
                        clean, findings = svg_safety.sanitize(norm)
                        up, rot, _ = safe_render.render_pair(norm)
                        txt, rho = diagnostics(norm, up, findings)
                        render_rho.append({"render": renders, "symmetry_rho": rho})
                        W = 500
                        comp = Image.new("RGB", (W * 2 + 30, W + 10), "white")
                        comp.paste(up, (5, 5)); comp.paste(rot, (W + 25, 5))
                        b64, raw = png_b64(comp)
                        (out / f"render-{renders}.png").write_bytes(raw)
                        (out / f"render-{renders}.original.svg").write_text(norm)
                        (out / f"render-{renders}.svg").write_text(clean)
                        last_svg_text = clean
                        images.append((renders, b64))
                        res = (f"render {renders}/{MAX_RENDERS}. Left image = A (upright), right image = B (rotated 180°). "
                               f"The image follows in the next message.\n{txt}")
                    except Exception as e:
                        renders -= 1  # a failed render does not use up a render
                        res = f"render failed (not counted): {e}"
            else:
                res = f"unknown tool {fn}"
            log("tool", turn=turns, name=fn, args=targs if fn != "run_python" else {"code": targs.get("code")}, result=res)
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
    rec = {"harness_version": HARNESS_VERSION, "model": model, "reasoning": reasoning, "max_tokens_per_turn": maxtok,
           "turns": turns, "tool_calls": toolcalls, "renders": renders, "prompt_tokens_total": ptok,
           "completion_tokens_total": ctok, "cost_usd": round(cost, 6), "cost_cap_usd": COST_CAP,
           "cost_overrun_usd": budget.overrun, "render_symmetry_rho": render_rho, "budget": budget.summary(), "finish": finish,
           "providers": sorted(providers), "api_failures_logged": apilog.count, "per_turn": per_turn,
           "event": ev.group(1).strip() if ev else None, "title": ti.group(1).strip() if ti else None,
           "seconds": round(time.time() - t0)}
    m = re.search(r"<svg\b.*?</svg>", text, re.S)
    if m:
        original = m.group(0)
        (out / f"{name}.original.svg").write_text(original)           # verbatim, never rendered unsandboxed
        try:
            norm = normalize_svg(original)
        except ValueError:
            norm = original
        delivered = '<?xml version="1.0" encoding="UTF-8"?>\n' + norm + "\n"
        (out / f"{name}.svg").write_text(delivered)
        rec["svg"], rec["svg_original"] = f"{name}.svg", f"{name}.original.svg"
        errors, warnings, _ = validate_svg.check_bytes(delivered.encode("utf-8"))
        rec["validator"] = {"errors": errors, "warnings": warnings, "passes_contract": not errors}
        rec["xml"] = "valid" if not any(e.startswith("invalid XML") for e in errors) else "INVALID"
        try:
            clean, findings = svg_safety.sanitize(delivered)
            (out / f"{name}.sanitized.svg").write_text(clean)
            rec["sanitizer_removed"] = [f.message for f in findings if f.severity == "error"]
        except svg_safety.SvgRejected as e:
            rec["sanitizer_rejected"] = e.message
    else:
        rec["svg"] = None
        if last_svg_text:
            rec["note"] = "no SVG in final answer; last rendered file kept as render-N.svg only (NOT delivered)"
    (out / "cost-log.json").write_text(json.dumps(rec, indent=1, ensure_ascii=False))
    print(name, {k: v for k, v in rec.items() if k not in ("per_turn", "budget")}, flush=True)
    return rec


if __name__ == "__main__":
    main()
