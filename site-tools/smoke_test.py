#!/usr/bin/env python3
"""Smoke-test the site in headless Chromium: console errors, key interactions,
and full-page screenshots of every section."""
import sys, json, time
from pathlib import Path
from playwright.sync_api import sync_playwright

import os, shutil
CHROME = os.environ.get("CHROMIUM_BIN") or shutil.which("chromium") or shutil.which("google-chrome")
import os
BASE = os.environ.get("RFB_BASE", "http://127.0.0.1:8811/index.html")
SHOTS = Path(os.environ.get("RFB_SHOTS", str(Path(__file__).resolve().parents[1] / "output" / "shots")))

def main():
    SHOTS.mkdir(parents=True, exist_ok=True)
    errors, warnings, logs = [], [], []
    with sync_playwright() as p:
        b = p.chromium.launch(executable_path=CHROME,
                              args=["--no-sandbox", "--disable-dev-shm-usage"])
        pg = b.new_page(viewport={"width": 1440, "height": 950}, device_scale_factor=1)
        pg.on("console", lambda m: (
            errors.append(m.text) if m.type == "error"
            else warnings.append(m.text) if m.type == "warning" else None))
        pg.on("pageerror", lambda e: errors.append("PAGEERROR: " + str(e)))
        pg.on("requestfailed", lambda r: errors.append("REQFAIL: " + r.url + " " + str(r.failure)))

        pg.goto(BASE, wait_until="networkidle")
        pg.wait_for_timeout(2200)

        # --- structural assertions -------------------------------------
        checks = {}
        checks["gallery_cards"] = pg.locator("#gal-grid .gal-card").count()
        checks["pg_options"] = pg.locator("#pg-select option").count()
        checks["tl_items"] = pg.locator("#timeline .tl-item").count()
        checks["prompt_rows"] = pg.locator("#prompt-table tbody tr").count()
        checks["base_rows"] = pg.locator("#base-table tbody tr:not(.base-detail)").count()
        checks["failure_cards"] = pg.locator("#failure-grid .failure-card").count()
        checks["dict_rows"] = pg.locator("#dict-table tbody tr").count()
        checks["sym_panels"] = pg.locator("#sym-panels .sym-panel").count()
        checks["caveats"] = pg.locator("#caveat-list li").count()
        checks["judge_rows"] = pg.locator("#judge-chart .judge-row").count()

        # --- hero image actually loaded -------------------------------
        checks["hero_img_natural"] = pg.evaluate(
            "() => { const i=document.getElementById('hero-img'); return i ? i.naturalWidth : -1; }")
        checks["gal_img_loaded"] = pg.evaluate(
            "() => { const i=document.querySelector('#gal-grid .gal-thumb img'); return i ? i.naturalWidth : -1; }")

        # --- rotation works --------------------------------------------
        pg.evaluate("() => { document.getElementById('pg-range').value='90';"
                    "document.getElementById('pg-range').dispatchEvent(new Event('input')); }")
        pg.wait_for_timeout(400)
        checks["rot_css"] = pg.evaluate(
            "() => getComputedStyle(document.getElementById('pg-img')).transform")
        checks["angle_out"] = pg.inner_text("#pg-angle")

        # --- symmetry lab produced numbers ------------------------------
        pg.wait_for_timeout(1600)
        checks["sym_readout"] = pg.inner_text("#sym-readout")[:220].replace("\n", " | ")
        checks["sym_canvas_nonblank"] = pg.evaluate("""() => {
            const c = document.querySelector('#sym-panels .sym-panel canvas');
            if (!c) return -1;
            const d = c.getContext('2d').getImageData(0,0,c.width,c.height).data;
            let min=255, max=0;
            for (let i=0;i<d.length;i+=4){ if(d[i]<min)min=d[i]; if(d[i]>max)max=d[i]; }
            return (max-min);
        }""")

        # --- split mode --------------------------------------------------
        pg.click("#pg-mode-split")
        pg.wait_for_timeout(300)
        checks["split_visible"] = pg.locator('.play-pane[data-pane="b"]').is_visible()

        # --- baselines detail row ---------------------------------------
        pg.locator("#base-table tbody tr:not(.base-detail)").first.click()
        pg.wait_for_timeout(500)
        checks["base_detail"] = pg.locator(".base-detail:not([hidden])").count()

        # --- language switch --------------------------------------------
        pg.click('.lang-switch button[data-lang="en"]')
        pg.wait_for_timeout(700)
        checks["en_nav"] = pg.inner_text(".site-nav a")[:40].replace("\n", " | ")
        pg.click('.lang-switch button[data-lang="pt"]')
        pg.wait_for_timeout(900)
        pg.evaluate("() => window.scrollTo(0,0)")
        pg.wait_for_timeout(400)

        # --- screenshots of every section --------------------------------
        pg.evaluate("() => window.scrollTo(0,0)")
        pg.wait_for_timeout(500)
        pg.screenshot(path=str(SHOTS / "00-hero.png"))
        for i, sel in enumerate(["#playground", "#galeria", "#geometria", "#simetria",
                                 "#rodadas", "#baselines", "#metodo"], start=1):
            pg.evaluate(f"() => document.querySelector('{sel}').scrollIntoView()")
            pg.wait_for_timeout(900)
            pg.screenshot(path=str(SHOTS / f"{i:02d}-{sel.strip('#')}.png"))

        # geometry tabs
        pg.evaluate("() => document.querySelector('#geometria').scrollIntoView()")
        for i, tab in enumerate(["dictionary", "canon", "compromise", "failures"], start=1):
            pg.click(f'.tab[data-tab="{tab}"]')
            pg.wait_for_timeout(800)
            pg.screenshot(path=str(SHOTS / f"10-geo-{tab}.png"))

        b.close()

    print(json.dumps(checks, indent=2, ensure_ascii=False))
    print("\n=== CONSOLE ERRORS ===")
    if errors:
        for e in errors[:40]:
            print(" ✗", e[:300])
    else:
        print(" none")
    print("\n=== WARNINGS ===")
    if warnings:
        for w in warnings[:15]:
            print(" !", w[:220])
    else:
        print(" none")
    return 1 if errors else 0

if __name__ == "__main__":
    sys.exit(main())
