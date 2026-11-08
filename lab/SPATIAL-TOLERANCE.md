# Spatial tolerance, feature visibility and semantic reattribution

**Status (2026-11-08): mathematical research hypotheses and an interactive *synthetic* field explorer, not empirical face-perception estimates.**

## Research problem

For each intended facial role, what **conditional region** in space, variation in shape/weight, degree of contour completion and visual context supports that role in an upright face, and under what circumstances does the *same physical path* support a different role after a fixed 180° page turn?

The hypothesis is **not** that every face feature is Gaussian or has one universal standard deviation. Detection of a face, role identification, expression recognition and artistic judgement are distinct tasks and may have different acceptance regions. Measurements may be multimodal, clustered by pose/identity, anisotropic and observer-dependent.

### Spatial variables and coordinate frames

For each interpretation f∈{A,B}, and feature j, define an observer's response-conditioned landmark distribution

    p(x_j | role_j, face pose q_f, expression e_f,
              art style s, holistic configuration h_f, observer o, task t).

Here x_j is measured in each interpretation's own upright 2D facial frame (not necessarily the canvas centre). B points are converted **once** into A's artwork page by R_(500,500)(x)=(1000-x,1000-y). When q_A and q_B differ (frontal vs profile, downward vs sideways) there may be no corresponding visible eye or other canonical landmark at all; record absence as a valid observation, not as missing data.

A simple demonstration **assumes** a bivariate Gaussian for each landmark:

    d_j²(x) = (x - μ_j)^T Σ_j^(-1) (x - μ_j).
    T_j(τ) = {x | d_j²(x) <= τ}.

For B, use μ_B'=R(μ_B), Σ_B' = (-I) Σ_B (-I)^T = Σ_B.
A shared physical position exists within both assumed ellipses iff
    T_A(τ_A) ∩ R(T_B(τ_B)) ≠ ∅.

Unlike the earlier RFB formula for two *equal Euclidean disks*, unequal/rotated anisotropic ellipses have no simple 2ε distance rule. Do not silently reuse a disk condition as an exact ellipse intersection theorem. An exploratory map may plot the intersection numerically; the map is *not* a calibrated perceptual acceptance region.

Higher quality models should allow mixtures or conditional normalizing flows and a **joint** spatial configuration

    p(x_eyes, x_nose, x_mouth, x_jaw, ..., roles | pose, style, observer, task)

rather than falsely assuming every landmark is independent. Pairwise covariance also does not capture a fully holistic facial parse.

### A “quadrant” depends on which face is being perceived

The four canvas quadrants about (500,500) map under C2 as TL↔BR and TR↔BL. Exact mathematics, but **not** four universal anatomical face quadrants. A bowed or side-facing head has a different facial centre, contour and intrinsic axes. Report both:
- **Page quadrant** (fixed 500,500) for exact rotation geometry.
- **Face-relative region** (brow / eyes / nose / mouth / jaw / hair / external contour) and distance from an estimated, pose-dependent centre for perception.

Avoid pretending retinal eccentricity equals distance from a face's page centre. Retinal eccentricity depends on an observer's gaze/fixation and viewing setup. Peripheral retinal acuity/crowding literature motivates hypotheses but **does not prove** a radius-based tolerance rule for illustrations.

### Peripheral vagueness: competing models

Let r be **face-relative normalized radius**, an operational proxy only. Consider competing dispersion models:

    H0: σ_j(r) = σ_0,j                     (constant tolerance)
    H+: σ_j(r) = σ_0,j exp(+β r)           (wider at outer regions)
    H-: σ_j(r) = σ_0,j exp(-β r)           (narrower at outer regions)
    HQ: σ_j(r,φ) = f(r, quadrant, contour family, pose)
    HR: no simple radial trend; role-specific and multi-modal.

Neither detailedness nor visibility should be equated to specificity:
- **Graphic complexity** D(x): path count/curvature/line frequency/hatching/ink density.
- **Semantic specificity** K(role | x, context): how strongly an observation determines a particular role.
- **Perceptual utility** U_j(context): causal contribution of the marks to successful A and B readings.

These are different variables. Whistler-like rich peripheral ornament can be highly detailed *and* open to contextual reinterpretation. This is an artistic hypothesis to test, not an established empirical law.

The browser explorer displays exactly H0/H+/H- (via a signed β) for position ellipses. Changing β changes **synthetic ellipse widths only**. It does not predict reading probability or alter any archived SVG.

### Distinctness and the right role in the right view

A successful double-function stroke is not required to physically disappear under one turn. The hypothesis is contextual *reassignment*:

    P(role=j | I, context_A) should be sufficiently high,
    P(role=k | R I, context_B) should be sufficiently high,
    while the two face interpretations are genuinely distinguishable.

For example, a mark may be an eyebrow in A, an eye-bag in B. We need not demand zero probability for the A label in B; the meaning of “not identified” has to be operationalized as a forced-choice, free description or independent role-assignment frequency with confidence. Statistical thresholds must be established *before* inspecting held-out outcomes.

A possible descriptive role-switch statistic (NOT measured):
    S_j = min(p_j→A, p_j→B) - p_confusion,
where p_confusion is predeclared as incorrect-role classification proportion. Crucially, avoid optimising a discriminability score on the same images used to evaluate it.

## Information mapping: inspired by “Bubbles”

Gosselin & Schyns (2001) selectively sampled visual information and related observers' categorization performance to the revealed regions. Schyns, Bonnar & Gosselin (2002) expanded task-specific diagnostic-information approaches. Transfer this as **protocol**, not as previously measured tolerance maps in reversible artwork.

Propose:
1. **Pre-screen independent reads:** A and B separately, randomized, no target labels. Record free description and whether any face is seen.
2. **Visibility interventions:** for a frozen reference SVG, disclose a controlled mask of patches/path fragments at varied frequencies/sizes; compare an unchanged baseline and physically modified variants. Keep source hashes.
3. **Task-separated mapping:** face present? facial part? identity/expression? story/joke? Use different maps for different tasks.
4. **Orientation-conditioned map:** estimate performance for A and B under **the same original physical region mask, rotated with the image**. A region in A's top left corresponds physically to B's bottom right.
5. **Model random effects:** control observer, drawing, pose, task, and repeated exposure; report confidence intervals and masks that produce no raster change.
6. **Spatial-frequency controls:** distinguish sparse meaningful contour and fine engraving. The same area can be rich in details without being diagnostic for a particular identity or expression.

Because Bubbles studies can need substantial repeated observations to achieve stable per-pixel maps, begin with **coarse, predeclared regions and limited stroke classes**, then increase resolution only after power/pilot analysis. Do not advertise per-pixel psychophysical certainty from a handful of subjective labels.

## Candidate statistical model [not fitted]

For an individual forced-choice correct role judgment Y_ijkt and perturbation mask m:

    logit P(Y_ijkt=1) =
        α + u_observer_i + v_image_j
        + b1·radius + b2·quadrant + b3·role
        + b4·gap_fraction + b5·stroke_weight
        + b6·detail_density + b7·pose_pair
        + b8·radius×gap_fraction
        + b9·orientation×role
        + ... predeclared terms.

This is a prospective hierarchical mixed-effects model, NOT an estimate. Random effects and hierarchical Bayesian extensions are alternatives. Vary centre, head pose and image scale **as controlled covariates**, not as invisible tuning after the fact.

The primary dependent variable is the weaker orientation's independent recognition and feature-role correctness, with a distinct artistic-quality endpoint. Record inconclusive and ambiguous judgments as such; do not label them failures of the SVG geometry.

## How to choose tests without closing hypotheses

Compare H0/H+/H-/HQ/HR, complete vs selectively incomplete contours, high vs low decorative detail, central vs external feature semantics, different poses, face-centred vs canvas-centred coordinates, and fixed vs context-conditioned tolerances. Conflicting hypotheses remain registered.

The initial interactive model is demonstrative. Its statistical numbers are **chosen by the user**, not derived from human samples. Collect independent observations before setting any "safe region" of eye/mouth/nose placements.

## Primary literature

- Maurer, Le Grand & Mondloch (2002), *The many faces of configural processing*, DOI 10.1016/S1364-6613(02)01903-4. https://pubmed.ncbi.nlm.nih.gov/12039607/
- Rotshtein et al. (2007), *Role of features and second-order spatial-relations in face discrimination, face recognition, and individual face skills*, DOI 10.1162/jocn.2007.19.9.1435. https://pmc.ncbi.nlm.nih.gov/articles/PMC2600425/
- Gosselin & Schyns (2001), *Bubbles: a technique to reveal the use of information in recognition tasks*, DOI 10.1016/S0042-6989(01)00097-9. https://pubmed.ncbi.nlm.nih.gov/11448718/
- Schyns, Bonnar & Gosselin (2002), *Show Me the Features!*, DOI 10.1111/1467-9280.00472. https://pubmed.ncbi.nlm.nih.gov/12219805/
- Johnson et al. (2021), *Foveal processing of emotion-informative facial features*, https://pmc.ncbi.nlm.nih.gov/articles/PMC8638924/
- Kellman & Shipley (1991), *A theory of visual interpolation in object perception*, DOI 10.1016/0010-0285(91)90009-D. https://pubmed.ncbi.nlm.nih.gov/2055000/
- McManus et al. (2016), *The role of external features in face recognition with central vision loss*, https://pmc.ncbi.nlm.nih.gov/articles/PMC4930829/
