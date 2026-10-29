# To Do

The base task (one SVG, two faces under a 180° rotation, a joke about a technology or AI event) stays the **reference condition**. Everything below is a proposed **variant or experiment**, not a replacement. The experimental priorities are set out in [`docs/future-work.md`](docs/future-work.md); this page keeps the composition idea and the practical items.

## 0. Experimental priorities (see `docs/future-work.md`)

- Independent perceptual protocol: each orientation alone, random order, blind to the model and to reversibility; then pair coherence; then whether the visual message is understood without explanation; keep generator intent apart from observer interpretation.
- A controlled v3/v4/v5 ablation with equivalent settings and multiple samples.
- Tools on versus off with everything else constant.

## 1. Composition (a variant of the task)

**(a) Current state.** The models generate faces that can be rotated 180° to reveal another face (round 1 for two of three models, and all three in rounds 3 and 4).

**(b) Open gap.** The models still do not convey an event, an idea or a message through the faces, and the artistic and comic quality is limited (round 4: well made, but not comic).

**(c) Proposed variant.** Run it **as a separate condition next to the base task**, adding one element at a time, so that the effect of each added demand on the geometric constraint can be measured. The models would be instructed to:

- **Choose an art style "to the model's own taste"**, for example engraving, grotesque realism, ukiyo-e, pop art / comic book, hand-painted watercolor, chalkboard, woodcut, chibi, classic exaggerated caricature, etc.
- **Build the image as a composition: a reversible background first, then the reversible face(s) in front of it.** The intended process:
  1. The model chooses the message it wants to convey.
  2. It imagines the two scenes that appear as the image is rotated 180° and that together could carry that message.
  3. It generates the background of the image, itself reversible (it must also work when rotated 180°).
  4. It generates the face(s) that sit in front of the background.

**(d) Open question.** It may be necessary to give brief instructions on humor, satire, caricature and visual narrative. In principle this should not be needed, since these concepts are already in the models' weights; the variant can test it.

**(e) Question the variant answers.** When the semantic complexity increases, does the model preserve a geometric constraint it can already satisfy in the base task?

## 2. Evaluation instrument

**(a) Independent human raters** following the perceptual protocol in `docs/future-work.md` (P1).

**(b) Model-as-judge check.** Give the questions of the perceptual protocol (as a prompt, not as a scoring rubric) to three models and to human evaluators, and test whether the models can assess the images consistently with human perception. The baseline work found that a text-only judge fed by a vision describer can inherit invented features ([`baselines/JUDGE-COMPARISON.md`](baselines/JUDGE-COMPARISON.md)); use multimodal judges and validate them against the human readings.

## 3. Paper

Keep paper version 2.0 intact. A version 3.0 is planned for later, once the controlled experiments above justify it; it would incorporate round 4, the baselines and the later results ([`paper/README.md`](paper/README.md)).
