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
| D2 | Rewrite the author of the existing commits (they carry the placeholder `Reversible Faces Bot <noreply@example.invalid>`) to the author above | ready to run, not run; do it as the last step before the push (`git filter-repo --mailmap` or an equivalent history rewrite, then re-check the log) |
| D2a | After the history rewrite every commit hash changes. The docs cite commit `6747499` (the harness that produced round 4) in 10 files (`README.md`, `docs/{reproduction,methodology,validator-audit,threats-to-validity,security,future-work}.md`, `rounds/round-04/SETUP.md`, `rounds/round-04/logs/COSTS.md`, `scripts/run_models_v6.py`) and `git show 6747499:...` commands; replace them with the new hash (find it with `git log --oneline` or `git filter-repo`'s commit map) and re-run the tests | ready to run after D2 |
| D3 | Garbage collection of the dangling commit | needs Claudio's decision |
| D4 | Tagging an immutable release (e.g. `v2.1.0`) | needs Claudio's decision |
| D5 | The actual push / publication | needs Claudio's decision |
