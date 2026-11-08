#!/usr/bin/env python3
"""Render every benchmark SVG with headless Chrome and compute the advisory
symmetry diagnostic rho with the repository's OWN code (scripts/perceptual.py).

The rendered PNGs are copied into the site as static previews, so the site never
has to rasterize anything to show a thumbnail.

Usage: python3 site-tools/compute_rho.py [--repo /workspace/repo] [--site /workspace/site]
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from PIL import Image
from playwright.sync_api import sync_playwright

import os, shutil
CHROME = os.environ.get("CHROMIUM_BIN") or shutil.which("chromium") or shutil.which("google-chrome")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", default=str(Path(__file__).resolve().parents[1]))
    ap.add_argument("--site", default=str(Path(__file__).resolve().parents[1] / "site"))
    ap.add_argument("--size", type=int, default=1000)
    a = ap.parse_args()

    repo = Path(a.repo)
    site = Path(a.site)
    sys.path.insert(0, str(repo / "scripts"))
    import perceptual  # noqa: E402
    import svg_safety  # noqa: E402

    manifest_path = site / "data" / "manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    out_dir = site / "data" / "rendered"
    out_dir.mkdir(parents=True, exist_ok=True)

    targets = [x for x in manifest["artifacts"] if x["kind"] == "svg"]

    rendered: dict[str, Path] = {}
    with sync_playwright() as p:
        browser = p.chromium.launch(
            executable_path=CHROME,
            args=["--no-sandbox", "--disable-dev-shm-usage", "--force-device-scale-factor=1"],
        )
        page = browser.new_page(viewport={"width": a.size, "height": a.size},
                                device_scale_factor=1)
        for art in targets:
            src = repo / art["repoPath"]
            raw = src.read_bytes()
            try:
                clean, _findings = svg_safety.sanitize(raw)
                payload = clean
            except Exception as exc:  # noqa: BLE001
                print(f"  !! {art['id']}: sanitize refused ({exc}); rendering raw")
                payload = raw.decode("utf-8", "replace")
            html = (
                "<!doctype html><meta charset='utf-8'>"
                "<style>html,body{margin:0;padding:0;background:#fff}"
                "svg{display:block;width:100vw;height:100vh}</style>"
                + payload
            )
            page.set_content(html, wait_until="load")
            png_path = out_dir / f"{Path(art['file']).stem}.png"
            page.screenshot(path=str(png_path), omit_background=False)
            rendered[art["id"]] = png_path
        browser.close()

    summary = {}
    for art in targets:
        img = Image.open(rendered[art["id"]]).convert("RGB")
        rho, frac, bbox = perceptual.stats(img)
        summary[art["id"]] = {
            "rho": round(float(rho), 4),
            "nonwhite": round(float(frac), 4),
            "bbox": bbox,
        }
        print(f"  rho={rho:.4f}  ink={frac:.4f}  {art['id']}")

    (site / "data" / "rho.json").write_text(
        json.dumps(summary, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    print(f"\nwrote {site / 'data' / 'rho.json'} ({len(summary)} entries)")


if __name__ == "__main__":
    main()
