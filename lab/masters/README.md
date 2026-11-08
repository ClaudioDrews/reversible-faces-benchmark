# Whistler reference corpus — geometric source study

**Purpose:** obtain original-resolution reference reproductions of four historical reversible-face illustrations, preserve their provenance, derive *one* canonical raster and SVG per illustration, and compare the vectorized result against the source before drawing any artistic or perceptual conclusions.

## Sources and rights

See [catalog.json](catalog.json) for exact Wikimedia Commons file titles and description pages. Those pages identify these works as **public-domain two-dimensional art / faithful reproductions (PD-Art)**. Rex Whistler died in 1944. The four works are dated 1930 on Commons, while Salisbury Museum catalogues certain early examples as 1931–32; recorded attribution/date differences should not be silently resolved. Source bytes, descriptions and any current Commons license metadata are saved per acquisition. Research outputs preserve source page URL, retrieval date and file SHA-256.

**Not published in the live Pages site** and not automatically added to the main repository. The workflow downloads images into an ephemeral Actions runner and publishes an inspection-only downloadable workflow artifact. We do not conflate original historical artwork and CC BY 4.0 original benchmark stimuli. For use in other jurisdictions, confirm source image licensing independently.

## Why a paired reproduction is not itself the original single drawing

Some Commons JPEGs place upright and inverted renderings side by side. Their panels may contain distinct crops, margins, signatures, orientation corrections or photographic artifacts. The left and right panels must be **verified after rotation**. Never independently vectorize them and then call their union a successful reversible artwork. Instead:

1. Save the original source bytes unchanged.
2. Extract and align panel A and the 180°-rotated panel B, recording confidence and disagreement.
3. Choose one canonical panel (initially the left, explicitly documented), letterboxed to a common square. Preserve B for **independent registration checks**, not to draw a second image.
4. Derive binary, contour and tonal vectorizations **from that same canonical A**, recording raster fidelity and differences.
5. Turn the resulting **one** vector SVG physically by 180° to obtain B.
6. Run controlled region and stroke treatments on temporary copies. Any changed-pixel result is geometric only until an independent human recognizes the interpretation.

High **A vs rotated-B agreement** is a check on a reproduction, not evidence that the artist's drawing is perceptually effective. Conversely poor agreement may reveal scanning/cropping/annotation rather than artistic failure. Review every split manually.

## Reproduction

Run the dedicated [Whistler reference workflow](../../.github/workflows/whistler-reference.yml) on the experimental branch, or run locally from the repository root:

    python -m pip install -r lab/masters/requirements.txt
    python lab/masters/build_corpus.py --catalog lab/masters/catalog.json --out output/whistler-corpus

The runner needs internet access to query Wikimedia Commons and retrieve the originals. **No live requests happen in the HTML laboratory.** An offline deterministic synthetic smoke test is provided:

    python -m unittest discover -s lab/masters/tests -p 'test_*.py' -v

Outputs from the workflow include:
- source/<id>.jpg original source bytes, provenance.json and exact SHA hashes;
- canonical/<id>.png single normalized source raster plus opposite panel/registration reports;
- vector/<id>-binary.svg, <id>-tonal.svg and <id>-contours.svg (generated from the same panel);
- preview/<id>-*.png renders obtained from generated SVG, fidelity_report.json and an index.html contact sheet;
- perturbations/<id>/*.png local controlled perturbations (radial detail, omission, line weight);
- report.json experimental measurements, reproducible settings, source and derivative hashes, failures.
- radial_quadrant_profiles.csv: 16 normalized page-location cells per representation (four radial bands × four quadrants), including dark-ink fraction, edge fraction and high-frequency grayscale residuals. **These are measured physical-image properties, not semantic vagueness or face-feature tolerances.**

The outputs are **derived analytical representations**, not faithful hand-drawn replacements for Whistler. Vectorization inevitably changes contours, tone and tiny hatching. See [VALIDATION.md](VALIDATION.md) for quantitative and human-inspection gates.

## Transfer to hypotheses, including conflicting ones

This corpus does **not** replace the existing experimental hypothesis register. It gives common images for testing all 35+ pre-existing alternatives, including C₂, landmark tolerance, pose diversity (front/profile/down/side), good continuation, omitted lines, radial central-vs-outer-region specificity, fine detail without unique anatomical role, local thickness/salience, figure-ground, semantic graph roles, and artistic/message perception.

A successful outcome would map which modifications preserve or damage the **weaker** of the two readings; which marks are functionally reassigned; and where measured geometric changes fail to predict changes in perception. This requires fresh blinded human annotations. The corpus is a starting point, not a normative ground truth of role coordinates.
