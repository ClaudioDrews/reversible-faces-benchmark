#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Cláudio Drews
"""Render a side-by-side preview of an SVG: upright (A) and rotated 180 degrees (B).

Usage: python scripts/render_preview.py in.svg out.png [--size 500]

Requires Pillow and a headless Chrome/Chromium on PATH (google-chrome, chromium or
chromium-browser). The preview is for README illustration only; the benchmark's
judgment is always made by a human looking at the SVG itself.
"""
import argparse
import shutil
import subprocess
import tempfile
from pathlib import Path

from PIL import Image, ImageDraw


def chrome():
    for name in ("google-chrome", "chromium", "chromium-browser"):
        path = shutil.which(name)
        if path:
            return path
    raise SystemExit("No Chrome/Chromium found on PATH.")


def render(svg, png, size):
    with tempfile.TemporaryDirectory() as tmp:
        html = Path(tmp) / "p.html"
        html.write_text(f'<html><body style="margin:0"><img src="{Path(svg).resolve().as_uri()}" '
                        f'width="{size}" height="{size}"></body></html>')
        subprocess.run([chrome(), "--headless", "--no-sandbox", "--disable-gpu",
                        f"--screenshot={png}", f"--window-size={size},{size}", html.as_uri()],
                       check=True, capture_output=True)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("svg")
    ap.add_argument("out")
    ap.add_argument("--size", type=int, default=500)
    a = ap.parse_args()
    with tempfile.TemporaryDirectory() as tmp:
        up = Path(tmp) / "up.png"
        render(a.svg, str(up), a.size)
        im = Image.open(up).convert("RGB")
        rot = im.rotate(180)
        pad, label_h = 12, 28
        canvas = Image.new("RGB", (a.size * 2 + pad * 3, a.size + label_h + pad * 2), "white")
        d = ImageDraw.Draw(canvas)
        canvas.paste(im, (pad, label_h + pad))
        canvas.paste(rot, (a.size + pad * 2, label_h + pad))
        d.text((pad, pad), "A: as drawn (upright)", fill="black")
        d.text((a.size + pad * 2, pad), "B: rotated 180 degrees", fill="black")
        canvas.save(a.out)


if __name__ == "__main__":
    main()
