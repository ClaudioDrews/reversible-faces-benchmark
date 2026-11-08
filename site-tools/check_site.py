#!/usr/bin/env python3
"""Validate the static GitHub Pages payload without third-party dependencies."""
from pathlib import Path
from html.parser import HTMLParser
import json, sys, re

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / 'site'

class Refs(HTMLParser):
    def __init__(self):
        super().__init__()
        self.paths = []
    def handle_starttag(self, tag, attrs):
        for key, value in attrs:
            if key in ('src','href') and value and not value.startswith(('http:', 'https:', 'data:', '#','mailto:')):
                self.paths.append(value.split('#',1)[0].split('?',1)[0])

def main():
    errors = []
    html = (SITE / 'index.html').read_text(encoding='utf-8')
    if '<html lang="en">' not in html: errors.append('English must be the default HTML language')
    parser = Refs(); parser.feed(html)
    for path in parser.paths:
        if not (SITE/path).is_file(): errors.append(f'HTML reference missing: {path}')
    if not (SITE/'.nojekyll').exists(): errors.append('Missing .nojekyll')
    manifest=json.loads((SITE/'data/manifest.json').read_text(encoding='utf-8'))
    rho=json.loads((SITE/'data/rho.json').read_text(encoding='utf-8'))
    arts=manifest['artifacts']
    if len(arts) != 33: errors.append(f'Expected 33 artifacts, got {len(arts)}')
    for art in arts:
        p=SITE/art['file']
        if not p.is_file(): errors.append(f'Artifact missing: {art["file"]}')
        if art['kind'] == 'svg' and art['id'] not in rho:
            errors.append(f'ρ missing: {art["id"]}')
    code=(SITE/'assets/js/i18n.js').read_text(encoding='utf-8')
    if "var current = 'en'" not in code: errors.append('English must be default JS language')
    if "return 'en'; // English is the default" not in code: errors.append('Missing English fallback')
    if not (SITE/'data/manifest.js').exists(): errors.append('Missing embedded JS manifest')
    if not (SITE/'data/art.js').exists(): errors.append('Missing inline art data')
    for p in sorted((SITE/'data/art').glob('*.svg')):
        svg=p.read_text(encoding='utf-8')
        if re.search(r'<\s*(?:script|foreignObject|iframe)\b|\bon\w+\s*=|javascript\s*:', svg, re.I):
            errors.append(f'Potential active SVG content: {p.name}')
    print(f'Assets: {len(arts)} artifacts; {len(parser.paths)} local HTML references; {len(rho)} ρ records')
    if errors:
        print('\n'.join('ERROR: '+e for e in errors),file=sys.stderr)
        return 1
    print('Static site integrity PASS')
    return 0
if __name__ == '__main__': raise SystemExit(main())
