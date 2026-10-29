# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Cláudio Drews
"""The validator: valid fixtures pass; every invalid fixture fails for the expected reason, including the three
cases of the external pre-publication review (external <use href>, 12x23 dimensions, SVG animation)."""
import json
import subprocess
import sys
import unittest

from _common import FIXTURES, ROOT, SCRIPTS
import validate_svg as V

# fixture name -> substring that must appear in at least one error
EXPECTED = {
    "use_external_href": "only href=\"#id\"",           # reviewer case 1
    "use_xlink_external": "only href=\"#id\"",
    "dimensions_12x23": "width is '12'",                 # reviewer case 2
    "missing_dimensions": "missing width",
    "bad_viewbox": "viewBox",
    "animation_animate": "animation element <animate>",   # reviewer case 3
    "animation_set": "animation element <set>",
    "animation_transform": "animation element <animateTransform>",
    "script_element": "<script>",
    "event_attribute": "event attribute 'onload'",
    "foreignobject": "<foreignObject>",
    "image_element": "<image>",
    "css_import_style_element": "@import",
    "style_attr_external_url": "url() that is not url(#id)",
    "fill_external_url": "url() that is not url(#id)",
    "javascript_value": "URL scheme",
    "css_escape": "CSS escape",
    "doctype_entity": "DTD",
    "external_entity": "DTD",
    "text_element": "text is forbidden",
    "gradient": "gradients are forbidden",
    "filter_blur": "filters are forbidden",
    "not_svg_root": "root element must be <svg>",
    "wrong_namespace": "root element must be <svg>",
    "xml_stylesheet": "processing instruction",
    "use_cycle": "cycle",
    "use_bomb": "expansion",
    "not_xml": "invalid XML",
    "a_link": "<a>",
    "width_decimal": "expected exactly",
}


class ValidSvg(unittest.TestCase):
    def test_valid_fixtures_pass(self):
        for p in sorted((FIXTURES / "valid").glob("*.svg")):
            with self.subTest(p.name):
                errors, warnings, _ = V.check_bytes(p.read_bytes())
                self.assertEqual(errors, [])

    def test_hidden_content_is_a_warning(self):
        errors, warnings, _ = V.check_bytes((FIXTURES / "valid" / "hidden_content_warning.svg").read_bytes())
        self.assertEqual(errors, [])
        self.assertEqual(len([w for w in warnings if "hides content" in w]), 2)

    def test_numeric_ids_are_legal(self):
        errors, warnings, _ = V.check_bytes((FIXTURES / "valid" / "numeric_ids.svg").read_bytes())
        self.assertEqual((errors, warnings), ([], []))

    def test_title_desc_is_a_warning_not_an_error(self):
        errors, warnings, info = V.check_bytes((FIXTURES / "valid" / "title_desc_warning.svg").read_bytes())
        self.assertEqual(errors, [])
        self.assertTrue(info["has_title_or_desc"])
        self.assertTrue(warnings)


class InvalidSvg(unittest.TestCase):
    def test_every_invalid_fixture_has_an_expectation(self):
        names = {p.stem for p in (FIXTURES / "invalid").glob("*.svg")}
        self.assertEqual(names, set(EXPECTED), "add/remove entries in EXPECTED to match the fixtures")

    def test_invalid_fixtures_fail_for_the_expected_reason(self):
        for name, needle in EXPECTED.items():
            with self.subTest(name):
                errors, _, _ = V.check_bytes((FIXTURES / "invalid" / f"{name}.svg").read_bytes())
                self.assertTrue(errors, f"{name} should fail")
                self.assertTrue(any(needle in e for e in errors), f"{name}: {needle!r} not in {errors}")

    def test_reviewer_case_use_external_href(self):
        data = (b'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 1000" width="1000" height="1000">'
                b'<use href="https://example.com/x.svg#a"/></svg>')
        self.assertTrue(V.check_bytes(data)[0])

    def test_reviewer_case_12x23(self):
        data = (b'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 1000" width="12" height="23">'
                b'<circle cx="5" cy="5" r="3"/></svg>')
        errors = V.check_bytes(data)[0]
        self.assertTrue(any("width" in e for e in errors) and any("height" in e for e in errors))

    def test_reviewer_case_animation(self):
        data = (b'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 1000" width="1000" height="1000">'
                b'<circle r="5"><animate attributeName="r" to="500" dur="1s"/></circle></svg>')
        self.assertTrue(any("animation" in e for e in V.check_bytes(data)[0]))

    def test_oversize(self):
        pad = b"<!--" + b"x" * (301 * 1024) + b"-->"
        data = (b'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 1000" width="1000" height="1000">'
                + pad + b"</svg>")
        self.assertTrue(any("300 KB" in e for e in V.check_bytes(data)[0]))
        # and the sanitizer / renderer path refuses it too, before parsing
        import svg_safety
        with self.assertRaises(svg_safety.SvgRejected):
            svg_safety.sanitize(data)

    def test_unit_suffix_is_not_exact(self):
        data = (b'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 1000" width="1000px" height="1000px">'
                b'<circle r="5"/></svg>')
        self.assertTrue(V.check_bytes(data)[0])


class Cli(unittest.TestCase):
    def run_cli(self, *args):
        return subprocess.run([sys.executable, str(SCRIPTS / "validate_svg.py"), *args], capture_output=True, text=True)

    def test_exit_codes(self):
        ok = self.run_cli(str(FIXTURES / "valid" / "minimal.svg"))
        bad = self.run_cli(str(FIXTURES / "invalid" / "dimensions_12x23.svg"))
        self.assertEqual(ok.returncode, 0)
        self.assertEqual(bad.returncode, 1)
        self.assertIn("FAIL", bad.stdout)

    def test_strict_fails_on_warnings(self):
        f = str(FIXTURES / "valid" / "title_desc_warning.svg")
        self.assertEqual(self.run_cli(f).returncode, 0)
        self.assertEqual(self.run_cli("--strict", f).returncode, 1)

    def test_json_output(self):
        out = self.run_cli("--json", str(FIXTURES / "invalid" / "script_element.svg"))
        data = json.loads(out.stdout)
        self.assertFalse(data[0]["ok"])
        self.assertTrue(data[0]["errors"])

    def test_backward_compatible_api(self):
        problems, info = V.check(FIXTURES / "valid" / "minimal.svg")
        self.assertEqual(problems, [])
        self.assertIn("has_title_or_desc", info)


if __name__ == "__main__":
    unittest.main()
