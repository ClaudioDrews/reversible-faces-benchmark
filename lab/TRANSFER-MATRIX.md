# Complete transfer inventory: Sinogram Ambigram → Reversible Faces

Labels: **E** exact algebra; **M** measured in sinogram corpus only; **H** hypothesis in faces; **D** demonstrated in current lab; **P** proposed, not implemented. No numbers from the sinogram corpus calibrate facial perceptual thresholds.

| Method / idea | Sinogram / RFB evidence | Lab status | How to test for facial use |
|---|---|---|---|
| C2 half-turn, involution, determinant +1; no mirror | Both repositories | E, D | exact point and double-rotation tests |
| General legibility-set intersection and transform inverses | both theoretical docs | E definition; H recognition | separate facial A/B and composition gates |
| C2 even/odd and cosine/Fourier angular parity | sinogram C2 lab, RFB geometry | E, D raster | show original, rotated, even, signed odd; no semantic claim |
| Angular-harmonic local fields | draft PR #15; visual C2 conceptual heatmap | H, P | compare field-preserving edits against matched controls |
| Adjustable rotation centre / landmark fitting | PRC historical 120; Sinogram v2 | M; D stress-test | adjust **construction centre** then freeze 500,500 for judging |
| Stroke registration and many-to-many fusion | PRC A/B draft #16/#21 | negative M; D ablation | record match count, accepted edits, pixel changes and per-view impact |
| Endpoint/type transformation, corner splitting | PRC R-STRUCT and IDS | M geometry; H facial | inspect shared contour junctions rather than call them anatomical endpoints |
| Width reconstruction, taper and opposite-sector weights | PRC #19 and R-SECT historical | M geometry; D regional heatmap | manipulate contour emphasis under ink-retention and perceptual gates |
| Semantic graph / IDS typed composition | Sinogram IDS algebra | E for symbolic permutation; H for faces | typed role graph with conditional semantic assignment and many-to-many nodes |
| Shape-space legibility / epsilon balls | both theories | E if metric balls assumed; H epsilon | do not copy 30 px or 8-unit thresholds; calibrate by observer |
| Bézier midpoint / compromise & double-R pitfall | RFB geometry | E, D | matched path degrees, tangents, within-A/B recognition |
| Radial silhouette majorant / containment | RFB geometry | E within assumptions, D | radial profiles and silhouette ablation; don't call morph closing |
| Figure-ground and border ownership | Gestalt literature | H, D visual polarity switch | annotate who owns a boundary in each orientation |
| Negative-space use and contour completion | Gestalt / Whistler-inspired design | H, D ink inversion | controlled region completion/occlusion perturbations |
| Good continuation, local tangent and curvature | Gestalt literature | H, D path/overlay tools | blind line-continuity probes with shared/junction zones |
| Pregnanz / MDL two-parse economy | Feldman 2016 | H, P (no calibrated MDL) | compare symbolic description length after defined coding scheme |
| Configural facial vs identity/expression | Maurer et al. 2002 | H, P for recognizer | independent first-order/second-order recognition experiments |
| Stroke salience / ablation | Sinogram ink-mass bias, RFB Q_shared proposal | H, D region/path ablation | record both readings; no untested salience weights as probabilities |
| Symmetry residual rho (not orbit distance) | both; RFB Python | E, D | advisory only; zero may be failed dual interpretation |
| Density/hub/enclosure bias, per-item null z | Sinogram v2 debias | M; H facial ranking | stratify by line/ink complexity and silhouette shape |
| Multi-resolution distance / IoU / Chamfer | Sinogram metrics | M; D IoU | never equate grid and exact scales or perceptual success |
| Story / joke / semiotic duality | RFB prompts v1-v6 | exploratory | independent spontaneous message recognition, not author intent |
| Typography vs anatomy / style regime | Sinogram gothic vs Mincho | M sinograms; H engraving | controlled lineweight/hatching ablation |
| Human independent, blind presentation | both future protocols | P; protocol written | unprompted first view before paired/coached reading |
| Prompt staging geometry→verify→style | RFB v5; round 4 changed conditions | H; D prompt generator | frozen matched budgets and stages |
| Safe, tool-enabled iterative rendering | RFB round 4 hardened harness | existing infrastructure; D instructions | automatic safe renderer, critique stage still pending |
| Error/no-op and version/provenance gates | PRC fusion null, width correction replay | M; D diagnostics | validate before/after bytes and pixels; frozen checkpoints |
| Artistic finishing / hatching and ornaments | Whistler aesthetic target | H; D explicit prompt rubric | judge separately at several screen sizes and contrast levels |

All transfers are **proposed mechanisms**, not replicated facial improvements. The historical PRC centre mean gain ≈ +0.0925, endpoint mean ≈ +0.00185, sector median ≈ +0.02287 were computed under the old renderer and retained for reproducibility; the corrected width result on independent 32 source outlines is median IoU 0.4743 → 0.9083 (32/32), a source-outline fidelity result only.

The distinct-pair PRC draft A/B test matched 31/32 pairs at its largest threshold but changed 0/32 rasters. Instrument accepted mutations before claiming any successful fusion. The 52-stimulus VLM recognition pilot is draft-only and does not replace independent human readers.

Original project source documents:
- https://github.com/ClaudioDrews/sinogram-ambigram/blob/main/theory/existence-criterion.md
- https://github.com/ClaudioDrews/sinogram-ambigram/blob/main/theory/ids-rotation-algebra.md
- https://github.com/ClaudioDrews/sinogram-ambigram/blob/main/findings/prc-extremity-analysis.md
- https://github.com/ClaudioDrews/sinogram-ambigram/blob/main/findings/prc-width-contour-fidelity.md
- https://github.com/ClaudioDrews/sinogram-ambigram/blob/main/findings/debias-report.md
- https://github.com/ClaudioDrews/sinogram-ambigram/blob/main/findings/prc-ab-fusion-null-diagnosis.md
- https://github.com/ClaudioDrews/sinogram-ambigram/pull/21
- https://github.com/ClaudioDrews/reversible-faces-benchmark/blob/main/docs/geometry.md
