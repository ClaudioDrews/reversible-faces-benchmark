# Methodology

## Principle

Give the evaluated model the best possible instructions so that it has the best possible chance of success. Material goes into the prompt when it helps the model succeed, not only when it can be scored.

## One-shot

- One prompt, one attempt, one SVG per model.
- Nobody answers questions or gives feedback during the attempt.
- If a call fails for technical reasons (timeout, token limit with no answer), it is retried; those retries and their costs are logged in each round. A retry changes only a setting such as reasoning effort, never the prompt, except for the discarded variant `prompts/discarded/prompt-v5b.md`.

## Human judgment, no rubric

A human opens the SVG in a browser and, holding the phone or the page, turns it upside down. They judge three things instinctively: whether both faces are convincing, how good the drawing is, and whether the joke works. There is no numeric scale, no blind-evaluation sheet and no statistical protocol. Earlier drafts had them (see `design-history/`); they were removed because the human can judge the three things directly, and a rubric would only be useful to the model, which is why a self-check list lives inside the prompt instead.

### How to read the verdict words

The evaluator's words are informal and are translated literally. Roughly: **effect "OK"** means both orientations read as recognizable faces and the second face is clearly different from the first; **effect "somewhat bad"** means the second reading is hard to see or confusing; **artistic quality "low"** means a simple, diagram-like drawing without much character or finish; **"somewhat funny"** means the contrast raises a mild smile; **"not used in an impactful way"** means a specific recent event is not recognizable from the drawing. These are descriptions of one person's reaction, not measurements. The evaluator is also the author of the benchmark.

## What the model sees

Only the prompt text (`prompts/`). Models had no tools: they could not run code, render the SVG or search the web. The prompts are therefore written for blind drawing, with a cheap symbolic check instead of rendering.

## File contract

- Standalone SVG, `xmlns`, `viewBox="0 0 1000 1000"`, `width="1000" height="1000"`, valid XML, no external references, at most 300 KB.
- Forbidden: text of any kind, `<image>`, `<foreignObject>`, `<script>`, gradients, blur/filters, drop shadows and any directional lighting.
- Allowed: line work, hatching, flat fills, a small flat palette, white space.
- From round 3 on, `<title>`, `<desc>` and `<metadata>` are removed from the delivered SVG; they would reveal the event when hovering in a desktop browser. The model states its event and title in two plain lines (`EVENT:` and `TITLE:`) before the SVG, which are logged separately.

## Settings and what was recorded

- Provider: OpenRouter, chat completions, `max_tokens` up to 64000 (lower where noted), reasoning effort `medium` unless noted.
- Recorded per run: prompt and completion tokens, cost reported by the provider, finish reason, raw answer, reasoning trace (when returned), the extracted SVG, validity of the XML.
- Costs are the provider's numbers; failed attempts that were billed are counted separately from delivered runs.

## Rounds and evaluation

Each evaluated round has an `EVALUATION.md` with the human's verdict (translated to English, original wording quoted), the models, prompt, settings, costs, and conclusions that fed the next prompt.
