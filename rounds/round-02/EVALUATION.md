# Round 2: prompt v4, human-evaluated

Evaluator: the benchmark's author (Claudio Drews). Date: 2026-10-28.

Prompt v4 made the current event central and added heavy art guidance (see `../../docs/prompt-evolution.md`).

| # | File | Model | Tokens in / out | Cost (USD) | Event declared by the model | Title declared |
|---|---|---|---|---|---|---|
| 1 | `svg/deepseek-v4.1-flash_prompt-v4.svg` | `deepseek/deepseek-v4.1-flash` | 6165 / 35560 | 0.0180 | DeepSeek-R1's release (Jan 2025) and Nvidia's record ~$600B one-day market-cap drop | Rack Tower, Morning After |
| 2 | `svg/glm-5.3-flash_prompt-v4.svg` | `z-ai/glm-5.3-flash` | 6242 / 10732 | 0.0008 | Humane AI Pin launch hype (Nov 2023) and its shutdown after the flop (Feb 2024) | The Pin and the Plug |
| 3 | `svg/minimax-m3.1-flash_prompt-v4.svg` | `minimax/minimax-m3.1-flash` | 6252 / 54808 | 0.0335 | DeepSeek R1's January 2025 launch and the AI-bubble wobble that erased ~$600B of market value | Triumph and the Morning After |

MiniMax's first attempt (reasoning effort medium) hit the 64000-token limit without delivering an SVG (cost US$0.0389, raw answer in `raw/*attempt1-truncated*`); the delivered run used low effort. Cost of delivered runs: US$0.0523; including the failed attempt: US$0.0913.

## The evaluation

> "It got a lot worse. Now there is no image at 180° anymore."

All three outputs lost the reversible effect.

## Lesson

The extra load from the event requirement and the art guidance pulled attention away from reversibility. The models followed the new instructions (events, props, hatching, palette) and dropped the hard geometric part. Reversibility has to be the absolute priority: art and event come only after the double reading is guaranteed.

## Notes

- The events in the table are what each model *declared*. The repository did not fact-check them (figures such as "~$600B" are the models' wording).
- These SVGs still contain `<title>` and `<desc>` metadata naming the event (prompt v4 asked for it). It is kept here as evaluated. From round 3 the metadata is stripped.
- The previews below were rendered by the repo's script; the author's own judgment was made by viewing the SVG itself.

![Round 2 results](../../assets/previews/round-02__all-models.png)

*Top to bottom: DeepSeek, GLM, MiniMax.*
