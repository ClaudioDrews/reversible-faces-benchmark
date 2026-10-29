# Review 7: the hardening of the scripts (after an external pre-publication review)

**Reviewer:** David (Peter's Hermes agent; the only model calls made for this work). **Material:** the new and
rewritten scripts (`svg_safety.py`, `safe_render.py`, `validate_svg.py`, `rfb_common.py`, both runners, `render_preview.py`)
and `docs/security.md`, inlined in the query. Two passes: a first review of the patch, and a second pass that checked how his
points had been handled. This page keeps his points in short form and what was done with each. He reviewed the code as text; it
was not run by him. It is his opinion, not ground truth.

## First pass

What he found correct: the sanitizer's core design (defusedxml, DTD/entity rejection, root-namespace check, rebuild instead of
regex surgery, escaped attributes, dropping style/script/animation/foreignObject/image and non-local references), the `<use>`
expansion check, data-URI `<img>` rendering with a hash-pinned CSP, the bubblewrap flag set and the refusal to run without it,
the exact `viewBox`/`width`/`height` check (the 12x23, animation and external-`<use>` cases), the structured `api-errors.jsonl`,
originals kept verbatim, and no silent overwrite.

| # | His point | Severity | What was done |
|---|---|---|---|
| 1 | The pre-call cost estimate ignored `reasoning_details` (re-sent every turn) and the tool schemas | blocker | Fixed: the estimate counts the full JSON of each message and the tools; the provider-reported prompt size is a floor from the second call on |
| 2 | A missing `usage.cost` read as free, so the cap never fired | blocker | Fixed: cost derived from tokens x price (`cost_source: derived`), or the pre-call estimate if there are no token counts; test with a fake API that omits the cost |
| 3 | The 300 KB limit was not applied on the sanitize/render path | should fix | Fixed: `parse()` rejects larger input before parsing (and before encoding a `str`); harness file reads use the same limit |
| 4 | No memory limit for Chrome | should fix | Not fixable that way: `ulimit -v` made Chrome fail at every value tried up to 32 GB. Documented; input bounded (300 KB, 20,000 elements); advice to use a container with a memory limit |
| 5 | The validator accepts hidden content (`display:none`, `opacity:0`), a `<style>` element, and does not check colours | should fix | Partly: hidden content is now a warning (for attributes and for `style`), with fixture and test; `<style>` stays a warning (documented; `--strict` fails on it). Colours are **not** validated: the prompt allows flat fills and a small palette |
| 6 | Ids and references had to start with a letter | should fix | Fixed (fixture `numeric_ids.svg`) |
| 7 | `run_models.py` normalization broke self-closing roots and a missing `height`, and mishandled `>` inside attribute values | should fix | Fixed: one shared `normalize_svg_head` for both runners, with tests |
| 8 | Docs said more than the code does (`HOME`, writable `/tmp`, the 18-call bound ignoring retries, "limits did not change") | should fix | Fixed in `docs/security.md`, `docs/reproduction.md` and the runner's header; the hardened runner can lower `max_tokens` and stop before a call, which the old one could not |
| 9 | Pin the sandbox uid/gid; consider seccomp | nit | `--uid 65534 --gid 65534` added; seccomp not added (listed as a possible hardening and as a residual risk) |
| 10 | Thin set of valid fixtures; `rho` computed and dropped; failed renders do not count as renders | nit | Valid fixtures grown from 4 to 10; the symmetry number is now recorded per render in `cost-log.json`; the render accounting is the round-4 protocol and was kept, documented (a failed render still counts as one of the 12 tool calls) |

## Second pass (on the fixes)

- Estimate: good, but only a floor from the second call on; the docstring now says it is an estimate, not a proof of an upper bound.
- Missing cost: correct and on the safe side; a free model is over-counted as "derived" (commented in the code).
- Size limit: he noted the `str` case (the length was tested after encoding) and the need for every path to go through `parse()`; both
  fixed, with a test for `str` and `bytes`.
- Memory: the dismissal was judged fair.
- Hidden content: confirmed that attributes (not only `style`) are covered; he noted it does not fail the default run. That is deliberate and
  now stated: a human judges the render, in which hidden content is not visible.
- `--uid/--gid`: he asked whether rendering still works (a single mapped uid and the working folder). It does (the whole suite and the
  pixel-identical round-4 preview run with it, and the folder is the invoking user's); the `home` folder is created by the renderer.
- `width="1000.0"`: he asked for the clause. The prompt's required opening tag is literally `width="1000" height="1000"`
  (`prompts/prompt-v6.md`, output requirements), and the external review asked for an exact contract, so non-identical values
  fail; a loosening would be a decision for the author.
- The name `rho` is the benchmark's symmetry number, not a correlation coefficient; the log key is now `symmetry_rho`.

No blocker is open after the second pass. Not done: seccomp, a memory limit, rerunning round 4 under the hardened harness.
