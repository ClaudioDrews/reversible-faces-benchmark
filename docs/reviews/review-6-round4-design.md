# Review 6: design of round 4 (prompt v6 and the tool harness)

Verbatim review (English) by the second agent (a Hermes agent in a "critic" role) of the draft prompt v6 and the draft harness, before round 4 was run. Line references (p6, h) are to those drafts. It did not review the round's outputs. What was applied is listed after the review and in [`rounds/round-04/SETUP.md`](../../rounds/round-04/SETUP.md).

Operation interrupted: waiting for model response (402.9s elapsed).
s are ±2 — I read the source without numbering, anchors quoted so you can find them).

1. PROMPT v6

Dictionary fix (p6:83) — correct. "B's own upright frame" + "page height y_A appears at 1000 − y_A in B's frame" is exactly right (rotate the page: page y → 1000−y in the viewing frame; page 680 → B-frame 320 = hat band, consistent with the Stage-1 example at p6:28). Two leftovers:
- The shorthand "at height −y" still assumes y is a signed offset from 500, while the table's "page y" column holds unsigned values (680, 320). Apply "−y" literally to 680 and you get −680. Replace the shorthand with "B-frame height = 1000 − page height" plus one worked row.
- The prose fix never reaches the table: the header at p6:~85 is "| in A (page) | is in B |". Change it to "in B (its own upright frame, y = 1000 − y_A)". That header is where the original confusion lived.

Other mislead risks:
- p6:3 "no help from a person" conflicts with the harness, which injects two user-role messages ("Cost limit reached…", "Deliver now…", h:230/237 and h:189-191). Say instead: "the harness may send you one stop notice; nobody else speaks."
- p6:198 "After that the tools stop answering" — they don't stop; they answer with a refusal string. Harmless but it teaches the wrong expectation.
- p6:25 + p6:37 ("deliver the version you last rendered"): if the model wrote draft.svg via run_python, it cannot read it back — PY_OUT=4000 chars truncates any 6 KB SVG. So "deliver what you saw" is not executable. Either raise PY_OUT to ~20000 or (better, see §5) have the harness paste the last rendered SVG into the forced-final message.
- p6:196 rho gloss is safe; the harness string "same face twice?" is an interpretation, not a leak, but models will optimize it (see §3).
- Removal of the Stage-2 arithmetic (old item: "for each stroke write A point → R(p) → what it is in B") removes the only cheap, deterministic check and replaces it with a probabilistic one (30 fuzzy pixels) under a hard 5-render cap. Combined with deleting the "no-tools" paragraph (which carried the load-bearing heuristics "B sits at 1000 − page y" and "use the midpoint where A and B conflict"), Stage 2 is now weaker than v5 in the one place that matters. Keep 3 strokes of arithmetic, not 6.
- 6b removal: wise on the unverified public-domain/Whistler-description grounds (both the legal claim and the "must be verified by Cláudio" note were liabilities). But it is falsifiable as a pure improvement: the deleted text was the only material showing (a) three-role strokes ("cheeks stay cheeks — highlight becomes eye pouch"), (b) ear/eye-level invariance, (c) accessory permutation (badge ↔ flower). The replacement keeps shared eyes, hair↔beard, hat↔collar, cup↔dome and "accessories carry the identity", so mechanisms mostly survive — except (a). Net effect: a real confound vs round 3, plus Stage-1 item 3 is now the single worked template, so all three models will converge on smile→hat band / hair→beard / bowtie→pompom. Diversity drops, and the benchmark drifts from "invent a mapping" to "execute the given mapping". Recommend: keep the deletion, restore one unattributed principle sentence about inert/three-role strokes, and log the change as a declared confound.
- "¡OHO!" → "OHO!" (p6:11): a factual regression, and the inverted marks are themselves the joke (¡ and ! swap under rotation). The file is already non-ASCII (—, ∪, °), so there was no encoding reason. Also "collected in" is odd; it's his own book. Suggest "his 1946 book ¡OHO!".

2. HARNESS

Blocking bugs (fix before any run):

a) Render race, h:56: `chrome --headless --screenshot` with no `--virtual-time-budget` — the screenshot can fire before the `<img>` decodes, giving a blank/white pair. The model then "sees" nothing and rewrites good geometry. Add `--virtual-time-budget=3000 --run-all-compositor-stages-before-draw --force-device-scale-factor=1`, then assert the PNG isn't ≥99% white and assert size == 500×500 (otherwise `comp.paste` misaligns).

b) Normalize before rendering, not after. h:200-207 renders the model's raw file; h:~250-262 injects xmlns/viewBox/width/height and strips title/desc only on the delivered copy. An SVG without viewBox rendered into `<img width=500 height=500>` is *cropped*, not scaled — the model gets a cropped picture and will "fix" correct geometry, then the scored file silently gets a viewBox. One `normalize(text)` used by both paths. Related: the header rewriter at h:~252 adds `width="1000" height="1000"` when only `height=` is present → duplicate attribute → ET parse fails and a broken file is delivered. Self-closing `<svg …/>` also yields `<svg … / viewBox="…">`. Fix per-attribute.

c) Termination branch with no message, h:232: `if renders >= MAX_RENDERS and not force and toolcalls >= MAX_TOOLCALLS - 0` sets `force` but appends nothing — the model silently gets `tool_choice:"none"` on the next turn, so it may answer "done" instead of EVENT/TITLE/SVG. Also `- 0` is dead. Append the same "Deliver now…" text.

d) Empty final accepted, h:178-179: `final_text = m.get("content") or ""` then `break`; `"" is not None`, so no forced final → empty deliverable, cell lost. Treat empty or SVG-less text as no final.

e) `tool_choice:"none"` + `tools` still present (h:152-153): several routes (DeepSeek, MiniMax, some GLM providers) 400 on that combination. Drop the `tools` key entirely on forced turns.

f) A failed render burns budget: `renders += 1` (h:198) precedes the try; a Chrome crash or the path check failing costs the model one of five. Decrement in the except.

g) `name = model.split("/")[1]` (h:130) breaks on `:free`/`:nitro` slugs and collides on shared tails; sanitize the full slug.

Message ordering / images (h:181-227): all tool results are appended, then *each image as its own user message*. Consequences: (i) three renders in one turn = three consecutive user messages — MiniMax and some GLM routes reject or merge those; (ii) the image is detached from the tool result it belongs to, so the model can't tell which render the numbers describe if it rendered twice; (iii) images are user-role, reinforcing the "a person is talking" confusion against p6:3. Fix: one single user message containing all image parts, each preceded by its "render N: A left, B right" text part, and labelled "[harness output — not a person]".

Reasoning/cost/quota:
- `reasoning_details` echo (h:174) is right for providers that require signed thinking back, but it re-sends the whole thinking text every turn; with 5 retained images this is the main cost driver against the $0.25 cap. Drop all but the last 2 images from `msgs`.
- `reasoning: {"effort": …}` (h:135) is silently ignored by models that don't support it, so "GLM medium / MiniMax low" may not be reproducible. Log `usage.completion_tokens_details.reasoning_tokens` per turn as proof (also for the NOREASON cell).
- No `provider` pin: OpenRouter can route different turns to different hosts/quantizations, which also breaks `reasoning_details` signature validation. Pin with `provider: {allow_fallbacks: false, order: [...]}` and log `r["provider"]`.
- `max_tokens: 32000` on every turn (h:136): if a route caps lower you get a 400, three retries, then `api_failure` with no artifact. Clamp per model and retry once with a reduced `max_tokens`; also flag `finish_reason == "length"` (a truncated tool-call argument becomes `args={}` → `run_python("")`).

Sandbox:
- Preflight: `env -i PATH=/usr/bin bwrap --unshare-all --ro-bind /usr /usr … python3 -c "import numpy, PIL.Image"`. If numpy lives in a venv, the `--ro-bind /usr` sandbox has no numpy and the tool description in p6:195 is a lie.
- `ulimit -v 2000000` (h:91) is tight for numpy/OpenBLAS VA reservations → spurious MemoryError; 4 GB or a cgroup.
- Add `ulimit -u 64`, `--cap-drop ALL`, and `--unshare-net` explicitly (unshare-all covers it, but be explicit).
- `ulimit -f 20000` is 512-byte blocks = 10 MB; a model dumping a PNG hits it with no clear error.
- The `--no-sandbox` Chrome reads the model's SVG. That's acceptable *only* because it's loaded via `<img>` (restricted static mode: no scripts, no subresources, so `file:///etc/passwd` and http refs are dropped). Never switch to inline/`<object>`/iframe. Still bind the render to a network-isolated Chrome (`--host-resolver-rules="MAP * ~NOTFOUND"`).
- Path check h:204-206 (`work.resolve() not in sp.parents`) is symlink-safe. Good. Don't relax it.
- Chrome `timeout=60` kills the child but leaves the `--user-data-dir` default profile contention if two models run concurrently — give each run a `--user-data-dir` in tmp.

Provider quirks to spot-check with one throwaway call each before the round: base64 `data:` image acceptance (DeepSeek routes vary; some want a URL), `role:"tool"` with `content` as a plain string (ok everywhere), assistant `content: ""` alongside `tool_calls` (DeepSeek accepts, some clones reject — use `null` on error), and `tool_choice:"none"`.

3. DIAGNOSTICS

- rho: valid only as a one-sided alarm. Low rho ⇒ symmetric ⇒ broken is sound; high rho ⇒ no information. It is area-normalised and dominated by big masses, so it is least sensitive to exactly the failure mode you care about (one missing B feature) — a 30-px stroke hardly moves it. It is gameable (one asymmetric speck), and false-positives on a dark-filled page (ink ≈ 255 everywhere ⇒ rho ≈ 0 ⇒ "same face twice"). Guard: skip the warning when ink fraction > 0.8. Do not use rho as a score.
- ink fraction: only an emptiness/blob detector, not a style or quality signal. Two inconsistent ink definitions sit on adjacent lines (`dark = g<140` for frac, `g<200` for bbox) — the model sees "ink 0.02" next to a bbox covering most of the page. Unify or explain.
- bbox: genuinely useful — it is the only thing detecting "cropped", "tiny", "in a corner", which is a live failure given the missing-viewBox bug. Its ×5 scaling is valid only for the 200-grid; it says nothing about B and nothing about faces.
- One extra cheap diagnostic (recommended): an element bbox table — for the top-level children of the root (cap 8 rows), print `id/type, bbox (x0,y0,x1,y1), bbox centre after R(p)`. This is the arithmetic Stage 2 no longer makes the model do, it is measured rather than eyeballed, it is non-leaking (it is the model's own drawing), and it directly hits the failure mode "this double-duty stroke lands on a face feature in the other reading". Implementation: one extra headless pass with `--dump-dom` after inlining the SVG with `<script>`/`on*` stripped, computing `getBBox()` per child.
- Fallback if getBBox is too much work: a 3×3 ink grid (9 integers). Cheaper, still fine for "mass drifted to the top row", but weaker for the actual failure.

4. COMPARABILITY / VALIDITY

Changed beyond tools: (i) Stage 2 method (deterministic arithmetic → read-the-render); (ii) deletion of the no-tools paragraph, which carried the "B at 1000 − page y" rule and the "use the midpoint where A and B conflict" compromise — probably load-bearing for round 3; (iii) 6b replacement; (iv) ¡OHO! → OHO!; (v) §9 adds ~350 words of instructions (more prompt tokens, new framing); (vi) stop rule "5 rounds" → "5 renders", now externally enforced; (vii) MAXTOK=32000/turn × 16 turns (v5 was one turn — a model can now spread the SVG across turns and truncate); (viii) harness user-role messages; (ix) delivered SVG post-processed (xmlns/viewBox/width injection, title stripping) while the rendered one is not — verify round 3 did the same, or models that omit viewBox now get it free.

Threats: ceiling effect is the big one — round 3 already restored B for all three, so pass/fail cannot improve; n=3 is not evidence. Single worked example (p6:28) plus rho warning ⇒ convergence. No seed, no provider pin, model build drift ("flash-1017"). The blind-read scaffold is a new capability substitute that cannot be separated from the 6b deletion.

Cheapest fix with real payoff: score render-1.png under the round-3 rubric, per model. Render 1 is the plain skeleton — i.e. the round-3 artifact — so you get a within-run, within-model "compose" measure alongside the "repair" measure, with zero extra API cost, and the ceiling problem disappears. Also pre-register one secondary metric (1-5 human rating of each reading, rater blind to condition) before the run.

5. TOP 5 EDITS (priority)

1. Normalize before rendering + kill the Chrome race + blank/size assertion (h:50-59, h:200-207, h:~250). Without this the feedback channel is unreliable and the scored SVG isn't the rendered SVG. Nothing else matters until this is fixed.
2. Fix the termination paths: message on the renders/toolcalls branch (h:232), drop `tools` instead of `tool_choice:"none"`, treat empty content as no-final (h:178), clamp/retry `max_tokens`, handle `finish_reason=="length"`, and paste the last rendered SVG into the forced-final message.
3. Image/message plumbing: one user message with all images, labelled "[harness output, not a person]", drop all but the last 2 images, refund a render on exception (h:198).
4. Prompt: restore 3 strokes of mandatory arithmetic in Stage 2 (p6:32); label the dictionary table column "in B (its own upright frame)" and replace the "−y" shorthand with an example (p6:83); fix p6:3 to acknowledge the harness stop notice; raise PY_OUT or tell the model how to round-trip its file.
5. Add the element-bbox-after-rotation table to diagnostics; record the v6 prompt edits as declared confounds; score render-1.png under the round-3 rubric; and if budget allows (it does: ~$0.75 max), add the prompt-v5 × tool-loop cell so the tool effect is separable from the prompt edits.

Preflight before spending anything: bwrap numpy/PIL check, one image round-trip per provider, and one `max_tokens=32000` smoke call per model.

## What was changed in response

- **Applied:** normalize the SVG before rendering and fix the Chrome screenshot race; a failed render does not use up a render; explicit messages on forced-delivery paths; `tools` dropped on forced turns; an empty or SVG-less final reply is requested again with the last rendered SVG; one user message for all images, labelled as harness output; only the last two images kept; reasoning tokens and provider logged; ink thresholds unified and a guard on ρ; the element bounding-box table; the stop-notice wording in the prompt; three strokes of written arithmetic restored in Stage 2; the dictionary header and the "−y" shorthand fixed; one sentence on three-role strokes restored; `--cap-drop ALL` and a larger memory limit in the sandbox.
- **Not applied:** pinning providers (OpenRouter routing varied for DeepSeek, which is recorded instead); `ulimit -u` (it counts every process of the user); restoring "¡OHO!" (museum and catalogue records use "OHO!"); the control cell of prompt v5 with tools (listed in `docs/future-work.md`).
- **Declared as confounds:** the removal of Section 6b, the frame wording, the title, the Stage 2 change (see `rounds/round-04/SETUP.md`).
