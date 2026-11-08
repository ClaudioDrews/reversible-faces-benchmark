#!/usr/bin/env python3
"""
Render the site to a print-ready PDF.

Why: an HTML file transferred through a media channel can be opened by a
viewer that does not apply the stylesheet (the page then looks like an
unstyled skeleton). A PDF renders identically everywhere, so it can always
be compared with the preview images.

    python3 site-tools/build_pdf.py
    -> output/reversible-faces-site.pdf
"""
import sys
from pathlib import Path
from playwright.sync_api import sync_playwright

import os, shutil
CHROME = os.environ.get("CHROMIUM_BIN") or shutil.which("chromium") or shutil.which("google-chrome")
BASE = os.environ.get("RFB_BASE", "http://127.0.0.1:8811/index.html")
OUT = Path(__file__).resolve().parent.parent / "output" / "reversible-faces-site.pdf"

PRINT_CSS = """
@page { size: A4; margin: 14mm 12mm; }
* { -webkit-print-color-adjust: exact; print-color-adjust: exact; }
.site-nav, .to-top, .hero-hint, .play-dial, .lang-switch, .tabs { display: none !important; }
.section { padding: 10mm 0 0 !important; break-inside: auto; }
.section-alt { background: #faf7ee !important; }
.wrap { max-width: 100% !important; padding: 0 !important; }
.hero { padding-top: 0 !important; }
canvas { break-inside: avoid; }
.hero-stage, .card, .method-card, .run-card, .oq-list li, .skill-list li { break-inside: avoid; }
a { color: inherit; text-decoration: none; }
h1, h2, h3 { break-after: avoid; }
.oq-list, .skill-list, .run-grid { grid-template-columns: 1fr 1fr !important; }
img { max-width: 100% !important; }
"""


def main():
    with sync_playwright() as p:
        b = p.chromium.launch(executable_path=CHROME, args=["--no-sandbox", "--disable-dev-shm-usage"])
        pg = b.new_page(viewport={"width": 1240, "height": 1600})
        pg.goto(BASE + "?lang=pt", wait_until="networkidle")
        pg.wait_for_timeout(2600)
        pg.add_style_tag(content=PRINT_CSS)
        pg.emulate_media(media="print")
        pg.wait_for_timeout(1200)
        OUT.parent.mkdir(parents=True, exist_ok=True)
        pg.pdf(path=str(OUT), format="A4", print_background=True,
               margin={"top": "14mm", "bottom": "14mm", "left": "12mm", "right": "12mm"})
        b.close()
    print("pdf written: %s (%.2f MB)" % (OUT, OUT.stat().st_size / 1048576))


if __name__ == "__main__":
    sys.exit(main())
