# Judge comparison: Cláudio vs. rubric vs. David (blind, per orientation)

> **Caveats (Cláudio flagged these as important; see also [`README.md`](README.md)).**
> 1. David is **text-only**: an auxiliary vision model describes each image and he reasons over that text.
> 2. That describer **sometimes hallucinates the expected second face** (for example an old man in the rotated Nano Banana panel).
> 3. David mixed up the **orientation** on the Qwen Image output.
> 4. **Stage 2 is not fully blind** to the rotation (he is told the right panel is the left one turned 180°).
> 5. **One call per cell**: no repeats, no variance estimate.
> 6. The 0-2 rubric is **Peter's own operationalisation** of the gates in prompt v5 section 7, and it was **scored non-blind**, so its 15/15 agreement with Cláudio is **not independent**.
> 7. **GLM 5.3 Max iterated about nine renders** (not one-shot). 8. **Manus 2.0 Lite** header translated from Portuguese. 9. **Meta Muse 1.3** was local-only before and is now included.
> 10. GPT 5.6 Terra (low) and Nemotron 3.5 Lightning were pasted by Cláudio as SVG only; their headers and whether they ran strictly one-shot were not recorded.


Date: 2026-10-29.

## 1. What was done

15 images from `baselines/` were judged three ways: (a) Cláudio's own verdicts, (b) a rubric applied by the first agent (Peter, Cláudio's assistant), (c) David (a Hermes agent), blind, who saw every image in both orientations (as delivered = 0°, and rotated 180°).

- 11 SVGs from text models (prompt v5, rendered with headless Google Chrome at 1000x1000), 4 raster images from image generators (plain "shared eyes" prompt, no tools).
- Each raster/SVG render was rotated 180° with PIL to get the second orientation. Rasters were re-saved without metadata and resized so that the longest side is at most 1000 px.
- Files: see [`david-evals/`](david-evals/): `RAW-ANSWERS.md` (all 45 verbatim answers, un-blinded after the fact), the prompts, `blind-key.json`, `call-codes.json`, `parsed-scores.json`, `vision-describer-excerpts.md`. Renders: [`previews/`](previews/).

## 2. The rubric ("crivo") used

**Where it comes from.** The repository has no scored rubric in force. `docs/methodology.md` and the README state that the human is the judge and that earlier weighted rubrics (`docs/design-history/spec-v0.4.md` §9, superseded) were dropped. The only explicit criteria are the **self-check list in prompt v5, section 7** (Gate 1 reversibility, Gate 2 contrast, Gate 3 light touches), plus the common-failure table below it, and `to-do.md` item 1(e) ("give the evaluation checklist to three models plus one human evaluator"). The first agent (Peter) took these three gates as the "suggested crivo" and turned them into a small 0-2 scale. This operationalisation is Peter's, not Cláudio's; it is meant only to make the gates comparable between judges.

| Item | Source gate | 0 | 1 | 2 |
|---|---|---|---|---|
| **G1a** A (as delivered) reads as ONE clear face | Gate 1 | no readable face | a face, but weak/odd or competing with a second face | one clear face |
| **G1b** B (rotated 180°) reads as ONE clear face, different from A, with its own eyes/nose/mouth/hat | Gate 1 | no face, or only A upside down | a face but incomplete, tiny or confusing | one clear, distinct face |
| **G1c** Integration: strokes genuinely shared; B not visible as a second face in A | Gate 1 / failure table (segregation, ghosting, same orientation) | two drawings stacked, side by side or overlaid | partly shared, some leftover/ghost strokes | genuinely shared strokes |
| **G2** Contrast: opposite expression AND props | Gate 2 | same/similar | some difference | clearly opposite |
| **G3** Light touches (only for SVGs from prompt v5, which asked for an event prop): prop per face, joke on an action, line weight, exaggeration; 0 if the contract is broken (text/letters) | Gate 3 | none/violation | present but weak | clear and funny |

**Core score** = G1a + G1b + G1c + G2 (0-8), comparable across all 15 images. G3 is reported only for the 11 SVGs, because the image generators were given a plain prompt with no event/prop requirement.
**Verdict rule** (Gate order as in the prompt: Gate 1 first, then Gate 2): PASS only if min(G1a, G1b) = 2 **and** G1c ≥ 1 **and** G2 ≥ 1 (and G3 > 0 for SVGs, i.e. the contract holds). Otherwise FAIL.

## 3. How David was invoked

- Same channel as the earlier reviews of this project: the local Hermes CLI, one-shot, non-interactive: `hermes chat --query-file <q> --image <png> --oneshot -Q` (David has a short persona instruction; model `deepseek/deepseek-v4.1-flash-1017` via OpenRouter). I added `-t vision` (only the image toolset) and `--max-turns 6`.
- **Important limitation on what "David sees".** His model is text-only. Hermes first sends the image to an auxiliary vision model, which writes a description that is injected into David's prompt ("The user attached an image. Here's what it contains: ..."), and David may then call `vision_analyze` with his own question. So David's "perception" is David reasoning over a vision model's description, not raw pixels. Excerpts of the pre-descriptions are in [`david-evals/vision-describer-excerpts.md`](david-evals/vision-describer-excerpts.md).
- **Blind:** every call got an anonymous file name (random code, orientation not encoded), no model name, no event/title, no Cláudio verdict, no word about reversible faces or the benchmark. The two orientations were sent in **separate independent sessions**, so he could not compare them; his first-impression perception of each orientation is therefore independent.
- **Stage 1 (30 calls, one per image per orientation)** asked: what do you see, how many faces and which way up, is there one clear face (who/what, expression, missing features), any extra/second/stray element, then scores FACE_CLARITY (0-2), SECOND_FACE_VISIBLE (0-2), EXPRESSION_CLARITY (0-2), OVERALL_FACE_QUALITY (0-5).
- **Stage 2 (15 calls, one per image)**: one picture with the drawing twice side by side (left as delivered, right rotated 180°, told so), asking: the face in each panel, whether they are different, integration (shared strokes vs. stacked), and scores LEFT/RIGHT_READS_AS_FACE, INTEGRATION, CONTRAST, PROPS_AND_JOKE (0-2), BREAKS_RULES, and a PASS/FAIL verdict. Stage 2 is needed because contrast and integration cannot be judged from one orientation. It does reveal to him that the panels are the same drawing rotated.
- Prompts: [`david-evals/prompt-stage1.md`](david-evals/prompt-stage1.md), [`david-evals/prompt-stage2.md`](david-evals/prompt-stage2.md).

## 4. Summary table

PASS/FAIL = verdict. "Mine" = rubric core score (0-8) and verdict. David stage 1 = FACE_CLARITY / SECOND_FACE_VISIBLE at 0° and at 180°. David stage 2 = LEFT / RIGHT face reading, INTEGRATION, CONTRAST, then his own verdict.

| Image | Model | Cláudio | Mine (G1a,G1b,G1c,G2 = core) | David 0° (clarity/2nd face) | David 180° (clarity/2nd face) | David pair (L,R,Int,Contrast) | David verdict |
|---|---|---|---|---|---|---|---|
| img01 | nanobanana-2.1 (raster) | FAIL | 2,1,0,1 = 4 → FAIL | 2/0 | 2/2 | 2,2,2,2 | PASS |
| img02 | chatgpt-medium (svg) | PASS | 2,2,2,2 = 8 → PASS | 2/0 | 2/1 | 2,2,2,2 | PASS |
| img03 | deepseek-v4.1 (svg) | FAIL | 2,1,1,1 = 5 → FAIL | 2/1 | 2/1 | 2,2,2,2 | PASS |
| img04 | qwen3.8-omni-flash (svg) | FAIL | 2,1,1,1 = 5 → FAIL | 2/0 | 1/1 | 2,2,2,1 | FAIL |
| img05 | manus-2.0-lite (svg) | FAIL | 2,1,1,2 = 6 → FAIL | 2/1 | 2/1 | 2,2,2,2 | PASS |
| img06 | gemini-3.1-pro (svg) | PASS | 2,2,2,2 = 8 → PASS | 2/1 | 2/0 | 2,2,2,2 | PASS |
| img07 | qwen-image-3.0 (raster) | FAIL | 1,0,0,2 = 3 → FAIL | 1/2 | 1/2 | 2,2,1,2 | FAIL |
| img08 | glm-5.3-max (svg) | PASS | 2,2,1,1 = 6 → PASS | 2/1 | 2/2 | 2,2,2,2 | PASS |
| img09 | chatgpt-images-2.5 (raster) | FAIL | 2,2,0,2 = 6 → FAIL | 2/2 | 2/1 | 2,2,2,2 | PASS |
| img10 | meta-muse-1.3 (svg) | PASS | 2,2,1,1 = 6 → PASS | 2/1 | 2/0 | 2,2,2,2 | PASS |
| img11 | grok-imagine-2.0 (raster) | FAIL | 2,2,0,2 = 6 → FAIL | 1/2 | 2/2 | 2,2,2,2 | PASS |
| img12 | claude-sonnet-5.5-medium (svg) | PASS | 2,2,2,2 = 8 → PASS | 2/2 | 2/1 | 2,2,2,2 | PASS |
| img13 | qwen-3.7-plus (svg) | FAIL | 1,1,1,0 = 3 → FAIL | 2/2 | 1/1 | 2,2,2,2 | PASS |
| img14 | gpt-5.6-terra-low (svg) | PASS | 2,2,2,2 = 8 → PASS | 2/1 | 2/0 | 2,2,2,2 | PASS |
| img15 | nemotron-3.5-lightning (svg) | PASS | 2,2,1,1 = 6 → PASS | 2/0 | 2/0 | 2,2,2,2 | PASS |

## 5. Per-image detail (David's words are verbatim quotes from his raw answers)

### img01: nanobanana-2.1 (raster, plain prompt)

- **Cláudio:** FAIL. "one head with a tiny head hidden in the collar"
- **Rubric (mine):** G1a=2, G1b=1, G1c=0, G2=1, G3=n/a; core 4/8 → **FAIL**. A is one clear lady; the only second face is a tiny old man in the collar/ruff. Rotated, the large face is still the same lady (upside down). Second reading is too small to count.
- **David at 0° (as delivered)** (`s918`; clarity 2, second-face 0, expression 2, quality 4/5):
  - saw: "An ornate vintage engraving-style portrait framed by filigree corners and hatched borders. A woman with a calm, faint smile looks straight at the viewer, her face stippled and cross-hatched. Enormous sculpted curls frame her head, topped by a small bonnet-like fascinator, with a heavy ruffled collar and bow below."
  - faces: "One clear human face/head, centred in the frame, upright (en face). No other recognisable head, upright or inverted."
  - main face: "Yes, one clear face. A young-to-middle-aged woman, serene and slightly enigmatic, faint closed-mouth smile. Clearly present: eyes with defined irises and lashes, arched brows, straight nose with nostrils, full lips, abundant curly hair, small hat with ribbon and leaves, high frilled collar with bow. Slight oddity: pupils uneven, hat ornaments nonsensical, collar melts into leaf-like hair strands."
- **David at 180° (rotated)** (`s358`; clarity 2, second-face 2, expression 2, quality 4/5):
  - saw: "A sepia-toned, engraving-style line drawing inside a double-ruled frame with scrollwork corners and hatched vignette shading. The centre is a mass of swirling, curling hair that resolves into a face staring straight out. Fine cross-hatching does all the modelling, giving it an antique, slightly unsettling quality."
  - faces: "Two large heads share the composition — an upright older man occupying the upper half, and an upside-down face in the lower half formed from the same features (its forehead is the upright man's chin, its hairline is his mouth line). A third, tiny tilted mask-like face sits at the very bottom, tangled in the curls."
  - main face: "Yes, one dominant face: an elderly, stern-looking man, likely male, no hat. Thick wavy hair parted centrally, heavy drooping eyelids, bags under the eyes, furrowed brow, prominent straight nose, downturned thin mouth. Expression: weary, severe, brooding. Eyes, nose, brows and hair are strong; the mouth is only implied (a shared contour), and the chin/jaw is soft and merges into the inverted head."
- **David on the pair** (`p932`): left 2, right 2, integration 2, contrast 2, joke 2, breaks rules: no.
  - left: "A young woman, upright, frontal. Large wide eyes, arched brows, small nose, gentle closed-mouth smile; soft rounded cheeks. Ornate curled/ringleted dark hair falling to the shoulders, a small tilted hat with leaves/ribbon on top, and a high ruffled collar closed by a large bow. Expression: sweet, mild, slightly coy."
  - right: "The same figure inverted. Read upright it is an older man: heavy furrowed brow, deep-set eyes, long prominent nose, thick drooping mustache, and a broad wavy beard/sideburns formed by the curls; a dark cap-like shape (the bow and collar) sits at the bottom. Expression: stern, severe, scowling — almost glaring."
  - different?: "Clearly DIFFERENT characters — a young smiling woman vs a grim bearded old man. Two faces, not one face upside down. Both panels read as faces."
  - integration: "Genuinely shared strokes, not two stacked drawings. The same contour lines do double duty: the woman's forehead/chin becomes the man's chin/brow, her nose becomes his mouth area, her eye-shading becomes his eye-sockets, her curls become his beard and hair, her bow/collar becomes his headgear. No second, separately drawn face is pasted into either panel."
  - verdict: "PASS — both orientations resolve into clear, strongly contrasting characters built from one set of shared engraved strokes, with no text or foreign elements."

### img02: chatgpt-medium (SVG, prompt v5)

- **Cláudio:** PASS. "passed"
- **Rubric (mine):** G1a=2, G1b=2, G1c=2, G2=2, G3=1; core 8/8 → **PASS**. A: smiling dark-haired man with a collar; B: stern bearded man. Hair = beard, collar = hat. Shared eyes work. Rocket prop on both faces (same prop, so weak contrast of props).
- **David at 0° (as delivered)** (`s433`; clarity 2, second-face 0, expression 2, quality 4/5):
  - saw: "A flat-vector head-and-shoulders portrait on plain beige, drawn with heavy black outlines and a beige/teal/red palette. A broad-jawed adult with black widow's-peak hair and a teal scoop-neck shirt looks straight out. The first thing that strikes me is the small red-and-white rocket-like object standing upright on the crown of the head."
  - faces: "One clear human face/head, centered, upright. No second human face — the only other "face-like" thing is a single white circle with a black dot on the topknot, which is a porthole/eye motif, not a face."
  - main face: "Yes, one clear face. Adult, androgynous, slightly masculine, no hat, thick black hair with a sharp widow's peak and thin white highlight strokes, teal shirt with two white downward chevrons. Expression calm, eyes wide and forward, slight closed-mouth smile — mildly blank but readable. Present: both eyes with pupils and highlights, brows, hooked line nose, mouth, ears, hair. Odd: a vertical black line with a short crossbar runs down the forehead from the hairline like a stylized symbol; straight horizontal lines sit under each eye."
- **David at 180° (rotated)** (`s302`; clarity 2, second-face 1, expression 2, quality 4/5):
  - saw: "A flat, vector-style bust of a bald, bearded man in thick black outlines on cream. The face is built almost entirely from the beard, brows and heavy dark eyes. It reads immediately as a stern cartoon portrait, and the shapes look deliberately ambiguous — a topsy-turvy type design."
  - faces: "One unmistakable upright head, centred. A second, upside-down head appears only if the picture is mentally inverted (the beard becomes headwear, the chin ornament becomes a crown jewel) — that one is faint/inferred, not plainly visible in the given orientation."
  - main face: "One clear face: a middle-aged to older male character, bald, huge bushy black beard and moustache, tiny teal trapezoid cap with two white chevrons at the very top. Expression: stern, scowling, slightly cross-eyed stare from the heavy angled brows. Present and clear: eyes, brows, hat, beard, ears, forehead crease. Odd/missing: nose is a single line ending in a small V, mouth is almost fully buried (only a small red curve), under-eye bags double as chevron accents, and the small red diamond-and-squiggle ornament hangs below the beard like a pendant or tie."
- **David on the pair** (`p295`): left 2, right 2, integration 2, contrast 2, joke 2, breaks rules: no.
  - left: "Young man, calm and mildly friendly, slight closed-mouth smile. Black bowl-cut hair with wavy texture lines, small red finial/topknot at the crown, arched brows, almond eyes, small hooked nose, teal V-collar with two white chevrons."
  - right: "Old, stern bearded man. The bowl cut now reads as a full black beard and moustache, the teal collar as a green flat cap with the same two chevrons, the topknot as a small dangling ornament under the chin. Same eyes but heavier, hooked line now points up as a forehead crease, mouth line reads as a grimace. Expression: older, grumpy."
  - different?: "Two clearly DIFFERENT faces — same drawing rotated 180°, and both readings are legible."
  - integration: "Genuinely shared strokes, not two stacked drawings. The hair of the young man is the beard of the old man, the collar is the cap, the topknot is the chin ornament, the nose line becomes the forehead crease. No second separate face piece appears anywhere in either panel."
  - verdict: "PASS — both panels resolve into clear, distinct characters (young man / bearded old man) built entirely from the same shared contours, which is exactly what a reversible face requires."

### img03: deepseek-v4.1 (SVG, prompt v5)

- **Cláudio:** FAIL. "failed; the face cannot be identified when rotated"
- **Rubric (mine):** G1a=2, G1b=1, G1c=1, G2=1, G3=1; core 5/8 → **FAIL**. A reads. In B the eyes and black beard read, but A's nose/mouth strokes end up above the eyes in B (misplaced features), so B is only half a face.
- **David at 0° (as delivered)** (`s346`; clarity 2, second-face 1, expression 2, quality 4/5):
  - saw: "A flat, cream-background vector portrait: an egg-shaped head in thick black outline, a solid black beanie with a white rocket glyph, arched brows, almond eyes with dot pupils, a U-shaped nose, a faint smile, a straight chin line, and a rust-red bowtie at the neck. Clean, symmetrical, almost logo-like. Almost nothing is shaded; it lives on outlines and negative space."
  - faces: "One upright face, centred, filling most of the frame. A second head is strongly implied upside-down at the bottom (the bowtie reading as a red cap, the chin line as a forehead, the mouth as heavy brows), but it only resolves if you mentally flip the image."
  - main face: "One clear face — a young, androgynous, cartoonish character, plausible astronaut/space cadet given the rocket patch. No hair, ears, or clothing beyond the bowtie. Expression is calm and faintly amused. Eyes, brows, nose, mouth, chin and hat are all present; the horizontal cheek lines and under-eye hooks are odd, anatomically arbitrary strokes."
- **David at 180° (rotated)** (`s297`; clarity 2, second-face 1, expression 1, quality 3/5):
  - saw: "A minimal flat-vector portrait on cream: an egg-shaped head with thick black outline, arched brows, almond eyes with catchlights, and a solid black beard filling the lower half. A terracotta bow tie floats above, tethered by two thin lines; a small white emblem sits inside the beard. It reads as a whimsical, stylised "portrait badge.""
  - faces: "One clear human head, centred and upright, filling the frame. A second, much smaller face-like shape is suggested inside the white emblem on the beard (upright but abstract)."
  - main face: "An adult male, seemingly older (forehead crease lines, slight bald crown), wearing a bow tie; heavily bearded. Expression is neutral, calm, faintly bemused. Clearly present: eyes, brows, beard, hairline/crown lines, cheek contours, bow tie. Missing or odd: no nose at all, no ears, mouth reduced to a thin white smile line, no visible neck or shoulders."
- **David on the pair** (`p619`): left 2, right 2, integration 2, contrast 2, joke 2, breaks rules: no.
  - left: "A stern, straight-faced man — long oval head, flat black skullcap with a small white crest/rocket emblem, arched brows, almond eyes, a U-shaped nose, a flat closed mouth, thin neck and a terracotta bow tie. Neutral/serious expression."
  - right: "A bald, cheerful older man with a big solid black beard filling the lower half of the head, a wide smiling mouth, wrinkles above the brows, and a terracotta bow perched on top of his head (like a hair bow), with two little lines rising from it. Goofy, amused expression."
  - different?: "Clearly DIFFERENT faces — a grim capped gentleman versus a jolly bald bearded man — produced by the same drawing turned 180°."
  - integration: "Genuinely shared strokes. The black cap is the black beard; the bow tie at the neck becomes the bow on the head; the neck lines become strands above the head; the chin/jaw line becomes the hairline; the nose and mouth become brow furrows and a wide grin. Nothing is stacked or overlaid — every element does double duty."
  - verdict: "PASS — both orientations read instantly as clear, distinctly different characters, and the transformation comes entirely from rereading shared strokes."

### img04: qwen3.8-omni-flash (SVG, prompt v5)

- **Cláudio:** FAIL. "failed; no face when rotated"
- **Rubric (mine):** G1a=2, G1b=1, G1c=1, G2=1, G3=1; core 5/8 → **FAIL**. A reads (smile, pointed cap). B has eyes and a 7-shaped nose but the mouth/hat zone is just a line and floating hat pieces; weak and not clearly different from A.
- **David at 0° (as delivered)** (`s942`; clarity 2, second-face 0, expression 2, quality 4/5):
  - saw: "A bold, thick-line cartoon drawing centered on white: a smiling figure in a tall pointed hat and a wide bowl-shaped collar. The hat's emblem is abstract. The only color in the whole picture is a small red circle acting as a clasp or button on the collar."
  - faces: "One. It sits center-frame and is upright, facing the viewer frontally. No inverted or secondary head is recognisable."
  - main face: "Yes, one clear face. A stylized, ageless, gender-neutral character — reminiscent of a jester, bishop or playing-card figure. Expression: calm, gently smiling, friendly and slightly blank. Present: brows (arched), eyes (circles with solid pupils), nose (long line with a hook), mouth (single upward curve), tall pointed hat with a band and circular emblem. Missing/odd: no hair, no ears, no defined neck; the nose hook is oddly angular and the chin tapers very sharply."
- **David at 180° (rotated)** (`s217`; clarity 1, second-face 1, expression 2, quality 3/5):
  - saw: "A tall, egg-shaped cartoon head drawn in thick black lines on white, topped by a dome-like hat with a single bright red dot. Round eyes with dot pupils, a hooked vertical nose line, and a wide curved smile dominate the middle. The bottom tapers to a sharp point containing a small circle with an X/cross inside."
  - faces: "Two readable faces. The main one sits upright in the upper/central oval. A second, upside-down face occupies the tapered lower section, with the dividing horizontal line acting as its mouth and the circled X as its eye/eye-patch."
  - main face: "Yes, one clear face: a simple, ageless cartoon figure, gender-neutral, wearing a domed cap with a red button/pompom. Expression is cheerful and slightly goofy, smiling broadly. Eyes, nose, mouth and hat are clearly present; brows are only suggested by a faint curved line, and there is no hair, ears, beard or clothing."
- **David on the pair** (`p955`): left 2, right 2, integration 2, contrast 1, joke 1, breaks rules: no.
  - left: "A stylized, cartoonish human face — elongated oval head, round dot-pupil eyes with arched brows, a hooked nose, and an upward-curving smile (friendly/cheerful). Topped by a pointed mitre-like hat containing a circle with an X/cross and a small hook mark; below the chin a bowl-shaped collar crossed by a horizontal line, with a solid red dot at its base."
  - right: "The same drawn face, now inverted: oval head, dot-pupil eyes, curved nose, and curved mouth lines. Above it, a rounded brim/dome carrying a horizontal line and the red dot at the very top (reads as a wide-brimmed hat with a red button/pompom); below it a downward-pointing triangle with the circle-and-X emblem (reads as a pointed collar, pendant, or small beard)."
  - different?: "Same face upside down — the two readings are the same smiling character in different headgear; not two clearly different characters, and neither panel is a non-face."
  - integration: "Genuinely shared strokes. The mitre and its emblem become the pointed collar/pendant, the collar becomes the hat brim, and the red dot migrates from collar to hat top. Nothing is stacked or overlaid."
  - verdict: "FAIL — the rotation is technically clean and the shared strokes are real, but both panels resolve to essentially the same cheerful face with only a headgear swap, so there is no clearly different second character or contrasting expression."

### img05: manus-2.0-lite (SVG, prompt v5)

- **Cláudio:** FAIL. "the second face is not clear"
- **Rubric (mine):** G1a=2, G1b=1, G1c=1, G2=2, G3=1; core 6/8 → **FAIL**. A clear. B reads as a bearded man, but a brown nose stroke sits on B's forehead (A's nose) and a cream mouth bar/sound-wave marks in A's hair are a faint ghost of B visible upright.
- **David at 0° (as delivered)** (`s399`; clarity 2, second-face 1, expression 2, quality 4/5):
  - saw: "A flat vector head-and-shoulders portrait on a cream background: peach skin, thick dark outlines, teal collar with white trim and a red diamond. The most striking thing is the very large dark hair mass with small white and teal marks that hint at a pattern above the forehead."
  - faces: "One unambiguous upright human head, centered/lower-middle. The hair above it contains marks that faintly suggest a second, upside-down face, but this is not clearly readable."
  - main face: "Yes, one clear face — a young, neutral-gender cartoon character with short dark bowl-cut hair, rounded ears, thick arched brows, almond eyes with white highlights, an L-shaped terracotta nose, and a closed gentle smile. Visible: eyes, brows, nose, mouth, ears, hair, teal shirt with collar and diamond emblem. Nothing important is missing; features are simple but consistent. Slight under-eye creases give a calm, friendly, faintly amused look."
- **David at 180° (rotated)** (`s587`; clarity 2, second-face 1, expression 2, quality 4/5):
  - saw: "A flat, vector-style head on beige — bald, bearded man wearing a teal pillbox-style cap with a small red diamond emblem on top. Thick charcoal outlines, heavy brows, almond eyes with bags, small tooth-like mouth sunk in a big black beard, plus a reddish "7"-shaped mark on the forehead and a red tab under the chin."
  - faces: "One clear head, centered and upright (the bearded man). A faint secondary face reading is arguable in the upper half only if you deliberately re-map the brows/eyes as a face, but it is not a distinct, self-contained second face."
  - main face: "Yes, one clear face: a middle-aged to older man, bald with a full dark beard, in a flat teal cap. Expression is stern, tired, faintly grumpy. All features are present — eyes, thick brows, hint of nose, small rectangular mouth, ears, hat, beard — the nose is nearly absent, implied only by the mustache edge, and the forehead mark is odd."
- **David on the pair** (`p497`): left 2, right 2, integration 2, contrast 2, joke 2, breaks rules: no.
  - left: "Young, round-faced man (East Asian official/scholar type), calm gentle smile, arched brows, open friendly eyes. Solid black hair with widow's peak, small red tab at crown, white/teal cloud emblem on the forehead, three teal shine lines on the hair; teal collar with white trim and a red diamond at the throat."
  - right: "Same silhouette read as an older, stern bearded elder — heavy-lidded eyes, frowning down-angled brows, eyesore lines, a reddish-brown hook/"7" mark and wrinkle on the bald forehead. Teal flat-topped cap with white trim and a red diamond; large black mustache-and-beard covering the whole lower face, containing the same white/teal emblem, three teal lines on the beard's left side, and a small red tab at the beard's bottom tip."
  - different?: "Two clearly DIFFERENT characters — a young slight-figure with a collar versus an old bearded figure in a cap — produced by the same drawing flipped 180°, not two unrelated faces."
  - integration: "genuinely shared strokes. Every element swaps roles: hair becomes beard, collar becomes cap, the forehead emblem becomes the beard's mouth-ornament, the three hair-shine lines become beard shine, and the two red diamonds are the same mark relocated."
  - verdict: "PASS — both orientations read as clear, distinct faces whose every accessory is re-parsed from the identical strokes of one drawing."

### img06: gemini-3.1-pro (SVG, prompt v5)

- **Cláudio:** PASS. "passed, with some humor"
- **Rubric (mine):** G1a=2, G1b=2, G1c=2, G2=2, G3=1; core 8/8 → **PASS**. A: furrowed-brow smirk with black hair and beard; B: sad frown. Strokes genuinely shared (hair = beard); rocket+star prop on both ends.
- **David at 0° (as delivered)** (`s671`; clarity 2, second-face 1, expression 2, quality 4/5):
  - saw: "A flat, cartoonish head with pale peach skin, bold black outlines, a solid black flat-top hair mass, and a black beard across the lower jaw. A small star-tipped rocket sits centered on top of the head. Thin white "pop" lines curve above the hair and below the beard on a plain beige background."
  - faces: "Two. One upright in the center (beard at bottom, hair at top). One upside-down in the same central figure — the beard reads as hair, the white gap as a wide toothy grin, and the rocket hangs below as a pendant."
  - main face: "Yes, one clear face: a bearded adult man, gender masculine, no visible age cues, wearing no hat (flat-top black hair). Expression is mild, calm, faintly amused with a small closed smile and eyes glancing to the side. Present clearly: eyes with pupils and catchlights, angular nose, small mouth, eyebrows, ears, hair, beard. Odd: the mouth sits very close to the beard with a white gap that reads like teeth."
- **David at 180° (rotated)** (`s726`; clarity 2, second-face 0, expression 2, quality 3/5):
  - saw: "A flat vector cartoon head of a stern, bearded man against plain cream, drawn in bold black outlines. The single most striking thing: a tiny striped rocket with a red nose cone and a yellow star exhaust pokes downward out of his beard where a mouth should be. The style is minimalist and slightly surreal."
  - faces: "One recognizable human head, centered and upright, facing forward."
  - main face: "One clear face — a middle-aged adult male, cartoonish and grumpy; short flat-top black hair, large solid black beard covering jaw and chin, simple ears. Expression is angry/stern: heavy brows angled down toward a forehead crease, round white eyes with small inward-set pupils, under-eye creases. Eyes, brows, hair, beard, ears, nose line all present. Missing: no visible mouth at all — the rocket occupies that spot, which is odd."
- **David on the pair** (`p287`): left 2, right 2, integration 2, contrast 2, joke 2, breaks rules: no.
  - left: "A calm, slightly amused man — pale oval face, black cap-like hair with a straight hatching hairline, large black U-shaped beard with hatched top edge, round eyes with forward pupils, arched brows, small angular nose, faint upturned smile. A striped rocket with a yellow star stands upright on top of his head, like a little antenna/launchpad."
  - right: "The same drawn head, now reading as a stern, grumpy man — heavy black hair mass above, furrowed downward brows, pupils looking down/inward, distinct frown, big black beard covering the jaw. The same rocket hangs downward inside the beard, star at the bottom, as if it crashed or is being swallowed by the chin."
  - different?: "Same face upside down — the identical strokes and colors, rotated 180°, deliberately read as two different characters (placid optimist vs. scowling grump)."
  - integration: "Genuinely shared strokes. The left's hairline becomes the right's beard's top hatch marks; the left's beard becomes the right's hair; the ears swap sides; the smile arc becomes the frown. Nothing is stacked or duplicated as a second separate piece — one set of lines does double duty."
  - verdict: "PASS — both orientations read immediately as clear, distinct faces with opposed expression and prop direction, drawn from one shared set of strokes."

### img07: qwen-image-3.0 (raster, plain prompt)

- **Cláudio:** FAIL. ""Dois rostos empilhados" (two stacked faces)"
- **Rubric (mine):** G1a=1, G1b=0, G1c=0, G2=2, G3=n/a; core 3/8 → **FAIL**. Two stacked upright faces (lady above, old man below), both upright at 0 degrees; rotated, both inverted. No second reading from shared strokes (the "same orientation" failure).
- **David at 0° (as delivered)** (`s343`; clarity 1, second-face 2, expression 1, quality 4/5):
  - saw: "A dense graphite drawing built entirely from shared contours: a soft young woman's face at the top and a weathered older man's face directly beneath, with one jawline serving as the other's forehead. The pencil work is heavy and detailed, dark curls merging into a beard. It reads immediately as a deliberate two-in-one illusion."
  - faces: "Two. The woman is in the upper half, upright. The man is in the lower half; he is upside-down relative to her, although his features read as a forward-facing face when the composition is flipped."
  - main face: "There is no single clear face — the two compete almost equally. The woman: young, serene, wide almond eyes, arched brows, small nose, faint closed-mouth smile, elaborate rose-trimmed wide-brim hat and tightly curled hair. All features present and coherent. The man: older, stern, deep-set hooded eyes, furrowed brow, broad nose, straight downturned mouth, heavy wrinkles, full beard."
- **David at 180° (rotated)** (`s248`; clarity 1, second-face 2, expression 1, quality 4/5):
  - saw: "A densely worked graphite drawing in which a mass of looping curly hair frames a single central facial complex, with a ribboned bowl of roses beneath it. My first impression is of one elaborate head, but the features keep re-organising: the same eyes, nose and mouth support two different readings. Lighting is soft and blended on the centre, harsher in the upper region."
  - faces: "Two. An older woman's face in the upper half, upright (forehead at top, chin pointing down to the centre). A younger woman's face in the lower/central area, inverted — chin toward the centre, mouth above the eyes, forehead below, hair spreading to the bottom."
  - main face: "No single dominant face; the drawing is a deliberate ambiguity. The clearest read is the upper, upright older woman: female, elderly, heavy-lidded shadowed eyes, wrinkled brow, thin set mouth, stern and weary. Eyes, nose, mouth, brows and hair all present; ears and neck absent, hidden by the hair."
- **David on the pair** (`p439`): left 2, right 2, integration 1, contrast 2, joke 1, breaks rules: no.
  - left: "Upright young woman — large eyes, small nose, gentle closed-mouth smile, voluminous curly hair; a flowered (roses, leaves, ribbon) hat sits at the very top of the panel. Below her chin, a second, fully drawn older man: heavy brow, deep-set eyes, big nose, mustache, full curly beard at the bottom edge. Two complete faces stacked in one panel."
  - right: "The same sheet rotated 180°. The old man reads at the top, upside down (beard now pointing up at the edge, inverted eyes/nose/mouth); the young woman reads at the bottom, also inverted, with her hat and roses hanging at the very bottom."
  - different?: "Two faces are visible in each panel, but they are the two faces from the same drawing seen inverted — a woman and an old man stacked, not one face that flips into a different character."
  - integration: "Only hair/beard and outline texture is shared at the seam; the eyes, noses and mouths are drawn separately at different heights. This reads as two complete faces stacked vertically (one above the other), not one set of strokes that yields two characters."
  - verdict: "FAIL — both panels show faces and their features are opposite in age and props, but the panel contains two separate stacked faces rather than one set of shared strokes flipping into another character, so it is not a genuine reversible face."

### img08: glm-5.3-max (SVG, prompt v5)

- **Cláudio:** PASS. "complied with the task, although the image came out strange (caveat: ~9 renders, not one-shot)"
- **Rubric (mine):** G1a=2, G1b=2, G1c=1, G2=1, G3=1; core 6/8 → **PASS**. Both orientations read as faces (grin with teeth/hood vs. surprised mouth/teeth hat band). Cluttered and strange (cheek discs, clouds), contrast between A and B only moderate.
- **David at 0° (as delivered)** (`s669`; clarity 2, second-face 1, expression 2, quality 4/5):
  - saw: "A flat, poster-style mask in cream, black and one red accent, dead-centre and fiercely symmetrical. A pointed black hood with a single white eye-slit sits on a large egg-shaped head with small loop ears. The wide rectangular grin of square white teeth and a black chin crossed by a red zigzag give it a manic, staring look, framed top and bottom by scalloped cloud shapes."
  - faces: "One human head, upright, filling the middle of the picture. A faint, small face-like reading exists in the pointed hood at top (still upright); nothing readable below."
  - main face: "One clear face — adult, gender-ambiguous, mask-like, tribal/totem character. No hair; wears a tall pointed hood/hat with an eye ornament and a cloud pompom, and a scalloped collar. Expression: wide-eyed, toothy, manic-surprised, slightly unsettling. Clearly present: eyes with pupils and catchlights, thick brows, a wide mouth with teeth, nose line, ears. Odd: no visible chin outline (chin is black), the `( o )` mark on the forehead, double dot clusters, and the red zigzag reading as a scar or second mouth."
- **David at 180° (rotated)** (`s745`; clarity 2, second-face 2, expression 2, quality 4/5):
  - saw: "A flat, symmetrical vector-style head in cream, black and one dark red accent, like a Daruma doll crossed with a cartoon character. A scalloped cloud floats above and an inverted one hangs below. Everything is heavy black outline, no shading. The striking thing is that the shapes look deliberately double-loaded."
  - faces: "Two heads share the same central oval. One upright, centred: cap with red zigzag, round staring eyes, black cheek discs, small nose, wide black beard/mouth. One upside-down, same space: the beard reads as a hat, the cheek discs as eyes, the tooth-band as a grin, the top cloud as a collar."
  - main face: "The upright one dominates. An ageless, sexless stylised character — doll, robot or masked figure — wearing a black helmet/cap with a red crack and a white segmented band, plus a heavy black beard or open mouth. Expression: wide-eyed, fixed, faintly stern or startled. Present: eyes, brows, nose, mouth/beard, headwear, ears. Odd: no real chin, mouth and beard merge, eyes are rings rather than eyes."
- **David on the pair** (`p429`): left 2, right 2, integration 2, contrast 2, joke 2, breaks rules: no.
  - left: "A jester/clown-like mask — wide concentric-circle eyes, arched brows, small nose-line curving into a smile, broad grille "toothy grin" below it, black chin patch with a red zigzag, two black hair puffs on the forehead, a pointed black hat with a white dot near the tip and a scalloped cloud pom-pom above; scalloped cloud collar at the base."
  - right: "A stern, grumpy mask — same round eyes with cheek wrinkles, but the grille now sits high as a blocky brow/headband, a heavy down-curving line reads as frown (or big nose), a solid black downturned mouth, black cheek pads low on the face, red-zigzag black cap on top, and a black pointed goatee with a white dot pointing down, over a cloud collar."
  - different?: "Clearly two DIFFERENT characters: cheerful jester vs. stern/grumpy mask — and they are one drawing upside down, not two drawings."
  - integration: "Fully shared strokes. The jester's hat and pom-pom become the goatee and collar; the chin patch with red zigzag becomes the zigzag cap; the toothy mouth becomes the brow band; the forehead hair puffs become cheek pads; smile becomes frown. Same lines, no separate overlaid face."
  - verdict: "PASS — both orientations read as clear, distinct faces built from exactly the same strokes, with opposed expressions and accessories."

### img09: chatgpt-images-2.5 (raster, plain prompt)

- **Cláudio:** FAIL. "two half-heads stacked"
- **Rubric (mine):** G1a=2, G1b=2, G1c=0, G2=2, G3=n/a; core 6/8 → **FAIL**. Lady upright on top with an old man inverted below; rotated, the old man is upright. Each orientation has a clear face but the other face is fully visible (two heads joined at the collar), so there is no integration.
- **David at 0° (as delivered)** (`s776`; clarity 2, second-face 2, expression 2, quality 5/5):
  - saw: "A finely hatched, engraving-style black-and-white portrait of a young woman in a wide-brimmed hat covered with flowers and a large feather, her curls and ruffled collar filling the lower part. The line work is dense and skilful, with an antique, romantic feel. It is an ambiguous "two-in-one" image."
  - faces: "Two. A woman's face in the upper half, upright and looking out at the viewer. An older bearded man in the lower half, upside-down relative to her — his forehead and eyes formed by her neck and collar, his nose by her chin, his beard by her curls."
  - main face: "The young woman is the dominant reading — a graceful, serene, idealized young woman, maybe late teens or twenties. She wears a broad dark hat with a rose and blossoms on the left, a sweeping feather on the right, voluminous ringlets and a lace ruffle at the neck. Expression: calm, faint smile, slightly enigmatic. Eyes, brows, nose, mouth and hair/hat are all clear and well drawn; only the shoulders are absent."
- **David at 180° (rotated)** (`s612`; clarity 2, second-face 1, expression 2, quality 4/5):
  - saw: "A dense black-and-white engraving-style drawing, full of curling hair, cross-hatching and a plumed hat, built so the same contours flip between two readings. My eye locks first onto a stern, bearded head in the upper half, then notices a second, softer face hiding in the lower half."
  - faces: "Two. Upper-centre head, upright — a hatted older man. Lower-centre head, upside-down in this orientation — a younger, smoother face that becomes upright if the picture is turned."
  - main face: "Yes, the upright man is the clear one — elderly, male, severe; wide-brimmed dark hat with feather and round brooch, thick wavy hair, heavy brows, deep-set eyes, strong nose, and a broad upcurled moustache. Expression: stern, intense, confrontational. Eyes, brows, nose and moustache are clearly present; the mouth is barely visible, swallowed by the moustache, and the "chin" area doubles oddly as the second face's forehead."
- **David on the pair** (`p220`): left 2, right 2, integration 2, contrast 2, joke 2, breaks rules: no.
  - left: "Upright reads clearly as a young woman — smooth face, large eyes, small nose, gentle closed-mouth smile, voluminous curly hair, wide-brimmed hat with a rose, small blossoms, leaves and a long sweeping feather, ruffled collar; a small round brooch sits low at the left. Inverted, the same strokes read as an old man with a bulbous nose, squinting eyes and a massive bushy beard, the hat becoming his collar/shoulders."
  - right: "The identical drawing turned 180°. Upright it reads as a stern old man — furrowed brow, intense glaring eyes, prominent nose, heavy mustache/beard, dark slouch hat with feather and round brooch, white ruffled collar. Inverted, the same lines read as the young woman with the floral hat and feather, serene expression."
  - different?: "Two clearly DIFFERENT faces: young gentle woman vs. stern old man — not the same character, and both panels are genuine faces."
  - integration: "Genuinely shared strokes. One continuous engraving; the woman's jaw is the man's nose, her curly hair is his beard, her hat with flowers/feather is his collar and shoulders, and his mustache becomes her brows/lashes. No second, separately outlined face is pasted in."
  - verdict: "PASS — both orientations read as clear, opposite characters built from the identical lines, exactly the reversible-face effect required."

### img10: meta-muse-1.3 (SVG, prompt v5)

- **Cláudio:** PASS. "simple, reasonably executed"
- **Rubric (mine):** G1a=2, G1b=2, G1c=1, G2=1, G3=1; core 6/8 → **PASS**. Minimal, floating strokes. A: smiling face with a blue hat band; B: frowning face with the band as a chin/mouth bar. Both read; some marks are orphaned.
- **David at 0° (as delivered)** (`s102`; clarity 2, second-face 1, expression 2, quality 3/5):
  - saw: "A thick black oval head on white, with big concentric-circle eyes, a small nose, and a wide upward smile. A single bright blue horizontal bar sits on the forehead under a wavy line. A tiny hollow circle floats above the head. Minimal, icon-like, slightly cartoonish."
  - faces: "One large upright face filling the oval. The upper forehead marks (blue bar plus two stacked short curves under the wavy line) can also be read as a small, faint second face in the same upright-ish orientation — it is a suggestion, not a fully drawn head."
  - main face: "Yes, one clear face. Reads as a simple, ageless, gender-neutral cartoon character — bald, no hat, hair, beard, or clothes; only a curved line below suggesting a chin/neckline. Expression: cheerful, gently smiling. Present: two eyes with pupils, brows, nose, mouth. Missing: ears, hair, any real jaw structure; the pupils are oddly large concentric circles, and the forehead has decorative marks that don't belong to human anatomy."
- **David at 180° (rotated)** (`s971`; clarity 2, second-face 0, expression 2, quality 4/5):
  - saw: "A stark black-line cartoon head on white, dominated by a thick bright-blue horizontal bar across the mouth like tape. The eyes are wide, ringed double circles with dot pupils, under-eye curves and stacked forehead wrinkles intensifying a worried stare. Everything is symmetrical and centered, with one arc floating above the head and one small hollow circle below."
  - faces: "One distinct head — centered, filling most of the frame, upright. No other faces, upright or inverted."
  - main face: "Single clear face; an older, gender-neutral cartoon character, hard to age precisely — wrinkled brow reads elderly. Expression: startled, anxious, silenced — wide-eyed alarm behind a taped-shut mouth. Present: eyes with pupils, brows, forehead wrinkles, nose, partial mouth line, chin line. Missing/odd: no hair, ears, neck, arms or clothes; the blue bar replaces the lips entirely; the arc above and circle below float detached."
- **David on the pair** (`p189`): left 2, right 2, integration 2, contrast 2, joke 2, breaks rules: no.
  - left: "A cheerful, smiling cartoon person — big concentric-circle eyes with pupils, arched eyebrows, small nose, wide upturned smile, calm/pleasant. On the head: a thick blue horizontal bar high on the forehead reading as a hat brim or headband, a wavy fringe above it, and a small open circle floating above like a pom-pom. A single curved line under the chin like a collar."
  - right: "The same oval face read upside down: eyes now near the top with drooping lines under them (eye-bags/cheeks), the double-arc under the blue bar reading as a nose/moustache, and the mouth drawn as a downturned line — a frowning, grimacing, grumpy expression. The blue bar now sits low at the chin like a beard band/collar, the wavy line beneath it reads as a beard, and the open circle hangs below like a button/ornament."
  - different?: "Two clearly DIFFERENT characters: an upright smiling hat-wearer vs. an inverted frowning bearded man — produced by the same drawing rotated 180°."
  - integration: "The two panels are separate renderings of the identical stroke set, one rotated; there is no second face overlaid inside a single panel and no duplicated piece — the hat/brim of the smile becomes the beard/collar of the frown."
  - verdict: "PASS — both orientations read as clear, distinct faces built from one shared set of strokes."

### img11: grok-imagine-2.0 (raster, plain prompt)

- **Cláudio:** FAIL. ""dois rostos separados em orientações opostas" (two separate faces in opposite orientations)"
- **Rubric (mine):** G1a=2, G1b=2, G1c=0, G2=2, G3=n/a; core 6/8 → **FAIL**. Two separate faces (young man with curls upright above, bearded man in bowler inverted below) joined at the collars. Rotating swaps which is upright; no shared strokes.
- **David at 0° (as delivered)** (`s386`; clarity 1, second-face 2, expression 2, quality 4/5):
  - saw: "A near mirror-symmetrical black-and-white engraving of a smiling young man with dense curly hair, built from hatching and stippling. The sharp dark collar below his chin looks odd at first, until the lower half resolves into a second face. It is a classic ambiguous-head figure."
  - faces: "Two. The upright young man occupying most of the picture, and an upside-down older man in the lower portion (bottom third), whose black top hat sits at the very bottom edge."
  - main face: "The upright young man: young, male, cheerful, broad open-toothed smile, looking straight ahead. Clean-shaven. Present: eyes with clear pupils and lids, dark brows, defined nose, open mouth with teeth, thick curly hair, dark pointed collar/clothes. Missing or odd: no ears, no neck or real shoulders; that pointed collar reads as a beak-like wedge until the illusion clicks."
- **David at 180° (rotated)** (`s129`; clarity 2, second-face 2, expression 2, quality 4/5):
  - saw: "A monochrome engraving-style drawing, dense hatching and stippling, built as a figure-ground illusion: an upright bearded man in a bowler hat on top, and below him, inverted, another face emerging from the same ink. My eye flips between the two readings and cannot hold both at once."
  - faces: "Two. Top half: upright face. Bottom half: a second face, upside-down, sharing the middle horizontal band with the first."
  - main face: "The upper upright one dominates. An older, stern-looking man in a dark bowler hat, thick wavy hair, heavy brows, deep-set intense eyes staring straight out, prominent nose, closed downturned mouth, and a full textured beard and moustache meeting a wide pointed dark collar. Expression: serious, stoic, faintly severe. Eyes, nose, mouth, brows, hair, hat and beard all clearly present; the lower jaw and neck are faint/ambiguous, absorbed into the inverted face below."
- **David on the pair** (`p664`): left 2, right 2, integration 2, contrast 2, joke 2, breaks rules: no.
  - left: "Upright, a beaming young woman — short dark curly hair, wide open eyes, broad open-mouthed smile with a row of teeth, white collar under a dark jacket with very wide pointed lapels. Below her, inverted, an old man with a full beard and mustache and a dark bowler hat at the bottom edge."
  - right: "Upright, a stern old man — heavy brows, deep-set staring eyes, prominent nose, thick mustache and full beard, dark bowler hat with rounded crown and brim, wide dark collar/lapels. Below him, inverted, the same smiling young face with curly hair and visible teeth."
  - different?: "Two clearly DIFFERENT characters: the young smiling woman and the stern bearded old man in a bowler hat. Since the right panel is the left rotated, each panel contains both — left leads with the girl, right leads with the old man."
  - integration: "shared strokes, not two pasted faces. The girl's chin/mouth band doubles as the old man's forehead/eye region, her neck and collar become his nose and mustache, her dark lapels become his hat brim, and the curly hair reads as his beard. One continuous engraved composite per panel, with no separate overlaid piece."
  - verdict: "PASS — both panels read as clear, sharply contrasting faces built from the same reused lines, which is exactly the reversible-face trick."

### img12: claude-sonnet-5.5-medium (SVG, prompt v5)

- **Cláudio:** PASS. "passed, and funny"
- **Rubric (mine):** G1a=2, G1b=2, G1c=2, G2=2, G3=2; core 8/8 → **PASS**. A: wide-eyed grin; B: sad frown. Hair = beard, red grin = hat band, red nose is the shared stroke that is a hat tag in A. Rocket and bow tie swap places. Funny.
- **David at 0° (as delivered)** (`s955`; clarity 2, second-face 2, expression 2, quality 4/5):
  - saw: "A flat vector cartoon of a wide-eyed man with black hair, black beard, red bow tie and a tiny teal rocket perched on his head. The white face area is dominated by two huge round eyes with horizontal lines and a broad red smile. Thin white highlight strokes inside the hair and beard are not just decoration — they read as extra faces when you stop looking at the middle."
  - faces: "Three readable faces, all same figure.
- Center: upright main face.
- Upper black hair: a second face, upright — two short white arcs as closed eyes, a long white arc as a smile.
- Lower black beard: a third face, upside-down — two white arcs as eyes with the red mouth line above them as its mouth."
  - main face: "One clear face — an adult male, cartoonish, bearded, with a hanging hair fringe and a red forehead mark; rocket as a hat, bow tie as clothing. Expression: cheerful, slightly cross-eyed grin. Present: eyes, brows, mouth, ears, hair, beard, cheeks. Missing/odd: no nose at all; eyes oversized with a hard horizontal bar instead of normal pupils."
- **David at 180° (rotated)** (`s609`; clarity 2, second-face 1, expression 2, quality 4/5):
  - saw: "A bold flat-vector portrait on cream: a stylized bearded man in an inverse-colour palette of black, red-orange, teal and white. The first impact is the heavy black beard and the big half-lidded eyes, which make it read as tired and melancholy. The symmetry and the frowning white line inside the beard hint at a deliberate ambiguous-figure trick."
  - faces: "One clear head, upright, centred in the frame. A second, upside-down head is only latent: the black beard mass plus its white curve could become hair and a smiling mouth if flipped, but in this orientation no separate eyes/nose resolve for it."
  - main face: "Yes — one clear face. An older-looking male character, cartoonish: black hair/cap with red headband, prominent red nose, full black beard, bow tie balanced on top, small tie/pendant at the chin. Expression: sad, worried, sleepy. Present: eyes (circular with pupils and heavy lids), brows (sloping down inward), nose, mouth as a pale frown line in the beard, hair/beard. Odd: the bow tie sits on the head, the "mouth" is the only white contour, and the tie hangs off the beard."
- **David on the pair** (`p897`): left 2, right 2, integration 2, contrast 2, joke 2, breaks rules: no.
  - left: "A cheerful young boy or space cadet in a bow tie — wide-eyed, smiling, rosy. Black hair with a white highlight, red inverted-triangle ornament at the hairline, small teal-and-red rocket on top of his head like a hat, red bow tie with teal knot and white collar points at his neck. Slightly anxious eyebrows but overall happy, alert expression."
  - right: "An older, glum man with a big red triangular nose, heavy black beard/moustache covering the lower face (pale line inside reads as a mouth), black hair or cap with a red headband/arc, and a red bow with teal center perched on top of his head; a small teal-and-red rocket hangs below his chin like a pendant. Worried, downturned expression."
  - different?: "Clearly two different characters — a smiling boy and a worried bearded man — from the same drawing upside down."
  - integration: "Genuinely shared strokes. The boy's rocket hat becomes the man's chin pendant; the boy's black chin/beard becomes the man's hair/cap; the red nose points down in one and up in the other; the bow tie migrates from neck to head; the collar lines read as hair-part marks. No separate or overlaid pieces."
  - verdict: "PASS — both panels read as clear, distinct faces (happy boy vs. worried bearded man) built entirely from the same shared strokes."

### img13: qwen-3.7-plus (SVG, prompt v5)

- **Cláudio:** FAIL. "strange, failed"
- **Rubric (mine):** G1a=1, G1b=1, G1c=1, G2=0, G3=0; core 3/8 → **FAIL**. Almost the same minimal face in both readings (no contrast); the SVG contains letter-shaped paths (M and W), which the contract forbids. Faces are barely faces.
- **David at 0° (as delivered)** (`s276`; clarity 2, second-face 2, expression 2, quality 3/5):
  - saw: "A single, wobbly black outline of a tall oval head on white, filled with simple line features — two round eyes with solid pupils, a small smile, and a chin arc. Above the head floats a small jagged "M" shape, and the forehead carries a tiny diamond plus a couple of small arcs. The whole thing reads as a hand-drawn doodle, very reduced, almost mask-like."
  - faces: "Two. (a) The large upright face occupying the whole oval — eyes, smile, chin. (b) A small upside-down face in the forehead area: the "M" above the head acts as its mouth, the diamond as its nose, and the small arcs as its eyes/brows, with the head's top edge as its skull."
  - main face: "One clear face — the upright one. It suggests a young, gender-neutral cartoon character, bald or with no hair/hat at all, no clothes, no beard. Expression: mild, pleasant, slightly blank smile. Clearly present: two eyes with pupils, brows, smile, chin. Missing or odd: no nose, no ears, no hair or hat, no neck detail — just a single base line."
- **David at 180° (rotated)** (`s911`; clarity 1, second-face 1, expression 1, quality 3/5):
  - saw: "A sparse black-line sketch of one long, pill-shaped head, floating on white, with a single gently curved line hovering above it and a capital "W" below. Inside sit stacked brow-wrinkle curves, two round eyes with dot pupils, a hooked nose line, a flat stitched mouth, and a small diamond chin mark. It reads as a doodle made to be ambiguous."
  - faces: "One upright face occupying the centre, elongated oval, right side up. The same lines, rotated 180°, would suggest a second, upside-down face (the "W" becoming an "M"), but no second face is visible when the sheet is seen as drawn."
  - main face: "One clear face — a long-headed older man, no hair or hat, hairline marked by curved lines, stitched/tight line mouth, small goatee-like diamond. Expression: weary, tight-lipped, mildly grim. Present: eyes, brows, eye-crease lines, nose, mouth, forehead lines. Missing/odd: no ears, no jaw shape, lips reduced to one line, cross-stroke through the mouth."
- **David on the pair** (`p366`): left 2, right 2, integration 2, contrast 2, joke 2, breaks rules: yes.
  - left: "A smiling bearded man/king — tall oval head, an "M"-shaped spiky crown with a diamond jewel beneath it, small eyes with brows and bags, a moustache/nose arc and a wide grin, with a beard/collar arc under the chin, plus a ground line below."
  - right: "RIGHT PANEL (upside down): A smoother, younger face, more woman/queen-like — two frown-arc brows at the top, same round eyes, a lens-shaped closed mouth, a diamond hanging like a pendant/chin jewel near the bottom, and the "W" reading as a collar or crown base; expression neutral, slightly piqued, no beard."
  - different?: "TWO DIFFERENT FACES — the same strokes read as an old bearded king upright and a bare-faced woman/queen inverted; not identical, both clearly faces."
  - integration: "Genuinely shared — the crown is the rotated collar/beard, the moustache-grin becomes brows, the chin arc becomes the hat line, the diamond moves from crown-jewel to pendant."
  - verdict: "PASS as a reversible face — both panels read as distinct, clear characters built from the identical strokes; the M/W letters are the only rule violation."

### img14: gpt-5.6-terra-low (SVG, prompt v5)

- **Cláudio:** PASS. "passed: it delivered both faces"
- **Rubric (mine):** G1a=2, G1b=2, G1c=2, G2=2, G3=2; core 8/8 → **PASS**. A: smiling face under a teal cap with a location-pin and chat-bubble badge, orange collar; B: scowling bearded man in an orange hat, a cracked-screen badge on the beard. Hat = beard, collar = hat; props differ between readings.
- **David at 0° (as delivered)** (`s575`; clarity 2, second-face 1, expression 2, quality 4/5):
  - saw: "A flat vector portrait of a round cream-colored head under a dark teal cap or helmet, on a solid light background. Thick navy outlines and just three colors give it a clean, friendly cartoon look. The face is wide-eyed and smiling."
  - faces: "One head is clearly recognisable, upright, filling the center of the picture. The bottom orange collar area, viewed inverted, hints at a second face (collar becoming a hat brim, smile becoming a frown), but it is only suggested, not clearly drawn."
  - main face: "One clear face — a young, stylized cartoon figure, probably male and childlike, wearing a teal cap with two orange patches (one with an X-and-bar symbol, one a tag with a white dot) and a single curl of hair on the forehead. Expression: gentle, wide-eyed smile. Clearly present: eyes with catchlights, brows, nose, smiling mouth, cap. Odd/absent: no real hair, no ears, no defined jaw or neck."
- **David at 180° (rotated)** (`s232`; clarity 2, second-face 0, expression 2, quality 4/5):
  - saw: "A flat-vector cartoon head against a cream background, drawn in only three colors — off-white, burnt orange and dark teal. The face is a long gourd-like oval, wrapped at the bottom by a jagged high collar. It reads instantly as a tired, stressed little official."
  - faces: "One distinct head, front-facing and upright, centered in the frame."
  - main face: "Yes, one clear face — a stylized cartoon adult of no definable age or gender, like a mascot or uniformed officer. He wears a wide flat-topped orange cap with a button and two white seam lines, plus a dark teal collared tunic with two orange patches. Expression is anxious and weary: heavy angled brows, wide white eyes with small pupils, under-eye bags, furrowed forehead with a squiggle. Eyes, nose, mouth, brows and hat are all present; hair, ears and neck are absent, and the mouth sits low, partly swallowed by the collar."
- **David on the pair** (`p275`): left 2, right 2, integration 2, contrast 2, joke 2, breaks rules: no.
  - left: "A cheerful, round-faced man smiling broadly. He wears a flat-topped teal military-style cap with two orange badges (a rectangle with an X, a circle with a dot) and a center loop; below is an orange collar piece with a teal button. Expression: friendly, content."
  - right: "A grumpy, scowling man with heavy furrowed brows and a down-turned mouth. On his head sits an orange cap with a teal button; a teal beard/chin-strap mass wraps his jaw, carrying the same orange circle and X rectangle. Expression: stern, angry."
  - different?: "Two clearly DIFFERENT faces — same drawing, flipped 180°, each orientation reading as its own distinct character (happy soldier vs. scowling man with beard)."
  - integration: "Genuinely shared strokes. Left's teal cap becomes right's teal beard; left's orange collar becomes right's orange hat; left's smile reads as right's angry brows; badges mirror. Nothing is stacked or duplicated as a separate piece."
  - verdict: "PASS — both orientations read as clear, distinct faces built entirely from the same strokes, with opposite expressions and props."

### img15: nemotron-3.5-lightning (SVG, prompt v5)

- **Cláudio:** PASS. "passed, although it simplified to the extreme"
- **Rubric (mine):** G1a=2, G1b=2, G1c=1, G2=1, G3=1; core 6/8 → **PASS**. Extremely reduced: a triangle (head) with two shared eyes, one brow arc and one mouth arc. A: a smiley (hat = the triangle point); B: a flat-mouthed face under an arc. Both read as faces, only just; contrast is slight and there is no real prop. A tiny leftover rectangle.
- **David at 0° (as delivered)** (`s707`; clarity 2, second-face 0, expression 2, quality 3/5):
  - saw: "A large, thin black-outlined upright triangle sits centered on plain white, with a very simple cartoon face drawn inside it. The face is comprised of a single curved brow line, two small hollow circle eyes, and a shallow upward smile. Just under the apex is a tiny hollow rectangle, giving the whole thing the feel of a beginner drawing exercise."
  - faces: "One. Centered in the picture, upright."
  - main face: "There is one clear face, though extremely abstract — no person type is readable: no age, gender, hair, beard, or clothing. It reads as a generic, friendly cartoon character, possibly a smiling head or mask. The expression is cheerful/pleasant. Clearly present: eyes (hollow circles), mouth (smile), brow (single line). Missing or odd: no nose, no pupils, no hair or hat, and the face floats inside a geometric outline rather than a head shape."
- **David at 180° (rotated)** (`s212`; clarity 2, second-face 0, expression 1, quality 3/5):
  - saw: "A single thin black outline of an inverted triangle on white, with a sparse face assembled inside it. The dominant impression is that the container is upside-down while the features read as an upright face. Minimal, roughly hand-drawn, no shading."
  - faces: "One recognizable face, centered in the upper-middle of the triangle, upright. The downward-pointing triangle around it is not itself a face, though rotating the whole image 180° flips the read into a frowning, distorted upside-down face."
  - main face: "One clear face, generically neutral-cute, no age or gender markers — an abstract person or doodle character. Expression: gentle, mild smile, slightly blank. Clearly present: two hollow circle eyes, a curved smiling mouth, and one arc above the eyes (reads as brow or closed second eye). Odd: that top arc is a single line spanning the width, not two brows; no nose; no hair, hat, or clothing; the shape has no head outline beyond the triangle."
- **David on the pair** (`p595`): left 2, right 2, integration 2, contrast 2, joke 1, breaks rules: no.
  - left: "A simple smiling face inside an upright isosceles triangle — two dot-circle eyes, one arched brow, a clear U-curve smile. At the top apex sits a tiny outlined square, reading as a small flat/party hat perched on the pointed head. Cheerful, friendly."
  - right: "The same strokes in a downward-pointing triangle. The curved line now sits low and reads as a flat/slightly downturned mouth; the eyes and brow stay above it. Overall a neutral-to-sad, glum face with a pointed chin/beard, and the tiny square at the bottom vertex reads as a tie or a beard tip/beard ornament."
  - different?: "Same face upside down — one drawing producing two opposite readings (happy vs. glum). Both panels clearly read as faces; neither is a non-face."
  - integration: "The strokes are identical — literally the same drawing rotated, so every mark serves both readings one-to-one (the apex hat becomes the beard/tip accessory; the smile becomes the frown). They are presented as two side-by-side copies of one drawing, but there is no separate second face pasted inside either panel."
  - verdict: "PASS — both orientations read as clear, distinctly different characters (happy vs. sad) built from exactly the same strokes."

## 6. Agreement

Cláudio's verdicts: 7 PASS (Claude, Gemini, ChatGPT, Muse, GLM, GPT 5.6 Terra, Nemotron 3.5 Lightning) and 8 FAIL (4 image generators + Qwen 3.7 Plus, DeepSeek, Manus, Qwen3.8 Omni Flash).

| Judge | Agrees with Cláudio | Rate | False PASS (Cláudio FAIL) | False FAIL (Cláudio PASS) |
|---|---|---|---|---|
| Rubric, Peter (not blind to Cláudio's verdicts) | 15/15 | 100% | 0: - | 0: - |
| David, stage 2 own verdict (both panels) | 9/15 | 60% | 6: img01 nanobanana-2.1, img03 deepseek-v4.1, img05 manus-2.0-lite, img09 chatgpt-images-2.5, img11 grok-imagine-2.0, img13 qwen-3.7-plus | 0: - |
| David, stage 2 numbers run through my verdict rule | 8/15 | 53% | 7: img01 nanobanana-2.1, img03 deepseek-v4.1, img04 qwen3.8-omni-flash, img05 manus-2.0-lite, img07 qwen-image-3.0, img09 chatgpt-images-2.5, img11 grok-imagine-2.0 | 0: - |
| David, stage 1 only (both clarity=2, no clearly visible second face in either orientation) | 11/15 | 73% | 2: img03 deepseek-v4.1, img05 manus-2.0-lite | 2: img08 glm-5.3-max, img12 claude-sonnet-5.5-medium |

Item-level agreement between David and my rubric scores (exact match of the 0-2 values): face clarity at 0° vs G1a 13/15; at 180° vs G1b 11/15; stage 2 left panel vs G1a 13/15; right panel vs G1b 9/15; CONTRAST vs G2 9/15; INTEGRATION (>0 vs >0) vs G1c 11/15.

**Caveat on the rubric row:** I scored all 15 images knowing Cláudio's verdicts (the assistant had them in context), so the 15/15 is not an independent check; it shows the rubric can be set up to reproduce his verdicts, not that it predicts them. David is the only blind judge here.

## 7. Notable divergences

**David says PASS, Cláudio says FAIL (6 of 8 Cláudio FAILs were passed by David in stage 2):**
- **img01 Nano Banana:** at 0° David saw one clear lady and no second face (agrees with Cláudio's "one head"); the rotated single image was read as "an upright older man plus an upside-down face". In the side-by-side stage 2 he described the right panel as a grim bearded old man and gave INTEGRATION 2. In the actual image the large face in the rotated reading is still the lady, upside down, and the old man is the tiny head in the ruff. This looks like the vision model describing the *expected* reversible-image reading rather than what is drawn (see the pre-description of call `p932` in [`david-evals/vision-describer-excerpts.md`](david-evals/vision-describer-excerpts.md): it explains the "illusion" feature by feature).
- **img03 DeepSeek, img05 Manus:** Cláudio could not identify the rotated face (DeepSeek) or found the second face unclear (Manus). David reads a face at 180° in both (eyes, brows, beard, bow tie/hat as accessories) and gives clarity 2. His bar for "a face" is lower than Cláudio's: eyes plus brows on an oval are enough. He did notice the leftover strokes (second-face score 1 in both orientations of img03 and img05), but did not count them against the pass.
- **img09 ChatGPT Images, img11 Grok Imagine:** in stage 1 David correctly saw two faces in each orientation (second-face score 2) and rated the 0° of img11 as weak (clarity 1). In stage 2 he nevertheless passed both with INTEGRATION 2, i.e. the two-heads-joined-at-the-collar design was accepted as "shared strokes". Stage 1 alone (D-solo) fails both, in line with Cláudio.
- **img13 Qwen 3.7 Plus:** Cláudio: strange, failed. David passed it on the two-panel view but did flag BREAKS_RULES = yes (letters "M" and "W"); the rule-based reading of his numbers therefore fails it. At 0° he also read a "second, upside-down face in the forehead" built from the M, a diamond and arcs, and at 180° he gave clarity 1.

**David says FAIL (stage 1 only) where Cláudio says PASS:** img08 GLM and img12 Claude. In both, David saw extra faces hidden inside the same figure (img12: "three readable faces" at 0° from the white highlight arcs in hair and beard; img08: second face 2 at 180°). This is the "B visible upright" ghosting failure from the prompt's failure table, and for img12 it is a real, if faint, leftover reading; Cláudio did not penalise it (he found the piece funny). Stage 2 passes both.

**Agreement on FAIL:** img04 Omni Flash (David: weaker 180°, clarity 1, contrast 1, verdict FAIL, matching "no face rotated") and img07 Qwen Image (two stacked faces; clarity 1 in both orientations, second face 2 in both; verdict FAIL).

**Misperceptions that matter for reading his answers:** for img07 David said the old man is "upside-down relative to the lady" at 0°; in the image both faces are upright at 0° and both inverted at 180°. At 180° he described an older woman above a younger woman. So his notion of which way up a face is can be wrong, which is exactly the thing this benchmark depends on.

## 8. Summary statistics (15 images; 7 Cláudio PASS, 8 FAIL)

- **Rubric (mine):** 15/15 agree with Cláudio, but see the caveat above (not blind).
- **David, own stage 2 verdict:** 9/15 = 60%. He catches all 7 PASS (recall 100%) and 2 of 8 FAILs; 6 false PASSes, no false FAILs. He is a lenient judge when shown the two panels together.
- **David, stage 2 numbers through my verdict rule:** 8/15 = 53% (his numeric scores are more generous than his verdict: img04 and img07 get INTEGRATION 2/1 and CONTRAST 1/2 yet FAIL).
- **David, stage 1 only (per-orientation, independent sessions):** 11/15 = 73%. The independent single-orientation view is the better predictor of Cláudio's verdicts: the two stacked/segregated image-generator failures are caught (second face 2), but it flags img08 and img12 (false FAIL) and misses img03 and img05 (false PASS).
- **Per-item agreement with my 0-2 scores:** 13/15 for clarity at 0°, 11/15 at 180° (the rotated reading is harder for him and for the vision model), 9/15 for contrast, 11/15 for integration (>0 vs 0).
- **Face clarity he assigns:** at 0° he scores 13 of 15 images as a clear face (2); the exceptions are img07 and img11 (both image-generator stacked designs). At 180° the exceptions are img04, img07, img13 (weak or failed rotated reading, matching Cláudio's FAIL for img04 and img13).
- **Where his perception matches the designer's intent:** img02 (smiling man with a rocket hat → stern bearded man), img12 (cheerful wide-eyed grin → tired, sad, bearded face), img14 (smile under a cap → scowling bearded man), img06 (smirk → sad frown). These are the cases where the stage-1 descriptions at 0° and 180° differ in the intended way, without David having seen the other orientation.
- **Mean of his OVERALL_FACE_QUALITY (0-5):** Cláudio PASS group 3.7 at 0° and 3.7 at 180°; Cláudio FAIL group 4.0 at 0° and 3.6 at 180°. At 0° it does not separate the groups (the FAIL group is even rated slightly higher); only the rotated reading differs slightly.

## 9. Reading the evidence: limits

1. **David is not looking at pixels.** His model is text-only; an auxiliary vision model describes each image and David reasons over that text (and over the answer of his own `vision_analyze` call, whose question he writes himself). Some "perceptions" are the vision model recognising a genre ("a classic ambiguous figure") and filling in the expected second reading. Stage 2 is especially exposed because the image was announced as "the same drawing upside down"; the pre-description of img01 (call `p932` in [`david-evals/vision-describer-excerpts.md`](david-evals/vision-describer-excerpts.md)) shows it inventing an old man in the rotated panel.
2. The two-stage design: stage 1 is independent per orientation; stage 2 is not blind to the rotation relation.
3. One call per cell, no repeats, no temperature control; judgments of one model with a persona, one prompt wording each.
4. The rubric scores are mine, made with knowledge of Cláudio's verdicts; the 0-2 scale and the verdict rule are my operationalisation of prompt v5 section 7, not an official rubric of the repository (the repository says "no rubric").
5. Image generators were given a different (plain) prompt from the SVG models, so G3 is not comparable and "pass" for them means passing Gates 1-2 only.
6. The 15 images have the same names/files as in `baselines/`; the rasters are not square, which could hint to David that those are not SVG-style drawings (he was never told the origin).

## 10. Cost and files

- David (Hermes, `deepseek/deepseek-v4.1-flash-1017` through OpenRouter, auxiliary vision calls included): 45 judged calls + 1 pilot call. Hermes' own estimate for David's main-model sessions: about US$0.065. Hermes `insights` total estimate for the day rose from about US$0.25 to US$0.81 over this work (about US$0.56 including the auxiliary vision calls, which the log reports as running on a paid lane); treat the second number as the upper bound.
- Files: see [`david-evals/README.md`](david-evals/README.md).
