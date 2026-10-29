# Review 2: after the v2 runs

Verbatim (it was written in English).

**1) Did v2 fix the issues raised?**
- Yes, structurally: the effort budget clause, the pre-rotated B group, the expression-differ-in-≥2-attributes rule, "joke = physical A-has-X/B-has-Y", no caption, props-in-both-readings, and the ≥3 dictionary pairs all landed. All three models produced valid, readable both-ways faces — v1's mechanics failures appear fixed.
- Partially only: expression contrast improved (minimax clearly, glm weakly, deepseek barely) but the ≥2-attribute rule produced "two friendly/neutral faces" in one model — the rule constrains attributes, not *amount* of exaggeration.

**2) What still fails**
- The joke is invisible in all three outputs. Nothing in the prompt forces a *prop-level* contrast tied to the tech idea; models default to generic hats/ties. The joke section names contrasts, but nothing requires A and B to differ in an artifact that signals "technology" (e.g. robot brow vs human brow, helmet vs hair, cable vs collar).
- Skeleton failure persists: "oval head + two generic eyes". No rule pushes a distinctive silhouette (Whistler's heavy jowls, domed head). The canon table actively encourages the oval.
- Stroke weight/timidity: "economy of line" is being read as "thin and sparse". Needs an explicit boldness rule.
- The 6b examples are still an unverified placeholder — shipping with it risks wrong facts.

**3) Three most valuable exact edits**
1. In §2 step 2, add: "At least one accessory must be unmistakably technological (headset, cable, antenna, robot visor, charging port, screen face) and its partner must be unmistakably human; the tech element must be visible in both readings."
2. In §6, replace the character bullet with: "Silhouette first, not oval first: give the head one strong asymmetry — heavy jowls, a domed bald crown, a squashed chin, a jutting nose — that survives rotation. A symmetric ellipse head is a failure."
3. In §6, add: "Line weight: main contours 8–12 px, features 5–7 px, detail 3 px. Bold and simplified beats thin and detailed. Every line you draw, double its confidence."

**4) Another iteration?**
One more, small, then ship. The mechanics are solved; only these three (tech prop, silhouette, line weight) plus filling/verifying 6b remain. They're one-line edits — worth one pass — but the prompt is already good enough that a human judge would get competent, if jokeless, results today. Don't iterate beyond that; diminishing returns.
