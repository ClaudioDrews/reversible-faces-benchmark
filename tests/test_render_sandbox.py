# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Claudio Drews
"""Rendering is sandboxed. Skipped when bubblewrap or Chrome is not installed."""
import os
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

import numpy as np
from PIL import Image

from _common import ROOT, have_render_stack
from mock_openrouter import hostile_svg, benign_svg

HAVE = have_render_stack()
if HAVE:
    import safe_render as R


@unittest.skipUnless(HAVE, "needs bwrap and Chrome/Chromium")
class Sandbox(unittest.TestCase):
    def sandboxed(self, python_code):
        with tempfile.TemporaryDirectory() as tmp:
            os.chmod(tmp, 0o777)
            cmd = R.sandbox_command("/usr/bin/python3", tmp, ["-c", python_code])
            return subprocess.run(cmd, capture_output=True, text=True, timeout=60,
                                  env={"PATH": "/usr/bin:/bin", "OPENROUTER_API_KEY": "must-not-leak"})

    def test_no_network(self):
        p = self.sandboxed("import socket,sys\n"
                           "try:\n socket.create_connection(('1.1.1.1',53),3); print('CONNECTED')\n"
                           "except OSError as e:\n print('blocked',e)")
        self.assertIn("blocked", p.stdout, p.stdout + p.stderr)
        self.assertNotIn("CONNECTED", p.stdout)

    def test_no_home_workspace_or_keys(self):
        p = self.sandboxed("import os\n"
                           "print('WS', os.path.exists('/workspace'), 'HOME', os.path.exists('/home'), "
                           "'ROOT', os.path.exists('/root'), 'KEY', 'OPENROUTER_API_KEY' in os.environ)")
        self.assertIn("WS False HOME False ROOT False KEY False", p.stdout, p.stdout + p.stderr)

    def test_only_the_work_dir_is_writable(self):
        p = self.sandboxed("import os\n"
                           "def w(path):\n"
                           "  try:\n    open(path,'w').write('x'); return True\n"
                           "  except OSError: return False\n"
                           "print('USR', w('/usr/evil'), 'ETC', w('/etc/evil'), 'WORK', w('/work/ok'))")
        self.assertIn("USR False ETC False WORK True", p.stdout, p.stdout + p.stderr)

    def test_refuses_without_bwrap(self):
        old = R.shutil.which
        R.shutil.which = lambda n: None if n == "bwrap" else old(n)
        try:
            os.environ.pop("RFB_ALLOW_UNSANDBOXED", None)
            with self.assertRaises(R.RenderUnavailable):
                R.render_png(benign_svg(), 100)
        finally:
            R.shutil.which = old

    def test_chrome_never_runs_without_bwrap_flags(self):
        cmd = R.sandbox_command("/usr/bin/true", "/tmp", [])
        for flag in ("--unshare-all", "--cap-drop", "--clearenv", "--die-with-parent"):
            self.assertIn(flag, cmd)
        self.assertNotIn("--share-net", cmd)


@unittest.skipUnless(HAVE, "needs bwrap and Chrome/Chromium")
class Render(unittest.TestCase):
    def test_render_benign(self):
        im, rot, findings = R.render_pair(benign_svg(), 200)
        self.assertEqual(im.size, (200, 200))
        a = np.asarray(im.convert("L"))
        self.assertGreater((a < 128).sum(), 100)   # something dark was drawn
        self.assertEqual(findings, [])

    def test_hostile_svg_renders_only_the_safe_part(self):
        im, _, findings = R.render_pair(hostile_svg(), 200)
        self.assertTrue(any(f.severity == "error" for f in findings))
        a = np.asarray(im.convert("L"))
        self.assertGreater((a < 128).sum(), 50)    # the benign path still draws

    def test_dtd_is_rejected_before_chrome(self):
        from svg_safety import SvgRejected
        with self.assertRaises(SvgRejected):
            R.render_png((ROOT / "tests/fixtures/invalid/doctype_entity.svg").read_bytes(), 100)

    def test_element_boxes(self):
        rows = R.element_boxes(benign_svg())
        self.assertTrue(rows)
        self.assertTrue(all(len(r["box"]) == 4 for r in rows))

    def test_committed_previews_are_reproduced(self):
        """Previews in assets/previews were made with the old unsandboxed renderer; the sandboxed one must give
        the same picture (small tolerance: Chrome versions may antialias differently)."""
        svg = ROOT / "rounds/round-04/svg/glm-5.3-flash_prompt-v6.svg"
        ref = ROOT / "assets/previews/round-04__glm-5.3-flash_prompt-v6.png"
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "p.png"
            R.side_by_side(svg.read_bytes(), out, 450)
            a = np.asarray(Image.open(out).convert("L"), float)
            b = np.asarray(Image.open(ref).convert("L"), float)
            self.assertEqual(a.shape, b.shape)
            self.assertLess(abs(a - b).mean(), 2.0)


if __name__ == "__main__":
    unittest.main()
