# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Claudio Drews
"""Documentation hygiene: relative Markdown links and images resolve, in-page anchors exist, the README renders
math in GitHub's `$...$` / `$$...$$` form, and the files the README tells readers to run exist."""
import re
import unittest
import urllib.parse

from _common import ROOT

FENCE = re.compile(r"```.*?```", re.S)
LINK = re.compile(r'(?<!\!)\[[^\]]*\]\(([^)\s]+)(?:\s+"[^"]*")?\)|<img[^>]*src="([^"]+)"|!\[[^\]]*\]\(([^)\s]+)\)')


def md_files():
    return [p for p in ROOT.rglob("*.md") if ".git" not in p.parts]


def anchors(text):
    out = set(re.findall(r'<a id="([^"]+)"', text))
    for h in re.findall(r"^#{1,6}\s+(.*)$", FENCE.sub("", text), flags=re.M):
        out.add(re.sub(r"[^\w\- ]", "", h.lower()).strip().replace(" ", "-"))
    return out


class Docs(unittest.TestCase):
    def test_relative_links_and_images_resolve(self):
        bad = []
        for f in md_files():
            text = FENCE.sub("", f.read_text(encoding="utf-8"))
            for m in LINK.finditer(text):
                link = m.group(1) or m.group(2) or m.group(3)
                if link.startswith(("http://", "https://", "mailto:", "#")):
                    continue
                path = urllib.parse.unquote(link.split("#")[0])
                if path and not (f.parent / path).resolve().exists():
                    bad.append((str(f.relative_to(ROOT)), link))
        self.assertEqual(bad, [])

    def test_in_page_anchors_exist(self):
        bad = []
        for f in md_files():
            raw = f.read_text(encoding="utf-8")
            have = anchors(raw)
            for link in re.findall(r"\]\((#[^)\s]+)\)", FENCE.sub("", raw)):
                if link[1:] not in have:
                    bad.append((str(f.relative_to(ROOT)), link))
        self.assertEqual(bad, [])

    def test_readme_math_is_github_style(self):
        text = (ROOT / "README.md").read_text(encoding="utf-8")
        self.assertNotIn("\\[", text)
        self.assertNotIn("\\(", text)
        self.assertGreater(text.count("$$"), 4)

    def test_commands_in_readme_point_at_existing_files(self):
        text = (ROOT / "README.md").read_text(encoding="utf-8")
        for rel in re.findall(r"python (?:scripts/[\w./-]+\.py)", text):
            self.assertTrue((ROOT / rel.split(" ", 1)[1]).exists(), rel)
        for rel in re.findall(r"prompts/prompt-v\d\.md", text):
            self.assertTrue((ROOT / rel).exists(), rel)

    def test_navigation_pages_exist(self):
        for rel in ("docs/README.md", "rounds/README.md", "PUBLISH-CHECKLIST.md", "paper/README.md", "to-do.md"):
            self.assertTrue((ROOT / rel).exists(), rel)


if __name__ == "__main__":
    unittest.main()
