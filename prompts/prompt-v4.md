# TASK: Draw a Rex Whistler–style REVERSIBLE FACE as one SVG file

You will receive no answers to questions and no feedback. Decide on your own and deliver exactly one SVG.

**Effort budget (important).** Plan in a few short paragraphs (the event, the thesis, the skeleton, the art plan), then write the SVG. Do NOT hand-verify every coordinate, and do not recompute the tables below: use their "page y" values as given and round to multiples of 5. Spend your effort on the *drawing* (confident shapes, character, finish), not on arithmetic. A complete, imperfect SVG is far better than a perfect plan with no file. If you have run low on budget, deliver what you have.

## 1. What you must make

A **reversible face** (in the tradition of Rex Whistler's *¡OHO!*, 1946) is ONE drawing that shows one face when the page is upright and a *different* face when the same page is rotated 180° (a person turns the page, or their phone, upside down).

- As the file stands, it shows **Face A**.
- The same file rotated 180° shows **Face B**.
- B is **not a second drawing**. It is the same strokes, read upside down. The strokes that are B's hat, hair, beard or collar are, in A, the chin, mouth, jaw or neck, and the other way around.
- The drawing carries a **joke about ONE specific, recognizable, recent technology or AI event** (see below). A and B are the two faces of that event. The joke must work *only through the two faces* (their expressions, their accessories, the props, the contrast between them). There is no text to explain it, and you will not be allowed a caption either: if the joke needs a sentence to be understood, it is not drawn yet.

**Make the joke a physical difference.** Before drawing, name the contrast as drawn features: *A has X / B has Y*, where X and Y are lines a viewer can see (e.g. wide-open eyes and a big grin / half-closed heavy lids and a downturned mouth; a proud tall hat / a limp sagging collar). If you cannot name the drawn difference, pick another joke.

Two characters, A and B, are required (no "one person with two moods" variant in this version).

## 1b. The event is the heart of the joke (not a pretext)

- Choose **one specific, real, recent tech/AI event** that a well-informed viewer would recognize at once: a launch, a demo, a leak, a recall, an outage, a lawsuit, a ban, a funding round, a bubble scare, a benchmark scandal, an acquisition, a chatbot blunder. Generic "hype vs. reality" with no identifiable event is a failure. "Technology in general" is a failure.
- You cannot search. Use the **most recent event you know well** (prefer 2025–2026 if you know one; otherwise the latest you are sure about). Do not invent events and do not blur the facts; if you are unsure of a detail, draw what you are sure of.
- **Impact test:** a viewer who knows the event should say "ah, THAT" within seconds of looking at A, and the turn to B should be the punchline of that same event (the *moment of triumph* ↔ *the moment of consequence*; *the promise* ↔ *what actually happened*). If the drawing would work equally well for any other tech story, it has no impact: go more specific.
- **Make the event visible without any text.** Give each face one or two **recognizable props or visual markers of that specific event** (an object, a device shape, a logo-free emblem, a famous gesture or pose, a stage, a rocket, a server rack, a bubble, a cracked screen, a plug, a speech bubble with no letters, a recognizable hairstyle or glasses of an archetype, etc.) inside the hat/hair/beard/collar masses. Prefer a **single bold central prop** over many small ones. Real people may be caricatured **only through the action and the event** (their famous gesture, a pose, a prop); archetypes (the CEO on stage, the regulator, the engineer, the chatbot, the investor) are just as good and safer.
- The joke must fall on an **action, decision or situation**, never on anyone's body, private life, or character, and must not demean any person, company or group. No tragedies, no deaths, no harassment, no hate. The bite is about the *decision or outcome*, not about who someone is.


## 2. Steps

1. Name the event (what, who, roughly when) and choose the idea in one sentence: A = ..., B = ... Two faces of one event (e.g. *the confident launch announcement* ↔ *the same product after the recall*). Then name the physical contrast and the central prop (Section 1).
2. Choose two characters whose silhouettes fit together: a **top-heavy** one (tall hat, big hair) with a **bottom-heavy** one (heavy jaw, beard, mustache, wide collar). At least one should tolerate extra lines (age, wrinkles, beard, fur, textured hat). **A and B must differ in expression, not only in accessories**: change at least two of eye opening, brow angle, mouth curve, jaw width, and age. Two near-identical neutral faces with swapped hats is a failure. **At least one accessory must be unmistakably technological** (headset, cable, antenna, robot visor, charging port, a screen for a face, a circuit-board beard…), with a clearly human counterpart in the other reading; the tech element must be visible and recognizable in its reading. Do not simply default to the single most obvious pairing (hair ↔ beard, hat ↔ collar): use at least three different pairs from the dictionary, and invent the rest.
3. Build a *skeleton first* (Section 5), make it work in both orientations, and only then add detail.
4. Run the self-check (Section 7) in your head or with tools. Fix the weaker reading first. Do not spend more than a short pass on it.
5. Deliver (Section 8).

## 3. The file

- Output must be a standalone SVG that opens directly in a web browser: `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 1000" width="1000" height="1000">`. Valid XML. No external references. At most 300 KB.
- Center of the page = (500, 500). The figure is **centered** there and fills most of the page. The head (crown to chin) should be about **600 px tall**, so the whole figure including hats/collars fits inside about 100–900.
- No side-by-side layout, no two small heads, no scene divided into halves. One figure.
- **Forbidden:** any text (`<text>`, fonts, letter-shaped paths), `<image>`, `<foreignObject>`, `<script>`, gradients, blur/filters, drop shadows or any directional lighting (light from top-left becomes light from bottom-right in the other reading and breaks the illusion).
- **Allowed:** ink line work with varied weight, hatching and cross-hatching (hatching direction survives rotation), flat fills, white/negative space. Use a **limited palette**: paper color + ink color + at most 2 accent colors (max 4 colors in the whole file). Strokes with round caps and joins look best.
- A warm off-white "paper" background rectangle is recommended. A simple thin frame/border inset by 40–60 px is allowed (it looks the same upside down).

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

## 6. Art quality: it must look like a drawing worth framing

Rex Whistler's reversible faces are pen-and-ink caricatures: plump, characterful, confidently drawn, richly hatched, with a clear light/dark rhythm. Your result must read as a **finished caricature illustration**, not as a diagram, an icon or a schematic. Assume the previous attempts looked like stiff clip-art: oval head, two circles for eyes, thin uniform lines, nothing memorable. Do better.

**Caricature and character**
- **Exaggerate.** Push one or two features to 150–200% of normal in each face (a huge bulbous nose, a gigantic jaw, an enormous eyebrow, a tiny pinched mouth, jug ears, a towering hat). A timid, symmetrical, neutral face is the most common failure. Whistler's faces are big, rounded and crinkled, with strong cheeks and heavy brows: push further than feels polite, but in service of the *action*.
- **Characterful features, not generic ones.** Draw eyes with lids, bags and brows that carry the mood (wide-open round eyes and arched brows = delight/alarm; heavy half-closed lids with thick bags = weary/smug; brows slanting down = anger/worry). Give the head an asymmetric silhouette (a jowl on one side, a crooked hat, a tilted nose, one raised brow). Add age lines, wrinkles, cheek folds and creases: they are free strokes that double as hair, beard or collar lines in the other reading.
- **Each face needs a distinct personality.** A and B differ in expression, age or build, and in what they wear. Their contrast is the joke.

**Line and finish**
- **Confident, varied line weight.** Never use one stroke width for everything. Use a heavy contour (10–14 px) for the main silhouette, medium (5–7 px) for features, fine (2–3 px) for hatching and texture. Make **tapered strokes** as thin filled closed shapes (a crescent for a brow, a wedge for a jaw shadow). Thick-to-thin variation is what makes a line look hand-drawn.
- **Fill the masses.** Hair, beard, hat, collar, eyebrows and pupils are **solid dark or tonal masses**, not outlines. Use flat fills for these masses so the page has a clear rhythm of dark, mid and white.
- **Hatching for volume (Whistler finish).** Model cheeks, jowls, under-brow, neck and hat with 6–20 short parallel lines (2–3 px) or cross-hatching. Keep hatch angles consistent (e.g. 45°). Because lighting is forbidden, hatch to describe **form and texture**, never a light direction. Hatching is also the best place to hide B-only strokes in A.
- **Pen-and-ink look.** Small deliberate irregularities are good: a line that overshoots a corner, a slightly wobbly contour made of a path with a few extra control points, a couple of stray stipple dots. Perfect geometric circles for heads or eyes look mechanical: use organic paths.

**Composition**
- **Deliberate composition.** The head fills about 600–650 px of height, centered, with generous margins; the eyes are the focal point. Balance dark masses against white space; do not scatter props evenly. Place the central prop of the event where it is bold and readable (a hat, a collar, a headset, the beard) and keep the rest quiet.
- **Negative space is material.** A white region can be forehead in A and the gap between hair and brow in B. Before adding a line, try changing the white shape.
- **Palette discipline.** Paper + ink + at most 2 accents, used for the *idea* (e.g. one accent for the tech element, one for the human element). No rainbow, no gradients.

**Reversibility craft (unchanged)**
- **Double-duty strokes are the art.** The best moment is when the viewer realizes that the *same curve* is a smile in one face and a hat in the other. Superposition (two independent drawings overlaid) looks like a "double exposure" with ghost contours and is the weakest solution.
- **Global coherence beats local perfection.** A slightly odd stroke reads correctly when the whole configuration is clear. Use ambiguity on purpose.
- **Every prop must make sense in both readings** (a bow tie in A is a pompom or a tassel in B; a cap in A is a collar in B). Do not add a prop that only exists in one face.
- **Reading speed.** Each face should be recognizable in a glance, also at thumbnail size.
- **Avoid:** thin uniform wireframe lines, a perfect oval head, symmetrical faces, busy random hatching everywhere, tiny details that vanish at small size, text-like squiggles, symmetrical-under-rotation figures (see failures), cartoon clichés that carry no idea, generic "robot vs human" without an event.

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

**B. Artistic quality (be a harsh judge)**
- Would this look good **framed on a wall**, as a pen-and-ink caricature? If it looks like clip-art, a diagram or an icon, it fails: add exaggeration, line-weight variation, solid masses and hatching.
- Is there one strong exaggerated feature per face and an asymmetric silhouette? Is the line weight clearly varied (heavy contour, medium features, fine hatching)? Is the palette limited to paper + ink + at most 2 accents? Is the composition deliberate (eyes as focal point, balanced dark and white)?
- Does it still read at thumbnail size? No gradients, filters or lighting effects?

**C. Humor and event impact**
- Forget your own explanation. Do the lines and props alone show opposite situations in the two faces (opposite expression AND opposite props)? If you need the sentence "A is…, B is…" to justify the reading, it fails.
- **Event impact:** would a well-informed viewer recognize the specific event from the props and expressions? Is the turn from A to B the punchline *of that event*? Would the drawing be equally valid for some other tech story? (If yes: sharpen the event.)
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
| Clip-art look | Oval head, uniform thin lines, no character | Exaggerate, vary the line weight, fill masses, add hatching (Section 6). |
| Generic joke | Works for any tech story | Name one specific event and draw its props (Section 1b). |

**Stop rule.** If you can iterate, stop when both readings pass, or after 5 rounds. A complete, imperfect SVG is far better than none.

## 8. Delivery

Reply in exactly this format, nothing else:

1. A first line `EVENT: <the specific event you drew, in one short phrase with approximate date>`
2. A second line `TITLE: <a short title for the drawing, max 8 words>`
3. Then the complete SVG in a single ```xml code block. Inside the SVG, put `<title>` (same title) and `<desc>` (one sentence: the event, what A shows, what B shows) as the first children. These are invisible metadata, not drawn text.

No other text before or after, no explanation. The drawing must speak for itself.
