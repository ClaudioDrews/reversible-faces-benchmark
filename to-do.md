# To Do

## 1. Composition

**(a) Current state.** The models are generating faces that can be rotated 180° to reveal another face.

**(b) Open gap.** The models still cannot convey an event, an idea or a message through the faces, nor can they raise the artistic or comic quality.

**(c) Next benchmark version.** The models should be instructed to:

- **Choose an art style "to the model's own taste"**, for example engraving, grotesque realism, ukiyo-e, pop art / comic book, hand-painted watercolor, chalkboard, woodcut, chibi, classic exaggerated caricature, etc.
- **Build the image as a composition: a reversible background first, then the reversible face(s) in front of it.** The intended process:
  1. The model chooses the message it wants to convey.
  2. It imagines the two scenes that appear as the image is rotated 180° and that together could carry that message.
  3. It generates the background of the image, itself reversible (it must also work when rotated 180°).
  4. It generates the face(s) that sit in front of the background.

**(d) Open question.** It may be necessary to give brief instructions on humor, satire, caricature and visual narrative. In principle this should not be needed, since these concepts are already in the models' weights.

**(e) Model-as-judge check.** Give the evaluation checklist to three models plus one human evaluator, and test whether the models can assess the images in a way that is consistent with human perception.
