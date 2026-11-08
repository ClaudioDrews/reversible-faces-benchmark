"""Numerical test of page-coordinate ink/frequency distribution only."""
import importlib.util
from pathlib import Path
import unittest
import numpy as np

src=Path(__file__).resolve().parents[1]/"radial_profile.py"
sp=importlib.util.spec_from_file_location("radial",src)
m=importlib.util.module_from_spec(sp)
sp.loader.exec_module(m)

class RadialTests(unittest.TestCase):
    def test_blank_and_ink(self):
        g=np.full((100,100),255,np.uint8)
        rows=m.features(g)
        self.assertEqual(len(rows),16)
        self.assertTrue(all(x["dark_pixel_fraction"]==0 for x in rows))
        self.assertTrue(all(not x["semantic_specificity_measured"] for x in rows))
        g[49:52,49:52]=0
        rows=m.features(g)
        self.assertTrue(any(x["dark_pixels"]>0 and x["ring"]==0 for x in rows))
        self.assertTrue(all(x["dark_pixels"]==0 for x in rows if x["ring"]>0))
    def test_coordinates_and_quadrants(self):
        g=np.full((100,100),255,np.uint8)
        g[2:8,2:8]=0
        a=m.features(g)
        self.assertTrue(any(x["dark_pixels"]>0 and x["quadrant"]=="top-left" for x in a))
        self.assertTrue(all(x["dark_pixels"]==0 for x in a if x["quadrant"]!="top-left"))
    def test_bad_dimensions(self):
        with self.assertRaises(ValueError):m.features(np.zeros((5,5),np.uint8))
if __name__=="__main__":unittest.main()
