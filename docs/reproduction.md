# Reproduction: environment, versions and limits

## What was tested together

| Component | Version in this repository's checks |
|---|---|
| OS / kernel | Debian GNU/Linux 13 (trixie), Linux 6.12 |
| Python | 3.13.5 (the code only needs 3.9+) |
| Pillow / numpy / defusedxml | 13.0.0 / 2.5.4 / 0.7.1 (`requirements.txt`) |
| Browser | Google Chrome **156.0.8078.47**, headless (the harness records `chrome --version` in `transcript.jsonl`) |
| Sandbox | bubblewrap 0.12.0 (needs unprivileged user namespaces) |
| Dev only | pytest 9.2.0, cffconvert 2.0.0 (`requirements-dev.txt`) |

```bash
python3 -m venv .venv && . .venv/bin/activate
pip install -r requirements.txt
python -m unittest discover -s tests -v      # no key, no network, no cost
```

Older or newer versions probably work; they have not been tested.

## What you can and cannot reproduce

- **Tests, validator, previews: yes.** `python -m unittest discover -s tests` runs everything offline. The committed
  round-4 preview is reproduced pixel for pixel by the sandboxed renderer with the Chrome version above.
- **Rendering varies.** A different Chrome/Chromium version, operating system, fonts or antialiasing can change pixels
  slightly (the tests use a small tolerance). Rendering never affects the SVG files themselves, and the benchmark's verdict is
  made by a human from the SVG. Previews are illustrations.
- **The model runs: no, not exactly.** The three evaluated models are called through OpenRouter. There are no seeds; the
  provider is not pinned (DeepSeek was served by three providers within one round-4 run); model ids can be retired or
  replaced; prices change; reasoning traces are not deterministic. A rerun will give different drawings. That is also why
  each model got a single run per prompt (with a retry only after a technical failure) and why no statistics are claimed.
- **Round 4 was produced by an earlier version of the harness** (commit `6747499`). The version in this repository is
  hardened (sanitized and sandboxed rendering, a pre-call cost estimate, structured API-failure logs, no silent overwrite). The
  prompts, tools, limits and settings are the same; the round-4 outputs were not regenerated. To inspect the exact code that
  ran: `git show 6747499:scripts/run_models_v6.py`.
- **Costs** in `rounds/*/EVALUATION.md` and `logs/` are the provider-reported figures at the time. A request that failed or timed
  out may have been billed without being reported (noted in round 3), so totals are lower bounds.
- **The cost cap is approximate.** It is an operational limit, not a guarantee: see the next section.

## The cost limit and the turn bound, exactly (`scripts/run_models_v6.py`)

- **Before each call** the harness estimates the worst case, `prompt_tokens_estimate x input_price + max_tokens x output_price`
  (the full JSON of every message, including the reasoning details that are sent back, and of the tool schemas, at 3 characters per
  token; 2,000 tokens per image; never less than the prompt size the provider reported for the previous call; prices from OpenRouter's public models list, or the environment, or a
  pessimistic default), and lowers `max_tokens` so that the estimate fits the remaining budget. If even 2,000 tokens do not
  fit, it stops without calling (`finish: cost_precheck_stop`). **After** each call it adds the provider-reported cost, or, if the provider leaves it out, a cost derived from the reported token counts (or, with no counts either, the pre-call estimate), so a missing figure is never counted as free (`cost_source` per call in `cost-log.json`). The
  estimate, the `max_tokens` actually used and the reported cost of every call are in `cost-log.json`; any excess of the
  reported total over the cap is recorded as `cost_overrun_usd`. The cap can still be exceeded by a failed request that is billed
  but not reported, by a wrong price, or by retries: each turn may make up to 3 HTTP attempts, so the 18-call bound is a bound on
  answered turns, not on POSTs (at most 54). `max_tokens` can be lowered by the estimate; the old harness never lowered it, so a run
  near the cap behaves differently from round 4.
- **Turns.** `MAX_TURNS` is 16; the loop's hard bound is `MAX_TURNS + 2 = 18` API calls. The 2 extra are the **recovery turns**:
  (1) the forced-delivery turn that follows a delivery notice (cost cap, tool budget or turn cap), where tools are removed;
  (2) one re-ask when a forced or final reply has no SVG. There is no third. Since each tool turn uses at least one of the 12
  tool calls, the observed maximum is 14 calls. A render that fails (for example because the SVG is malformed) does not count toward the 5 renders (as in round 4) but does count as a tool call, so failing renders cannot loop beyond the 12 tool calls. Round 4 used 10 to 12 (11 for DeepSeek, 10 for GLM, 12 for the MiniMax re-run,
  2 for MiniMax's first run). A wall-clock limit of 1,800 s is checked between calls; a single call can last up to 3 attempts of 600 s.

## Pre-commit checks used for this repository

```bash
python -m unittest discover -s tests
python -m py_compile scripts/*.py
grep -rInE "sk-or-[A-Za-z0-9]{10,}|Bearer [A-Za-z0-9]{20,}" . --exclude-dir=.git     # no output
git ls-files -z | xargs -0 ls -l | sort -k5 -n | tail -5                                # the largest tracked files
cffconvert --validate -i CITATION.cff                                                    # with requirements-dev.txt
```
