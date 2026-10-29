# v5 costs (OpenRouter, US$)
- run A (medium): deepseek 0.0581 (truncated at 64000 tok, no SVG) + glm 0.0035 (SVG ok) = 0.0616
- run C (deepseek effort low): 0.0571 (truncated)
- run D (deepseek reasoning max_tokens=14000, ignored): 0.0268 (truncated at 30000)
- run v5b (deepseek, prompt-v5b with "Stage 2 one pass"): 0.0225 (truncated at 24000)
- run v5c (deepseek, reasoning disabled, prompt-v5): 0.0043 -> SVG used
- minimax (low): 1st attempt timed out at 900 s (cost not reported, <= ~0.04); 2nd attempt 0.0219 -> SVG used
Total reported: 0.194 (+ unknown for the timed-out request)
