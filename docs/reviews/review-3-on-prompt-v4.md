# Review 3: on prompt v4

Verbatim. This review arrived after the round-2 run had already started, so it was **not** applied to v4. Its first risk (no feedback loop, overload of constraints) is a plausible explanation for the round-2 failure and informed v5.

**Three biggest risks**

1. **No visual feedback loop.** The prompt tells the model it "cannot run code or render" (§5.8) while inventing a hard geometric puzzle. Without rendering, cheap models produce exactly the "stiff clip-art" it warns against — the compromise-stroke and sum-rule arithmetic will be done badly in one mental pass, so one face reads and the other is ghost noise.

2. **Unverifiable recency.** "Most recent event you know well (2025–2026)" is a knowledge-cutoff lottery: the model will pick a stale or half-remembered event, then draw props for details it "is unsure of" — the event recognition test (§1b) fails silently.

3. **Constraint overload collapses craft.** ~220 lines of rules (dictionary, canon, palette, forbidden list, 5-round stop rule) exceed cheap-model attention: it will satisfy the measurable ones (no text, 1000×1000, valid XML) and drop the unmeasurable art-quality ones — uniform thin lines, symmetric oval heads.

**Single most valuable fix:** require a self-check pass that rasterizes or at least structurally verifies both orientations (or supply a rendered A/B reference pair), turning the blind arithmetic into visual iteration.
