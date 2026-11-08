/* ============================================================
   App — wiring for the whole site.
   ============================================================ */

(function () {
  'use strict';

  var M = window.RFB_MANIFEST;
  var byId = {};
  M.artifacts.forEach(function (a) { byId[a.id] = a; });

  var $ = function (s, r) { return (r || document).querySelector(s); };
  var $$ = function (s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); };
  var el = function (tag, cls, html) {
    var n = document.createElement(tag);
    if (cls) n.className = cls;
    if (html !== undefined) n.innerHTML = html;
    return n;
  };

  /* Manifest rows carry an English and a Portuguese wording; pick by language. */
  var isPt = function () { return (window.rfbLang && window.rfbLang() === 'pt'); };
  var locRow = function (row, key) {
    var v = isPt() ? row[key + 'Pt'] : row[key];
    return (v === undefined || v === null || v === '') ? (row[key] || '') : v;
  };

  /* Three states, not two: between the two readings there is a stretch of the
     half-turn where neither face is readable. Saying so is more honest than a
     binary A/B switch. */
  var rotationState = function (deg) {
    var a = Math.abs(((deg % 360) + 360) % 360);
    if (a > 180) a = 360 - a;                 /* fold onto [0,180] */
    if (a <= 15) return 'up';
    if (a >= 165) return 'down';
    return 'mid';
  };
  window.rfbRotationState = rotationState;

  /* Manifest text is plain data, not markup: escape it before it goes into
     innerHTML (the prompt changelists legitimately mention <title> etc.). */
  var esc = function (s) {
    if (s === null || s === undefined) return '';
    return String(s)
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;');
  };

  /* ===========================================================
     Navigation, language, scroll spy
     =========================================================== */
  function initChrome() {
    var navToggle = $('#nav-toggle');
    var nav = $('#site-nav');
    if (navToggle && nav) {
      navToggle.addEventListener('click', function () {
        var open = nav.classList.toggle('is-open');
        navToggle.setAttribute('aria-expanded', String(open));
      });
      nav.addEventListener('click', function (e) {
        if (e.target.tagName === 'A') {
          nav.classList.remove('is-open');
          navToggle.setAttribute('aria-expanded', 'false');
        }
      });
    }

    $$('.lang-switch button').forEach(function (b) {
      b.addEventListener('click', function () {
        window.applyI18n(b.getAttribute('data-lang'));
      });
    });

    /* ?lang= in the URL wins, then the stored preference, then the browser */
    window.applyI18n(window.rfbInitialLang(), true);

    /* scroll spy */
    var sections = $$('main section[id]');
    var links = {};
    $$('.site-nav a').forEach(function (a) {
      var id = a.getAttribute('href').replace('#', '');
      if (id) links[id] = a;
    });
    if ('IntersectionObserver' in window) {
      var spy = new IntersectionObserver(function (entries) {
        entries.forEach(function (en) {
          if (en.isIntersecting) {
            Object.keys(links).forEach(function (k) { links[k].classList.remove('is-active'); });
            if (links[en.target.id]) links[en.target.id].classList.add('is-active');
          }
        });
      }, { rootMargin: '-45% 0px -50% 0px' });
      sections.forEach(function (s) { spy.observe(s); });
    }

    var top = $('#to-top');
    if (top) {
      window.addEventListener('scroll', function () {
        top.classList.toggle('is-visible', window.scrollY > 600);
      }, { passive: true });
      top.addEventListener('click', function () {
        window.scrollTo({ top: 0, behavior: 'smooth' });
      });
    }
  }

  /* ===========================================================
     HERO
     =========================================================== */
  function initHero() {
    var img = $('#hero-img');
    var stage = $('#hero-stage');
    var hint = $('#hero-hint');
    var flip = $('#hero-flip');
    if (!img) return;

    var stateEl = $('#hero-state');

    function paintState(deg) {
      if (!stateEl) return;
      var st = rotationState(deg);
      stateEl.textContent = window.t('rot.' + st);
      stateEl.classList.toggle('is-mid', st === 'mid');
      stateEl.classList.toggle('is-b', st === 'down');
    }

    var rotator = new window.Rotator($('#hero-rotor'), {
      onStart: function () { if (hint) hint.classList.add('is-hidden'); },
      onChange: paintState
    });
    window.heroRotator = rotator;
    paintState(0);

    var hintTimer = setTimeout(function () {
      if (hint) hint.classList.add('is-hidden');
    }, 5200);

    if (flip) {
      flip.addEventListener('click', function () {
        clearTimeout(hintTimer);
        if (hint) hint.classList.add('is-hidden');
        rotator.animateTo(rotator.angle > 90 ? 0 : 180, 900);
      });
    }

    /* subtle entrance */
    if (stage) {
      stage.style.opacity = '0';
      stage.style.transform = 'translateY(14px)';
      setTimeout(function () {
        stage.style.transition = 'opacity .7s ease, transform .7s cubic-bezier(.2,.7,.3,1)';
        stage.style.opacity = '1';
        stage.style.transform = 'none';
      }, 120);
    }
  }

  /* ===========================================================
     PLAYGROUND
     =========================================================== */
  var pg = { rot: null, cur: null, playing: false, mode: 'single' };

  function initPlayground() {
    var sel = $('#pg-select');
    var img = $('#pg-img'), imgB = $('#pg-img-b');
    var imgX1 = $('#pg-img-x1'), imgX2 = $('#pg-img-x2');
    var stage = $('#pg-stage');
    var range = $('#pg-range');
    var out = $('#pg-angle');
    var pgState = $('#pg-state');
    var playBtn = $('#pg-play');
    if (!sel) return;

    /* group the options */
    var groups = {};
    M.artifacts.forEach(function (a) {
      var key = a.group === 'round' ? 'round-' + a.round : 'baseline';
      if (!groups[key]) groups[key] = [];
      groups[key].push(a);
    });

    var order = ['round-0', 'round-1', 'round-2', 'round-3', 'round-4', 'baseline'];
    order.forEach(function (g) {
      if (!groups[g]) return;
      var og = el('optgroup');
      og.label = groups[g][0].roundLabel + (g === 'baseline' ? '' : '');
      groups[g].forEach(function (a) {
        var o = el('option');
        o.value = a.id;
        o.textContent = a.modelLabel + ' — ' + (a.title || a.id);
        og.appendChild(o);
      });
      sel.appendChild(og);
    });

    sel.addEventListener('change', function () { setArtifact(sel.value); });

    $('#pg-prev').addEventListener('click', function () { step(-1); });
    $('#pg-next').addEventListener('click', function () { step(1); });
    $('#pg-random').addEventListener('click', function () {
      var ids = M.artifacts.map(function (a) { return a.id; });
      var id = ids[Math.floor(Math.random() * ids.length)];
      sel.value = id;
      setArtifact(id);
    });

    pg.rot = new window.Rotator($('#pg-rotor'), {
      onChange: function (deg) {
        if (range && Math.round(+range.value) !== Math.round(deg)) range.value = String(Math.round(deg));
        if (out) out.textContent = Math.round(deg) + '°';
        if (pgState) {
          var st = rotationState(deg);
          pgState.textContent = window.t('rot.' + st);
          pgState.classList.toggle('is-mid', st === 'mid');
          pgState.classList.toggle('is-b', st === 'down');
        }
        var cross = $('#play-cross');
        if (cross) {
          cross.style.setProperty('--rot', deg.toFixed(2) + 'deg');
        }
      }
    });

    if (range) {
      range.addEventListener('input', function () {
        if (pg.playing) togglePlay(false);
        pg.rot.set(+range.value);
      });
    }
    if (playBtn) playBtn.addEventListener('click', function () { togglePlay(!pg.playing); });

    $('#pg-snap90').addEventListener('click', function () { snap(90); });
    $('#pg-snap180').addEventListener('click', function () { snap(180); });

    ['pg-mode-single', 'pg-mode-split', 'pg-mode-cross'].forEach(function (id) {
      var b = document.getElementById(id);
      if (!b) return;
      b.addEventListener('click', function () {
        var mode = b.id.replace('pg-mode-', '');
        setMode(mode);
      });
    });

    setArtifact('r04-glm-5.3-flash');
  }

  function setMode(mode) {
    pg.mode = mode;
    var stage = $('#pg-stage');
    if (stage) stage.dataset.mode = mode;
    $$('.play-modes .chip').forEach(function (c) {
      c.classList.toggle('is-active', c.id === 'pg-mode-' + mode);
    });
    var paneA = $('.play-pane[data-pane="a"]');
    var paneB = $('.play-pane[data-pane="b"]');
    var cross = $('#play-cross');
    if (paneA) paneA.hidden = (mode === 'cross');
    if (paneB) paneB.hidden = (mode !== 'split');
    if (cross) cross.hidden = (mode !== 'cross');
  }

  function snap(deg) {
    if (pg.playing) togglePlay(false);
    pg.rot.animateTo(deg, 620);
  }

  function togglePlay(on) {
    pg.playing = on;
    var btn = $('#pg-play');
    if (btn) {
      btn.classList.toggle('is-playing', on);
      btn.innerHTML = on
        ? '<svg viewBox="0 0 24 24" width="18" height="18" fill="currentColor"><rect x="6" y="5" width="4" height="14" rx="1"/><rect x="14" y="5" width="4" height="14" rx="1"/></svg>'
        : '<svg viewBox="0 0 24 24" width="18" height="18" fill="currentColor"><path d="M8 5v14l11-7z"/></svg>';
    }
    pg.rot.spin(on);
  }

  function step(dir) {
    var ids = M.artifacts.map(function (a) { return a.id; });
    var i = ids.indexOf(pg.cur ? pg.cur.id : ids[0]);
    var n = ids[(i + dir + ids.length) % ids.length];
    var sel = $('#pg-select');
    if (sel) sel.value = n;
    setArtifact(n);
  }

  function setArtifact(id) {
    var a = byId[id];
    if (!a) return;
    pg.cur = a;
    var selEl = $('#pg-select');
    if (selEl && selEl.value !== id) selEl.value = id;
    var img = $('#pg-img'), imgB = $('#pg-img-b'), imgX1 = $('#pg-img-x1'), imgX2 = $('#pg-img-x2');
    [img, imgB, imgX1, imgX2].forEach(function (n) { if (n) n.src = a.file; });
    if (pg.rot) pg.rot.set(0);
    renderMeta(a);
  }

  function verdictLabel(v) {
    if (v === 'pass') return window.t('gal.verdict.pass');
    if (v === 'fail') return window.t('gal.verdict.fail');
    return window.t('gal.verdict.none');
  }

  function quoteFor(a) {
    if (a.group === 'baseline') return null;
    if (a.round === 1) {
      if (a.id.indexOf('deepseek') >= 0) return window.t('quote.r01-deepseek-v4.1-flash');
      if (a.id.indexOf('glm') >= 0) return window.t('quote.r01-glm-5.3-flash');
      return window.t('quote.r01-minimax-m3.1-flash');
    }
    if (a.round === 2) return window.t('quote.r02');
    if (a.round === 3) return window.t('quote.r03');
    if (a.round === 4) return window.t('quote.r04');
    return null;
  }

  function renderMeta(a) {
    var box = $('#pg-meta');
    if (!box) return;
    var badgeCls = a.verdict === 'pass' ? 'badge-pass' : (a.verdict === 'fail' ? 'badge-fail' : 'badge-none');

    var rows = [];
    function row(k, v) { if (v !== null && v !== undefined && v !== '') rows.push('<div><dt>' + k + '</dt><dd>' + v + '</dd></div>'); }

    row(window.t('meta.round'), locRow(a, 'roundLabel'));
    row(window.t('meta.prompt'), 'v' + String(a.prompt).replace(/^v/, ''));
    row(window.t('meta.model'), a.modelLabel + ' <span style="color:var(--ink-faint)">· ' + a.vendor + '</span>');
    if (a.title) row(window.t('meta.title'), '<em>' + esc(a.title) + '</em>');
    if (a.event) row(window.t('meta.event'), esc(a.event));
    if (a.settings) row(window.t('meta.settings'), a.settings);
    if (a.tokensIn) row(window.t('meta.tokens'), a.tokensIn.toLocaleString('en-US') + ' in / ' + a.tokensOut.toLocaleString('en-US') + ' out');
    if (a.cost !== null && a.cost !== undefined) row(window.t('meta.cost'), '$' + a.cost.toFixed(4));
    if (a.turns) row(window.t('meta.turns'), a.turns + ' / ' + a.toolCalls + ' / ' + a.renders);
    if (a.rubric !== undefined && a.rubric !== null) row(window.t('meta.rubric'), a.rubric + ' / 8');
    if (a.david1) row(window.t('meta.judge'), a.david1 + ' / ' + a.david2);
    if (a.impression) row(window.t('meta.impression'), esc(a.impression));

    var q = quoteFor(a);
    var rho = (window.RFB_RHO || {})[a.id];

    box.innerHTML =
      '<span class="meta-badge ' + badgeCls + '">' + verdictLabel(a.verdict) + '</span>' +
      '<h3 class="meta-title">' + a.modelLabel + '</h3>' +
      '<p class="meta-sub">' + locRow(a, 'roundLabel') + ' · prompt v' + String(a.prompt).replace(/^v/, '') +
      (a.kind === 'raster' ? ' · raster' : ' · SVG') + '</p>' +
      (q ? '<blockquote class="meta-quote">' + q + '</blockquote>' : '') +
      '<dl class="meta-rows">' + rows.join('') + '</dl>' +
      (rho ? '<dl class="meta-rows"><div><dt>ρ</dt><dd>' + rho.rho.toFixed(4) +
        ' <span style="color:var(--ink-faint)">(' + esc(window.t('meta.rhoRef')) + ')</span></dd></div></dl>' : '') +
      (a.note ? '<p class="note" style="margin-bottom:14px">' + esc(a.note) + '</p>' : '') +
      '<div class="meta-links">' +
      '<a href="https://github.com/ClaudioDrews/reversible-faces-benchmark/blob/main/' + a.repoPath +
      '" target="_blank" rel="noopener">' + esc(window.t('meta.repoFile')) + ' ↗</a>' +
      '</div>';
  }

  /* ===========================================================
     GALLERY
     =========================================================== */
  var galFilter = 'all';

  function initGallery() {
    var grid = $('#gal-grid');
    var filters = $('#gal-filters');
    if (!grid) return;

    renderGalFilters();
    renderGallery();
  }

  function renderGalFilters() {
    var filters = $('#gal-filters');
    if (!filters) return;
    var FILTERS = [
      { key: 'all', label: 'gal.filter.all' },
      { key: 'round', label: 'gal.filter.round' },
      { key: 'baseline', label: 'gal.filter.baseline' },
      { key: 'pass', label: 'gal.filter.pass' },
      { key: 'fail', label: 'gal.filter.fail' },
      { key: 'svg', label: 'gal.filter.svg' },
      { key: 'raster', label: 'gal.filter.raster' },
      { key: 'r0', label: 'gal.filter.r0' },
      { key: 'r1', label: 'gal.filter.r1' },
      { key: 'r2', label: 'gal.filter.r2' },
      { key: 'r3', label: 'gal.filter.r3' },
      { key: 'r4', label: 'gal.filter.r4' }
    ];
    filters.innerHTML = '';
    FILTERS.forEach(function (f) {
      var b = el('button', 'chip' + (f.key === galFilter ? ' is-active' : ''));
      b.type = 'button';
      b.textContent = window.t(f.label);
      b.dataset.filter = f.key;
      b.addEventListener('click', function () {
        galFilter = f.key;
        $$('.chip', filters).forEach(function (c) { c.classList.toggle('is-active', c === b); });
        renderGallery();
      });
      filters.appendChild(b);
    });
  }

  function matches(a, f) {
    switch (f) {
      case 'all': return true;
      case 'round': return a.group === 'round';
      case 'baseline': return a.group === 'baseline';
      case 'pass': return a.verdict === 'pass';
      case 'fail': return a.verdict === 'fail';
      case 'svg': return a.kind === 'svg';
      case 'raster': return a.kind === 'raster';
      default:
        if (f.charAt(0) === 'r' && a.group === 'round') return String(a.round) === f.slice(1);
        return true;
    }
  }

  function renderGallery() {
    var grid = $('#gal-grid');
    if (!grid) return;
    grid.innerHTML = '';
    var list = M.artifacts.filter(function (a) { return matches(a, galFilter); });
    var empty = $('#gal-empty');
    if (empty) empty.hidden = list.length > 0;

    list.forEach(function (a) {
      var card = el('button', 'gal-card');
      card.type = 'button';
      var flagCls = a.verdict === 'pass' ? 'is-pass' : (a.verdict === 'fail' ? 'is-fail' : '');
      var sub = a.group === 'round'
        ? locRow(a, 'roundLabel') + ' · prompt v' + String(a.prompt).replace(/^v/, '')
        : 'Baseline · ' + (a.prompt === 'shared-eyes' ? window.t('gal.promptShared') : 'prompt v5');
      card.innerHTML =
        '<div class="gal-thumb">' +
        '<span class="gal-flag ' + flagCls + '">' + verdictLabel(a.verdict) + '</span>' +
        '<img src="' + a.file + '" alt="' + a.modelLabel + ' — leitura A" loading="lazy">' +
        '</div>' +
        '<div class="gal-body">' +
        '<span class="gal-model">' + a.modelLabel + '</span>' +
        '<span class="gal-sub">' + sub + '</span>' +
        (a.title ? '<span class="gal-sub"><em>' + esc(a.title) + '</em></span>' : '') +
        '<span class="gal-note">' + esc(a.note) + '</span>' +
        '</div>';
      card.addEventListener('click', function () {
        var sel = $('#pg-select');
        if (sel) sel.value = a.id;
        setArtifact(a.id);
        var p = document.getElementById('playground');
        if (p) p.scrollIntoView({ behavior: 'smooth', block: 'start' });
      });
      grid.appendChild(card);
    });
  }

  /* ===========================================================
     GEOMETRY TABS
     =========================================================== */
  function initTabs() {
    var tabs = $('#geo-tabs');
    if (!tabs) return;
    tabs.addEventListener('click', function (e) {
      var b = e.target.closest('.tab');
      if (!b) return;
      $$('.tab', tabs).forEach(function (t) { t.classList.toggle('is-active', t === b); });
      $$('.tab-panel').forEach(function (p) {
        p.classList.toggle('is-active', p.dataset.panel === b.dataset.tab);
      });
      window.rfbRedrawGeometry();
    });
  }

  /* ===========================================================
     TIMELINE (rounds)
     =========================================================== */
  function initTimeline() {
    renderTimeline();
  }

  function renderTimeline() {
    var tl = $('#timeline');
    if (!tl) return;
    tl.innerHTML = '';
    var rounds = [0, 1, 2, 3, 4];
    rounds.forEach(function (r) {
      var info = M.rounds[String(r)];
      var arts = M.artifacts.filter(function (a) { return a.group === 'round' && a.round === r && a.evaluated !== false; });
      var item = el('article', 'tl-item');

      var side = el('div', 'tl-side');
      side.innerHTML =
        '<span class="tl-round">' + window.t('round.' + r + '.label') + '</span>' +
        '<span class="tl-prompt">prompt v' + info.prompt.replace(/^v/, '') + '</span>' +
        '<span class="tl-verdict">' + window.t('round.' + r + '.verdict') + '</span>';

      var main = el('div', 'tl-main');
      var changes = el('ul', 'tl-changes');
      var nch = (r === 1) ? 2 : 1;
      for (var i = 0; i < nch; i++) {
        var key = 'round.' + r + '.change' + i;
        if (window.t(key) !== key) changes.appendChild(el('li', null, window.t(key)));
      }
      main.innerHTML = '<h3>' + window.t('round.' + r + '.headline') + '</h3>' +
        '<p class="tl-lesson">' + window.t('round.' + r + '.lesson') + '</p>';

      var art = el('div', 'tl-art');
      arts.forEach(function (a) {
        var fig = el('figure');
        fig.innerHTML =
          '<div class="rotor"><img src="' + a.file + '" alt="' + a.modelLabel + ' — leitura A" loading="lazy"></div>' +
          '<figcaption>' + esc(a.modelLabel) + '</figcaption>';
        art.appendChild(fig);
        var rot = new window.Rotator(fig.querySelector('.rotor'), {});
        fig.querySelector('.rotor').addEventListener('pointerdown', function () { rot.set(0); });
      });
      main.appendChild(changes);
      main.appendChild(art);
      item.appendChild(side);
      item.appendChild(main);
      tl.appendChild(item);
    });
  }

  /* ===========================================================
     PROMPT TABLE
     =========================================================== */
  function initPromptTable() {
    renderPromptTable();
  }

  function renderPromptTable() {
    var tb = $('#prompt-table tbody');
    if (!tb) return;
    tb.innerHTML = '';
    M.promptVersions.forEach(function (p) {
      var tr = el('tr');
      var list = isPt() ? (p.changes_pt || p.changes) : p.changes;
      var changes = list.map(function (c) { return '<li>' + esc(c) + '</li>'; }).join('');
      tr.innerHTML =
        '<td><span class="ver">' + p.version + '</span></td>' +
        '<td>' + esc(isPt() ? (p.used_pt || p.used) : p.used) + '</td>' +
        '<td>' + window.t('pv.' + p.version + '.what') + '<br><span style="color:var(--ink-faint);font-size:.78rem">' +
        p.size_kb + ' KB</span></td>' +
        '<td><ul>' + changes + '</ul></td>' +
        '<td>' + window.t('pv.' + p.version + '.outcome') + '</td>';
      tb.appendChild(tr);
    });
  }

  /* ===========================================================
     BASELINES
     =========================================================== */
  var baseFilter = 'all';
  var baseSort = 'verdict';

  function renderBaseFilters() {
    var filters = $('#base-filters');
    if (!filters) return;
    var FILTERS = [
      { key: 'all', label: 'gal.filter.all' },
      { key: 'text', label: 'base.filter.text' },
      { key: 'raster', label: 'base.filter.raster' },
      { key: 'pass', label: 'gal.filter.pass' },
      { key: 'fail', label: 'gal.filter.fail' }
    ];
    filters.innerHTML = '';
    FILTERS.forEach(function (f) {
      var b = el('button', 'chip' + (f.key === baseFilter ? ' is-active' : ''));
      b.type = 'button';
      b.textContent = window.t(f.label);
      b.addEventListener('click', function () {
        baseFilter = f.key;
        $$('.chip', filters).forEach(function (c) { c.classList.toggle('is-active', c === b); });
        renderBaseTable();
      });
      filters.appendChild(b);
    });
  }

  function initBaselines() {
    renderBaseFilters();

    var sortBtn = $('#base-sort');
    if (sortBtn) {
      sortBtn.addEventListener('click', function () {
        baseSort = baseSort === 'verdict' ? 'rubric' : (baseSort === 'rubric' ? 'model' : 'verdict');
        renderSortLabel();
        renderBaseTable();
      });
    }

    renderBaseStats();
    renderBaseTable();
    renderJudgeChart();
  }

  function renderSortLabel() {
    var fl = $('#base-sort');
    if (!fl) return;
    var names = { verdict: 'base.sortVerdict', rubric: 'base.sortRubric', model: 'base.sortModel' };
    fl.textContent = window.t('base.sort') + ': ' + window.t(names[baseSort]);
  }

  function renderBaseStats() {
    var box = $('#base-stats');
    if (!box) return;
    var baselines = M.artifacts.filter(function (a) { return a.group === 'baseline'; });
    var text = baselines.filter(function (a) { return a.kind === 'svg'; });
    var raster = baselines.filter(function (a) { return a.kind === 'raster'; });
    var textPass = text.filter(function (a) { return a.verdict === 'pass'; }).length;
    var imgFail = raster.filter(function (a) { return a.verdict === 'fail'; }).length;

    var cards = [
      { n: baselines.length, l: window.t('base.stat.total'), cls: '' },
      { n: textPass + '/' + text.length, l: window.t('base.stat.textPass'), cls: 'is-ok' },
      { n: imgFail + '/' + raster.length, l: window.t('base.stat.imgFail'), cls: 'is-bad' }
    ];
    box.innerHTML = '';
    cards.forEach(function (c) {
      var d = el('div', 'stat-card ' + c.cls);
      d.innerHTML = '<div class="stat-num">' + c.n + '</div><div class="stat-label">' + c.l + '</div>';
      box.appendChild(d);
    });
  }

  function renderBaseTable() {
    var tb = $('#base-table tbody');
    if (!tb) return;
    tb.innerHTML = '';

    var list = M.artifacts.filter(function (a) { return a.group === 'baseline'; });
    list = list.filter(function (a) {
      if (baseFilter === 'all') return true;
      if (baseFilter === 'text') return a.kind === 'svg';
      if (baseFilter === 'raster') return a.kind === 'raster';
      if (baseFilter === 'pass') return a.verdict === 'pass';
      if (baseFilter === 'fail') return a.verdict === 'fail';
      return true;
    });

    var rank = { pass: 0, fail: 1, none: 2 };
    list.sort(function (x, y) {
      if (baseSort === 'rubric') return (y.rubric || 0) - (x.rubric || 0) || x.model.localeCompare(y.model);
      if (baseSort === 'model') return x.modelLabel.localeCompare(y.modelLabel);
      return (rank[x.verdict] - rank[y.verdict]) || (y.rubric || 0) - (x.rubric || 0);
    });

    list.forEach(function (a) {
      var tr = el('tr');
      var pillCls = a.verdict === 'pass' ? 'pill-pass' : (a.verdict === 'fail' ? 'pill-fail' : 'pill-none');
      var promptLabel = a.prompt === 'shared-eyes' ? window.t('base.promptShared') : 'v5';
      tr.innerHTML =
        '<td class="id">' + a.id + '</td>' +
        '<td class="model">' + esc(a.modelLabel) + '</td>' +
        '<td class="prompttype">' + promptLabel + '</td>' +
        '<td><span class="pill ' + pillCls + '">' + verdictLabel(a.verdict) + '</span></td>' +
        '<td class="rubric">' + (a.rubric !== undefined && a.rubric !== null ? a.rubric : '—') + '</td>' +
        '<td class="rubric">' + (a.david1 || '—') + '</td>' +
        '<td class="rubric">' + (a.david2 || '—') + '</td>' +
        '<td class="impression">' + esc(a.impression) + '</td>';

      var detail = el('tr', 'base-detail');
      detail.hidden = true;
      var inner = el('td');
      inner.colSpan = 8;
      var dInner = el('div', 'base-detail-inner');
      dInner.innerHTML =
        '<div class="rotor"><img src="' + a.file + '" alt="' + a.modelLabel + ' — leitura A"></div>' +
        '<div>' +
        '<h5>' + esc(a.modelLabel) + '</h5>' +
        '<dl>' +
        '<dt>' + window.t('base.event') + '</dt><dd>' + esc(a.event || '—') + '</dd>' +
        '<dt>' + window.t('base.titleField') + '</dt><dd>' + esc(a.title || '—') + '</dd>' +
        '<dt>' + window.t('base.note') + '</dt><dd>' + esc(a.note || '—') + '</dd>' +
        '<dt>' + window.t('base.impression') + '</dt><dd>' + esc(a.impression || '—') + '</dd>' +
        '<dt>' + window.t('base.src') + '</dt><dd><a href="https://github.com/ClaudioDrews/reversible-faces-benchmark/blob/main/' +
        esc(a.repoPath) + '" target="_blank" rel="noopener">' + esc(a.repoPath) + ' ↗</a></dd>' +
        '</dl></div>';
      inner.appendChild(dInner);
      detail.appendChild(inner);

      tr.addEventListener('click', function () {
        var open = !detail.hidden;
        detail.hidden = open;
        tr.classList.toggle('is-open', !open);
        if (!open) {
          var rot = new window.Rotator(dInner.querySelector('.rotor'), {});
          void rot;
        }
      });

      tb.appendChild(tr);
      tb.appendChild(detail);
    });
  }

  function renderJudgeChart() {
    var box = $('#judge-chart');
    if (!box) return;
    box.innerHTML = '';
    M.judges.forEach(function (j) {
      var pct = Math.round(j.rate * 100);
      var row = el('div', 'judge-row');
      var jName = isPt() ? (j.name_pt || j.name) : j.name;
      var jNote = isPt() ? (j.note_pt || j.note) : j.note;
      row.innerHTML =
        '<div><strong>' + esc(jName) + '</strong><br><span class="judge-note">' + esc(jNote) + '</span></div>' +
        '<div class="judge-bar"><i style="width:' + pct + '%"></i></div>' +
        '<div class="val">' + j.agrees + '</div>';
      box.appendChild(row);
    });
  }

  /* ===========================================================
     FAILURE ATLAS
     =========================================================== */
  function initFailures() {
    var grid = $('#failure-grid');
    if (!grid) return;
    M.failureModes.forEach(function (f) {
      var card = el('article', 'failure-card');
      var isPt = (window.rfbLang && window.rfbLang() === 'pt');
      var fName = isPt ? (f.name_pt || f.name) : f.name;
      var fSym = isPt ? (f.symptom_pt || f.symptom) : f.symptom;
      card.innerHTML = '<h4>' + esc(fName) + '</h4><p>' + esc(fSym) + '</p>';
      var thumbs = el('div', 'failure-thumbs');
      f.examples.forEach(function (id) {
        var a = byId[id];
        if (!a) return;
        var fig = el('figure');
        fig.innerHTML =
          '<div class="rotor thumb-rotor"><img src="' + a.file + '" alt="' + a.modelLabel + ' — leitura A" loading="lazy"></div>' +
          '<figcaption>' + a.modelLabel + '</figcaption>';
        thumbs.appendChild(fig);
        new window.Rotator(fig.querySelector('.rotor'), {});
      });
      card.appendChild(thumbs);
      grid.appendChild(card);
    });
  }

  /* ===========================================================
     METHOD — caveats
     =========================================================== */
  function initCaveats() {
    renderCaveats();
  }

  function renderCaveats() {
    var list = $('#caveat-list');
    if (!list) return;
    list.innerHTML = '';
    for (var i = 1; i <= 11; i++) {
      var k = 'caveat.' + i;
      if (window.t(k) === k) continue;
      list.appendChild(el('li', null, window.t(k)));
    }
  }

  /* ===========================================================
     BOOT
     =========================================================== */
  /* The rotation readouts carry the current angle, so they must be repainted
     after every language change — otherwise applyI18n() would reset them to
     the "upright" wording regardless of the actual angle. */
  function repaintRotationState() {
    var hero = $('#hero-state');
    if (hero && window.heroRotator) {
      var st = rotationState(window.heroRotator.angle);
      hero.textContent = window.t('rot.' + st);
      hero.classList.toggle('is-mid', st === 'mid');
      hero.classList.toggle('is-b', st === 'down');
    }
    var pgEl = $('#pg-state');
    if (pgEl && pg.rot) {
      var p2 = rotationState(pg.rot.angle);
      pgEl.textContent = window.t('rot.' + p2);
      pgEl.classList.toggle('is-mid', p2 === 'mid');
      pgEl.classList.toggle('is-b', p2 === 'down');
    }
  }

  function renderAll() {
    renderMeta(pg.cur || M.artifacts[0]);
    renderGalFilters();
    renderGallery();
    renderBaseFilters();
    renderBaseStats();
    renderBaseTable();
    renderTimeline();
    renderPromptTable();
    renderCaveats();
    if (window.rfbReloadSymmetry) window.rfbReloadSymmetry();
    window.rfbRedrawGeometry();
    repaintRotationState();
  }

  function boot() {
    /* Each section is initialised independently: a failure in one must not
       take the rest of the site down with it. */
    var steps = [
      ['chrome', initChrome],
      ['hero', initHero],
      ['playground', initPlayground],
      ['gallery', initGallery],
      ['tabs', initTabs],
      ['timeline', initTimeline],
      ['prompt-table', initPromptTable],
      ['baselines', initBaselines],
      ['failures', initFailures],
      ['caveats', initCaveats],
      ['geometry', function () { if (window.rfbInitGeometry) window.rfbInitGeometry(); }],
      ['symmetry', function () { if (window.rfbInitSymmetry) window.rfbInitSymmetry(); }]
    ];

    steps.forEach(function (s) {
      try {
        s[1]();
      } catch (err) {
        if (window.console && console.error) {
          console.error('[rfb] failed to initialise "' + s[0] + '":', err);
        }
      }
    });

    window.rfbOnLanguageChange = function () {
      try { renderAll(); } catch (err) {
        if (window.console && console.error) console.error('[rfb] re-render failed:', err);
      }
      renderSortLabel();
    };

    var rt;
    window.addEventListener('resize', function () {
      clearTimeout(rt);
      rt = setTimeout(function () { window.rfbRedrawGeometry(); }, 180);
    });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', boot);
  } else {
    boot();
  }
})();
