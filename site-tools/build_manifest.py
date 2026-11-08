#!/usr/bin/env python3
"""Build site/data/manifest.json for the Reversible Faces Benchmark interactive site.

Source of truth: the benchmark repository itself (rounds/*/EVALUATION.md,
baselines/README.md, docs/*). Every metadata field below was transcribed from
those files; nothing is invented. Art files are copied from the repository.

Usage:  python3 site-tools/build_manifest.py [--repo /workspace/repo] [--out /workspace/site/data/manifest.json]
"""

from __future__ import annotations

import argparse
import json
import shutil
from pathlib import Path

MODELS = {
    "deepseek-v4.1-flash": ("DeepSeek V4.1 Flash", "DeepSeek"),
    "glm-5.3-flash": ("GLM 5.3 Flash", "Z.ai"),
    "minimax-m3.1-flash": ("MiniMax M3.1 Flash", "MiniMax"),
    "chatgpt-medium": ("ChatGPT (medium)", "OpenAI"),
    "deepseek-v4.1": ("DeepSeek V4.1", "DeepSeek"),
    "qwen3.8-omni-flash": ("Qwen3.8-Omni-Flash", "Alibaba"),
    "manus-2.0-lite": ("Manus 2.0 Lite", "Manus"),
    "gemini-3.1-pro": ("Gemini 3.1 Pro", "Google"),
    "glm-5.3-max": ("GLM 5.3 Max", "Z.ai"),
    "meta-muse-1.3": ("Meta Muse 1.3", "Meta"),
    "claude-sonnet-5.5-medium": ("Claude Sonnet 5.5 (medium)", "Anthropic"),
    "qwen-3.7-plus": ("Qwen 3.7 Plus", "Alibaba"),
    "gpt-5.6-terra-low": ("GPT 5.6 Terra (low)", "OpenAI"),
    "nemotron-3.5-lightning": ("Nemotron 3.5 Lightning", "NVIDIA"),
    "nanobanana-2.1": ("Nano Banana 2.1", "Google"),
    "qwen-image-3.0": ("Qwen Image 3.0", "Alibaba"),
    "chatgpt-images-2.5": ("ChatGPT Images 2.5", "OpenAI"),
    "grok-imagine-2.0": ("Grok Imagine 2.0", "xAI"),
}

# ---------------------------------------------------------------------------
# Rounds. Transcribed from rounds/round-0X/EVALUATION.md
# ---------------------------------------------------------------------------

ROUNDS = [
    # --- Round 0: pilot, prompt v1, NOT human-evaluated -------------------
    dict(
        id="r00-deepseek-v4.1-flash", round=0, prompt="v1", model="deepseek-v4.1-flash",
        src="rounds/round-00-pilot/svg/deepseek-v4.1-flash_prompt-v1.svg",
        art="deepseek-v4.1-flash_prompt-v1.svg",
        evaluated=False, verdict="none", reversible="unrated",
        tokens_in=4279, tokens_out=57638, cost=0.0379, settings="reasoning effort medium",
        note="Pilot: valid SVG, weak expression contrast, oval heads, budget burned on coordinate arithmetic.",
    ),
    dict(
        id="r00-glm-5.3-flash", round=0, prompt="v1", model="glm-5.3-flash",
        src="rounds/round-00-pilot/svg/glm-5.3-flash_prompt-v1.svg",
        art="glm-5.3-flash_prompt-v1.svg",
        evaluated=False, verdict="none", reversible="unrated",
        tokens_in=4332, tokens_out=22287, cost=0.0046, settings="reasoning effort medium",
        note="Pilot: valid SVG, weak expression contrast, oval heads, budget burned on coordinate arithmetic.",
    ),
    dict(
        id="r00-minimax-m3.1-flash", round=0, prompt="v1", model="minimax-m3.1-flash",
        src="rounds/round-00-pilot/svg/minimax-m3.1-flash_prompt-v1.svg",
        art="minimax-m3.1-flash_prompt-v1.svg",
        evaluated=False, verdict="none", reversible="unrated",
        tokens_in=4389, tokens_out=54317, cost=0.0329, settings="reasoning effort medium",
        note="Pilot: valid SVG, weak expression contrast, oval heads, budget burned on coordinate arithmetic.",
    ),

    # --- Round 1: prompt v2/v3, human-evaluated ---------------------------
    dict(
        id="r01-deepseek-v4.1-flash", round=1, prompt="v3", model="deepseek-v4.1-flash",
        src="rounds/round-01/svg/deepseek-v4.1-flash_prompt-v3.svg",
        art="deepseek-v4.1-flash_prompt-v3.svg",
        evaluated=True, verdict="pass", reversible="ok", artistic="low", humor="somewhat",
        event_used="not impactful",
        tokens_in=4990, tokens_out=23700, cost=0.0162, settings="one-shot, reasoning effort medium",
        note="Effect OK, low artistic quality, somewhat funny, but the current event is not used in an impactful way.",
    ),
    dict(
        id="r01-glm-5.3-flash", round=1, prompt="v3", model="glm-5.3-flash",
        src="rounds/round-01/svg/glm-5.3-flash_prompt-v3.svg",
        art="glm-5.3-flash_prompt-v3.svg",
        evaluated=True, verdict="fail", reversible="somewhat bad", artistic="low", humor="none",
        event_used="not impactful",
        tokens_in=5055, tokens_out=8111, cost=0.0034, settings="one-shot, reasoning effort medium",
        note="Effect somewhat bad; no much artistic quality.",
    ),
    dict(
        id="r01-minimax-m3.1-flash", round=1, prompt="v2", model="minimax-m3.1-flash",
        src="rounds/round-01/svg/minimax-m3.1-flash_prompt-v2.svg",
        art="minimax-m3.1-flash_prompt-v2.svg",
        evaluated=True, verdict="pass", reversible="ok", artistic="low", humor="somewhat",
        event_used="not impactful",
        tokens_in=4894, tokens_out=61524, cost=0.0373, settings="one-shot, reasoning effort medium",
        note="Its prompt-v3 run was interrupted, so the prompt-v2 output was evaluated instead.",
    ),
    dict(
        id="r01-deepseek-v4.1-flash-v2", round=1, prompt="v2", model="deepseek-v4.1-flash",
        src="rounds/round-01/not-evaluated/deepseek-v4.1-flash_prompt-v2.svg",
        art="deepseek-v4.1-flash_prompt-v2.svg",
        evaluated=False, verdict="none", reversible="unrated",
        tokens_in=None, tokens_out=None, cost=0.0193, settings="one-shot, reasoning effort medium",
        note="Superseded by the v3 run; not judged.",
    ),
    dict(
        id="r01-glm-5.3-flash-v2", round=1, prompt="v2", model="glm-5.3-flash",
        src="rounds/round-01/not-evaluated/glm-5.3-flash_prompt-v2.svg",
        art="glm-5.3-flash_prompt-v2.svg",
        evaluated=False, verdict="none", reversible="unrated",
        tokens_in=None, tokens_out=None, cost=0.0039, settings="one-shot, reasoning effort medium",
        note="Superseded by the v3 run; not judged.",
    ),

    # --- Round 2: prompt v4 — all three LOST the 180-degree reading --------
    dict(
        id="r02-deepseek-v4.1-flash", round=2, prompt="v4", model="deepseek-v4.1-flash",
        src="rounds/round-02/svg/deepseek-v4.1-flash_prompt-v4.svg",
        art="deepseek-v4.1-flash_prompt-v4.svg",
        evaluated=True, verdict="fail", reversible="lost", artistic="n/a", humor="n/a", event_used="n/a",
        title="Rack Tower, Morning After",
        event="DeepSeek-R1's release (Jan 2025) and Nvidia's record ~$600B one-day market-cap drop",
        tokens_in=6165, tokens_out=35560, cost=0.0180, settings="one-shot, reasoning effort medium",
        note="The event and art guidance pulled attention away from reversibility; there is no image at 180 degrees.",
    ),
    dict(
        id="r02-glm-5.3-flash", round=2, prompt="v4", model="glm-5.3-flash",
        src="rounds/round-02/svg/glm-5.3-flash_prompt-v4.svg",
        art="glm-5.3-flash_prompt-v4.svg",
        evaluated=True, verdict="fail", reversible="lost", artistic="n/a", humor="n/a", event_used="n/a",
        title="The Pin and the Plug",
        event="Humane AI Pin launch hype (Nov 2023) and its shutdown after the flop (Feb 2024)",
        tokens_in=6242, tokens_out=10732, cost=0.0008, settings="one-shot, reasoning effort medium",
        note="The event and art guidance pulled attention away from reversibility; there is no image at 180 degrees.",
    ),
    dict(
        id="r02-minimax-m3.1-flash", round=2, prompt="v4", model="minimax-m3.1-flash",
        src="rounds/round-02/svg/minimax-m3.1-flash_prompt-v4.svg",
        art="minimax-m3.1-flash_prompt-v4.svg",
        evaluated=True, verdict="fail", reversible="lost", artistic="n/a", humor="n/a", event_used="n/a",
        title="Triumph and the Morning After",
        event="DeepSeek R1's January 2025 launch and the AI-bubble wobble that erased ~$600B of market value",
        tokens_in=6252, tokens_out=54808, cost=0.0335, settings="one-shot, reasoning effort low",
        note="First attempt hit the 64000-token limit without delivering an SVG; the delivered run used low effort.",
    ),

    # --- Round 3: prompt v5 — all three identifiable in both orientations --
    dict(
        id="r03-deepseek-v4.1-flash", round=3, prompt="v5", model="deepseek-v4.1-flash",
        src="rounds/round-03/svg/deepseek-v4.1-flash_prompt-v5.svg",
        art="deepseek-v4.1-flash_prompt-v5.svg",
        evaluated=True, verdict="pass", reversible="ok", artistic="improved", humor="weak",
        event_used="generic",
        title="The Promise and the Prompt",
        event="AI model release hype cycle, mid-2020s",
        tokens_in=4956, tokens_out=2407, cost=0.0043, settings="one-shot, reasoning disabled, max 20000 tokens",
        note="Delivered only with reasoning disabled: with reasoning on it re-verified its own geometry until the token limit.",
    ),
    dict(
        id="r03-glm-5.3-flash", round=3, prompt="v5", model="glm-5.3-flash",
        src="rounds/round-03/svg/glm-5.3-flash_prompt-v5.svg",
        art="glm-5.3-flash_prompt-v5.svg",
        evaluated=True, verdict="pass", reversible="ok", artistic="improved", humor="weak",
        event_used="weak",
        title="Launch Antenna / Dead Battery",
        event="AI assistant launch demo, 2024: triumphant unveil vs. the confident wrong answer",
        tokens_in=5042, tokens_out=8533, cost=0.0035, settings="one-shot, reasoning effort medium, max 64000 tokens",
        note="Identifiable images in both orientations; artistic quality improved.",
    ),
    dict(
        id="r03-minimax-m3.1-flash", round=3, prompt="v5", model="minimax-m3.1-flash",
        src="rounds/round-03/svg/minimax-m3.1-flash_prompt-v5.svg",
        art="minimax-m3.1-flash_prompt-v5.svg",
        evaluated=True, verdict="pass", reversible="ok", artistic="improved", humor="weak",
        event_used="weak",
        title="The Plug Gets Pulled",
        event="ChatGPT launch and the AI boom, followed by 'the plug gets pulled' (late 2022 onward)",
        tokens_in=5085, tokens_out=36639, cost=0.0219, settings="one-shot, reasoning effort low, max 40000 tokens",
        note="First attempt timed out after 900 s; the delivered run used low effort.",
    ),

    # --- Round 4: prompt v6, tools — all reversible, well made, not comic ---
    dict(
        id="r04-deepseek-v4.1-flash", round=4, prompt="v6", model="deepseek-v4.1-flash",
        src="rounds/round-04/svg/deepseek-v4.1-flash_prompt-v6.svg",
        art="deepseek-v4.1-flash_prompt-v6.svg",
        evaluated=True, verdict="pass", reversible="ok", artistic="well made", humor="none",
        event_used="vague",
        title="Headset Hype, Server Sag",
        event="the generative-AI hype cycle: launch-day promise to post-launch burnout (approx. 2023-2025)",
        tokens_in=137666, tokens_out=10633, cost=0.0232,
        settings="tools, reasoning disabled, max 20000 tokens per turn",
        turns=11, tool_calls=11, renders=5,
        note="Both readings are faces, but B is cluttered: a moustache mass where a mouth would be.",
    ),
    dict(
        id="r04-glm-5.3-flash", round=4, prompt="v6", model="glm-5.3-flash",
        src="rounds/round-04/svg/glm-5.3-flash_prompt-v6.svg",
        art="glm-5.3-flash_prompt-v6.svg",
        evaluated=True, verdict="pass", reversible="ok", artistic="well made", humor="none",
        event_used="vague",
        title="Launch Day, Six Months Later",
        event="the big AI chatbot/agent product launch wave of 2024-2025: launch-day euphoria vs. the tired aftermath",
        tokens_in=153508, tokens_out=11504, cost=0.0116,
        settings="tools, reasoning effort medium, max 32000 per turn",
        turns=10, tool_calls=9, renders=4,
        note="The simplest and cleanest: a grinning man in a dark cap, antenna and bow tie; rotated, a frowning bearded man.",
    ),
    dict(
        id="r04-minimax-m3.1-flash", round=4, prompt="v6", model="minimax-m3.1-flash",
        src="rounds/round-04/svg/minimax-m3.1-flash_prompt-v6.svg",
        art="minimax-m3.1-flash_prompt-v6.svg",
        evaluated=True, verdict="pass", reversible="ok", artistic="well made", humor="none",
        event_used="vague",
        title="The Beard Is a Hat Now",
        event="humanoid AI robots / AI agents going to work (2024-25)",
        tokens_in=836616, tokens_out=80012, cost=0.0781,
        settings="tools, reasoning effort low, max 64000 per turn (re-run)",
        turns=12, tool_calls=11, renders=5,
        note="The most Whistler-like: a bearded man in a domed hat; rotated, a frowning man in a tall pointed hat.",
    ),
    dict(
        id="r04-minimax-no-tools", round=4, prompt="v6", model="minimax-m3.1-flash",
        src="rounds/round-04/not-evaluated/minimax-m3.1-flash_run1-no-tools-used_prompt-v6.svg",
        art="minimax-m3.1-flash_run1-no-tools-used_prompt-v6.svg",
        evaluated=False, verdict="none", reversible="unrated",
        tokens_in=43494, tokens_out=33415, cost=0.0263,
        settings="tools offered, effort low, max 32000 per turn; never called a tool",
        turns=2, tool_calls=0, renders=0,
        note="First run: spent all 32000 tokens of its first turn on reasoning and never called a tool. Kept as an extra.",
    ),
]

# ---------------------------------------------------------------------------
# Baselines: 15 comparison runs (baselines/README.md, results table)
# ---------------------------------------------------------------------------

BASELINES = [
    dict(
        id="img01", model="nanobanana-2.1", prompt_type="shared-eyes", kind="raster",
        src="baselines/nanobanana-2.1-shared-eyes/output-web.jpg",
        art="nanobanana-2.1.jpg",
        verdict="fail", rubric=4, david1="fail", david2="pass",
        event="n/a (plain prompt asks for no event)", title=None,
        impression="One clear lady; the second face is a tiny head in the collar, so there is no real second reading.",
        note="FAIL: one head with a tiny head hidden in the collar",
    ),
    dict(
        id="img02", model="chatgpt-medium", prompt_type="v5", kind="svg",
        src="baselines/chatgpt-medium-benchmark/chatgpt-medium.svg",
        art="chatgpt-medium.svg",
        verdict="pass", rubric=8, david1="pass", david2="pass",
        event="GPT-5 launch (August 2025)", title="Launch Day, Power Drain",
        impression="Smiling man becomes a stern bearded man; hair = beard, collar = hat. Same rocket prop on both faces.",
        note="PASS: completed the task",
    ),
    dict(
        id="img03", model="deepseek-v4.1", prompt_type="v5", kind="svg",
        src="baselines/deepseek-v4.1-benchmark/deepseek-v4.1.svg",
        art="deepseek-v4.1.svg",
        verdict="fail", rubric=5, david1="pass", david2="pass",
        event="The 2023 generative-AI boom and the hype/disillusion cycle",
        title="The Bow Tie That Was a Propeller",
        impression="A reads; in B the nose and mouth of A end up above the eyes, so B is half a face.",
        note="FAIL: rotated face cannot be identified",
    ),
    dict(
        id="img04", model="qwen3.8-omni-flash", prompt_type="v5", kind="svg",
        src="baselines/qwen3.8-omni-flash-benchmark/qwen3.8-omni-flash.svg",
        art="qwen3.8-omni-flash.svg",
        verdict="fail", rubric=5, david1="fail", david2="fail",
        event="generative AI chatbot boom (2023)", title="Launch Grin, Aftermath Beard",
        impression="A reads; B has eyes and a nose but floating hat pieces and a flat mouth line, weak and not clearly different.",
        note="FAIL: no face visible when rotated",
    ),
    dict(
        id="img05", model="manus-2.0-lite", prompt_type="v5", kind="svg",
        src="baselines/manus-2.0-lite-benchmark/manus-2.0-lite.svg",
        art="manus-2.0-lite.svg",
        verdict="fail", rubric=6, david1="pass", david2="pass",
        event="GPT-4o launch (May 2024)", title="The Voice and the Echo",
        impression="B reads as a bearded man, but a stray nose stroke sits on its forehead and ghost marks of B show in A's hair.",
        note="FAIL: second face not clear when rotated",
    ),
    dict(
        id="img06", model="gemini-3.1-pro", prompt_type="v5", kind="svg",
        src="baselines/gemini-3.1-pro-benchmark/gemini-3.1-pro.svg",
        art="gemini-3.1-pro.svg",
        verdict="pass", rubric=8, david1="pass", david2="pass",
        event="SpaceX Starship test flights (2024)", title="Launch and RUD",
        impression="Strong shared strokes (hair = beard); smirk becomes a frown; clean and readable.",
        note="PASS: 'managed some humor'",
    ),
    dict(
        id="img07", model="qwen-image-3.0", prompt_type="shared-eyes", kind="raster",
        src="baselines/qwen-image-3.0-shared-eyes/output-web.jpg",
        art="qwen-image-3.0.jpg",
        verdict="fail", rubric=3, david1="fail", david2="fail",
        event="n/a (plain prompt asks for no event)", title=None,
        impression="Two upright faces stacked (lady above, old man below); rotated, both are inverted. The 'same orientation' failure.",
        note='FAIL: "two stacked faces"',
    ),
    dict(
        id="img08", model="glm-5.3-max", prompt_type="v5", kind="svg",
        src="baselines/glm-5.3-max-benchmark/glm-5.3-max.svg",
        art="glm-5.3-max.svg",
        verdict="pass", rubric=6, david1="fail", david2="pass",
        event="DeepSeek shock, Nvidia ~$600B one-day plunge, Jan 2025", title="To the Moon and Back",
        impression="Both orientations read, but cluttered and strange (cheek discs, clouds); iterated about nine renders.",
        note="PASS (with caveat): completed the task, image strange",
    ),
    dict(
        id="img09", model="chatgpt-images-2.5", prompt_type="shared-eyes", kind="raster",
        src="baselines/chatgpt-images-2.5-shared-eyes/output-web.jpg",
        art="chatgpt-images-2.5.jpg",
        verdict="fail", rubric=6, david1="fail", david2="pass",
        event="n/a (plain prompt asks for no event)", title=None,
        impression="Two full heads joined at the collar, each clear when upright but never one drawing that turns into another.",
        note="FAIL: two half-heads stacked",
    ),
    dict(
        id="img10", model="meta-muse-1.3", prompt_type="v5", kind="svg",
        src="baselines/meta-muse-1.3-benchmark/meta-muse-1.3.svg",
        art="meta-muse-1.3.svg",
        verdict="pass", rubric=6, david1="pass", david2="pass",
        event="Apple Vision Pro launch Feb 2024: promise vs fatigue", title="The Headset Promise and The Weight",
        impression="Minimal but both faces read; floating marks are partly orphaned.",
        note="PASS: simple, reasonably executed",
    ),
    dict(
        id="img11", model="grok-imagine-2.0", prompt_type="shared-eyes", kind="raster",
        src="baselines/grok-imagine-2.0-shared-eyes/output-web.jpg",
        art="grok-imagine-2.0.jpg",
        verdict="fail", rubric=6, david1="fail", david2="pass",
        event="n/a (plain prompt asks for no event)", title=None,
        impression="Two separate faces joined at the collars; rotating only swaps which one is upright.",
        note='FAIL: "two separate faces in opposite orientations"',
    ),
    dict(
        id="img12", model="claude-sonnet-5.5-medium", prompt_type="v5", kind="svg",
        src="baselines/claude-sonnet-5.5-medium-benchmark/claude-sonnet-5.5.svg",
        art="claude-sonnet-5.5.svg",
        verdict="pass", rubric=8, david1="fail", david2="pass",
        event="AI investment boom and bubble worries, 2025", title="Liftoff and Landing",
        impression="Clever sharing (hair = beard, red grin = hat band); cheerful vs sad, with a funny swap of rocket and bow tie.",
        note='PASS: both readings work, "even funny"',
    ),
    dict(
        id="img13", model="qwen-3.7-plus", prompt_type="v5", kind="svg",
        src="baselines/qwen-3.7-plus-benchmark/qwen-3.7-plus.svg",
        art="qwen-3.7-plus.svg",
        verdict="fail", rubric=3, david1="fail", david2="pass",
        event="The Great AI Hype Cycle vs. Backend Crash", title="The Pitch and The Crash",
        impression="Nearly the same face in both readings and the file contains letter-shaped paths (M, W), against the contract.",
        note="FAIL: strange, did not pass",
    ),
    dict(
        id="img14", model="gpt-5.6-terra-low", prompt_type="v5", kind="svg",
        src="baselines/gpt-5.6-terra-low-benchmark/gpt-5.6-terra-low.svg",
        art="gpt-5.6-terra-low.svg",
        verdict="pass", rubric=8, david1="pass", david2="pass",
        event="not recorded", title=None,
        impression="Clear contrast (smile under a cap vs scowl with a beard) and different props per face; well integrated.",
        note="PASS: delivered both faces",
    ),
    dict(
        id="img15", model="nemotron-3.5-lightning", prompt_type="v5", kind="svg",
        src="baselines/nemotron-3.5-lightning-benchmark/nemotron-3.5-lightning.svg",
        art="nemotron-3.5-lightning.svg",
        verdict="pass", rubric=6, david1="pass", david2="pass",
        event="not recorded", title=None,
        impression="A triangle with two eyes, a brow and a mouth arc; both readings are only just faces; barely any contrast or prop.",
        note="PASS: but simplified to the extreme",
    ),
]

ROUND_INFO = {
    0: dict(
        key="round-00-pilot", label="Round 0 (pilot)", label_pt="Rodada 0 (piloto)", prompt="v1",
        headline="The setup is exercised end to end",
        verdict="Not human-evaluated",
        lesson="Valid SVGs, but weak expression contrast, oval heads with generic eyes, little visible joke, "
               "and a lot of token budget spent on coordinate arithmetic.",
        changes=["Contract, geometry kit (rotation, canon, dual-function dictionary, sum rule), workflow, "
                 "art notes, self-check, failure catalog, a minimal neutral example."],
    ),
    1: dict(
        key="round-01", label="Round 1", label_pt="Rodada 1", prompt="v2 / v3",
        headline="The effect is achievable — but crude",
        verdict="2 of 3 reversible",
        lesson="The effect is achievable: two of three models produced a working two-face drawing. The general "
               "weakness is artistic quality, and the current event has to become central and impactful.",
        changes=["v2: effort budget, joke as a physical difference, expression contrast, symbolic check.",
                 "v3: a technological accessory with a human counterpart, silhouette first, bold line weight."],
    ),
    2: dict(
        key="round-02", label="Round 2", label_pt="Rodada 2", prompt="v4",
        headline="Adding the event and the art broke the illusion",
        verdict="0 of 3 reversible",
        lesson="It got a lot worse. Now there is no image at 180 degrees anymore. The extra load from the event "
               "requirement and the art guidance pulled attention away from reversibility.",
        changes=["v4: one specific recent tech/AI event made central, plus a large art section "
                 "(150-200% exaggeration, hatching, palette)."],
    ),
    3: dict(
        key="round-03", label="Round 3", label_pt="Rodada 3", prompt="v5",
        headline="Rebuilt from v3, with reversibility as the absolute priority",
        verdict="3 of 3 reversible",
        lesson="All three models did better. All of them managed to make identifiable images in both orientations, "
               "and the artistic quality improved.",
        changes=["v5: absolute priority order (reversibility first), staged workflow "
                 "(geometry, then verify by rotating coordinates, then style), event reduced to one prop, "
                 "art reduced to three short cues."],
    ),
    4: dict(
        key="round-04", label="Round 4", label_pt="Rodada 4", prompt="v6",
        headline="The models can now look at their own drawing",
        verdict="3 of 3 reversible",
        lesson="The three models managed to create the reversible images. The images are well made, interesting, "
               "but they do not convey a comic message. The bottleneck moved from geometry to humor.",
        changes=["v6: v5 plus a tool loop — a sandboxed Python tool and a render tool showing the SVG upright "
                 "and rotated 180 degrees, with text diagnostics; at most 5 renders."],
    ),
}

# Prompt versions, from docs/prompt-evolution.md
PROMPT_VERSIONS = [
    dict(version="v1", used="Round 0 (pilot)", used_pt="Rodada 0 (piloto)", size_kb=16,
         what="Distilled from the v0.4 design spec.",
         changes=["Contract", "Geometry kit (rotation, canon, dual-function dictionary, sum rule)",
                  "Workflow", "Art notes", "Self-check", "Failure catalog", "Minimal neutral example"],
         changes_pt=['Contrato', 'Kit de geometria (rotação, cânone, dicionário de dupla função, regra da soma)', 'Fluxo de trabalho', 'Notas de arte', 'Auto-verificação', 'Catálogo de falhas', 'Exemplo neutro mínimo'],
         outcome="Baseline: valid SVGs, weak contrast."),
    dict(version="v2", used="Round 1 (MiniMax)", used_pt="Rodada 1 (MiniMax)", size_kb=18,
         what="v1 plus fixes from the pilot critique.",
         changes=["Effort budget ('think briefly, round to multiples of 5')",
                  "Joke as a physical difference ('A has X / B has Y')",
                  "A and B must differ in expression",
                  "At least three different dictionary pairs",
                  "Cheap symbolic check instead of heavy arithmetic"],
         changes_pt=["Orçamento de esforço ('pense rápido, arredonde para múltiplos de 5')", "Piada como diferença física ('A tem X / B tem Y')", 'A e B devem diferir na expressão', 'Pelo menos três pares diferentes do dicionário', 'Verificação simbólica barata em vez de aritmética pesada'],
         outcome="Two of three reversible; low artistic quality."),
    dict(version="v3", used="Round 1 (DeepSeek, GLM)", used_pt="Rodada 1 (DeepSeek, GLM)", size_kb=19,
         what="v2 plus a second critique pass.",
         changes=["At least one unmistakably technological accessory",
                  "Silhouette first, not oval first",
                  "Bold line weight (contours 8-12 px, features 5-7 px, detail 3 px)"],
         changes_pt=['Pelo menos um acessório inequivocamente tecnológico', 'Silhueta antes do oval', 'Peso de linha audaz (contornos 8-12 px, features 5-7 px, detalhe 3 px)'],
         outcome="Same round; DeepSeek and GLM judged here."),
    dict(version="v4", used="Round 2", used_pt="Rodada 2", size_kb=24,
         what="v3 rebuilt after the round-1 feedback.",
         changes=["One specific recent tech/AI event made central",
                  "Large art section (exaggeration at 150-200%, hatching, palette)",
                  "EVENT: / TITLE: lines plus <title>/<desc> in the SVG"],
         changes_pt=['Um evento recente e específico de tecnologia/IA tornado central', 'Seção grande de arte (exagero de 150-200%, hachura, paleta)', 'Linhas EVENT:/TITLE: e <title>/<desc> dentro do SVG'],
         outcome="All three lost the 180-degree face."),
    dict(version="v5", used="Round 3", used_pt="Rodada 3", size_kb=18,
         what="Rebuilt from v3, not from v4.",
         changes=["Absolute priority order: reversibility, then contrast, then light touches",
                  "Staged workflow: geometry, verify by rotating coordinates, then style",
                  "Reversibility gate in the self-check",
                  "Event reduced to one droppable prop; art reduced to three cues",
                  "No <title>/<desc> in the SVG"],
         changes_pt=['Ordem de prioridade absoluta (reversibilidade, depois contraste, depois toques leves)', 'Fluxo em etapas (geometria, verificação girando coordenadas, depois estilo)', 'Portão de reversibilidade na auto-verificação', 'Evento reduzido a um acessório descartável; arte reduzida a três pistas', 'Sem <title>/<desc> no SVG'],
         outcome="All three identifiable in both orientations."),
    dict(version="v6", used="Round 4", used_pt="Rodada 4", size_kb=20,
         what="v5 with a tool loop.",
         changes=["Sandboxed Python tool and a render tool (upright + rotated, with diagnostics)",
                  "Dictionary frame made precise (B's own upright frame)",
                  "Stage 2 adds a render and a blind reading",
                  "Unverified Whistler descriptions removed"],
         changes_pt=['Ferramenta Python em sandbox e uma ferramenta de render (em pé + girado, com diagnósticos)', 'Referencial do dicionário tornado preciso (referencial próprio de B)', 'A etapa 2 acrescenta um render e uma leitura cega', 'Descrições de Whistler não verificadas foram removidas'],
         outcome="All three reversible and well made; none comic."),
]

# Dual-function dictionary: rows of how-it-works.md / geometry.md
# `a`/`b`/`note` are the repository's English wording; `*_pt` are the
# Portuguese rendering used by the PT version of the site.
DICTIONARY = [
    dict(a="eyes",             a_pt="olhos",
         ya=0.00,  pb=0.00,  b="eyes",              b_pt="olhos",
         note="anchor: lids and brows decide the mood",
         note_pt="âncora: pálpebras e sobrancelhas decidem o humor"),
    dict(a="brow",             a_pt="sobrancelha",
         ya=-0.08, pb=0.08,  b="under-eye bag",     b_pt="bolsa sob o olho",
         note="", note_pt=""),
    dict(a="hairline / fringe",a_pt="linha do cabelo / franja",
         ya=-0.20, pb=0.20,  b="nose bridge",       b_pt="ponte do nariz",
         note="", note_pt=""),
    dict(a="hat brim",         a_pt="aba do chapéu",
         ya=-0.25, pb=0.25,  b="nose tip",          b_pt="ponta do nariz",
         note="", note_pt=""),
    dict(a="hat or hair dome", a_pt="copa do chapéu ou do cabelo",
         ya=-0.30, pb=0.30,  b="mouth",             b_pt="boca",
         note="a smile is the band of a hat",
         note_pt="um sorriso é a faixa do chapéu"),
    dict(a="crown / top of hat", a_pt="copa / topo do chapéu",
         ya=-0.50, pb=0.50, b="chin",               b_pt="queixo",
         note="", note_pt=""),
    dict(a="plume, pompom",    a_pt="pluma, pompom",
         ya=-0.65, pb=0.65,  b="collar, bow tie",   b_pt="gola, gravata-borboleta",
         note="", note_pt=""),
    dict(a="hair mass",        a_pt="massa de cabelo",
         ya=None,  pb=None,  b="beard, wrinkles, cheeks", b_pt="barba, rugas, bochechas",
         note="free variable", note_pt="variável livre"),
]

# Failure modes: docs/how-it-works.md
FAILURE_MODES = [
    dict(key="same-orientation", name="Same orientation", name_pt="Mesma orientação",
         symptom="B was drawn upright, so A shows two upright faces.",
         symptom_pt="B foi desenhado em pé, então A mostra dois rostos em pé.",
         examples=["img07", "img11", "img09"]),
    dict(key="segregation", name="Segregation", name_pt="Segregação",
         symptom="A in one region, B in another; strokes not shared.",
         symptom_pt="A numa região, B noutra; os traços não são compartilhados.",
         examples=["img03", "img04"]),
    dict(key="ghosting", name="Ghosting", name_pt="Duplicação",
         symptom="Doubled contours ('double exposure') from two overlaid drawings.",
         symptom_pt="Contornos duplicados ('dupla exposição') de dois desenhos sobrepostos.",
         examples=["img05", "img12"]),
    dict(key="b-lost", name="B lost", name_pt="B perdido",
         symptom="The rotated reading shows no face (all of round 2).",
         symptom_pt="A leitura girada não mostra nenhum rosto (toda a rodada 2).",
         examples=["r02-deepseek-v4.1-flash", "r02-glm-5.3-flash", "r02-minimax-m3.1-flash"]),
    dict(key="neutral-faces", name="Neutral faces", name_pt="Rostos neutros",
         symptom="A and B differ only by accessories, with flat expressions.",
         symptom_pt="A e B diferem apenas por acessórios, com expressões planas.",
         examples=["img15", "img13"]),
    dict(key="clip-art", name="Clip-art look", name_pt="Visual de clip-art",
         symptom="Oval head, uniform thin lines, no character.",
         symptom_pt="Cabeça ovalada, linhas finas uniformes, sem caráter.",
         examples=["r00-deepseek-v4.1-flash", "r00-glm-5.3-flash"]),
    dict(key="generic-joke", name="Generic joke", name_pt="Piada genérica",
         symptom="'Hype vs. reality' with no identifiable event.",
         symptom_pt="'Hype vs. realidade' sem nenhum evento identificável.",
         examples=["r03-deepseek-v4.1-flash", "r04-glm-5.3-flash"]),
]

# Judge agreement, baselines/README.md
JUDGES = [
    dict(name="Peter rubric (0-2 gates)", name_pt="Rubrica de Peter (portões 0-2)",
         agrees="15/15", rate=1.00,
         note="Not independent: scored knowing Claudio's verdicts.",
         note_pt="Não é independente: pontuada conhecendo os vereditos do Claudio."),
    dict(name="David stage 1 (single orientation, independent)",
         name_pt="David etapa 1 (uma orientação, independente)",
         agrees="11/15", rate=11/15,
         note="Better predictor; 2 false FAIL (GLM, Claude: faint 'extra faces'), 2 false PASS (DeepSeek, Manus).",
         note_pt="Melhor preditor; 2 falsos FAIL (GLM, Claude: 'rostos extras' tênues), 2 falsos PASS (DeepSeek, Manus)."),
    dict(name="David stage 2 (own verdict, side-by-side)",
         name_pt="David etapa 2 (veredito próprio, lado a lado)",
         agrees="9/15", rate=9/15,
         note="Passes all 7 of Claudio's PASSes but also 6 of his 8 FAILs; lenient.",
         note_pt="Aprova todos os 7 PASS do Claudio, mas também 6 dos 8 FAIL; leniente."),
]


def build(repo: Path, out: Path, art_dir: Path, raster_dir: Path) -> None:
    artifacts = []

    for r in ROUNDS:
        label, vendor = MODELS[r["model"]]
        src = repo / r["src"]
        assert src.exists(), f"missing source: {src}"
        art = art_dir / r["art"]
        shutil.copyfile(src, art)
        info = ROUND_INFO[r["round"]]
        artifacts.append({
            "id": r["id"],
            "group": "round",
            "round": r["round"],
            "roundLabel": info["label"],
            "roundLabelPt": info.get("label_pt", info["label"]),
            "roundKey": info["key"],
            "prompt": r["prompt"],
            "model": r["model"],
            "modelLabel": label,
            "vendor": vendor,
            "kind": "svg",
            "file": f"data/art/{r['art']}",
            "repoPath": r["src"],
            "evaluated": r["evaluated"],
            "verdict": r["verdict"],
            "reversible": r["reversible"],
            "artistic": r.get("artistic"),
            "humor": r.get("humor"),
            "eventUsed": r.get("event_used"),
            "event": r.get("event"),
            "title": r.get("title"),
            "tokensIn": r.get("tokens_in"),
            "tokensOut": r.get("tokens_out"),
            "cost": r.get("cost"),
            "settings": r.get("settings"),
            "turns": r.get("turns"),
            "toolCalls": r.get("tool_calls"),
            "renders": r.get("renders"),
            "note": r.get("note", ""),
        })

    for b in BASELINES:
        label, vendor = MODELS[b["model"]]
        src = repo / b["src"]
        assert src.exists(), f"missing source: {src}"
        sub = art_dir if b["kind"] == "svg" else raster_dir
        art = sub / b["art"]
        shutil.copyfile(src, art)
        artifacts.append({
            "id": b["id"],
            "group": "baseline",
            "round": None,
            "roundLabel": "Baselines",
            "roundLabelPt": "Baselines",
            "roundKey": "baselines",
            "prompt": b["prompt_type"],
            "model": b["model"],
            "modelLabel": label,
            "vendor": vendor,
            "kind": b["kind"],
            "file": f"data/{'art' if b['kind'] == 'svg' else 'raster'}/{b['art']}",
            "repoPath": b["src"],
            "evaluated": True,
            "verdict": b["verdict"],
            "reversible": "ok" if b["verdict"] == "pass" else "fail",
            "artistic": None,
            "humor": None,
            "eventUsed": None,
            "event": b.get("event"),
            "title": b.get("title"),
            "tokensIn": None,
            "tokensOut": None,
            "cost": None,
            "settings": "benchmark prompt v5" if b["prompt_type"] == "v5" else "plain shared-eyes prompt",
            "turns": None,
            "toolCalls": None,
            "renders": None,
            "blindId": b["id"],
            "rubric": b["rubric"],
            "david1": b["david1"],
            "david2": b["david2"],
            "impression": b["impression"],
            "note": b["note"],
        })

    manifest = {
        "meta": {
            "title": "Reversible Faces Benchmark",
            "author": "Claudio Drews",
            "repo": "https://github.com/ClaudioDrews/reversible-faces-benchmark",
            "licenseCode": "MIT",
            "licenseContent": "CC BY 4.0",
            "generated": "2026-11-07",
        },
        "artifacts": artifacts,
        "rounds": {str(k): v for k, v in ROUND_INFO.items()},
        "promptVersions": PROMPT_VERSIONS,
        "dictionary": DICTIONARY,
        "failureModes": FAILURE_MODES,
        "judges": JUDGES,
    }

    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(manifest, indent=2, ensure_ascii=False), encoding="utf-8")

    # Also emit a plain-JS copy so the site works from file:// (no fetch needed).
    js = out.with_suffix(".js")
    js.write_text(
        "/* Generated by site-tools/build_manifest.py - do not edit by hand. */\n"
        "window.RFB_MANIFEST = " + json.dumps(manifest, indent=2, ensure_ascii=False) + ";\n",
        encoding="utf-8",
    )

    n_round = sum(1 for a in artifacts if a["group"] == "round")
    n_base = sum(1 for a in artifacts if a["group"] == "baseline")
    print(f"wrote {out} :: {len(artifacts)} artifacts ({n_round} rounds, {n_base} baselines)")
    print(f"  svg art files  : {len(list(art_dir.glob('*.svg')))}")
    print(f"  raster files   : {len(list(raster_dir.glob('*.jpg')))}")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", default=str(Path(__file__).resolve().parents[1]))
    ap.add_argument("--out", default=str(Path(__file__).resolve().parents[1] / "site" / "data" / "manifest.json"))
    ap.add_argument("--art", default=str(Path(__file__).resolve().parents[1] / "site" / "data" / "art"))
    ap.add_argument("--raster", default=str(Path(__file__).resolve().parents[1] / "site" / "data" / "raster"))
    a = ap.parse_args()
    build(Path(a.repo), Path(a.out), Path(a.art), Path(a.raster))


if __name__ == "__main__":
    main()
