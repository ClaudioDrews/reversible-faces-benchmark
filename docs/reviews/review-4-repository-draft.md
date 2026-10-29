# Review 4: draft of this repository

Verbatim review (English) of the first draft of this repository, followed by what was done about each point.

Review of the Reversible Faces Benchmark repo (read-only audit; 7 files inspected).

**1. Unclear or missing for a first-time reader**
- What "success" means is never quantified: with no rubric and no examples of good vs. bad judgments, a reader cannot tell how a "working" reversible face differs from a "somewhat bad" one. The judgment is entirely one person's instinct.
- No scoring/scale anywhere, yet EVALUATION.md uses words like "OK", "Somewhat bad", "Low" — a first-time reader cannot reconstruct a ranking.
- Nothing explains what a "dual-function dictionary" pair looks like in an actual SVG; there is no annotated sample SVG. The complexity of the task is hard to grasp without seeing one worked example.

**2. Overstated / unverified / inconsistent claims**
- README: "In the author's experience... almost never produce a convincing result" — anecdotal, unverified, and no evidence is given.
- README says "Both LLMs and diffusion image models almost never produce..." — diffusion models were never tested in the repo; the claim is out of scope.
- "Both of these had much better artistic quality" (round 3) vs. round-1 EVALUATION.md: "None of the three has much artistic quality" — a direct contradiction, not noted as improvement/nuance.
- "The effect is achievable: two of three models produced a working two-face drawing" — contradicted by round-2 where all three lost the 180° reading; the claim is fragile but stated as if settled.
- No criterion or evidence links "artistic quality improved" to anything measurable; the single human evaluator is also the author — a clear conflict of interest never flagged.

**3. Sensitive / inappropriate for a public repo**
- R1 evaluation names DeepSeek's R1 launch and the Nvidia ~$600B market-cap drop as the "event" — this is a real, specific financial/stock event; fine to mention, but the repo repeatedly attributes financial claims ("$600B") to model outputs, not to sources — risky to publish as fact.
- The prompt includes unverified Whistler drawings — fine for reproducibility, but the disclaimer is buried; should be more prominent.
- The joke/claim about "Humane AI Pin launch hype (Nov 2023) and its shutdown after the flop (Feb 2024)" is fine as a model's declared event, but presenting it as a repo claim is risky.
- No privacy issues found.

**4. Top 5 edits, ordered**
1. Add a short worked example (annotated SVG or diagram) showing what a "good" reversible face looks like — the single biggest clarity gain.
2. Resolve the round-3 "artistic quality improved" vs. round-1 "no artistic quality" contradiction — either temper the claim or note the improvement.
3. Add a one-line caveat: evaluator is the author; no rubric, single judge, single run per model.
4. Flag the "diffusion models almost never produce this" claim as anecdotal, not a measured result.
5. Soften financial figures ($600B) to "as reported by the models" or cite a source.

## What was changed in response

- **Worked example** added: `docs/worked-example.md` (annotated real output, stroke by stroke).
- **Round-1 vs round-3 "artistic quality" tension:** the README now says explicitly that the round-3 improvement is relative (the evaluator's round-1 verdict was "none has much artistic quality") and that the drawings are still simple.
- **Conflict of interest, single judge, single run per model:** stated in the README status note and Limitations.
- **Diffusion claim:** reworded as the author's informal observation, not a measured result, and noted that diffusion models were not tested here.
- **Financial figures (e.g. "$600B") and events:** marked as the models' own declarations, not fact-checked (README heads-up, round-2 evaluation).
- **Whistler descriptions:** the "unverified" warning was moved up to a prominent note in the README.
- **No scale / meaning of verdict words:** `docs/methodology.md` now has a short "How to read the verdict words" section stating that they are informal labels. (The suggestion to add a scoring scale was not adopted: the benchmark deliberately has no rubric.)
- **"Two of three models produced a working drawing" being fragile after round 2:** the lesson now says that this did not hold once more instructions were added.
