# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Cláudio Drews
"""Render untrusted (model-written) SVG with headless Chrome/Chromium inside a bubblewrap sandbox.

Defence in depth, in this order:
  1. `svg_safety.sanitize()` rebuilds the SVG from an allowlist (no scripts, no event handlers, no external
     references, no DTD/entities). Nothing is rendered that has not passed through it.
  2. The sanitized SVG is embedded in a minimal HTML page with a Content-Security-Policy that forbids every
     network fetch (the only script is the harness's own, pinned by hash, and only in `element_boxes`).
  3. Chrome runs inside `bwrap`: all namespaces unshared (no network), all capabilities dropped, a clean
     environment, system directories mounted read-only, and ONLY a fresh temporary directory writable. The
     user's home, /workspace, credentials and API keys are not mounted or exported. Chrome's own sandbox is
     disabled (`--no-sandbox`) because it cannot nest inside bwrap; bwrap is the sandbox.
  4. Wall-clock timeout, CPU-time and file-size limits, and bounded input (300 KB, 20000 elements). There is no
     memory limit: Chrome reserves tens of GB of virtual address space, so `ulimit -v` breaks it (tested up to
     32 GB). Run the whole harness in a container with a memory limit if that matters to you.
If bwrap is missing or cannot start, rendering REFUSES to run (set RFB_ALLOW_UNSANDBOXED=1 only for SVG you
wrote yourself; this is never done by the harness).
"""
import base64
import hashlib
import html as htmllib
import json
import os
import re
import shutil
import subprocess
import tempfile
from pathlib import Path

from svg_safety import sanitize, serialize, process, SvgRejected  # noqa: F401  (re-exported for callers)

CHROME_NAMES = ("google-chrome", "chromium", "chromium-browser")
TIMEOUT = 60

BBOX_JS = """window.onload=function(){var out=[];var svg=document.querySelector('svg');var sc=1000/svg.getBoundingClientRect().width;
function add(el,label){var r=el.getBoundingClientRect();if(!r.width&&!r.height)return;
 var b=[r.left*sc,r.top*sc,r.right*sc,r.bottom*sc].map(Math.round);out.push({label:label,box:b,area:(b[2]-b[0])*(b[3]-b[1])});}
var kids=[].slice.call(svg.children);var i=0;
kids.forEach(function(k){var t=k.tagName.toLowerCase();i++;
 if(t==='g'){var rot=(k.getAttribute('transform')||'').indexOf('rotate')>=0;var j=0;
   [].slice.call(k.children).forEach(function(c){j++;add(c,'g'+i+(rot?'(rotated)':'')+'/'+c.tagName.toLowerCase()+j)});}
 else add(k,t+i);});
var pre=document.createElement('pre');pre.id='bboxes';pre.textContent=JSON.stringify(out);document.body.appendChild(pre);};"""


class RenderUnavailable(RuntimeError):
    pass


def chrome_path():
    for n in CHROME_NAMES:
        p = shutil.which(n)
        if p:
            return os.path.realpath(p)
    raise RenderUnavailable("no Chrome/Chromium found on PATH")


def chrome_version():
    try:
        return subprocess.run([chrome_path(), "--version"], capture_output=True, text=True, timeout=20).stdout.strip()
    except Exception as e:  # pragma: no cover
        return f"unknown ({e})"


def bwrap_path():
    return shutil.which("bwrap")


def sandbox_command(chrome, workdir, args):
    """The full command line: bwrap + Chrome. `workdir` is the only writable mount (as /work)."""
    cdir = str(Path(chrome).resolve().parent)
    cmd = [bwrap_path(), "--unshare-all", "--die-with-parent", "--new-session", "--cap-drop", "ALL", "--clearenv",
           "--uid", "65534", "--gid", "65534",      # Chrome never runs as (a mapped) uid 0
           "--ro-bind", "/usr", "/usr", "--symlink", "usr/lib", "/lib", "--symlink", "usr/lib64", "/lib64",
           "--symlink", "usr/bin", "/bin", "--symlink", "usr/sbin", "/sbin",
           "--ro-bind-try", "/etc/fonts", "/etc/fonts", "--ro-bind-try", "/etc/ld.so.cache", "/etc/ld.so.cache",
           "--proc", "/proc", "--dev", "/dev", "--tmpfs", "/tmp", "--tmpfs", "/dev/shm",
           "--bind", str(workdir), "/work", "--chdir", "/work",
           "--setenv", "HOME", "/work/home", "--setenv", "PATH", "/usr/bin",
           "--setenv", "XDG_CONFIG_HOME", "/work/home", "--setenv", "XDG_CACHE_HOME", "/work/home"]
    if not cdir.startswith("/usr"):
        cmd += ["--ro-bind", cdir, cdir]
    cmd += ["--remount-ro", "/"]          # the (tmpfs) root is read-only too; only /work and /tmp are writable
    inner = f"ulimit -t 90; ulimit -f 100000; exec {shlex_join([chrome] + args)}"
    return cmd + ["bash", "-c", inner]


def shlex_join(parts):
    import shlex
    return " ".join(shlex.quote(p) for p in parts)


CHROME_FLAGS = ["--headless", "--no-sandbox", "--disable-gpu", "--disable-dev-shm-usage", "--hide-scrollbars",
                "--force-device-scale-factor=1", "--disable-extensions", "--disable-background-networking",
                "--disable-sync", "--no-first-run", "--no-default-browser-check", "--mute-audio",
                "--host-resolver-rules=MAP * ~NOTFOUND", "--virtual-time-budget=3000",
                "--run-all-compositor-stages-before-draw"]


def _run_chrome(workdir, args):
    chrome = chrome_path()
    (Path(workdir) / "home").mkdir(exist_ok=True)
    if bwrap_path():
        cmd = sandbox_command(chrome, workdir, CHROME_FLAGS + args)
        env = {"PATH": "/usr/bin:/bin"}
    elif os.environ.get("RFB_ALLOW_UNSANDBOXED") == "1":
        cmd = [chrome] + CHROME_FLAGS + args
        env = {"PATH": os.environ.get("PATH", ""), "HOME": str(workdir), "XDG_CONFIG_HOME": str(workdir),
               "XDG_CACHE_HOME": str(workdir)}
    else:
        raise RenderUnavailable("bubblewrap (bwrap) is required to render untrusted SVG; refusing to run Chrome "
                                "unsandboxed (RFB_ALLOW_UNSANDBOXED=1 overrides this for SVG you wrote yourself)")
    p = subprocess.run(cmd, capture_output=True, text=True, timeout=TIMEOUT, env=env)
    return p


def _page(body, csp):
    return ('<!doctype html><html><head><meta charset="utf-8">'
            f'<meta http-equiv="Content-Security-Policy" content="{htmllib.escape(csp, quote=True)}">'
            f'</head><body style="margin:0;background:#fff">{body}</body></html>')


def render_png(svg_text, size=500):
    """Sanitize, then render upright at size x size. Returns (PIL image, sanitize findings)."""
    from PIL import Image
    clean, findings = sanitize(svg_text)
    uri = "data:image/svg+xml;base64," + base64.b64encode(clean.encode()).decode()
    page = _page(f'<img src="{uri}" width="{size}" height="{size}" style="display:block">',
                 "default-src 'none'; img-src data:; style-src 'unsafe-inline'")
    with tempfile.TemporaryDirectory(prefix="rfb-render-") as tmp:
        os.chmod(tmp, 0o777)
        (Path(tmp) / "p.html").write_text(page)
        p = _run_chrome(tmp, [f"--screenshot=/work/up.png", f"--window-size={size},{size}", "file:///work/p.html"])
        shot = Path(tmp) / "up.png"
        if not shot.exists():
            raise RuntimeError("render failed: " + (p.stderr or "")[-300:])
        im = Image.open(shot).convert("RGB")
        im.load()
    if im.size != (size, size):
        im = im.crop((0, 0, size, size)) if min(im.size) >= size else im.resize((size, size))
    return im, findings


def render_pair(svg_text, size=500):
    """(upright, rotated 180 degrees, findings)."""
    up, findings = render_png(svg_text, size)
    return up, up.rotate(180), findings


def element_boxes(svg_text, size=500):
    """Per-element bounding boxes in page units (0..1000), measured by Chrome on the sanitized SVG."""
    clean_root, _ = process(svg_text)
    clean = serialize(clean_root)
    clean = clean.replace("<svg", f'<svg style="width:{size}px;height:{size}px;display:block"', 1)
    digest = base64.b64encode(hashlib.sha256(BBOX_JS.encode()).digest()).decode()
    csp = f"default-src 'none'; style-src 'unsafe-inline'; script-src 'sha256-{digest}'"
    page = _page(clean + f"<script>{BBOX_JS}</script>", csp)
    with tempfile.TemporaryDirectory(prefix="rfb-bbox-") as tmp:
        os.chmod(tmp, 0o777)
        (Path(tmp) / "b.html").write_text(page)
        p = _run_chrome(tmp, [f"--window-size={size},{size}", "--dump-dom", "file:///work/b.html"])
    m = re.search(r'<pre id="bboxes">(.*?)</pre>', p.stdout, re.S)
    if not m:
        return None
    return json.loads(htmllib.unescape(m.group(1)))


def side_by_side(svg_path_or_text, out_png, size=500):
    """README-style preview: A (upright) and B (rotated 180 degrees) with labels."""
    from PIL import Image, ImageDraw
    text = svg_path_or_text
    if "<" not in str(text):
        text = Path(text).read_bytes()
    im, rot, _ = render_pair(text, size)
    pad, label_h = 12, 28
    canvas = Image.new("RGB", (size * 2 + pad * 3, size + label_h + pad * 2), "white")
    d = ImageDraw.Draw(canvas)
    canvas.paste(im, (pad, label_h + pad))
    canvas.paste(rot, (size + pad * 2, label_h + pad))
    d.text((pad, pad), "A: as drawn (upright)", fill="black")
    d.text((size + pad * 2, pad), "B: rotated 180 degrees", fill="black")
    canvas.save(out_png)
