# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Cláudio Drews
"""Shared helpers for the runners: pre-call cost estimate, structured API-failure log, no-silent-overwrite
output directories, and the HTTP transport (replaceable by a mock for offline tests)."""
import json
import os
import re
import time
import urllib.request
from datetime import datetime
from pathlib import Path

API_URL = "https://openrouter.ai/api/v1/chat/completions"
MODELS_URL = "https://openrouter.ai/api/v1/models"      # public list; no key, no model call, no cost
# Used only when neither the models list nor the environment gives a price. Deliberately pessimistic for the
# cheap models of this project (round 4 paid about US$0.1-0.4 per million tokens).
DEFAULT_PRICE_IN_PER_MTOK = 1.0
DEFAULT_PRICE_OUT_PER_MTOK = 4.0
CHARS_PER_TOKEN = 3.0        # pessimistic (English text is about 4)
IMAGE_TOKENS = 2000          # pessimistic charge per image
MIN_USEFUL_MAX_TOKENS = 2000


# ---------------------------------------------------------------- <svg> head normalisation
_SVG_HEAD = re.compile(r"<svg\b(?:[^>\"']|\"[^\"]*\"|'[^']*')*>")


def normalize_svg_head(text):
    """Text-level helper used by both runners: add xmlns / viewBox / width / height to the root <svg> tag only
    where each is missing (each attribute independently; self-closing roots and '>' inside quoted attribute
    values are handled). It never changes a value the model wrote, so a wrong viewBox stays wrong and is
    reported by the validator. Raises ValueError if there is no <svg> tag. It is NOT a security measure."""
    m = _SVG_HEAD.search(text)
    if not m:
        raise ValueError("no <svg> element found")
    head = m.group(0)
    selfclose = head.endswith("/>")
    inner = head[4:-2] if selfclose else head[4:-1]
    inner = inner.rstrip()
    for attr, add in (("xmlns", ' xmlns="http://www.w3.org/2000/svg"'), ("viewBox", ' viewBox="0 0 1000 1000"'),
                      ("width", ' width="1000"'), ("height", ' height="1000"')):
        if not re.search(r"(?<![\w:-])" + attr + r"\s*=", inner):
            inner += add
    new = "<svg" + inner + ("/>" if selfclose else ">")
    return text[:m.start()] + new + text[m.end():]


# ---------------------------------------------------------------- output directories
def prepare_out_dir(path, timestamped=False, force=False):
    """Return a directory that is safe to write into. Refuses to reuse a non-empty directory unless
    `force`; with `timestamped`, creates `<path>/<YYYYmmdd-HHMMSS>` instead."""
    p = Path(path)
    if timestamped:
        p = p / datetime.now().strftime("%Y%m%d-%H%M%S")
    if p.exists() and any(p.iterdir()) and not force:
        raise SystemExit(f"refusing to write into the non-empty directory {p} (it would overwrite earlier "
                         f"results). Use a new directory, --timestamped, or --force.")
    p.mkdir(parents=True, exist_ok=True)
    return p


# ---------------------------------------------------------------- structured API log
class ApiLog:
    """Append-only JSON-lines log of every API attempt that did not return usable choices."""

    def __init__(self, path):
        self.path = Path(path)
        self.count = 0
        self.path.touch()          # an empty file means "no API failure", not "not logged"

    def record(self, **kw):
        self.count += 1
        rec = {"t": datetime.now().astimezone().isoformat(timespec="seconds"), **kw}
        with self.path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")


def http_transport(key, body, timeout=600):
    req = urllib.request.Request(API_URL, json.dumps(body).encode(),
                                 {"Authorization": "Bearer " + key, "Content-Type": "application/json"})
    return json.load(urllib.request.urlopen(req, timeout=timeout))


def call_api(key, body, log, transport=http_transport, attempts=3, sleep=5, model=None, turn=None):
    """POST with retries. Every failed attempt is written to `log` (HTTP status and body excerpt, timeout,
    malformed answer). Returns the response dict or None."""
    for attempt in range(attempts):
        b = dict(body)
        if attempt == attempts - 1 and attempts > 1:
            b["max_tokens"] = min(b.get("max_tokens", 16000), 16000)
        try:
            r = transport(key, b)
            if isinstance(r, dict) and r.get("choices"):
                return r
            log.record(model=model, turn=turn, attempt=attempt, kind="no_choices",
                       detail=json.dumps(r, ensure_ascii=False)[:500] if r is not None else None)
        except Exception as e:
            kind, status, detail = type(e).__name__, getattr(e, "code", None), str(e)
            if hasattr(e, "read"):
                try:
                    detail += " | " + e.read().decode("utf-8", "replace")[:500]
                except Exception:
                    pass
            log.record(model=model, turn=turn, attempt=attempt, kind=kind, status=status, detail=detail[:800])
        print(f"API attempt {attempt} failed (see api-errors.jsonl)", flush=True)
        time.sleep(sleep * (attempt + 1))
    return None


# ---------------------------------------------------------------- cost estimate before each call
def fetch_prices(model, timeout=20):
    """USD per token (input, output) from the public models list, or None. A GET, not a model call."""
    try:
        with urllib.request.urlopen(MODELS_URL, timeout=timeout) as r:
            for m in json.load(r).get("data", []):
                if m.get("id") == model:
                    pr = m.get("pricing") or {}
                    return float(pr["prompt"]), float(pr["completion"])
    except Exception:
        return None
    return None


def price_for(model, offline=False):
    """Returns (price_in_per_token, price_out_per_token, source)."""
    env_in, env_out = os.environ.get("PRICE_IN_PER_MTOK"), os.environ.get("PRICE_OUT_PER_MTOK")
    if env_in and env_out:
        return float(env_in) / 1e6, float(env_out) / 1e6, "environment"
    if not offline:
        p = fetch_prices(model)
        if p:
            return p[0], p[1], "openrouter models list"
    return DEFAULT_PRICE_IN_PER_MTOK / 1e6, DEFAULT_PRICE_OUT_PER_MTOK / 1e6, "pessimistic default"


def estimate_prompt_tokens(messages, tools=None):
    """Defensive estimate of the prompt (an estimate, not a proven upper bound; Budget adds a floor from the
    provider's own prompt_tokens once a call has been answered): every message is counted as its full JSON (content, tool calls,
    reasoning_details that the harness sends back, ...), images are charged IMAGE_TOKENS instead of their
    base64 text, and the tool schemas are included."""
    chars, images = 0, 0
    for m in messages:
        m = dict(m)
        c = m.get("content")
        if isinstance(c, list):
            parts = []
            for part in c:
                if part.get("type") == "image_url":
                    images += 1
                else:
                    parts.append(part)
            m["content"] = parts
        chars += len(json.dumps(m, ensure_ascii=False))
    if tools:
        chars += len(json.dumps(tools, ensure_ascii=False))
    return int(chars / CHARS_PER_TOKEN) + images * IMAGE_TOKENS + 8 * len(messages)


class Budget:
    """Operational spending limit. It is APPROXIMATE: it uses a defensive estimate before each call
    (prompt tokens x input price + max_tokens x output price, so a call is never started that could, by that
    estimate, exceed the cap), and the provider-reported cost after it. Anything it cannot see (a failed or
    timed-out request that the provider still billed, a wrong price) can still push the real spend over the
    cap; overruns of the reported cost are recorded, not hidden."""

    def __init__(self, cap, price_in, price_out, price_source, tools=None):
        self.cap, self.pin, self.pout, self.source = cap, price_in, price_out, price_source
        self.tools = tools
        self.spent, self.calls = 0.0, []
        self.last_prompt_tokens = 0     # reported by the provider; a conversation only grows, so it is a floor

    def prompt_tokens(self, messages):
        return max(estimate_prompt_tokens(messages, self.tools), self.last_prompt_tokens)

    def estimate(self, messages, max_tokens):
        return self.prompt_tokens(messages) * self.pin + max_tokens * self.pout

    def plan(self, messages, max_tokens):
        """-> (max_tokens_to_use or None, estimate). Lowers max_tokens so the worst case fits the remaining
        budget; None means even MIN_USEFUL_MAX_TOKENS does not fit (do not call)."""
        remaining = self.cap - self.spent
        est = self.estimate(messages, max_tokens)
        if est <= remaining:
            return max_tokens, est
        fit = int((remaining - self.prompt_tokens(messages) * self.pin) / self.pout) if self.pout > 0 else 0
        if fit >= MIN_USEFUL_MAX_TOKENS:
            fit = min(fit, max_tokens)
            return fit, self.estimate(messages, fit)
        return None, est

    def record(self, turn, estimate, max_tokens, usage):
        """Adds the cost of one answered call and returns it. Uses the provider-reported `usage.cost`; if it is
        missing or zero, derives it from the reported token counts and the price (cost_source="derived"), and
        if there are no token counts either, charges the pre-call estimate (cost_source="estimate"). A missing
        cost therefore never reads as free."""
        usage = usage or {}
        # note: a genuinely free model (cost 0) is charged as "derived" here; that over-counts, which is the safe side
        actual, source = usage.get("cost") or 0, "reported"
        pt, ct = usage.get("prompt_tokens") or 0, usage.get("completion_tokens") or 0
        if not actual:
            if pt or ct:
                actual, source = pt * self.pin + ct * self.pout, "derived"
            else:
                actual, source = estimate, "estimate"
        if pt:
            self.last_prompt_tokens = max(self.last_prompt_tokens, pt)
        self.spent += actual
        self.calls.append({"turn": turn, "estimate_usd": round(estimate, 6), "max_tokens_used": max_tokens,
                           "actual_usd": round(actual, 6), "cost_source": source})
        return actual

    @property
    def overrun(self):
        return round(max(0.0, self.spent - self.cap), 6)

    def summary(self):
        return {"cap_usd": self.cap, "spent_reported_usd": round(self.spent, 6), "overrun_usd": self.overrun,
                "price_source": self.source, "price_in_per_mtok": self.pin * 1e6, "price_out_per_mtok": self.pout * 1e6,
                "calls": self.calls,
                "note": "approximate operational limit: estimate before each call, provider-reported cost after"}
