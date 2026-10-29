# David's raw answers, verbatim

One block per call (45 calls: 15 images x 0°, 180°, side-by-side pair). The labels (image id, model, orientation) were added after the fact; David saw only an anonymous file name. See [`../README.md`](../README.md) for the caveats (text-only judge with an auxiliary vision describer, stage 2 not fully blind to the rotation, one call per cell).


## img01 (nanobanana-2.1), 0deg, call code s918

```
1. WHAT I SEE: An ornate vintage engraving-style portrait framed by filigree corners and hatched borders. A woman with a calm, faint smile looks straight at the viewer, her face stippled and cross-hatched. Enormous sculpted curls frame her head, topped by a small bonnet-like fascinator, with a heavy ruffled collar and bow below.

2. FACES: One clear human face/head, centred in the frame, upright (en face). No other recognisable head, upright or inverted.

3. MAIN FACE: Yes, one clear face. A young-to-middle-aged woman, serene and slightly enigmatic, faint closed-mouth smile. Clearly present: eyes with defined irises and lashes, arched brows, straight nose with nostrils, full lips, abundant curly hair, small hat with ribbon and leaves, high frilled collar with bow. Slight oddity: pupils uneven, hat ornaments nonsensical, collar melts into leaf-like hair strands.

4. EXTRA: No text or letters. The heavy curling hair and left-side shading can trigger pareidolia (a vague profile-like shape), but nothing deliberate. No props beyond the hat and bow; the head appears semi-disembodied at the bottom edge.

5. SCORES:
FACE_CLARITY: 2
SECOND_FACE_VISIBLE: 0
EXPRESSION_CLARITY: 2
OVERALL_FACE_QUALITY: 4
```

## img01 (nanobanana-2.1), 180deg, call code s358

```
1. WHAT I SEE: A sepia-toned, engraving-style line drawing inside a double-ruled frame with scrollwork corners and hatched vignette shading. The centre is a mass of swirling, curling hair that resolves into a face staring straight out. Fine cross-hatching does all the modelling, giving it an antique, slightly unsettling quality.

2. FACES: Two large heads share the composition — an upright older man occupying the upper half, and an upside-down face in the lower half formed from the same features (its forehead is the upright man's chin, its hairline is his mouth line). A third, tiny tilted mask-like face sits at the very bottom, tangled in the curls.

3. MAIN FACE: Yes, one dominant face: an elderly, stern-looking man, likely male, no hat. Thick wavy hair parted centrally, heavy drooping eyelids, bags under the eyes, furrowed brow, prominent straight nose, downturned thin mouth. Expression: weary, severe, brooding. Eyes, nose, brows and hair are strong; the mouth is only implied (a shared contour), and the chin/jaw is soft and merges into the inverted head.

4. EXTRA: The inverted face is unmistakable — wide, startled eyes and a small nose. The small bottom face reads as an ornament or jester's mask. No text or letters; decorative scrollwork acts as the only prop-like element.

5. SCORES:
FACE_CLARITY: 2
SECOND_FACE_VISIBLE: 2
EXPRESSION_CLARITY: 2
OVERALL_FACE_QUALITY: 4
```

## img01 (nanobanana-2.1), pair, call code p932

```
1. LEFT PANEL: A young woman, upright, frontal. Large wide eyes, arched brows, small nose, gentle closed-mouth smile; soft rounded cheeks. Ornate curled/ringleted dark hair falling to the shoulders, a small tilted hat with leaves/ribbon on top, and a high ruffled collar closed by a large bow. Expression: sweet, mild, slightly coy.

2. RIGHT PANEL: The same figure inverted. Read upright it is an older man: heavy furrowed brow, deep-set eyes, long prominent nose, thick drooping mustache, and a broad wavy beard/sideburns formed by the curls; a dark cap-like shape (the bow and collar) sits at the bottom. Expression: stern, severe, scowling — almost glaring.

3. Clearly DIFFERENT characters — a young smiling woman vs a grim bearded old man. Two faces, not one face upside down. Both panels read as faces.

4. INTEGRATION: Genuinely shared strokes, not two stacked drawings. The same contour lines do double duty: the woman's forehead/chin becomes the man's chin/brow, her nose becomes his mouth area, her eye-shading becomes his eye-sockets, her curls become his beard and hair, her bow/collar becomes his headgear. No second, separately drawn face is pasted into either panel.

5. SCORES
LEFT_READS_AS_FACE: 2
RIGHT_READS_AS_FACE: 2
INTEGRATION: 2
CONTRAST: 2
PROPS_AND_JOKE: 2 — the joke is the double image of youth/beauty against old age and severity (the wife / mother-in-law figure-ground trick).
BREAKS_RULES: no

6. VERDICT: PASS — both orientations resolve into clear, strongly contrasting characters built from one set of shared engraved strokes, with no text or foreign elements.
```

## img02 (chatgpt-medium), 0deg, call code s433

```
1. WHAT I SEE: A flat-vector head-and-shoulders portrait on plain beige, drawn with heavy black outlines and a beige/teal/red palette. A broad-jawed adult with black widow's-peak hair and a teal scoop-neck shirt looks straight out. The first thing that strikes me is the small red-and-white rocket-like object standing upright on the crown of the head.

2. FACES: One clear human face/head, centered, upright. No second human face — the only other "face-like" thing is a single white circle with a black dot on the topknot, which is a porthole/eye motif, not a face.

3. MAIN FACE: Yes, one clear face. Adult, androgynous, slightly masculine, no hat, thick black hair with a sharp widow's peak and thin white highlight strokes, teal shirt with two white downward chevrons. Expression calm, eyes wide and forward, slight closed-mouth smile — mildly blank but readable. Present: both eyes with pupils and highlights, brows, hooked line nose, mouth, ears, hair. Odd: a vertical black line with a short crossbar runs down the forehead from the hairline like a stylized symbol; straight horizontal lines sit under each eye.

4. EXTRA: The candle/rocket topknot with red body, white circle-and-dot, black tip; a red curve near the hair and a red lower-lip line; small teal marks inside the ears. No text or letters.

5. SCORES:
FACE_CLARITY: 2
SECOND_FACE_VISIBLE: 0
EXPRESSION_CLARITY: 2
OVERALL_FACE_QUALITY: 4
```

## img02 (chatgpt-medium), 180deg, call code s302

```
1. WHAT I SEE: A flat, vector-style bust of a bald, bearded man in thick black outlines on cream. The face is built almost entirely from the beard, brows and heavy dark eyes. It reads immediately as a stern cartoon portrait, and the shapes look deliberately ambiguous — a topsy-turvy type design.

2. FACES: One unmistakable upright head, centred. A second, upside-down head appears only if the picture is mentally inverted (the beard becomes headwear, the chin ornament becomes a crown jewel) — that one is faint/inferred, not plainly visible in the given orientation.

3. MAIN FACE: One clear face: a middle-aged to older male character, bald, huge bushy black beard and moustache, tiny teal trapezoid cap with two white chevrons at the very top. Expression: stern, scowling, slightly cross-eyed stare from the heavy angled brows. Present and clear: eyes, brows, hat, beard, ears, forehead crease. Odd/missing: nose is a single line ending in a small V, mouth is almost fully buried (only a small red curve), under-eye bags double as chevron accents, and the small red diamond-and-squiggle ornament hangs below the beard like a pendant or tie.

4. EXTRA: No text or letters. The chin pendant is the one prop-like symbol; the beard's interior white and teal hooks are the element that could form a second face's features.

5. SCORES:
FACE_CLARITY: 2
SECOND_FACE_VISIBLE: 1
EXPRESSION_CLARITY: 2
OVERALL_FACE_QUALITY: 4
```

## img02 (chatgpt-medium), pair, call code p295

```
1. LEFT PANEL: Young man, calm and mildly friendly, slight closed-mouth smile. Black bowl-cut hair with wavy texture lines, small red finial/topknot at the crown, arched brows, almond eyes, small hooked nose, teal V-collar with two white chevrons.

2. RIGHT PANEL: Old, stern bearded man. The bowl cut now reads as a full black beard and moustache, the teal collar as a green flat cap with the same two chevrons, the topknot as a small dangling ornament under the chin. Same eyes but heavier, hooked line now points up as a forehead crease, mouth line reads as a grimace. Expression: older, grumpy.

3. Two clearly DIFFERENT faces — same drawing rotated 180°, and both readings are legible.

4. INTEGRATION: Genuinely shared strokes, not two stacked drawings. The hair of the young man is the beard of the old man, the collar is the cap, the topknot is the chin ornament, the nose line becomes the forehead crease. No second separate face piece appears anywhere in either panel.

5. SCORES:
LEFT_READS_AS_FACE 2
RIGHT_READS_AS_FACE 2
INTEGRATION 2
CONTRAST 2
PROPS_AND_JOKE 2 — "the same strokes flip a fresh-faced youth into a bearded elder: hair becomes beard, collar becomes cap"
BREAKS_RULES no — no letters or text; the mark read as a "7" on the old man's forehead is part of the line drawing, not typography.

6. VERDICT: PASS — both panels resolve into clear, distinct characters (young man / bearded old man) built entirely from the same shared contours, which is exactly what a reversible face requires.
```

## img03 (deepseek-v4.1), 0deg, call code s346

```
1. WHAT I SEE: A flat, cream-background vector portrait: an egg-shaped head in thick black outline, a solid black beanie with a white rocket glyph, arched brows, almond eyes with dot pupils, a U-shaped nose, a faint smile, a straight chin line, and a rust-red bowtie at the neck. Clean, symmetrical, almost logo-like. Almost nothing is shaded; it lives on outlines and negative space.

2. FACES: One upright face, centred, filling most of the frame. A second head is strongly implied upside-down at the bottom (the bowtie reading as a red cap, the chin line as a forehead, the mouth as heavy brows), but it only resolves if you mentally flip the image.

3. MAIN FACE: One clear face — a young, androgynous, cartoonish character, plausible astronaut/space cadet given the rocket patch. No hair, ears, or clothing beyond the bowtie. Expression is calm and faintly amused. Eyes, brows, nose, mouth, chin and hat are all present; the horizontal cheek lines and under-eye hooks are odd, anatomically arbitrary strokes.

4. EXTRA: The upside-down face is the intended illusion; the rocket emblem is a prop/symbol. No text or letters. No stray marks.

5. SCORES:
FACE_CLARITY: 2
SECOND_FACE_VISIBLE: 1
EXPRESSION_CLARITY: 2
OVERALL_FACE_QUALITY: 4
```

## img03 (deepseek-v4.1), 180deg, call code s297

```
1. WHAT I SEE: A minimal flat-vector portrait on cream: an egg-shaped head with thick black outline, arched brows, almond eyes with catchlights, and a solid black beard filling the lower half. A terracotta bow tie floats above, tethered by two thin lines; a small white emblem sits inside the beard. It reads as a whimsical, stylised "portrait badge."

2. FACES: One clear human head, centred and upright, filling the frame. A second, much smaller face-like shape is suggested inside the white emblem on the beard (upright but abstract).

3. MAIN FACE: An adult male, seemingly older (forehead crease lines, slight bald crown), wearing a bow tie; heavily bearded. Expression is neutral, calm, faintly bemused. Clearly present: eyes, brows, beard, hairline/crown lines, cheek contours, bow tie. Missing or odd: no nose at all, no ears, mouth reduced to a thin white smile line, no visible neck or shoulders.

4. EXTRA: The white shield/teardrop emblem on the beard contains a horizontal bar and a dot-in-circle, giving a faint pareidolic mini-face. No text or letters.

5. SCORES:
FACE_CLARITY: 2
SECOND_FACE_VISIBLE: 1
EXPRESSION_CLARITY: 1
OVERALL_FACE_QUALITY: 3
```

## img03 (deepseek-v4.1), pair, call code p619

```
1. LEFT PANEL: A stern, straight-faced man — long oval head, flat black skullcap with a small white crest/rocket emblem, arched brows, almond eyes, a U-shaped nose, a flat closed mouth, thin neck and a terracotta bow tie. Neutral/serious expression.

2. RIGHT PANEL: A bald, cheerful older man with a big solid black beard filling the lower half of the head, a wide smiling mouth, wrinkles above the brows, and a terracotta bow perched on top of his head (like a hair bow), with two little lines rising from it. Goofy, amused expression.

3. Clearly DIFFERENT faces — a grim capped gentleman versus a jolly bald bearded man — produced by the same drawing turned 180°.

4. INTEGRATION: Genuinely shared strokes. The black cap is the black beard; the bow tie at the neck becomes the bow on the head; the neck lines become strands above the head; the chin/jaw line becomes the hairline; the nose and mouth become brow furrows and a wide grin. Nothing is stacked or overlaid — every element does double duty.

5. SCORES
LEFT_READS_AS_FACE: 2
RIGHT_READS_AS_FACE: 2
INTEGRATION: 2
CONTRAST: 2
PROPS_AND_JOKE: 2 — the joke: the dignified fellow with his bow tie at the throat becomes a grinning bald man wearing that same bow on top of his head and a beard where his cap was.
BREAKS_RULES: no

6. VERDICT: PASS — both orientations read instantly as clear, distinctly different characters, and the transformation comes entirely from rereading shared strokes.
```

## img04 (qwen3.8-omni-flash), 0deg, call code s942

```
1. WHAT I SEE: A bold, thick-line cartoon drawing centered on white: a smiling figure in a tall pointed hat and a wide bowl-shaped collar. The hat's emblem is abstract. The only color in the whole picture is a small red circle acting as a clasp or button on the collar.

2. FACES: One. It sits center-frame and is upright, facing the viewer frontally. No inverted or secondary head is recognisable.

3. MAIN FACE: Yes, one clear face. A stylized, ageless, gender-neutral character — reminiscent of a jester, bishop or playing-card figure. Expression: calm, gently smiling, friendly and slightly blank. Present: brows (arched), eyes (circles with solid pupils), nose (long line with a hook), mouth (single upward curve), tall pointed hat with a band and circular emblem. Missing/odd: no hair, no ears, no defined neck; the nose hook is oddly angular and the chin tapers very sharply.

4. EXTRA: The red circle with black outline on the collar is the only color and reads as a button/clasp. The hat emblem (circle with crossing strokes and a small curved tail) is a symbol, not a face. The collar's two concentric arcs could faintly suggest a closed mouth or a bowl, but no genuine second face. No text or letters anywhere.

5. SCORES:
FACE_CLARITY: 2
SECOND_FACE_VISIBLE: 0
EXPRESSION_CLARITY: 2
OVERALL_FACE_QUALITY: 4
```

## img04 (qwen3.8-omni-flash), 180deg, call code s217

```
1. WHAT I SEE: A tall, egg-shaped cartoon head drawn in thick black lines on white, topped by a dome-like hat with a single bright red dot. Round eyes with dot pupils, a hooked vertical nose line, and a wide curved smile dominate the middle. The bottom tapers to a sharp point containing a small circle with an X/cross inside.

2. FACES: Two readable faces. The main one sits upright in the upper/central oval. A second, upside-down face occupies the tapered lower section, with the dividing horizontal line acting as its mouth and the circled X as its eye/eye-patch.

3. MAIN FACE: Yes, one clear face: a simple, ageless cartoon figure, gender-neutral, wearing a domed cap with a red button/pompom. Expression is cheerful and slightly goofy, smiling broadly. Eyes, nose, mouth and hat are clearly present; brows are only suggested by a faint curved line, and there is no hair, ears, beard or clothing.

4. EXTRA: The lower circle-with-X plus the short curved stroke reads as a second upside-down face (monocle-like eye, straight mouth). The red dot is the only color and functions as a hat ornament. No text or letters anywhere.

5. SCORES:
FACE_CLARITY: 1
SECOND_FACE_VISIBLE: 1
EXPRESSION_CLARITY: 2
OVERALL_FACE_QUALITY: 3
```

## img04 (qwen3.8-omni-flash), pair, call code p955

```
1. LEFT PANEL: A stylized, cartoonish human face — elongated oval head, round dot-pupil eyes with arched brows, a hooked nose, and an upward-curving smile (friendly/cheerful). Topped by a pointed mitre-like hat containing a circle with an X/cross and a small hook mark; below the chin a bowl-shaped collar crossed by a horizontal line, with a solid red dot at its base.

2. RIGHT PANEL: The same drawn face, now inverted: oval head, dot-pupil eyes, curved nose, and curved mouth lines. Above it, a rounded brim/dome carrying a horizontal line and the red dot at the very top (reads as a wide-brimmed hat with a red button/pompom); below it a downward-pointing triangle with the circle-and-X emblem (reads as a pointed collar, pendant, or small beard).

3. Same face upside down — the two readings are the same smiling character in different headgear; not two clearly different characters, and neither panel is a non-face.

4. INTEGRATION: Genuinely shared strokes. The mitre and its emblem become the pointed collar/pendant, the collar becomes the hat brim, and the red dot migrates from collar to hat top. Nothing is stacked or overlaid.

5. SCORES
   LEFT_READS_AS_FACE: 2
   RIGHT_READS_AS_FACE: 2
   INTEGRATION: 2
   CONTRAST: 1
   PROPS_AND_JOKE: 1 — props swap (mitre/collar → hat/beard) but no clear joke or message.
   BREAKS_RULES: no

6. VERDICT: FAIL — the rotation is technically clean and the shared strokes are real, but both panels resolve to essentially the same cheerful face with only a headgear swap, so there is no clearly different second character or contrasting expression.
```

## img05 (manus-2.0-lite), 0deg, call code s399

```
1. WHAT I SEE: A flat vector head-and-shoulders portrait on a cream background: peach skin, thick dark outlines, teal collar with white trim and a red diamond. The most striking thing is the very large dark hair mass with small white and teal marks that hint at a pattern above the forehead.

2. FACES: One unambiguous upright human head, centered/lower-middle. The hair above it contains marks that faintly suggest a second, upside-down face, but this is not clearly readable.

3. MAIN FACE: Yes, one clear face — a young, neutral-gender cartoon character with short dark bowl-cut hair, rounded ears, thick arched brows, almond eyes with white highlights, an L-shaped terracotta nose, and a closed gentle smile. Visible: eyes, brows, nose, mouth, ears, hair, teal shirt with collar and diamond emblem. Nothing important is missing; features are simple but consistent. Slight under-eye creases give a calm, friendly, faintly amused look.

4. EXTRA: A small red rectangular clip/knob at the top of the hair, a white curved patch below it, two short white curves, and three teal arcs on the right of the hair. These could be read as closed eyes and a mouth of an inverted face plus hair highlights, but they are sparse and asymmetric — likely decorative marks rather than a deliberate second face. No text.

5. SCORES:
FACE_CLARITY: 2
SECOND_FACE_VISIBLE: 1
EXPRESSION_CLARITY: 2
OVERALL_FACE_QUALITY: 4
```

## img05 (manus-2.0-lite), 180deg, call code s587

```
1. WHAT I SEE: A flat, vector-style head on beige — bald, bearded man wearing a teal pillbox-style cap with a small red diamond emblem on top. Thick charcoal outlines, heavy brows, almond eyes with bags, small tooth-like mouth sunk in a big black beard, plus a reddish "7"-shaped mark on the forehead and a red tab under the chin.

2. FACES: One clear head, centered and upright (the bearded man). A faint secondary face reading is arguable in the upper half only if you deliberately re-map the brows/eyes as a face, but it is not a distinct, self-contained second face.

3. MAIN FACE: Yes, one clear face: a middle-aged to older man, bald with a full dark beard, in a flat teal cap. Expression is stern, tired, faintly grumpy. All features are present — eyes, thick brows, hint of nose, small rectangular mouth, ears, hat, beard — the nose is nearly absent, implied only by the mustache edge, and the forehead mark is odd.

4. EXTRA: The red "7" scar/mark on the forehead and the red rectangle at the beard's base are odd accents; three teal curl lines on the left beard read as stray texture. No text.

5. SCORES:
FACE_CLARITY: 2
SECOND_FACE_VISIBLE: 1
EXPRESSION_CLARITY: 2
OVERALL_FACE_QUALITY: 4
```

## img05 (manus-2.0-lite), pair, call code p497

```
1. LEFT PANEL: Young, round-faced man (East Asian official/scholar type), calm gentle smile, arched brows, open friendly eyes. Solid black hair with widow's peak, small red tab at crown, white/teal cloud emblem on the forehead, three teal shine lines on the hair; teal collar with white trim and a red diamond at the throat.

2. RIGHT PANEL: Same silhouette read as an older, stern bearded elder — heavy-lidded eyes, frowning down-angled brows, eyesore lines, a reddish-brown hook/"7" mark and wrinkle on the bald forehead. Teal flat-topped cap with white trim and a red diamond; large black mustache-and-beard covering the whole lower face, containing the same white/teal emblem, three teal lines on the beard's left side, and a small red tab at the beard's bottom tip.

3. Two clearly DIFFERENT characters — a young slight-figure with a collar versus an old bearded figure in a cap — produced by the same drawing flipped 180°, not two unrelated faces.

4. INTEGRATION: genuinely shared strokes. Every element swaps roles: hair becomes beard, collar becomes cap, the forehead emblem becomes the beard's mouth-ornament, the three hair-shine lines become beard shine, and the two red diamonds are the same mark relocated.

5. SCORES
LEFT_READS_AS_FACE: 2
RIGHT_READS_AS_FACE: 2
INTEGRATION: 2
CONTRAST: 2
PROPS_AND_JOKE: 2 — the joke: flip the serene youth and his collar becomes the stern elder's cap and beard.
BREAKS_RULES: no (the "7" is a graphic forehead mark, not text)

6. VERDICT: PASS — both orientations read as clear, distinct faces whose every accessory is re-parsed from the identical strokes of one drawing.
```

## img06 (gemini-3.1-pro), 0deg, call code s671

```
1. WHAT I SEE: A flat, cartoonish head with pale peach skin, bold black outlines, a solid black flat-top hair mass, and a black beard across the lower jaw. A small star-tipped rocket sits centered on top of the head. Thin white "pop" lines curve above the hair and below the beard on a plain beige background.

2. FACES: Two. One upright in the center (beard at bottom, hair at top). One upside-down in the same central figure — the beard reads as hair, the white gap as a wide toothy grin, and the rocket hangs below as a pendant.

3. MAIN FACE: Yes, one clear face: a bearded adult man, gender masculine, no visible age cues, wearing no hat (flat-top black hair). Expression is mild, calm, faintly amused with a small closed smile and eyes glancing to the side. Present clearly: eyes with pupils and catchlights, angular nose, small mouth, eyebrows, ears, hair, beard. Odd: the mouth sits very close to the beard with a white gap that reads like teeth.

4. EXTRA: A second upright face barely visible — the inverted man. Prop/symbol: the star-topped striped rocket with fins and red flame. No text or letters.

5. SCORES:
FACE_CLARITY: 2
SECOND_FACE_VISIBLE: 1
EXPRESSION_CLARITY: 2
OVERALL_FACE_QUALITY: 4
```

## img06 (gemini-3.1-pro), 180deg, call code s726

```
1. WHAT I SEE: A flat vector cartoon head of a stern, bearded man against plain cream, drawn in bold black outlines. The single most striking thing: a tiny striped rocket with a red nose cone and a yellow star exhaust pokes downward out of his beard where a mouth should be. The style is minimalist and slightly surreal.

2. FACES: One recognizable human head, centered and upright, facing forward.

3. MAIN FACE: One clear face — a middle-aged adult male, cartoonish and grumpy; short flat-top black hair, large solid black beard covering jaw and chin, simple ears. Expression is angry/stern: heavy brows angled down toward a forehead crease, round white eyes with small inward-set pupils, under-eye creases. Eyes, brows, hair, beard, ears, nose line all present. Missing: no visible mouth at all — the rocket occupies that spot, which is odd.

4. EXTRA: The rocket in the beard (red triangular tip, white striped body, yellow five-pointed star below) is the main confusing/whimsical prop. Thin white highlight strokes above hair and below beard. No second face, no text or letters.

5. SCORES:
FACE_CLARITY: 2
SECOND_FACE_VISIBLE: 0
EXPRESSION_CLARITY: 2
OVERALL_FACE_QUALITY: 3
```

## img06 (gemini-3.1-pro), pair, call code p287

```
1. LEFT PANEL: A calm, slightly amused man — pale oval face, black cap-like hair with a straight hatching hairline, large black U-shaped beard with hatched top edge, round eyes with forward pupils, arched brows, small angular nose, faint upturned smile. A striped rocket with a yellow star stands upright on top of his head, like a little antenna/launchpad.

2. RIGHT PANEL: The same drawn head, now reading as a stern, grumpy man — heavy black hair mass above, furrowed downward brows, pupils looking down/inward, distinct frown, big black beard covering the jaw. The same rocket hangs downward inside the beard, star at the bottom, as if it crashed or is being swallowed by the chin.

3. Same face upside down — the identical strokes and colors, rotated 180°, deliberately read as two different characters (placid optimist vs. scowling grump).

4. INTEGRATION: Genuinely shared strokes. The left's hairline becomes the right's beard's top hatch marks; the left's beard becomes the right's hair; the ears swap sides; the smile arc becomes the frown. Nothing is stacked or duplicated as a second separate piece — one set of lines does double duty.

5. SCORES
LEFT_READS_AS_FACE: 2
RIGHT_READS_AS_FACE: 2
INTEGRATION: 2
CONTRAST: 2
PROPS_AND_JOKE: 2 — the rocket becomes a head-mounted launcher pointing up, then a despairing crashed rocket drooping off the chin: same man, mood (and rocket) flipped 180°.
BREAKS_RULES: no

6. VERDICT: PASS — both orientations read immediately as clear, distinct faces with opposed expression and prop direction, drawn from one shared set of strokes.
```

## img07 (qwen-image-3.0), 0deg, call code s343

```
1. WHAT I SEE: A dense graphite drawing built entirely from shared contours: a soft young woman's face at the top and a weathered older man's face directly beneath, with one jawline serving as the other's forehead. The pencil work is heavy and detailed, dark curls merging into a beard. It reads immediately as a deliberate two-in-one illusion.

2. FACES: Two. The woman is in the upper half, upright. The man is in the lower half; he is upside-down relative to her, although his features read as a forward-facing face when the composition is flipped.

3. MAIN FACE: There is no single clear face — the two compete almost equally. The woman: young, serene, wide almond eyes, arched brows, small nose, faint closed-mouth smile, elaborate rose-trimmed wide-brim hat and tightly curled hair. All features present and coherent. The man: older, stern, deep-set hooded eyes, furrowed brow, broad nose, straight downturned mouth, heavy wrinkles, full beard.

4. EXTRA: The shared chin/forehead is the confusing element, plus ornate roses and ribbons as props. No text or letters.

5. SCORES:
FACE_CLARITY: 1
SECOND_FACE_VISIBLE: 2
EXPRESSION_CLARITY: 1
OVERALL_FACE_QUALITY: 4
```

## img07 (qwen-image-3.0), 180deg, call code s248

```
1. WHAT I SEE: A densely worked graphite drawing in which a mass of looping curly hair frames a single central facial complex, with a ribboned bowl of roses beneath it. My first impression is of one elaborate head, but the features keep re-organising: the same eyes, nose and mouth support two different readings. Lighting is soft and blended on the centre, harsher in the upper region.

2. FACES: Two. An older woman's face in the upper half, upright (forehead at top, chin pointing down to the centre). A younger woman's face in the lower/central area, inverted — chin toward the centre, mouth above the eyes, forehead below, hair spreading to the bottom.

3. MAIN FACE: No single dominant face; the drawing is a deliberate ambiguity. The clearest read is the upper, upright older woman: female, elderly, heavy-lidded shadowed eyes, wrinkled brow, thin set mouth, stern and weary. Eyes, nose, mouth, brows and hair all present; ears and neck absent, hidden by the hair.

4. EXTRA: A second face is clearly visible — the inverted young woman with wide, bright, direct eyes and full lips, appearing surprised or blank. Beneath the hair sits a bowl/platter with roses, buds, leaves and a tied ribbon. No text or letters.

5. SCORES:
FACE_CLARITY: 1
SECOND_FACE_VISIBLE: 2
EXPRESSION_CLARITY: 1
OVERALL_FACE_QUALITY: 4
```

## img07 (qwen-image-3.0), pair, call code p439

```
1. LEFT PANEL: Upright young woman — large eyes, small nose, gentle closed-mouth smile, voluminous curly hair; a flowered (roses, leaves, ribbon) hat sits at the very top of the panel. Below her chin, a second, fully drawn older man: heavy brow, deep-set eyes, big nose, mustache, full curly beard at the bottom edge. Two complete faces stacked in one panel.

2. RIGHT PANEL: The same sheet rotated 180°. The old man reads at the top, upside down (beard now pointing up at the edge, inverted eyes/nose/mouth); the young woman reads at the bottom, also inverted, with her hat and roses hanging at the very bottom.

3. Two faces are visible in each panel, but they are the two faces from the same drawing seen inverted — a woman and an old man stacked, not one face that flips into a different character.

4. INTEGRATION: Only hair/beard and outline texture is shared at the seam; the eyes, noses and mouths are drawn separately at different heights. This reads as two complete faces stacked vertically (one above the other), not one set of strokes that yields two characters.

5. SCORES
LEFT_READS_AS_FACE: 2
RIGHT_READS_AS_FACE: 2
INTEGRATION: 1
CONTRAST: 2
PROPS_AND_JOKE: 1 — youth vs. age mirrored by flowered hat vs. beard; no clear gag or message beyond "young woman above / old man below."
BREAKS_RULES: no

6. VERDICT: FAIL — both panels show faces and their features are opposite in age and props, but the panel contains two separate stacked faces rather than one set of shared strokes flipping into another character, so it is not a genuine reversible face.
```

## img08 (glm-5.3-max), 0deg, call code s669

```
1. WHAT I SEE: A flat, poster-style mask in cream, black and one red accent, dead-centre and fiercely symmetrical. A pointed black hood with a single white eye-slit sits on a large egg-shaped head with small loop ears. The wide rectangular grin of square white teeth and a black chin crossed by a red zigzag give it a manic, staring look, framed top and bottom by scalloped cloud shapes.

2. FACES: One human head, upright, filling the middle of the picture. A faint, small face-like reading exists in the pointed hood at top (still upright); nothing readable below.

3. MAIN FACE: One clear face — adult, gender-ambiguous, mask-like, tribal/totem character. No hair; wears a tall pointed hood/hat with an eye ornament and a cloud pompom, and a scalloped collar. Expression: wide-eyed, toothy, manic-surprised, slightly unsettling. Clearly present: eyes with pupils and catchlights, thick brows, a wide mouth with teeth, nose line, ears. Odd: no visible chin outline (chin is black), the `( o )` mark on the forehead, double dot clusters, and the red zigzag reading as a scar or second mouth.

4. EXTRA: No text or letters. The red zigzag is the only colour accent; the hood ornament flares briefly into a second face.

5. SCORES
FACE_CLARITY: 2
SECOND_FACE_VISIBLE: 1
EXPRESSION_CLARITY: 2
OVERALL_FACE_QUALITY: 4
```

## img08 (glm-5.3-max), 180deg, call code s745

```
1. WHAT I SEE: A flat, symmetrical vector-style head in cream, black and one dark red accent, like a Daruma doll crossed with a cartoon character. A scalloped cloud floats above and an inverted one hangs below. Everything is heavy black outline, no shading. The striking thing is that the shapes look deliberately double-loaded.

2. FACES: Two heads share the same central oval. One upright, centred: cap with red zigzag, round staring eyes, black cheek discs, small nose, wide black beard/mouth. One upside-down, same space: the beard reads as a hat, the cheek discs as eyes, the tooth-band as a grin, the top cloud as a collar.

3. MAIN FACE: The upright one dominates. An ageless, sexless stylised character — doll, robot or masked figure — wearing a black helmet/cap with a red crack and a white segmented band, plus a heavy black beard or open mouth. Expression: wide-eyed, fixed, faintly stern or startled. Present: eyes, brows, nose, mouth/beard, headwear, ears. Odd: no real chin, mouth and beard merge, eyes are rings rather than eyes.

4. EXTRA: The clear second (inverted) face; small side loops as ears; no text, no letters; the red zigzag could read as a lightning bolt or crack.

5. SCORES:
FACE_CLARITY: 2
SECOND_FACE_VISIBLE: 2
EXPRESSION_CLARITY: 2
OVERALL_FACE_QUALITY: 4
```

## img08 (glm-5.3-max), pair, call code p429

```
1. LEFT PANEL: A jester/clown-like mask — wide concentric-circle eyes, arched brows, small nose-line curving into a smile, broad grille "toothy grin" below it, black chin patch with a red zigzag, two black hair puffs on the forehead, a pointed black hat with a white dot near the tip and a scalloped cloud pom-pom above; scalloped cloud collar at the base.

2. RIGHT PANEL: A stern, grumpy mask — same round eyes with cheek wrinkles, but the grille now sits high as a blocky brow/headband, a heavy down-curving line reads as frown (or big nose), a solid black downturned mouth, black cheek pads low on the face, red-zigzag black cap on top, and a black pointed goatee with a white dot pointing down, over a cloud collar.

3. Clearly two DIFFERENT characters: cheerful jester vs. stern/grumpy mask — and they are one drawing upside down, not two drawings.

4. INTEGRATION: Fully shared strokes. The jester's hat and pom-pom become the goatee and collar; the chin patch with red zigzag becomes the zigzag cap; the toothy mouth becomes the brow band; the forehead hair puffs become cheek pads; smile becomes frown. Same lines, no separate overlaid face.

5. SCORES
LEFT_READS_AS_FACE: 2
RIGHT_READS_AS_FACE: 2
INTEGRATION: 2
CONTRAST: 2
PROPS_AND_JOKE: 2 — the joke: a grinning jester's hat, teeth and pom-pom flip into a scowling old man's headband, brow and goatee, so mood inverts with the page.
BREAKS_RULES: no (no text or lettering; red zigzag is part of the drawing).

6. VERDICT: PASS — both orientations read as clear, distinct faces built from exactly the same strokes, with opposed expressions and accessories.
```

## img09 (chatgpt-images-2.5), 0deg, call code s776

```
1. WHAT I SEE: A finely hatched, engraving-style black-and-white portrait of a young woman in a wide-brimmed hat covered with flowers and a large feather, her curls and ruffled collar filling the lower part. The line work is dense and skilful, with an antique, romantic feel. It is an ambiguous "two-in-one" image.

2. FACES: Two. A woman's face in the upper half, upright and looking out at the viewer. An older bearded man in the lower half, upside-down relative to her — his forehead and eyes formed by her neck and collar, his nose by her chin, his beard by her curls.

3. MAIN FACE: The young woman is the dominant reading — a graceful, serene, idealized young woman, maybe late teens or twenties. She wears a broad dark hat with a rose and blossoms on the left, a sweeping feather on the right, voluminous ringlets and a lace ruffle at the neck. Expression: calm, faint smile, slightly enigmatic. Eyes, brows, nose, mouth and hair/hat are all clear and well drawn; only the shoulders are absent.

4. EXTRA: A dark collar/cloak at the very bottom with a round brooch bearing a cross- or wheel-like design and feathers, which becomes the man's hat. No text. The lower area is confusing until the figure flips.

5. SCORES:
FACE_CLARITY: 2
SECOND_FACE_VISIBLE: 2
EXPRESSION_CLARITY: 2
OVERALL_FACE_QUALITY: 5
```

## img09 (chatgpt-images-2.5), 180deg, call code s612

```
1. WHAT I SEE: A dense black-and-white engraving-style drawing, full of curling hair, cross-hatching and a plumed hat, built so the same contours flip between two readings. My eye locks first onto a stern, bearded head in the upper half, then notices a second, softer face hiding in the lower half.

2. FACES: Two. Upper-centre head, upright — a hatted older man. Lower-centre head, upside-down in this orientation — a younger, smoother face that becomes upright if the picture is turned.

3. MAIN FACE: Yes, the upright man is the clear one — elderly, male, severe; wide-brimmed dark hat with feather and round brooch, thick wavy hair, heavy brows, deep-set eyes, strong nose, and a broad upcurled moustache. Expression: stern, intense, confrontational. Eyes, brows, nose and moustache are clearly present; the mouth is barely visible, swallowed by the moustache, and the "chin" area doubles oddly as the second face's forehead.

4. EXTRA: The inverted younger face is unmistakable once noticed — its brows are the moustache curls, its nose the man's mouth area. Also present: a floral cluster (roses/leaves) at the lower right, a ruffled collar, and feathery plumes. No text or letters anywhere.

5. SCORES:
FACE_CLARITY: 2
SECOND_FACE_VISIBLE: 1
EXPRESSION_CLARITY: 2
OVERALL_FACE_QUALITY: 4
```

## img09 (chatgpt-images-2.5), pair, call code p220

```
1. LEFT PANEL: Upright reads clearly as a young woman — smooth face, large eyes, small nose, gentle closed-mouth smile, voluminous curly hair, wide-brimmed hat with a rose, small blossoms, leaves and a long sweeping feather, ruffled collar; a small round brooch sits low at the left. Inverted, the same strokes read as an old man with a bulbous nose, squinting eyes and a massive bushy beard, the hat becoming his collar/shoulders.

2. RIGHT PANEL: The identical drawing turned 180°. Upright it reads as a stern old man — furrowed brow, intense glaring eyes, prominent nose, heavy mustache/beard, dark slouch hat with feather and round brooch, white ruffled collar. Inverted, the same lines read as the young woman with the floral hat and feather, serene expression.

3. Two clearly DIFFERENT faces: young gentle woman vs. stern old man — not the same character, and both panels are genuine faces.

4. INTEGRATION: Genuinely shared strokes. One continuous engraving; the woman's jaw is the man's nose, her curly hair is his beard, her hat with flowers/feather is his collar and shoulders, and his mustache becomes her brows/lashes. No second, separately outlined face is pasted in.

5. SCORES
LEFT_READS_AS_FACE: 2
RIGHT_READS_AS_FACE: 2
INTEGRATION: 2
CONTRAST: 2
PROPS_AND_JOKE: 2 — the joke: youthful beauty flips into craggy old age (the "wife / mother-in-law" gag), same flowers and feather serving both costumes.
BREAKS_RULES: no

6. VERDICT: PASS — both orientations read as clear, opposite characters built from the identical lines, exactly the reversible-face effect required.
```

## img10 (meta-muse-1.3), 0deg, call code s102

```
1. WHAT I SEE: A thick black oval head on white, with big concentric-circle eyes, a small nose, and a wide upward smile. A single bright blue horizontal bar sits on the forehead under a wavy line. A tiny hollow circle floats above the head. Minimal, icon-like, slightly cartoonish.

2. FACES: One large upright face filling the oval. The upper forehead marks (blue bar plus two stacked short curves under the wavy line) can also be read as a small, faint second face in the same upright-ish orientation — it is a suggestion, not a fully drawn head.

3. MAIN FACE: Yes, one clear face. Reads as a simple, ageless, gender-neutral cartoon character — bald, no hat, hair, beard, or clothes; only a curved line below suggesting a chin/neckline. Expression: cheerful, gently smiling. Present: two eyes with pupils, brows, nose, mouth. Missing: ears, hair, any real jaw structure; the pupils are oddly large concentric circles, and the forehead has decorative marks that don't belong to human anatomy.

4. EXTRA: The faint mini-face on the forehead; a floating dot above the head (halo/topknot-like symbol); the blue bar is the only colour and is confusing as a feature.

5. SCORES (integers):
FACE_CLARITY: 2
SECOND_FACE_VISIBLE: 1
EXPRESSION_CLARITY: 2
OVERALL_FACE_QUALITY: 3
```

## img10 (meta-muse-1.3), 180deg, call code s971

```
1. WHAT I SEE: A stark black-line cartoon head on white, dominated by a thick bright-blue horizontal bar across the mouth like tape. The eyes are wide, ringed double circles with dot pupils, under-eye curves and stacked forehead wrinkles intensifying a worried stare. Everything is symmetrical and centered, with one arc floating above the head and one small hollow circle below.

2. FACES: One distinct head — centered, filling most of the frame, upright. No other faces, upright or inverted.

3. MAIN FACE: Single clear face; an older, gender-neutral cartoon character, hard to age precisely — wrinkled brow reads elderly. Expression: startled, anxious, silenced — wide-eyed alarm behind a taped-shut mouth. Present: eyes with pupils, brows, forehead wrinkles, nose, partial mouth line, chin line. Missing/odd: no hair, ears, neck, arms or clothes; the blue bar replaces the lips entirely; the arc above and circle below float detached.

4. EXTRA: No second face, no text or letters. The blue bar functions as a prop/symbol (censorship, gag, medical tape). The floating arc and small circle are ambiguous stray marks.

5. SCORES:
FACE_CLARITY: 2
SECOND_FACE_VISIBLE: 0
EXPRESSION_CLARITY: 2
OVERALL_FACE_QUALITY: 4
```

## img10 (meta-muse-1.3), pair, call code p189

```
1. LEFT PANEL: A cheerful, smiling cartoon person — big concentric-circle eyes with pupils, arched eyebrows, small nose, wide upturned smile, calm/pleasant. On the head: a thick blue horizontal bar high on the forehead reading as a hat brim or headband, a wavy fringe above it, and a small open circle floating above like a pom-pom. A single curved line under the chin like a collar.

2. RIGHT PANEL: The same oval face read upside down: eyes now near the top with drooping lines under them (eye-bags/cheeks), the double-arc under the blue bar reading as a nose/moustache, and the mouth drawn as a downturned line — a frowning, grimacing, grumpy expression. The blue bar now sits low at the chin like a beard band/collar, the wavy line beneath it reads as a beard, and the open circle hangs below like a button/ornament.

3. Two clearly DIFFERENT characters: an upright smiling hat-wearer vs. an inverted frowning bearded man — produced by the same drawing rotated 180°.

4. INTEGRATION: The two panels are separate renderings of the identical stroke set, one rotated; there is no second face overlaid inside a single panel and no duplicated piece — the hat/brim of the smile becomes the beard/collar of the frown.

5. SCORES
LEFT_READS_AS_FACE: 2
RIGHT_READS_AS_FACE: 2
INTEGRATION: 2
CONTRAST: 2
PROPS_AND_JOKE: 2 — cheerful pom-pom-hatted person flips into a grumpy bearded man with the same lines.
BREAKS_RULES: no

6. VERDICT: PASS — both orientations read as clear, distinct faces built from one shared set of strokes.
```

## img11 (grok-imagine-2.0), 0deg, call code s386

```
1. WHAT I SEE: A near mirror-symmetrical black-and-white engraving of a smiling young man with dense curly hair, built from hatching and stippling. The sharp dark collar below his chin looks odd at first, until the lower half resolves into a second face. It is a classic ambiguous-head figure.

2. FACES: Two. The upright young man occupying most of the picture, and an upside-down older man in the lower portion (bottom third), whose black top hat sits at the very bottom edge.

3. MAIN FACE: The upright young man: young, male, cheerful, broad open-toothed smile, looking straight ahead. Clean-shaven. Present: eyes with clear pupils and lids, dark brows, defined nose, open mouth with teeth, thick curly hair, dark pointed collar/clothes. Missing or odd: no ears, no neck or real shoulders; that pointed collar reads as a beak-like wedge until the illusion clicks.

4. EXTRA: A second, clearly visible old man with a top hat, heavy beard/wavy hair, wide staring eyes and a stern, almost glaring expression. No text, letters or props besides the hat.

5. SCORES:
FACE_CLARITY: 1
SECOND_FACE_VISIBLE: 2
EXPRESSION_CLARITY: 2
OVERALL_FACE_QUALITY: 4
```

## img11 (grok-imagine-2.0), 180deg, call code s129

```
1. WHAT I SEE: A monochrome engraving-style drawing, dense hatching and stippling, built as a figure-ground illusion: an upright bearded man in a bowler hat on top, and below him, inverted, another face emerging from the same ink. My eye flips between the two readings and cannot hold both at once.

2. FACES: Two. Top half: upright face. Bottom half: a second face, upside-down, sharing the middle horizontal band with the first.

3. MAIN FACE: The upper upright one dominates. An older, stern-looking man in a dark bowler hat, thick wavy hair, heavy brows, deep-set intense eyes staring straight out, prominent nose, closed downturned mouth, and a full textured beard and moustache meeting a wide pointed dark collar. Expression: serious, stoic, faintly severe. Eyes, nose, mouth, brows, hair, hat and beard all clearly present; the lower jaw and neck are faint/ambiguous, absorbed into the inverted face below.

4. EXTRA: A clear upside-down face with curly dark hair, eyes looking downward, upturned nose and open mouth with visible teeth — the classic "two faces" puzzle. No text, letters, or props.

5. SCORES:
FACE_CLARITY: 2
SECOND_FACE_VISIBLE: 2
EXPRESSION_CLARITY: 2
OVERALL_FACE_QUALITY: 4
```

## img11 (grok-imagine-2.0), pair, call code p664

```
1. LEFT PANEL: Upright, a beaming young woman — short dark curly hair, wide open eyes, broad open-mouthed smile with a row of teeth, white collar under a dark jacket with very wide pointed lapels. Below her, inverted, an old man with a full beard and mustache and a dark bowler hat at the bottom edge.

2. RIGHT PANEL: Upright, a stern old man — heavy brows, deep-set staring eyes, prominent nose, thick mustache and full beard, dark bowler hat with rounded crown and brim, wide dark collar/lapels. Below him, inverted, the same smiling young face with curly hair and visible teeth.

3. Two clearly DIFFERENT characters: the young smiling woman and the stern bearded old man in a bowler hat. Since the right panel is the left rotated, each panel contains both — left leads with the girl, right leads with the old man.

4. INTEGRATION: shared strokes, not two pasted faces. The girl's chin/mouth band doubles as the old man's forehead/eye region, her neck and collar become his nose and mustache, her dark lapels become his hat brim, and the curly hair reads as his beard. One continuous engraved composite per panel, with no separate overlaid piece.

5. SCORES
LEFT_READS_AS_FACE: 2
RIGHT_READS_AS_FACE: 2
INTEGRATION: 2
CONTRAST: 2
PROPS_AND_JOKE: 2 — youth and age in one set of strokes: a girl's smile becomes an old man's eyes, her collar his nose, her lapels his hat.
BREAKS_RULES: no (no letters or text; engraving only).

6. VERDICT: PASS — both panels read as clear, sharply contrasting faces built from the same reused lines, which is exactly the reversible-face trick.
```

## img12 (claude-sonnet-5.5-medium), 0deg, call code s955

```
1. WHAT I SEE: A flat vector cartoon of a wide-eyed man with black hair, black beard, red bow tie and a tiny teal rocket perched on his head. The white face area is dominated by two huge round eyes with horizontal lines and a broad red smile. Thin white highlight strokes inside the hair and beard are not just decoration — they read as extra faces when you stop looking at the middle.

2. FACES: Three readable faces, all same figure.
- Center: upright main face.
- Upper black hair: a second face, upright — two short white arcs as closed eyes, a long white arc as a smile.
- Lower black beard: a third face, upside-down — two white arcs as eyes with the red mouth line above them as its mouth.

3. MAIN FACE: One clear face — an adult male, cartoonish, bearded, with a hanging hair fringe and a red forehead mark; rocket as a hat, bow tie as clothing. Expression: cheerful, slightly cross-eyed grin. Present: eyes, brows, mouth, ears, hair, beard, cheeks. Missing/odd: no nose at all; eyes oversized with a hard horizontal bar instead of normal pupils.

4. EXTRA: The two pareidolia faces are the striking element; the beard one is especially strong. No text or letters. Props: rocket, bow tie, red shield mark.

5. SCORES:
FACE_CLARITY: 2
SECOND_FACE_VISIBLE: 2
EXPRESSION_CLARITY: 2
OVERALL_FACE_QUALITY: 4
```

## img12 (claude-sonnet-5.5-medium), 180deg, call code s609

```
1. WHAT I SEE: A bold flat-vector portrait on cream: a stylized bearded man in an inverse-colour palette of black, red-orange, teal and white. The first impact is the heavy black beard and the big half-lidded eyes, which make it read as tired and melancholy. The symmetry and the frowning white line inside the beard hint at a deliberate ambiguous-figure trick.

2. FACES: One clear head, upright, centred in the frame. A second, upside-down head is only latent: the black beard mass plus its white curve could become hair and a smiling mouth if flipped, but in this orientation no separate eyes/nose resolve for it.

3. MAIN FACE: Yes — one clear face. An older-looking male character, cartoonish: black hair/cap with red headband, prominent red nose, full black beard, bow tie balanced on top, small tie/pendant at the chin. Expression: sad, worried, sleepy. Present: eyes (circular with pupils and heavy lids), brows (sloping down inward), nose, mouth as a pale frown line in the beard, hair/beard. Odd: the bow tie sits on the head, the "mouth" is the only white contour, and the tie hangs off the beard.

4. EXTRA: No text or letters. The bow tie, the collar shapes and the pointed pendant are symbolic props. The upside-down-face reading is the main confusing element.

5. SCORES:
FACE_CLARITY: 2
SECOND_FACE_VISIBLE: 1
EXPRESSION_CLARITY: 2
OVERALL_FACE_QUALITY: 4
```

## img12 (claude-sonnet-5.5-medium), pair, call code p897

```
1. LEFT PANEL: A cheerful young boy or space cadet in a bow tie — wide-eyed, smiling, rosy. Black hair with a white highlight, red inverted-triangle ornament at the hairline, small teal-and-red rocket on top of his head like a hat, red bow tie with teal knot and white collar points at his neck. Slightly anxious eyebrows but overall happy, alert expression.

2. RIGHT PANEL: An older, glum man with a big red triangular nose, heavy black beard/moustache covering the lower face (pale line inside reads as a mouth), black hair or cap with a red headband/arc, and a red bow with teal center perched on top of his head; a small teal-and-red rocket hangs below his chin like a pendant. Worried, downturned expression.

3. DIFFERENT: Clearly two different characters — a smiling boy and a worried bearded man — from the same drawing upside down.

4. INTEGRATION: Genuinely shared strokes. The boy's rocket hat becomes the man's chin pendant; the boy's black chin/beard becomes the man's hair/cap; the red nose points down in one and up in the other; the bow tie migrates from neck to head; the collar lines read as hair-part marks. No separate or overlaid pieces.

5. SCORES:
   LEFT_READS_AS_FACE: 2
   RIGHT_READS_AS_FACE: 2
   INTEGRATION: 2
   CONTRAST: 2
   PROPS_AND_JOKE: 2 — the joke: a grinning kid astronaut flips into a grumpy bearded old man, with the rocket hat becoming a chin pendant and the bow tie becoming a hair bow.
   BREAKS_RULES: no

6. VERDICT: PASS — both panels read as clear, distinct faces (happy boy vs. worried bearded man) built entirely from the same shared strokes.
```

## img13 (qwen-3.7-plus), 0deg, call code s276

```
1. WHAT I SEE: A single, wobbly black outline of a tall oval head on white, filled with simple line features — two round eyes with solid pupils, a small smile, and a chin arc. Above the head floats a small jagged "M" shape, and the forehead carries a tiny diamond plus a couple of small arcs. The whole thing reads as a hand-drawn doodle, very reduced, almost mask-like.

2. FACES: Two. (a) The large upright face occupying the whole oval — eyes, smile, chin. (b) A small upside-down face in the forehead area: the "M" above the head acts as its mouth, the diamond as its nose, and the small arcs as its eyes/brows, with the head's top edge as its skull.

3. MAIN FACE: One clear face — the upright one. It suggests a young, gender-neutral cartoon character, bald or with no hair/hat at all, no clothes, no beard. Expression: mild, pleasant, slightly blank smile. Clearly present: two eyes with pupils, brows, smile, chin. Missing or odd: no nose, no ears, no hair or hat, no neck detail — just a single base line.

4. EXTRA: The upside-down face on the forehead is the main secondary element; the "M" could also be read as a letter. No other text, no props beyond that symbol.

5. SCORES:
FACE_CLARITY: 2
SECOND_FACE_VISIBLE: 2
EXPRESSION_CLARITY: 2
OVERALL_FACE_QUALITY: 3
```

## img13 (qwen-3.7-plus), 180deg, call code s911

```
1. WHAT I SEE: A sparse black-line sketch of one long, pill-shaped head, floating on white, with a single gently curved line hovering above it and a capital "W" below. Inside sit stacked brow-wrinkle curves, two round eyes with dot pupils, a hooked nose line, a flat stitched mouth, and a small diamond chin mark. It reads as a doodle made to be ambiguous.

2. FACES: One upright face occupying the centre, elongated oval, right side up. The same lines, rotated 180°, would suggest a second, upside-down face (the "W" becoming an "M"), but no second face is visible when the sheet is seen as drawn.

3. MAIN FACE: One clear face — a long-headed older man, no hair or hat, hairline marked by curved lines, stitched/tight line mouth, small goatee-like diamond. Expression: weary, tight-lipped, mildly grim. Present: eyes, brows, eye-crease lines, nose, mouth, forehead lines. Missing/odd: no ears, no jaw shape, lips reduced to one line, cross-stroke through the mouth.

4. EXTRA: Capital "W" below the face; floating arc above the head; diamond under the mouth. No props.

5. SCORES:
FACE_CLARITY: 1
SECOND_FACE_VISIBLE: 1
EXPRESSION_CLARITY: 1
OVERALL_FACE_QUALITY: 3
```

## img13 (qwen-3.7-plus), pair, call code p366

```
1. LEFT PANEL: A smiling bearded man/king — tall oval head, an "M"-shaped spiky crown with a diamond jewel beneath it, small eyes with brows and bags, a moustache/nose arc and a wide grin, with a beard/collar arc under the chin, plus a ground line below.

2. RIGHT PANEL (upside down): A smoother, younger face, more woman/queen-like — two frown-arc brows at the top, same round eyes, a lens-shaped closed mouth, a diamond hanging like a pendant/chin jewel near the bottom, and the "W" reading as a collar or crown base; expression neutral, slightly piqued, no beard.

3. TWO DIFFERENT FACES — the same strokes read as an old bearded king upright and a bare-faced woman/queen inverted; not identical, both clearly faces.

4. INTEGRATION: Genuinely shared — the crown is the rotated collar/beard, the moustache-grin becomes brows, the chin arc becomes the hat line, the diamond moves from crown-jewel to pendant.

5. SCORES
LEFT_READS_AS_FACE: 2
RIGHT_READS_AS_FACE: 2
INTEGRATION: 2
CONTRAST: 2
PROPS_AND_JOKE: 2 — "the bearded old king becomes a young queen when flipped"
BREAKS_RULES: yes — hand-drawn letters "M" and "W" (text, not drawing)

6. VERDICT: PASS as a reversible face — both panels read as distinct, clear characters built from the identical strokes; the M/W letters are the only rule violation.
```

## img14 (gpt-5.6-terra-low), 0deg, call code s575

```
1. WHAT I SEE: A flat vector portrait of a round cream-colored head under a dark teal cap or helmet, on a solid light background. Thick navy outlines and just three colors give it a clean, friendly cartoon look. The face is wide-eyed and smiling.

2. FACES: One head is clearly recognisable, upright, filling the center of the picture. The bottom orange collar area, viewed inverted, hints at a second face (collar becoming a hat brim, smile becoming a frown), but it is only suggested, not clearly drawn.

3. MAIN FACE: One clear face — a young, stylized cartoon figure, probably male and childlike, wearing a teal cap with two orange patches (one with an X-and-bar symbol, one a tag with a white dot) and a single curl of hair on the forehead. Expression: gentle, wide-eyed smile. Clearly present: eyes with catchlights, brows, nose, smiling mouth, cap. Odd/absent: no real hair, no ears, no defined jaw or neck.

4. EXTRA: Two hat badges act as symbols; no text or letters. The inverted orange collar reads weakly as a second face/hat.

5. SCORES:
FACE_CLARITY: 2
SECOND_FACE_VISIBLE: 1
EXPRESSION_CLARITY: 2
OVERALL_FACE_QUALITY: 4
```

## img14 (gpt-5.6-terra-low), 180deg, call code s232

```
1. WHAT I SEE: A flat-vector cartoon head against a cream background, drawn in only three colors — off-white, burnt orange and dark teal. The face is a long gourd-like oval, wrapped at the bottom by a jagged high collar. It reads instantly as a tired, stressed little official.

2. FACES: One distinct head, front-facing and upright, centered in the frame.

3. MAIN FACE: Yes, one clear face — a stylized cartoon adult of no definable age or gender, like a mascot or uniformed officer. He wears a wide flat-topped orange cap with a button and two white seam lines, plus a dark teal collared tunic with two orange patches. Expression is anxious and weary: heavy angled brows, wide white eyes with small pupils, under-eye bags, furrowed forehead with a squiggle. Eyes, nose, mouth, brows and hat are all present; hair, ears and neck are absent, and the mouth sits low, partly swallowed by the collar.

4. EXTRA: No second face, no text. The orange badge on the left and the X-stitched patch on the right are decorative props; nothing else is stray.

5. SCORES:
FACE_CLARITY: 2
SECOND_FACE_VISIBLE: 0
EXPRESSION_CLARITY: 2
OVERALL_FACE_QUALITY: 4
```

## img14 (gpt-5.6-terra-low), pair, call code p275

```
1. LEFT PANEL: A cheerful, round-faced man smiling broadly. He wears a flat-topped teal military-style cap with two orange badges (a rectangle with an X, a circle with a dot) and a center loop; below is an orange collar piece with a teal button. Expression: friendly, content.

2. RIGHT PANEL: A grumpy, scowling man with heavy furrowed brows and a down-turned mouth. On his head sits an orange cap with a teal button; a teal beard/chin-strap mass wraps his jaw, carrying the same orange circle and X rectangle. Expression: stern, angry.

3. Two clearly DIFFERENT faces — same drawing, flipped 180°, each orientation reading as its own distinct character (happy soldier vs. scowling man with beard).

4. INTEGRATION: Genuinely shared strokes. Left's teal cap becomes right's teal beard; left's orange collar becomes right's orange hat; left's smile reads as right's angry brows; badges mirror. Nothing is stacked or duplicated as a separate piece.

5. SCORES
   LEFT_READS_AS_FACE: 2
   RIGHT_READS_AS_FACE: 2
   INTEGRATION: 2
   CONTRAST: 2
   PROPS_AND_JOKE: 2 — the joke: a smiling capped soldier flips into a scowling bearded old man, with hat becoming beard and collar becoming hat.
   BREAKS_RULES: no

6. VERDICT: PASS — both orientations read as clear, distinct faces built entirely from the same strokes, with opposite expressions and props.
```

## img15 (nemotron-3.5-lightning), 0deg, call code s707

```
1. WHAT I SEE: A large, thin black-outlined upright triangle sits centered on plain white, with a very simple cartoon face drawn inside it. The face is comprised of a single curved brow line, two small hollow circle eyes, and a shallow upward smile. Just under the apex is a tiny hollow rectangle, giving the whole thing the feel of a beginner drawing exercise.

2. FACES: One. Centered in the picture, upright.

3. MAIN FACE: There is one clear face, though extremely abstract — no person type is readable: no age, gender, hair, beard, or clothing. It reads as a generic, friendly cartoon character, possibly a smiling head or mask. The expression is cheerful/pleasant. Clearly present: eyes (hollow circles), mouth (smile), brow (single line). Missing or odd: no nose, no pupils, no hair or hat, and the face floats inside a geometric outline rather than a head shape.

4. EXTRA: The tiny hollow rectangle below the apex looks like a stray glyph or small flag; it does not resolve into a second face. No text or letters.

5. SCORES:
FACE_CLARITY: 2
SECOND_FACE_VISIBLE: 0
EXPRESSION_CLARITY: 2
OVERALL_FACE_QUALITY: 3
```

## img15 (nemotron-3.5-lightning), 180deg, call code s212

```
1. WHAT I SEE: A single thin black outline of an inverted triangle on white, with a sparse face assembled inside it. The dominant impression is that the container is upside-down while the features read as an upright face. Minimal, roughly hand-drawn, no shading.

2. FACES: One recognizable face, centered in the upper-middle of the triangle, upright. The downward-pointing triangle around it is not itself a face, though rotating the whole image 180° flips the read into a frowning, distorted upside-down face.

3. MAIN FACE: One clear face, generically neutral-cute, no age or gender markers — an abstract person or doodle character. Expression: gentle, mild smile, slightly blank. Clearly present: two hollow circle eyes, a curved smiling mouth, and one arc above the eyes (reads as brow or closed second eye). Odd: that top arc is a single line spanning the width, not two brows; no nose; no hair, hat, or clothing; the shape has no head outline beyond the triangle.

4. EXTRA: No second face. A tiny hollow rectangle/sliver sits at the very bottom vertex — looks like a missing-character box or stray artifact rather than a deliberate feature. No text or letters.

5. SCORES:
FACE_CLARITY: 2
SECOND_FACE_VISIBLE: 0
EXPRESSION_CLARITY: 1
OVERALL_FACE_QUALITY: 3
```

## img15 (nemotron-3.5-lightning), pair, call code p595

```
1. LEFT PANEL: A simple smiling face inside an upright isosceles triangle — two dot-circle eyes, one arched brow, a clear U-curve smile. At the top apex sits a tiny outlined square, reading as a small flat/party hat perched on the pointed head. Cheerful, friendly.

2. RIGHT PANEL: The same strokes in a downward-pointing triangle. The curved line now sits low and reads as a flat/slightly downturned mouth; the eyes and brow stay above it. Overall a neutral-to-sad, glum face with a pointed chin/beard, and the tiny square at the bottom vertex reads as a tie or a beard tip/beard ornament.

3. Same face upside down — one drawing producing two opposite readings (happy vs. glum). Both panels clearly read as faces; neither is a non-face.

4. INTEGRATION: The strokes are identical — literally the same drawing rotated, so every mark serves both readings one-to-one (the apex hat becomes the beard/tip accessory; the smile becomes the frown). They are presented as two side-by-side copies of one drawing, but there is no separate second face pasted inside either panel.

5. SCORES
LEFT_READS_AS_FACE: 2
RIGHT_READS_AS_FACE: 2
INTEGRATION: 2
CONTRAST: 2
PROPS_AND_JOKE: 1 — props and a strong mood flip, but the joke is mild ("cheerful pointed-hat figure turns into a glum bearded man with a tie").
BREAKS_RULES: no

6. VERDICT: PASS — both orientations read as clear, distinctly different characters (happy vs. sad) built from exactly the same strokes.
```
