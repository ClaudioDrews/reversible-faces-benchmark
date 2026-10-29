# Reversible Faces Benchmark: a one-shot test of rotation-consistent line drawing in language models

**Author:** Cláudio Drews  
**Version:** 2.0 (29 October 2026). This version describes the design that was actually run (one-shot, no tools, human judgment, no rubric). The earlier v0.3/v0.4 specifications are kept for context in [`docs/design-history/`](../docs/design-history/).  
**Status:** early research. A benchmark design plus three informal pilot rounds. **One human evaluator, who is also the author. Three inexpensive models. One run per model per prompt. No statistics are claimed.** The results are design notes, not a leaderboard.  
**Repository:** this paper accompanies the files in this repository ([`README.md`](../README.md), [`docs/`](../docs/), [`prompts/`](../prompts/), [`rounds/`](../rounds/), [`scripts/`](../scripts/)). Bibliography details and how each reference was checked: [`docs/references.md`](../docs/references.md).  

---

## Abstract

The Reversible Faces Benchmark (RFB) asks a language model to write **one SVG file that shows one face when viewed upright and a different face when rotated by 180°**, in the tradition of Rex Whistler's reversible faces. The drawing must also carry a joke about a recent technology or AI event, told only through the two faces, with no text. The model receives one prompt, makes one attempt, and a human judges the result by turning the page. The task combines three abilities that models usually exercise separately: spatial reasoning under a rotation that cannot be checked by eye while writing code, drawing quality, and humor.

We give a formal description of the geometry (a half-turn acting as an involution, a feasible set defined by two recognition regions, and a closed-form rule for compromise strokes), the one-shot protocol and file contract, and the results of three human-evaluated rounds with three models. The main empirical finding is negative and instructive: **in the single run per model, adding event and art instructions (prompt v4, with several changes at once) coincided with all three models losing the 180° reading**, while a rebuilt prompt with reversibility as the absolute priority and a staged workflow (v5) restored identifiable faces in both orientations for all three (DeepSeek ran with reasoning disabled in that round and is not comparable with the other two). The evidence is weak (single author-evaluator, three models, one run each, no repeats) and is presented as such.

**Keywords:** reversible faces; ambigrams; rotational symmetry; SVG generation; LLM evaluation; one-shot benchmark; human evaluation.

---

## 1. Introduction

A reversible face is **one set of strokes read in two orientations**. After a 180° turn, a curve that was a smile becomes something else (a hat band, for example), the hat of one face becomes the beard of the other, the chin becomes the crown, and left and right swap. Whistler's drawings were collected in the book *OHO! Certain Two-Faced Individuals* (1946), with verses by his brother Laurence Whistler [12]. The Salisbury Museum's Rex Whistler Archive dates the reversible faces to 1931–32 and records that they were first used in advertisements commissioned by Shell [12]. Rex Whistler died in 1944, so the 1946 book was assembled after his death.

The author's informal observation, not a measured result, is that both language models writing SVG and diffusion image models rarely produce a convincing Whistler-style reversible caricature unaided. Diffusion models were **not** tested in this work. RFB targets language models because SVG is plain text, valid in any browser, inspectable, rotatable with one attribute, and cheap to store, and because it forces explicit coordinates: the model has to reason about geometry it cannot see.

The benchmark looks at three abilities and one requirement tying the joke to the real world:

| # | Ability | What a human looks for |
|---|---|---|
| 1 | **A convincing two-face image** | Do both orientations read as faces, and are they clearly different faces? Is it one set of strokes, not two drawings overlaid? |
| 2 | **Artistic quality** | Is it a confident caricature (line, character, composition) rather than a diagram? |
| 3 | **Humor through the technique** | Does the *contrast between the two faces* tell a joke, with no text? |
| + | **Current events** | Is the joke about a specific, recognizable recent technology/AI event, used in an impactful way? |

The prompt supplies what the model needs to understand the task and plan a sensible strategy (geometry, a workflow, a failure catalog). The benchmark measures what the model does with that help in one attempt.

**Contributions.** (i) A formal description of reversibility and of the construction rules used in the prompt; (ii) a one-shot protocol and file contract; (iii) three pilot rounds, including one that made things worse, with the lessons that followed; (iv) an explicit list of threats to validity and of experiments needed before any comparative claim.

## 2. Background and related work

**Whistler and reversible faces.** Wade and Nekes give an account of Whistler's two-faced drawings [1]. Whistler and Fuller's 1960 catalogue of his work [13] was not consulted directly. This repository does not bundle the original drawings.

**Face orientation.** Face processing is sensitive to orientation: inversion impairs face recognition more than it impairs recognition of other objects [2], and local feature changes become hard to notice in an inverted face (the Thatcher illusion [3]). This motivates one design choice in the prompt: B must be constructed as a face that is *upright in the rotated frame*, with its own eyes, nose, mouth and hat or hair, rather than hoped for as an accident of A's strokes. These results are context for the task, not evidence that any automatic classifier can judge Whistler-style drawings.

**Ambigrams and multi-view illusions.** Rotational ambigrams, letter designs that read differently when turned, pose an analogous problem in typography. Loviscach searched a dictionary for nearly point-symmetric words and made them exact with a vector editor that enforces 180° symmetry and fuses shapes smoothly [4]. AmbiGen optimizes glyph outlines by distilling a pretrained diffusion model so that a word is legible in both orientations [5]. Ambifusion trains a diffusion model that generates ambigram images for letter pairs [6]. Visual Anagrams produces images whose interpretation changes under transformations such as a 180° rotation, by combining noise estimates from the different views during denoising [7]. Polster's "Mathemagical Ambigrams" is a complementary construction-oriented reference [8]. These systems address letters or raster images. RFB differs in five ways: the output is a single SVG written as code, the content is a pair of faces rather than letters, the shared structure is anatomical rather than glyph-to-glyph, the drawing must carry a joke, and the generator is a language model that cannot see its output.

**LLMs drawing with code.** Early experiments with a text-only early version of GPT-4 showed that a language model can write drawing code (TikZ, SVG) for recognizable objects without seeing the result [9]. RFB pushes this to a task where correctness depends on a transformation the model cannot visualize.

**Humor and caricature.** The two-reading structure maps naturally onto incongruity-resolution accounts of humor [10]: the incongruity is two faces from one set of strokes, and the resolution is the rule that connects them (promise versus consequence). Caricature is commonly described as deliberate exaggeration of distinctive features [11]. The prompt's three "art cues" (varied line weight, exaggeration, asymmetric silhouette) are practical stand-ins for this; they are not derived from, or validated against, the cited literature.

## 3. The task and the protocol

**One-shot.** The model receives one prompt as its only message and produces one SVG. Nobody answers questions or gives feedback. If a call fails for technical reasons (timeout, token limit with no answer) it is retried, changing only a setting such as reasoning effort, never the prompt (the single exception is the discarded variant [`prompts/discarded/prompt-v5b.md`](../prompts/discarded/prompt-v5b.md)). All retries and costs are logged.

**No tools.** All calls went through OpenRouter with no tools: the models could not run code, render the SVG, or search the web. The prompts are therefore written for blind drawing, with a cheap symbolic check (Section 4.6) in place of rendering. The "recent event" is whatever the model knows.

**File contract.** One standalone SVG with `viewBox="0 0 1000 1000"`, `width="1000" height="1000"`, valid XML, no external references, at most 300 KB. Forbidden: any text, `<image>`, `<foreignObject>`, `<script>`, gradients, blur or filters, drop shadows and any directional lighting (a light direction flips with the rotation and breaks the illusion). Allowed: line work, hatching, flat fills, a small flat palette, white space. From prompt v4 on, the model replies with two plain lines, `EVENT:` and `TITLE:`, followed by the SVG. From round 3 on, any `<title>`, `<desc>` and `<metadata>` is stripped by the runner, because it appears as a tooltip and gives the joke away.

**Task variant.** Prompt v5 requires two distinct characters, A and B, that differ in expression and not only in accessories (at least two of eye opening, brow angle, mouth curve, jaw width, age), and a joke stated as a drawn difference ("A has X / B has Y"). The "one person with two expressions" variant was left out of this version.

**Human judgment, no rubric.** A human opens the SVG in a browser, looks at it, turns it upside down, and judges three things: whether both faces are convincing, how good the drawing is, and whether the joke works, plus whether a specific event is recognizable. Verdict words ("OK", "somewhat bad", "low", "somewhat funny", "not used in an impactful way") are informal labels, defined roughly in [`docs/methodology.md`](../docs/methodology.md), not points on a scale. Earlier design drafts (`docs/design-history/`, specs v0.3 and v0.4) had a weighted rubric, scoring gates, anonymized evaluator sheets and a statistical protocol. They were dropped because a person can judge the three things directly, and a rubric is more useful to the model than to the judge. The only explicit criteria are the self-check list inside the prompt, which the *model* uses before delivering.

## 4. Geometry

All coordinates use the 1000 × 1000 page with center C = (500, 500). The prompt presents this material as "a design tool, not a law": Whistler drew by hand, and the numbers are scaffolding for a model that cannot see what it draws.

### 4.1 The half-turn

$$R_C(p) = 2C - p, \qquad R_C \circ R_C = \mathrm{id}. \qquad (1)$$

On the page this is $(x,y) \mapsto (1000-x,\,1000-y)$, and in SVG `transform="rotate(180 500 500)"`. It is a proper rotation ($\det = +1$), **not** a mirror: `scale(-1,1)` has $\det=-1$ and is a different genre of illusion (equivalently, a half-turn is a reflection in both axes). The map generates the group $C_2=\{e,R_C\}$. Lines keep their direction, a cup ∪ becomes a dome ∩, left and right swap, and the vertical order flips. A reversible figure need not satisfy $R(I)=I$; full rotational symmetry is a failure mode (it shows the same face twice).

### 4.2 Feasible set

Let $P_A(I)$ and $P_B(I)$ be idealized scores for "I reads as face A" and "I reads as face B", and $\tau_A,\tau_B$ thresholds. Define $\mathcal C_A=\{I: P_A(I)\ge\tau_A\}$ and $\mathcal C_B=\{I: P_B(I)\ge\tau_B\}$. A drawing is a valid reversible pair when

$$I \in \mathcal S_{A,B} = \mathcal C_A \cap R[\mathcal C_B] = \{\, I : P_A(I)\ge\tau_A \ \text{and}\ P_B(RI)\ge\tau_B \,\}. \qquad (2)$$

(Here $R^{-1}=R$, so $R[\mathcal C_B]=R^{-1}[\mathcal C_B]$.) Equality of the two readings is not required, only membership in two legibility regions. The roles of the faces are interchangeable: $I\in\mathcal S_{A,B}$ if and only if $RI\in\mathcal S_{B,A}$, that is, $\mathcal S_{A,B}=R[\mathcal S_{B,A}]$. The scores $P$ and the thresholds are idealizations; in practice the "recognizer" is a human, and nothing here is calibrated.

### 4.3 Even and odd parts

For a rasterized image viewed as a real vector, $I_+=\tfrac12(I+RI)$ and $I_-=\tfrac12(I-RI)$ give $I=I_++I_-$ and $RI=I_+-I_-$. The even part is what the half-turn preserves; the odd part is what changes sign (and can be negative as an intensity). This decomposition is algebraic and does not by itself isolate the meanings of A and B. It is useful only to separate the content that survives rotation from the content that does not.

### 4.4 Shared strokes and compromise strokes

Let a stroke have target position $a$ in face A (page frame) and target position $b$ in face B's **own upright frame**. On the page, B's target sits at $R(b)$. A shared stroke $s$, drawn once, should be near both:

$$\|s-a\|_2\le\varepsilon,\qquad \|s-R(b)\|_2\le\varepsilon. \qquad (3)$$

Two closed balls of equal radius $\varepsilon$ intersect if and only if

$$\|a-R(b)\|_2\le 2\varepsilon. \qquad (4)$$

If the cost is $w_A\|s-a\|^2+w_B\|s-R(b)\|^2$ with $w_A,w_B>0$, the minimizer is

$$s^\ast=\frac{w_A\,a+w_B\,R(b)}{w_A+w_B}. \qquad (5)$$

For equal weights, $s^\ast=(a+R(b))/2$, which is also the minimizer of the worst deviation $\max\{\|s-a\|,\|s-R(b)\|\}$. This is the prompt's rule "take the average of where A wants it and where B wants it". Because Bézier curves are affine-covariant and $R$ is affine, (5) can be applied to corresponding control points of two Bézier curves of equal degree, provided the control points are paired consistently. Geometric closeness does not guarantee semantic recognition.

**Pitfall (double rotation).** If the formula already applies $R$ to $b$, the caller must pass $b$ in B's own upright frame. Passing $R(b)$ gives $R(R(b))=b$ and cancels the conjugation. The left/right swap must also be applied exactly once. (These two errors correspond to the "Swapped sides" and "Same orientation" entries in the prompt's failure table.)

### 4.5 Canon and dual-function dictionary

The prompt fixes a head height $H=600$ px with the eyes at $y=0$ and page position $500+600y$. With shared eyes at about (415, 500) and (585, 500), a feature of A at page height $y_A$ and a feature of B at height $y_B$ **in B's own frame** are the same strokes when $y_A = 1000-y_B$:

**Wording note.** The prompts the models received state the dictionary more loosely: "a feature of A at height y and a feature of B at height −y (as seen on the page)". The statement used in this paper, with B's heights in B's own frame, is the precise one; this affects how the prompts should be read, not the table below. The dictionary is also not a partition: a stroke near page y ≈ 320–350 can be B's mouth (via A's hat dome) and, for hair or hat masses spanning y 200–350, part of B's beard mass; the table lists typical pairings, not an exclusive assignment.

| Feature of A (page y) | is, in B (B-frame y) | Page-y check |
|---|---|---|
| eyes (500) | eyes (500) | anchor: lids and brows decide the mood |
| brow (452) | under-eye bag (548) | 1000 − 548 = 452 |
| hairline or fringe (380) | nose bridge (620) | 1000 − 620 = 380 |
| hat brim (350) | nose tip (650) | 1000 − 650 = 350 |
| hat or hair dome (320) | mouth (680): a smile is the band of a hat | 1000 − 680 = 320 |
| crown or top of hat (200) | chin (800) | 1000 − 800 = 200 |
| plume or pompom (110) | collar or bow tie (890) | 1000 − 890 = 110 |
| hair mass | beard, wrinkles, cheeks | free variable |

**Consequence.** Nothing below A's eyes can stay below B's eyes: A's mouth cannot be B's nose (A's mouth is at 680; B's nose tip lands at 350 on the page, 330 px away). A's mouth becomes B's hat zone, and B's nose comes from A's hat brim or fringe.

**Sum rule.** Recognition tolerates deviations of about $0.05H=30$ px from the canon, which corresponds to $\varepsilon\approx30$ px in (3)–(4). Every exaggeration in A must be paid by its partner in B (a very long nose in A means a lower hat brim in B). Hats, hair, beards, collars and wrinkles are free variables that absorb the leftovers. The canon values, the tolerance, and the pairs are **design heuristics**. They are not measured, not claimed as historical facts about Whistler, and not validated against human recognition.

### 4.6 The symbolic check used instead of rendering

Because the models cannot render, the prompt asks for a cheap check: for each double-duty stroke, write *A point (x, y) → R(p) = (1000 − x, 1000 − y) → what it is in B*, and for each expression curve write whether it is concave up or down on the page and what it becomes after the half-turn (a ∪ smile becomes a ∩ dome; a ∩ brow becomes a ∪ lid line).

### 4.7 Silhouette

One outline must contain both anatomies. For silhouettes that are star-shaped about C, with radial functions $r_A(\phi)$ and $r_{B}(\phi+\pi)$ (B's radius seen through the half-turn), an inclusive envelope is

$$r_0(\phi)=\max\{\,r_A(\phi),\; r_B(\phi+\pi)\,\}. \qquad (6)$$

Smoothing must not cut into either face. The operation $r_S=\max\{K\ast r_0,\ r_0\}$ with an averaging kernel $K$ preserves containment, but note what it does: it fills valleys of $r_0$ and keeps its peaks, so it guarantees containment, not smoothness at peaks. The prompt states this in words ("the wider of the two at each height... round it, but never cut it inside either face").

### 4.8 A symmetry diagnostic

$$\rho(I)=\frac{\|I-RI\|_2}{\|I\|_2}\in[0,2], \qquad \|I\|_2>0. \qquad (7)$$

$\rho=0$ means rotational symmetry (the same face twice). A high $\rho$ does not prove two faces and a low $\rho$ does not prove failure. None of the quantities in this section was computed in the three rounds; [`scripts/validate_svg.py`](../scripts/validate_svg.py) checks the file contract only.

### 4.9 A worked check

[`docs/worked-example.md`](../docs/worked-example.md) annotates one round-3 output (MiniMax, prompt v5) stroke by stroke. Three rows suffice to show the mechanism (vertical extents from the path coordinates):

| Stroke | Page y in A | Page y after the half-turn | Role in A | Role in B |
|---|---|---|---|---|
| Red lens-shaped stroke | 666–694 | 306–334 | smile (∪) | hat band (∩) |
| Two arched strokes above the eyes | 428–458 | 542–572 | raised brows | eye-bags |
| Small outlined shape between the cheeks | 545–598 | 402–455 | nose | forehead mark |

In that file, B-only strokes (angry brows, eyelids, a small clasp) are drawn in a `<g transform="rotate(180 500 500)">` group, where they stay inert in A.

## 5. Pilot rounds

Models used in every round (OpenRouter ids at the time): `deepseek/deepseek-v4.1-flash`, `z-ai/glm-5.3-flash`, `minimax/minimax-m3.1-flash`. Model names may change or be retired. Events named below are whatever each model declared; they were **not fact-checked** here.

| Round | Prompt | Human verdict (author-evaluator) |
|---|---|---|
| 0 (pilot, not human-evaluated) | v1 | Valid SVGs, weak expression contrast, oval heads with generic eyes, little visible joke, much budget spent on coordinate arithmetic (from a second-agent critique). |
| 1 | v2 (MiniMax), v3 (DeepSeek, GLM) | Effect "OK" for DeepSeek and MiniMax, "somewhat bad" for GLM; artistic quality "low" for all; DeepSeek and MiniMax "somewhat funny"; no use of current events "in an impactful way". |
| 2 | v4 | "It got a lot worse. Now there is no image at 180° anymore." All three lost the reversible effect. |
| 3 | v5 | "All three models did better. All of them managed to make identifiable images in both orientations, and the artistic quality improved." |

**Prompt changes.** v2 added an effort budget, the "joke as a physical difference" rule, a requirement that A and B differ in expression, and a symbolic check. v3 added a required technological accessory, "silhouette first", and bold line weights. After round 1 the author made the event central (v4) and added extensive art direction (exaggeration at 150–200%, varied line weight, hatching, palette, composition, "would it look good framed?"). v5 was rebuilt **from v3, not v4**, with an absolute priority order (reversibility, then contrast, then light touches), a staged workflow (1: geometry only; 2: verify by rotating coordinates; 3: style, undoing any touch that endangers a reading), a reversibility gate in the self-check, one droppable prop per face, three short art cues, and no `<title>`/`<desc>`. See [`docs/prompt-evolution.md`](../docs/prompt-evolution.md).

**Costs** (USD, as reported by OpenRouter; delivered runs / everything including failed attempts): round 0, 0.075 / 0.075; round 1, 0.057 / 0.080; round 2, 0.052 / 0.091; round 3, 0.030 / 0.194, plus one timed-out request with no reported cost. The whole project cost roughly half a dollar in model calls.

**Model behavior under the same prompt.** In round 3, DeepSeek kept re-verifying its own geometry with reasoning on (three configurations plus the v5b variant, four runs in total) until the token cap, and delivered no SVG; it delivered only with reasoning disabled, so its result is **not comparable** with the others. MiniMax needed low reasoning effort to avoid token blow-ups and had one 900 s timeout. GLM was the cheapest and the most consistent.

### Lessons

1. **Mechanics can be taught, to a degree.** With the rotation math, the dictionary and a skeleton-first workflow, two of three models produced working two-face drawings in round 1. That did not hold once more instructions were added.
2. **Reversibility must be the absolute priority.** In round 2 the models followed the new event and art instructions and dropped the hard geometric part, in all three outputs. More instructions pulled attention away from the part that cannot be checked by eye.
3. **Staging recovered the effect.** v5 restored identifiable faces in both orientations for all three models, and the evaluator judged artistic quality better than before. This is a relative statement (in round 1 he had said none of the three had much artistic quality), and the drawings are still simple.
4. **Event use is still weak.** In round 3 the event is often only hinted at, and in two of three cases the declared event is generic (for example "AI model release hype cycle" is not a specific event). Making the event central without breaking the illusion is the open problem.
5. **Metadata leaks the joke.** Some round-2 SVGs contain `<title>`/`<desc>` naming the event; this is why the runner strips them from round 3 on.

## 6. Threats to validity

- **Evaluator conflict of interest.** The only judge is the benchmark's author, who also wrote every prompt after seeing earlier results. There is no blind protocol, no second rater, and no agreement statistic.
- **Informal verdicts.** The verdict words are descriptions of one person's reaction, not measurements, and cannot be ranked reliably.
- **Sample size.** Three models, one run per model per prompt (apart from retries after technical failures). Variance across runs is unknown.
- **Uneven comparisons.** In round 1 the MiniMax output came from v2 because its v3 run was interrupted. In round 3, DeepSeek ran with reasoning disabled and MiniMax with low effort, while GLM used medium effort. Round 3 versus round 1 is a before/after comparison with several things changed at once, and the evaluator's expectations may also have changed.
- **Unverified prompt content.** Every prompt contains the same placeholder section with short text descriptions of two real Whistler drawings, written from public images and flagged inside the prompt as unverified. The prompt text also contains a literal production note ("[PLACEHOLDER — Cláudio to add and verify.]") and calls the drawings "public domain", an unverified legal assertion. All of it is kept verbatim because the models saw it, and it is a possible confound.
- **Events and recency.** Models have no search, so the "recent event" depends on training data; several chose events from 2023–2025. Declared events and figures (for example market-value drops) are model wording and are not fact-checked.
- **Heuristic geometry.** The canon, tolerance and dictionary are design conventions, not validated perceptual facts.
- **Scope of the informal claim.** The statement that diffusion models rarely manage this task is an untested observation.

## 7. Future work

The following experiments are needed before any comparative claim:

- **Ablations on the prompt.** v5 was rebuilt from v3, so a v3-versus-v5 comparison under identical model settings isolates the effect of priority ordering and staging. A with/without-geometry-kit condition would test how much of the effect comes from the supplied mechanics.
- **Dose-controlled additions.** Add event and art instructions one at a time, checking the 180° reading after each (suggested by round 3).
- **More runs, more models, more judges.** $N$ independent one-shot runs per model and condition; at least three judges; blind presentation with randomized orientation order; an ordinal agreement statistic; report the distribution, the failure types and the best-of-$N$ separately.
- **Tool-enabled condition.** Let the model render, rotate and look at its output, to measure how much of the failure is "blind drawing".
- **Second mode.** One person with two expressions, left out of v5, is probably harder.
- **A possible diagnostic for stroke sharing (not validated).** For each stroke $S_j$, measure how much removing it lowers the recognition score of each reading, with $f_A, f_B$ any reading-specific recognizer:

$$\Delta_A^j=f_A(I)-f_A(I\setminus S_j),\qquad \Delta_B^j=f_B(RI)-f_B(R(I\setminus S_j)), \qquad (8)$$

$$Q_{\mathrm{shared}}=\frac{\sum_j\min\{[\Delta_A^j]_+,[\Delta_B^j]_+\}}{\sum_j\max\{[\Delta_A^j]_+,[\Delta_B^j]_+\}+\delta},\qquad \delta>0. \qquad (9)$$

$Q_{\mathrm{shared}}\in[0,1)$ is high when strokes contribute to both readings. It needs controls for ablation artifacts, a calibrated recognizer and validation against human judgment.

## 8. Conclusion

RFB is a difficult test because it separates perceptual reinterpretation from mere geometric transformation. The half-turn is trivial to state ($R\circ R=\mathrm{id}$); the difficulty lies in choosing strokes, negative space and relations that survive two facial readings while still carrying a joke, and doing so without being able to look at the drawing. In three small pilot rounds, the most useful result was a failure: more instructions destroyed the part of the task that cannot be checked by eye, and a smaller, staged prompt with an explicit priority order brought it back. Whether that holds beyond one evaluator, three models and one run each is exactly what the next experiments must test.

## References

All entries below were checked against a publisher, library, preprint-server or museum record on 29 October 2026; see [`docs/references.md`](../docs/references.md) for what was checked for each.

[1] Wade, N. J.; Nekes, W. The two faces of Rex Whistler (1905–1944). *Perception*, 34(6), 639–644, 2005. DOI: 10.1068/p34wh.

[2] Yin, R. K. Looking at upside-down faces. *Journal of Experimental Psychology*, 81(1), 141–145, 1969. DOI: 10.1037/h0027474.

[3] Thompson, P. Margaret Thatcher: a new illusion. *Perception*, 9(4), 483–484, 1980. DOI: 10.1068/p090483.

[4] Loviscach, J. Finding approximate ambigrams and making them exact. In H. P. A. Lensch and S. Seipel (eds.), *Eurographics 2010 – Short Papers*, pp. 25–28. The Eurographics Association, 2010. DOI: 10.2312/egsh.20101039.

[5] Zhao, B.; Hanocka, R.; Yeh, R. A. AmbiGen: Generating Ambigrams from Pre-trained Diffusion Model. arXiv:2312.02967, December 2023.

[6] Shirakawa, T.; Uchida, S. Ambigram generation by a diffusion model. In *Document Analysis and Recognition – ICDAR 2023*, Lecture Notes in Computer Science 14189, pp. 314–330. Springer, 2023. DOI: 10.1007/978-3-031-41682-8_20. Preprint: arXiv:2306.12049. Code: Ambifusion.

[7] Geng, D.; Park, I.; Owens, A. Visual Anagrams: Generating Multi-View Optical Illusions with Diffusion Models. *Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR)*, pp. 24154–24163, 2024. DOI: 10.1109/CVPR52733.2024.02280.

[8] Polster, B. Mathemagical Ambigrams. *Proceedings of the Mathematics and Art Conference 2000*, Bond University, 10–12 December 2000, pp. 21–32. PDF: https://www.qedcat.com/articles/ambigram.pdf.

[9] Bubeck, S. et al. Sparks of Artificial General Intelligence: Early experiments with GPT-4. arXiv:2303.12712, 2023 (the "draw a unicorn in TikZ" experiments are in Section 1).

[10] Suls, J. M. A two-stage model for the appreciation of jokes and cartoons: an information-processing analysis. In J. H. Goldstein & P. E. McGhee (eds.), *The Psychology of Humor*, Academic Press, pp. 81–100, 1972. DOI: 10.1016/B978-0-12-288950-9.50010-9.

[11] Kris, E.; Gombrich, E. H. *Caricature*. King Penguin Books, Harmondsworth, 1940. See also Gombrich, E. H., *Art and Illusion: A Study in the Psychology of Pictorial Representation*, Phaidon, London, 1960 (chapter "The Experiment of Caricature").

[12] Salisbury Museum, Rex Whistler Archive. Reversible face: The scholar and the bruiser, 1931–32. https://salisburymuseum.org.uk/collections/reversible-face-the-scholar-and-the-bruiser/ (accessed 29 October 2026).

[13] Whistler, L.; Fuller, R. *The Work of Rex Whistler*. Batsford, London, 1960 (not consulted directly; catalogue record: Fitzwilliam Museum, PB 366-2003).

## Repository files referred to

[`README.md`](../README.md); [`docs/how-it-works.md`](../docs/how-it-works.md); [`docs/geometry.md`](../docs/geometry.md); [`docs/worked-example.md`](../docs/worked-example.md); [`docs/methodology.md`](../docs/methodology.md); [`docs/prompt-evolution.md`](../docs/prompt-evolution.md); [`docs/threats-to-validity.md`](../docs/threats-to-validity.md); [`docs/future-work.md`](../docs/future-work.md); [`docs/related-work.md`](../docs/related-work.md); [`docs/references.md`](../docs/references.md); [`docs/glossary.md`](../docs/glossary.md); [`docs/design-history/`](../docs/design-history/) (specs v0.3 and v0.4); [`prompts/`](../prompts/) (`prompt-v1.md` to `prompt-v5.md`); `rounds/round-0*/EVALUATION.md`; [`scripts/`](../scripts/) (`run_models.py`, `validate_svg.py`, `render_preview.py`).
