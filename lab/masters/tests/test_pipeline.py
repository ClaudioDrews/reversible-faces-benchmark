"""Offline synthetic tests. No copyrighted or network inputs required."""
import importlib.util
import io
from pathlib import Path
import unittest

import cv2
import numpy as np
from PIL import Image,ImageDraw

SCRIPT=Path(__file__).resolve().parents[1]/"build_corpus.py"
spec=importlib.util.spec_from_file_location("whistler_lab",SCRIPT)
m=importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)

def art(size=512):
    im=Image.new("L",(size,size),"white")
    d=ImageDraw.Draw(im)
    d.ellipse((55,35,460,485),outline=0,width=11)
    d.ellipse((90,195,170,260),fill=40)
    d.ellipse((335,195,415,260),fill=40)
    d.polygon([(235,260),(270,330),(200,335)],fill=90)
    d.arc((180,330,330,425),start=0,end=180,fill=60,width=7)
    d.line((40,65,95,125,150,68,205,140),fill=115,width=4,joint="curve")
    return im

class CorpusMathTests(unittest.TestCase):
    def test_commons_url(self):
        url=m.commons_hashed_url("Rex Whistler - Reversible Face - Hair Bald & Bearded.jpg")
        self.assertTrue(url.startswith("https://upload.wikimedia.org/wikipedia/commons/"))
        self.assertIn("Whistler",url)
    def test_crop_and_split(self):
        a=art(256).convert("RGB")
        b=a.rotate(180)
        paired=Image.new("RGB",(512,256),"white");paired.paste(a,(0,0));paired.paste(b,(256,0))
        aa,bb,transform=m.panels(paired,256)
        self.assertEqual(aa.size,(256,256));self.assertEqual(bb.size,(256,256))
        check=m.compare_panels(aa,bb)
        self.assertGreater(check["rotate_right_180"]["correlation"],.80)
        self.assertEqual(check["higher_correlation_alignment"],"180")
    def test_paths(self):
        g=np.array(art(256),dtype=np.uint8)
        s,stat=m.svg_from_raster(g,"binary")
        self.assertIn("<svg ",s);self.assertGreater(stat["primitive_count"],0)
        self.assertIn('viewBox="0 0 1000 1000"',s)
        self.assertNotIn("<image",s)
        rendered=m.render_svg(s,256)
        self.assertEqual(rendered.shape,g.shape)
        f=m.fidelity(g,rendered)
        self.assertTrue(0<=f["SSIM"]<=1)
        self.assertGreater(f["SSIM"],.20)
    def test_tonal_details(self):
        g=np.array(art(256),dtype=np.uint8)
        for kind in ("tonal","contours"):
            s,stat=m.svg_from_raster(g,kind)
            self.assertGreater(stat["primitive_count"],0)
            drawn=m.render_svg(s,256)
            self.assertLess(float(drawn.mean()),254)
    def test_perturbations_have_measured_pixels(self):
        g=np.array(art(256),dtype=np.uint8)
        results={}
        for region in ("centre","outer"):
            for operation in ("blur","gaps","dilate-ink","erode-ink"):
                v=m.perturb_variant(g,region,operation)
                self.assertEqual(v.shape,g.shape)
                self.assertEqual(v.dtype,g.dtype)
                results[region+operation]=int(np.count_nonzero(v!=g))
        self.assertTrue(any(n>0 for n in results.values()))
        self.assertGreater(results["centredilate-ink"],0)
    def test_radial_mask_is_not_retinal_eccentricity(self):
        core=m.region_mask((100,100),"centre")
        outer=m.region_mask((100,100),"outer")
        self.assertTrue(core[50,50]);self.assertFalse(core[0,0])
        self.assertTrue(outer[0,0]);self.assertFalse(outer[50,50])
        self.assertEqual(int((core&outer).sum()),0)
    def test_hash(self):
        self.assertEqual(m.digest(b"abc"),"ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad")

if __name__=="__main__":unittest.main()
