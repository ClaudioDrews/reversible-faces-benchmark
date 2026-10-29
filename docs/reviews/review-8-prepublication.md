# Review 8: pre-publication consistency and accuracy review

**Reviewer:** David (Peter's Hermes agent), text-only, one call (`hermes chat --query-file <packet> --oneshot -Q -t vision --max-turns 3`, model `deepseek/deepseek-v4.1-flash-1017` through OpenRouter; no tools were needed or used). **Material:** the new `README.md`, `docs/README.md`, `rounds/README.md`, the new "Scope and versions" section of `paper/README.md`, the rewritten `to-do.md`, and the new or changed sections of `docs/threats-to-validity.md`, `docs/methodology.md`, `docs/geometry.md` and `docs/future-work.md`, together with a list of facts taken from the repository's own data. He did not read the repository itself, so every finding below was checked by Peter Weyland (Claudio's Grok Bot assistant) against the repository before anything was applied. His answer is reproduced verbatim in the next section, followed by what was done about each point.

**Cost:** Hermes' estimate for the 30-day total moved from about US$2.57 to US$2.58 for this call, i.e. about US$0.01 (one call of roughly 15,000 input tokens and 3,000 output tokens; the input was a 54 KB text packet).

## What was done about each point

Applied = the text was changed. Partly = a different fix from the one proposed. Rejected = no change, with the reason.

| # | Severity (David) | Disposition | What was done, or why not |
|---|---|---|---|
| 1 | HIGH | Partly | `MAXTOK=20000` is correct for what it described: DeepSeek in round 3 ran with `NOREASON=1 MAXTOK=20000` (round 3 `EVALUATION.md`). The line was misleading, because it read as the setting for all models. Replaced by the variables with their real defaults (`MAXTOK` 64000 for `run_models.py`, 32000 for `run_models_v6.py`) and an explicit per-model example. |
| 2 | HIGH | Applied | Same edit: GLM used the defaults, MiniMax `EFFORT=low`, DeepSeek `NOREASON=1`. |
| 3 | HIGH/MED | Applied | The README now says the prompts ask for the contract and that the runners add `xmlns`, `viewBox` and size if a model leaves them out; it states that the current validator enforces the contract exactly, the earlier one was weaker, and that this did not affect the results (link to the new validator section). |
| 4 | MED | Applied | Tagline changed to "an experimental framework, with reproducible offline tooling and archived artifacts". |
| 5 | MED | **Applied; a real error found** | Confirmed with `git show 6747499:scripts/run_models_v6.py`: the round-4 harness stopped only when the provider-reported cost reached the cap; the pre-call estimate was added in the hardening. `docs/threats-to-validity.md` and `docs/methodology.md` (existing text, not only the new text) said the opposite for round 4. Both, and the README, now say what the round-4 harness did and what the current one does. |
| 6 | MED/HIGH | Applied | The baseline paragraph now states that the judge agent is text-only, worked from descriptions by a vision model that sometimes invented the expected face, was not told the model or verdict, agreed 11/15 and 9/15, and that the assistant's 15/15 rubric was not blind and is not an independent check. |
| 7 | MED | Applied | Replaced "two faces side by side or stacked" with the author's judgments (for example two stacked faces, or a head with a tiny second head in the collar), which is what the baseline records support. |
| 8 | MED | Applied | "The results are not affected" became "no sign that the results were affected, but equivalence with the current rendering path was assumed, not re-run" in the README and in `threats-to-validity.md`. |
| 9 | MED | Applied | The implementation section now says that the scripts are the current hardened versions, that round 4 was produced by the earlier harness (commit `6747499`, with the same prompts, tools and limits), and how to read that code. |
| 10 | MED | Applied | `to-do.md` no longer implies an evaluation checklist exists; it proposes giving the perceptual-protocol questions (not a scoring rubric) to models and humans. |
| 11 | MED | Applied | The "Running" section now says: validate first, look at the sandboxed preview, and do not open unvalidated model SVG in a personal browser. |
| 12 | LOW | Rejected as stated, applied as a precision | "The cheapest" is supported by the repository's own numbers: GLM had the lowest delivered-run cost in each of rounds 1–4 (US$0.0034, 0.0008, 0.0035, 0.0116). The claim now says exactly that. |
| 13 | LOW | Applied (README) | The README now says "apart from retries after technical failures" and declares the one selected re-run (MiniMax, round 4). `methodology.md` already had the retry rule. |
| 14 | LOW | Applied | The README names the advisory symmetry number and element table shown to the models in round 4 as a further difference from the earlier rounds. |
| 15 | LOW | Applied | "Two somewhat funny" restored in the round-1 row; `to-do.md` now says round 1 (two of three models) as well as rounds 3 and 4. |
| 16 | LOW | Rejected | Round 1 effort is documented: its `EVALUATION.md` says "default reasoning effort (medium)". The index row now says so explicitly. |
| 17 | LOW | Applied | The set is now named: the 18 SVG files under `rounds/*/svg/` and `rounds/*/not-evaluated/`. |
| 18 | LOW | Applied | "In the 1000 × 1000 coordinate system of the contract" added after the rotation formula. |
| 19 | LOW | Partly | "In this setting" and the per-model prompt version in round 1 were added to the round-1 sentence. The tagline "Evaluating geometric consistency, perceptual ambiguity, and semantic composition in generative AI" was kept (the author approved it); the status box and the limitations section right under it carry the scope. |
| 20 | LOW | Applied | Reworded as "one evaluator found no comic message in any of three outputs ... a hypothesis, not a finding". |
| Omissions | - | Partly | Blind-to-model: **added** (the evaluation is not blind to the generating model; the evaluator opens files named after model and prompt). Whether the evaluator read the declared `EVENT:`/`TITLE:` lines before judging: **not recorded; stated as such** in the README and in `threats-to-validity.md`. Discarded prompts beyond retries: only the one discarded variant exists (`prompts/discarded/prompt-v5b.md`), already documented in `methodology.md`. Different prompt version per model within a round: only round 1 (MiniMax v2), already documented; now also mentioned in the README. |

What he did not catch, found in Peter's own scan of the old documents: `docs/geometry.md` said the symmetry number ρ "was not computed in any round" and that no quantity of its sections 3–6 was computed in the rounds, although the round-4 harness computes and shows ρ to the models; fixed ([`geometry.md`](../geometry.md)). The older validator text in `threats-to-validity.md` contradicted the current validator (the original reason for this pass); fixed.

## David's answer (verbatim)

Review of (B) against (A). Findings only; no praise.

1. HIGH — Wrong token setting in README.
Quote: "Settings used in the rounds (environment variables): `EFFORT=low`, `NOREASON=1`, `MAXTOK=20000`, ..."
Fact: `run_models.py` MAXTOK default is 64000; the round-2 attempt hit 64000; the round-4 MiniMax re-run used 64000 per turn; `run_models_v6.py` defaults to 32000. Nothing in (A) supports 20000, and 20000 would make the "hit the token limit" narratives incoherent.
Fix: delete the single settings line; give a per-round table (model / effort / NOREASON / MAXTOK) or an example invocation labelled "example only".

2. HIGH — `EFFORT=low`, `NOREASON=1` presented as "used in the rounds".
Fact: GLM ran at medium effort (default) in rounds 1/3/4; MiniMax at low; DeepSeek had reasoning disabled only in rounds 3 and 4. The README itself states this two paragraphs later ("GLM ... default reasoning effort (medium)"), so the line contradicts its own table.
Fix: remove; state per-model settings, and state that settings differed between rounds (already correctly said in "Interpretation").

3. HIGH/MED — Output contract attributed to the models is historically false.
Quote: "Each model must produce: ... a `viewBox="0 0 1000 1000"` coordinate system, with `width="1000" height="1000"`".
Facts: the historical validator did not check width/height values, and "the runner of that time injected `viewBox`/`width`/`height` itself" (threats doc, same repository). So for rounds 0–3 the models did not have to produce these attributes; they were added.
Fix: split into "contract as documented to the model" vs "what the validator enforced then" vs "what 2.1.0 enforces now", or move the sentence under "Output contract (current)".

4. MED — "Reproducible" contradicts the reproducibility section.
Quote: "A reproducible experimental framework for testing whether language models can synthesize..."
Later: "Model runs are **not** reproducible bit for bit". "Framework is reproducible" is defensible only for the offline parts.
Fix: "a framework for reproducible offline tooling and archived, non-reproducible model runs".

5. MED — Internal contradiction on the cost cap of round 4.
threats: "The prompts, tools, limits and settings are the same; what changed is ... the pre-call cost estimate, logging and overwrite protection."
README/methodology: the round-4 harness's "cost budget ... estimates the worst case before each call and adds the reported cost after it".
If the pre-call estimator was added during hardening, the round-4 harness did not have it, and the README's description of the US$0.25 mechanism is anachronistic (or the threats sentence is wrong).
Fix: state explicitly which components existed in commit 6747499; if unknown, say so and downgrade the claim to "the reported totals are lower bounds".

6. MED/HIGH — Overclaim about the baseline judge's independence.
Quote: "A second AI agent judged every image blind in both orientations".
Facts: the agent was text-only and fed by an auxiliary vision describer that "sometimes hallucinated the expected second face"; its 0–2 rubric agreed 15/15 but was scored non-blind and "not independent"; stage 1 agreed 11/15, stage 2 9/15. "Blind" without this is materially misleading.
Fix: "A second, text-only agent produced blind verdicts through a vision describer that sometimes invented the expected face; its rubric scores were not blind and its agreement with the author was 11/15 and 9/15 across stages."

7. MED — Unsupported specific failure mode for the raster baselines.
Quote: "two faces side by side or stacked, never one drawing read two ways".
Fact (A) only records that the 4 raster generators were "judged failed by the author" with a plain prompt. The mechanism is an interpretation, stated as observation.
Fix: "judged failed (the author's description: two faces presented separately rather than one drawing read two ways)", or cite the baseline record.

8. MED — "Results are not affected" is an unverified inference.
Quote: "The delivered round-4 SVGs contain only plain drawing elements, so the results are not affected".
Facts: the round-4 pipeline ran Chrome with `--no-sandbox` outside bubblewrap and cleaned SVG with regexes; that the 18 stored files pass the current validator does not show the delivered/rendered artifacts were identical to what the model intended, nor that the renderer behaved as the current one would.
Fix: "the surviving files are benign and pass the current validator; the rendering path differed and was not re-run, so equivalence is assumed, not demonstrated".

9. MED — Implementation table implies the round-4 production harness is in the repository.
Quote: "The repository contains the experimental data and the infrastructure used to produce and inspect it" followed by `safe_render.py` ("Chrome inside bubblewrap").
Fact: round 4 was produced by the harness of commit 6747499, with `--no-sandbox` outside bubblewrap; the current scripts are not the producing code.
Fix: add a column or note per component: "current (2.1.0)" vs "used for round 4".

10. MED — to-do.md invents an instrument that does not exist.
Quote: "Give the evaluation checklist to three models plus human evaluators".
Contradicts README: "There is no rubric ... The only checklist is the self-check inside the prompt, which the *model* uses".
Fix: "give the P1 protocol's questions (as a prompt, not a scoring rubric) to three models".

11. MED — Broken security logic in "Running the benchmark".
Quotes: "The judgment itself is human: open the SVG in a browser, rotate it and decide." and, two sentences later, "Only open SVGs from a model in a browser if you trust them; the previews and the harness never render them raw."
The prescribed judging procedure is exactly what the warning forbids, with no alternative given.
Fix: "judge from a bubblewrap-isolated render (`safe_render.py` / `render_preview.py`); opening raw model SVG in a personal browser is not recommended."

12. LOW — "The cheapest" for GLM is unsupported.
Quote: "`z-ai/glm-5.3-flash` | The cheapest".
Fact (A) gives only per-round totals (0.075/0.057/0.052/0.030/0.113), not per-model costs; and settings differ, which the doc itself says makes costs non-comparable.
Fix: delete, or quote the actual per-model logs.

13. LOW — "One evaluated output per model per prompt" vs retries.
README and methodology say one run per model per prompt; facts record a MiniMax retry in round 2 (token limit), a MiniMax re-run in round 4, and a MiniMax timeout in round 3. threats hedges with "(apart from retries after technical failures)" — the other two documents do not.
Fix: one consistent sentence everywhere: "one evaluated output per model per prompt, after at most one retry for a technical failure (rounds 2, 3, 4 — MiniMax)".

14. LOW — Round-4 confound omitted: the advisory ρ alarm.
Fact: the round-4 harness computed ρ and showed the models a warning when ρ < 0.15. The README's round-4 section and its confound sentence ("prompt v6 and other conditions also changed") never mention that models received an extra geometric self-check signal absent from rounds 0–3. Only `geometry.md`/`SETUP.md` do.
Fix: name it among the round-4 confounds in the README table or the round-4 paragraph.

15. LOW — Round-1 verdict is truncated and mis-summarised elsewhere.
README table: "Effect OK for DeepSeek and MiniMax, somewhat bad for GLM; low artistic quality; no impactful use of the event" — drops "first and third somewhat funny". Separately, to-do.md says the models' current reversible state comes from "rounds 3 and 4", although round 1 already had an acceptable effect for two of three.
Fix: restore the omitted clause; in to-do.md say "rounds 1, 3 and 4".

16. LOW — Unsupported "default effort" for round 1.
rounds/README: round 1 "All three, default effort". Fact (A) records settings for rounds 2–4 only; round-1 effort is not documented.
Fix: "effort not recorded".

17. LOW — Count ambiguity that can contradict rounds/README.
"Every one of the 18 SVGs in the repository passes ... including the 12 evaluated ones" coexists with "Round 1 and round 4 also have `not-evaluated/`". If any file there is an SVG, 18 is wrong.
Fix: "the 18 SVG files under `rounds/*/svg/`" — pin the set.

18. LOW — MATH: the rotation formula silently depends on the contract.
"$$R(x, y) = (1000 - x,\; 1000 - y)$$" is only the centre half-turn if the canvas really is width=height=1000 — which, per item 3, the historical pipeline sometimes injected rather than enforced. Elsewhere the equations ($I_\pm$, $s^*$, $I \in C_A \cap R[C_B]$) are algebraically consistent with docs/geometry.md, and the `$...$`/`$$...$$` constructs are the ones GitHub's MathJax supports (no `\label`, `\begin{align}`, or bare `\\`), so no rendering defect. Fix: add one clause "in the 1000×1000 viewBox".

19. LOW — Promotional/undefined framing in the opening.
"Evaluating geometric consistency, perceptual ambiguity, and semantic composition in generative AI" reads as a field-wide programme; the evidence is three models, one author-evaluator, one run, no statistics. Same for "The result suggests that explicit geometric instructions and feature correspondences can help a model build two readings" — round 1 changed prompt and per-model prompt version simultaneously.
Fix: qualify both with "in this setting" and note the prompt-per-model difference in the round-1 paragraph.

20. LOW — "Round 4 suggests that humor, not geometry, is now the bottleneck" (open questions) is an inference from three outputs by one non-blind evaluator; it is hedged, but appears in a list of research questions where readers will read it as a finding.
Fix: mark as "one evaluator's impression from round 4".

Critical omissions a technical reader will look for and not find: whether the round judgments were blind to model identity; whether the author saw the model's declared `EVENT:`/`TITLE:` before judging (that would explain "no comic message" verdicts); how many prompts/attempts were discarded and why (beyond retries); and a statement that the five prompt-version files differ per model inside a single "round", which weakens every round-to-round comparison.
