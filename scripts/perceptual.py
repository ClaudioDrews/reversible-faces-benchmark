# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Cláudio Drews
"""Perceptual DIAGNOSTICS for a rendered drawing. These are hints for a model or a reader, not validity checks.

Structural validity (does the file meet the contract, is it safe) lives in `validate_svg.py` and never depends
on how the drawing looks. Nothing here decides whether an output passes; the benchmark is judged by a human.
Requires numpy and Pillow.
"""
import numpy as np

RHO_WARN = 0.15          # below this the figure is nearly rotationally symmetric
BLANK_FRACTION = 0.004   # below this almost nothing is drawn
FULL_FRACTION = 0.8      # above this the page is almost all non-white and rho says little


def stats(img):
    """rho = ||I - R(I)|| / ||I|| on a 200 px grayscale ink image (R = half-turn); non-white fraction and bbox."""
    g = np.asarray(img.convert("L").resize((200, 200)), dtype=float)
    ink = 255.0 - g
    rot = np.rot90(ink, 2)
    rho = float(np.linalg.norm(ink - rot) / (np.linalg.norm(ink) + 1e-9))
    nonwhite = g < 200
    frac = float(nonwhite.mean())
    ys, xs = np.where(nonwhite)
    bbox = [int(xs.min() * 5), int(ys.min() * 5), int(xs.max() * 5), int(ys.max() * 5)] if len(xs) else None
    return rho, frac, bbox


def lines(img):
    rho, frac, bbox = stats(img)
    out = [f"rho (rotational symmetry; 0 = looks identical upside down; only a one-sided alarm): {rho:.3f}",
           f"non-white fraction of the page: {frac:.3f}; bounding box of non-white pixels (x0,y0,x1,y1): {bbox}"]
    if frac > FULL_FRACTION:
        out.append("note: the page is almost all non-white, so rho is not informative.")
    elif frac < BLANK_FRACTION:
        out.append("WARNING: almost nothing is drawn (blank or tiny figure).")
    elif rho < RHO_WARN:
        out.append("WARNING: very low rho: the figure is nearly rotationally symmetric.")
    return out, rho
