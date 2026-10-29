#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Cláudio Drews
"""Run one benchmark prompt, one-shot, on one or more models via OpenRouter.

Usage:
    export OPENROUTER_API_KEY=...            # never commit keys
    python scripts/run_models.py OUT_DIR PROMPT_FILE [MODEL ...]

Example:
    python scripts/run_models.py runs/my-run prompts/prompt-v5.md \
        deepseek/deepseek-v4.1-flash z-ai/glm-5.3-flash minimax/minimax-m3.1-flash

Environment variables (all optional):
    OPENROUTER_API_KEY  required
    EFFORT              reasoning effort: low | medium (default) | high
    NOREASON=1          disable reasoning entirely (used for DeepSeek in round 3)
    MAXTOK              max completion tokens (default 64000)
    STRIP_METADATA=1    remove <title>/<desc>/<metadata> from the SVG (rounds 3+)

For each model it writes, in OUT_DIR:
    <model>.raw.txt        the model's final answer, verbatim
    <model>.reasoning.txt  the reasoning trace, if the API returned one
    <model>.svg            the extracted SVG (xmlns / viewBox / width / height are
                           added if missing; XML validity is checked)
    cost-log.json          tokens and cost (USD) per model, as reported by OpenRouter
Prompts from v4 on ask the model to start its answer with `EVENT:` and `TITLE:` lines;
those are parsed and stored in cost-log.json.
"""
import json
import os
import re
import sys
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path

DEFAULT_MODELS = ["deepseek/deepseek-v4.1-flash", "z-ai/glm-5.3-flash", "minimax/minimax-m3.1-flash"]


def main():
    if len(sys.argv) < 3:
        sys.exit(__doc__)
    out = Path(sys.argv[1])
    prompt = Path(sys.argv[2]).read_text()
    models = sys.argv[3:] or DEFAULT_MODELS
    key = os.environ.get("OPENROUTER_API_KEY")
    if not key:
        sys.exit("Set OPENROUTER_API_KEY in your environment.")
    out.mkdir(parents=True, exist_ok=True)

    if os.environ.get("NOREASON"):
        reasoning = {"enabled": False}
    else:
        reasoning = {"effort": os.environ.get("EFFORT", "medium")}

    total, log = 0.0, []
    for model in models:
        name = model.split("/")[1]
        body = json.dumps({
            "model": model,
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": int(os.environ.get("MAXTOK", "64000")),
            "reasoning": reasoning,
            "usage": {"include": True},
        }).encode()
        req = urllib.request.Request(
            "https://openrouter.ai/api/v1/chat/completions", body,
            {"Authorization": "Bearer " + key, "Content-Type": "application/json"})
        try:
            r = json.load(urllib.request.urlopen(req, timeout=900))
        except Exception as e:  # network / API error
            print(name, "ERROR", e)
            continue
        choice = r["choices"][0]
        msg = choice["message"]
        text = msg.get("content") or ""
        usage = r.get("usage", {})
        cost = usage.get("cost", 0) or 0
        total += cost
        (out / f"{name}.raw.txt").write_text(text)
        (out / f"{name}.reasoning.txt").write_text(str(msg.get("reasoning") or ""))
        ev = re.search(r"^EVENT:\s*(.+)$", text, re.M)
        ti = re.search(r"^TITLE:\s*(.+)$", text, re.M)
        rec = {"model": model, "prompt_tokens": usage.get("prompt_tokens"),
               "completion_tokens": usage.get("completion_tokens"), "cost_usd": cost,
               "finish_reason": choice.get("finish_reason"),
               "event": ev.group(1).strip() if ev else None,
               "title": ti.group(1).strip() if ti else None}
        m = re.search(r"<svg\b.*?</svg>", text, re.S)
        if not m:
            rec["svg"] = None
            log.append(rec)
            print(name, rec, "NO SVG")
            continue
        svg = m.group(0)
        head = re.match(r"<svg\b[^>]*>", svg).group(0)
        new = head
        if "xmlns=" not in new:
            new = new.replace("<svg", '<svg xmlns="http://www.w3.org/2000/svg"', 1)
        if "viewBox" not in new:
            new = new[:-1] + ' viewBox="0 0 1000 1000">'
        if not re.search(r"\swidth=", new):
            new = new[:-1] + ' width="1000" height="1000">'
        svg = svg.replace(head, new, 1)
        if os.environ.get("STRIP_METADATA"):
            svg = re.sub(r"\s*<(title|desc|metadata)\b.*?</\1>", "", svg, flags=re.S)
        svg = '<?xml version="1.0" encoding="UTF-8"?>\n' + svg + "\n"
        try:
            ET.fromstring(svg.split("?>", 1)[1])
            rec["xml"] = "valid"
        except ET.ParseError as e:
            rec["xml"] = f"INVALID: {e}"
        (out / f"{name}.svg").write_text(svg)
        rec["svg"] = f"{name}.svg"
        log.append(rec)
        print(name, rec)
    (out / "cost-log.json").write_text(json.dumps({"total_cost_usd": total, "runs": log}, indent=1))
    print("TOTAL cost (USD):", total)


if __name__ == "__main__":
    main()
