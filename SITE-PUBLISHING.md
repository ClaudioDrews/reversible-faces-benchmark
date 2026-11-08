# Reversible Faces Benchmark — Interactive Site

English-first, bilingual educational site for the [Reversible Faces Benchmark](https://github.com/ClaudioDrews/reversible-faces-benchmark). Explore real benchmark drawings, rotate them through 180 degrees, compare the two interpretations, and examine the geometry and C₂ symmetry decomposition.

**Live site (after Pages is enabled):** https://claudiodrews.github.io/reversible-faces-benchmark/

## Scope

- The website's public files live in `site/`. The research documentation in the existing `docs/` directory must not be overwritten.
- `site-tools/` holds maintenance scripts and browser-level tests. They are not published.
- The site is static HTML/CSS/JavaScript with no build process, backend, or API key.
- The 33 primary visual artifacts are local copies of the benchmark's original SVG/JPEG files; the manifest maps each to its research provenance (`repoPath`).
- Reference ρ values are calculated offline and committed to `site/data/rho.json`. The interactive C₂ lab also computes ρ in the browser.
- English is the default, with Portuguese selectable via the header or `?lang=pt`. `?lang=en` always selects English.

## Local development

```bash
python3 -m http.server 8811 --directory site
# http://localhost:8811/
```

Static validation (requires Python 3 and Node.js):

```bash
python3 site-tools/check_site.py
find site/assets/js site/data -name '*.js' -type f -print0 | xargs -0 -n1 node --check
```

Optional browser checks require `pip install playwright` and a Chromium binary. To capture screenshots use `RFB_SHOTS=output/shots`. Browser tests assume the server is running:

```bash
python3 site-tools/smoke_test.py
python3 site-tools/final_validate.py
python3 site-tools/bilingual_check.py
```

## Deployment

1. Open a pull request with the site files, then merge into `main` after reviewing the diff and the validation job.
2. At **Settings → Pages**, choose **GitHub Actions** as the build/deployment source.
3. The workflow at `.github/workflows/pages.yml` runs static checks for pull requests and deploys the `site/` folder on updates to `main` or manual dispatch.

**Publishing cautions:** The benchmark distinguishes model-produced SVG source from validated/sandboxed previews. Maintain SVG source validation and avoid adding any untrusted active SVG content. The site is a visual companion, not a replacement for the methodology or the research limitations described in the repository.
