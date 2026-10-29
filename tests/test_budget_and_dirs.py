# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Claudio Drews
"""Pre-call cost estimate, overrun recording, structured API log, no silent overwrite."""
import json
import tempfile
import unittest
from pathlib import Path

from _common import ROOT
import rfb_common as C
import mock_openrouter as M

MSGS = [{"role": "user", "content": "x" * 3000}]       # ~1000 estimated prompt tokens


class BudgetTests(unittest.TestCase):
    def test_estimate_is_worst_case(self):
        b = C.Budget(1.0, 1e-6, 4e-6, "test")
        est = b.estimate(MSGS, 10000)
        self.assertAlmostEqual(est, C.estimate_prompt_tokens(MSGS) * 1e-6 + 10000 * 4e-6)
        self.assertGreater(est, 10000 * 4e-6)

    def test_images_are_charged(self):
        with_img = MSGS + [{"role": "user", "content": [{"type": "image_url", "image_url": {"url": "data:..."}}]}]
        self.assertGreater(C.estimate_prompt_tokens(with_img), C.estimate_prompt_tokens(MSGS) + C.IMAGE_TOKENS - 1)

    def test_plan_passes_when_it_fits(self):
        b = C.Budget(1.0, 1e-6, 4e-6, "test")
        mt, est = b.plan(MSGS, 32000)
        self.assertEqual(mt, 32000)

    def test_plan_lowers_max_tokens_to_fit(self):
        b = C.Budget(0.05, 1e-6, 4e-6, "test")
        mt, est = b.plan(MSGS, 32000)          # 32000 * 4e-6 = 0.128 > 0.05
        self.assertLess(mt, 32000)
        self.assertGreaterEqual(mt, C.MIN_USEFUL_MAX_TOKENS)
        self.assertLessEqual(est, 0.05 + 1e-9)

    def test_plan_refuses_when_nothing_fits(self):
        b = C.Budget(0.001, 1e-6, 4e-6, "test")
        mt, _ = b.plan(MSGS, 32000)
        self.assertIsNone(mt)

    def test_overrun_is_recorded_not_hidden(self):
        b = C.Budget(0.10, 1e-6, 4e-6, "test")
        b.record(1, 0.09, 20000, {"cost": 0.07})
        b.record(2, 0.09, 20000, {"cost": 0.09})         # reported cost went past the cap
        self.assertAlmostEqual(b.overrun, 0.06)
        self.assertAlmostEqual(b.summary()["overrun_usd"], 0.06)
        self.assertEqual(len(b.summary()["calls"]), 2)
        self.assertIn("approximate", b.summary()["note"])

    def test_price_from_environment(self):
        import os
        os.environ["PRICE_IN_PER_MTOK"], os.environ["PRICE_OUT_PER_MTOK"] = "0.2", "0.8"
        try:
            pin, pout, src = C.price_for("any/model", offline=True)
        finally:
            del os.environ["PRICE_IN_PER_MTOK"], os.environ["PRICE_OUT_PER_MTOK"]
        self.assertAlmostEqual(pin, 0.2e-6)
        self.assertAlmostEqual(pout, 0.8e-6)
        self.assertEqual(src, "environment")

    def test_default_price_is_labelled(self):
        self.assertEqual(C.price_for("any/model", offline=True)[2], "pessimistic default")


class OutDirTests(unittest.TestCase):
    def test_refuses_non_empty_dir(self):
        with tempfile.TemporaryDirectory() as t:
            (Path(t) / "old.txt").write_text("keep me")
            with self.assertRaises(SystemExit):
                C.prepare_out_dir(t)
            self.assertEqual((Path(t) / "old.txt").read_text(), "keep me")

    def test_empty_or_new_dir_is_fine(self):
        with tempfile.TemporaryDirectory() as t:
            self.assertTrue(C.prepare_out_dir(t).exists())
            self.assertTrue(C.prepare_out_dir(Path(t) / "new").exists())

    def test_timestamped_makes_a_new_subdir(self):
        with tempfile.TemporaryDirectory() as t:
            (Path(t) / "old.txt").write_text("keep me")
            d = C.prepare_out_dir(t, timestamped=True)
            self.assertNotEqual(d, Path(t))
            self.assertEqual(d.parent, Path(t))

    def test_force_allows_reuse(self):
        with tempfile.TemporaryDirectory() as t:
            (Path(t) / "old.txt").write_text("x")
            self.assertEqual(C.prepare_out_dir(t, force=True), Path(t))


class ApiLogTests(unittest.TestCase):
    def test_failures_are_logged_as_json_lines(self):
        with tempfile.TemporaryDirectory() as t:
            log = C.ApiLog(Path(t) / "api-errors.jsonl")
            tr = M.MockTransport([{"error": "HTTP 429 rate limited"}, {"error": "timeout"}, {"content": "ok"}])
            r = C.call_api("k", {"max_tokens": 100}, log, transport=tr, sleep=0, model="m/x", turn=1)
            self.assertIsNotNone(r)
            lines = [json.loads(l) for l in (Path(t) / "api-errors.jsonl").read_text().splitlines()]
            self.assertEqual(len(lines), 2)
            self.assertEqual(lines[0]["attempt"], 0)
            self.assertIn("429", lines[0]["detail"])
            self.assertEqual(lines[0]["model"], "m/x")

    def test_total_failure_returns_none(self):
        with tempfile.TemporaryDirectory() as t:
            log = C.ApiLog(Path(t) / "e.jsonl")
            tr = M.MockTransport([{"error": "down"}])
            self.assertIsNone(C.call_api("k", {"max_tokens": 100}, log, transport=tr, sleep=0))
            self.assertEqual(log.count, 3)


if __name__ == "__main__":
    unittest.main()


class CostAccountingTests(unittest.TestCase):
    """Review fixes: the estimate counts reasoning_details and tool schemas; a missing cost is never free."""

    def test_estimate_counts_reasoning_details_and_tools(self):
        plain = [{"role": "assistant", "content": "ok"}]
        heavy = [{"role": "assistant", "content": "ok", "reasoning_details": [{"text": "r" * 30000}]}]
        self.assertGreater(C.estimate_prompt_tokens(heavy), C.estimate_prompt_tokens(plain) + 9000)
        tools = [{"type": "function", "function": {"name": "t", "description": "d" * 3000}}]
        self.assertGreater(C.estimate_prompt_tokens(plain, tools), C.estimate_prompt_tokens(plain) + 900)

    def test_images_are_not_counted_as_base64_text(self):
        big = [{"role": "user", "content": [{"type": "image_url", "image_url": {"url": "data:image/png;base64," + "A" * 500000}}]}]
        self.assertLess(C.estimate_prompt_tokens(big), C.IMAGE_TOKENS + 100)

    def test_reported_prompt_tokens_are_a_floor(self):
        b = C.Budget(1.0, 1e-6, 4e-6, "test")
        b.record(1, 0.01, 1000, {"cost": 0.001, "prompt_tokens": 50000, "completion_tokens": 10})
        self.assertGreaterEqual(b.prompt_tokens(MSGS), 50000)

    def test_missing_cost_is_derived_from_tokens(self):
        b = C.Budget(1.0, 1e-6, 4e-6, "test")
        c = b.record(1, 0.5, 1000, {"prompt_tokens": 1000, "completion_tokens": 500})   # provider omitted cost
        self.assertAlmostEqual(c, 1000 * 1e-6 + 500 * 4e-6)
        self.assertEqual(b.calls[-1]["cost_source"], "derived")
        self.assertGreater(b.spent, 0)

    def test_missing_cost_and_tokens_charges_the_estimate(self):
        b = C.Budget(1.0, 1e-6, 4e-6, "test")
        c = b.record(1, 0.5, 1000, {})
        self.assertEqual(c, 0.5)
        self.assertEqual(b.calls[-1]["cost_source"], "estimate")

    def test_reported_cost_is_used_when_present(self):
        b = C.Budget(1.0, 1e-6, 4e-6, "test")
        self.assertEqual(b.record(1, 0.5, 1000, {"cost": 0.002, "prompt_tokens": 10, "completion_tokens": 10}), 0.002)
        self.assertEqual(b.calls[-1]["cost_source"], "reported")


class NormalizeHeadTests(unittest.TestCase):
    def test_adds_each_missing_attribute_independently(self):
        out = C.normalize_svg_head('<svg width="1000"><g/></svg>')
        self.assertIn('height="1000"', out)
        self.assertIn('viewBox="0 0 1000 1000"', out)
        self.assertIn("xmlns=", out)
        self.assertEqual(out.count("width="), 1)

    def test_self_closing_root(self):
        out = C.normalize_svg_head("<svg/>")
        self.assertTrue(out.startswith("<svg ") and out.endswith("/>") and "<svg/ " not in out)
        import xml.etree.ElementTree as ET
        ET.fromstring(out)

    def test_gt_inside_attribute_value(self):
        out = C.normalize_svg_head('<svg data-x="a>b" xmlns="http://www.w3.org/2000/svg"><g/></svg>')
        import xml.etree.ElementTree as ET
        root = ET.fromstring(out)
        self.assertEqual(root.get("data-x"), "a>b")
        self.assertEqual(root.get("width"), "1000")

    def test_never_changes_a_value_the_model_wrote(self):
        out = C.normalize_svg_head('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 10 10" width="12" height="23"/>')
        self.assertIn('viewBox="0 0 10 10"', out)
        self.assertIn('width="12"', out)

    def test_stroke_width_is_not_mistaken_for_width(self):
        out = C.normalize_svg_head('<svg stroke-width="3"><g/></svg>')
        self.assertIn(' width="1000"', out)

    def test_no_svg_raises(self):
        with self.assertRaises(ValueError):
            C.normalize_svg_head("hello")
