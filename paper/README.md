# Paper

**`reversible-faces-benchmark-paper.md`** is the accompanying paper for this repository: *Reversible Faces Benchmark: a one-shot test of rotation-consistent line drawing in language models* (Cláudio Drews, version 2.0, 29 October 2026).

## Status

- **Early research, not peer reviewed.** A benchmark design plus three informal pilot rounds.
- **One human evaluator, who is also the author.** Three inexpensive models, one run per model per prompt. No statistics are claimed. The results are design notes, not a leaderboard.
- The paper describes the design that was actually run (one-shot, no tools, human judgment with no rubric). The older v0.3/v0.4 specifications in [`../docs/design-history/`](../docs/design-history/) describe a heavier design (weighted rubric, gates, blind protocol, tool use) that was **not** used and is superseded.

## What is in the paper

Abstract and introduction; related work; the task and protocol; the geometry (half-turn, feasible set, even/odd parts, compromise strokes, canon and dictionary, silhouette, a symmetry diagnostic); the pilot rounds with costs and lessons; threats to validity; future work; references.

## How it relates to the rest of the repository

| Paper section | Repository material |
|---|---|
| 1 Introduction | [`README.md`](../README.md), [`docs/how-it-works.md`](../docs/how-it-works.md) |
| 2 Related work | [`docs/related-work.md`](../docs/related-work.md), [`docs/references.md`](../docs/references.md) |
| 3 Task and protocol | [`docs/methodology.md`](../docs/methodology.md), [`prompts/`](../prompts/), [`scripts/`](../scripts/) |
| 4 Geometry | [`docs/geometry.md`](../docs/geometry.md), [`docs/worked-example.md`](../docs/worked-example.md) |
| 5 Pilot rounds | [`rounds/`](../rounds/), [`docs/prompt-evolution.md`](../docs/prompt-evolution.md) |
| 6 Threats to validity | [`docs/threats-to-validity.md`](../docs/threats-to-validity.md) |
| 7 Future work | [`docs/future-work.md`](../docs/future-work.md) |

## Reference checking

Every reference was checked against a publisher, library, preprint-server or museum record on 29 October 2026 (details in [`../docs/references.md`](../docs/references.md)). Two items were **not** consulted directly (Whistler & Fuller 1960; the Gombrich/Kris texts); they are cited by catalogue record or by their bibliographic data only.

## License and citation

The paper is licensed under CC BY 4.0 (see [`../LICENSING.md`](../LICENSING.md)). To cite it, see [`../CITATION.cff`](../CITATION.cff).
