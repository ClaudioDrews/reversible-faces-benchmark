# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Claudio Drews
"""The sanitizer: what comes out contains only allowlisted content, whatever goes in."""
import re
import unittest

from _common import FIXTURES, ROOT
import svg_safety as S
from mock_openrouter import hostile_svg, benign_svg

NS_DECL = 'xmlns="http://www.w3.org/2000/svg"'


def body(clean):
    """The sanitized text without the one legitimate URL, the SVG namespace declaration."""
    return clean.replace(NS_DECL, "")


DANGEROUS = [r"<script", r"\bon[a-z]+\s*=", r"foreignObject", r"<image", r"<animate", r"<set\b", r"example\.(com|invalid)",
             r"https?:", r"javascript:", r"<!DOCTYPE", r"<!ENTITY", r"@import", r"xlink:href", r"<a\b"]


class Sanitize(unittest.TestCase):
    def test_hostile_svg_is_neutralized(self):
        clean, findings = S.sanitize(hostile_svg())
        for pat in DANGEROUS:
            self.assertIsNone(re.search(pat, body(clean), re.I), f"{pat} survived: {clean}")
        # allowed drawing content survives
        self.assertIn("<path", clean)
        self.assertIn("<rect", clean)
        self.assertTrue(any(f.severity == "error" for f in findings))

    def test_every_invalid_fixture_is_either_rejected_or_clean(self):
        for p in sorted((FIXTURES / "invalid").glob("*.svg")):
            with self.subTest(p.name):
                try:
                    clean, _ = S.sanitize(p.read_bytes())
                except S.SvgRejected:
                    continue
                for pat in DANGEROUS:
                    self.assertIsNone(re.search(pat, body(clean), re.I), f"{p.name}: {pat} survived")

    def test_output_is_valid_and_idempotent(self):
        clean, _ = S.sanitize(hostile_svg())
        again, findings = S.sanitize(clean)
        self.assertEqual(clean, again)
        self.assertEqual([f for f in findings if f.severity == "error"], [])

    def test_benign_svg_is_unchanged_in_content(self):
        clean, findings = S.sanitize(benign_svg())
        self.assertEqual(findings, [])
        for tag in ("rect", "ellipse", "circle", "path"):
            self.assertIn("<" + tag, clean)

    def test_dtd_and_entities_are_rejected(self):
        for name in ("doctype_entity", "external_entity"):
            with self.assertRaises(S.SvgRejected) as cm:
                S.sanitize((FIXTURES / "invalid" / f"{name}.svg").read_bytes())
            self.assertEqual(cm.exception.code, "dtd")

    def test_use_bomb_and_cycle_are_rejected(self):
        for name, code in (("use_bomb", "use-bomb"), ("use_cycle", "use-cycle")):
            with self.assertRaises(S.SvgRejected) as cm:
                S.sanitize((FIXTURES / "invalid" / f"{name}.svg").read_bytes())
            self.assertEqual(cm.exception.code, code)

    def test_local_use_is_kept(self):
        clean, findings = S.sanitize((FIXTURES / "valid" / "local_use.svg").read_bytes())
        self.assertIn('href="#eye"', clean)
        self.assertEqual([f for f in findings if f.severity == "error"], [])

    def test_too_deep_and_too_many(self):
        deep = "<g>" * (S.MAX_DEPTH + 5) + "</g>" * (S.MAX_DEPTH + 5)
        with self.assertRaises(S.SvgRejected):
            S.sanitize('<svg xmlns="http://www.w3.org/2000/svg">' + deep + "</svg>")
        many = "<g/>" * (S.MAX_ELEMENTS + 5)
        with self.assertRaises(S.SvgRejected):
            S.sanitize('<svg xmlns="http://www.w3.org/2000/svg">' + many + "</svg>")

    def test_foreign_namespace_attributes_are_dropped(self):
        svg = ('<svg xmlns="http://www.w3.org/2000/svg" xmlns:inkscape="http://www.inkscape.org/namespaces/inkscape" '
               'viewBox="0 0 1000 1000" width="1000" height="1000"><g inkscape:label="x"><path d="M0 0L9 9"/></g></svg>')
        clean, findings = S.sanitize(svg)
        self.assertNotIn("inkscape", clean)
        self.assertTrue(any(f.code == "foreign-attribute" for f in findings))

    def test_existing_round_svgs_sanitize_without_errors(self):
        for p in sorted((ROOT / "rounds").rglob("*.svg")):
            with self.subTest(str(p.relative_to(ROOT))):
                _, findings = S.sanitize(p.read_bytes())
                self.assertEqual([f for f in findings if f.severity == "error"], [])


class SizeLimit(unittest.TestCase):
    def test_oversize_is_rejected_before_parsing_for_str_and_bytes(self):
        big = '<svg xmlns="http://www.w3.org/2000/svg">' + "<g/>" * 100000 + "</svg>"
        for data in (big, big.encode()):
            with self.assertRaises(S.SvgRejected) as cm:
                S.sanitize(data)
            self.assertEqual(cm.exception.code, "too-large")


if __name__ == "__main__":
    unittest.main()
