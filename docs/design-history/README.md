# Design history (superseded)

These are the design specifications that preceded the benchmark as it was actually run:

- `spec-v0.3.md`
- `spec-v0.4.md`

**They are superseded.** They describe a heavier design than the one used in rounds 0–3: a weighted scoring rubric with gates, a three-evaluator blind protocol with randomized orientation order, models allowed to use tools (code execution, rendering, search) with up to five render-and-correct cycles, a 500 KB file limit and a 90-day event window.

What was actually run: **one-shot, no tools, a human judge with no rubric, 300 KB limit** (see [`../methodology.md`](../methodology.md) and the [paper](../../paper/reversible-faces-benchmark-paper.md)). The rubric, gates and statistical protocol were dropped because a person can judge the three things directly. They are kept here for context and as a possible starting point for a more formal future version ([`../future-work.md`](../future-work.md)). Wherever the specs and the rest of the repository disagree, the rest of the repository is correct.
