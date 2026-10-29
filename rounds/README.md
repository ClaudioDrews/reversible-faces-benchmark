# Rounds: index

One folder per round. Every round folder has `EVALUATION.md` (the human verdict, models, settings, costs, lessons), `svg/` (the evaluated SVGs), `raw/` (raw model answers and reasoning traces where available) and `logs/` (token and cost logs). Round 1 and round 4 also have `not-evaluated/` (runs that were not part of the evaluated set); round 4 also has `SETUP.md` (the tool-augmented harness and its confounds).

All rounds use the same three models through OpenRouter: `deepseek/deepseek-v4.1-flash`, `z-ai/glm-5.3-flash`, `minimax/minimax-m3.1-flash`. The evaluator is the benchmark's author (one person); verdicts are informal and there is no scoring scale. Do not pool or rank rounds with different protocols.

| Round | Prompt | Protocol | Models and notable settings | Evaluation | Result (the evaluator's verdict, summarized) |
|---|---|---|---|---|---|
| [0 (pilot)](round-00-pilot/) | [v1](../prompts/prompt-v1.md) | One-shot, no tools | All three; first end-to-end test | [`EVALUATION.md`](round-00-pilot/EVALUATION.md) (not judged by the human evaluator; reviewed by David) | Used only to improve the prompt (v2). |
| [1](round-01/) | [v2](../prompts/prompt-v2.md) (MiniMax), [v3](../prompts/prompt-v3.md) (DeepSeek, GLM) | One-shot, no tools | All three, default effort (medium); MiniMax's v3 run was interrupted, so its v2 output was evaluated | [`EVALUATION.md`](round-01/EVALUATION.md) | Effect OK for DeepSeek and MiniMax, somewhat bad for GLM; low artistic quality; no impactful use of the event. |
| [2](round-02/) | [v4](../prompts/prompt-v4.md) | One-shot, no tools | All three; MiniMax's first attempt hit the token limit, the delivered run used low effort | [`EVALUATION.md`](round-02/EVALUATION.md) | All three lost the 180° reading ("it got a lot worse"). |
| [3](round-03/) | [v5](../prompts/prompt-v5.md) | One-shot, no tools | DeepSeek **reasoning disabled** (not comparable), GLM medium, MiniMax low effort | [`EVALUATION.md`](round-03/EVALUATION.md) | Identifiable faces in both orientations for all three; artistic quality improved. |
| [4](round-04/) | [v6](../prompts/prompt-v6.md) | **Single-attempt, tool-augmented** (sandboxed Python and a render tool; at most 5 renders, 12 tool calls, 16 turns, approx. US$0.25 per model) | DeepSeek reasoning disabled, GLM medium, MiniMax low effort (re-run at 64000 tokens per turn after a first run that never used a tool); produced by the harness before the renderer hardening | [`EVALUATION.md`](round-04/EVALUATION.md), [`SETUP.md`](round-04/SETUP.md) | Reversible and well made for all three; none conveys a comic message. Not a controlled comparison with round 3. |

## Where the paper stops

The [paper](../paper/README.md) (version 2.0) covers rounds 0–3. Round 4 is documented only in the repository.

## Not in this index

The 15 comparison runs (raster image generators and more text models) are in [`../baselines/`](../baselines/README.md), kept apart from the rounds on purpose: they do not follow the same protocol and are not comparable with it.

How the prompt changed between rounds: [`../docs/prompt-evolution.md`](../docs/prompt-evolution.md). Protocol wording and rules: [`../docs/methodology.md`](../docs/methodology.md).
