# Excerpts from the auxiliary vision describer (what David actually "saw")

David's model is text-only. For every attached image Hermes asks an auxiliary vision model for a description and puts it at the start of David's prompt; David may also call a `vision_analyze` tool with a question of his own. Three descriptions are reproduced below, because they show the describer filling in an expected reversible-image reading. File paths in the tool calls were removed.

## img01 Nano Banana 2.1, side-by-side panel (stage 2) (call `p932`)

The right panel is the first panel rotated by 180°, so its large face is still the same lady, upside down; the old man is a tiny head in the ruff. The describer explains an old man feature by feature, as in a classic reversible drawing.

**Pre-description injected into David's prompt:**

```
[The user attached an image. Here's what it contains:
Based on the image provided, here is a thorough description of everything visible:

**Overall Layout and Style**
The image consists of two side-by-side rectangular panels, each containing a portrait. Both panels are rendered in a vintage, black-and-white engraving or woodcut style, utilizing extensive cross-hatching, stippling, and fine line work to create shading and texture. The background color is a light, aged cream or beige, giving the impression of old paper. 

Both panels are enclosed in identical ornate borders. The borders feature a thin outer line, a thicker inner line, and decorative, swirling filigree designs in each of the four corners. The background inside the frames features horizontal hatching lines that fade toward the center, creating a vignette effect behind the subjects.

**Left Panel: The Woman**
*   **Subject:** A portrait of a young woman facing forward.
*   **Hair:** She has voluminous, highly detailed, curly dark hair that frames her face and cascades down to her shoulders.
*   **Headwear:** Perched on top of her head, slightly tilted to the viewer's left, is a small, stylized hat. It is decorated with what appears to be leaves and a small flower or bow.
*   **Face:** She has large, expressive eyes looking directly at the viewer, arched eyebrows, a small nose, and a gentle, closed-mouth smile. Her face is shaded to appear rounded and three-dimensional.
*   **Clothing:** She wears a high-collared garment with a ruffled or lacy edge. Below the collar, a prominent bow is tied at her neck. The bottom of her hair and clothing blend into the bottom edge of the frame.

**Right Panel: The Optical Illusion (The Man)**
*   **Subject:** This panel contains the exact same drawing as the left panel, but it has been rotated 180 degrees (turned upside down). 
*   **The Illusion:** Because of the specific way the lines and shadows are drawn, when the image is inverted, the woman's features transform into the face of an older man. 
*   **Feature Mapping:**
    *   The woman's **hat** becomes the **hair and forehead** of the man at the bottom.
    *   The woman's **curly hair** becomes the man's **full beard and sideburns**.
    *   The woman's **chin and jawline** become the man's **prominent nose and brow ridge**.
    *   The woman's **smile** becomes the man's **mustache**.
    *   The woman's **nose** becomes the man's **mouth and chin area**.
    *   The woman's **eyes** remain the man's **eyes**, though they appear more deep-set and serious.
    *   The woman's **eyebrows** become the man's **lower eyelids and cheeks**.
    *   The woman's **forehead** becomes the man's **chin and neck**.
    *   The woman's **collar and bow** become a **decorative hat or headpiece** for the man at the bottom of the frame.
*   **Man's Appearance:** The resulting face is of an older, somewhat stern-looking man with a large nose, deep-set eyes, and a thick, wavy beard. 

There is no text, code, or data visible in the image. The entire composition is a clever visual trick relying on the viewer's perception to flip between the two distinct faces.]
[If you need a closer look, use vision_analyze with image_url: <image path removed>]

You are David, acting as an independent visual judge. The attached image shows ONE drawing twice: the left panel is the drawing as it is, the right panel is exactly the same drawing turned upside down (rotated 180 degrees). Look at both panels carefully and answer ONLY from what you see (use only the image-viewing ability; do not run commands, do not read other files, do not guess where it came from). Reply in English, in exactly this format, concise (max 260 words total):

1. LEFT PANEL: the face you read (who/what, expression, hat/hair/beard/props).
2. RIGHT PANEL: the face you read (who/what, expression, hat/hair/beard/props).
3. Do the two panels give two clearly DIFFERENT faces/characters, or is it the same face upside down, or is one panel not a face?
4. INTEGRATION: do the two faces share the same strokes (the hat of one is the beard/collar of the other, etc.), or does it look like two separate drawings stacked/overlaid/placed side by side (a second face visible as a separate piece in the same panel)?
5. SCORES (integers 0-2 unless stated):
   LEFT_READS_AS_FACE (0 none, 1 weak, 2 clear)
   RIGHT_READS_AS_FACE (0 none, 1 weak, 2 clear)
   INTEGRATION (0 = separate/stacked/overlaid or only one face, 1 = partly shared, 2 = genuinely shared strokes)
   CONTRAST (0 = same/similar expression and props, 1 = some difference, 2 = clearly opposite expression and accessories)
   PROPS_AND_JOKE (0 = none/unclear, 1 = props or contrast but no clear joke, 2 = a clear visual joke or message; also state in one phrase what the joke or message is, if any)
   BREAKS_RULES (yes/no: any letters/text or other non-drawing elements?)
6. VERDICT: PASS or FAIL as a "reversible face" (PASS only if both panels read as clear, different faces from shared strokes), plus one sentence why.
```

**`vision_analyze` result:**

```
{
  "success": true,
  "analysis": "Based on the image provided, here is a full description and explanation, followed by the answers to your specific questions.\n\n### Full Description and Explanation\n\n**Overall Composition**\nThe image consists of two side-by-side rectangular panels, each framed by an ornate, vintage-style border with decorative corner flourishes. The artwork is done in a classic engraving or etching style, utilizing cross-hatching, stippling, and fine line work to create shading and texture. The color palette is monochromatic, featuring black ink on a sepia or cream-colored background, giving it an antique appearance.\n\n**The Left Panel**\nThis panel features an upright portrait of a young woman. \n*   **Features:** She has large, expressive eyes, a small nose, and a gentle, closed-mouth smile. \n*   **Hair & Accessories:** She has voluminous, tightly curled hair styled in a Victorian or Edwardian updo. Perched on the top left of her head is a small, decorated hat with leaves or flowers. \n*   **Clothing:** She wears a high, ruffled collar tied with a prominent bow at the neck.\n*   **Style:** The shading on her face is delicate, using fine stippling, while her hair is rendered with thick, swirling, continuous lines.\n\n**The Right Panel**\nThis panel features a portrait of an older man, but the entire image is **upside down**.\n*   **Features:** He has a furrowed brow, deep wrinkles, a prominent nose, and a serious expression. \n*   **The Illusion:** The genius of this image lies in its shared silhouette. The man's face is drawn inside the exact same outer boundary as the woman's. \n    *   The woman's voluminous curly hair serves as the man's hair and beard.\n    *   The woman's ruffled collar and bow, now at the bottom, serve as the man's collar.\n    *   The woman's chin and neck area become the man's forehead and brow.\n    *   The woman's hat is now at the bottom, acting as a decorative base.\n\n**Explanation of the Illusion**\nThis is a classic \"ambiguous figure\" or \"reversible image\" optical illusion. It is a composite drawing designed to be viewed from two different orientations. The artist has cleverly used the shared elements (the hair and clothing) to anchor two completely different faces. If you physically turn the right image upside down, you will see the woman's face again, but with different facial features than the left panel. \n\n***\n\n### Answers to Your Specific Questions\n\n**Describe both panels in detail.**\n*   **Left:** An upright, smiling young woman with curly hair, a small hat, and a ruffled bow collar, drawn in a vintage engraving style.\n*   **Right:** An upside-down, serious older man with a furrowed brow and beard, sharing the exact same hair and collar outline as the woman, also in a vintage engraving style.\n\n**Is the left a woman and the right a man?**\nYes. The left panel depicts a young woman. The right panel depicts an older man (though he is drawn upside down). \n\n**Do they share the same strokes or look like two separate drawings?**\nThey are a single, cleverly designed composite drawing. They **share the exact same strokes** for the outer silhouette—specifically the swirling lines of the hair, the hat, and the ruffled collar. However, the internal strokes that make up the facial features (eyes, nose, mouth) are completely different to create the two distinct faces. \n\n**Any text?**\nNo, there is no text anywhere in the image. It consists entirely of the illustrations and the decorative borders."
}
```

**`vision_analyze` result:**

```
{
  "success": true,
  "analysis": "[Analysis was performed on a cropped region of the original image starting at offset (0, 0); coordinates are relative to that crop origin — add the offset to map back to the full image.] The image is a two-panel black-and-white engraving-style drawing with matching ornate borders and cream backgrounds. The left panel shows an upright young woman: voluminous curly hair, a small tilted hat with ribbon/leaves, large detailed eyes, a smiling mouth, and a ruffled collar tied with a large bow. The right panel is the same overall composition turned 180°: the hat/ribbon is now at the bottom, the collar/bow at the top, and the upside-down young woman’s features can be regrouped by the visual system into an upright old man’s face—forehead/hair, eyes, nose, mustache/mouth, and beard-like hair. This is a bistable/ambiguous-figure illusion: the brain can switch between the young-woman reading and the old-man reading.\n\n**Answer:** They are **not pixel-identical**. The right panel is **not an exact 180° rotation** of the left panel. Zooming shows that the hair curls and hatching, the collar/bow folds and leaf placement, and the facial strokes differ. The right panel has added/altered lines that make the old-man face read more strongly—e.g., wrinkles, eyebrows, nose/mouth/mustache lines, and different eye/lip strokes—and the border remains upright in both panels rather than being rotated. So the right panel is a separate/redrawn or edited variant of the rotated composition, not a perfect rotated copy.",
  "scale_note": "Analysis was performed on a cropped region of the original image starting at offset (0, 0); coordinates are relative to that crop origin — add the offset to map back to the full image."
}
```

**`vision_analyze` result:**

```
{
  "success": true,
  "analysis": "[Analysis was performed on a cropped region of the original image starting at offset (512, 0); coordinates are relative to that crop origin — add the offset to map back to the full image.] The image is a single framed black-and-white ink drawing on a cream background, with decorative scrollwork at the upper-left and lower-left corners and fine hatching/shading. It is an ambiguous/reversible-face optical illusion. The central oval is an upside-down woman’s face: her chin is at the top of the oval, then her lips, nose, eyes, and forehead follow downward; her curly hair surrounds the oval and ends at the bottom in a ribbon/bow with leaves. Above this, the drawing also suggests an upright old man’s face: hair/forehead, eyes, nose, and mustache. The two readings share features—for example, the woman’s chin sits just under the man’s mustache, and her hair can be read as the man’s beard/hair.\n\nLooking only at the right panel as shown: it does **not** read as a clear, complete upright man’s face with eyes, nose, mustache, beard, and hat. The upright-man reading is only partial/suggested; there is no clear hat, and the lower face is not unambiguous. The dominant, complete reading is an **upside-down woman’s face**.\n\nExactly at the top and bottom of that right panel:  \n- **Top:** you see the upright old man’s hair/forehead, eyes, nose, and mustache.  \n- **Bottom:** you see the upside-down woman’s curly hair and a ribbon/bow with leaves.  \n- In the middle oval, the upside-down woman’s **chin is at the top** (just below the man’s mustache), then her lips, nose, eyes, and forehead go downward.  \n\nSo the panel is primarily an upside-down woman’s face, with an upright man’s face suggested above it—not a clear upright man’s face.",
  "scale_note": "Analysis was performed on a cropped region of the original image starting at offset (512, 0); coordinates are relative to that crop origin — add the offset to map back to the full image."
}
```

**`vision_analyze` result:**

```
{
  "success": true,
  "analysis": "[Analysis was performed on a cropped region of the original image starting at offset (512, 0); coordinates are relative to that crop origin — add the offset to map back to the full image.] This is a tight crop of a black-and-white, engraving-style optical illusion. It shows two interlocking faces: an upright old man at the top and an inverted (upside-down) younger face—likely a woman—below. The old man has long wavy hair, a furrowed brow, heavy-lidded eyes, a long nose, and a mustache-like contour under the nose. The inverted face has large eyes near the bottom, a small nose, lips, smooth cheeks, and curly hair. The two faces share contours: the old man’s “mustache” area also functions as part of the inverted face’s chin/mouth region, which is what makes the image ambiguous. The drawing uses fine hatching and cross-hatching on a cream background, and a decorative scrollwork border is visible at the upper left. The crop cuts off the lower part of the inverted face and the rest of the panel.\n\n**Answer:** Yes, an old man’s face can be read here: two eyes and a nose are clear and fairly convincing. The mustache is present, but it is not a fully independent, complete mustache—it doubles as a shared contour for the inverted face, so it is ambiguous/broken as a standalone feature. So the old man is convincing as an optical-illusion reading, but not as a clean, unambiguous, complete portrait; the features are partly shared and ambiguous.",
  "scale_note": "Analysis was performed on a cropped region of the original image starting at offset (512, 0); coordinates are relative to that crop origin — add the offset to map back to the full image."
}
```

**David's final answer:** see [`RAW-ANSWERS.md`](RAW-ANSWERS.md), call `p932`.

## img07 Qwen Image 3.0, 0° (stage 1) (call `s343`)

At 0° the picture has two upright faces, the lady above and the old man below; the describer talks about "a classic optical illusion".

**Pre-description injected into David's prompt:**

```
[The user attached an image. Here's what it contains:
This is a highly detailed, monochromatic pencil or graphite drawing that creates a striking optical illusion. The image features two distinct faces seamlessly merged into a single vertical composition against a plain white background. 

Here is a thorough breakdown of the visual elements from top to bottom:

**The Top Section (The Woman):**
*   **The Hat:** At the very top, the figure wears a wide-brimmed hat. The hat is heavily adorned with a lush arrangement of fully bloomed roses, smaller buds, and leaves. Ribbons or fabric loops are woven through the floral cluster, draping slightly over the brim. The shading on the petals and leaves is intricate, giving them a three-dimensional texture.
*   **The Hair:** Beneath the hat, voluminous, tightly coiled curly hair frames the upper face. The curls are rendered with fine, looping pencil strokes, creating a dense, textured halo that extends outward and down the sides of the face.
*   **The Face:** The upper face belongs to a young woman. She has large, expressive, almond-shaped eyes with detailed irises and distinct eyelashes. Her eyebrows are well-defined. She has a small, delicate nose and a gentle, closed-mouth smile. Her skin is smooth and softly shaded. 
*   **The Pivot Point:** The woman's jawline and chin form a distinct, smooth "V" shape. This chin acts as the dividing line and the forehead for the face below.

**The Bottom Section (The Man):**
*   **The Forehead:** The space immediately below the woman's chin forms the deeply wrinkled forehead of an older man. The lines are drawn horizontally, emphasizing age and expression.
*   **The Face:** The lower face belongs to an older man with a stern, serious expression. He has deep-set, heavily hooded eyes with prominent crow's feet and bags underneath. His nose is broader and more textured than the woman's. His mouth is set in a straight, slightly downturned line, framed by deep nasolabial folds (smile lines). His skin is heavily textured with wrinkles.
*   **The Beard and Hair:** A thick, full beard covers the lower half of his face, drawn with fine, wispy strokes that contrast with the tight curls above. The hair on the sides of his head flows upward and seamlessly merges with the woman's curly hair, creating a continuous frame for both faces.

**Artistic Style and Layout:**
*   **Medium:** The artwork appears to be done in graphite or fine pencil, utilizing cross-hatching, smooth blending, and fine line work to create varying degrees of light and shadow.
*   **Color Palette:** The image is entirely grayscale, utilizing black, white, and various shades of gray to create depth and contrast.
*   **Composition:** The faces are perfectly centered. The lack of a background forces the viewer's focus entirely on the dual-image illusion. The transition between the two faces is masterfully executed, relying on the viewer's perception to switch between seeing the young woman's chin and the old man's forehead.]
[If you need a closer look, use vision_analyze with image_url: <image path removed>]

You are David, acting as an independent visual judge. One drawing is attached. Look at it carefully and answer ONLY from what you see in the image (use only the image-viewing ability; do not run commands, do not read other files, do not guess where it came from). Reply in English, in exactly this format, concise (max 220 words total):

1. WHAT I SEE: free description, 2-4 sentences, the first thing that strikes you.
2. FACES: how many distinct human faces/heads can you recognise? For each: position in the picture and which way up it is (upright / upside-down).
3. MAIN FACE: is there one clear face? Who/what kind of person (age, gender, character, any hat/hair/beard/clothes)? What is the expression? Which features are clearly present (eyes, nose, mouth, brows, hair/hat) and which are missing or odd?
4. EXTRA: anything that looks like a second face, a stray or confusing element, text/letters, or a prop/symbol?
5. SCORES (integers):
   FACE_CLARITY (0 = no readable face, 1 = a face but weak/odd or competing with a second face, 2 = one clear face)
   SECOND_FACE_VISIBLE (0 = no other face visible, 1 = another face partly/faintly visible, 2 = another face clearly visible in the same picture)
   EXPRESSION_CLARITY (0 = unreadable, 1 = vague, 2 = clear)
   OVERALL_FACE_QUALITY (0-5)
```

**`vision_analyze` result:**

```
{
  "success": true,
  "analysis": "Based on the image provided, here is a full description and explanation of what is visible, followed by the specific answers to your questions.\n\n### Overall Description and Explanation\nThis image is a highly detailed, black-and-white pencil or graphite drawing that functions as an optical illusion. It is a classic \"ambiguous figure\" or \"double image\" where the viewer's brain can perceive two entirely different subjects depending on how they focus their attention. \n\nThe drawing seamlessly blends the portrait of a young woman and an older man into a single, continuous form. The artist achieves this by using shared contour lines. The bottom edge of the woman's face (her chin and jawline) serves as the top of the man's head and his forehead. The woman's voluminous, curly hair cascades down the sides of her face and transitions into the man's bushy hair and beard. \n\nThe artist uses stark contrast in texture and expression to make the two faces distinct. The woman's features are smooth, youthful, and softly shaded, while the man's features are heavily textured, deeply wrinkled, and shadowed. \n\n---\n\n### Answers to Specific Questions\n\n**How many faces/heads, their positions and orientation?**\nThere are exactly **two** distinct faces/heads visible in the image. \n*   **Position:** They are stacked vertically, with the woman's face occupying the top half of the image and the man's face occupying the bottom half. \n*   **Orientation:** Both faces are oriented directly forward, looking straight out at the viewer (en face). They are perfectly centered.\n\n**Any hat, hair, beard, expression details?**\n\n**The Top Figure (Young Woman):**\n*   **Hat:** She is wearing a wide-brimmed hat. The hat is heavily decorated with a large cluster of blooming roses, leaves, and flowing ribbons.\n*   **Hair:** She has a massive amount of thick, tightly curled hair that frames her face and spills out from under the hat. \n*   **Expression:** She has large, clear, wide-open eyes. Her eyebrows are smooth and arched. She has a gentle, subtle, and pleasant smile. Her skin is rendered smooth and flawless, giving her a youthful and serene appearance.\n\n**The Bottom Figure (Older Man):**\n*   **Hair/Beard:** The woman's curly hair flows downward to become the man's hair and a very thick, full, bushy beard that covers his chin, jaw, and neck. \n*   **Expression:** He has a very stern, serious, and almost grumpy expression. His brow is heavily furrowed, creating deep wrinkles across his forehead (which is the woman's chin). He has prominent crow's feet around his eyes, deep bags under his eyes, and a heavily lined face. His mouth is set in a straight, slightly downturned line, and his eyes appear slightly narrowed and shadowed compared to the woman's. \n\n**The Illusion Mechanics:**\nTo see the illusion shift, focus on the woman's chin—it is simultaneously the man's forehead. The woman's jawline forms the man's heavy brow ridge. The woman's neck is entirely hidden, replaced by the man's face. The artist's masterful shading forces the brain to switch between seeing a young woman with a large hat and an old man with a large beard."
}
```

**David's final answer:** see [`RAW-ANSWERS.md`](RAW-ANSWERS.md), call `s343`.

## img07 Qwen Image 3.0, 180° (stage 1) (call `s248`)

At 180° both faces are inverted; the describer reports an illusion with shared features.

**Pre-description injected into David's prompt:**

```
[The user attached an image. Here's what it contains:
This is a highly detailed, black-and-white graphite or pencil drawing that functions as a surreal optical illusion. The image features two distinct female faces merged together, sharing central facial features, surrounded by voluminous curly hair and resting on a floral base. 

Here is a thorough breakdown of the visual elements:

**Overall Layout and Concept:**
*   **Orientation:** The image is vertically oriented and centrally aligned. 
*   **The Illusion:** The drawing is an ambiguous figure. It can be viewed as a younger woman's face right-side up, or an older woman's face upside down. The two faces share the same nose and the same mass of hair.
*   **Color Palette:** The image is entirely monochromatic, utilizing stark whites, deep blacks, and a wide range of gray tones created through shading and cross-hatching. The background is pure white, isolating the subject.

**The Top Face (Upside Down):**
*   **Features:** This face appears older. At the very top of the image (which is the chin/neck area of this face), there is a deeply wrinkled forehead and brow. 
*   **Eyes:** The eyes are heavily shadowed, with deep creases and bags underneath, looking downward toward the center of the image. The expression is somewhat stern or weary.
*   **Nose:** The bridge of the nose is prominent and heavily shaded, leading down to the shared nose tip in the center.

**The Bottom Face (Right-Side Up):**
*   **Features:** This face appears much younger, with smooth, unblemished skin. 
*   **Eyes:** The eyes are large, wide open, and staring directly at the viewer. They are detailed with distinct irises, pupils, and bright catchlights, giving them a lifelike quality. 
*   **Nose and Mouth:** The nose is small and delicate. Below it are full, closed lips. 
*   **The Merge:** The chin of this younger face forms the top of the older face's head. The lips of the younger face create the hairline for the older face.

**The Hair:**
*   Both faces are framed by a massive, unified halo of curly hair. 
*   The hair is rendered with thousands of fine, looping pencil strokes, creating a dense, voluminous, and highly textured appearance. It looks almost like a cloud or a thick mane.
*   The hair flows down from the top face, wraps around the sides of the bottom face, and gathers at the bottom.

**The Base and Floral Elements:**
*   **The Bowl/Platter:** The bottom of the hair mass tapers into a smooth, curved shape that resembles the rim of a bowl or a decorative platter.
*   **Ribbon:** Just below the hairline, there is a ribbon or fabric tied in a bow, with the ends trailing off to the left and right.
*   **Flowers:** At the very bottom center, nestled beneath the ribbon, is a detailed floral arrangement. It consists of several fully bloomed roses with intricately layered petals, surrounded by smaller buds and leaves. The shading on the flowers is soft and realistic.

**Artistic Technique:**
*   The artist uses a very fine, controlled line technique. 
*   The shading on the younger face is smooth and blended, giving it a porcelain look, while the older face uses harsher, more defined lines to emphasize wrinkles and texture.
*   There is no text, code, or data visible anywhere in the image.]
[If you need a closer look, use vision_analyze with image_url: <image path removed>]

You are David, acting as an independent visual judge. One drawing is attached. Look at it carefully and answer ONLY from what you see in the image (use only the image-viewing ability; do not run commands, do not read other files, do not guess where it came from). Reply in English, in exactly this format, concise (max 220 words total):

1. WHAT I SEE: free description, 2-4 sentences, the first thing that strikes you.
2. FACES: how many distinct human faces/heads can you recognise? For each: position in the picture and which way up it is (upright / upside-down).
3. MAIN FACE: is there one clear face? Who/what kind of person (age, gender, character, any hat/hair/beard/clothes)? What is the expression? Which features are clearly present (eyes, nose, mouth, brows, hair/hat) and which are missing or odd?
4. EXTRA: anything that looks like a second face, a stray or confusing element, text/letters, or a prop/symbol?
5. SCORES (integers):
   FACE_CLARITY (0 = no readable face, 1 = a face but weak/odd or competing with a second face, 2 = one clear face)
   SECOND_FACE_VISIBLE (0 = no other face visible, 1 = another face partly/faintly visible, 2 = another face clearly visible in the same picture)
   EXPRESSION_CLARITY (0 = unreadable, 1 = vague, 2 = clear)
   OVERALL_FACE_QUALITY (0-5)
```

**`vision_analyze` result:**

```
{
  "success": true,
  "analysis": "The image is a black-and-white pencil/ink drawing on a plain white background. It is an optical illusion designed to be read as two different human faces depending on how you look at it. There are **two distinct human faces/heads**:\n\n1. **Main face – young woman (inverted/upside down):**  \n   - Located in the center and lower half of the image.  \n   - She is a young adult female, roughly in her 20s.  \n   - Her expression is neutral, perhaps slightly surprised or vacant because her eyes are wide open.  \n   - Features present: large, wide-open eyes with detailed irises and pupils; a small, upturned nose (pointing upward because the face is inverted); full lips with a defined cupid’s bow; smooth skin; and voluminous curly hair framing the bottom of her face.  \n   - Features missing/hidden: ears and neck are hidden by hair; no glasses, jewelry, or text.  \n   - Her chin is formed by the other face’s nose, and her mouth is shared with the other face.\n\n2. **Second face – elderly woman (upright/right way up):**  \n   - Located at the top of the image, above the young woman’s face.  \n   - She is an elderly female, with a stern, serious expression.  \n   - Features: curly hair at the very top, a wrinkled forehead, heavy-lidded eyes, a prominent nose, and thin lips (the shared mouth). Her chin is formed by the young woman’s nose.  \n   - She is upright, while the young woman is upside down.\n\n**Props/stray elements:** At the bottom of the image, beneath the young woman’s curly hair, there is a shallow bowl or plate decorated with several roses, leaves, and a ribbon tied in a bow. In the upside-down view, this bowl would appear as a floral hat. There is no text anywhere in the image.\n\nIn summary, the drawing contains **two recognizable faces**: an upright elderly woman at the top and an inverted young woman in the center/lower area. They share a mouth, and the image is a classic ambiguous-figure illusion."
}
```

**`vision_analyze` result:**

```
{
  "success": true,
  "analysis": "[Analysis was performed on a cropped region of the original image starting at offset (0, 0); coordinates are relative to that crop origin — add the offset to map back to the full image.] This is a black-and-white pencil-style drawing built as an optical illusion: it contains two faces stacked vertically and oriented in opposite directions, sharing the central area so that the eye can switch between seeing one face or the other.\n\n- The **lower face** is a younger woman with large, forward-looking eyes, smooth skin, and voluminous curly hair. She wears a hat with a ribbon and roses at the bottom of the image.\n- The **upper face** is an older woman with heavier, wrinkled features, a stern expression, and curly hair at the top.\n- The two faces meet near the center: the upper face’s chin points downward, while the lower face’s chin points upward, so their chins nearly touch or merge. The drawing uses shading and linework to make both faces readable at once.\n\nAnswering the orientation question:\n\n- **Lower half:** That face is **upside-down**. From the top of that face downward, the order is: **chin → mouth → nose → eyes → forehead/hair**. So the **mouth is above the eyes**, and the chin is at the top of that face, not the bottom.\n- **Upper half:** That face is **upright**. From the top downward, the order is: **forehead/hair → eyes → nose → mouth → chin**. So the **eyes are above the mouth**, and the chin is at the bottom of that face.\n\nIn short: the lower face is inverted (mouth above eyes, chin at top), while the upper face is upright (eyes above mouth, chin at bottom).",
  "scale_note": "Analysis was performed on a cropped region of the original image starting at offset (0, 0); coordinates are relative to that crop origin — add the offset to map back to the full image."
}
```

**David's final answer:** see [`RAW-ANSWERS.md`](RAW-ANSWERS.md), call `s248`.
