# Experimental protocol (draft for preregistration)

## Main question

Can **structure-first role-graph authoring plus calibrated perceptual feedback** improve both-face recognition and independent artistic quality versus geometric blending and unconstrained SVG prompting, without extra inference budget?

## Frozen principles

1. One original drawing, page 1000 × 1000, official R around (500,500); always record source SVG SHA-256 and sanitized render provenance.
2. Never choose the best only by inspecting the expected two labels: blind raters see orientations individually, randomized.
3. Report every attempted candidate, failed SVG, no-op edit and rejection: no "best of N" hidden as a one-shot rate.
4. Keep prompt, model identifier/provider, sampling, per-attempt turns, tool calls, dollar/token budget, rendering settings and seeds where supported.
5. Pilot and hold-out sets are separate. Never calibrate metrics or weighting on the final test examples.
6. Evaluation branches don't rewrite original historical rounds, legacy code or selected evidence. No branch merge/release until review.

## Conditions

- C0: original RFB prompt v5, no tools.
- C1: geometry-only and midpoint stroke correspondence, same generation budget.
- C2: structure-first role graph with typed many-to-many correspondences, same budget.
- C3: C2 + contour/negative-space and style-aware constraints.
- C4: C3 + safe visual feedback/revision, with **matched rendering/time budget for control**, to isolate what the feedback contributes.
- C5: C4 + separate nonverbal story/joke planning stage, measured independently.
- Negative controls: self-C2 identical face, independent overlaid faces, wrong-axis mirror, a broken eye anchor, one unreadable orientation, increased-detail-only treatment, excessive ink/erasure.

Compare on held-out briefs and balanced model settings with repeated random seeds when possible. Sample size and stopping rules must be fixed after a feasibility pilot **before** formal outcome inspection.

## Measures, no single composite score

**Structural validity:** strict SVG validator, script-free local-only references, file size, correct official rotation, true one-piece drawing; count of path elements, changes in output bytes/pixels.

**Geometry:** C2 even/odd, rho, ink fraction, local 3×3 sector balance, region ablation effects, silhouette containment, landmark residuals, contour junction/tangent costs, bbox and complexity-stratified null ranks. All are diagnostics, **not passing grades**.

**Perception:** independent open description per orientation before hints, rate first-order face configuration, expression/identity differentiation, robustness to line loss and size; record the **worse orientation**, not the mean alone. Compare new art against simple collage controls. Distinguish "a face" from intended A/B interpretation.

**Semiotics:** spontaneous nonverbal message description, story congruence and shared-stroke roles separately. The model's intent statement is hidden until after open responses.

**Artistry:** independently rated linework/engraving control, silhouette expressivity, hatching and tonal hierarchy, anatomical plausibility, coherent ornaments, balance at multiple sizes. Compare with ethically sourced historical references only after initial blind reading; avoid unsubstantiated "matches Whistler" claims.

**Diagnostic intervention:** for each region / stroke ablation collect baseline and perturbed views, identity of changed paths and pixel fraction, geometric metrics and human recognition effect. Reject no-op treatment. Record fitted centre vs frozen official centre separately.

## Minimum pilot

Start with all 29 archived SVGs and four raster stimuli as separate classes. Label ten diverse SVGs (success/failure and linework range) without changing them; annotate feature/role correspondence. Use a small set of held-out briefs for generation, and obtain several independent, blinded initial descriptions before designing a numeric recognizer.

## Gates

- G0: deterministic math and security/unit tests pass, no source mutation.
- G1: selected-path ablations and visual measurements demonstrably change the expected pixels; zero-change tests trigger failure reports.
- G2: structural annotations yield inter-annotator agreement; report ambiguous or unassigned regions.
- G3: dual reading exceeds matched negative controls on held-out samples; no unblinded score fitting.
- G4: artistic quality increases *without reducing the weaker facial reading* under an art-only pass.
- G5: interpretation of the visual joke increases relative to controls and is spontaneous, not prompted by knowing the intended story.

If any gate fails, publish the null result and its mechanism rather than turning exploratory evidence into success claims.
