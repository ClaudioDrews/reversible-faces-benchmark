# David's evaluations (blind)

David is a second AI agent (a Hermes agent, `deepseek/deepseek-v4.1-flash-1017` through OpenRouter) that reviewed this project's design earlier (see [`../../docs/reviews/`](../../docs/reviews/)). Here he judged the 15 baseline images.

## Method

- Invocation: the local Hermes CLI, one-shot, one image per call (`hermes chat --query-file <prompt> --image <png> --oneshot -Q -t vision --max-turns 6`).
- **Blind:** each image had an anonymous random file name that did not reveal the orientation, no model name, no event/title, no verdict, no mention of reversible faces or of this benchmark.
- **Stage 1 (30 calls):** every image in both orientations (as delivered, and rotated 180°), each in its **own independent session**, asked: what do you see, how many faces and which way up, is there one clear face (who, expression, missing features), anything extra, then scores for face clarity, visibility of a second face, expression clarity and overall quality. Prompt: [`prompt-stage1.md`](prompt-stage1.md).
- **Stage 2 (15 calls):** one picture showing the drawing twice (left as is, right rotated 180°, and David was told so), asked for the face in each panel, whether they differ, whether strokes are shared or stacked, scores for the two readings, integration, contrast, props/joke, rule breaks and a PASS/FAIL. Prompt: [`prompt-stage2.md`](prompt-stage2.md).
- Rendering: SVGs rendered with headless Google Chrome at 1000x1000, rotated with PIL; rasters re-saved without metadata, longest side at most 1000 px.
- Cost: about US$0.065 for David's main-model sessions by Hermes' own estimate; about US$0.56 by Hermes' daily insights estimate including the paid auxiliary vision calls.

## Files

| File | Content |
|---|---|
| [`RAW-ANSWERS.md`](RAW-ANSWERS.md) | all 45 answers verbatim, labelled |
| [`vision-describer-excerpts.md`](vision-describer-excerpts.md) | what the auxiliary vision model told David for three calls |
| [`prompt-stage1.md`](prompt-stage1.md), [`prompt-stage2.md`](prompt-stage2.md) | the prompts |
| [`blind-key.json`](blind-key.json) | image id -> model/folder |
| [`call-codes.json`](call-codes.json) | anonymous call code -> image id and orientation (`0deg`, `180deg`, `pair`) |
| [`parsed-scores.json`](parsed-scores.json) | David's numeric scores per call, parsed from the answers |

The 30 blind input images are not stored again; the renders are in [`../previews/`](../previews/). Full Hermes session logs were not kept in the repository.

## Caveats

See the list at the top of [`../README.md`](../README.md): text-only judge fed by a describer that sometimes invents the expected second face, orientation mix-ups, stage 2 not fully blind to the rotation, one call per cell.
