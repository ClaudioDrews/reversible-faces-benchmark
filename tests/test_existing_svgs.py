# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Cláudio Drews
"""Audit of the SVGs already in the repository against the CURRENT validator (documented in
docs/validator-audit.md). The files themselves are never modified."""
import unittest

from _common import ROOT
import validate_svg as V


class ExistingSvgs(unittest.TestCase):
    def results(self):
        out = {}
        for p in sorted((ROOT / "rounds").rglob("*.svg")):
            errors, warnings, _ = V.check_bytes(p.read_bytes())
            out[str(p.relative_to(ROOT))] = (errors, warnings)
        return out

    def test_counts(self):
        r = self.results()
        self.assertEqual(len(r), 18)

    def test_no_existing_svg_fails_the_new_validator(self):
        failing = {k: e for k, (e, w) in self.results().items() if e}
        self.assertEqual(failing, {})

    def test_only_round_2_has_warnings_and_they_are_title_desc(self):
        warned = {k: w for k, (e, w) in self.results().items() if w}
        self.assertEqual(sorted(warned), [
            "rounds/round-02/svg/deepseek-v4.1-flash_prompt-v4.svg",
            "rounds/round-02/svg/glm-5.3-flash_prompt-v4.svg",
            "rounds/round-02/svg/minimax-m3.1-flash_prompt-v4.svg"])
        for w in warned.values():
            self.assertTrue(all("<title>" in x or "<desc>" in x for x in w))


if __name__ == "__main__":
    unittest.main()
