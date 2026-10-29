# Documentation map

All technical documents sit directly in `docs/`; this page only tells you where to start. It does not duplicate their content.

## By reader interest

| If you want to... | Read |
|---|---|
| Understand the problem | [`how-it-works.md`](how-it-works.md), [`worked-example.md`](worked-example.md), [`glossary.md`](glossary.md) |
| Study the mathematics | [`geometry.md`](geometry.md) |
| Understand the experiments | [`methodology.md`](methodology.md), [`prompt-evolution.md`](prompt-evolution.md), the index of rounds in [`../rounds/README.md`](../rounds/README.md) |
| Reproduce the results | [`reproduction.md`](reproduction.md), [`security.md`](security.md) |
| Examine the scientific grounding | [`related-work.md`](related-work.md), [`references.md`](references.md) |
| Assess the limitations | [`threats-to-validity.md`](threats-to-validity.md), [`validator-audit.md`](validator-audit.md) |
| Explore future work | [`future-work.md`](future-work.md), [`../to-do.md`](../to-do.md) |

## Other material

| Location | What it is |
|---|---|
| [`design-history/`](design-history/) | Earlier design specifications (v0.3, v0.4). **Superseded**: they describe a heavier design (weighted rubric, gates, blind protocol) than the one that was run. Kept for context. |
| [`reviews/`](reviews/) | Critiques written by David (Peter's Hermes agent) of the prompt, the repository and the round-4 design, and the pre-publication review; each lists what was applied and what was not. |
| [`../baselines/`](../baselines/README.md) | Fifteen additional comparison runs (not part of the rounds) with the judge comparison. |
| [`../paper/`](../paper/README.md) | The accompanying paper (version 2.0, rounds 0–3) and its scope note. |
| [`../PUBLISH-CHECKLIST.md`](../PUBLISH-CHECKLIST.md) | Pre-publication tasks and their status. |

## Historical versus current

Some documents describe the state of the project at a given time (the paper, the round evaluations, `design-history/`, the "before hardening" parts of [`security.md`](security.md)). Those parts say so explicitly. Statements about what the code does today (the validator, the harness limits, the security design) are about the current version 2.1.0.
