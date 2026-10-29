# Paper

**`reversible-faces-benchmark-paper.md`** is the accompanying paper for this repository: *Reversible Faces Benchmark: a one-shot test of rotation-consistent line drawing in language models* (Cláudio Drews, version 2.0, 29 October 2026).

## Status

- **Early research, not peer reviewed.** A benchmark design plus three informal pilot rounds (the paper) and a later tool-enabled round 4 (repository only).
- **One human evaluator, who is also the author.** Three inexpensive models, one run per model per prompt. No statistics are claimed. The results are design notes, not a leaderboard.
- The paper describes the design that was actually run (one-shot, no tools, human judgment with no rubric). The older v0.3/v0.4 specifications in [`../docs/design-history/`](../docs/design-history/) describe a heavier design (weighted rubric, gates, blind protocol, tool use) that was **not** used and is superseded.

## Round 4 is post-paper

The paper describes rounds 0–3, all one-shot with no tools. **Round 4 (prompt v6, a tool-enabled condition) was run after the paper was written** and is **not covered by it**; the paper has not been rewritten. Round 4 is documented only in the repository: [`../rounds/round-04/`](../rounds/round-04/) (evaluation, setup, outputs, transcripts), [`../prompts/prompt-v6.md`](../prompts/prompt-v6.md), [`../scripts/run_models_v6.py`](../scripts/run_models_v6.py), and the README summary. Where the paper says that the models had no tools, that holds for rounds 0–3 only. In round 4 all three models produced reversible, well-made drawings, but the evaluator found none of them comic; humor became the open problem (see [`../docs/future-work.md`](../docs/future-work.md)).

**Versions.** The paper is version 2.0 and was not changed. The repository is version 2.1.0 (see [`../CITATION.cff`](../CITATION.cff)): it adds round 4 and prompt v6, and hardened scripts. Where the paper mentions the file validator, the runner or the previews, those scripts have since been rewritten for safety (untrusted-SVG handling, an exact file contract, structured logs, no silent overwrite; see [`../docs/security.md`](../docs/security.md) and [`../docs/validator-audit.md`](../docs/validator-audit.md)). The audit shows that none of the SVGs evaluated in the paper fails the stricter validator; the three round-2 files only carry `<title>`/`<desc>` warnings.

## What is in the paper

Abstract and introduction; related work; the task and protocol; the geometry (half-turn, feasible set, even/odd parts, compromise strokes, canon and dictionary, silhouette, a symmetry diagnostic); the pilot rounds with costs and lessons; threats to validity; future work; references.

## How it relates to the rest of the repository

| Paper section | Repository material |
|---|---|
| 1 Introduction | [`README.md`](../README.md), [`docs/how-it-works.md`](../docs/how-it-works.md) |
| 2 Related work | [`docs/related-work.md`](../docs/related-work.md), [`docs/references.md`](../docs/references.md) |
| 3 Task and protocol | [`docs/methodology.md`](../docs/methodology.md), [`prompts/`](../prompts/), [`scripts/`](../scripts/) |
| 4 Geometry | [`docs/geometry.md`](../docs/geometry.md), [`docs/worked-example.md`](../docs/worked-example.md) |
| 5 Pilot rounds (0–3) | [`rounds/`](../rounds/) (round 4 is post-paper, see above), [`docs/prompt-evolution.md`](../docs/prompt-evolution.md) |
| 6 Threats to validity | [`docs/threats-to-validity.md`](../docs/threats-to-validity.md) (extended for round 4) |
| 7 Future work | [`docs/future-work.md`](../docs/future-work.md) (updated after round 4) |

## Reference checking

Every reference was checked against a publisher, library, preprint-server or museum record on 29 October 2026 (details in [`../docs/references.md`](../docs/references.md)). Two items were **not** consulted directly (Whistler & Fuller 1960; the Gombrich/Kris texts); they are cited by catalogue record or by their bibliographic data only.

## License and citation

The paper is licensed under CC BY 4.0 (see [`../LICENSING.md`](../LICENSING.md)). To cite it, see [`../CITATION.cff`](../CITATION.cff).
