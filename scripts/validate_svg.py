#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Claudio Drews
"""Validate that an SVG meets the benchmark's FILE CONTRACT and is safe to handle. Structure only.

Usage: python scripts/validate_svg.py [--strict] [--json] file.svg [file2.svg ...]
Exit status: 0 if every file has no errors (and, with --strict, no warnings); 1 otherwise.

ERRORS (the file fails the contract):
  * size > 300 KB; not valid XML; a DTD or entity declaration; root is not <svg> in the SVG namespace;
  * viewBox is not exactly "0 0 1000 1000"; width and height are not exactly "1000" (so 12x23 fails);
  * a forbidden element: <text>, <image>, <foreignObject>, <script>, gradients, filters;
  * animation (<animate>, <animateTransform>, <animateMotion>, <set>, ...);
  * any event attribute (on*), any href / xlink:href that is not "#id" on <use>, any url(...) that is not
    url(#id), @import, javascript:/data: values, CSS escapes; unknown elements; too many/too deep elements;
    <use> cycles and expansion bombs.
WARNINGS (reported, do not fail unless --strict): <title>/<desc> (the benchmark strips them from round 3 on),
  <metadata>, a <style> element, unknown or foreign-namespace attributes.

This module does NOT judge how the drawing looks (reversibility, symmetry, quality): that is done by a human;
the harness's perceptual diagnostics are in `perceptual.py` and are advisory only.
The same allowlist drives `svg_safety.sanitize()`, which every renderer in this repository uses.
"""
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import svg_safety as S  # noqa: E402

EXPECTED_VIEWBOX = ["0", "0", "1000", "1000"]
EXPECTED_SIZE = "1000"
_PI = re.compile(rb"<\?(?!xml[\s?])", re.I)


def check_bytes(data):
    """Return (errors, warnings, info) for raw file bytes. Pure structure."""
    errors, warnings, info = [], [], {"has_title_or_desc": False}
    if _PI.search(data):
        errors.append("processing instruction other than the XML declaration (e.g. xml-stylesheet)")
    try:
        root = S.parse(data)
    except S.SvgRejected as e:
        errors.append(e.message)
        return errors, warnings, info
    vb = root.get("viewBox", "").replace(",", " ").split()
    if vb != EXPECTED_VIEWBOX:
        errors.append(f"viewBox is {root.get('viewBox')!r}, expected '0 0 1000 1000'")
    for dim in ("width", "height"):
        v = root.get(dim)
        if v is None:
            errors.append(f"missing {dim} (expected {dim}=\"1000\")")
        elif v.strip() != EXPECTED_SIZE:
            errors.append(f"{dim} is {v!r}, expected exactly \"1000\"")
    for f in S.audit(data):
        (errors if f.severity == "error" else warnings).append(f.message)
        if f.code == "metadata" and ("<title>" in f.message or "<desc>" in f.message):
            info["has_title_or_desc"] = True
    # preserve order, drop duplicates
    errors = list(dict.fromkeys(errors))
    warnings = list(dict.fromkeys(warnings))
    return errors, warnings, info


def check(path):
    """Backward-compatible API: (problems, info). `problems` are errors only; warnings are in info['warnings']."""
    errors, warnings, info = check_bytes(Path(path).read_bytes())
    info["warnings"] = warnings
    return errors, info


def main(argv):
    strict = "--strict" in argv
    as_json = "--json" in argv
    paths = [a for a in argv if not a.startswith("--")]
    if not paths:
        sys.exit(__doc__)
    status, results = 0, []
    for p in paths:
        errors, warnings, info = check_bytes(Path(p).read_bytes())
        failed = bool(errors) or (strict and bool(warnings))
        status |= failed
        results.append({"file": p, "ok": not failed, "errors": errors, "warnings": warnings})
        if not as_json:
            print(f"{'FAIL' if failed else 'OK  '} {p}")
            for e in errors:
                print("     - ERROR:", e)
            for w in warnings:
                print("     - warning:", w)
    if as_json:
        print(json.dumps(results, indent=1))
    return status


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
