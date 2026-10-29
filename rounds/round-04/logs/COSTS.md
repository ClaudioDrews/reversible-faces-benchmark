# Round 4 (prompt v6, tool loop): costs and settings

Costs are as reported by OpenRouter (`usage.cost`). Harness limits: 5 `render_svg` calls, 12 tool calls, 16 turns (+2 recovery turns), and an approximate operational cost cap of US$0.25 per model (see `docs/reproduction.md`; this round used the harness of commit `07d7ff8`, which checked the cap after each turn). Per-turn details (tokens, reasoning tokens, provider, cost) are in the `cost-log_*.json` files.

| Run | Model | Settings | Turns | Tool calls | Renders | Tokens in / out | Cost (USD) | Final |
|---|---|---|---|---|---|---|---|---|
| main | deepseek/deepseek-v4.1-flash | reasoning **disabled**, 20000 max tokens/turn | 11 | 11 | 5 | 137,666 / 10,633 | 0.0232 | delivered = render 5 (pixel-identical) |
| main | z-ai/glm-5.3-flash | reasoning effort medium, 32000/turn | 10 | 9 | 4 | 153,508 / 11,504 | 0.0116 | delivered = render 4 (pixel-identical) |
| first run (extra) | minimax/minimax-m3.1-flash | effort low, 32000/turn | 2 | 0 | 0 | 43,494 / 33,415 | 0.0263 | no tool call: turn 1 spent all 32000 tokens on reasoning (`finish=length`); the harness forced a final answer |
| re-run | minimax/minimax-m3.1-flash | effort low, **64000**/turn (only change) | 12 | 11 | 5 | 836,616 / 80,012 | 0.0781 | delivered = render 5 (pixel-identical) |

**Round total: US$0.139** (all four runs). Delivered runs used in the evaluated set: 0.0232 + 0.0116 + 0.0781 = US$0.113. Smoke tests of the harness before the round (about US$0.002) are not counted.

## Failures and caveats
- MiniMax's first run did not use the tools (token cap hit inside reasoning); see the re-run selection note in [`../EVALUATION.md`](../EVALUATION.md).
- DeepSeek was served by three different providers across turns (CoreWeave, Together, Wafer); GLM by InferenceNet; MiniMax by Parasail. Providers were not pinned. DeepSeek's reasoning tokens were 0, as intended.
- GLM wrapped the `EVENT:`/`TITLE:` lines in backticks; the parser was widened afterwards and GLM's `cost-log` was corrected from its raw answer.
- Files: `run-*.log` are the harness's console summaries; `transcripts/*.jsonl` are the full message and tool logs (images are not stored in them). The first MiniMax run is under `../not-evaluated/`.
