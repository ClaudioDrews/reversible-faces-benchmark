# TASK: Draw a Rex Whistler–style REVERSIBLE FACE as one SVG file

You will receive no answers to questions and no feedback. Decide on your own and deliver exactly one SVG.

**Effort budget (important).** Think briefly: a few short paragraphs to pick the idea and the skeleton, then write the SVG. Do NOT hand-verify every coordinate, and do not recompute the tables below: use their "page y" values as given and round to multiples of 5. A complete, imperfect SVG is far better than a perfect plan with no file. If you have run low on budget, deliver what you have.

## 1. What you must make

A **reversible face** (in the tradition of Rex Whistler's *¡OHO!*, 1946) is ONE drawing that shows one face when the page is upright and a *different* face when the same page is rotated 180° (a person turns the page, or their phone, upside down).

- As the file stands, it shows **Face A**.
- The same file rotated 180° shows **Face B**.
- B is **not a second drawing**. It is the same strokes, read upside down. The strokes that are B's hat, hair, beard or collar are, in A, the chin, mouth, jaw or neck, and the other way around.
- The drawing carries a **joke**: A and B are two faces of one witty idea about technology or AI. The joke must work *only through the two faces* (their expressions, their accessories, the contrast between them). There is no text to explain it, and you will not be allowed a caption either: if the joke needs a sentence to be understood, it is not drawn yet.

**Make the joke a physical difference.** Before drawing, name the contrast as drawn features: *A has X / B has Y*, where X and Y are lines a viewer can see (e.g. wide-open eyes and a big grin / half-closed heavy lids and a downturned mouth; a proud tall hat / a limp sagging collar). If you cannot name the drawn difference, pick another joke.

Two characters, A and B, are required (no "one person with two moods" variant in this version).

The event/joke is only a pretext. Pick any recent, well-known technology or AI event or situation you know about (no searching needed), or a recognizable situation drawn from the real tech world (hype vs. reality, promise vs. outcome, human vs. machine, before vs. after). The joke must fall on an **action, decision or situation**, never on anyone's body, private life, or character, and must not demean any person, company or group. No tragedies. Real people may be caricatured if the likeness serves the action; archetypes (the CEO, the regulator, the engineer, the chatbot) work just as well and are safer.

## 2. Steps

1. Choose the idea in one sentence: A = ..., B = ... Two faces of one thesis (e.g. *confident launch* ↔ *sheepish recall*).
2. Choose two characters whose silhouettes fit together: a **top-heavy** one (tall hat, big hair) with a **bottom-heavy** one (heavy jaw, beard, mustache, wide collar). At least one should tolerate extra lines (age, wrinkles, beard, fur, textured hat). **A and B must differ in expression, not only in accessories**: change at least two of eye opening, brow angle, mouth curve, jaw width, and age. Two near-identical neutral faces with swapped hats is a failure. **At least one accessory must be unmistakably technological** (headset, cable, antenna, robot visor, charging port, a screen for a face, a circuit-board beard…), with a clearly human counterpart in the other reading; the tech element must be visible and recognizable in its reading. Do not simply default to the single most obvious pairing (hair ↔ beard, hat ↔ collar): use at least three different pairs from the dictionary, and invent the rest.
3. Build a *skeleton first* (Section 5), make it work in both orientations, and only then add detail.
4. Run the self-check (Section 7) in your head or with tools. Fix the weaker reading first. Do not spend more than a short pass on it.
5. Deliver (Section 8).

## 3. The file

- Output must be a standalone SVG that opens directly in a web browser: `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 1000" width="1000" height="1000">`. Valid XML. No external references. At most 300 KB.
- Center of the page = (500, 500). The figure is **centered** there and fills most of the page. The head (crown to chin) should be about **600 px tall**, so the whole figure including hats/collars fits inside about 100–900.
- No side-by-side layout, no two small heads, no scene divided into halves. One figure.
- **Forbidden:** any text (`<text>`, fonts, letter-shaped paths), `<image>`, `<foreignObject>`, `<script>`, gradients, blur/filters, drop shadows or any directional lighting (light from top-left becomes light from bottom-right in the other reading and breaks the illusion).
- **Allowed:** black line work, hatching (hatching direction survives rotation), flat fills, a small flat palette, white/negative space. Strokes with round caps and joins look best.
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

## 5. Strategy and workflow

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

## 6. Art quality: what makes it good (and what makes it bad)

- **Economy of line.** Few, confident strokes beat many timid ones. Every line should earn its place in *both* faces. If a stroke only serves one face, ask whether the other face can use it too; if not, make it light or remove it.
- **Double-duty strokes are the art.** The best moment is when the viewer realizes that the *same curve* is a smile in one face and a hat in the other. Superposition (two independent drawings overlaid) looks like a "double exposure" with ghost contours and is the weakest solution.
- **Negative space is material.** A white region can be forehead in A and the gap between hair and brow in B. Before adding a line, try changing the white shape.
- **Global coherence beats local perfection.** A slightly odd stroke reads correctly when the whole configuration is clear. Use ambiguity on purpose.
- **Silhouette first, not oval first.** Give the head one strong asymmetry that survives rotation: heavy jowls, a domed bald crown, a squashed chin, a jutting nose, an oversized hat. A symmetrical ellipse with two dots for eyes is a failure; the canon is a guide to *where* things go, not a shape to copy.
- **Bold line weight.** Main contours 8–12 px, features 5–7 px, small detail 3 px; flat black or flat color masses (hair, beard, hat, collar) give the eye something to hold. Bold and simplified beats thin and detailed. "Economy of line" means fewer, more confident lines, not timid ones.
- **Character.** Strong, simple shapes: big expressive eyes, one exaggeration per face (an enormous hat, a huge mustache, a tiny chin), caricature that serves the *action*, not the person's looks.
- **Contrast between A and B is the joke:** make the two moods or situations unmistakable (proud ↔ sheepish; calm ↔ panicked; human ↔ robot).
- **Expression toolkit (exaggerate!).** Wide-open round eyes with raised brows = delight or alarm; heavy half-closed lids with a thick lower bag = weary or smug; brows slanting down toward the nose = anger or worry; a wide ∪ mouth = grin, a ∩ mouth = sulk. Whistler's faces are big, rounded, with crinkled eyes, strong cheeks and heavy brows: push the features further than feels polite. A timid, symmetrical, neutral face is the most common failure in this task.
- **Every prop must make sense in both readings** (a bow tie in A is a pompom or a tassel in B; a cap in A is a collar in B). Do not add a prop that only exists in one face.
- **Reading speed.** Each face should be recognizable in a glance, also at thumbnail size.
- **Avoid:** busy hatching everywhere, tiny details that vanish at small size, text-like squiggles, symmetrical-under-rotation figures (see failures), cartoon clichés that carry no idea.

## 6b. Real examples (for understanding only)

> **[PLACEHOLDER — Cláudio to add and verify.]** Short text descriptions of 1–2 real Whistler reversible drawings (public domain, Wikimedia Commons: *Hair Bald & Bearded*, *Scotsman & Englishman*). Draft below was written from the public images and **must be verified by Cláudio** before use.
>
> *Draft, to verify:*
> - **Hair Bald & Bearded.** Frontal, heavily hatched, a plump face. Upright: a cheerful man with thick wavy hair, crinkled eyes, rosy cheeks and a lopsided smile. Rotated: a tired, bald, bearded man with heavy lids and a furrowed forehead. The eyes are shared (the lids and brows turn "smiling and crinkled" into "weary and baggy"). The *hair* becomes the *beard*; the *smile and chin* become the *forehead and bald dome*; the cheeks stay cheeks (bright round cheek highlights in one are the pouches under the eyes in the other). The ears stay at eye level on both sides.
> - **Scotsman & Englishman.** Two heads in plaid caps. Upright (one reading): a glum, heavy-lidded man with a sour downturned mouth, a small cap with a horseshoe badge on top, and a plaid collar at the bottom with a flower. Rotated: a grinning man with a plaid cap topped by the flower and a collar with the horseshoe buckle. The *cap* becomes the *collar*, the *collar* becomes the *cap*, the frown becomes a smile (cup ↔ dome), the forehead creases become cheek creases, and the flower and horseshoe swap places. The eyes are shared again.
>
> Take from these examples the *principles* (shared eyes; hat ↔ collar, hair ↔ beard, frown ↔ smile; accessories carry the second identity), not their characters.

## 7. Self-check list (do it before delivering, as far as your tools allow)

Judge the drawing as a human will: first looking at it as it stands, then rotated by 180°. A human will score **three things**.

**A. Reversibility: do BOTH faces read?**
- Looking at the file as is: do I see ONE clear upright face (A)? Does B stay hidden? (If I can see B without rotating, B's exclusive strokes are too heavy: lighten, dash or move them.)
- Rotated by 180°: do I see ONE clear upright face (B), recognizably different from A?
- Judge each reading separately and work on the **weaker** one. The result is only as good as the weaker face.
- Are the strokes genuinely shared (double duty), or are there two drawings overlaid?

**B. Artistic quality**
- Economy of line, strong silhouette, clear negative space, character, a coherent look, no gradients or lighting effects.
- Does it still read at thumbnail size?

**C. Humor**
- Forget your own explanation. Do the lines alone show opposite situations in the two faces (opposite expression AND opposite props)? If you need the sentence "A is…, B is…" to justify the reading, it fails.
- Does it say something witty about technology or AI, and does it work for someone who has no idea which event inspired it?
- Does the joke fall on the action or situation and not on anyone's looks or character? Nobody is demeaned?

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

Reply with **only** the complete SVG in a single ```xml code block. No text before or after it, no caption, no description of the drawing (the drawing must speak for itself).
