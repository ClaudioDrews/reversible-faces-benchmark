# TASK: Draw a Rex Whistler–style REVERSIBLE FACE as one SVG file

You will receive no answers to questions and no feedback. Decide on your own and deliver exactly one SVG.

**Effort budget (important).** Spend your thinking on **reversibility** (Stages 1 and 2 below), not on decoration. Do NOT recompute the tables below: use their "page y" values as given and round to multiples of 5. A complete, working SVG is far better than a perfect plan with no file. If you have run low on budget, deliver what you have.

**Priority order (absolute).** 1) The two readings (A upright, B rotated 180°) must both be clear faces. 2) A and B must look different (different expression). 3) Only then: a simple prop that hints at a recent tech/AI event, and a little art. **If any later touch endangers a reading, delete the touch.** A plain drawing where both faces read beats a pretty one where B is lost.

## 1. What you must make

A **reversible face** (in the tradition of Rex Whistler's *¡OHO!*, 1946) is ONE drawing that shows one face when the page is upright and a *different* face when the same page is rotated 180° (a person turns the page, or their phone, upside down).

- As the file stands, it shows **Face A**.
- The same file rotated 180° shows **Face B**.
- B is **not a second drawing**. It is the same strokes, read upside down. The strokes that are B's hat, hair, beard or collar are, in A, the chin, mouth, jaw or neck, and the other way around.
- The drawing carries a small **joke about technology or AI**, told *only through the two faces* (their expressions, their accessories, the contrast between them). There is no text, and no caption.

**Make the joke a physical difference.** Name the contrast as drawn features: *A has X / B has Y* (e.g. wide-open eyes and a big grin / half-closed heavy lids and a downturned mouth; a proud tall hat / a limp sagging collar). If you cannot name the drawn difference, pick another joke.

Two characters, A and B, are required (no "one person with two moods" variant in this version).

**The event (lightweight).** Pick **one recognizable, recent technology or AI event** you know well (no searching; use the most recent one you are sure about) and give each face **one simple prop** that hints at it (a headset, a rocket, a server rack, a bubble, a cracked screen, a plug, a speech bubble with no letters, a cap with an antenna...). A: the moment of promise or triumph. B: the consequence. Keep the prop a simple bold shape that sits inside a hat, hair, beard or collar mass. If you cannot place the prop without hurting a reading, drop the prop and keep the expressions. The joke must fall on an **action, decision or situation**, never on anyone's body, private life, or character, and must not demean any person, company or group. No tragedies. Archetypes (the CEO, the regulator, the engineer, the chatbot) are safer than real people.

## 2. Staged workflow (follow in order; do not skip ahead)

**Stage 1: Geometry only (no style).**
1. State the idea in one sentence (A = ..., B = ...) and the event in a few words. A and B must differ in expression, not only in accessories: change at least two of eye opening, brow angle, mouth curve, jaw width, age.
2. Place the **shared eye anchors**: two eyes near (415, 500) and (585, 500). They are the same strokes in A and B.
3. Write the **double-duty feature map**: for each feature of A, name its partner in B using the dictionary (Section 4). Use at least four pairs, for example: A's smile (a ∪ at y≈680) = B's hat band/dome (y≈320); A's hat or hair mass (y≈200–350) = B's beard mass (y≈650–800); A's brows = B's eye-bags; A's fringe or hat brim (y≈350) = B's nose; A's bow tie or collar (y≈890) = B's pompom (y≈110). Choose a head outline whose top contour is B's chin and whose chin is B's hat top.
4. Draw only: one head outline, the eyes, the shared strokes (drawn once), and the B-only strokes inside a `<g transform="rotate(180 500 500)">` group. Plain flat shapes. No hatching, no extra detail.

**Stage 2: Verify by rotating coordinates (mandatory).**
For each double-duty stroke, write one line: `A point (x, y) -> R(p) = (1000 - x, 1000 - y) -> what it is in B`. Check at least these: the mouth/grin curve, the nose, the hat or hair mass, the chin/collar, one brow. Check that (a) A's mouth lands in B's hat zone (y ≈ 300–350), not on top of a second mouth; (b) B has its own nose and mouth at the right heights from the B-only group; (c) left/right swap was applied once; (d) B-only strokes are light and sit inside masses so A does not show a second face. If a check fails, fix the geometry once and move on. **Stage 2 is ONE short pass (about 12 lines in total). Do not re-verify, do not restart, do not re-derive the tables.** Keep your whole planning under about 3000 words, then write the SVG.

**Stage 3: Style (only after Stages 1–2 pass).**
Add the event prop and the art touches of Section 6. After each touch, ask: do both faces still read? If not, undo it.

**Stage 4: Deliver (Section 8).**


## 3. The file

- Output must be a standalone SVG that opens directly in a web browser: `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 1000" width="1000" height="1000">`. Valid XML. No external references. At most 300 KB.
- Center of the page = (500, 500). The figure is **centered** there and fills most of the page. The head (crown to chin) should be about **600 px tall**, so the whole figure including hats/collars fits inside about 100–900.
- No side-by-side layout, no two small heads, no scene divided into halves. One figure.
- **Forbidden:** any text (`<text>`, fonts, letter-shaped paths), `<image>`, `<foreignObject>`, `<script>`, gradients, blur/filters, drop shadows or any directional lighting (light from top-left becomes light from bottom-right in the other reading and breaks the illusion).
- **Allowed:** black or dark ink line work, hatching (hatching direction survives rotation), flat fills, a small flat palette (paper + ink + at most 2 accents), white/negative space. Strokes with round caps and joins look best.
- **Do not** put `<title>`, `<desc>` or `<metadata>` in the SVG (they would reveal the event on hover).
- A white or off-white background rectangle is fine.

## 4. Geometry you can use (a design tool, not a law)

Whistler drew by hand; the numbers below are a *convention* for planning, not a historical fact. Use them as scaffolding.

**Rotation.** Let C = (500, 500) be the page center. Rotating the page by 180° sends every point p to R(p) = 2C − p. Doing it twice returns the original. In SVG this is `transform="rotate(180 500 500)"`. It is NOT a mirror (`scale(-1,1)`): a mirror is a different genre.

What 180° does: straight lines keep their direction; a cup ∪ becomes a dome ∩ (relative to the viewer); **left and right swap** (A's right eyebrow is built from B's left eye-bag); the vertical order flips (what is above A's eyes is below B's eyes).

**Shared eyes.** Real Whistler reversible faces typically share the eyes: they sit near the middle of the head, so the eyes of A can also be the eyes of B (eyes stay eyes; eyelids, brows and the eye bags change meaning, which changes the mood). Everything else is *reinterpreted*.

**Canon** (unit H = head height = 600 px; eyes at y = 0; y grows downward; page point = (500 + 600·x, 500 + 600·y)):

| feature | y (in H) | page y |
|---|---|---|
| plume / pompom (top of hat) | −0.65 | 110 |
| crown / top of hat | −0.50 | 200 |
| hat dome | −0.30 | 320 |
| hat brim | −0.25 | 350 |
| hairline | −0.20 | 380 |
| brow | −0.08 | 452 |
| upper-lid crease | −0.04 | 476 |
| **eyes** | **0** | **500** |
| lower lid | +0.04 | 524 |
| under-eye bag | +0.08 | 548 |
| nose bridge | +0.20 | 620 |
| nose tip / nostrils | +0.25 | 650 |
| mouth line | +0.30 | 680 |
| lower lip | +0.34 | 704 |
| chin | +0.50 | 800 |
| collar / bow tie | +0.65 | 890 |

Horizontal: face half-width ±0.36H (±216 px); eye centers ±0.14H (±84 px); mouth half-width ±0.13H (±78 px); jaw ±0.30H at y +0.40; ears ±0.36H at eye level.

**Dual-function dictionary.** With shared eyes, a feature of A at height y and a feature of B at height −y (as seen on the page) are the *same strokes*. This gives the natural pairs:

| in A (page) | is in B | typical double reading |
|---|---|---|
| eyes | eyes | anchor: lids and brows decide the mood |
| upper-lid crease (−0.04) | lower lid (+0.04) | |
| brow (−0.08) | under-eye bag (+0.08) | a heavy brow = a baggy eye |
| hairline / fringe (−0.20) | nose bridge (+0.20) | a lock of hair = the line of the nose |
| **hat brim (−0.25)** | **nose tip (+0.25)** | the dome of the brim = the cup of the nose |
| **hat/hair dome (−0.30)** | **mouth (+0.30)** | a smile = the band of a hat; a frown = the dome of a cap |
| side of hair/hat (−0.40) | jawline (+0.40) | |
| crown / top of hat (−0.50) | chin (+0.50) | top contour of A = bottom contour of B |
| plume, pompom, flower (−0.65) | collar, bow tie, buckle (+0.65) | |
| hair mass | beard / wrinkles / cheeks | tufts of hair = tufts of beard |

**Consequence (order flip).** Nothing below A's eyes can stay below B's eyes. "A's mouth becomes B's nose" is impossible with shared eyes; A's mouth becomes B's *hat* zone, and B's nose comes from A's hat brim or fringe.

**Slack and the sum rule.** Recognition forgives small deviations (about 0.05H = 30 px) from the canon. Every exaggeration in A must be paid by its partner in B: a very long nose in A means a lower hat brim in B; a very wide smile in A means a wide hat band in B. Hats, hair, beards, collars, wrinkles are *free variables* that absorb leftovers, which is why the genre is full of hats, beards and old faces.

**Compromise strokes.** For a shared stroke, take the average of where A wants it and where B wants it (after rotating B's target to the page): s = (A + R(B)) / 2. Draw it once.

## 5. Reference notes for Stage 1 and 2

1. **Thesis first.** One sentence. Pick two characters whose *accessories* carry the joke (a hat that is a halo in one reading and a collar in the other; a smile that is a frown...).
2. **Skeleton first.** Only: head outline, two eyes, nose, mouth, one free element (hat, hair or beard). Make both orientations read as faces before adding anything else.
3. **Table of correspondences.** For every feature of A, name its partner in B using the dictionary (Section 4). Note where the sum rule forces a compromise.
4. **Draw each shared stroke once.** Pairing is where the left/right swap happens (A's left corner pairs with B's right corner). Do not rotate a second time afterwards.
5. **Add B-only strokes** in a group rotated 180° (`<g transform="rotate(180 500 500)">`), drawn in B's own upright frame, and A-only strokes in the unrotated group. B-only strokes must be few, light and placed where they are inert in A (inside hair, hat or collar masses).
6. **Silhouette.** One outline that contains both anatomies in both readings (the wider of the two at each height). Round it, but never cut it inside either face.
7. **Check both orientations after each significant edit.** Add expression, props and the joke only after the skeleton works.
8. **Without any tools** (you cannot run code or render): keep the figure simple. Take A's heights from the "page y" column; for B, a feature at B-height y_B (from the same column) sits on the page at 1000 − page y. Where A and B want the same stroke in different places, use the midpoint. Write one short list of coordinates, then the SVG. As a cheap symbolic check, for each expression curve write down: *concave up or down on the page → what it becomes after rotation* (a ∪ smile becomes a ∩ dome; a ∩ brow becomes a ∪ lid line). Do not do more arithmetic than that.

**Optional tip, only if you can run code:** rasterize the SVG (e.g. `cairosvg`), rotate the image 180°, and *look* at both images. If you have a vision model, first ask it "what do you see?" for each image *before* telling it your intention. Its approval is not proof; a human makes the final judgment.

### Minimal neutral mechanism example (NOT a face; do NOT reuse it)

This toy shows only the mechanism: one stroke serving two roles, one B-only stroke in a rotated group, and the shared eyes. It is intentionally not a complete figure. Copying it, or its characters, will be judged as no originality.

```xml
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 1000" width="1000" height="1000">
  <rect width="1000" height="1000" fill="#fff"/>
  <g fill="none" stroke="#111" stroke-width="4" stroke-linecap="round" stroke-linejoin="round">
    <!-- shared eyes: they sit at the same spot in A and in B (yours should have more character) -->
    <circle cx="430" cy="500" r="16"/>
    <circle cx="570" cy="500" r="16"/>
    <!-- ONE stroke, drawn once: a smile (cup) at y=680 in A.
         Rotated 180° by the viewer it is a dome at y=320 in B: a hat band. -->
    <path d="M 422 680 Q 500 724 578 680"/>
    <!-- B-only stroke, drawn in B's own upright frame (a nose tip at y=650).
         The rotation puts it at y=350 on the page, where A reads it as a hat brim / fringe. -->
    <g transform="rotate(180 500 500)">
      <path d="M 470 650 Q 500 672 530 650"/>
    </g>
  </g>
</svg>
```

## 6. Art touches (Stage 3 only, always subordinate to reversibility)

Use at most these three, and only if both readings stay clear:
- **Varied line weight.** Heavy outline (8–12 px), medium features (5–7 px), fine hatching (2–3 px). Flat dark masses for hair, beard, hat, collar.
- **Caricature exaggeration.** Push one or two features per face (a huge nose or jaw, heavy brows, an oversized hat). Expression toolkit: wide-open round eyes with raised brows = delight or alarm; heavy half-closed lids with thick bags = weary or smug; brows slanting down = anger or worry; a wide ∪ mouth = grin, a ∩ mouth = sulk. A timid, neutral face is a failure.
- **Asymmetric silhouette.** One strong asymmetry (a jowl, a crooked hat, a tilted nose) that survives rotation.

Always true: few confident double-duty strokes beat many timid ones; every prop must make sense in both readings; the faces must be recognizable at a glance and at thumbnail size. **Avoid:** busy hatching, tiny details, text-like squiggles, rotationally symmetric figures.

## 6b. Real examples (for understanding only)

> **[PLACEHOLDER — Cláudio to add and verify.]** Short text descriptions of 1–2 real Whistler reversible drawings (public domain, Wikimedia Commons: *Hair Bald & Bearded*, *Scotsman & Englishman*). Draft below was written from the public images and **must be verified by Cláudio** before use.
>
> *Draft, to verify:*
> - **Hair Bald & Bearded.** Frontal, heavily hatched, a plump face. Upright: a cheerful man with thick wavy hair, crinkled eyes, rosy cheeks and a lopsided smile. Rotated: a tired, bald, bearded man with heavy lids and a furrowed forehead. The eyes are shared (the lids and brows turn "smiling and crinkled" into "weary and baggy"). The *hair* becomes the *beard*; the *smile and chin* become the *forehead and bald dome*; the cheeks stay cheeks (bright round cheek highlights in one are the pouches under the eyes in the other). The ears stay at eye level on both sides.
> - **Scotsman & Englishman.** Two heads in plaid caps. Upright (one reading): a glum, heavy-lidded man with a sour downturned mouth, a small cap with a horseshoe badge on top, and a plaid collar at the bottom with a flower. Rotated: a grinning man with a plaid cap topped by the flower and a collar with the horseshoe buckle. The *cap* becomes the *collar*, the *collar* becomes the *cap*, the frown becomes a smile (cup ↔ dome), the forehead creases become cheek creases, and the flower and horseshoe swap places. The eyes are shared again.
>
> Take from these examples the *principles* (shared eyes; hat ↔ collar, hair ↔ beard, frown ↔ smile; accessories carry the second identity), not their characters.

## 7. Self-check (reversibility first)

**GATE 1. Reversibility (this decides everything).**
- As the file stands: ONE clear upright face (A). B must not be visible as a second face.
- Rotated by 180° (each point p goes to 2C − p, i.e. (x, y) -> (1000 − x, 1000 − y)): ONE clear upright face (B), with its own eyes, nose, mouth, hat or hair, and clearly different from A. Picture the page upside down and name B's hat, eyes, nose, mouth, beard. If any of them is missing, B has failed: go back to Stage 1.
- Are the strokes genuinely shared (double duty), or are there two drawings overlaid?
- If either reading fails, remove styling and props until both read. Do not deliver a drawing whose B face is lost.

**GATE 2. Contrast.** Are the expressions and accessories of A and B opposite (opposite expression AND opposite props)?

**GATE 3. Light touches.** Is there one simple prop per face hinting at the event? Is the joke about an action or situation, nobody demeaned? Is the line weight varied and at least one feature exaggerated? (Only if Gates 1–2 are already passed.)


Common failures to catch:

| Failure | Symptom | Fix |
|---|---|---|
| Same orientation | In A you see two upright faces | B was drawn upright. Draw B's strokes pre-rotated (`rotate(180 500 500)` group). |
| Segregation | A in one region, B in another | Strokes not shared; merge them using the dictionary. |
| Dominance | One face is clear, the other weak | Fix the weaker; lighten the dominant face's exclusive strokes. |
| Ghosting | Doubled contours, "double exposure" | Two drawings overlaid; draw one compromise stroke instead. |
| B visible upright | You can see B without rotating | B-only strokes too heavy; lighten or hide them in masses. |
| Rotationally symmetric | Rotated page looks the same | Break the symmetry (asymmetric hat, hair, expression). |
| Swapped sides | In B the face looks twisted | The left/right swap was skipped or applied twice. |
| Mirror, not rotation | B looks like a mirror image | You used `scale(-1,1)`. Use `rotate(180 500 500)`. |
| Lighting | Shadows look wrong rotated | Remove gradients and directional shadows. |
| Text | Letters in the image | Remove them. |

**Stop rule.** If you can iterate, stop when both readings pass, or after 5 rounds. A complete, imperfect SVG is far better than none.

## 8. Delivery

Reply in exactly this format, nothing else:

`EVENT: <the tech/AI event you hinted at, short phrase with approximate date>`
`TITLE: <short title, max 8 words>`

followed by the complete SVG in a single ```xml code block (no `<title>` or `<desc>` inside it). No other text, no explanation.
