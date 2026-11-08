"""Offline unit tests; no provider calls, no rendering."""
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

src=Path(__file__).resolve().parents[1]/"agent.py"
spec=importlib.util.spec_from_file_location("dual_agent",src)
lab=importlib.util.module_from_spec(spec)
spec.loader.exec_module(lab)

def sample_plan():
    return {"intent":"an inventor becomes a skeptical critic","face_a":{"identity":"inventor","expression":"joyful"},
            "face_b":{"identity":"critic","expression":"concerned"},
            "shared_eyes":[{"x":410,"y":500},{"x":590,"y":500}],
            "role_pairs":[{"role_a":"brow","role_b":"eye bag","point_a":[430,452],"point_b":[570,548]}
                          for _ in range(5)],
            "silhouette":"one enclosing head","failure_risks":["collage","weak second view"]}

class TestLabAgent(unittest.TestCase):
    def test_prepare_prompts(self):
        p,s=lab.prep_prompts("A grateful inventor becomes a skeptical critic")
        self.assertIn("Apply R EXACTLY ONCE",p)
        self.assertIn("standalone, original SVG",s)
    def test_plan_frames(self):
        fences=chr(96)*3
        plan=lab.parse_plan(fences+"json\n"+json.dumps(sample_plan())+"\n"+fences)
        self.assertEqual(lab.residuals(plan),[0.0]*5)
    def test_plan_rejects(self):
        with self.assertRaises(ValueError):lab.parse_plan("{}")
        bad=sample_plan();bad["role_pairs"][0]["point_b"]=[1001,0]
        with self.assertRaises(ValueError):lab.parse_plan(json.dumps(bad))
    def test_svg_extract(self):
        good='<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 1000" width="1000" height="1000"></svg>'
        self.assertEqual(lab.extract_svg("START\n"+good+"\nEND"),good)
        with self.assertRaises(ValueError):lab.extract_svg("no svg")
    def test_urls(self):
        for good in ("https://openrouter.ai/api/v1/chat/completions","http://localhost:1234/v1/chat/completions"):
            lab.allowed_endpoint(good)
        for bad in ("http://example.com","file:///tmp/secrets","https://a:b@host.com/"):
            with self.assertRaises(ValueError):lab.allowed_endpoint(bad)
    def test_offline_package(self):
        with tempfile.TemporaryDirectory() as tmp:
            lab.prepare("Two expressive faces, one engraved outline",Path(tmp))
            self.assertTrue((Path(tmp)/"prompt-plan.txt").exists())
            self.assertFalse((Path(tmp)/"candidate.svg").exists())
    def test_validator_fails_active_svg(self):
        try:import defusedxml
        except ImportError:self.skipTest("defusedxml not installed")
        good='<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 1000" width="1000" height="1000"><circle cx="500" cy="500" r="20"/></svg>'
        bad=good.replace("</svg>","<script>alert(1)</script></svg>")
        self.assertFalse(lab.check_svg(good)[0])
        self.assertTrue(lab.check_svg(bad)[0])
if __name__=="__main__":unittest.main()
