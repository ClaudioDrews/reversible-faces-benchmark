# Security: handling model-written SVG

**Model output is untrusted input.** An SVG can carry scripts, event handlers, external references (`<use href>`,
`<image>`, CSS `url()`/`@import`), animation, a DTD with entities, or a `<foreignObject>` that embeds HTML. The harness
and the preview script render such files in a browser engine, so they must not hand it raw model output.

This page describes the current design, what the round-4 harness did before it, and what is still not covered.

## What happened in round 4 (version before hardening)

Round 4 ran with the harness of commit `6747499`. An external pre-publication review pointed out two weaknesses in it:

1. Headless Chrome was started with `--no-sandbox` **directly on the host**, outside the bubblewrap sandbox that
   isolated the model's *code* (`run_python`). A bug in the renderer would have run with the user's privileges.
2. For the per-element bounding-box table the harness pasted the model's SVG **inline into an HTML page** after removing
   `<script>` elements and quoted `on*=` attributes with regular expressions. That is not a sanitizer.

Mitigations that did exist: the main picture was drawn through an `<img>` element (scripts in an SVG used as an image
do not run, and it cannot load external resources); DNS was disabled (`--host-resolver-rules=MAP * ~NOTFOUND`); Chrome
got a throw-away profile directory. What the audit of the outputs shows: every delivered round-4 SVG uses only `svg`, `g`,
`path`, `circle`, `ellipse` and `rect` ([`validator-audit.md`](validator-audit.md)), so none of the round-4 files exercised
these weaknesses, and the round results are unaffected. The exposure was in the tool, not in the data, and it is closed
from this version on. **The round-4 runs were not repeated** (no paid calls were made for this fix).

## Current design (defence in depth)

1. **Parse safely.** `scripts/svg_safety.py` parses with `defusedxml` (no DTD, no entities, no external resolution) and
   rejects outright: input larger than 300 KB (checked before parsing), a DTD or entity declaration, XML that does not parse, a root that is not `<svg>` in the SVG
   namespace, more than 20,000 elements, nesting deeper than 64, `<use>` cycles, `<use>` expansion beyond 200,000 elements.
2. **Rebuild from an allowlist.** The sanitizer does not "remove the bad parts" of the original text; it builds a new tree
   containing only allowlisted elements (`svg g defs path circle ellipse rect line polyline polygon use symbol clipPath mask
   title desc`, plus gradients, which the contract forbids but which are harmless to draw) and allowlisted attributes. It drops:
   scripts, `on*` attributes, `<foreignObject>`, `<image>`, `<a>`, `<iframe>`, `<style>` (its rules are ignored), `<metadata>`,
   animation (`animate`, `animateTransform`, `animateMotion`, `set`), any `href`/`xlink:href` that is not `#id` on a `<use>`,
   any `url(...)` that is not `url(#id)`, `@import`, scheme strings (`javascript:`, `data:`, `http:`...), CSS escapes
   and comments, foreign-namespace elements and attributes (`inkscape:` etc.), and the `filter` attribute. It is serialized
   without namespace prefixes, so the same text is valid as a standalone file and as inline SVG.
3. **Embed with a Content-Security-Policy.** The page that Chrome loads says `default-src 'none'` (images only as
   `data:`). The one script, the harness's own bounding-box script in the element table, is allowed by its hash only.
4. **Run Chrome inside bubblewrap** (`scripts/safe_render.py`): every namespace unshared (so **no network at all**), all
   capabilities dropped, a cleared environment (no API key; `HOME` points to a scratch folder inside the temporary directory), uid/gid 65534 inside
   the sandbox (never uid 0), `/usr` read-only, the root read-only, `/workspace` and the user's home **not mounted**, and only a
   fresh temporary directory (as `/work`) plus the in-memory `/tmp` and `/dev/shm` writable (they vanish with the process). Chrome's own sandbox is disabled
   (`--no-sandbox`) because it cannot nest inside bubblewrap; bubblewrap is the sandbox. Limits: 60 s wall clock, 90 s CPU,
   100 MB file size, and bounded input (300 KB, 20,000 elements). **There is no memory limit**: Chrome reserves tens of GB of
   virtual address space, and `ulimit -v` made it fail at every value tested up to 32 GB. Use a container or VM with a memory
   limit if that matters. If `bwrap` is missing the renderer **refuses to run** (`RFB_ALLOW_UNSANDBOXED=1` overrides this for SVG
   you wrote yourself; the harness never sets it).
5. **Files keep their evidence.** The model's SVG is saved verbatim (`<model>.original.svg`, `render-N.original.svg`);
   the normalized delivered file is `<model>.svg`; the copy renderers use is `<model>.sanitized.svg` / `render-N.svg`. The
   cost log records the validator's findings and what the sanitizer removed. A hostile file is therefore preserved, flagged and
   never opened raw.
6. **Same path everywhere.** `render_preview.py` and the harness both call `safe_render`; there is no other renderer in the
   repository (a `grep` for `no-sandbox` finds only `safe_render.py`, plus historical mentions in the documentation).

The code-execution tool (`run_python`) was already in bubblewrap (no network, private temp dir, 20 s, memory and file-size
limits, cleared environment); it is unchanged except that it now returns an error instead of running if `bwrap` is missing.

## Tested

`tests/test_svg_safety.py`, `tests/test_render_sandbox.py` and `tests/test_harness_offline.py` (no network, no cost): hostile
inputs are neutralized; inside the sandbox command, the network is unreachable, `/workspace`, `/home`, `/root` do not exist,
the API key is not in the environment, `/usr` and `/etc` are not writable, `/work` is; rendering refuses without bwrap; a hostile
SVG still renders its harmless part; a hostile run through the whole harness leaves no script in `render-N.svg`.

## What this does not cover

- **A Chrome or kernel vulnerability.** bubblewrap shares the host kernel and no extra seccomp filter is installed here (a custom one is a possible hardening); a kernel exploit
  from inside Chrome would escape. Run the repository in a VM or container if the SVGs come from sources you do not control.
  The sandbox needs unprivileged user namespaces.
- **Content-level abuse that is not code:** very expensive but valid drawings (CPU time is bounded by the limits above;
  the element and `<use>` caps help), offensive imagery, or text hidden in path shapes. The prompt forbids text; a human
  judges the image.
- **Prompt injection through model output** into the *model's own* loop (tool results are labelled "[harness output, not a
  person]", but a model can still be misled by what it reads). The sandbox limits the damage to the temporary folder.
- **API-key handling:** the key lives only in the harness's environment; it is not passed to Chrome or to `run_python`. Do not
  paste it into prompts, files or logs. (`grep -r "sk-or"` is part of the pre-commit checks in `docs/reproduction.md`.)
- **What the validator does not judge.** Contract-valid SVG can still hide content (`display:none`, `opacity:0`: reported as a
  warning, not an error) or use a `<style>` element (also a warning: the safe renderer ignores it, so a browser may draw the file
  differently from the preview). Colours are not part of the contract (flat fills and a small palette are allowed by the prompt).
  `--strict` turns every warning into a failure (the default run does not: hidden content does not change what a human sees in the render, which is what is judged).
- **The validator is not a general SVG security scanner.** It enforces an allowlist suited to this benchmark's file contract.
  Use the sanitizer, not the validator, before showing a file to anything.
