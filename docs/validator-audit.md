# Validator audit of the existing SVGs

An external pre-publication review found that the original `validate_svg.py` accepted files it should reject. The
validator was rewritten (see [`security.md`](security.md)); this page records what the **new** validator says about the
SVGs already in the repository. **None of those files was modified.** Reproduce with:

```bash
python scripts/validate_svg.py rounds/*/svg/*.svg rounds/*/not-evaluated/*.svg          # errors only
python scripts/validate_svg.py --strict rounds/*/svg/*.svg rounds/*/not-evaluated/*.svg # warnings count too
python -m unittest discover -s tests -p "test_existing_svgs.py"   # the same audit as a test
```

## Result

- **18 SVGs checked** (3 pilot, 3 + 2 in round 1 incl. not-evaluated, 3 each in rounds 2 and 3, 3 + 1 in round 4 incl. the unevaluated MiniMax first run). Of these, **12 are the evaluated ones** (rounds 1 to 4).
- **0 fail** the new validator: every one has the exact `viewBox="0 0 1000 1000"`, `width="1000"`, `height="1000"`, the SVG namespace, no forbidden element, no external reference, no animation, no script or event attribute, no DTD or entity, and is smaller than 300 KB. They also pass the sanitizer without any error finding, i.e. the sanitized copy that renderers use has the same content.
- **3 carry warnings** (they fail only under `--strict`): the round-2 files contain `<title>` and `<desc>` metadata that names the event (the runner has stripped it since round 3, see the README's notes):
  - `rounds/round-02/svg/deepseek-v4.1-flash_prompt-v4.svg`
  - `rounds/round-02/svg/glm-5.3-flash_prompt-v4.svg`
  - `rounds/round-02/svg/minimax-m3.1-flash_prompt-v4.svg`

  The round-2 evaluation text is unchanged; the tooltip issue is already documented there and in the README.
- The elements used across all 18 files are only `svg`, `g`, `path`, `circle`, `ellipse`, `rect`, `title` and `desc`.

So the review's concern was about the **tool**, not about the data: the evaluated results stand as they were.

## What the old validator missed (the tool, not the data)

Run on the 30 deliberately invalid fixtures in `tests/fixtures/invalid/`, the validator of commit `07d7ff8` **accepted 18**
of them, among them the three cases from the review: `<use href="https://...">`, `width="12" height="23"` and SVG
animation (`<animate>`, `<set>`, `<animateTransform>`); also event attributes (`onload`, `onclick`), external `url()` in
`fill` or in `style`, an `<a>` link, a CSS `@import`, CSS escapes, a DTD with entities (it was rejected only when the
entity was external), an `xml-stylesheet` instruction, a non-exact size (`width="1000.0"`), and `<use>` cycles or expansion bombs. The new validator rejects all 30, each for the expected reason (`tests/test_validate_svg.py`).

## What the validator does and does not decide

- **Structure and safety only** (the file contract, and whether the file is safe to handle). It never judges how the drawing looks.
- **Perceptual diagnostics** (the symmetry number rho, the non-white fraction, bounding boxes) are in `scripts/perceptual.py`; they are shown to models in the tool-enabled run and are advisory. Nothing passes or fails on them. The benchmark's verdict is a human's.
- Warnings (`<title>`/`<desc>`, `<metadata>`, a `<style>` element, unknown attributes, hidden content such as `display:none` or `opacity:0`) do not fail a file unless `--strict` is used.
