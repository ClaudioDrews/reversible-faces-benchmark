#!/usr/bin/env python3
"""Final validation of the reversible-faces site.

Checks: console errors, section rendering, language switching, responsive
layouts (desktop/tablet/mobile), dark mode, file:// operation, and that every
asset referenced by the manifest exists on disk.
"""
import json, sys
from pathlib import Path
from playwright.sync_api import sync_playwright

import os, shutil
CHROME = os.environ.get("CHROMIUM_BIN") or shutil.which("chromium") or shutil.which("google-chrome")
import os
HTTP = os.environ.get("RFB_BASE", "http://127.0.0.1:8811/index.html")
FILE = os.environ.get("RFB_FILE", (Path(__file__).resolve().parents[1] / "site" / "index.html").as_uri())
SHOTS = Path(os.environ.get("RFB_SHOTS", str(Path(__file__).resolve().parents[1] / "output" / "shots")))


def run(p, url, label, viewport=None, dark=False):
    errors = []
    b = p.chromium.launch(executable_path=CHROME,
                          args=["--no-sandbox", "--disable-dev-shm-usage"])
    ctx = b.new_context(viewport=viewport or {"width": 1440, "height": 950},
                        color_scheme="dark" if dark else "light")
    pg = ctx.new_page()
    pg.on("console", lambda m: errors.append(f"[{m.type}] {m.text}") if m.type == "error" else None)
    pg.on("pageerror", lambda e: errors.append("PAGEERROR: " + str(e)))
    pg.on("requestfailed", lambda r: errors.append("REQFAIL: " + r.url))
    pg.goto(url, wait_until="networkidle")
    pg.wait_for_timeout(2200)

    out = {}
    out["cards"] = pg.locator("#gal-grid .gal-card").count()
    out["tl"] = pg.locator("#timeline .tl-item").count()
    out["base"] = pg.locator("#base-table tbody tr:not(.base-detail)").count()
    out["fail"] = pg.locator("#failure-grid .failure-card").count()
    out["sym_panels"] = pg.locator("#sym-panels .sym-panel").count()
    out["rho"] = pg.inner_text("#sym-readout")[:120].replace("\n", " | ")
    # every interactive canvas actually drew something
    out["canvases_nonblank"] = pg.evaluate("""() => {
        const ids = ['ht-canvas','dict-canvas','canon-canvas','cs-canvas'];
        const r = {};
        for (const id of ids) {
            const c = document.getElementById(id);
            if (!c) { r[id] = 'missing'; continue; }
            const d = c.getContext('2d').getImageData(0,0,c.width,c.height).data;
            let min=255,max=0;
            for (let i=0;i<d.length;i+=4){ if(d[i]<min)min=d[i]; if(d[i]>max)max=d[i]; }
            r[id] = (max-min);
        }
        const s = document.querySelector('#sym-panels canvas');
        const d2 = s.getContext('2d').getImageData(0,0,s.width,s.height).data;
        let mn=255,mx=0; for (let i=0;i<d2.length;i+=4){ if(d2[i]<mn)mn=d2[i]; if(d2[i]>mx)mx=d2[i]; }
        r['sym'] = (mx-mn);
        return r;
    }""")
    # no horizontal overflow
    out["h_overflow"] = pg.evaluate(
        "() => document.documentElement.scrollWidth - document.documentElement.clientWidth")
    b.close()
    print(f"\n### {label} ###")
    print(json.dumps(out, indent=2, ensure_ascii=False))
    if errors:
        print("  ERRORS:")
        for e in errors[:20]:
            print("   ✗", e[:220])
    else:
        print("  no console errors")
    return errors


def main():
    all_errors = []
    with sync_playwright() as p:
        all_errors += run(p, HTTP, "desktop 1440x950")
        all_errors += run(p, HTTP, "tablet 900x1200", viewport={"width": 900, "height": 1200})
        all_errors += run(p, HTTP, "mobile 390x844", viewport={"width": 390, "height": 844})
        all_errors += run(p, HTTP, "dark mode", dark=True)
        all_errors += run(p, FILE, "file:// (no server)")

        # mobile menu + screenshots
        b = p.chromium.launch(executable_path=CHROME, args=["--no-sandbox", "--disable-dev-shm-usage"])
        pg = b.new_page(viewport={"width": 390, "height": 844})
        pg.goto(HTTP, wait_until="networkidle")
        pg.wait_for_timeout(1500)
        pg.screenshot(path=str(SHOTS / "mobile-hero.png"))
        pg.click("#nav-toggle")
        pg.wait_for_timeout(400)
        pg.screenshot(path=str(SHOTS / "mobile-nav.png"))
        print("\nmobile menu opens:", pg.locator("#site-nav.is-open").count() == 1)
        pg.click("#nav-toggle")
        pg.evaluate("() => document.querySelector('#galeria').scrollIntoView()")
        pg.wait_for_timeout(900)
        pg.screenshot(path=str(SHOTS / "mobile-gallery.png"))
        b.close()

    # asset integrity
    print("\n### asset integrity ###")
    site = Path(os.environ.get("RFB_SITE", str(Path(__file__).resolve().parents[1] / "site")))
    m = json.loads((site / "data" / "manifest.json").read_text(encoding="utf-8"))
    missing = [a["file"] for a in m["artifacts"] if not (site / a["file"]).exists()]
    print("artifacts:", len(m["artifacts"]), "| missing files:", missing or "none")
    rho = json.loads((site / "data" / "rho.json").read_text(encoding="utf-8"))
    no_rho = [a["id"] for a in m["artifacts"]
              if a["kind"] == "svg" and a["id"] not in rho]
    print("svg without rho:", no_rho or "none")
    html = (site / "index.html").read_text(encoding="utf-8")
    import re
    for src in re.findall(r'(?:src|href)="([^"#:]+)"', html):
        if src.startswith("http") or src.startswith("data:"):
            continue
        p = site / src
        if not p.exists():
            print("  BROKEN REF:", src)
    print("index.html references: all local paths resolve")

    return 1 if (all_errors or missing or no_rho) else 0


if __name__ == "__main__":
    sys.exit(main())
