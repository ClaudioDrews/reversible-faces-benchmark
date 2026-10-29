# Methodology

## Principle

Give the evaluated model the best possible instructions so that it has the best possible chance of success. Material goes into the prompt when it helps the model succeed, not only when it can be scored.

## One-shot

- One prompt, one attempt, one SVG per model.
- Nobody answers questions or gives feedback during the attempt.
- If a call fails for technical reasons (timeout, token limit with no answer), it is retried; those retries and their costs are logged in each round. A retry changes only a setting such as reasoning effort, never the prompt, except for the discarded variant `prompts/discarded/prompt-v5b.md`.

## Human judgment, no rubric

A human opens the SVG in a browser and, holding the phone or the page, turns it upside down. They judge three things instinctively: whether both faces are convincing, how good the drawing is, and whether the joke works. There is no numeric scale, no blind-evaluation sheet and no statistical protocol. Earlier drafts had them (see [`design-history/`](design-history/), superseded); they were removed because the human can judge the three things directly, and a rubric would only be useful to the model, which is why a self-check list lives inside the prompt instead.

### How to read the verdict words

The evaluator's words are informal. Roughly: **effect "OK"** means both orientations read as recognizable faces and the second face is clearly different from the first; **effect "somewhat bad"** means the second reading is hard to see or confusing; **artistic quality "low"** means a simple, diagram-like drawing without much character or finish; **"somewhat funny"** means the contrast raises a mild smile; **"not used in an impactful way"** means a specific recent event is not recognizable from the drawing. These are descriptions of one person's reaction, not measurements. The evaluator is also the author of the benchmark.

## Task variant

Prompt v5 requires **two distinct characters**, A and B, who differ in expression and not only in accessories (at least two of eye opening, brow angle, mouth curve, jaw width, age), and a joke stated as a drawn difference ("A has X / B has Y"). The variant "one person with two expressions" was left out of this version; it is probably harder and is listed in [`future-work.md`](future-work.md).

## What the model sees

Only the prompt text (`prompts/`). In rounds 0–3 the models had no tools: they could not run code, render the SVG or search the web. Those prompts are therefore written for blind drawing, with a cheap symbolic check instead of rendering.

## Round 4: the tool-enabled condition

Round 4 (prompt v6, after the paper) is the exception: the model may call two tools in a loop run by [`scripts/run_models_v6.py`](../scripts/run_models_v6.py): `run_python` (Python in a sandbox with no network) and `render_svg` (Chrome renders the SVG upright and rotated by 180°; the image and text diagnostics come back; models that accept images see it). Limits: 5 renders, 12 tool calls, 16 turns, US$0.25 per model. The judging is unchanged (a human, informal, no rubric). Everything about it, including the differences from prompt v5 and the MiniMax re-run, is in [`../rounds/round-04/SETUP.md`](../rounds/round-04/SETUP.md). It is **not** a controlled comparison with round 3.

## File contract

- Standalone SVG, `xmlns`, `viewBox="0 0 1000 1000"`, `width="1000" height="1000"`, valid XML, no external references, at most 300 KB.
- Forbidden: text of any kind, `<image>`, `<foreignObject>`, `<script>`, gradients, blur/filters, drop shadows and any directional lighting.
- Allowed: line work, hatching, flat fills, a small flat palette, white space.
- From round 3 on, `<title>`, `<desc>` and `<metadata>` are removed from the delivered SVG; they would reveal the event when hovering in a desktop browser. The model states its event and title in two plain lines (`EVENT:` and `TITLE:`) before the SVG, which are logged separately.

## Settings and what was recorded

- Provider: OpenRouter, chat completions, `max_tokens` up to 64000 (lower where noted; in round 4 the limit is per turn), reasoning effort `medium` unless noted.
- Recorded per run: prompt and completion tokens, cost reported by the provider, finish reason, raw answer, reasoning trace (when returned), the extracted SVG, validity of the XML.
- Costs are the provider's numbers; failed attempts that were billed are counted separately from delivered runs.

## Limits of the method

See [`threats-to-validity.md`](threats-to-validity.md): one evaluator who is also the author, informal verdicts, three models, one run each, uneven settings in rounds 3 and 4.

## Rounds and evaluation

Each evaluated round has an `EVALUATION.md` with the human's verdict (in English), the models, prompt, settings, costs, and conclusions that fed the next prompt.
