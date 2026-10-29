#!/usr/bin/env python3
"""Check that SVGs meet the benchmark's file contract.

Usage: python scripts/validate_svg.py file.svg [file2.svg ...]

Checks: valid XML, xmlns, viewBox="0 0 1000 1000", width/height, no forbidden
elements (text, image, foreignObject, script, gradients, filters), size <= 300 KB,
and reports whether <title>/<desc> metadata is present.
"""
import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

FORBIDDEN = {"text", "image", "foreignObject", "script", "linearGradient", "radialGradient", "filter"}


def check(path):
    problems = []
    data = Path(path).read_bytes()
    if len(data) > 300 * 1024:
        problems.append("larger than 300 KB")
    try:
        root = ET.fromstring(data)
    except ET.ParseError as e:
        return [f"invalid XML: {e}"], {}
    if root.tag != "{http://www.w3.org/2000/svg}svg":
        problems.append("missing xmlns http://www.w3.org/2000/svg")
    if root.get("viewBox", "").split() != ["0", "0", "1000", "1000"]:
        problems.append(f"viewBox is {root.get('viewBox')!r}, expected '0 0 1000 1000'")
    if not (root.get("width") and root.get("height")):
        problems.append("missing width/height")
    tags = {el.tag.split("}")[-1] for el in root.iter()}
    for bad in sorted(FORBIDDEN & tags):
        problems.append(f"forbidden element <{bad}>")
    return problems, {"has_title_or_desc": bool(tags & {"title", "desc"})}


if __name__ == "__main__":
    status = 0
    for p in sys.argv[1:]:
        problems, info = check(p)
        flag = "OK  " if not problems else "FAIL"
        extra = " (has <title>/<desc>)" if info.get("has_title_or_desc") else ""
        print(f"{flag} {p}{extra}")
        for pr in problems:
            print("     -", pr)
        status |= bool(problems)
    sys.exit(status)
