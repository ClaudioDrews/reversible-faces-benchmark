# Validation gates for historical raster → derived SVG

## Stage 0 — provenance and acquisition
- Exact Commons filename, file URL, page URL, retrieval timestamp, HTTP redirects, content MIME, original dimensions and source SHA-256.
- Commons public-domain claim, source/photographer and photographer/reproduction caveat, verified against live description before redistribution.
- No source modifications; downloaded source preserved verbatim in CI artifact.

## Stage 1 — panels and alignment
- Save both panels, crop/normalization transform and estimated padding.
- One panel is canonical; the other is an **independent rotation-consistency check**.
- Compare 0° and R180 orientation correlations, 180°-aligned IoU and SSIM. Do not claim matching faces solely from high pixel overlap.
- Document failures: if panels are not equivalent reproductions, do not silently blend them or use one to "repair" the other.
- Inspect against the original manually. This is especially important when two panels include different labels or cropping.

## Stage 2 — vectorization fidelity
- Binary silhouette alone is insufficient for fine engraving: record at least (a) binary ink, (b) a few grayscale tonal iso-contours and (c) edge contours.
- Each vector SVG is rendered back into PNG and compared to **its own original canonical raster** at the same size.
- Report source raster size, vector size, path count, MAE, SSIM, PSNR (with explicit inf when identical), original/derived gray-level histogram, dark-ink area, changed pixel fraction.
- A satisfactory PSNR/SSIM does not establish that observers recognize the image. Fidelity, artfulness and perceptual function are three different outcomes.
- The official RFB generator constraint <=300 KB need **not** be falsely claimed by historical analysis SVGs. Record vector size and separately flag whether the strict contract can be met.

## Stage 3 — perturbations and ablations
- Per generated variant report source SHA, parameter settings, random seed, measured delta and changed pixels. No-op does not equal improvement.
- Preserve paired 0°/180° source views; do not prepare unrelated faces.
- Test intentionally *opposed* hypotheses: more/less omission at centre vs outer radial area, more/less detail, uniform vs region-dependent width, symmetry and asymmetry, face-relative vs page-relative axes.
- Match approximate area of physical edits between radial conditions where practical. Otherwise differences may be due simply to more ink removed.
- Keep trial IDs separate from aesthetic or perceptual assessments.

## Stage 4 — blinded observation, not implemented
- Each orientation presented alone before participants see the pair or descriptive title.
- Open response first; then independent face-present, feature, apparent head yaw/pitch/roll, expression, character/story, artistic quality.
- Avoid supplying expected feature locations or roles. Have multiple observers and a held-out cohort.
- Report uncertainty and at least the weaker-view result; do not train weighting functions on the same drawings used for proof.

## Special caution

**Successful SVG tracing is not successful ambigram synthesis.** The goal is to understand how actual effective drawings distribute geometric and semantically relevant information, then transfer what survives controlled tests to LLM generation.
