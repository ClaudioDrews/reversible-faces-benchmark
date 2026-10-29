# Review 1: after the pilot (round 0). English summary

This is an English summary of the review's points.

**Blockers and main problems**

1. **The model is never forced to *see* its result.** The rasterization tip is optional and the workflow explicitly assumes no tools, so drawing blind reads as a supported mode. This explains an expression claim ("smile vs. grimace") in one output that does not exist in the strokes. Suggested: make verification mandatory when tools exist; otherwise replace weak mental iteration with a cheap, forced symbolic check: for each expression curve write its concavity on the page and what it becomes after a 180° turn.
2. **The reasoning budget is consumed by coordinate arithmetic, and the prompt causes it.** Section 4 provides a precomputed canon table but the workflow asks the model to compute (500 + 600x). One model died doing exactly that. Suggested: "use the page-y values as given, do not compute coordinates in your reasoning, round to multiples of 5"; write one final list of coordinates, then the SVG.
3. **The canon table is a trap, not scaffolding.** All three outputs used the most obvious dictionary pairs (hair ↔ beard, hat ↔ collar), giving near-mirror faces with flat emotions. Suggested: require A and B to differ in at least two expression attributes in the drawing itself; downgrade outputs where faces differ only by accessories; limit the dictionary to at most three pairs and invent the rest.
4. **The joke has no form.** Nothing translates "the joke works only through the two faces" into geometry. Suggested: require a stated physical difference, "A has X / B has Y" with X and Y drawn features, and forbid anything that needs a caption.

**Minor**

5. No prop that exists only in A or only in B: every prop should exist in both readings.
6. Rephrase the humor check: "Erase your mental caption. Do the strokes alone show the opposite situation in the other face?"
7. Add a delivery-budget clause: deliver even if imperfect; if tokens are limited, skip some steps.
8. The neutral mechanism example may be copied structurally; make it visibly odd so that copying it blindly looks strange.

**Do not edit:** the dual-function dictionary, the sum rule and the failure table, which were working (all three outputs got the geometry right).

Order of leverage: (1) mandatory visual verification or a symbolic curve-direction table, (3) asymmetry requirement, (4) joke-as-geometry, (2) arithmetic-free budget.
