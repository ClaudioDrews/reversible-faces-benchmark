# Pre-publication checklist

Status of the editorial and consistency pass before the repository is published. Nothing has been pushed or published. Status values: `todo`, `in progress`, `done`, `needs Claudio's decision`.

Task list kept here so that nothing gets lost; updated as the work proceeds.

## A. Editorial and consistency tasks

| # | Task | Status |
|---|---|---|
| A0 | Write this checklist first | done |
| A1 | Replace `README.md` with the technical README (dual-interpretation synthesis, sections 1-10, no badges) and verify every path, link, model id, CLI argument and factual claim it cites against the repository | done |
| A1a | Create missing preview images from existing round artifacts (if any are missing) | done: none were missing; every image the README cites already existed under `assets/previews/` |
| A1b | Keep the math GitHub-compatible (`$...$` / `$$...$$`) | done |
| A2 | Fix the validator contradiction: check `scripts/validate_svg.py`; in `docs/threats-to-validity.md` separate historical validator limits, current validator capabilities and the impact on published results | done |
| A2a | Scan all docs for other historical-vs-current contradictions | done |
| A3 | Add `docs/README.md` navigation map by reader interest | done |
| A4 | Add `rounds/README.md` index: round, prompt, protocol, models, evaluation, results | done |
| A5 | Add to threats-to-validity / methodology: capability vs reliability vs efficiency; DeepSeek token exhaustion is a task-completion failure, not geometric incapacity; the cost budget is not a hard financial limit; round 4 ran before renderer hardening | done |
| A6 | `docs/future-work.md`: independent perceptual protocol; controlled v3/v4/v5 ablation; tools on/off; expanded composition as a variant (base task stays the reference); update `to-do.md` | done |
| A7 | `paper/`: keep v2.0 intact; `paper/README.md` states scope and that a v3.0 is planned later | done |
| A8 | Fix the README `<your-account>` placeholder to `ClaudioDrews` | done |
| A9 | Author name "Claudio Drews" (no accent) in `CITATION.cff`, `LICENSE`, `LICENSE-CONTENT`, `LICENSING.md`, README citation, paper, docs; "Claudio's Grok Bot assistant" in the Peter/David wording. Exception: the prompts v1-v5 (and quotes of them) keep the literal production note "[PLACEHOLDER — Cláudio to add and verify.]" because the models saw it | done |
| A10 | Repo-local git config `user.name` / `user.email` set to the chosen author for new commits | done |

## B. Assistant review by David (Peter's Hermes agent)

| # | Task | Status |
|---|---|---|
| B1 | Give David the new README and the changed docs (text) plus repository facts; ask for a critical consistency and accuracy review | done (one call, about US$0.01) |
| B2 | Record his feedback in `docs/reviews/review-8-prepublication.md` | done |
| B3 | Apply valid points; note rejected ones with reasons | done (2 rejected, 2 applied differently; see the review table) |

## C. Final review by Peter Weyland (Claudio's Grok Bot assistant)

| # | Task | Status |
|---|---|---|
| C1 | All links in the Markdown files resolve | done (checked by script and by the new `tests/test_docs.py`) |
| C2 | All tests pass (89 or more) | done: 94 tests pass (89 earlier plus 5 documentation tests) |
| C3 | Personal-data scan is clean | done: no keys, no machine paths, no email address in any file (one scratch path removed from a quoted review) |
| C4 | English only | done: no Portuguese text; the only non-English strings are the accented name in the verbatim prompt placeholder and quotations of it |
| C5 | Commit locally (no push) | done |
| C6 | Sync changed and new files to the Drive review folder in place | done (all changed and new files updated or created in place; folder id `1w7hkKpurPOiZm8SQMfT3H2LRmTKOa7Dn`) |

## D. Pending publication items

| # | Item | Status |
|---|---|---|
| D1 | Commit author name and email | resolved: name "Claudio Drews", email = the Proton address Claudio chose (not written in any repository file) |
| D2 | Rewrite author and committer of all commits to "Claudio Drews" with the chosen Proton address | done (`git filter-branch` env-filter; backup bundle `/workspace/rfb-backup-20261029.bundle` made first, outside the repository) |
| D2a | Update every cited commit hash after the rewrite | done: the only cited hash was the round-4 harness commit, `6747499` before the rewrite and `07d7ff8` now (12 files updated, `git show 07d7ff8:scripts/run_models_v6.py` works) |
| D3 | Expire the reflog and garbage-collect so no dangling or old commits remain | done (`git reflog expire --expire=now --all`, `git gc --prune=now --aggressive`; `git fsck --lost-found` reports nothing) |
| D4 | Annotated tag for the release | done: `v2.1.0` (the repository version in `CITATION.cff`) on the final HEAD |
| D5 | The actual push / publication | pending: Claudio must first create an **empty** GitHub repository (`ClaudioDrews/reversible-faces-benchmark`, no README, licence or .gitignore); then add it as `origin` and push `main` and the tag `v2.1.0`. Not done by the assistant. |
