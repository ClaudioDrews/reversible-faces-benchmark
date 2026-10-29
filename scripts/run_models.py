#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Claudio Drews
"""Run one benchmark prompt on one or more models via OpenRouter: ONE-SHOT WITHOUT TOOLS (rounds 0-3).

One request per model, the prompt as the only message, no tools, no follow-up, no retries of the content
(only of failed HTTP calls). For the tool-augmented single-attempt run of round 4 see run_models_v6.py.

Usage:
    export OPENROUTER_API_KEY=...            # never commit keys
    python scripts/run_models.py [--timestamped|--force] [--mock] OUT_DIR PROMPT_FILE [MODEL ...]

Example:
    python scripts/run_models.py runs/my-run prompts/prompt-v5.md \
        deepseek/deepseek-v4.1-flash z-ai/glm-5.3-flash minimax/minimax-m3.1-flash

Environment variables (all optional):
    OPENROUTER_API_KEY  required (not for --mock)
    EFFORT              reasoning effort: low | medium (default) | high
    NOREASON=1          disable reasoning entirely (used for DeepSeek in rounds 3 and 4)
    MAXTOK              max completion tokens (default 64000)
    STRIP_METADATA=1    remove <title>/<desc>/<metadata> from the SVG (rounds 3+)
    COST_CAP_USD        optional approximate cap for the whole invocation (default: none); checked with a
                        defensive estimate BEFORE each call (see rfb_common.Budget) and recorded after
    PRICE_IN_PER_MTOK / PRICE_OUT_PER_MTOK   override prices (USD per million tokens)

OUT_DIR must be new or empty (the script refuses to overwrite earlier results; use --timestamped or --force).
For each model it writes, in OUT_DIR:
    <model>.raw.txt        the model's final answer, verbatim
    <model>.reasoning.txt  the reasoning trace, if the API returned one
    <model>.original.svg   the SVG exactly as the model wrote it (never rendered unsandboxed)
    <model>.svg            the normalized SVG (xmlns / viewBox / width / height added if missing;
                           title/desc/metadata stripped if STRIP_METADATA=1). This is the delivered file.
    <model>.sanitized.svg  the allowlist-sanitized copy that renderers use
    api-errors.jsonl       structured log of every failed API attempt (HTTP status, body excerpt, timeout...)
    cost-log.json          tokens, cost (USD), status, validator report per model
Prompts from v4 on ask the model to start its answer with `EVENT:` and `TITLE:` lines;
those are parsed and stored in cost-log.json.
"""
import argparse
import json
import os
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import rfb_common as C  # noqa: E402
import svg_safety  # noqa: E402
import validate_svg  # noqa: E402

DEFAULT_MODELS = ["deepseek/deepseek-v4.1-flash", "z-ai/glm-5.3-flash", "minimax/minimax-m3.1-flash"]


def normalize(svg_text, strip_metadata):
    svg = C.normalize_svg_head(svg_text)
    if strip_metadata:
        svg = re.sub(r"\s*<(title|desc|metadata)\b.*?</\1>", "", svg, flags=re.S)
    return '<?xml version="1.0" encoding="UTF-8"?>\n' + svg + "\n"


def main(argv=None, transport=None):
    ap = argparse.ArgumentParser(description="One-shot, no-tools runner (rounds 0-3).")
    ap.add_argument("out_dir")
    ap.add_argument("prompt_file")
    ap.add_argument("models", nargs="*")
    ap.add_argument("--timestamped", action="store_true", help="write into OUT_DIR/<YYYYmmdd-HHMMSS>")
    ap.add_argument("--force", action="store_true", help="allow a non-empty OUT_DIR (may overwrite)")
    ap.add_argument("--mock", action="store_true", help="offline smoke test with a scripted fake API (no cost)")
    ap.add_argument("--mock-svg", choices=["benign", "hostile"], default="benign")
    args = ap.parse_args(sys.argv[1:] if argv is None else argv)
    prompt = Path(args.prompt_file).read_text()
    models = args.models or DEFAULT_MODELS
    if args.mock:
        import mock_openrouter as M
        key = "mock"
        svg = M.hostile_svg() if args.mock_svg == "hostile" else M.benign_svg()
        transport = transport or M.MockTransport(M.oneshot_script(svg))
    else:
        key = os.environ.get("OPENROUTER_API_KEY")
        if not key:
            sys.exit("Set OPENROUTER_API_KEY in your environment.")
        transport = transport or C.http_transport
    out = C.prepare_out_dir(args.out_dir, args.timestamped, args.force)
    apilog = C.ApiLog(out / "api-errors.jsonl")

    reasoning = {"enabled": False} if os.environ.get("NOREASON") else {"effort": os.environ.get("EFFORT", "medium")}
    maxtok = int(os.environ.get("MAXTOK", "64000"))
    cap = float(os.environ["COST_CAP_USD"]) if os.environ.get("COST_CAP_USD") else None

    total, log = 0.0, []
    for model in models:
        name = model.split("/")[-1]
        pin, pout, psrc = C.price_for(model, offline=args.mock)
        budget = C.Budget(cap if cap is not None else float("inf"), pin, pout, psrc)
        messages = [{"role": "user", "content": prompt}]
        mt, est = budget.plan(messages, maxtok)
        rec = {"model": model, "status": None, "estimate_before_call_usd": round(est, 6), "price_source": psrc,
               "max_tokens_used": mt}
        if mt is None:
            rec["status"] = "skipped_cost_precheck"
            log.append(rec)
            print(name, "SKIPPED: the defensive cost estimate exceeds COST_CAP_USD")
            continue
        body = {"model": model, "messages": messages, "max_tokens": mt, "reasoning": reasoning,
                "usage": {"include": True}}
        r = C.call_api(key, body, apilog, transport=transport, sleep=0 if args.mock else 5, model=model, turn=1)
        if not r:
            rec["status"] = "api_failure"
            log.append(rec)
            print(name, "ERROR: no usable answer (see api-errors.jsonl)")
            continue
        choice = r["choices"][0]
        msg = choice["message"]
        text = msg.get("content") or ""
        usage = r.get("usage", {})
        cost = budget.record(1, est, mt, usage)   # reported cost; derived from tokens if the provider omits it
        total += cost
        (out / f"{name}.raw.txt").write_text(text)
        (out / f"{name}.reasoning.txt").write_text(str(msg.get("reasoning") or ""))
        ev = re.search(r"^EVENT:\s*(.+)$", text, re.M)
        ti = re.search(r"^TITLE:\s*(.+)$", text, re.M)
        rec.update({"status": "ok", "prompt_tokens": usage.get("prompt_tokens"),
                    "completion_tokens": usage.get("completion_tokens"), "cost_usd": cost,
                    "cost_overrun_usd": budget.overrun if cap is not None else 0.0,
                    "finish_reason": choice.get("finish_reason"),
                    "event": ev.group(1).strip() if ev else None, "title": ti.group(1).strip() if ti else None})
        m = re.search(r"<svg\b.*?</svg>", text, re.S)
        if not m:
            rec["svg"] = None
            rec["status"] = "no_svg"
            log.append(rec)
            print(name, rec, "NO SVG")
            continue
        original = m.group(0)
        (out / f"{name}.original.svg").write_text(original)
        svg = normalize(original, bool(os.environ.get("STRIP_METADATA")))
        (out / f"{name}.svg").write_text(svg)
        rec["svg"], rec["svg_original"] = f"{name}.svg", f"{name}.original.svg"
        errors, warnings, _ = validate_svg.check_bytes(svg.encode("utf-8"))
        rec["validator"] = {"errors": errors, "warnings": warnings, "passes_contract": not errors}
        rec["xml"] = "valid" if not any(e.startswith("invalid XML") for e in errors) else "INVALID"
        try:
            clean, findings = svg_safety.sanitize(svg)
            (out / f"{name}.sanitized.svg").write_text(clean)
            rec["sanitizer_removed"] = [f.message for f in findings if f.severity == "error"]
        except svg_safety.SvgRejected as e:
            rec["sanitizer_rejected"] = e.message
        log.append(rec)
        print(name, rec)
    (out / "cost-log.json").write_text(json.dumps({"total_cost_usd": total, "api_failures_logged": apilog.count,
                                                   "runs": log}, indent=1, ensure_ascii=False))
    print("TOTAL cost (USD):", total)
    return log


if __name__ == "__main__":
    main()
