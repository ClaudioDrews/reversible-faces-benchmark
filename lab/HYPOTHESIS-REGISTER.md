# Research hypothesis portfolio — preserve, test, and update

**Rule:** contradictory hypotheses may coexist. Do not discard a hypothesis because a prior model prefers frontal faces, more ink, complete outlines, or symmetry. Freeze evidence and label status; retire or refine hypotheses only after measured controls. No claim that the present lab has measured facial perception.

| ID | Hypothesis | Distinguishing manipulation | Evidence status |
|---|---|---|---|
| H01 | Shared eye pair supports two faces | eye anchors present vs absent | RFB design heuristic; open |
| H02 | One visible eye can support profile reading | second eye removed / nonfrontal A/B pair | open |
| H03 | Two poses can differ in yaw | front/side vs front/front | literature motivated; open |
| H04 | Two poses can differ in pitch | downward/side vs upright/upright | literature motivated; open |
| H05 | Independent roll helps assign contour ownership | rolled/level vs rolled/rolled | open |
| H06 | Gaze differs from facing direction | head yaw × eye gaze | open |
| H07 | Deliberate gaps improve second-face reading | gap fraction grid × contour location | completion literature; open |
| H08 | Fully drawn contours sometimes impede ambiguity | complete contour vs selective omission | open |
| H09 | Spatial tolerance is anisotropic and contextual | feature displacements in eye/nose/mouth/silhouette | open, ε uncalibrated |
| H10 | Stroke width shifts semantic role | per-region thickness ± with invariant geometry | sinogram transfer, open |
| H11 | Line-weight tapers and hatching shape expression | detailed vs flat ink with matched pixels | open |
| H12 | Negative space/border ownership supports alternate face | closure/figure-ground controls | Gestalt motivated, open |
| H13 | C₂ symmetry is necessary only in an anchor subset | core preserved / outer asymmetry varied | open |
| H14 | Asymmetry is necessary for distinct interpretation | rho low/mid/high, distinctness judged | open |
| H15 | Structure-first graph authoring beats raster fusion | matched model and generation budgets | open |
| H16 | Semantic role assignment beats geometry-only matching | blind role annotation, held-out images | open |
| H17 | Artistic ornament can be dual-role | same strokes with vs without ornament | open |
| H18 | Rich detail helps one view but can harm the weaker | detail increment across resolutions | open |
| H19 | Head pose and contour omission interact | pose pair × gap location factorial experiment | open |
| H20 | Story/expression can bias perceptual grouping | semantically distinct vs neutral brief, blinded | open |

For each test report: protocol hash, source SHA, model/seed/budget, SVG hash, edit changed pixels, human descriptive A/B results, strongest and weakest hypotheses, negative and null outcomes. The primary optimization endpoint is **the weaker independently recognizable face**, with art quality separately measured. Complex drawing does not automatically imply either.

## Shared mathematical and construction hypotheses preserved

| ID | Hypothesis / operator | Evidence and testing status |
|---|---|---|
| H21 | Optimizable construction centre can align a dual role, with benchmark centre fixed at evaluation | geometric transfer; open perceptual |
| H22 | Bézier target compromise improves dual roles | exact quadratic construction; open perceptual |
| H23 | C₂ even/odd separation reveals where asymmetry resides | algebra exact; no semantic parser |
| H24 | Angular Fourier/harmonic controls may constrain region-level modifications | exploratory; not human-validated |
| H25 | Star-shaped silhouette radial majorants permit consistent containment | exact within assumptions; artistic usefulness open |
| H26 | Contour tangency/curvature junction rules aid dual parsing | contour completion literature; open |
| H27 | Recognition-complexity normalization beats unweighted geometric distance | Sinogram result; face transfer open |
| H28 | Symmetry residual and sector balance are only one-sided diagnostics | exact geometry; not a success metric |
| H29 | Structural stroke splitting/merging is preferable to mere endpoint tuning | Sinogram geometric signal; face transfer open |
| H30 | A/B SVG critic/render loop improves legibility under matched budget | open, tool-enabled round not causal |
| H31 | Hatching and detailed ornament improve expressive dual-role performance | open artistic test |
| H32 | Incomplete contours, local weight and nonfrontal pose interact | factorial hypothesis; open |
| H33 | Perceptual parser organization matters more than individual positions | central architecture hypothesis, not established |
| H34 | Emotional contrast, narrative surprise and aesthetic resonance can be independently judged | protocol planned; no empirical claim |
| H35 | Alternate composition grammars may represent different geometric families | open: never auto-exclude hypotheses |

