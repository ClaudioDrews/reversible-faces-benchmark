# David's prompt, stage 1 (one orientation per session)

Sent verbatim with one image attached.

```
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
