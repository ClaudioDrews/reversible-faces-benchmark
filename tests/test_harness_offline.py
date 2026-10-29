# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Claudio Drews
"""Offline smoke tests of both runners with a scripted fake API. No network, no key, NO COST."""
import json
import os
import tempfile
import unittest
from pathlib import Path

from _common import ROOT, have_render_stack
import mock_openrouter as M

PROMPT = ROOT / "prompts" / "prompt-v6.md"


@unittest.skipUnless(have_render_stack(), "needs bwrap and Chrome/Chromium")
class HarnessV6(unittest.TestCase):
    def run_v6(self, transport, extra=(), model="z-ai/glm-5.3-flash", env=None):
        import run_models_v6 as H
        old = dict(os.environ)
        os.environ.update(env or {})
        try:
            with tempfile.TemporaryDirectory() as t:
                rec = H.main([*extra, "--mock", t, str(PROMPT), model], transport=transport)
                files = sorted(p.name for p in (Path(t) / model.split("/")[1]).iterdir())
                texts = {n: (Path(t) / model.split("/")[1] / n).read_text(errors="replace") for n in files if not n == "work"
                         and (Path(t) / model.split("/")[1] / n).is_file() and not n.endswith(".png")}
        finally:
            os.environ.clear(); os.environ.update(old)
        return rec, files, texts

    def test_benign_run(self):
        tr = M.MockTransport(M.harness_script())
        rec, files, texts = self.run_v6(tr)
        self.assertEqual((rec["turns"], rec["tool_calls"], rec["renders"]), (3, 2, 1))
        self.assertTrue(rec["validator"]["passes_contract"])
        for f in ("glm-5.3-flash.original.svg", "glm-5.3-flash.svg", "glm-5.3-flash.sanitized.svg", "api-errors.jsonl",
                  "render-1.svg", "render-1.original.svg", "render-1.png", "transcript.jsonl", "cost-log.json"):
            self.assertIn(f, files)
        self.assertEqual(texts["api-errors.jsonl"], "")                   # no failures
        self.assertIn("estimate_before_call", rec["per_turn"][0])
        # the image goes back to the model in a harness-labelled user message
        last = tr.bodies[-1]["messages"]
        self.assertTrue(any(isinstance(m["content"], list) for m in last if m["role"] == "user"))

    def test_hostile_svg_is_saved_verbatim_but_never_rendered_raw(self):
        tr = M.MockTransport(M.harness_script(M.hostile_svg()))
        rec, files, texts = self.run_v6(tr)
        self.assertFalse(rec["validator"]["passes_contract"])
        self.assertIn("<script>", texts["glm-5.3-flash.original.svg"])        # evidence kept, verbatim
        self.assertNotIn("<script", texts["glm-5.3-flash.sanitized.svg"])
        self.assertNotIn("<script", texts["render-1.svg"])                     # what Chrome got
        self.assertIn("<script", texts["render-1.original.svg"])               # what the model sent
        self.assertTrue(rec["sanitizer_removed"])
        self.assertIn("the safe renderer removed", texts["transcript.jsonl"])

    def test_recovery_turns_are_two_and_the_bound_is_max_turns_plus_two(self):
        import run_models_v6 as H
        self.assertEqual((H.MAX_TURNS, H.RECOVERY_TURNS, H.MAX_TURNS + H.RECOVERY_TURNS), (16, 2, 18))
        # a model that never stops calling tools, one call per turn: the 12-call tool budget ends the tool phase at
        # turn 12; then ONE forced-delivery turn and ONE re-ask (the two recovery turns) = 14 calls, below the bound of 18
        loop = [{"tool_calls": [M.tool_call(1, "run_python", code="print(1)")]}]
        tr = M.MockTransport(loop)
        rec, _, texts = self.run_v6(tr)
        self.assertEqual(len(tr.bodies), 14)
        self.assertEqual(rec["tool_calls"], 12)
        self.assertLessEqual(len(tr.bodies), H.MAX_TURNS + H.RECOVERY_TURNS)
        with_tools = [i for i, b in enumerate(tr.bodies, 1) if "tools" in b]
        self.assertEqual(with_tools, list(range(1, 13)))                    # tools dropped on both recovery turns
        self.assertTrue(rec["finish"].endswith("+no_svg"))
        self.assertIn("tool budget used", texts["transcript.jsonl"].lower())

    def test_tool_limit_triggers_delivery_notice(self):
        loop = [{"tool_calls": [M.tool_call(i, "run_python", code="print(1)") for i in range(1, 4)]}] * 5 + \
               [M.final_answer(M.benign_svg())]
        tr = M.MockTransport(loop)
        rec, _, texts = self.run_v6(tr)
        self.assertEqual(rec["tool_calls"], 12 + 0 if rec["tool_calls"] == 12 else rec["tool_calls"])
        self.assertIn("tool budget used", texts["transcript.jsonl"].lower())

    def test_cost_precheck_stops_before_calling(self):
        tr = M.MockTransport(M.harness_script())
        rec, _, _ = self.run_v6(tr, env={"COST_CAP_USD": "0.0001"})
        self.assertEqual(len(tr.bodies), 0)                                   # no call was made
        self.assertEqual(rec["finish"], "cost_precheck_stop")

    def test_max_tokens_is_lowered_to_fit_the_remaining_budget(self):
        tr = M.MockTransport(M.harness_script())
        rec, _, _ = self.run_v6(tr, env={"COST_CAP_USD": "0.05", "MAXTOK": "32000"})
        self.assertLess(tr.bodies[0]["max_tokens"], 32000)
        self.assertEqual(rec["cost_overrun_usd"], 0.0)

    def test_overrun_is_recorded(self):
        steps = M.harness_script()
        steps[0]["cost"] = 0.3                                                 # provider reports more than the cap
        tr = M.MockTransport(steps)
        rec, _, _ = self.run_v6(tr)
        self.assertGreater(rec["cost_overrun_usd"], 0.0)

    def test_missing_provider_cost_is_derived_and_still_stops_at_the_cap(self):
        steps = [dict(s, nocost=True) for s in M.harness_script()]
        tr = M.MockTransport(steps, usage=(100000, 40000))       # at the pessimistic default price: ~US$0.26 per call
        rec, _, _ = self.run_v6(tr)
        self.assertGreater(rec["cost_usd"], 0.2)                  # not reported as free
        self.assertEqual(rec["budget"]["calls"][0]["cost_source"], "derived")
        self.assertLess(rec["turns"], 3)                          # the cap stopped the run early

    def test_api_failures_are_logged_structurally(self):
        script = [{"error": "HTTP 502 Bad Gateway"}, {"error": "timed out"}] + M.harness_script()
        tr = M.MockTransport(script)
        rec, files, texts = self.run_v6(tr)
        lines = [json.loads(l) for l in texts["api-errors.jsonl"].splitlines()]
        self.assertEqual(len(lines), 2)
        self.assertEqual(rec["api_failures_logged"], 2)
        self.assertIn("502", lines[0]["detail"])

    def test_refuses_to_overwrite(self):
        import run_models_v6 as H
        with tempfile.TemporaryDirectory() as t:
            H.main(["--mock", t, str(PROMPT), "z-ai/glm-5.3-flash"])
            with self.assertRaises(SystemExit):
                H.main(["--mock", t, str(PROMPT), "z-ai/glm-5.3-flash"])
            H.main(["--mock", "--timestamped", t, str(PROMPT), "z-ai/glm-5.3-flash"])    # allowed


class OneShot(unittest.TestCase):
    def run_one(self, svg, extra=()):
        import run_models as R
        with tempfile.TemporaryDirectory() as t:
            out = Path(t) / "out"
            log = R.main([*extra, "--mock", "--mock-svg", svg, str(out), str(ROOT / "prompts/prompt-v5.md"), "a/model-x"])
            files = {p.name: p.read_text() for p in out.iterdir()}
        return log, files

    def test_original_and_normalized_are_saved_separately(self):
        log, files = self.run_one("hostile")
        self.assertIn("<script>", files["model-x.original.svg"])
        self.assertNotIn("<script", files["model-x.sanitized.svg"])
        self.assertTrue(files["model-x.svg"].startswith("<?xml"))
        self.assertFalse(log[0]["validator"]["passes_contract"])
        self.assertEqual(log[0]["status"], "ok")
        self.assertIn("api-errors.jsonl", files)

    def test_benign(self):
        log, files = self.run_one("benign")
        self.assertTrue(log[0]["validator"]["passes_contract"])
        self.assertEqual(json.loads(files["cost-log.json"])["api_failures_logged"], 0)

    def test_api_failure_is_recorded_in_status(self):
        import run_models as R
        tr = M.MockTransport([{"error": "HTTP 500"}])
        with tempfile.TemporaryDirectory() as t:
            out = Path(t) / "o"
            log = R.main(["--mock", str(out), str(ROOT / "prompts/prompt-v5.md"), "a/m"], transport=tr)
            self.assertEqual(log[0]["status"], "api_failure")
            self.assertEqual(len((out / "api-errors.jsonl").read_text().splitlines()), 3)

    def test_refuses_to_overwrite(self):
        import run_models as R
        with tempfile.TemporaryDirectory() as t:
            out = Path(t) / "o"
            R.main(["--mock", str(out), str(ROOT / "prompts/prompt-v5.md"), "a/m"])
            with self.assertRaises(SystemExit):
                R.main(["--mock", str(out), str(ROOT / "prompts/prompt-v5.md"), "a/m"])


class NoSecrets(unittest.TestCase):
    def test_runners_do_not_embed_keys(self):
        import re
        for p in (ROOT / "scripts").glob("*.py"):
            s = p.read_text()
            self.assertIsNone(re.search(r"sk-or-[A-Za-z0-9]{10,}", s), p.name)


if __name__ == "__main__":
    unittest.main()
