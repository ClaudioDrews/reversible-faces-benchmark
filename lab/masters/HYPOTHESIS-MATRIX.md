# Historical-master study: complete, nonexclusive hypothesis matrix

**Status: preregistration draft.** All hypotheses from \`lab/HYPOTHESIS-REGISTER.md\`, \`lab/AMBIGUITY.md\`, \`lab/POSE-SPACE.md\`, \`lab/SPATIAL-TOLERANCE.md\`, \`lab/THEORY.md\`, and the Whistler-source discussion are retained. This is an **experiment portfolio**, not a shortlist of favorites. Hypotheses may contradict one another, and competing hypotheses are part of the design.

**Shared input:** exactly the same one physical historical artwork, normalized from one side of a paired reproduction. The other side is only a provenance/registration check. Each temporary variant keeps the same canonical drawing and is physically rotated for B. Never independently optimize B's raster by tracing the opposite panel.

The 4 source reproductions are exploratory art references, not a statistically representative population or controlled evidence that all images are Whistler-original copies with identical printing. Verify source quality and reuse permissions per Commons page.

| ID family | Manipulated condition / comparison | Required data | What would distinguish mechanisms? | Current state |
|---|---|---|---|---|
| H01 / H02 | two shared eyes vs one visible vs neither forced | feature role and pose annotation | can profile faces exist without fixed shared pair? | annotation planned |
| H03–H06 | independently front/side, down/up, yaw/pitch/roll and gaze | blind perceived-pose judgments | observer sees different pose despite same 180° page turn | manual controls only |
| H07 / H08 | progressively complete vs selectively omitted contours | fixed-coordinate mask variants | how does weakest-face recognition change with removal? | exploratory raster omissions generated; readers absent |
| H09 | feature x/y displacement and covariance ellipse orientation | annotated landmarks and observer judgements | anisotropic vs scalar epsilon tolerance | synthetic ellipse mathematics only |
| H10 / H11 | even vs contrasting local width; hatching and taper | source contour + targeted ink perturbation | does salience change role or only darken art? | basic radial dilation/erosion generated |
| H12 | region closure, border ownership and negative space | closed components, polarity stimuli | different facial parts assigned to identical contour | perceptual annotation planned |
| H13 / H14 / H23 / H28 | lower/higher C2 symmetry; even/odd; radial ρ | raster metrics and perceptual reading | symmetry helps which components but erases distinctness elsewhere? | geometry implemented, humans absent |
| H15 / H16 / H29 / H33 / H35 | structure-first role graphs and alternative grammars vs geometric fusion | matched generator budgets, annotated graphs | does the semantic parse predict success beyond contour overlap? | graph design planned |
| H17 / H18 / H31 / H34 | ornament, line density, nonverbal story / expressivity | multi-resolution stimuli + blind art and message ratings | higher detail with ambiguity vs detail with rigid semantic interpretation | vectors and controlled complexity manipulations planned |
| H19 / H32 | pose × contour omission × salience and radial location | factorial stimulus design | interaction stronger than main effects? | candidate controls listed |
| H20 | meaningful story vs neutral description before drawing | frozen creative briefs | improves unprompted dual reading rather than prompted agreement? | prompt agent variants exist |
| H21 | centred vs small off-centre construction; fixed evaluation centre | landmark fit and rotation comparison | centre alignment rescues compatible traces? | geometric probe implemented |
| H22 | weighted Bézier compromise | control point stress test, two-view scores | do matched anchors improve weaker face or create ghosting? | exact math implemented |
| H24 | spatially even/odd harmonic fields | deformation/line-width variant controls | harmonic editing outperforms local field? | theoretical/prototype only |
| H25 | star-shaped radial envelope union vs unconstrained silhouette | traced shape regions and leakage | does enclosure preservation maintain dual reading? | exact ideal math only |
| H26 | tangent/curvature continuity and junction perturbation | polyline and gap annotations | does completion vary with tangent and curvature constraints? | no human calibration |
| H27 | density/hub/enclosure correction with complexity strata | stroke/path/ink measures, paired ranking | is normalized geometry more predictive of perception? | planned after ratings |
| H30 | safe render-and-critic vs fixed-budget no-feedback | multiple matched LLM models | any real geometric or perceptual gain, not just syntactic repair? | structural validator only |
| H36 | constant-vs-outward widening-vs-outward narrowing σ(r) | landmarks in face-relative frames | is the alleged peripheral vagueness monotonic, inverted, or absent? | synthetic math only |
| H37 | radial vs quadrant-specific vs role-specific variation | mixed-effect fits, calibrated masks | are errors explained by distance or semantic role/pose? | analysis planned |
| H38 | high graphic detail with low semantic specificity | frequency and role recognition maps | fine textured marks can remain dual-function | multi-tone source representations |
| H39 | task-specific visual information ('Bubbles') | independently blinded masking and spontaneous reports | which regions drive A versus B and face vs expression? | protocol only |
| H40 | modal/amodal completion vs ordinary contour association | depth/occlusion and gap controls | does an inferred hidden edge behave like a completed visible line? | protocol only |
| H41 | high vs low spatial frequency and scale | multiscale stimuli / source rendering fidelity | does fine hatching add identity, expression or mere texture? | tonal/binary/edge vectors generated |
| H42 | image-centre radial vs face-centre radial | independently annotated face centres | are centrality effects actually about each inferred head? | page-centred perturbations generated, face-relative future |
| H43 | positive vs negative space as outline carriers | border/region masks, coherent-shape controls | does same margin acquire different owners after turn? | geometric masks prepared |
| H44 | raster reconstruction fidelity vs human readability | three SVG traces of same source | can high SSIM still remove the essential facial cues? | three vectorizations with fidelity output |
| H45 | exact left/right panel registration | correlation, 180° checks, scan metadata | avoid mistaking reproduction inconsistency for intentional ambiguity | source pipeline implemented |
| H46 | richer detail only at outer radius vs equally rich centre | matched ink-change and frequency/geometry | peripheral detail can be highly intricate and still dual-role | planned variants |
| H47 | random omission vs designed incompleteness | seeded masks vs annotation-selected contours | purposeful ambiguity should outperform random deletion | seeded raster controls, designed comparison future |
| H48 | face percept vs expression vs recognition of a nonverbal joke | independent judgment tasks | effects may differ or oppose one another | requires observers |

## Statistical analysis (do not fit now)

An observational score is not a psychometric threshold. First run a source-quality / display pilot and independent, counterbalanced human presentation, with participants initially unaware of the intended two interpretations. Estimate hierarchical observer–image random effects; report item-level results, uncertainty intervals, no-op modifications and all failing controls.

For conditional landmark coordinates, start with empirical quantiles or a mixture; only use a Gaussian elliptical acceptance region if justified. The RFB 30-px heuristic and PRC 8-unit terminal-distance choices are NOT observed tolerances for historical faces.

**Most relevant effect for generation:** the function of a path (A-feature, B-feature or decoration) conditional on orientation and complete composition. Physical disappearance is unnecessary. A complex detail may be perceptually subordinate to one frame and decisive in the other.

## Registration and vectorization diagnostics to prevent false findings

1. Source hash, Commons file metadata/rights and exact paired reproduction.
2. Left/right auto-crop flag, pre/post turn correlation; human-verify split.
3. One canonical A from a single side; B always R(A), never independent drawing.
4. Compare binary, grayscale tonal and contour SVGs for changes, not “vector = perfect.”
5. Each radial/projection/ink variant has unchanged original as the control.
6. No artifact is labelled "recognizable" without observer readings.
7. Apply any chosen method on **held-out LLM-generated SVGs** under fixed prompting/model budget.

## Next implementation sequence

- Acquisition+fidelity first (CI artifact can be inspected before any visual claim).
- Manual registration/crop corrections, source quality gate.
- Controlled mask/landmark annotation files; no fake labels.
- Parametric perturbation sweeps with changed-pixel and image-level controls.
- Independent blinded psychophysics, then statistical estimation.
- Use estimates as **soft guidance**, not as a hard-coded generator dogma; compare an open LLM baseline against conditional prompts and learned tolerances.
