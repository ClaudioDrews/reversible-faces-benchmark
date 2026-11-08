#!/usr/bin/env python3
"""Capture screenshots of the key sections in both languages."""
import sys
from pathlib import Path
from playwright.sync_api import sync_playwright

import os, shutil
CHROME = os.environ.get("CHROMIUM_BIN") or shutil.which("chromium") or shutil.which("google-chrome")
BASE = os.environ.get("RFB_BASE", "http://127.0.0.1:8811/index.html")
SHOTS = Path(os.environ.get("RFB_SHOTS", str(Path(__file__).resolve().parents[1] / "output" / "shots")))

SECTIONS = [("hero", None), ("laboratorio", "#playground"), ("galeria", "#galeria"),
            ("geometria", "#geometria"), ("simetria", "#simetria"),
            ("rodadas", "#rodadas"), ("baselines", "#baselines"), ("metodo", "#metodo"),
            ("perguntas", "#perguntas"), ("rode", "#rode")]


def main():
    SHOTS.mkdir(parents=True, exist_ok=True)
    with sync_playwright() as p:
        b = p.chromium.launch(executable_path=CHROME, args=["--no-sandbox", "--disable-dev-shm-usage"])
        for lang in ("pt", "en"):
            pg = b.new_page(viewport={"width": 1440, "height": 950})
            pg.goto(f"{BASE}?lang={lang}", wait_until="networkidle")
            pg.wait_for_timeout(2200)
            for name, sel in SECTIONS:
                if sel:
                    pg.evaluate(f"() => document.querySelector('{sel}').scrollIntoView()")
                    pg.wait_for_timeout(800)
                pg.screenshot(path=str(SHOTS / f"{lang}-{name}.png"))
            # geometry tabs
            pg.evaluate("() => document.querySelector('#geometria').scrollIntoView()")
            for tab in ("dictionary", "canon", "compromise", "failures"):
                pg.click(f'.tab[data-tab="{tab}"]')
                pg.wait_for_timeout(700)
                pg.screenshot(path=str(SHOTS / f"{lang}-geo-{tab}.png"))
            pg.close()
        b.close()
    print("screenshots done")


if __name__ == "__main__":
    sys.exit(main())
