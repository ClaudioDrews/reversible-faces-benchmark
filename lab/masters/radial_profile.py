#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Describe physical radial and quadrant distribution of ink and fine detail.
NOT a spatial tolerance estimate or face-relative perceptual salience score.
"""
from __future__ import annotations
import argparse
import csv
import json
from pathlib import Path
import cv2
import numpy as np
from PIL import Image

RINGS=(0,.35,.60,.85,1.44)

def features(g: np.ndarray,centre=None) -> list[dict]:
    """Measure page-centred radial ink, fine residual and edge frequencies.
    The normalizing radius is half the image width, NOT retinal eccentricity.
    """
    if g.ndim != 2 or g.shape[0]<20 or g.shape[1]<20:
        raise ValueError("grayscale image with at least 20x20 pixels required")
    h,w=g.shape
    if centre is None:centre=(w/2,h/2)
    if len(centre)!=2:raise ValueError("invalid centre")
    cx,cy=centre
    yy,xx=np.indices(g.shape)
    r=np.hypot((xx+.5-cx)/(w/2),(yy+.5-cy)/(h/2))
    gg=g.astype(np.float64)
    ink=(255-gg)
    dark=gg<190
    edges=cv2.Canny(np.uint8(g),60,160)>0
    highpass=np.abs(gg-cv2.GaussianBlur(gg,(0,0),1.5))
    rows=[]
    for ring in range(len(RINGS)-1):
        lower,upper=RINGS[ring:ring+2]
        rmask=(r>=lower)&(r<upper)
        for quadrant in range(4):
            quad=np.where(yy<cy,0,2)+np.where(xx<cx,0,1)
            mask=rmask&(quad==quadrant)
            count=int(mask.sum())
            inkpixels=mask&dark
            valid=int(inkpixels.sum())
            rows.append({
                "ring":ring,"radius_min":lower,"radius_max":upper,
                "quadrant":["top-left","top-right","bottom-left","bottom-right"][quadrant],
                "pixels":count,"dark_pixels":valid,
                "dark_pixel_fraction":round(float(valid/max(1,count)),6),
                "mean_ink_0_255":round(float(ink[mask].mean()),5) if count else 0,
                "edge_fraction":round(float(edges[mask].mean()),6) if count else 0,
                "mean_highpass":round(float(highpass[mask].mean()),5) if count else 0,
                "mean_highpass_on_dark":round(float(highpass[inkpixels].mean()),5) if valid else 0,
                "coordinate_frame":"canvas-page, not face-relative",
                "semantic_specificity_measured":False})
    return rows

def run(root: Path) -> list[dict]:
    report=json.loads((root/"report.json").read_text(encoding="utf-8"))
    output=[]
    for item in report["results"]:
        ident=item["id"]
        p=root/"canonical"/(ident+"-single-source.png")
        raster=np.asarray(Image.open(p).convert("L"))
        for row in features(raster):output.append({"id":ident,"representation":"original-raster",**row})
        for kind in ("binary","tonal","contours"):
            q=root/"preview"/(ident+"-"+kind+".png")
            raster=np.asarray(Image.open(q).convert("L"))
            for row in features(raster):output.append({"id":ident,"representation":kind+"-SVG-raster",**row})
    path=root/"radial_quadrant_profiles.csv"
    with open(path,"w",newline="",encoding="utf-8") as f:
        writer=csv.DictWriter(f,fieldnames=list(output[0]));writer.writeheader();writer.writerows(output)
    return output

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--root",default="output/whistler-corpus")
    a=ap.parse_args()
    rows=run(Path(a.root))
    print("Radial/quadrant physical measurements",len(rows),"rows; no inferred face recognition.")
    return 0

if __name__=="__main__":raise SystemExit(main())
