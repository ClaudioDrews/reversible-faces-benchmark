# Ambiguity is not a defect: an explicit experimental programme

**Status:** hypothesis and controlled perturbation study; no face-recognition claims.
**Scientific motivation:** a completed depiction can be less useful for a reversible face than a graphically underdetermined but highly suggestive contour. This document adds a core mechanism to the research design rather than treating incompleteness as low-quality drawing.

## 1. What incompleteness means

An omitted line is not always an invisible physical boundary in the observer's perception. Distinguish:
- **Fragmented contour integration:** adjacent/distant orientated fragments are perceptually grouped by good continuation, closure and proximity; no visible occluder is necessary.
- **Amodal completion:** a boundary is inferred behind an occluding surface (the missing portion is not literally seen).
- **Modal completion:** an illusory edge or surface is experienced as present despite homogeneous local luminance.
- **Semantic suggestion:** marks evoke a role such as a "nose" or "hat brim" without necessarily completing a geometrically precise contour.

Do NOT equate these effects. In an illustration, the effective role of a mark is context-dependent. A visible SVG path can be unequivocally defined as geometry yet *semantically underdetermined*. Our hypothesis is that judiciously omitted fragments can create multiple plausible perceptual completions after a half-turn, while indiscriminate gaps merely damage both views.

### Candidate mathematical language

Let M denote a controllable visibility mask on vector contours and I_M the physically displayed image. The perceptual interpretation graph in orientation θ is a hypothetical random variable G_θ conditioned on I_M and contextual grouping cues. The aim is not to minimize ink or maximize entropy in isolation. It is to seek **two strong distinct conditional parses**:

    G_A ~ p(G | I_M, context_A)
    G_B ~ p(G | R(I_M), context_B)

No calibrated probabilities or semantic parser exist in this laboratory. The notation is an experimental target, not a numerical claim.

## 2. Configural tolerance is multidimensional [HYPOTHESIS]

The original benchmark's fixed ε≈30px is an authoring heuristic, **not** a psychophysically calibrated tolerance. Recognition is not generally determined by one fixed Euclidean radius.

Suppose a vector x contains measurable features (eye separation, mouth–nose spacing, brow angles, normalized head width, silhouette landmarks, etc.). For each reading, define a *hypothetical* tolerance region around a prototype μ_A or μ_B:

    (x-μ_A)^T Σ_A^{-1} (x-μ_A) <= t_A

Likewise for B in its own upright frame. The covariance matrices Σ and thresholds t must be estimated from independent observer judgments; diagonal, isotropic and Gaussian models are assumptions that require testing. This is an illustrative anisotropic tolerance envelope, **not** an established neural code.

A practical pilot tests one coordinate change at a time, then combinations. Report the weakest interpretation and record whether expression/identity changes even while a face remains detectable.

## 3. Relative head pose can switch between the parses [HYPOTHESIS]

Physical page rotation is exactly 180 degrees. **Perceived head orientation** is an interpretation-dependent latent variable. In the two upright viewing frames, pose estimates θ_A and θ_B need not be equal. The eye line, inferred head axis, neck, hairstyle, nose projection and outer silhouette can anchor conflicting pose interpretations from identical marks.

The lab therefore displays two *independent manual pose-axis annotations* with angle sliders. These axes are hypotheses supplied by the user, not pose-estimation outputs. The axis lines are NOT added to the SVG and cannot be interpreted as a measured pose difference.

Head tilt and facial emotion interact: changes in head position can change the appearance of brows and expressions without moving the facial muscles. This makes apparent pose potentially a semantic resource, but a controlled reversible-face test remains necessary.

## 4. Ink thickness and expressive suppression

Stroke width is not simply a typographic defect. It controls contrast, edge ownership, salience, layering, and the suggestion of volume and expression. Local thickness adjustments may cause one component to dominate in orientation A but become contextual texture in B.

A controlled perturbation keeps the **underlying original SVG unchanged**, modifies a temporary copy of exactly one primitive (stroke dash gap, width factor), renders the result in both orientations and computes the actual changed pixel fraction, ρ and ink occupancy. If it changes no pixels, it is a **no-op**. If a region is a solid fill, dashing the stroke may be a no-op by construction; the experiment must report rather than conceal this.

No fixed recipe from the Sinogram PRC terminal weights (e.g. δ=8) transfers across tasks.

## 5. Three distinct kinds of incompleteness

1. **Physical incompleteness**: actual missing stroke fragments, simulated with dashed paths or masked segments.
2. **Geometric under-specification**: a curve could fit two incompatible anatomical roles within tolerable variation.
3. **Semantic under-specification**: a complete graphic contour acquires different roles in different facial contexts.

The most compelling artwork may combine all three; empirical tests must manipulate them separately.

## 6. Two experiments for the new lab

### Experiment G — completion frontier (geometric perturbation)

For each selected original SVG primitive, create a grid of gap fraction g∈{0,.1,.25,.4,.6} and stroke-width factor w∈{.65,1,1.35,1.8}. Keep the page's 180-degree transformation fixed. Record exact modified source hashes, per-orientation raster differences (rotated views are not independent samples), opacity/ink fraction, local region balance and failure/no-op status. The browser workbench provides a manual prototype; an automated batch must be added and frozen later.

Then present candidate views separately, randomized and blind. Ask: “What do you see?” before mentioning faces or rotations. Compare rates of spontaneous face detection, feature description, distinct A/B roles, and aesthetic quality. Do not infer that a geometric minimum is an observer optimum.

### Experiment P — apparent head-pose dissociation

Annotate eye line, inferred nose-midline, jaw/hat silhouette and neck direction independently for each interpretation of archived images. Collect blinded observer pose-angle estimates separately in A and B, including confidence and whether either image was recognized as a face. Compare observer angular distributions with a model's manual annotations; do not merely rotate the same axis.

Hypothesis: some successful reversible pairs permit θ_A≠θ_B in their own upright viewer frames. Variation of the observer's pose estimate is not the physical 180-degree page turn.

## 7. Art target and empirical criterion

A “Whistler-level” quality goal cannot be reduced to high path count, high structural overlap, or a single face-recognition probability. The relevant quality is the **creative resolution of conflicting constraints**, with confident composition, painterly line variation and suggestive omission. Compare:
- fully explicit contours vs strategically incomplete contours;
- uniform stroke vs varied stroke;
- centered canonical head vs asymmetric and tilted pose;
- rich linework before vs after a verified two-face skeleton;
- meaningful shared marks vs independent overlaid faces.

An explicit *quality gate* is non-inferiority on the weaker face's independent recognition when stylistic detail is added, plus independent art appraisal. Report no-op perturbations and quality regressions.

## Literature

- Kellman & Shipley (1991), **A Theory of Visual Interpolation in Object Perception**, *Cognitive Psychology*. DOI 10.1016/0010-0285(91)90009-D: physically incomplete boundaries and “relatability” of edge fragments.
- Wagemans et al. (2012), **A Century of Gestalt Psychology in Visual Perception**, *Psychological Bulletin*. https://pmc.ncbi.nlm.nih.gov/articles/PMC3482144/ : grouping, figure-ground, modal versus amodal completion.
- Van Lier & Gerbino (2020), **Amodal Completion Revisited**, https://pmc.ncbi.nlm.nih.gov/articles/PMC7466902/ : caution about visually and conceptually incomplete figures.
- McKone & Yovel (2009), **Why does picture-plane inversion sometimes dissociate perception of features and spacing in faces, and sometimes not?**, DOI 10.3758/PBR.16.5.778: facial feature shape and spacing interact.
- Collishaw, Hole & Schwaninger (2005), **Configural processing and perceptions of head tilt**, DOI 10.1068/p5216: inner-feature position changes perceived head tilt and apparent nose length.
- Witkower & Tracy (2019), **A Facial-Action Imposter: How Head Tilt Influences Perceptions of Dominance From a Neutral Face**, DOI 10.1177/0956797619838762: head pose can alter perceived facial expression and social evaluation.
- Salisbury Museum, *Reversible face: The scholar and the bruiser* (1931–32), https://salisburymuseum.org.uk/collections/reversible-face-the-scholar-and-the-bruiser/ : primary artifact and technique context; original ink wash, later OHO! collection. No copied image is stored here.
