# Dual Interpretation Research Lab (experimental)

**Status: research prototype on a separate branch; not the public benchmark and not a demonstrated Whistler-quality generator.** Language: English. The main repository, its research results and GitHub Pages site must remain unchanged until explicit review.

## Mission

Build and test a reproducible, prompt-to-SVG method for **one coherent, carefully finished illustration that supports two different recognizable faces when physically rotated 180 degrees**. Rex Whistler's historic reversible drawings are an artistic **quality target**, not a claim of achieved fidelity. No historic images are copied into this laboratory.

The target is deliberately harder than a reversible icon: expression, personality, illustration quality, feature sharing, a coherent visual message, and reliable production under a fixed SVG contract all matter. Treat geometry, perception, and artistry as distinct evaluation endpoints.

## What is implemented now

- Interactive, offline-capable **visual diagnostics** using the existing benchmark's archived SVGs, not new model output.
- Deterministic C2 utilities, movable-centre stress tests, ink diagnostics, radial containment, feature correspondences, shared-stroke / negative-space exploration and reproducible region-ablation controls.
- A **staged prompt/plan/production** command-line harness for LLMs via a user-specified OpenAI-compatible chat-completions endpoint; it makes no external request unless explicitly enabled, never executes model-supplied code, and reuses the parent benchmark's strict SVG validator.
- A research notebook, transfer matrix, literature register, evaluation protocol and tests.

**Not implemented or not proven:** calibrated face detectors or salience maps, automatic contour ownership, reliable semantic-role graphs inferred from arbitrary art, a trained neural face recognizer, human study, art-quality optimization, automated visual critique, or a Whistler-level result. Controls labelled "hypothesis" are not measured effects.

## Run the browser laboratory

From repository root:

    python3 -m http.server 8811

Open **http://localhost:8811/lab/**. The lab reads the same local, archived \`site/data/manifest.js\` and \`site/data/art.js\` that power the current educational site; it does not mutate any source artifact. The script can also run from a checked-out experiment branch through a local static server.

The website is not automatically published from this experimental branch: the existing Pages action deploys **only site/** from **main**.

## Use the prompt-to-SVG harness

Prepare prompts and a frozen planning template (no network):

    python3 lab/agent.py prepare --brief "A triumphant inventor turns into a skeptical critic; one shared engraving, two distinct faces, wry visual joke." --out output/lab-trial-01

Then, *explicitly opt into* an external inference endpoint:

    export RFB_LAB_API_KEY="...secret..."
    python3 lab/agent.py generate --brief "..." --model "your/model" --endpoint "https://your-compatible-provider/v1/chat/completions" --out output/lab-trial-01

Do not commit credentials, private prompts, provider output logs, or artwork without checking reuse rights. The command stores prompts, raw plan text, source SVG, diagnostic results and a manifest in an ignored local output folder. It validates the final SVG but does **not** certify either face is recognizable. To get upright/rotated preview, follow the parent's sandboxed renderer instructions:

    python3 scripts/render_preview.py output/lab-trial-01/candidate.svg output/lab-trial-01/preview.png

If the required sandboxed renderer is unavailable, the preview command refuses to render; do **not** substitute an unsafe headless browser for arbitrary model SVG.

Run unit tests:

    node --test lab/tests/math.test.cjs
    python3 -m unittest discover -s lab/tests -p 'test_*.py' -v

The existing benchmark validator/dependencies are described in the root README and requirements.txt.

## Files

- \`THEORY.md\`: mathematics, semiotic graph, Gestalt hypotheses, failure modes, scope.
- \`TRANSFER-MATRIX.md\`: every identified sinogram and reversible-face idea, origin, status, test.
- \`RESEARCH.md\`: primary references, limitations and artifact policy.
- \`EXPERIMENTS.md\`: preregistration-oriented design and explicit gates.
- \`PROMPT-PROTOCOL.md\`: staged authoring, critique, repair and illustration-quality targets.
- \`schemas/design-plan.schema.json\`: proposed plan contract for a future structured generator.
- \`index.html\`, \`style.css\`, \`app.js\`, \`math.js\`: research interface.
- \`agent.py\`: optional provider-agnostic inference adapter; structural validation only.
- \`tests/\`: deterministic algebra, shape and pipeline tests.

## Evidence discipline

Mark statements as **EXACT**, **MEASURED / domain-specific**, **HYPOTHESIS**, or **NOT YET TESTED**. The Sinogram Ambigram's archived PRC geometric improvements are not face-perception improvements. Its VLM pilot and fusion-threshold results exist in separate draft PRs and are not treated as released human evidence. Never train a score on the same selected instances used to validate it.
