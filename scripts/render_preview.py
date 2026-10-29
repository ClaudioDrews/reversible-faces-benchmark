#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Claudio Drews
"""Render a side-by-side preview of an SVG: upright (A) and rotated 180 degrees (B).

Usage: python scripts/render_preview.py in.svg out.png [--size 500]

The SVG is treated as UNTRUSTED: it is rebuilt by `svg_safety.sanitize()` (allowlist; scripts, event handlers,
external references, DTD/entities are removed or rejected) and rendered by headless Chrome/Chromium inside a
bubblewrap sandbox with no network and only a temporary directory writable (see `safe_render.py`).
Requires Pillow, defusedxml, bubblewrap and Chrome/Chromium. If bubblewrap is missing the script refuses to
run. The preview is for README illustration only; the benchmark's judgment is made by a human looking at the
SVG itself. Rendering may differ slightly between Chrome versions and platforms (see docs/reproduction.md).
"""
import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import safe_render  # noqa: E402
import svg_safety  # noqa: E402


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("svg")
    ap.add_argument("out")
    ap.add_argument("--size", type=int, default=500)
    a = ap.parse_args()
    try:
        safe_render.side_by_side(Path(a.svg).read_bytes(), a.out, a.size)
    except svg_safety.SvgRejected as e:
        sys.exit(f"refusing to render: {e.message}")
    except safe_render.RenderUnavailable as e:
        sys.exit(str(e))


if __name__ == "__main__":
    main()
