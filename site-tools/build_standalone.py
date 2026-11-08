#!/usr/bin/env python3
"""
Build a single-file, fully self-contained version of the site.

The folder build needs 9 sibling files (CSS + 8 scripts) plus 29 SVG and
4 JPEG assets. Opening `index.html` on its own therefore produces a broken
shell: every asset 404s and the page renders unstyled with no data.

This script folds everything into ONE .html file with zero external
requests, so the deliverable can be double-clicked and just work — also
from `file://`, where the symmetry lab still rasterises (the canvas reads
an inline data: URI, which is never tainted).

    python3 site-tools/build_standalone.py
    -> output/reversible-faces-site-standalone.html
"""

import base64
import json
import re
import sys
from pathlib import Path
from urllib.parse import quote

SITE = Path(__file__).resolve().parent.parent / "site"
OUT = Path(__file__).resolve().parent.parent / "output" / "reversible-faces-site-standalone.html"

# order matters: the page loads these in this sequence
JS_FILES = [
    "data/manifest.js",
    "data/rho.js",
    "data/art.js",
    "assets/js/i18n.js",
    "assets/js/rotator.js",
    "assets/js/geometry.js",
    "assets/js/symmetry.js",
    "assets/js/app.js",
]

# SVG sources already live in window.RFB_ART, so their URLs are rebuilt at
# runtime instead of being pasted here as megabytes of escaped text.
PATCH = """
/* ---- standalone build: resolve every artifact to an inline data URI ---- */
(function () {
  var enc = function (s) {
    return 'data:image/svg+xml;charset=utf-8,' + encodeURIComponent(s);
  };
  var raster = window.RFB_RASTER || {};
  var m = window.RFB_MANIFEST;
  if (!m) return;
  m.artifacts.forEach(function (a) {
    if (raster[a.file]) { a.file = raster[a.file]; return; }
    var src = (window.RFB_ART || {})[a.id];
    if (src) a.file = enc(src);
  });
})();
"""


def guard(text, closer):
    """Make sure an inlined payload cannot close its own host tag."""
    return text.replace(closer, "<\\/" + closer[1:])


def main():
    html = (SITE / "index.html").read_text(encoding="utf-8")

    # ---- 1. inline the stylesheet -------------------------------------
    css = (SITE / "assets/css/style.css").read_text(encoding="utf-8")
    css_tag = '<link rel="stylesheet" href="assets/css/style.css">'
    if css_tag not in html:
        print("!! could not find the stylesheet link")
        return 1
    html = html.replace(css_tag, "<style>\n" + guard(css, "</style>") + "\n</style>", 1)

    # ---- 2. inline the raster images as base64 data URIs --------------
    manifest = json.loads((SITE / "data/manifest.json").read_text(encoding="utf-8"))
    raster = {}
    for a in manifest["artifacts"]:
        if a.get("kind") == "raster":
            p = SITE / a["file"]
            if not p.exists():
                print("!! missing raster %s" % p)
                return 1
            mime = "image/jpeg" if p.suffix.lower() in (".jpg", ".jpeg") else "image/png"
            b64 = base64.b64encode(p.read_bytes()).decode("ascii")
            raster[a["file"]] = "data:%s;base64,%s" % (mime, b64)
    raster_js = "window.RFB_RASTER = " + json.dumps(raster) + ";\n"

    # ---- 3. insert the data-URI patch -------------------------------
    # It must run after manifest.js and art.js (it needs RFB_MANIFEST and
    # RFB_ART) but before app.js boots, so it goes immediately before the
    # app.js tag — while the tags still carry their src attributes.
    anchor = '<script src="assets/js/app.js"></script>'
    if anchor not in html:
        print("!! could not find the app.js script tag")
        return 1
    html = html.replace(
        anchor,
        "<script>\n" + raster_js + guard(PATCH, "</script>") + "\n</script>\n" + anchor,
        1,
    )

    # ---- 4. inline the scripts ----------------------------------------
    for rel in JS_FILES:
        src = (SITE / rel).read_text(encoding="utf-8")
        tag = '<script src="%s"></script>' % rel
        if tag not in html:
            print("!! could not find <script src=\"%s\">" % rel)
            return 1
        html = html.replace(tag, "<script>\n" + guard(src, "</script>") + "\n</script>", 1)

    # ---- 5. the static <img> tags (first paint, before JS runs) ------
    # index.html hard-codes three of them (hero-img, pg-img, pg-img-b) so
    # the page shows something before the manifest is parsed.
    for rel in sorted(set(re.findall(r'src="(data/art/[^"]+)"', html))):
        svg_path = SITE / rel
        if not svg_path.exists():
            print("!! missing %s" % svg_path)
            return 1
        uri = "data:image/svg+xml;charset=utf-8," + quote(
            svg_path.read_text(encoding="utf-8"), safe=""
        )
        html = html.replace('src="%s"' % rel, 'src="%s"' % uri)

    # ---- 6. no local requests left ------------------------------------
    # Scan only the markup outside <script>/<style>: the inlined JS and CSS
    # legitimately contain path-like strings (manifest fields, concatenations).
    markup = re.sub(r"<script\b[^>]*>.*?</script>", "<script></script>", html, flags=re.S)
    markup = re.sub(r"<style\b[^>]*>.*?</style>", "<style></style>", markup, flags=re.S)
    leftovers = re.findall(r'(?:src|href)="(?!https?:|data:|#|mailto:)([^"]+)"', markup)
    leftovers = [x for x in leftovers if not x.startswith("#")]
    if leftovers:
        print("!! still referencing local files:", leftovers[:8])
        return 1
    if re.search(r'src="data/art/', markup):
        print("!! a static artifact image was not inlined")
        return 1

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(html, encoding="utf-8")
    print("standalone written: %s (%.2f MB)" % (OUT, OUT.stat().st_size / 1048576))
    return 0


if __name__ == "__main__":
    sys.exit(main())
