# Review 5: paper and docs integration

Verbatim review (English) by David (Peter's Hermes agent), in a "critic" role, of the repository after the paper, the new docs and the README changes were integrated, followed by what was done about each point. The review also ran its own link checker, a DOI check against Crossref and a re-computation of the geometry tables; the tool-use listing printed at the top of its raw output is omitted here.

Read-only audit complete. I checked every internal link/anchor (script), validated all 14 shipped SVGs, re-computed the geometry tables, and cross-checked the cost logs and DOIs (Crossref/doi.org). No files were modified; scratch probes went to a temporary scratch directory.

WHAT CHECKS OUT (so you don't re-litigate it)
- 300 KB: consistent (README:80, docs/methodology.md:31, paper:57, all prompts, scripts/validate_svg.py:23). The 500 KB figures are only in design-history, explicitly marked superseded (docs/design-history/README.md:8–10).
- y_A = 1000 − y_B: arithmetically correct in README:100, paper:105–115, docs/geometry.md:54–64, docs/how-it-works.md:44, docs/glossary.md:18 (including the H-unit form u_A = −u_B). Every table row and every "Page-y check" verifies. The problem is wording, not math (see 1.1).
- Costs: 0.075/0.057/0.052/0.030 and 0.075/0.080/0.091/0.194 match rounds/*/EVALUATION.md and logs/COSTS.md; "roughly half a dollar" is right (~0.44 + one unreported timeout).
- No broken internal links or anchors; no missing referenced files; all SVGs pass the validator (round-2 metadata flagged, as documented).

1) INCONSISTENCIES
1.1 Frame wording — the one real contradiction. All docs say face B's heights are in B's own (rotated) frame (README:100, paper:105, docs/geometry.md:54, docs/glossary.md:18, docs/how-it-works.md:44). Prompt v5 says the opposite: "a feature of A at height y and a feature of B at height −y (as seen on the page)" (prompts/prompt-v5.md:84; same in v1–v5b), and Stage 8 mixes frames: "a feature at B-height y_B ... sits on the page at 1000 − page y" (:114). "(as seen on the page)" is false under either reading and is the only place the stimulus disagrees with the paper.
1.2 Tools. README:72 "The model may, if it can run code, check its own output" vs README:140 and paper:55 "no tools … could not run code". Prompt v5:114 also says "Without any tools", yet :188 invites iteration ("after 5 rounds").
1.3 Self-check. README:82 says the model checks "(A) both faces read, (B) artistic quality, (C) humor". The actual prompt has GATE 1 reversibility, GATE 2 contrast, GATE 3 light touches (prompts/prompt-v5.md:162–170) — no humor gate, and contrast is missing from the README.
1.4 Counting. Paper:45 "RFB differs in four ways"; docs/related-work.md:27 lists five (the fifth is the real differentiator: blind generator).
1.5 Glossary "Round" = "one batch … of one prompt version" (docs/glossary.md:22) — round 1 mixed v2 and v3 (README:115, rounds/round-01/EVALUATION.md:5–9).
1.6 docs/future-work.md:3 "They are listed in section 7 of the paper" — items 6 (diffusion) and 7 (event quality) are not in paper:190–203. Likewise docs/threats-to-validity.md:3 "the same list" — its "Models and providers change" bullet (:16) is absent from paper:179–186.
1.7 EVENT:/TITLE: is described as part of the contract in paper:57, but only exists from v4 (prompts/prompt-v4.md:217); rounds 0–1 ran v1–v3.
1.8 Dictionary overlap at y≈320–350: "A's smile (680) = B's hat band/dome (320)" and "A's hat or hair mass (200–350) = B's beard mass (650–800)" (prompts/prompt-v5.md:29; README:100 + :49). A stroke at page 320 is simultaneously B's mouth and B's beard. The table is not a partition, and nothing says so.
1.9 CITATION.cff:5 sets `version: "2.0"` for the dataset while README:24/255 use 2.0 for the paper — same number, two objects, no v1. LICENSING.md:9 says CITATION.cff has "no separate license (same as the content)" while CITATION.cff:15–17 declares MIT + CC-BY-4.0.

2) OVERSTATED / UNVERIFIED
2.1 Causal abstract. "adding event and art instructions (prompt v4) made all three models lose the 180° reading" (README:20, paper:14) is n=1 per cell, with prompt size 19→24 KB, several variables changed at once and no repeat runs. The qualifier lives in §6, not in the abstract.
2.2 "restored identifiable faces … for all three" (README:20) omits that DeepSeek ran with reasoning disabled and is "not comparable" (paper:167, :182).
2.3 Validator. "checks the file contract" (README:195, :219) is too strong: I ran an SVG with `width="10" height="10"`, `<style>` and an external `<use href="https://…">` — validate_svg.py printed OK, exit 0. It never checks width/height values or external references (scripts/validate_svg.py:17,33). Also run_models.py:101–104 injects viewBox/width/height, so the contract isn't purely the model's output.
2.4 "verified bibliography" (README:251) / "nothing was taken from memory" (docs/references.md:3): true for the 7 Crossref DOIs I re-queried (all metadata match), but 10.2312/egsh.20101039 is not a Crossref DOI (resolves at doi.org), LNCS 14189 is not independently confirmed, and [11]/[13] were not consulted — with author order flagged as "least certain" (docs/references.md:29).
2.5 The prompt's "public domain" assertion for the two Whistler works (prompts/prompt-v5.md:152) is an unverified legal claim, repeated nowhere with a caveat.

3) BROKEN LINKS / MISSING FILES
None. All relative markdown links, anchors and `<img src>` in the 13 audited files resolve. External: doi.org/10.2312/egsh.20101039 → 200; the Salisbury Museum URL (paper:235) returns 403 to scripted requests (bot wall — verify by hand); arXiv API was unavailable from here.

4) FIRST-TIME-READER CONFUSION
4.1 Three frames in play (page, rotated page, "B's own frame"), with the glossary as the only clear definition (docs/glossary.md:10) and the prompt contradicting it (:84).
4.2 The prompts are advertised as "exactly as sent" (README:185, docs/prompt-evolution.md:3) but contain an internal production note addressed to the author: "**[PLACEHOLDER — Cláudio to add and verify.]** … must be verified by Cláudio before use" (prompts/prompt-v5.md:152). run_models.py:45 sends the file whole, so the models saw it. No doc mentions this; it is both a credibility problem and a confound.
4.3 Round arithmetic: "three rounds" (README:12) vs a four-row table (:114), and paper §5 titled "Pilot rounds" containing three evaluated rounds plus the pilot.
4.4 The 300 KB limit looks meaningful but the largest shipped SVG is 8.9 KB.
4.5 In the math, A/B denote faces, while a/b denote stroke targets and R(b) a rotated target (paper:87–99) — one symbol set, two roles.

5) TOP 5 EDITS, PRIORITY ORDER
1. Resolve the frame contradiction at its source: in prompts v5 (and a footnote for v1–v5b) change ":84" to "in B's own upright frame" and rewrite :114 as "the stroke goes to page y = 1000 − (B's page y in B's frame)". Since the prompts are historical stimuli, add one sentence in README:100 and paper:105 stating that the shipped prompt used the looser wording "(as seen on the page)".
2. Deal with the placeholder: either mark the prompt files as literal archival transcripts and quote the note in README:14/paper:183 as something the models actually read (plus drop or verify "public domain"), or replace the section in a new prompt version and re-run. Right now the repo asserts both "exact prompt" and "curated docs".
3. Fix the two protocol errors a reviewer will catch first: README:72 (models could run code) and README:82 (self-check A/B/C) → no tools; Gates 1–3 = reversibility / contrast / light touches.
4. Soften the abstract to match §6: "in this single run per model, adding … coincided with all three losing the 180° reading", and add "DeepSeek with reasoning disabled, not comparable" to the "for all three" sentence (README:20, paper:14).
5. Sweep the small factual mismatches in one pass: paper:45 "four" → five; docs/future-work.md:3 and docs/threats-to-validity.md:3 ("listed in §7/§6") → "mostly"; docs/glossary.md:22 round definition; CITATION.cff version scoping + add `url`/`repository-code`; LICENSING.md:9 license wording.

## What was changed in response

- **1.1 Frame wording (prompt vs. docs).** The prompts are historical stimuli and were **not** edited. Instead the wording difference is documented: a note in the README geometry section, the paper (section 4.5), `docs/geometry.md` and `docs/threats-to-validity.md`. The docs and the paper keep the precise statement (B's heights in B's own frame, y_A = 1000 − y_B).
- **1.2 Tools.** README "may, if it can run code" corrected: the models in the rounds had no tools.
- **1.3 Self-check.** README now describes v5's Gates 1–3 (reversibility, contrast, light touches).
- **1.4 "Four ways".** The paper now says five (adds the blind generator).
- **1.5 Round definition.** Glossary corrected (round 1 mixed v2 and v3).
- **1.6 "same list".** `docs/future-work.md` and `docs/threats-to-validity.md` now say they extend the paper's lists and name the additions.
- **1.7 EVENT/TITLE.** Paper now says from prompt v4 on.
- **1.8 Dictionary overlap.** A "not a partition" note was added to the paper, `docs/geometry.md` and the threats list.
- **1.9 Versions and licenses.** README/CITATION.cff say 2.0 is the version of the repository and the paper; `LICENSING.md` says `CITATION.cff` declares MIT + CC BY 4.0.
- **2.1, 2.2 Abstract.** README and paper abstracts now say "in the single run per model, ... coincided with", mention the several simultaneous changes and that DeepSeek (reasoning off) is not comparable.
- **2.3 Validator.** README says "checks parts of the file contract"; the threats list states what it does not check. (The script was not changed.)
- **2.4 Bibliography wording.** `docs/references.md` now states exactly how each entry was checked, and that [11] and [13] were not consulted and the author order of [11] is the least certain detail. (LNCS 14189 had been confirmed on the SpringerLink chapter page.)
- **2.5, 4.2 Placeholder and "public domain" in the prompts.** README heads-up, paper and threats list now say the models read the literal production note and an unverified "public domain" claim, and that this is a possible confound. The prompts are unchanged.
- **4.3 Round count.** README says three evaluated rounds plus an unevaluated pilot.
- **4.5 Symbols.** Glossary entry explains A/B (faces) versus a/b (stroke targets).
- **Not changed:** the prompts themselves (kept verbatim); the 300 KB limit versus the 8.9 KB largest output (left as a safety cap); `repository-code`/`url` in `CITATION.cff` (no public URL decided; GitHub not touched).
