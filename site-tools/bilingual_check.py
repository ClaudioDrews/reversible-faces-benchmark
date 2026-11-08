#!/usr/bin/env python3
"""Bilingual integrity check.

Loads the site in both languages and verifies that no UI string is left in the
wrong language — including text drawn on <canvas>, which a DOM-text diff
cannot see. The canvas is instrumented by patching fillText.

Only *interface* text is checked. Content that comes from the benchmark
repository (model names, declared events and titles, evaluator notes and
impressions) is quoted research material and deliberately stays in the
repository's original English in both language versions.
"""
import re
import sys
from playwright.sync_api import sync_playwright

import os, shutil
CHROME = os.environ.get("CHROMIUM_BIN") or shutil.which("chromium") or shutil.which("google-chrome")
import os
BASE = os.environ.get("RFB_BASE", "http://127.0.0.1:8811/index.html")

# Selectors that hold site-authored interface text (not manifest data).
UI_SELECTORS = [
    ".site-nav a", ".brand-text", ".eyebrow", ".hero h1", ".lede",
    ".hero-actions .btn", ".hero-stats dt", ".hero-credit", ".hero-hint",
    ".hero-caption", ".section-index", ".section-head h2", ".section-sub",
    ".play-toolbar .chip", ".play-dial .chip", "#pg-angle",
    ".play-meta .meta-badge", ".play-meta .meta-title", ".play-meta .meta-sub",
    ".play-meta .meta-quote", ".play-meta .meta-rows dt", ".play-meta .note",
    ".play-meta .meta-links a", ".pane-tag",
    "#gal-filters .chip", ".gal-model", ".gal-flag",
    "#geo-tabs .tab", ".geo-text h3", ".geo-text p", ".geo-facts span",
    ".dict-legend span", ".dict-table th", ".dict-table td",
    ".canon-controls label span", ".canon-controls output", ".callout",
    ".cs-readout span", ".failure-card h4", ".failure-card p",
    ".sym-picker span", ".sym-toggles span", ".sym-readout span", ".sym-note",
    ".sym-panel h4", ".sym-panel .sym-explain",
    ".tl-round", ".tl-prompt", ".tl-verdict", ".tl-main h3", ".tl-lesson",
    ".tl-changes li", ".prompt-table th", ".prompt-table td",
    ".stat-num", ".stat-label", "#base-filters .chip", "#base-sort",
    ".base-table th", ".base-table .pill", ".base-table .prompttype",
    ".base-detail dt", ".base-detail h5", ".judge-row", ".judge-note",
    ".method-card h3", ".method-card p", ".caveats h3", ".caveats li",
    ".method-cols h3", ".method-cols p", ".spec-list li",
    ".footer-title", ".footer-note", ".footer-links a",
]

PT_MARKERS = [
    "rodada", "rodadas", "laboratório", "galeria", "geometria", "simetria",
    "método", "aprovado", "reprovado", "não avaliado", "artefato", "artefatos",
    "modelo", "título", "evento", "condição", "custo", "rubrica", "impressão",
    "olhos", "chapéu", "sobrancelha", "boca", "queixo", "nariz", "gola",
    "barba", "página", "leitura", "traço", "traços", "meia-volta", "girado",
    "girada", "desenhado", "alvo", "alvos", "distância", "teste", "falha",
    "passa", "rosto", "rostos", "decomposição", "ilusão", "desenho",
    "desenhos", "figura", "copa", "aba", "linha do cabelo", "bolsa sob o olho",
    "ponta do nariz", "ponte do nariz", "gravata", "pluma",
    "mesmos traços", "outra leitura", "referencial", "b em coordenadas",
    "olhos em y", "posição = 500", "faixa laranja", "tolerância", "ressalva",
    "etapa", "artefatos públicos", "desenho vetorial", "traços compartilhados",
    "diagnósticos geométricos", "companheiro educativo", "materiais de pesquisa",
    "invertido", "compartilhado", "geométrico", "em pé",
]

EN_MARKERS = [
    "round", "rounds", "gallery", "geometry", "symmetry", "method",
    "not evaluated", "artifact", "artifacts", "model",
    "run settings", "cost", "rubric", "impression",
    "eyes", "brow", "beard",
    "page", "reading", "stroke", "strokes", "half-turn", "turned", "drawn",
    "target", "targets", "distance", "test", "decomposition",
    "illusion", "drawing", "drawings", "brim", "hairline",
    "under-eye bag", "nose tip", "nose bridge", "plume",
    "same strokes", "different reading", "own frame", "in b", "eyes at y",
    "position = 500", "orange band", "tolerance", "caveat", "text judge",
    "stage", "educational companion", "research materials", "public artifacts",
    "vector drawing", "shared strokes", "geometric diagnostics", "upright",
    "shared", "geometric",
]


def collect(pg, lang):
    pg.goto(f"{BASE}?lang={lang}", wait_until="networkidle")
    pg.wait_for_timeout(1800)
    pg.evaluate("""() => {
        if (!CanvasRenderingContext2D.prototype.__patched) {
            const orig = CanvasRenderingContext2D.prototype.fillText;
            CanvasRenderingContext2D.prototype.fillText = function (t, ...a) {
                window.__ctexts.push(String(t));
                return orig.apply(this, [t, ...a]);
            };
            CanvasRenderingContext2D.prototype.__patched = true;
        }
        window.__ctexts = [];
        if (window.rfbRedrawGeometry) window.rfbRedrawGeometry();
    }""")
    pg.wait_for_timeout(700)
    ui = pg.evaluate("""(sels) => {
        const out = [];
        sels.forEach(s => {
            document.querySelectorAll(s).forEach(el => {
                const t = (el.innerText || el.textContent || '').trim();
                if (t) out.push(t);
            });
        });
        return out;
    }""", UI_SELECTORS)
    canvas = pg.evaluate("() => window.__ctexts || []")
    meta = {
        "lang": pg.evaluate("() => document.documentElement.lang"),
        "title": pg.title(),
        "desc": pg.evaluate("() => document.querySelector('meta[name=description]')?.content || ''"),
        "url": pg.url,
        "activeBtn": pg.evaluate("() => document.querySelector('.lang-switch button.is-active')?.textContent || ''"),
    }
    return ui, canvas, meta


def scan(texts, markers):
    """Word-boundary match, so 'model' does not fire inside 'modelo' and
    'hat' does not fire inside 'ChatGPT'."""
    blob = " \n".join(texts).lower()
    hits = []
    for m in markers:
        pat = r'(?<![a-z0-9])' + re.escape(m.lower()) + r'(?![a-z0-9])'
        if re.search(pat, blob):
            hits.append(m)
    return sorted(set(hits))


def main():
    problems = []
    with sync_playwright() as p:
        b = p.chromium.launch(executable_path=CHROME,
                              args=["--no-sandbox", "--disable-dev-shm-usage"])
        pg = b.new_page(viewport={"width": 1440, "height": 950})
        errs = []
        pg.on("pageerror", lambda e: errs.append(str(e)))
        pg.on("console", lambda m: errs.append(m.text) if m.type == "error" else None)

        en_ui, en_canvas, en_meta = collect(pg, "en")
        pt_ui, pt_canvas, pt_meta = collect(pg, "pt")

        print(f"EN  ui-strings={len(en_ui):4d}  canvas-strings={len(en_canvas):3d}  "
              f"lang={en_meta['lang']!r}  switch={en_meta['activeBtn']!r}")
        print(f"PT  ui-strings={len(pt_ui):4d}  canvas-strings={len(pt_canvas):3d}  "
              f"lang={pt_meta['lang']!r}  switch={pt_meta['activeBtn']!r}")
        print(f"EN title: {en_meta['title']}")
        print(f"PT title: {pt_meta['title']}")
        print(f"EN url  : {en_meta['url']}")
        print(f"PT url  : {pt_meta['url']}")

        # 1. no Portuguese left in the English build
        hits = scan(en_ui + en_canvas + [en_meta["title"], en_meta["desc"]], PT_MARKERS)
        if hits:
            problems.append(f"EN build still shows Portuguese: {hits}")

        # 2. no English left in the Portuguese build
        hits2 = scan(pt_ui + pt_canvas + [pt_meta["title"], pt_meta["desc"]], EN_MARKERS)
        if hits2:
            problems.append(f"PT build still shows English: {hits2}")

        # 3. structural parity
        if abs(len(en_ui) - len(pt_ui)) > 8:
            problems.append(f"UI string count differs: EN {len(en_ui)} vs PT {len(pt_ui)}")
        if abs(len(en_canvas) - len(pt_canvas)) > 8:
            problems.append(f"canvas string count differs: EN {len(en_canvas)} vs PT {len(pt_canvas)}")

        # 3b. positive assertions: each language must show ITS OWN wording
        def has(sel, needle):
            txt = pg.evaluate(
                "(s)=>Array.from(document.querySelectorAll(s)).map(e=>(e.innerText||e.textContent||'')).join(' ')",
                sel) or ""
            return needle.lower() in txt.lower()

        pg.goto(f"{BASE}?lang=pt", wait_until="networkidle"); pg.wait_for_timeout(1500)
        for sel, needle, why in [
            ("#dict-table tbody", "sobrancelha", "PT dictionary term"),
            ("#dict-table tbody", "bolsa sob o olho", "PT dictionary partner term"),
            (".tl-round", "Rodada 0 (piloto)", "PT round label"),
            (".failure-card h4", "Mesma orientação", "PT failure-mode name"),
            (".geo-facts", "distância p", "PT canvas label"),
            (".sym-readout", "Fração de tinta", "PT symmetry readout"),
            (".prompt-table td", "reversibilidade", "PT prompt changelist"),
            ("#perguntas h2", "Perguntas de pesquisa em aberto", "PT open-questions heading"),
            ("#perguntas li h3", "Interferência de restrições", "PT open-questions item"),
            ("#perguntas", "É uma hipótese, não um achado", "PT hedging of the humor hypothesis"),
            ("#rode h2", "Rode você mesmo", "PT run-it-yourself heading"),
            ("#rode", "Nunca abra um SVG escrito por modelo", "PT SVG safety warning"),
            (".skill-list strong", "Composição semântica", "PT task-demand skill"),
            ("#hero-state", "Em pé: leitura A", "PT rotation readout"),
        ]:
            if not has(sel, needle):
                problems.append(f"PT build is missing {why} ({needle!r} in {sel})")

        pg.goto(f"{BASE}?lang=en", wait_until="networkidle"); pg.wait_for_timeout(1500)
        for sel, needle, why in [
            ("#dict-table tbody", "under-eye bag", "EN dictionary partner term"),
            (".tl-round", "Round 0 (pilot)", "EN round label"),
            (".failure-card h4", "Same orientation", "EN failure-mode name"),
            (".geo-facts", "distance p", "EN canvas label"),
            (".sym-readout", "Ink fraction", "EN symmetry readout"),
            (".prompt-table td", "reversibility", "EN prompt changelist"),
            ("#perguntas h2", "Open research questions", "EN open-questions heading"),
            ("#perguntas li h3", "Constraint interference", "EN open-questions item"),
            ("#perguntas", "That is a hypothesis, not a finding", "EN hedging of the humor hypothesis"),
            ("#rode h2", "Run it yourself", "EN run-it-yourself heading"),
            ("#rode", "Never open unvalidated model-written SVG", "EN SVG safety warning"),
            (".skill-list strong", "Semantic composition", "EN task-demand skill"),
            ("#hero-state", "Upright: reading Face A", "EN rotation readout"),
        ]:
            if not has(sel, needle):
                problems.append(f"EN build is missing {why} ({needle!r} in {sel})")

        # 4. document identity
        if en_meta["lang"] != "en":
            problems.append(f"EN build html lang = {en_meta['lang']!r}")
        if pt_meta["lang"] != "pt-BR":
            problems.append(f"PT build html lang = {pt_meta['lang']!r}")
        if en_meta["activeBtn"] != "EN":
            problems.append(f"EN build switch shows {en_meta['activeBtn']!r}")
        if pt_meta["activeBtn"] != "PT":
            problems.append(f"PT build switch shows {pt_meta['activeBtn']!r}")
        if en_meta["title"] == pt_meta["title"]:
            problems.append("document title does not change with the language")
        if "lang=pt" not in pt_meta["url"]:
            problems.append(f"PT url lost the parameter: {pt_meta['url']}")

        b.close()

    print()
    if problems:
        print("PROBLEMS:")
        for x in problems:
            print("  ✗", x)
    else:
        print("✓ both language versions complete, in sync, and free of cross-contamination")
    if errs:
        print("console errors:", errs[:8])
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
