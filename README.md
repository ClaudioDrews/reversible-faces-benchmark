# Reversible Faces Benchmark

A small, one-shot benchmark that asks an LLM to draw **one SVG that shows two different faces: one when you look at it upright, and a different one when you turn it upside down.** This is the trick behind Rex Whistler's *reversible faces* in the book *OHO! Certain Two-Faced Individuals* (1946).

The drawing must also carry a **joke about a recent technology / AI event**, told only through the two faces. There is no caption, no text in the image, and no follow-up: the model gets one prompt, makes one attempt, and a human looks at the result (turning the phone in their hand).

<p align="center"><img src="assets/previews/round-03__minimax-m3.1-flash_prompt-v5.png" alt="Round 3 example: MiniMax output, upright and rotated 180 degrees" width="720"></p>
<p align="center"><em>Round 3 output from one of the tested models (MiniMax, prompt v5). Left: as drawn. Right: the same file rotated 180°. Previews are for illustration only; the benchmark is judged on the SVG itself.</em></p>

This repository contains the full story so far: the task design, every prompt version (v1–v5), the scripts, all generated SVGs, raw model responses, costs, and the human evaluations from three rounds (plus an unevaluated pilot, round 0), including a round that **made things worse** and what we learned from it.

> **Status:** early research / work in progress. Three rounds, three cheap models, **one human evaluator who is also the author of the benchmark**, one run per model per prompt. There is no scoring scale: verdicts are qualitative. Treat the results as design notes rather than a leaderboard.
>
> **Heads-up:** the prompts contain short text descriptions of two Whistler drawings that were drafted from public images and **never verified** (each prompt says so). They are kept verbatim because the models saw them, **including the literal production note "[PLACEHOLDER — Cláudio to add and verify.]" and the assertion that the drawings are "public domain"**, which is itself unverified. The events named in the rounds are whatever each model declared; they were **not fact-checked** by this repository.

## Abstract

The Reversible Faces Benchmark (RFB) asks a language model to write **one SVG file that shows one face when viewed upright and a different face when rotated by 180°**, in the tradition of Rex Whistler's reversible faces. The drawing must also carry a joke about a recent technology or AI event, told only through the two faces, with no text. The model receives one prompt, makes one attempt, and a human judges the result by turning the page. The task combines three abilities that models usually exercise separately: spatial reasoning under a rotation that cannot be checked by eye while writing code, drawing quality, and humor.

This repository gives a formal description of the geometry (a half-turn acting as an involution, a feasible set defined by two recognition regions, and a closed-form rule for compromise strokes), the one-shot protocol and file contract, and the results of three human-evaluated rounds with three models. The main empirical finding is negative and instructive: **in the single run per model, adding event and art instructions (prompt v4, with several changes at once) coincided with all three models losing the 180° reading**, while a rebuilt prompt with reversibility as the absolute priority and a staged workflow (v5) restored identifiable faces in both orientations for all three (DeepSeek ran with reasoning disabled in that round and is not comparable with the other two). The evidence is weak (single author-evaluator, three models, one run each, no repeats) and is presented as such.

**Contributions.** (i) A formal description of reversibility and of the construction rules used in the prompt; (ii) a one-shot protocol and file contract; (iii) three pilot rounds, including one that made things worse, with the lessons that followed; (iv) an explicit list of threats to validity and of experiments needed before any comparative claim.

Full text: [`paper/reversible-faces-benchmark-paper.md`](paper/reversible-faces-benchmark-paper.md) (version 2.0, 29 October 2026). To cite: see [How to cite](#how-to-cite).

---

## Contents

- [Abstract](#abstract)
- [Why this is hard](#why-this-is-hard)
- [What is being tested](#what-is-being-tested)
- [Design decisions](#design-decisions)
- [The geometry in one page](#the-geometry-in-one-page)
- [The three rounds](#the-three-rounds)
- [Models, settings and costs](#models-settings-and-costs)
- [Repository layout](#repository-layout)
- [How to run it](#how-to-run-it)
- [Limitations and honest notes](#limitations-and-honest-notes)
- [Future work](#future-work)
- [References and related work](#references-and-related-work)
- [How to cite](#how-to-cite)
- [License](#license)

---

## Why this is hard

A reversible face is **one set of strokes read in two orientations**. A curve that is a smile in the upright face must, after a 180° turn, be something meaningful in the other face (a hat band, for example). The eyes can be shared, but everything around them is reinterpreted: the hat of one face becomes the beard of the other, the chin becomes the crown, left and right swap.

The author's informal observation (not a measured result, and diffusion models were not tested in this repository) is that both LLMs writing SVG and diffusion image models rarely manage a convincing Whistler-style reversible caricature on their own. The task combines three things that models usually do separately:

1. **Spatial reasoning under a rotation** that cannot be checked by eye while writing code.
2. **Drawing quality**: line, caricature, character, composition.
3. **Humor**: a witty point expressed through the drawing alone.

## What is being tested

The benchmark looks at three abilities, plus a requirement tying the joke to the real world:

| # | Ability | What a human looks for |
|---|---|---|
| 1 | **A convincing two-face image** | Do both orientations read as faces, and are they clearly different faces? Is it really one set of strokes, not two drawings overlaid? |
| 2 | **Artistic quality** | Does it look like a confident caricature (line, character, composition) and not a diagram? |
| 3 | **Humor through the technique** | Does the *contrast between the two faces* tell a joke, with no text? |
| + | **Current events** | Is the joke about a specific, recognizable recent technology/AI event, used in an impactful way? |

The prompt gives the model what it needs to *understand the task* and to *plan a sensible strategy* (the geometry, a workflow, a failure catalog). The benchmark measures what the model does with that help, in one attempt.

## Design decisions

**One-shot.** The model receives a single prompt, produces a single SVG, and nobody answers questions or gives feedback. The models in the rounds had no tools (they could not run code, render the SVG or search); they could only check their output by reasoning, using the symbolic check the prompt describes.

**The human is the judge, with no rubric.** Anyone looking at the result can instinctively tell whether the two faces work, whether it is well drawn, and whether it is funny. We deliberately dropped the scoring rubric, the scoring gates, the anonymized evaluator sheets and the statistical protocol that appeared in earlier design drafts (see [`docs/design-history/`](docs/design-history/), which is **superseded**: it describes a heavier design than the one run). The only "criteria" that exist are the **self-check list inside the prompt**, which the *model* uses to judge its own work before delivering.

**Why SVG (for v1).** The first version targets LLMs, which can write text but not paint pixels. SVG is plain text, valid in any browser, inspectable, rotatable with one attribute, and cheap to produce and store. It also forces explicit geometry: the model has to reason about coordinates and rotation, which is the heart of the task. (A later version could target image/diffusion models.)

**Task variant.** Prompt v5 requires **two distinct characters** who differ in expression, not only in accessories. The variant "one person with two expressions" was left out of this version; it is probably harder and is listed under future work.

**File contract.** One standalone SVG: `xmlns`, `viewBox="0 0 1000 1000"`, `width`/`height`, valid XML, no text, no external references, no gradients/filters/lighting (a directional light flips with the rotation and breaks the illusion), at most 300 KB.

**Self-check list inside the prompt.** In prompt v5 the model is asked to pass three gates in this order: **Gate 1** reversibility (both readings are clear faces), **Gate 2** contrast (A and B look different), **Gate 3** light touches (one simple event prop per face, varied line weight, nobody demeaned), and to delete any touch that endangers a reading. Common failures are listed with fixes (see the prompts). Earlier prompt versions used different checklists (see [`docs/prompt-evolution.md`](docs/prompt-evolution.md)).

## The geometry in one page

All coordinates use a 1000 × 1000 page with the center C = (500, 500). Turning the page by 180° sends every point to

```
R(p) = 2C − p      i.e.      (x, y)  →  (1000 − x, 1000 − y)
```

In SVG: `transform="rotate(180 500 500)"` (not a mirror: `scale(-1,1)` is a different trick).

What the half-turn does (a rotation, not a mirror): straight lines keep their direction; a cup ∪ becomes a dome ∩; **left and right swap**; the vertical order flips.

The prompt gives the model a planning scaffold (explicitly "a design tool, not a law"):

- **Shared eyes** near (415, 500) and (585, 500): eyes stay eyes; the lids, brows and eye-bags change meaning and therefore the mood.
- A **canon** of vertical positions for a head about 600 px tall (hat dome ≈ y 320, brim ≈ 350, brow ≈ 452, eyes 500, nose tip ≈ 650, mouth ≈ 680, chin ≈ 800, collar ≈ 890, ...).
- A **dual-function dictionary**: a feature of face A at page height *y_A* is the same stroke as a feature of face B at height *y_B* **in B's own frame**, where *y_A = 1000 − y_B*. (The shipped prompts word this more loosely as "a feature of B at height −y (as seen on the page)"; the docs and the paper use the precise statement. See [`docs/geometry.md`](docs/geometry.md).) For example: A's smile (∪ at y ≈ 680) = B's hat band (dome at y ≈ 320); A's hat/hair = B's beard; A's brows = B's eye-bags; A's hat brim or fringe = B's nose; A's bow tie = B's pompom.
- A **sum rule** (every exaggeration in A is paid by its partner in B; hats, hair, beards and collars absorb leftovers) and **compromise strokes** (a shared stroke sits at the average of where A wants it and where the rotated B wants it).
- A tiny, deliberately **neutral mechanism example** (not a face) showing one stroke serving two roles and one B-only stroke in a rotated group.

A rotationally symmetric figure (the same face twice) is a **failure mode**, not a success.

More detail is in [`docs/how-it-works.md`](docs/how-it-works.md); the formal statement (involution and C₂, feasible set, even/odd parts, ε-ball condition ‖a − R(b)‖ ≤ 2ε, weighted compromise stroke, silhouette envelope, symmetry diagnostic ρ) is in [`docs/geometry.md`](docs/geometry.md); an annotated real output is in [`docs/worked-example.md`](docs/worked-example.md); the terms are in [`docs/glossary.md`](docs/glossary.md). The canon, the tolerance and the dictionary are design heuristics, and none of the formal quantities was computed in the rounds.

## The three rounds

Round 0 was a pilot; the human-evaluated rounds are 1, 2 and 3. Every round used the same three inexpensive models. Image strips below always show, from top to bottom: DeepSeek, GLM, MiniMax.

| Round | Prompt | Human verdict (see each round's `EVALUATION.md`) |
|---|---|---|
| 0 (pilot, not evaluated) | v1 | — |
| 1 | v2 (MiniMax), v3 (DeepSeek, GLM) | Effect OK on DeepSeek and MiniMax, weak on GLM; none has much artistic quality; two are mildly funny; none uses current events in an impactful way. |
| 2 | v4 | "It got a lot worse. Now there is no image at 180° anymore." |
| 3 | v5 | "In this third round all three models did better. All of them managed to make identifiable images in both orientations, and the artistic quality improved." |

### Lessons

1. **Mechanics can be taught, to a degree.** Giving the model the rotation math, a dual-function dictionary and a skeleton-first workflow produced two-face drawings in round 1 that the evaluator found OK for two of three models. (That result did not hold when more instructions were added in round 2.)
2. **Reversibility has to be the absolute priority.** Round 2 added a lot (a central, impactful event; heavy art direction: exaggeration, varied line weight, palette, composition, hatching, "would it look good framed?"). The models obeyed the art and event instructions and **lost the 180° reading in all three outputs**. More instructions pulled attention away from the hard geometric part.
3. **Fix: go back, make it smaller, put it in stages.** Round 3's prompt started again from the round-1 prompt, stated an explicit priority order, and split the work into stages: (1) geometry only, (2) verify by rotating coordinates, (3) style only after that, with only three short art cues and a light version of the event requirement. All three models then produced identifiable faces in both orientations, and the evaluator judged the artistic quality *better than before* (a relative statement: in round 1 he had said none had much artistic quality, and the drawings are still simple).
4. **Event use is still weak.** In round 3 the event is often only hinted at (a vague label, a small prop). Making the event central without destroying the illusion is the open problem.
5. **Models behave very differently under the same prompt.** DeepSeek went into endless verification loops with reasoning on in round 3 (four runs hit the token limit without delivering any SVG). It delivered only with reasoning turned off, so that result is not comparable with the others. MiniMax needed low effort to avoid token blowouts. GLM was the cheapest and the most consistent.

Per-round details, previews, raw outputs and costs: [`rounds/round-01`](rounds/round-01), [`rounds/round-02`](rounds/round-02), [`rounds/round-03`](rounds/round-03) (and the pilot in [`rounds/round-00-pilot`](rounds/round-00-pilot)). How the prompt evolved: [`docs/prompt-evolution.md`](docs/prompt-evolution.md).

#### Round 1 (prompts v2/v3)
<img src="assets/previews/round-01__all-models.png" alt="Round 1 results" width="640">

#### Round 2 (prompt v4): the 180° face was lost
<img src="assets/previews/round-02__all-models.png" alt="Round 2 results" width="640">

#### Round 3 (prompt v5): both faces back
<img src="assets/previews/round-03__all-models.png" alt="Round 3 results" width="640">

## Models, settings and costs

All calls went through [OpenRouter](https://openrouter.ai), one-shot, no tools (the models could not run code or search), with the prompt as the only message.

| Model (OpenRouter id) | Notes |
|---|---|
| `deepseek/deepseek-v4.1-flash` | Overthinks with reasoning on; round 3 result produced with reasoning disabled. |
| `z-ai/glm-5.3-flash` | Cheapest; default reasoning effort (medium). |
| `minimax/minimax-m3.1-flash` | Heavy reasoning; low effort used in rounds 2 (second attempt) and 3. |

Approximate cost of the delivered runs per round (USD, as reported by OpenRouter):

| Round | Delivered runs | Everything incl. failed/truncated attempts |
|---|---|---|
| 0 pilot (v1) | 0.075 | 0.075 |
| 1 (v2/v3, evaluated outputs) | 0.057 | 0.080 (also v2 runs for DeepSeek/GLM that were not evaluated) |
| 2 (v4) | 0.052 | 0.091 |
| 3 (v5) | 0.030 | 0.194 (+ one timed-out request, cost not reported) |

The whole project so far cost roughly half a dollar in model calls. Exact per-run tokens and costs are in each round's `logs/` and `EVALUATION.md`.

## Repository layout

```
reversible-faces-benchmark/
README.md                 this file
CITATION.cff              how to cite (CFF 1.2.0)
LICENSE                   MIT (code in scripts/)
LICENSE-CONTENT           CC BY 4.0 (everything else)
LICENSING.md              what is covered by which license
paper/
  reversible-faces-benchmark-paper.md   the accompanying paper (v2.0)
  README.md               status of the paper and how it maps to the repo
docs/
  how-it-works.md         the task, half-turn math, dual-function dictionary
  geometry.md             the geometry stated formally
  glossary.md             terms used throughout
  worked-example.md       one real output, stroke by stroke
  methodology.md          one-shot design, human judgment, file contract, run settings
  prompt-evolution.md     what changed from v1 to v5, and why
  related-work.md         literature map and how RFB differs
  references.md           verified bibliography and what was checked
  threats-to-validity.md  what limits the conclusions
  future-work.md          experiments still needed
  design-history/         earlier design specs (v0.3, v0.4): SUPERSEDED, kept for context
  reviews/                critiques of the prompt/repo/paper integration by a second agent (summaries)
prompts/
  prompt-v1.md ... prompt-v5.md   the exact prompts sent to the models
  discarded/prompt-v5b.md         a variant that did not fix the DeepSeek loop
rounds/
  round-00-pilot/ round-01/ round-02/ round-03/
      EVALUATION.md       human evaluation, models, settings, costs, lessons
      svg/                the evaluated SVGs
      raw/                raw model answers (and reasoning traces where available)
      logs/               token and cost logs
scripts/
  run_models.py           one-shot runner (OpenRouter; key from environment)
  validate_svg.py         checks parts of the file contract (size, XML, viewBox, forbidden elements)
  render_preview.py       upright + rotated side-by-side PNG (README previews only)
assets/previews/          PNG previews
```

## How to run it

Requirements: Python 3.9+, `Pillow` (previews only), and Chrome/Chromium for previews.

```bash
git clone https://github.com/<your-account>/reversible-faces-benchmark.git
cd reversible-faces-benchmark

# 1. Run a prompt one-shot on one or more models (set your key in the environment, never in files)
export OPENROUTER_API_KEY=...
python scripts/run_models.py runs/my-run prompts/prompt-v5.md \
    deepseek/deepseek-v4.1-flash z-ai/glm-5.3-flash minimax/minimax-m3.1-flash

# Settings used in the rounds:
EFFORT=low python scripts/run_models.py runs/mm prompts/prompt-v5.md minimax/minimax-m3.1-flash
NOREASON=1 MAXTOK=20000 python scripts/run_models.py runs/ds prompts/prompt-v5.md deepseek/deepseek-v4.1-flash
STRIP_METADATA=1 python scripts/run_models.py ...        # remove <title>/<desc> (used from round 3)

# 2. Check the file contract
python scripts/validate_svg.py runs/my-run/*.svg

# 3. Look at it: open the .svg in a browser, then turn your phone (or the page) 180 degrees.
#    Optional side-by-side preview:
python scripts/render_preview.py runs/my-run/minimax-m3.1-flash.svg preview.png
```

The judgment is human: open the SVG, look at it, rotate, and decide. Write your verdict next to the round, as in `rounds/*/EVALUATION.md`.

## Limitations and honest notes

- One human evaluator, who is also the author of the benchmark, which is a conflict of interest. Three models; one run per model per prompt (apart from retries after technical failures). No statistics are claimed. Verdict words such as "OK", "somewhat bad" or "low" are informal labels, not points on a scale (see `docs/methodology.md`).
- The prompts include short text descriptions of two Whistler drawings that were **drafted from public images and never verified** (the prompts say so in a placeholder note). They are kept verbatim because they are part of what the models saw.
- Models did not have search, so the "recent event" is whatever they know; several chose events from 2023–2025.
- Some SVGs in round 2 contain `<title>`/`<desc>` metadata that names the event. The runner now strips it, because it appears as a tooltip when hovering in a desktop browser and gives the joke away.
- The original Whistler drawings are **not** bundled here. See [`docs/related-work.md`](docs/related-work.md) and [`docs/references.md`](docs/references.md).
- The full list of threats to validity (uneven comparisons, heuristic geometry, untested diffusion claim, and more) is in [`docs/threats-to-validity.md`](docs/threats-to-validity.md).
- Model names are the OpenRouter ids used at the time; providers may change or retire them.

## Future work

Nothing below has been done. Details: [`docs/future-work.md`](docs/future-work.md).

- A v3-versus-v5 ablation and a with/without-geometry-kit condition, under identical model settings.
- Adding event and art instructions in small steps, checking the 180° reading after each.
- More runs, more models and more judges, with blind presentation and randomized orientation order.
- A tool-enabled condition (the model can render and rotate its output).
- The second mode, "one person with two expressions".
- An unvalidated stroke-sharing diagnostic (Q_shared).

## References and related work

The verified bibliography (with what was checked for each entry) is in [`docs/references.md`](docs/references.md); how the benchmark relates to Whistler, face-inversion research, ambigram generation (Loviscach, AmbiGen, Ambifusion, Visual Anagrams, Polster), LLM drawing (Bubeck et al.) and humor/caricature theory (Suls; Kris & Gombrich) is in [`docs/related-work.md`](docs/related-work.md). The original Whistler drawings are not included in this repository.

## How to cite

Cláudio Drews (2026). *Reversible Faces Benchmark: a one-shot test of rotation-consistent line drawing in language models* (version 2.0, the version of the repository and of the paper). See [`CITATION.cff`](CITATION.cff); GitHub shows a "Cite this repository" button once the file is published.

## License

Copyright (c) 2026 Cláudio Drews.

- **Code** (`scripts/`): MIT, see [`LICENSE`](LICENSE).
- **Content** (paper, docs, prompts, evaluations, logs, SVGs, raw outputs, previews): CC BY 4.0, see [`LICENSE-CONTENT`](LICENSE-CONTENT).

Details and caveats about AI-generated outputs: [`LICENSING.md`](LICENSING.md).
