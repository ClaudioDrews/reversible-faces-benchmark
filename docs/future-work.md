# Future work

Experiments needed before any comparative claim is made. Most of them are in section 7 of the [paper](../paper/reversible-faces-benchmark-paper.md) (this page adds the diffusion and event-quality items); nothing here has been done.

1. **Ablations on the prompt.** Prompt v5 was rebuilt from v3, so a v3-versus-v5 comparison under identical model settings isolates the effect of the priority ordering and the staging. A with/without-geometry-kit condition would test how much of the effect comes from the supplied mechanics.
2. **Dose-controlled additions.** Add event instructions and art instructions one at a time, checking the 180° reading after each (suggested by round 3).
3. **More runs, more models, more judges.** N independent one-shot runs per model and condition; at least three judges; blind presentation with randomized orientation order; an ordinal agreement statistic; report the distribution, the failure types and the best-of-N separately. This would also address the conflict-of-interest problem (see [`threats-to-validity.md`](threats-to-validity.md)).
4. **Tool-enabled condition.** Let the model render, rotate and look at its output, to measure how much of the failure is "blind drawing". Compare only within comparable tool conditions.
5. **Second mode.** "One person with two expressions", left out of prompt v5, is probably harder.
6. **Diffusion image models.** Not tested so far. The informal claim that they rarely succeed is an open question; a later version of the benchmark could target them.
7. **Event quality.** Make the event central and recognizable without breaking the illusion (the open problem after round 3); find a way to stop DeepSeek-like models from endless self-verification without turning reasoning off completely.
8. **A possible diagnostic for stroke sharing (not validated).** For each stroke S_j, measure how much removing it lowers the recognition score of each reading, with f_A and f_B any reading-specific recognizer: Δ_A^j = f_A(I) − f_A(I∖S_j), Δ_B^j = f_B(R·I) − f_B(R·(I∖S_j)). A score such as Q_shared = Σ_j min{[Δ_A^j]₊, [Δ_B^j]₊} / (Σ_j max{[Δ_A^j]₊, [Δ_B^j]₊} + δ), with δ > 0, lies in [0, 1) and is high when strokes contribute to both readings. It needs controls for ablation artifacts, a calibrated recognizer and validation against human judgment.

**What earlier drafts proposed and this version dropped.** The v0.4 specification ([`design-history/`](design-history/)) contained a weighted rubric, scoring gates and a three-evaluator blind protocol. They were dropped because the human can judge the three things directly. They remain a possible starting point for a more formal future version.
