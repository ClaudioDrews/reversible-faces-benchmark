# Related work

A short map of the literature around the benchmark. Full bibliographic details and how each entry was checked: [`references.md`](references.md). Numbers in brackets are the paper's reference numbers (see the [paper](../paper/reversible-faces-benchmark-paper.md)). None of this work evaluates language models on Whistler-style reversible caricatures; it is context, not a baseline.

## Whistler and reversible faces

- Rex Whistler drew his reversible faces in 1931–32 for advertisements commissioned by Shell [12]; they were collected in *OHO! Certain Two-Faced Individuals* (1946), with verses by Laurence Whistler [12].
- Wade and Nekes give an account of his two-faced drawings [1]. Whistler and Fuller's 1960 catalogue of his work [13] was not consulted directly.
- This repository does not bundle any of the original drawings.

## Face orientation

- Inversion impairs face recognition more than it impairs recognition of other objects [2], and local feature changes become hard to notice in an inverted face (the Thatcher illusion [3]).
- Why it matters here: face B has to be constructed as a face that is upright in the rotated frame, with its own eyes, nose, mouth and hat or hair, rather than hoped for as an accident of A's strokes.
- This is context for the task. It is not evidence that any automatic classifier can judge Whistler-style drawings.

## Ambigrams and multi-view illusions

| Work | What it does |
|---|---|
| Loviscach, 2010 [4] | Searches a dictionary for nearly point-symmetric words and makes them exact with a vector editor that enforces 180° symmetry and fuses shapes smoothly. |
| AmbiGen, 2023 [5] | Optimizes glyph outlines (Bézier control points) by distilling a pretrained diffusion model, so that a word is legible in both orientations. |
| Ambifusion, 2023 [6] | Trains a diffusion model that generates ambigram images for letter pairs; introduces "ambigramability" for letter pairs. |
| Visual Anagrams, 2024 [7] | Produces images whose interpretation changes under transformations such as a 180° rotation, by combining noise estimates from different views during denoising. |
| Polster, 2000 [8] | A construction-oriented reference on rotational ambigrams. |

**How RFB differs.** (1) The output is a single SVG written as code. (2) The content is a pair of faces, not letters. (3) The shared structure is anatomical (hat band = smile), not glyph-to-glyph. (4) The drawing must also carry a joke about a recent event. (5) The generator is a language model that cannot see its output; the cited systems optimize or sample with a differentiable renderer or an image model.

## Language models drawing with code

An early text-only version of GPT-4 could write drawing code (TikZ, SVG) for recognizable objects without seeing the result [9]. RFB pushes this to a task where correctness depends on a transformation the model cannot visualize.

## Humor and caricature

- The two-reading structure maps onto incongruity-resolution accounts of humor [10]: the incongruity is two faces from one set of strokes; the resolution is the rule that connects them (promise versus consequence).
- Caricature is commonly described as deliberate exaggeration of distinctive features [11]. The prompt's three "art cues" (varied line weight, exaggeration, asymmetric silhouette) are practical stand-ins; they are not derived from, or validated against, this literature.
