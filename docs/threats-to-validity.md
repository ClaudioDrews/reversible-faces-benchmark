# Threats to validity

What limits the conclusions that can be drawn from the three evaluated rounds. Most of the list appears in section 6 of the [paper](../paper/reversible-faces-benchmark-paper.md); the points on the validator, on the prompt's production note and on provider changes are added here.

- **Evaluator conflict of interest.** The only judge is the benchmark's author, who also wrote every prompt after seeing earlier results. There is no blind protocol, no second rater and no agreement statistic.
- **Informal verdicts.** The verdict words ("OK", "somewhat bad", "low", ...) describe one person's reaction. They are not measurements and cannot be ranked reliably (see [`methodology.md`](methodology.md)).
- **Sample size.** Three models, one run per model per prompt (apart from retries after technical failures). Variance across runs is unknown.
- **Uneven comparisons.**
  - In round 1 the MiniMax output came from prompt v2 because its v3 run was interrupted.
  - In round 3, DeepSeek ran with reasoning disabled and MiniMax at low reasoning effort, while GLM used medium effort. DeepSeek's round 3 result is therefore **not comparable** with the other two.
  - Round 3 versus round 1 is a before/after comparison with several things changed at once, and the evaluator's expectations may also have changed.
- **Unverified prompt content.** Every prompt contains the same placeholder section (6b) with short text descriptions of two real Whistler drawings, written from public images and flagged inside the prompt as unverified. They are kept verbatim because the models saw them.
- **Round 4 (tool-enabled, post-paper) is uncontrolled.** Prompt v6 changed more than the tools: the unverified Whistler descriptions and the placeholder note were removed, the dictionary's frame wording was made precise, the title was changed to "OHO!", and Stage 2 now includes a render and a blind reading. The tool effect cannot be separated from these changes, and round 4 cannot be compared with round 3 without caveats.
- **MiniMax in round 4 is a selection.** Its first run spent its whole first turn reasoning and never called a tool; it was re-run once with a larger per-turn token limit (the only change), and the re-run is the reported result.
- **Providers and routing in round 4.** Providers were not pinned; DeepSeek was served by three providers over the turns of one run. DeepSeek again ran with reasoning disabled.
- **The harness gives its own feedback.** The diagnostics (symmetry number ρ, bounding boxes, element table) and the image the models see are produced by code written by the author, and a model may optimize for them rather than for the evaluator's judgment.
- **Humor is untested by design.** The evaluation of round 4 says the images do not convey a comic message; that is one person's reaction, and the prompt asks for a physical difference, not for a tested joke.
- **Production note and legal assertion inside the prompts.** The prompts v1–v5 say "[PLACEHOLDER — Cláudio to add and verify.]" and call the two Whistler drawings "public domain" (unverified). The models read both, so they are part of the stimulus and a possible confound; the text is kept verbatim. Prompt v6 (round 4) removed both.
- **Frame wording in the prompts.** The prompts v1–v5 state the dictionary as "a feature of B at height −y (as seen on the page)", which is looser than the docs' "B's own frame"; a model could have been misled by it.
- **The validator checks only part of the contract.** `scripts/validate_svg.py` checks size, XML, namespace, viewBox, presence of width/height and forbidden elements. It does not check width/height values or external references, and the runner itself injects viewBox/width/height. Passing it says little about the drawing.
- **Events and recency.** The models had no search, so the "recent event" depends on training data; several chose events from 2023–2025. Declared events and figures (for example market-value drops) are model wording and are not fact-checked.
- **Heuristic geometry.** The canon, the tolerance and the dictionary are design conventions, not validated perceptual facts. The dictionary is not a partition of strokes.
- **Scope of the informal claim.** The statement that diffusion image models rarely manage this task is an untested observation: diffusion models were **not** tested here.
- **Models and providers change.** Model names are OpenRouter ids at the time; providers may change or retire them, and provider-side behavior (reasoning limits that were not enforced, timeouts) affected some runs.
