# Future work

Experiments needed before any comparative claim is made. Round 4 (prompt v6, with tools) has since been run; see the first item below and [`../rounds/round-04/EVALUATION.md`](../rounds/round-04/EVALUATION.md). Most of them are in section 7 of the [paper](../paper/reversible-faces-benchmark-paper.md) (this page adds the diffusion and event-quality items); nothing here has been done (apart from the single, uncontrolled round 4).

## Priorities

What is missing is not more code. The repository can already run, record and inspect experiments. What is missing are **controlled experimental conditions** and **independent perceptual evidence**. Keep three things separate: the original artistic task, the evaluation instrument, and the scientific hypotheses that the results allow to be tested.

### P1. Independent perceptual evaluation protocol

Replace "the author looks at it" with a small protocol that does not depend on the author's interpretation:

1. **Each orientation alone.** Show every orientation in isolation, in random order, to raters who do not know the generating model and are **not told** that the figure is reversible.
2. **Open question first.** Ask what is depicted (who or what, expression), without mentioning reversibility.
3. **Pair coherence.** Only afterwards show both orientations and ask whether the transformation forms a single coherent composition (one drawing read two ways) or two overlaid drawings.
4. **Visual message.** Ask, separately, whether a visual message or joke is present and whether it is understood **without any explanation**.
5. **Generator intent versus observer interpretation.** A drawing does not communicate a joke because the model can explain which joke it meant to draw. Record the model's declared intent (the `EVENT:` and `TITLE:` lines) and the observers' independent readings, and compare them; do not score the intent.

A few independent raters are enough to start; it does not need dozens. Report agreement, not only means. This also addresses the evaluator conflict of interest ([`threats-to-validity.md`](threats-to-validity.md)). AI judges can be added later as an instrument to be validated against these human readings, not as a replacement (see the baseline findings in [`../baselines/JUDGE-COMPARISON.md`](../baselines/JUDGE-COMPARISON.md): a text-only judge fed by a vision describer inherited the describer's invented second faces).

### P2. Controlled prompt ablation (v3, v4, v5)

Repeat a simple comparison of prompts v3, v4 and v5 with **equivalent model settings**, **multiple samples per cell**, and **independent raters** (P1). Prompt v5 was rebuilt from v3 with several simultaneous changes, so separate the changes: geometry (priority order, staging), style (art cues) and semantic demand (the event requirement). Report the distribution, the failure types and the best-of-N separately. Round 2 suggests that added demands can hurt the geometric constraint and round 3 that explicit prioritization can help, but changes were made together, so neither can yet be attributed to a single component.

### P3. Tools on versus off

Run the **same prompt** with and without the render/feedback tools, keeping everything else constant (model settings, reasoning mode, providers, limits, number of samples). Round 4 changed the prompt and other conditions together with the tools, so its effect cannot be isolated. Concretely: prompt v5 with tools, and prompt v6 without tools. Pin providers and use more than one run per model.

### P4. Expanded composition as a variant, not a replacement

The proposal in [`../to-do.md`](../to-do.md) (a reversible background, faces in front, a chosen art style, a visual message) is interesting but should be introduced as an **experimental variant**; the **base task stays the reference condition**. Changing background, style and narrative at once risks repeating what round 2 showed. A well-posed question for the variant is: *when semantic complexity increases, does the model preserve a geometric constraint it has previously mastered?* This needs the base task and the variant run under the same conditions, one added element at a time.

## Further items

0. **Humor (the open problem after round 4).** With tools and a render of their own drawing, all three models produced reversible, well-made drawings, but the evaluator found none of them comic. Open questions: how to make the A/B contrast and the event carry a joke without endangering the 180° reading; whether a separate idea/joke stage before the geometry helps; whether the models can test the joke the way they test the reading (for example, describe what a viewer would find funny from the render alone); and how to evaluate humor less informally (several judges, blind presentation).
1. **Ablations on the prompt.** Prompt v5 was rebuilt from v3, so a v3-versus-v5 comparison under identical model settings isolates the effect of the priority ordering and the staging. A with/without-geometry-kit condition would test how much of the effect comes from the supplied mechanics.
2. **Dose-controlled additions.** Add event instructions and art instructions one at a time, checking the 180° reading after each (suggested by round 3).
3. **More runs, more models, more judges.** N independent runs per model and condition (one-shot without tools, or single-attempt tool-augmented; do not mix them); at least three judges; blind presentation with randomized orientation order; an ordinal agreement statistic; report the distribution, the failure types and the best-of-N separately. This would also address the conflict-of-interest problem (see [`threats-to-validity.md`](threats-to-validity.md)).
4. **A controlled tool-enabled condition.** Round 4 gave the models a render tool, but prompt v6 changed other things too (see [`../rounds/round-04/SETUP.md`](../rounds/round-04/SETUP.md)) and MiniMax was re-run once. Run prompt v5 with tools and prompt v6 without tools to separate the effects; pin providers; use more than one run per model; compare only within comparable tool conditions.
5. **Second mode.** "One person with two expressions", left out of prompt v5, is probably harder.
6. **Diffusion image models.** Not tested so far. The informal claim that they rarely succeed is an open question; a later version of the benchmark could target them.
7. **Event quality.** Make the event central and recognizable without breaking the illusion (the open problem after round 3); find a way to stop DeepSeek-like models from endless self-verification without turning reasoning off completely.
8. **A possible diagnostic for stroke sharing (not validated).** For each stroke S_j, measure how much removing it lowers the recognition score of each reading, with f_A and f_B any reading-specific recognizer: Δ_A^j = f_A(I) − f_A(I∖S_j), Δ_B^j = f_B(R·I) − f_B(R·(I∖S_j)). A score such as Q_shared = Σ_j min{[Δ_A^j]₊, [Δ_B^j]₊} / (Σ_j max{[Δ_A^j]₊, [Δ_B^j]₊} + δ), with δ > 0, lies in [0, 1) and is high when strokes contribute to both readings. It needs controls for ablation artifacts, a calibrated recognizer and validation against human judgment.
9. **Re-run round 4 with the hardened harness.** The round-4 outputs were produced by the earlier harness (commit `07d7ff8`); the current one differs in how model SVG is sanitized, rendered and logged, and in its cost estimate. A paid re-run (several runs per model, pinned providers) would show whether anything changes. Not done: the hardening was made without paid model calls.

**What earlier drafts proposed and this version dropped.** The v0.4 specification ([`design-history/`](design-history/)) contained a weighted rubric, scoring gates and a three-evaluator blind protocol. They were dropped because the human can judge the three things directly. They remain a possible starting point for a more formal future version.
