# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Cláudio Drews
"""The baselines section: every baseline SVG meets the file contract, every baseline folder is documented
and has an evaluation, and the caveats that must travel with the numbers are present."""
import unittest

from _common import ROOT
import validate_svg as V

B = ROOT / "baselines"


class Baselines(unittest.TestCase):
    def test_eleven_svgs_pass_the_validator(self):
        svgs = sorted(B.glob("*-benchmark/*.svg"))
        self.assertEqual(len(svgs), 11)
        for p in svgs:
            errors, _w, _ = V.check_bytes(p.read_bytes())
            self.assertEqual(errors, [], p.name)

    def test_every_folder_has_readme_or_prompt_and_an_image(self):
        bench = sorted(B.glob("*-benchmark"))
        shared = sorted(B.glob("*-shared-eyes"))
        self.assertEqual((len(bench), len(shared)), (11, 4))
        for d in bench:
            self.assertTrue((d / "README.md").exists(), d.name)
            self.assertIn("## Evaluation", (d / "README.md").read_text(encoding="utf-8"), d.name)
        for d in shared:
            self.assertTrue((d / "prompt.md").exists(), d.name)
            self.assertTrue(list(d.glob("output*.jp*g")) or list(d.glob("output*.png")), d.name)

    def test_previews_exist_for_all_15(self):
        names = {p.name.split("__")[0] for p in (B / "previews").glob("*__*deg.*")}
        self.assertEqual(len(names), 15)

    def test_caveats_present(self):
        text = (B / "README.md").read_text(encoding="utf-8")
        for needle in ("text-only", "hallucinate", "not fully blind", "One call per cell",
                       "non-blind", "not an independent", "nine renders", "Portuguese", "local-only"):
            self.assertIn(needle, text)

    def test_no_machine_paths_or_secrets(self):
        import re
        bad = re.compile(r"/home/box|/workspace|sk-or-|api[_-]?key\s*[:=]", re.I)
        for p in B.rglob("*.md"):
            self.assertIsNone(bad.search(p.read_text(encoding="utf-8")), p)
        for p in B.rglob("*.json"):
            self.assertIsNone(bad.search(p.read_text(encoding="utf-8")), p)


if __name__ == "__main__":
    unittest.main()
