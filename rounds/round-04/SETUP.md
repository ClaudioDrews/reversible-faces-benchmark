# Round 4 setup: prompt v6, tool-enabled condition

Goal: the same task as round 3 (one SVG showing one face upright and another when rotated by 180°, with a joke about a recent technology/AI event), the same three models, but the models **may run code and look at their own drawing**. Date: 2026-10-29. Human evaluation: [`EVALUATION.md`](EVALUATION.md).

## Files
- [`../../prompts/prompt-v6.md`](../../prompts/prompt-v6.md): the prompt sent (identical for the three models).
- [`../../scripts/run_models_v6.py`](../../scripts/run_models_v6.py): the harness (no secrets: the key is read from `OPENROUTER_API_KEY`).
- `svg/`: the three evaluated SVGs. `raw/`: final answers and reasoning traces. `logs/`: run summaries, per-turn cost logs, `COSTS.md`, and `transcripts/` (every model message, tool call and tool result; images are not stored in the transcripts).
- `not-evaluated/`: the first MiniMax run (it never called a tool).
- Intermediate render images and the sandbox working folders are not included.

## The tool loop
1. The prompt is the only user message. The model is offered two tools (OpenAI-style function calling through OpenRouter).
2. **`run_python(code)`**: Python 3 (standard library, numpy, Pillow) in a bubblewrap sandbox: no network, nothing outside a private temporary folder (which persists between calls of the same run), an empty `/tmp`, dropped capabilities, a clean environment without any keys, 20 s per call, memory and file-size limits, output truncated at 8000 characters. The model uses it to compute coordinates and write SVG files.
3. **`render_svg(path | svg)`**: the harness (outside the sandbox) normalizes the SVG (adds `xmlns`, `viewBox`, `width`, `height` if missing; strips `<title>`, `<desc>`, `<metadata>`), renders it in headless Chrome (through an `<img>`, so no scripts, with DNS resolution disabled) at 500×500, rotates the image by 180°, and returns **one image** with A (upright) on the left and B (rotated) on the right, **plus text diagnostics**:
   - file-contract problems (size, XML, viewBox, forbidden elements, title/desc);
   - ρ = ‖I − R(I)‖ / ‖I‖ on a 200 px grayscale render (0 = the figure looks identical upside down; a one-sided alarm only, not a score; a warning if below 0.15, and a note that it is uninformative when the page is almost all non-white);
   - the non-white fraction and bounding box of the drawing;
   - a table of the largest elements with their bounding boxes on the page and where those boxes appear in B after the half-turn (measured by Chrome).
   All three models accept image input, so the image is sent in a user message labelled "[harness output, not a person]"; only the two most recent images stay in the context.
4. The final reply (without a tool call) follows the prompt's delivery format: an `EVENT:` line, a `TITLE:` line and the complete SVG in one ```xml block. The harness extracts, normalizes and saves it.

## Limits
- At most **5** `render_svg` calls, **12** tool calls in total, **16** turns, and **US$0.25** per model. A render that fails does not count.
- When a budget is used up, the harness sends one notice ("Deliver now…") containing the last rendered SVG, and the next call is made without tools. An empty or SVG-less final reply is requested once more. Wall-clock limit per run: 30 minutes.
- Max tokens per turn: DeepSeek 20000; GLM 32000; MiniMax 32000 (first run) and 64000 (re-run).

## Models and settings (as in round 3, through OpenRouter)
| Model | Reasoning | Max tokens per turn |
|---|---|---|
| `deepseek/deepseek-v4.1-flash` | disabled (`reasoning.enabled=false`), as in round 3 | 20000 |
| `z-ai/glm-5.3-flash` | effort medium | 32000 |
| `minimax/minimax-m3.1-flash` | effort low | 32000, then 64000 for the re-run |

Providers were not pinned: DeepSeek was served by three different providers over the turns (CoreWeave, Together, Wafer), GLM by InferenceNet and MiniMax by Parasail.

## The MiniMax re-run (a declared selection)
In the first run (32000 tokens per turn) MiniMax spent all 32000 tokens of its first turn on reasoning (`finish=length`) with no content and no tool call; the harness forced a final answer, which produced a valid SVG without any render. Since the condition under test is "with tools", **one** re-run was made with only the per-turn limit changed (64000). The re-run did use the tools (11 calls, 5 renders) and is the MiniMax result in the evaluated set; the first run is kept as an extra. This is a selection between two runs and should be reported as such.

## Differences between prompt v5 and prompt v6 (declared confounds)
Besides the tools (Section 9, the 5-render limit, the harness notice):
1. The `[PLACEHOLDER …]` production note, the "public domain" assertion and the two unverified Whistler descriptions (Section 6b) were removed and replaced with a short paragraph of genre principles (shared eyes; hair ↔ beard; hat ↔ collar; smile ↔ hat band; a stroke can serve three roles; ears stay at eye level; accessories can swap places).
2. The dictionary states the frame precisely: a stroke that is a feature of A at page height y_A is a feature of B at y_B = 1000 − y_A **in B's own upright frame** (round 3 said "as seen on the page"); the table header was corrected.
3. The title is written "OHO!" (the form in museum and catalogue records), not "¡OHO!".
4. Stage 2 keeps v5's written rotation of coordinates (at least three strokes) and adds a render and a "read it blind" step (say what you see in A and in B before comparing with your intention); the "without any tools" paragraph became a short symbolic-check note; the stop rule "5 rounds" became "5 renders".
5. Section 9 (about 350 words) and a statement that only the harness sends messages besides tool results.

Unchanged: the task, the priority order (reversibility, contrast, light touches), the file contract (300 KB, no text, gradients or filters), the canon and dictionary values, the delivery format.

**Consequence:** the effect of the tools cannot be separated from the effect of these prompt changes, and the round cannot be compared with round 3 without caveats (one run per model, one evaluator who is also the author, DeepSeek without reasoning, MiniMax selected between two runs, providers not pinned).

## Design review by David
Before the round, David (Peter's Hermes agent), in a "critic" role, reviewed the prompt and the harness: [`../../docs/reviews/review-6-round4-design.md`](../../docs/reviews/review-6-round4-design.md). It did not review the outputs.
- **Applied:** normalize before rendering and fix a Chrome screenshot race; failed renders are not counted; explicit messages on forced-delivery paths, no `tools` on forced turns, an empty or SVG-less final reply is requested again with the last rendered SVG pasted in; one user message for all images, labelled as harness output; only the last two images are kept; reasoning tokens and provider are logged; ink thresholds unified and a guard on ρ; the element bounding-box table; a stop-notice statement in the prompt; three strokes of written arithmetic restored; the dictionary header and one "three-role stroke" sentence restored; dropped capabilities and more memory in the sandbox.
- **Not applied:** pinning providers; `ulimit -u` (it would count all of the user's processes); restoring "¡OHO!"; a control run of prompt v5 with tools (left as future work).

## Note added after the round: hardening of the harness
The runs above were made with the harness of commit `07d7ff8`. The harness in this repository was hardened afterwards (sanitized SVG, Chrome inside bubblewrap, pre-call cost estimate, structured API-failure log, the model's SVG saved verbatim, no silent overwrite; requires `defusedxml` as well). Prompts, tools, limits and settings are unchanged and the round-4 outputs were **not** regenerated. What the earlier version did and did not isolate: [`../../docs/security.md`](../../docs/security.md). The cost cap is an approximate operational limit and the turn bound is `MAX_TURNS + 2 = 18` calls (observed maximum 14; this round used 10 to 12): [`../../docs/reproduction.md`](../../docs/reproduction.md).

## Sandbox safety
Model code runs only inside bubblewrap (network off, isolated namespaces, read-only system files except the working folder, clean environment). Chrome opens the model's SVG only through an `<img>` or, for the bounding-box table, inline without `<script>` and `on*` attributes and with DNS disabled. The API key stays in the harness and never enters the sandbox.

## How to rerun
```bash
export OPENROUTER_API_KEY=...
NOREASON=1 MAXTOK=20000 python scripts/run_models_v6.py runs/r4 prompts/prompt-v6.md deepseek/deepseek-v4.1-flash
EFFORT=medium MAXTOK=32000 python scripts/run_models_v6.py runs/r4 prompts/prompt-v6.md z-ai/glm-5.3-flash
EFFORT=low MAXTOK=64000 python scripts/run_models_v6.py runs/r4 prompts/prompt-v6.md minimax/minimax-m3.1-flash
```
Requires Pillow, numpy, defusedxml, headless Chrome/Chromium and bubblewrap (versions: `requirements.txt`).
