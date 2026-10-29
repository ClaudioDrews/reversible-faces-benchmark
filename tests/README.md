# Tests

No paid model call, no network, no API key is needed. Everything uses fixtures or a scripted fake API
(`scripts/mock_openrouter.py`).

```bash
pip install -r requirements.txt            # Pillow, numpy, defusedxml
python -m unittest discover -s tests -v    # plain unittest; nothing else needed
# or, if you have pytest (requirements-dev.txt):  pytest tests
```

| File | What it checks |
|---|---|
| `test_validate_svg.py` | `fixtures/valid/*` pass; every `fixtures/invalid/*` fails for the expected reason, including the three cases of the external review (`<use href="https://...">`, 12x23 dimensions, SVG animation); size limit; CLI exit codes, `--strict`, `--json` |
| `test_svg_safety.py` | the sanitizer neutralizes scripts, `on*`, `foreignObject`, external `href`/`url()`, animation, DTD/entities, `<use>` cycles and expansion bombs; output is idempotent; all round SVGs sanitize without errors |
| `test_render_sandbox.py` | (skipped without `bwrap` + Chrome) the render sandbox has no network, no home/workspace/keys, a read-only root; refuses to run without bwrap; a hostile SVG renders only its safe part; the committed round-4 preview is reproduced |
| `test_budget_and_dirs.py` | the defensive pre-call cost estimate (counts reasoning details, tool schemas, images), max_tokens lowering, a missing provider cost derived rather than counted as free, overrun recording, `<svg>` head normalization, refusal to overwrite output, timestamped output, structured API-failure log |
| `test_harness_offline.py` | both runners end to end against the fake API: normal run, hostile SVG, recovery turns (14 calls observed, bound 18), tool limit, cost precheck, API failures, original-vs-normalized saved separately, no silent overwrite |
| `test_perceptual.py` | the perceptual diagnostics (rho etc.) are advisory and separate from the structural validator |
| `test_existing_svgs.py` | the audit in `docs/validator-audit.md`: no existing SVG fails the new validator; three round-2 files carry title/desc warnings |
| `test_baselines.py` | the 11 baseline SVGs meet the file contract; every baseline folder has its README/evaluation or prompt and an image; previews exist for all 15; the caveats are present; no machine paths or keys in the baseline docs |

`fixtures/invalid/` are deliberately hostile or non-conforming files. They are only ever parsed or sanitized; never open
them in a browser outside a sandbox.
