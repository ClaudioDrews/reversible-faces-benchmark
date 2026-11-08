# LLM authoring protocol: from brief to polished dual-face SVG

This is a **research recipe**, not an achieved production-quality claim. A model can follow it with textual SVG generation; visual feedback requires an actual safe render and a separate reader or vision-capable model. Never invent "I saw the image" in a text-only loop.

## Stage A — semantic concept, before geometry

Extract two visually distinguishable character briefs and a single nonverbal relationship/joke from the user's prompt. Choose distinct expressions, age/impression, facial structure and period-like accessories. Explain what a viewer is expected to see **without textual captions**. Do not turn the drawing into two stacked independently complete faces.

Write a **design plan** with A/B reading descriptions; eye-anchor coordinates; 5–10 explicit dual-function stroke/region correspondences; proposed outline envelope; likely negative-space groupings; failure modes; a short list of ornamental details that change roles under rotation. Each correspondence is in both frames (B upright → R(B) page), with one and only one rotation.

## Stage B — structural skeleton

Create a single vector outline + shared facial anchor + major expression/role curves before decoration. Keep the fixed 1000×1000 page, centre (500,500), no visible text, no external images, scripts, gradients or filters. For each marked keypoint \`b\`, compute \`R(b)=(1000-x,1000-y)\`. Do not assume a midpoint is recognizable; visually inspect the two frames when a safe renderer is available.

Use 1/2/3-level contour hierarchy: (1) overall silhouette; (2) necessary eyes, mouth, brows/nose; (3) ornament and engraving texture. Complexity is a **budget** to protect readability, not a global minimization target. Do not compensate a failed B by making A more elaborate.

## Stage C — structural review

Explicitly verify all anchor/keypoint correspondences. Inspect region ownership / empty-space silhouette, continuity of contour junctions, missing second-face elements and overlay or ghosting. Record any unpaired stroke and whether it has a meaningful role in the opposite orientation. Reject a failed construction before detailed hatching.

## Stage D — illustration craft (conditional)

Only after a viable dual interpretation, add original controlled hatching, cross-hatching, weighted ink profiles, taper, expression-relevant wrinkles, purposeful asymmetry, apparel/period ornament and controlled chiaroscuro. Do not paste an old Whistler drawing, and do not assume expensive/detail-heavy SVG is automatically good. Test thickness, rendering at 1000/500/200 px and inverted/monochrome presentation; remove marks that destroy the weaker reading. Favor shared detail over B-only inset shapes.

## Stage E — render / critique / revise

Use only the repository's sandboxed, sanitizer-backed render pipeline for untrusted SVG. Show A and R(A) in isolation before side-by-side. Use two judges if available: structural code critic and independent blinded human/vision assessor. Record per-orientation readability, detail quality, genuine shared contours, message and no-op change counts. Repair the **weaker** reading before optimizing art. Freeze and label each attempt; no silent best-of-N.

## Output requirements

- One self-contained SVG with \`xmlns\`, \`viewBox="0 0 1000 1000"\`, \`width="1000"\`, \`height="1000"\`.
- No labels, scripts, animations, external URLs, gradients, filters or hidden helper images; <=300 KB.
- No two independent pasted portraits.
- The same ink must yield distinct, genuinely coherent faces in two orientations.
- Include a separate text plan and evaluation provenance **outside the SVG**.
- Report limitations and actual viewing method. Structural-validity PASS is not a face-quality pass.

A provider-neutral harness in \`agent.py\` can obtain a plan and SVG in two model calls and validate them. It does **not** implement the visual stages C–E automatically yet: those remain research goals, explicitly represented in \`TRANSFER-MATRIX.md\` and \`EXPERIMENTS.md\`.

## Pose-divergent and incompleteness hypotheses

Do not hard-code two front-facing portraits. Generate structured candidate plans for alternative A/B pose pairs: frontal/frontal, down/side, three-quarter/profile, mixed yaw/pitch/roll and different inferred gaze directions. A physically shared SVG path need not have the same anatomical label in A and B. Missing contours may be intentional: specify which fragments have a completion hypothesis and which segments would become distracting if fully drawn. Never assume that sparsity alone improves the two readings. Use A/B independently evaluated perceptual outcomes to decide; original prompt contract and expanded open-design condition must be distinguished in reports.
