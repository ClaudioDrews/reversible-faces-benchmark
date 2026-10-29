# Glossary and terminology

The README, the docs and the [paper](../paper/reversible-faces-benchmark-paper.md) use these terms the same way.

| Term | Meaning |
|---|---|
| **RFB** | Reversible Faces Benchmark: the task and protocol described in this repository. |
| **Reversible face** | One set of strokes that reads as one face upright and as a different face after a 180° turn. |
| **Face A** | The face seen when the SVG is displayed as drawn (the *page frame*). |
| **Face B** | The face seen after the half-turn. B is constructed as a face that is upright in its **own frame** (the frame obtained by turning the page). |
| **Half-turn** | The 180° rotation about the page center C = (500, 500): R(p) = 2C − p, that is (x, y) → (1000 − x, 1000 − y). In SVG: `transform="rotate(180 500 500)"`. It is a rotation, not a mirror. Earlier docs sometimes said just "the rotation". |
| **Reading** | One interpretation of the drawing: reading A (as drawn) or reading B (after the half-turn). |
| **Shared stroke / double-duty stroke** | A stroke drawn once that has a role in both readings (for example A's smile is B's hat band). |
| **Compromise stroke** | A shared stroke placed at the (weighted) average of where A wants it and where B (rotated onto the page) wants it. |
| **B-only stroke** | A stroke that matters only in reading B. It is drawn inside a `<g transform="rotate(180 500 500)">` group and should be inert in A. |
| **Canon** | The vertical positions used for a head of height H = 600 px with the eyes at y = 0. Page position = 500 + 600·y. |
| **Dual-function dictionary** | The table of which feature of A is the same stroke as which feature of B. |
| **Page y vs. B-frame y** | The dictionary pairs a feature of A at height y_A on the page with a feature of B at height y_B in **B's own frame**, where y_A = 1000 − y_B (in page units) or y_A = −y_B (in units of H relative to the eyes). |
| **Sum rule** | Every exaggeration in A must be paid by its partner in B; hats, hair, beards, collars and wrinkles absorb leftovers. |
| **Free variable** | A feature that has no fixed partner (hair mass, hats, beards, collars, wrinkles). |
| **One-shot** | One prompt, one attempt, one SVG per model; no feedback. |
| **Round** | One batch of one-shot runs on the three models, normally of one prompt version (round 1 mixed v2 and v3; see its evaluation). Round 0 is a pilot that was not human-evaluated. |
| **Tool-enabled condition** | Round 4: the model may call a sandboxed Python tool and a render tool in a loop (at most 5 renders) before delivering. Rounds 0–3 had no tools. |
| **Harness** | The program that runs a model (`scripts/run_models.py` one-shot; `scripts/run_models_v6.py` for the tool loop), enforces the limits and records everything. |
| **Prompt version** | v1 to v6 (plus the discarded v5b); see [`prompt-evolution.md`](prompt-evolution.md). |
| **Event** | The recent technology/AI event that the joke is about, as declared by the model (`EVENT:` line). It is not fact-checked. |
| **Verdict words** | The evaluator's informal labels ("OK", "somewhat bad", "low", ...); see [`methodology.md`](methodology.md). |
| **A, B vs. a, b** | A and B name the two faces. In the geometry pages, a is the target position of a stroke in A (page frame) and b its target in B's own frame, so R(b) is B's target on the page. |
| **Evaluator** | The human judge. In all rounds so far: the benchmark's author. |
