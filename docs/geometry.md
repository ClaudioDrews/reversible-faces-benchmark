# Geometry (formal statement)

This page states the geometry behind the prompt kit in compact mathematical form. The full discussion, with the worked check, is in section 4 of the [paper](../paper/reversible-faces-benchmark-paper.md). Plain-language version: [`how-it-works.md`](how-it-works.md). Terms: [`glossary.md`](glossary.md).

**Status of everything below.** The half-turn facts are exact. The canon, the tolerance (about 30 px) and the dictionary pairs are **design heuristics** for a model that cannot see its drawing: not measured, not claimed as facts about Whistler, not validated against human recognition. None of the quantities in sections 3–5 was computed in any round. The symmetry number ρ of section 6 was computed only by the round-4 harness, as an advisory number shown to the models (rounds 0–3 did not compute it). [`scripts/validate_svg.py`](../scripts/validate_svg.py) checks the file contract only (structure and safety) and never judges the drawing.

Notation: page 1000 × 1000, center C = (500, 500), R the half-turn, I a drawing.

## 1. The half-turn is an involution

R(p) = 2C − p, i.e. (x, y) → (1000 − x, 1000 − y), and R∘R = id.

- It is a proper rotation (det = +1), **not** a mirror: `scale(-1, 1)` has det = −1 and is a different kind of illusion.
- It generates the group C₂ = {e, R}.
- Lines keep their direction; a cup ∪ becomes a dome ∩; left and right swap; vertical order flips.
- A reversible figure need not satisfy R(I) = I. Full rotational symmetry is a **failure mode** (the same face twice).

## 2. Feasible set (what "valid" means)

Let P_A(I) and P_B(I) be idealized scores for "I reads as face A" and "I reads as face B", with thresholds τ_A, τ_B, and C_A = {I : P_A(I) ≥ τ_A}, C_B = {I : P_B(I) ≥ τ_B}. A drawing is a valid reversible pair when

I ∈ S(A,B) = C_A ∩ R[C_B] = { I : P_A(I) ≥ τ_A and P_B(R·I) ≥ τ_B }.

Equality of the two readings is not required; only membership in two legibility regions. Roles are interchangeable: S(A,B) = R[S(B,A)]. In practice the "recognizer" is a human and nothing is calibrated.

## 3. Even and odd parts

For a rasterized image treated as a real vector: I₊ = ½(I + R·I) and I₋ = ½(I − R·I), so I = I₊ + I₋ and R·I = I₊ − I₋. The even part is what the half-turn preserves; the odd part is what changes sign. This is algebra only: it does not isolate the meanings of A and B.

## 4. Shared strokes and compromise strokes

A stroke has target position a in face A (page frame) and target b in face B's **own upright frame**; on the page B's target is R(b). A shared stroke s, drawn once, should satisfy

‖s − a‖ ≤ ε and ‖s − R(b)‖ ≤ ε.

Two closed balls of equal radius ε intersect if and only if **‖a − R(b)‖ ≤ 2ε**. With a quadratic cost w_A‖s − a‖² + w_B‖s − R(b)‖² (w_A, w_B > 0) the minimizer is

s* = (w_A·a + w_B·R(b)) / (w_A + w_B).

For equal weights s* = (a + R(b)) / 2, which also minimizes the worst deviation max{‖s − a‖, ‖s − R(b)‖}. This is the prompt's rule "take the average of where A wants it and where B wants it". It can be applied to corresponding control points of two Bézier curves of equal degree, if the control points are paired consistently. Geometric closeness does not guarantee semantic recognition.

**Pitfall (double rotation).** If the formula already applies R to b, pass b in B's own frame. Passing R(b) gives R(R(b)) = b and cancels the conjugation. The left/right swap must also be applied exactly once. In the prompt v5 failure table these two mistakes are "Same orientation" and "Swapped sides".

## 5. Silhouette

One outline must contain both anatomies. For silhouettes that are star-shaped about C, with radial functions r_A(φ) and r_B(φ + π) (B's radius seen through the half-turn), an inclusive envelope is r₀(φ) = max{r_A(φ), r_B(φ + π)}. Smoothing must not cut into either face. r_S = max{K ∗ r₀, r₀} (K an averaging kernel) preserves containment: it fills valleys and keeps peaks, so it guarantees containment, not smoothness at peaks. The prompt says it in words: "the wider of the two at each height ... round it, but never cut it inside either face".

## 6. A symmetry diagnostic (round 4 only, advisory)

ρ(I) = ‖I − R·I‖ / ‖I‖, in [0, 2]. ρ = 0 means rotational symmetry. A high ρ does not prove two faces and a low ρ does not prove failure; resolution, anti-aliasing and background would have to be fixed before comparing values. It was not computed in rounds 0–3. The round-4 harness computes it on a 200 px grayscale render of the model's own SVG and shows it to the model as a one-sided alarm (a warning when ρ is below 0.15), not as a score; see [`../rounds/round-04/SETUP.md`](../rounds/round-04/SETUP.md) and `scripts/perceptual.py`. No result is judged by it.

## 7. Canon and dictionary in page coordinates

**Wording note.** The prompts the models received say "a feature of A at height y and a feature of B at height −y (as seen on the page)". That is looser than, and in the strict sense inconsistent with, the statement here, where B's heights are in B's own frame. The prompts are kept verbatim (the models saw them); this page and the paper use the precise statement. The dictionary is also not a partition: a stroke near page y ≈ 320–350 can be B's mouth and, for hat or hair masses spanning y 200–350, part of B's beard mass; the table lists typical pairings only.

Head height H = 600 px, eyes at y = 0 (page y 500), page y = 500 + 600·y. A feature of A at page height y_A is the same stroke as a feature of B at height y_B **in B's own frame** when y_A = 1000 − y_B:

| Feature of A (page y) | is, in B (B-frame y) | Check |
|---|---|---|
| eyes (500) | eyes (500) | anchor: lids and brows decide the mood |
| brow (452) | under-eye bag (548) | 1000 − 548 = 452 |
| hairline or fringe (380) | nose bridge (620) | 1000 − 620 = 380 |
| hat brim (350) | nose tip (650) | 1000 − 650 = 350 |
| hat or hair dome (320) | mouth (680): a smile is the band of a hat | 1000 − 680 = 320 |
| crown or top of hat (200) | chin (800) | 1000 − 800 = 200 |
| plume or pompom (110) | collar or bow tie (890) | 1000 − 890 = 110 |
| hair mass | beard, wrinkles, cheeks | free variable |

**Consequence.** Nothing below A's eyes can stay below B's eyes: A's mouth cannot be B's nose (A's mouth is at 680; B's nose tip lands at 350 on the page, 330 px away). **Sum rule:** recognition tolerates deviations of about 0.05·H = 30 px, which corresponds to ε ≈ 30 px above.

## 8. The symbolic check used instead of rendering

The models could not render. For each double-duty stroke the prompt asks them to write *A point (x, y) → R(p) = (1000 − x, 1000 − y) → what it is in B*, and for each expression curve whether it is concave up or down on the page and what it becomes (a ∪ smile becomes a ∩ dome; a ∩ brow becomes a ∪ lid line).
