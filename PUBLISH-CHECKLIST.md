# Pre-publication checklist

Status of the editorial and consistency pass before the repository is published. Nothing has been pushed or published. Status values: `todo`, `in progress`, `done`, `needs Claudio's decision`.

Task list kept here so that nothing gets lost; updated as the work proceeds.

## A. Editorial and consistency tasks

| # | Task | Status |
|---|---|---|
| A0 | Write this checklist first | done |
| A1 | Replace `README.md` with the technical README (dual-interpretation synthesis, sections 1-10, no badges) and verify every path, link, model id, CLI argument and factual claim it cites against the repository | todo |
| A1a | Create missing preview images from existing round artifacts (if any are missing) | todo |
| A1b | Keep the math GitHub-compatible (`$...$` / `$$...$$`) | todo |
| A2 | Fix the validator contradiction: check `scripts/validate_svg.py`; in `docs/threats-to-validity.md` separate historical validator limits, current validator capabilities and the impact on published results | todo |
| A2a | Scan all docs for other historical-vs-current contradictions | todo |
| A3 | Add `docs/README.md` navigation map by reader interest | todo |
| A4 | Add `rounds/README.md` index: round, prompt, protocol, models, evaluation, results | todo |
| A5 | Add to threats-to-validity / methodology: capability vs reliability vs efficiency; DeepSeek token exhaustion is a task-completion failure, not geometric incapacity; the cost budget is not a hard financial limit; round 4 ran before renderer hardening | todo |
| A6 | `docs/future-work.md`: independent perceptual protocol; controlled v3/v4/v5 ablation; tools on/off; expanded composition as a variant (base task stays the reference); update `to-do.md` | todo |
| A7 | `paper/`: keep v2.0 intact; `paper/README.md` states scope and that a v3.0 is planned later | todo |
| A8 | Fix the README `<your-account>` placeholder to `ClaudioDrews` | todo |
| A9 | Author name "Claudio Drews" (no accent) in `CITATION.cff`, `LICENSE`, `LICENSE-CONTENT`, `LICENSING.md`, README citation, paper, docs; "Claudio's Grok Bot assistant" in the Peter/David wording. Exception: the prompts v1-v5 (and quotes of them) keep the literal production note "[PLACEHOLDER — Cláudio to add and verify.]" because the models saw it | done |
| A10 | Repo-local git config `user.name` / `user.email` set to the chosen author for new commits | done |

## B. Assistant review by David (Peter's Hermes agent)

| # | Task | Status |
|---|---|---|
| B1 | Give David the new README and the changed docs (text) plus repository facts; ask for a critical consistency and accuracy review | todo |
| B2 | Record his feedback in `docs/reviews/review-8-prepublication.md` | todo |
| B3 | Apply valid points; note rejected ones with reasons | todo |

## C. Final review by Peter Weyland (Claudio's Grok Bot assistant)

| # | Task | Status |
|---|---|---|
| C1 | All links in the Markdown files resolve | todo |
| C2 | All tests pass (89 or more) | todo |
| C3 | Personal-data scan is clean | todo |
| C4 | English only | todo |
| C5 | Commit locally (no push) | todo |
| C6 | Sync changed and new files to the Drive review folder in place | todo |

## D. Pending publication items

| # | Item | Status |
|---|---|---|
| D1 | Commit author name and email | resolved: name "Claudio Drews", email = the Proton address Claudio chose (not written in any repository file) |
| D2 | Rewrite the author of the existing commits (they carry the placeholder `Reversible Faces Bot <noreply@example.invalid>`) to the author above | ready to run, not run; do it as the last step before the push (`git filter-repo --mailmap` or an equivalent history rewrite, then re-check the log) |
| D3 | Garbage collection of the dangling commit | needs Claudio's decision |
| D4 | Tagging an immutable release (e.g. `v2.1.0`) | needs Claudio's decision |
| D5 | The actual push / publication | needs Claudio's decision |
