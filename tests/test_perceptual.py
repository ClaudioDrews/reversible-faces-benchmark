# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Claudio Drews
"""Perceptual diagnostics are separate from structural validity and are advisory."""
import unittest

from PIL import Image, ImageDraw

from _common import ROOT
import perceptual as P


def img(draw_fn):
    im = Image.new("RGB", (200, 200), "white")
    draw_fn(ImageDraw.Draw(im))
    return im


class Perceptual(unittest.TestCase):
    def test_point_symmetric_figure_has_low_rho(self):
        rho, frac, bbox = P.stats(img(lambda d: d.ellipse([60, 60, 139, 139], fill="black")))
        self.assertLess(rho, 0.05)

    def test_asymmetric_figure_has_high_rho(self):
        rho, _, _ = P.stats(img(lambda d: d.rectangle([20, 20, 80, 70], fill="black")))
        self.assertGreater(rho, 0.5)

    def test_blank_page_warns(self):
        lines, _ = P.lines(Image.new("RGB", (200, 200), "white"))
        self.assertTrue(any("almost nothing" in l for l in lines))

    def test_validator_does_not_depend_on_perceptual(self):
        src = (ROOT / "scripts" / "validate_svg.py").read_text()
        self.assertNotIn("import perceptual", src)
        self.assertNotIn("numpy", src)


if __name__ == "__main__":
    unittest.main()
