# How the task works

## What a reversible face is

One drawing that shows **Face A** as it stands and **Face B** when the page is turned 180°. B is not a second drawing: it is the same strokes read upside down. The strokes that are B's hat, hair, beard or collar are, in A, the chin, mouth, jaw or neck, and the other way around. The classic example is Rex Whistler's *¡OHO!* (1946).

In this benchmark the two faces also carry a joke: A and B are two sides of one witty idea about technology or AI, shown only through expressions, accessories and props (no text, no caption).

## The rotation

Use a 1000 × 1000 page, center C = (500, 500). A half turn sends

```
R(p) = 2C − p,   (x, y) → (1000 − x, 1000 − y),   and R(R(p)) = p.
```

- In SVG: `<g transform="rotate(180 500 500)">`.
- It is **not** a mirror. `scale(-1, 1)` would give a different genre of illusion.
- Straight lines keep their direction. A cup (∪) becomes a dome (∩) relative to the viewer. **Left and right swap**: A's right eyebrow is built from B's left eye-bag. The vertical order flips: what is above A's eyes is below B's eyes.

## The model kit given in the prompt

The prompt calls this "a design tool, not a law": Whistler drew by hand, without numbers; the numbers are scaffolding for a model that cannot see what it draws.

**Shared eyes.** In many Whistler reversible faces the eyes sit at the middle of the head, so A's eyes can also be B's eyes. Eyes stay eyes; eyelids, brows and eye-bags change meaning, and that changes the mood.

**Canon** (head height H = 600 px; eyes at y = 0; page position = 500 + 600·y):

| feature | y (in H) | page y |
|---|---|---|
| plume / pompom | −0.65 | 110 |
| crown / top of hat | −0.50 | 200 |
| hat dome | −0.30 | 320 |
| hat brim | −0.25 | 350 |
| hairline | −0.20 | 380 |
| brow | −0.08 | 452 |
| **eyes** | **0** | **500** |
| under-eye bag | +0.08 | 548 |
| nose tip | +0.25 | 650 |
| mouth line | +0.30 | 680 |
| chin | +0.50 | 800 |
| collar / bow tie | +0.65 | 890 |

**Dual-function dictionary.** With shared eyes, a feature of A at height *y* and a feature of B at height *−y* (as seen on the page) are the same strokes:

| in A | is in B |
|---|---|
| eyes | eyes (anchor; lids and brows decide the mood) |
| brow (−0.08) | under-eye bag (+0.08) |
| hairline / fringe (−0.20) | nose bridge (+0.20) |
| hat brim (−0.25) | nose tip (+0.25) |
| hat or hair dome (−0.30) | mouth (+0.30): a smile is the band of a hat |
| crown / top of hat (−0.50) | chin (+0.50) |
| plume, pompom (−0.65) | collar, bow tie (+0.65) |
| hair mass | beard, wrinkles, cheeks |

**Consequence.** Nothing below A's eyes can stay below B's eyes. A's mouth becomes B's hat zone, and B's nose comes from A's hat brim or fringe.

**Sum rule.** Recognition forgives deviations of about 0.05 H (30 px). Every exaggeration in A must be paid by its partner in B (a very long nose in A means a lower hat brim in B). Hats, hair, beards, collars and wrinkles are free variables that absorb the leftovers.

**Compromise strokes.** For a shared stroke, take the average of where A wants it and where B (rotated onto the page) wants it: s = (A + R(B)) / 2. Draw it once.

## Workflow that the best prompt (v5) imposes

1. **Geometry only**: choose the idea, place the shared eyes, write the double-duty feature map, draw plain shapes. B-only strokes go in a rotated group.
2. **Verify by rotating coordinates**: for each double-duty stroke, write `A point → R(p) → what it is in B`, in one short pass.
3. **Only then style**: a simple prop for the event and at most three art touches, undone if they endanger either reading.

## Failure modes seen in practice

| Failure | Symptom |
|---|---|
| Same orientation | B was drawn upright, so A shows two upright faces |
| Segregation | A in one region, B in another; strokes not shared |
| Ghosting | Doubled contours ("double exposure") from two overlaid drawings |
| B lost | The rotated reading shows no face (all of round 2) |
| Neutral faces | A and B differ only by accessories, with flat expressions |
| Clip-art look | Oval head, uniform thin lines, no character |
| Generic joke | "Hype vs. reality" with no identifiable event |
