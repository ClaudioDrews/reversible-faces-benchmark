# Research reading list and scientific boundaries

## Primary science, checked 2026-11-08

1. Wertheimer / Gestalt tradition (modern overview): Wagemans et al., **A Century of Gestalt Psychology in Visual Perception I: Perceptual Grouping and Figure-Ground Organization**, Psychological Bulletin 2012. https://pmc.ncbi.nlm.nih.gov/articles/PMC3482144/ . Justifies testing good continuation, closure, proximity and figure-ground as **candidate mechanisms**, not as a universal explicit algorithm.
2. Field, Hayes & Hess (1993), **Contour integration by the human visual system: evidence for a local association field**, Vision Research 33:173–193, DOI 10.1016/0042-6989(93)90156-Q. https://pubmed.ncbi.nlm.nih.gov/8447091/ . Oriented local contour association motivates a local tangent/curvature diagnostic.
3. von der Heydt (2018), **Figure and ground: how the visual cortex integrates local cues for global organization**, Journal of Neurophysiology, DOI 10.1152/jn.00125.2018. https://journals.physiology.org/doi/full/10.1152/jn.00125.2018 . Border ownership is a meaningful variable distinct from edge location.
4. Maurer, Le Grand & Mondloch (2002), **The many faces of configural processing**, Trends in Cognitive Sciences 6(6):255–260, DOI 10.1016/S1364-6613(02)01903-4. https://pubmed.ncbi.nlm.nih.gov/12039607/ . First-order face configuration, holistic processing and second-order spacing are separable; inversion affects more than spacing.
5. Feldman (2016), **The simplicity principle in perception and cognition**, WIREs Cognitive Science, DOI 10.1002/wcs.1406. https://pmc.ncbi.nlm.nih.gov/articles/PMC5125387/ . Motivates a falsifiable compression / MDL proxy, **not** a calibrated "beauty" score.
6. Kornmeier & Bach (2012), **Ambiguous Figures – What Happens in the Brain When Perception Changes But Not the Stimulus**, Frontiers in Human Neuroscience 6:51. https://pmc.ncbi.nlm.nih.gov/articles/PMC3309967/ . Spontaneous perceptual alternation **without** stimulus rotation is not equivalent to the RFB's transformation-triggered reinterpretation.
7. Zou, Cai, Zhang & Lee (2024), **VGBench: Evaluating Large Language Models on Vector Graphics Understanding and Generation**, EMNLP. https://aclanthology.org/2024.emnlp-main.213/ . Encourages evaluating structural generation beyond just a convincing raster.
8. Zini et al. (NeurIPS 2025), **vHector and HeisenVec: Scalable Vector Graphics Generation Through Large Language Models**, https://proceedings.neurips.cc/paper_files/paper/2025/hash/20b5750c81b8ef055bd99b4915fe29a3-Abstract-Datasets_and_Benchmarks_Track.html . Large vector descriptions motivate token budgets, structured editing, and long-context tests.
9. Perlman et al. (2026), **Evaluating Constrained Iterative Refinement for Scalable Vector Graphics Generation with Off-the-Shelf VLMs**, https://arxiv.org/abs/2608.28678 . Constrained decoding improved compilability; iterative revision is not guaranteed to improve visual reasoning.
10. Wang et al. (2026), **IntroSVG: Learning from Rendering Feedback for Text-to-SVG Generation via an Introspective Generator-Critic Framework**, https://arxiv.org/abs/2603.09312 . Generator/critic loop motivates, but does not prove, benefit on reversible faces.

## Art target and reuse

Rex Whistler's reversible drawings provide a historical goal for a *highly polished, expressive, richly rendered single original image*. Unlike an exact copy of a historical face, the target is a **set of qualities**: differentiated personalities, coherent anatomy in two orientations, confident contour hierarchy, detailed period-like pen-and-ink handling, appropriate ornament, purposeful negative space, and a nonverbal joke.

The artist died in 1944. Some reproductions are explicitly marked public domain by Wikimedia Commons; nevertheless, this branch intentionally **does not copy/rehost his images or any extracted tracing**. For later side-by-side comparisons, audit each image file's provenance and jurisdiction before redistribution. Never publish external raster references as if they were original model outputs.

## Limits

A C2 eigen-decomposition is algebra, not a semantic parser; dot-product or raster overlap is not a human recognizer. Recognition thresholds such as 30 px in RFB and 8 units in Sinogram PRC are **design choices measured under different domains**. No existing PRC VLM pilot is controlled native-reader evidence, and no stage here claims to solve high-quality dual-face generation. Any art-quality claim needs independent, blinded, consistent evaluation.

## Viewpoint and perceptual-completion counter-hypotheses

- Van der Linde & Watson (2010), *A combinatorial study of pose effects in unfamiliar face recognition*, Vision Research, DOI 10.1016/j.visres.2009.12.012. https://pubmed.ncbi.nlm.nih.gov/20043938/ . Recognition varied continuously with roll/yaw and their combinations, with evidence of view-specific effects; do not reduce pose to a single tilt scalar.
- Liu & Chaudhuri (2002), *Reassessing the 3/4 view effect in face recognition*. https://pubmed.ncbi.nlm.nih.gov/11814485/ . Challenges an unconditional 3/4-view superiority; avoid defining one ideal viewpoint in advance.
- Kellman & Shipley (1991), *A theory of visual interpolation in object perception*, Cognitive Psychology, DOI 10.1016/0010-0285(91)90009-D. https://www.sciencedirect.com/science/article/abs/pii/001002859190009D . Spatially incomplete visible contours may support interpolated boundaries.
- Singh & Hoffman (1999), *Completing visual contours: the relationship between relatability and minimizing inflections*, Perception & Psychophysics, DOI 10.3758/BF03206908. https://pubmed.ncbi.nlm.nih.gov/10499006/ . Model of contour interpolation with necessary assumptions; not a universal face-likeness loss function.
- Anderson, Singh & Fleming (2002), *The interpolation of object and surface structure*, Cognitive Psychology, DOI 10.1006/cogp.2001.0765. https://pubmed.ncbi.nlm.nih.gov/11863323/ . Modal and amodal completion can have different conditions and outcomes; keep them as alternative hypotheses.
