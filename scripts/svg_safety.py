# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Claudio Drews
"""Allowlist-based parsing, auditing and sanitizing of untrusted SVG (model output).

Model-written SVG is untrusted input. Nothing in this repository renders it before it has passed
through `sanitize()`, and rendering itself happens in a sandbox (see `safe_render.py`).

One walker (`_filter`) does both jobs, so the validator and the renderer agree:
  * `audit(data)`    -> findings (errors / warnings) for the validator;
  * `sanitize(data)` -> a rebuilt SVG that contains ONLY allowlisted elements and attributes.

Rejected outright (SvgRejected): a DTD, entity declarations, XML that does not parse, a root that is
not <svg> in the SVG namespace, too many elements, too deep nesting, <use> cycles or <use> expansion bombs.
Removed with an error finding: scripts, event attributes (on*), <foreignObject>, <image>, animation
(animate, animateTransform, animateMotion, set), any href / xlink:href that is not "#id", any url(...) that
is not url(#id), @import, javascript: values, CSS escapes, unknown elements, <a>, <iframe> and the like.
Removed with a warning: <style> (safe content only), <metadata>, unknown attributes, foreign-namespace
attributes (inkscape:, sodipodi:...).
Requires `defusedxml` (see requirements.txt).
"""
import re
from collections import namedtuple
from xml.etree.ElementTree import Element

try:
    import defusedxml.ElementTree as DET
    from defusedxml import DefusedXmlException
except ImportError as e:  # pragma: no cover
    raise SystemExit("defusedxml is required (pip install -r requirements.txt): " + str(e))

SVG_NS = "http://www.w3.org/2000/svg"
XLINK_NS = "http://www.w3.org/1999/xlink"
XML_NS = "http://www.w3.org/XML/1998/namespace"

MAX_BYTES = 300 * 1024          # the benchmark's file-size contract
MAX_ELEMENTS = 20000
MAX_DEPTH = 64
MAX_EXPANDED = 200000           # elements after expanding <use> references
MAX_ATTR_LEN = 300 * 1024

# Elements the SVG contract of the benchmark allows (plus title/desc, which are tolerated with a warning).
CONTRACT_ELEMENTS = {"svg", "g", "defs", "path", "circle", "ellipse", "rect", "line", "polyline", "polygon",
                     "use", "symbol", "clipPath", "mask", "title", "desc"}
# Harmless to draw, but forbidden by the contract ("no gradients"): kept by sanitize(), flagged by audit().
CONTRACT_FORBIDDEN_DRAWABLE = {"linearGradient", "radialGradient", "stop"}
SANITIZER_ELEMENTS = CONTRACT_ELEMENTS | CONTRACT_FORBIDDEN_DRAWABLE
# Names for clearer messages.
ANIMATION = {"animate", "animateTransform", "animateMotion", "animateColor", "set", "discard", "mpath"}
SCRIPTING = {"script", "foreignObject", "iframe", "object", "embed", "handler", "listener"}
EXTERNAL_CONTENT = {"image", "a", "video", "audio", "canvas", "feImage", "link"}
TEXTUAL = {"text", "tspan", "textPath", "tref", "font", "font-face", "glyph"}
FILTERS = {"filter", "feBlend", "feColorMatrix", "feComponentTransfer", "feComposite", "feConvolveMatrix",
           "feDiffuseLighting", "feDisplacementMap", "feDistantLight", "feDropShadow", "feFlood", "feFuncA",
           "feFuncB", "feFuncG", "feFuncR", "feGaussianBlur", "feMerge", "feMergeNode", "feMorphology",
           "feOffset", "fePointLight", "feSpecularLighting", "feSpotLight", "feTile", "feTurbulence"}

GEOMETRY_ATTRS = {"d", "cx", "cy", "r", "rx", "ry", "x", "y", "width", "height", "x1", "y1", "x2", "y2", "points",
                  "transform", "viewBox", "preserveAspectRatio", "id", "class", "version", "pathLength", "fx",
                  "fy", "offset", "gradientUnits", "gradientTransform", "spreadMethod", "clipPathUnits",
                  "maskUnits", "maskContentUnits"}
PRESENTATION_ATTRS = {"fill", "fill-opacity", "fill-rule", "stroke", "stroke-width", "stroke-opacity",
                      "stroke-linecap", "stroke-linejoin", "stroke-miterlimit", "stroke-dasharray",
                      "stroke-dashoffset", "opacity", "clip-path", "clip-rule", "mask", "display", "visibility",
                      "stop-color", "stop-opacity", "vector-effect", "paint-order", "shape-rendering", "color"}
ALLOWED_ATTRS = GEOMETRY_ATTRS | PRESENTATION_ATTRS | {"style"}
STYLE_PROPS = PRESENTATION_ATTRS

_ID = re.compile(r"^[A-Za-z0-9_][A-Za-z0-9_.:-]*$")      # digits allowed first: id="1" is legal output
_LOCAL_HREF = re.compile(r"^#[A-Za-z0-9_][A-Za-z0-9_.:-]*$")
_URL = re.compile(r"url\s*\(", re.I)
_LOCAL_URL = re.compile(r"url\(\s*(['\"]?)#[A-Za-z0-9_][A-Za-z0-9_.:-]*\1\s*\)", re.I)
_DOCTYPE = re.compile(rb"<!\s*(DOCTYPE|ENTITY|ELEMENT|ATTLIST|NOTATION)", re.I)
_BAD_SCHEME = re.compile(r"(javascript|vbscript|data|file|ftp|https?)\s*:", re.I)

Finding = namedtuple("Finding", "severity code message")


class SvgRejected(Exception):
    """The SVG cannot be processed safely (DTD/entities, parse failure, wrong root, size/expansion limits)."""

    def __init__(self, code, message):
        super().__init__(message)
        self.code, self.message = code, message


def local(tag):
    return tag.rsplit("}", 1)[-1] if isinstance(tag, str) else ""


def parse(data):
    """Parse bytes/str with defusedxml (no DTD, no entities, no external resolution). Returns the root Element."""
    if isinstance(data, str):
        if len(data) > MAX_BYTES:          # characters <= bytes, so this is checked before encoding a huge str
            raise SvgRejected("too-large", f"larger than 300 KB ({len(data)} characters)")
        data = data.encode("utf-8")
    if len(data) > MAX_BYTES:      # checked before any parsing; every caller (validator, sanitizer, renderers) goes through parse()
        raise SvgRejected("too-large", f"larger than 300 KB ({len(data)} bytes)")
    if _DOCTYPE.search(data):
        raise SvgRejected("dtd", "DTD / entity declarations are not allowed")
    try:
        root = DET.fromstring(data, forbid_dtd=True)
    except DefusedXmlException as e:
        raise SvgRejected("dtd", f"DTD / entities rejected: {e}")
    except Exception as e:  # xml.etree.ElementTree.ParseError and friends
        raise SvgRejected("xml", f"invalid XML: {e}")
    if root.tag != "{%s}svg" % SVG_NS:
        raise SvgRejected("namespace", "the root element must be <svg> in the namespace http://www.w3.org/2000/svg")
    return root


def _css_value_problem(value):
    """Return a reason string if a CSS/attribute value is unsafe, else None."""
    if "\\" in value:
        return "CSS escape sequence"
    if "@import" in value.lower() or "expression(" in value.lower():
        return "@import / expression()"
    for m in _URL.finditer(value):
        if not _LOCAL_URL.match(value[m.start():]):
            return "url() that is not url(#id)"
    if _BAD_SCHEME.search(value):
        return "URL scheme in value"
    if "/*" in value:
        return "CSS comment"
    return None


def _hidden(prop, val, findings, where):
    """Advisory: content a viewer cannot see passes the file contract, so say so."""
    v = val.strip().lower()
    hid = (prop == "display" and v == "none") or (prop == "visibility" and v in ("hidden", "collapse"))
    if prop in ("opacity", "fill-opacity", "stroke-opacity"):
        try:
            hid = float(v.rstrip("%")) == 0.0
        except ValueError:
            pass
    if hid:
        findings.append(Finding("warning", "hidden-content",
                                f"{where}: {prop}:{val.strip()} hides content from the viewer (contract-valid, but check it)"))


def _clean_style(value, findings, where):
    keep = []
    for decl in value.split(";"):
        if not decl.strip():
            continue
        prop, _, val = decl.partition(":")
        prop, val = prop.strip().lower(), val.strip()
        why = _css_value_problem(val) or _css_value_problem(prop)
        if why:
            findings.append(Finding("error", "unsafe-style", f"{where}: style declaration '{prop}' is not allowed ({why})"))
        elif prop in STYLE_PROPS:
            _hidden(prop, val, findings, where)
            keep.append(f"{prop}:{val}")
        else:
            findings.append(Finding("warning", "unsupported-style", f"{where}: style property '{prop}' ignored"))
    return ";".join(keep)


def _element_problem(name):
    if name in ANIMATION:
        return "error", "animation", f"animation element <{name}> is not allowed"
    if name in SCRIPTING:
        return "error", "scripting", f"<{name}> is not allowed (scripting / embedded content)"
    if name in EXTERNAL_CONTENT:
        return "error", "external-content", f"<{name}> is not allowed (external or embedded content)"
    if name in TEXTUAL:
        return "error", "forbidden-element", f"<{name}>: text is forbidden by the contract"
    if name in FILTERS:
        return "error", "forbidden-element", f"<{name}>: filters are forbidden by the contract"
    return None


def _filter(el, findings, depth, counter):
    """Return a rebuilt copy of `el` (or None if the element is dropped), appending findings."""
    name = local(el.tag)
    counter[0] += 1
    if counter[0] > MAX_ELEMENTS:
        raise SvgRejected("too-many-elements", f"more than {MAX_ELEMENTS} elements")
    if depth > MAX_DEPTH:
        raise SvgRejected("too-deep", f"nesting deeper than {MAX_DEPTH}")
    ns = el.tag[1:].split("}")[0] if el.tag.startswith("{") else ""
    if ns != SVG_NS:
        findings.append(Finding("error", "foreign-element", f"element <{name}> in namespace '{ns}' is not allowed"))
        return None
    if name == "metadata":
        findings.append(Finding("warning", "metadata", "<metadata> removed"))
        return None
    if name == "style":
        css = "".join(el.itertext())
        why = _css_value_problem(css)
        if why:
            findings.append(Finding("error", "unsafe-style", f"<style> is not allowed ({why})"))
        else:
            findings.append(Finding("warning", "style-element",
                                    "<style> is ignored by the safe renderer (use presentation attributes)"))
        return None
    if name not in SANITIZER_ELEMENTS:
        prob = _element_problem(name)
        findings.append(Finding(*prob) if prob else
                        Finding("error", "unsupported-element", f"<{name}> is not in the allowed element set"))
        return None
    if name in CONTRACT_FORBIDDEN_DRAWABLE:
        findings.append(Finding("error", "forbidden-element", f"<{name}>: gradients are forbidden by the contract"))
    if name in ("title", "desc"):
        findings.append(Finding("warning", "metadata", f"<{name}> present (the benchmark strips it from rounds 3 on)"))

    attrs = {}
    for k, v in el.attrib.items():
        an = local(k)
        ans = k[1:].split("}")[0] if k.startswith("{") else ""
        if an.lower().startswith("on"):
            findings.append(Finding("error", "event-attribute", f"<{name}>: event attribute '{an}' is not allowed"))
            continue
        if an == "href" and ans in ("", XLINK_NS):
            if name == "use" and _LOCAL_HREF.match(v.strip()):
                attrs["href"] = v.strip()
            else:
                findings.append(Finding("error", "external-reference",
                                        f"<{name}>: {an}={v[:60]!r} is not allowed (only href=\"#id\" on <use> is allowed)"))
            continue
        if ans not in ("", XML_NS) or (ans == XML_NS and an != "space"):
            findings.append(Finding("warning", "foreign-attribute", f"<{name}>: attribute '{an}' ({ans}) removed"))
            continue
        if ans == XML_NS:
            continue
        if an == "filter":
            findings.append(Finding("error", "forbidden-element", f"<{name}>: the filter attribute is forbidden"))
            continue
        if an not in ALLOWED_ATTRS:
            findings.append(Finding("warning", "unsupported-attribute", f"<{name}>: attribute '{an}' ignored"))
            continue
        if len(v) > MAX_ATTR_LEN:
            findings.append(Finding("error", "too-large", f"<{name}>: attribute '{an}' is too long"))
            continue
        if an == "style":
            s = _clean_style(v, findings, f"<{name}>")
            if s:
                attrs["style"] = s
            continue
        if an == "id" or an == "class":
            if an == "id" and not _ID.match(v):
                findings.append(Finding("warning", "bad-id", f"<{name}>: id {v[:40]!r} removed"))
                continue
            attrs[an] = v
            continue
        why = _css_value_problem(v)
        if why:
            code = "external-url" if "url()" in why else "unsafe-value"
            findings.append(Finding("error", code, f"<{name}>: attribute '{an}' is not allowed ({why})"))
            continue
        _hidden(an, v, findings, f"<{name}>")
        attrs[an] = v
    if name == "use" and "href" not in attrs:
        findings.append(Finding("error", "external-reference", "<use> without a local href=\"#id\" is not allowed"))
        return None

    new = Element(el.tag, attrs)
    if name in ("title", "desc"):
        new.text = (el.text or "")[:1000]
    for child in el:
        if not isinstance(child.tag, str):  # comments / processing instructions
            continue
        c = _filter(child, findings, depth + 1, counter)
        if c is not None:
            new.append(c)
    return new


def _check_use_expansion(root):
    ids = {}
    for el in root.iter():
        i = el.get("id")
        if i:
            ids.setdefault(i, el)
    memo, stack = {}, set()

    def size(el):
        key = id(el)
        if key in memo:
            return memo[key]
        if key in stack:
            raise SvgRejected("use-cycle", "<use> reference cycle")
        stack.add(key)
        n = 1
        for c in el:
            n += size(c)
        if local(el.tag) == "use":
            tgt = ids.get(el.get("href", "")[1:])
            if tgt is not None:
                n += size(tgt)
        stack.discard(key)
        memo[key] = n
        if n > MAX_EXPANDED:
            raise SvgRejected("use-bomb", f"<use> expansion exceeds {MAX_EXPANDED} elements")
        return n

    size(root)


def process(data):
    """Parse and filter. Returns (clean_root, findings). Raises SvgRejected."""
    root = parse(data)
    findings = []
    clean = _filter(root, findings, 0, [0])
    _check_use_expansion(clean)
    return clean, findings


def audit(data):
    """Findings for the validator. Never raises: a rejection becomes one error finding."""
    try:
        return process(data)[1]
    except SvgRejected as e:
        return [Finding("error", e.code, e.message)]


def _esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def serialize(el, root=True):
    """Serialize a (clean) tree without namespace prefixes, so the result is valid both as a standalone
    SVG file and as inline SVG inside an HTML page."""
    name = local(el.tag)
    parts = ["<" + name]
    if root:
        parts.append(f' xmlns="{SVG_NS}"')
    for k, v in el.attrib.items():
        parts.append(f' {k}="{_esc(v)}"')
    parts.append(">")
    if el.text:
        parts.append(_esc(el.text))
    for c in el:
        parts.append(serialize(c, False))
    parts.append(f"</{name}>")
    return "".join(parts)


def sanitize(data):
    """Return (clean_svg_text, findings). Raises SvgRejected if the input cannot be made safe."""
    root, findings = process(data)
    return '<?xml version="1.0" encoding="UTF-8"?>\n' + serialize(root) + "\n", findings
