/* ============================================================
   Geometry lab — four interactive canvases.

   The drawing used throughout is a faithful realisation of the
   repository's canonical ladder (docs/geometry.md, docs/how-it-works.md):
   every feature sits exactly where the canon puts it, so rotating it by
   180 degrees really does produce the second reading.
   ============================================================ */

(function () {
  'use strict';

  var INK = '#1b1917', ACCENT = '#b23f26', TEAL = '#2c5f66', FAINT = 'rgba(27,25,23,.28)';
  var M = window.RFB_MANIFEST;

  function css(name, fallback) {
    var v = getComputedStyle(document.documentElement).getPropertyValue(name);
    return (v && v.trim()) || fallback;
  }

  function fitCanvas(cv) {
    var dpr = Math.min(window.devicePixelRatio || 1, 2);
    var w = cv.clientWidth || cv.width;
    var h = (cv.width / cv.height) * (cv.clientWidth || cv.width);
    var ratio = cv.getAttribute('width') / cv.getAttribute('height');
    h = w / ratio;
    cv.width = Math.round(w * dpr);
    cv.height = Math.round(h * dpr);
    cv.style.height = h + 'px';
    var ctx = cv.getContext('2d');
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    return { ctx: ctx, w: w, h: h };
  }

  /* page (1000x1000) -> canvas */
  function mapper(w, h, box) {
    var s = Math.min(box.w / 1000, box.h / 1000);
    var ox = box.x + (box.w - 1000 * s) / 2;
    var oy = box.y + (box.h - 1000 * s) / 2;
    return {
      s: s, ox: ox, oy: oy,
      x: function (px) { return ox + px * s; },
      y: function (py) { return oy + py * s; },
      l: function (px) { return px * s; }
    };
  }

  /* ---------------------------------------------------------------
     The canonical reversible face.
     Page coordinates follow the repository's canon exactly.
     --------------------------------------------------------------- */
  var CANON = {
    pompom: 110, crown: 200, dome: 320, brim: 350, hairline: 380,
    brow: 452, eye: 500, lid: 548, nose: 650, mouth: 680, chin: 800, collar: 890
  };

  function drawFace(ctx, m, opt) {
    opt = opt || {};
    var lw = Math.max(1.2, m.l(7));
    var lwFine = Math.max(1, m.l(4.5));
    ctx.save();
    ctx.lineCap = 'round';
    ctx.lineJoin = 'round';
    ctx.strokeStyle = opt.ink || INK;
    ctx.lineWidth = lw;

    /* --- head outline --- */
    ctx.beginPath();
    ctx.ellipse(m.x(500), m.y(500), m.l(200), m.l(300), 0, 0, Math.PI * 2);
    ctx.stroke();

    /* --- hat: dome, brim, crown, pompom --- */
    ctx.lineWidth = lw;
    ctx.beginPath();
    ctx.moveTo(m.x(312), m.y(CANON.brim));
    ctx.bezierCurveTo(m.x(330), m.y(CANON.dome), m.x(400), m.y(CANON.crown), m.x(500), m.y(CANON.crown));
    ctx.bezierCurveTo(m.x(600), m.y(CANON.crown), m.x(670), m.y(CANON.dome), m.x(688), m.y(CANON.brim));
    ctx.stroke();

    /* hat band = the "dome" rung (mouth of B) */
    ctx.lineWidth = Math.max(1.6, m.l(5.5));
    ctx.beginPath();
    ctx.moveTo(m.x(340), m.y(CANON.dome));
    ctx.quadraticCurveTo(m.x(500), m.y(CANON.dome - 16), m.x(660), m.y(CANON.dome));
    ctx.stroke();

    /* brim = the nose of B */
    ctx.lineWidth = lw;
    ctx.beginPath();
    ctx.moveTo(m.x(300), m.y(CANON.brim));
    ctx.quadraticCurveTo(m.x(500), m.y(CANON.brim + 14), m.x(700), m.y(CANON.brim));
    ctx.stroke();

    /* pompom = the collar of B */
    ctx.beginPath();
    ctx.moveTo(m.x(500), m.y(CANON.crown - 4));
    ctx.lineTo(m.x(500), m.y(CANON.pompom + 16));
    ctx.stroke();
    ctx.beginPath();
    ctx.arc(m.x(500), m.y(CANON.pompom), m.l(20), 0, Math.PI * 2);
    ctx.stroke();

    /* --- hairline = the nose bridge of B --- */
    ctx.lineWidth = lwFine;
    ctx.beginPath();
    ctx.moveTo(m.x(390), m.y(CANON.hairline));
    ctx.quadraticCurveTo(m.x(440), m.y(CANON.hairline - 16), m.x(500), m.y(CANON.hairline - 4));
    ctx.quadraticCurveTo(m.x(560), m.y(CANON.hairline - 16), m.x(610), m.y(CANON.hairline));
    ctx.stroke();

    /* --- brows = the under-eye bags of B --- */
    ctx.lineWidth = lwFine;
    ctx.beginPath();
    ctx.moveTo(m.x(388), m.y(CANON.brow));
    ctx.quadraticCurveTo(m.x(420), m.y(CANON.brow - 14), m.x(452), m.y(CANON.brow - 2));
    ctx.moveTo(m.x(548), m.y(CANON.brow));
    ctx.quadraticCurveTo(m.x(580), m.y(CANON.brow - 14), m.x(612), m.y(CANON.brow - 2));
    ctx.stroke();

    /* --- shared eyes --- */
    /* NOTE: each arc needs its own path: two arcs in one path are joined by a
       straight line, which would draw a false stroke between the eyes. */
    ctx.lineWidth = lw;
    ctx.beginPath();
    ctx.arc(m.x(418), m.y(CANON.eye), m.l(26), 0, Math.PI * 2);
    ctx.stroke();
    ctx.beginPath();
    ctx.arc(m.x(582), m.y(CANON.eye), m.l(26), 0, Math.PI * 2);
    ctx.stroke();
    ctx.fillStyle = opt.ink || INK;
    ctx.beginPath();
    ctx.arc(m.x(418), m.y(CANON.eye), m.l(9), 0, Math.PI * 2);
    ctx.fill();
    ctx.beginPath();
    ctx.arc(m.x(582), m.y(CANON.eye), m.l(9), 0, Math.PI * 2);
    ctx.fill();

    /* --- lower lids = the brows of B --- */
    ctx.lineWidth = lwFine;
    ctx.beginPath();
    ctx.moveTo(m.x(392), m.y(CANON.lid));
    ctx.quadraticCurveTo(m.x(418), m.y(CANON.lid + 16), m.x(446), m.y(CANON.lid + 2));
    ctx.moveTo(m.x(554), m.y(CANON.lid));
    ctx.quadraticCurveTo(m.x(582), m.y(CANON.lid + 16), m.x(610), m.y(CANON.lid + 2));
    ctx.stroke();

    /* --- nose = the hat brim of B --- */
    /* the nose bridge starts just under the eye line and the tip lands on the
       nose rung (+0.25 H); it shares that stroke with B's hat brim. */
    ctx.lineWidth = lw;
    ctx.beginPath();
    ctx.moveTo(m.x(500), m.y(CANON.lid + 18));
    ctx.bezierCurveTo(m.x(492), m.y(CANON.nose - 52), m.x(484), m.y(CANON.nose - 18), m.x(500), m.y(CANON.nose));
    ctx.bezierCurveTo(m.x(516), m.y(CANON.nose - 18), m.x(508), m.y(CANON.nose - 52), m.x(500), m.y(CANON.lid + 18));
    ctx.stroke();

    /* --- mouth = the hat band of B --- */
    ctx.lineWidth = lw;
    ctx.beginPath();
    ctx.moveTo(m.x(436), m.y(CANON.mouth - 14));
    ctx.quadraticCurveTo(m.x(500), m.y(CANON.mouth + 20), m.x(564), m.y(CANON.mouth - 14));
    ctx.stroke();

    /* --- collar = the pompom of B --- */
    ctx.lineWidth = lw;
    ctx.beginPath();
    ctx.moveTo(m.x(392), m.y(CANON.collar));
    ctx.quadraticCurveTo(m.x(500), m.y(CANON.collar - 30), m.x(608), m.y(CANON.collar));
    ctx.stroke();
    ctx.beginPath();
    ctx.moveTo(m.x(500), m.y(CANON.chin - 20));
    ctx.lineTo(m.x(500), m.y(CANON.collar - 12));
    ctx.stroke();

    ctx.restore();
  }

  function drawPageFrame(ctx, m, label) {
    ctx.save();
    ctx.strokeStyle = FAINT;
    ctx.lineWidth = 1;
    ctx.strokeRect(m.x(0), m.y(0), m.l(1000), m.l(1000));
    ctx.strokeStyle = 'rgba(27,25,23,.09)';
    ctx.beginPath();
    ctx.moveTo(m.x(500), m.y(0)); ctx.lineTo(m.x(500), m.y(1000));
    ctx.moveTo(m.x(0), m.y(500)); ctx.lineTo(m.x(1000), m.y(500));
    ctx.stroke();
    if (label) {
      ctx.fillStyle = 'rgba(27,25,23,.45)';
      ctx.font = '11px ' + css('--mono', 'monospace');
      ctx.textAlign = 'left';
      ctx.fillText(label, m.x(8), m.y(-8));
    }
    ctx.restore();
  }

  /* ===========================================================
     TAB 1 — the half-turn
     =========================================================== */
  function initHalfTurn() {
    var cv = document.getElementById('ht-canvas');
    if (!cv) return;
    var facts = document.getElementById('ht-facts');
    var p = { x: 620, y: 300 };
    var dragging = false;

    function render() {
      var f = fitCanvas(cv), ctx = f.ctx, w = f.w, h = f.h;
      ctx.clearRect(0, 0, w, h);
      var box = { x: 22, y: 38, w: Math.min(w * 0.60, h - 66), h: h - 66 };
      var m = mapper(w, h, box);

      drawPageFrame(ctx, m, 'page 1000 × 1000');

      /* the drawing, upright */
      ctx.save();
      ctx.globalAlpha = 0.95;
      drawFace(ctx, m, { ink: INK });
      ctx.restore();

      /* the same drawing, rotated 180 */
      ctx.save();
      ctx.globalAlpha = 0.30;
      ctx.translate(m.x(500), m.y(500));
      ctx.rotate(Math.PI);
      ctx.translate(-m.x(500), -m.y(500));
      drawFace(ctx, m, { ink: TEAL });
      ctx.restore();

      /* the centre */
      ctx.save();
      ctx.fillStyle = INK;
      ctx.beginPath();
      ctx.arc(m.x(500), m.y(500), 3.2, 0, Math.PI * 2);
      ctx.fill();
      ctx.fillStyle = 'rgba(27,25,23,.6)';
      ctx.font = '11px ' + css('--mono', 'monospace');
      ctx.textAlign = 'left';
      ctx.fillText('C = (500, 500)', m.x(10), m.y(992));
      ctx.restore();

      /* the point and its image */
      var rx = 1000 - p.x, ry = 1000 - p.y;
      ctx.save();
      ctx.strokeStyle = 'rgba(178,63,38,.45)';
      ctx.setLineDash([4, 4]);
      ctx.lineWidth = 1.4;
      ctx.beginPath();
      ctx.moveTo(m.x(p.x), m.y(p.y));
      ctx.lineTo(m.x(rx), m.y(ry));
      ctx.stroke();
      ctx.setLineDash([]);

      ctx.fillStyle = ACCENT;
      ctx.beginPath();
      ctx.arc(m.x(p.x), m.y(p.y), 7, 0, Math.PI * 2);
      ctx.fill();
      ctx.fillStyle = TEAL;
      ctx.beginPath();
      ctx.arc(m.x(rx), m.y(ry), 7, 0, Math.PI * 2);
      ctx.fill();

      ctx.font = '600 12px ' + css('--sans', 'sans-serif');
      ctx.fillStyle = ACCENT;
      ctx.textAlign = 'right';
      ctx.fillText('p', m.x(p.x) - 11, m.y(p.y) + 4);
      ctx.fillStyle = TEAL;
      ctx.textAlign = 'left';
      ctx.fillText('R(p)', m.x(rx) + 11, m.y(ry) + 4);
      ctx.restore();

      /* legend */
      var lx = box.x + box.w + 26;
      ctx.save();
      ctx.textAlign = 'left';
      ctx.font = '600 12px ' + css('--sans', 'sans-serif');
      ctx.fillStyle = INK;
      ctx.fillText('R(p) = 2C − p', lx, 64);
      ctx.font = '12px ' + css('--mono', 'monospace');
      ctx.fillStyle = ACCENT;
      ctx.fillText('p   = (' + Math.round(p.x) + ', ' + Math.round(p.y) + ')', lx, 88);
      ctx.fillStyle = TEAL;
      ctx.fillText('R(p)= (' + Math.round(rx) + ', ' + Math.round(ry) + ')', lx, 108);
      ctx.fillStyle = 'rgba(27,25,23,.6)';
      ctx.fillText('R(R(p)) = (' + Math.round(1000 - rx) + ', ' + Math.round(1000 - ry) + ')', lx, 128);

      ctx.font = '11px ' + css('--sans', 'sans-serif');
      ctx.fillStyle = 'rgba(27,25,23,.55)';
      wrap(ctx, 'Drag p. A half-turn moves it to the opposite point; turning again returns p.', lx, 158, Math.max(180, w - lx - 20), 15);

      ctx.fillStyle = INK;
      ctx.beginPath();
      ctx.arc(lx + 5, 232, 6, 0, Math.PI * 2);
      ctx.fillStyle = INK;
      ctx.globalAlpha = 0.22;
      ctx.fill();
      ctx.globalAlpha = 1;
      ctx.fillStyle = 'rgba(27,25,23,.6)';
      ctx.fillText('the same drawing, rotated 180°', lx + 18, 236);
      ctx.restore();

      /* facts */
      if (facts) {
        var ok = (1000 - rx === p.x && 1000 - ry === p.y);
        facts.innerHTML =
          '<div><span>p</span><span>(' + Math.round(p.x) + ', ' + Math.round(p.y) + ')</span></div>' +
          '<div><span>R(p)</span><span>(' + Math.round(rx) + ', ' + Math.round(ry) + ')</span></div>' +
          '<div><span>R(R(p))</span><span class="' + (ok ? 'is-ok' : 'is-bad') + '">' +
          (ok ? '= p ✓' : '≠ p') + '</span></div>' +
          '<div><span>distance p → R(p)</span><span>' +
          Math.round(Math.hypot(rx - p.x, ry - p.y)) + ' px</span></div>' +
          '<div><span>passa por C</span><span class="is-ok">sempre ✓</span></div>';
      }
    }

    function wrap(ctx, text, x, y, maxw, lh) {
      var words = text.split(' '), line = '', yy = y;
      words.forEach(function (word) {
        var test = line ? line + ' ' + word : word;
        if (ctx.measureText(test).width > maxw && line) {
          ctx.fillText(line, x, yy); line = word; yy += lh;
        } else { line = test; }
      });
      if (line) ctx.fillText(line, x, yy);
    }

    function pos(e) {
      var r = cv.getBoundingClientRect();
      var box = { x: 22, y: 38, w: Math.min(r.width * 0.60, r.height - 66), h: r.height - 66 };
      var m = mapper(r.width, r.height, box);
      return { x: (e.clientX - r.left - m.ox) / m.s, y: (e.clientY - r.top - m.oy) / m.s };
    }

    cv.addEventListener('pointerdown', function (e) {
      dragging = true; cv.setPointerCapture(e.pointerId); apply(e); e.preventDefault();
    });
    cv.addEventListener('pointermove', function (e) { if (dragging) apply(e); });
    cv.addEventListener('pointerup', function () { dragging = false; });
    cv.addEventListener('pointercancel', function () { dragging = false; });
    function apply(e) {
      var q = pos(e);
      p.x = Math.max(0, Math.min(1000, q.x));
      p.y = Math.max(0, Math.min(1000, q.y));
      render();
    }

    window.rfbRenderHalfTurn = render;
    render();
  }

  /* ===========================================================
     TAB 2 — the dual-function dictionary
     =========================================================== */
  function initDictionary() {
    var cv = document.getElementById('dict-canvas');
    var table = document.getElementById('dict-table');
    if (!cv || !table) return;
    var active = 1; /* index into M.dictionary */

    var tbody = table.querySelector('tbody');
    M.dictionary.forEach(function (row, i) {
      var tr = document.createElement('tr');
      var ya = row.ya === null ? '—' : (row.ya > 0 ? '+' : '') + row.ya.toFixed(2);
      var pb = row.pb === null ? '—' : (row.pb > 0 ? '+' : '') + row.pb.toFixed(2);
      tr.innerHTML =
        '<td>' + row.a + '<br><span class="y">y = ' + ya + '</span></td>' +
        '<td>' + row.b + '<br><span class="y">y = ' + pb + '</span></td>' +
        '<td>' + (row.note || '') + '</td>';
      tr.addEventListener('click', function () {
        active = i;
        Array.prototype.forEach.call(tbody.children, function (r, j) { r.classList.toggle('is-active', j === i); });
        render();
      });
      tbody.appendChild(tr);
    });
    tbody.children[active].classList.add('is-active');

    function render() {
      var f = fitCanvas(cv), ctx = f.ctx, w = f.w, h = f.h;
      ctx.clearRect(0, 0, w, h);
      var box = { x: 20, y: 34, w: Math.min(w * 0.5, h - 60), h: h - 60 };
      var m = mapper(w, h, box);

      drawPageFrame(ctx, m, null);
      ctx.save();
      drawFace(ctx, m, { ink: INK });
      ctx.restore();

      var row = M.dictionary[active];
      if (row.ya !== null) {
        var pageY = 500 + 600 * row.ya;
        ctx.save();
        /* the band on the page */
        ctx.fillStyle = 'rgba(178,63,38,.14)';
        ctx.fillRect(m.x(0), m.y(pageY) - 16, m.l(1000), 32);
        ctx.strokeStyle = ACCENT;
        ctx.lineWidth = 1.4;
        ctx.beginPath();
        ctx.moveTo(m.x(0), m.y(pageY)); ctx.lineTo(m.x(1000), m.y(pageY));
        ctx.stroke();

        /* labels */
        ctx.font = '600 12px ' + css('--sans', 'sans-serif');
        ctx.textAlign = 'left';
        ctx.fillStyle = ACCENT;
        ctx.fillText('A: ' + row.a, m.x(12), m.y(pageY) - 22);
        ctx.fillStyle = TEAL;
        ctx.fillText('B: ' + row.b, m.x(12), m.y(pageY) + 34);
        ctx.restore();
      }

      /* side explanation */
      var lx = box.x + box.w + 26, lw = Math.max(170, w - lx - 16);
      ctx.save();
      ctx.textAlign = 'left';
      ctx.font = '600 13px ' + css('--sans', 'sans-serif');
      ctx.fillStyle = INK;
      ctx.fillText('Upright reading A', lx, 54);
      ctx.font = '600 13px ' + css('--sans', 'sans-serif');
      ctx.fillStyle = TEAL;
      ctx.fillText('B reading at 180°', lx, 76);
      ctx.font = '11.5px ' + css('--sans', 'sans-serif');
      ctx.fillStyle = 'rgba(27,25,23,.6)';
      ctx.fillText('same strokes, different reading', lx, 94);

      if (row.ya !== null) {
        var py = 500 + 600 * row.ya;
        var by = 1000 - py;
        ctx.fillStyle = 'rgba(27,25,23,.55)';
        ctx.font = '11.5px ' + css('--sans', 'sans-serif');
        ctx.fillText('on page', lx, 128);
        ctx.font = '12px ' + css('--mono', 'monospace');
        ctx.fillStyle = ACCENT;
        ctx.fillText('y_A = ' + Math.round(py), lx, 146);
        ctx.fillStyle = TEAL;
        ctx.fillText('y_B = ' + Math.round(by) + '  (no referencial de B)', lx, 164);
        ctx.fillStyle = 'rgba(27,25,23,.55)';
        ctx.font = '11.5px ' + css('--sans', 'sans-serif');
        ctx.fillText('same stroke on page', lx, 190);
        ctx.font = '12px ' + css('--mono', 'monospace');
        ctx.fillStyle = INK;
        ctx.fillText('1000 − ' + Math.round(by) + ' = ' + Math.round(py), lx, 208);
      }
      ctx.fillStyle = 'rgba(27,25,23,.5)';
      ctx.font = '11.5px ' + css('--sans', 'sans-serif');
      wrap(ctx, 'Click a table row to highlight the feature pair on the page.', lx, 246, lw, 15);
      ctx.restore();
    }

    function wrap(ctx, text, x, y, maxw, lh) {
      var words = text.split(' '), line = '', yy = y;
      words.forEach(function (word) {
        var test = line ? line + ' ' + word : word;
        if (ctx.measureText(test).width > maxw && line) { ctx.fillText(line, x, yy); line = word; yy += lh; }
        else line = test;
      });
      if (line) ctx.fillText(line, x, yy);
    }

    window.rfbRenderDict = render;
    render();
  }

  /* ===========================================================
     TAB 3 — the canonical ladder
     =========================================================== */
  function initCanon() {
    var cv = document.getElementById('canon-canvas');
    if (!cv) return;
    var H = 600, EPS = 30;
    var hIn = document.getElementById('canon-h'), hOut = document.getElementById('canon-h-out');
    var eIn = document.getElementById('canon-eps'), eOut = document.getElementById('canon-eps-out');

    var RUNGS = [
      ['plume / pompom', -0.65], ['crown / top of hat', -0.50], ['hat dome', -0.30],
      ['hat brim', -0.25], ['hairline', -0.20], ['brow', -0.08], ['eyes', 0.00],
      ['under-eye bag', 0.08], ['nose tip', 0.25], ['mouth line', 0.30],
      ['chin', 0.50], ['collar / bow tie', 0.65]
    ];

    function render() {
      var f = fitCanvas(cv), ctx = f.ctx, w = f.w, h = f.h;
      ctx.clearRect(0, 0, w, h);
      var box = { x: 20, y: 30, w: Math.min(w * 0.52, h - 56), h: h - 56 };
      var m = mapper(w, h, box);

      drawPageFrame(ctx, m, null);

      /* head height band */
      var topY = 500 - H / 2, botY = 500 + H / 2;
      ctx.save();
      ctx.fillStyle = 'rgba(44,95,102,.07)';
      ctx.fillRect(m.x(300), m.y(topY), m.l(400), m.l(botY - topY));
      ctx.strokeStyle = 'rgba(44,95,102,.3)';
      ctx.setLineDash([3, 4]);
      ctx.strokeRect(m.x(300), m.y(topY), m.l(400), m.l(botY - topY));
      ctx.setLineDash([]);

      /* eyes line */
      ctx.strokeStyle = 'rgba(27,25,23,.3)';
      ctx.beginPath();
      ctx.moveTo(m.x(270), m.y(500)); ctx.lineTo(m.x(730), m.y(500));
      ctx.stroke();
      ctx.restore();

      /* ladder rows */
      ctx.save();
      ctx.textAlign = 'right';
      ctx.font = '11px ' + css('--sans', 'sans-serif');
      RUNGS.forEach(function (r) {
        var py = 500 + H * r[1];
        var isEye = r[1] === 0;
        ctx.strokeStyle = isEye ? ACCENT : 'rgba(27,25,23,.16)';
        ctx.lineWidth = isEye ? 1.6 : 1;
        ctx.beginPath();
        ctx.moveTo(m.x(300), m.y(py));
        ctx.lineTo(m.x(700), m.y(py));
        ctx.stroke();

        ctx.fillStyle = isEye ? ACCENT : 'rgba(27,25,23,.62)';
        ctx.font = (isEye ? '600 ' : '') + '11px ' + css('--sans', 'sans-serif');
        ctx.fillText(r[0], m.x(292), m.y(py) + 4);

        ctx.font = '10px ' + css('--mono', 'monospace');
        ctx.fillStyle = isEye ? ACCENT : 'rgba(27,25,23,.4)';
        ctx.textAlign = 'left';
        ctx.fillText(String(Math.round(py)), m.x(708), m.y(py) + 4);
        ctx.textAlign = 'right';
      });
      ctx.restore();

      /* the epsilon tolerance band around a sample rung */
      var sample = 500 + H * 0.30; /* the mouth line */
      ctx.save();
      ctx.fillStyle = 'rgba(178,63,38,.13)';
      ctx.fillRect(m.x(300), m.y(sample) - EPS * m.s, m.l(400), 2 * EPS * m.s);
      ctx.strokeStyle = ACCENT;
      ctx.setLineDash([3, 3]);
      ctx.beginPath();
      ctx.moveTo(m.x(300), m.y(sample) - EPS * m.s);
      ctx.lineTo(m.x(700), m.y(sample) - EPS * m.s);
      ctx.moveTo(m.x(300), m.y(sample) + EPS * m.s);
      ctx.lineTo(m.x(700), m.y(sample) + EPS * m.s);
      ctx.stroke();
      ctx.setLineDash([]);
      ctx.restore();

      /* side panel */
      var lx = box.x + box.w + 24, lw = Math.max(160, w - lx - 14);
      ctx.save();
      ctx.textAlign = 'left';
      ctx.font = '600 12px ' + css('--sans', 'sans-serif');
      ctx.fillStyle = INK;
      ctx.fillText('H = ' + H + ' px', lx, 58);
      ctx.font = '11.5px ' + css('--sans', 'sans-serif');
      ctx.fillStyle = 'rgba(27,25,23,.6)';
      ctx.fillText('eyes at y = 0  →  page y = 500', lx, 78);
      ctx.fillText('position = 500 + H · y', lx, 96);

      ctx.fillStyle = ACCENT;
      ctx.font = '600 12px ' + css('--sans', 'sans-serif');
      ctx.fillText('ε = ' + EPS + ' px  ≈ 0.05 · H', lx, 128);
      ctx.font = '11.5px ' + css('--sans', 'sans-serif');
      ctx.fillStyle = 'rgba(27,25,23,.6)';
      wrap(ctx, 'The orange band shows the prompt’s assumed placement tolerance. This is not a measured recognition threshold.', lx, 148, lw, 15);
      ctx.restore();
    }

    function wrap(ctx, text, x, y, maxw, lh) {
      var words = text.split(' '), line = '', yy = y;
      words.forEach(function (word) {
        var test = line ? line + ' ' + word : word;
        if (ctx.measureText(test).width > maxw && line) { ctx.fillText(line, x, yy); line = word; yy += lh; }
        else line = test;
      });
      if (line) ctx.fillText(line, x, yy);
    }

    if (hIn) hIn.addEventListener('input', function () {
      H = +hIn.value; if (hOut) hOut.textContent = H + ' px'; render();
    });
    if (eIn) eIn.addEventListener('input', function () {
      EPS = +eIn.value; if (eOut) eOut.textContent = EPS + ' px'; render();
    });

    window.rfbRenderCanon = render;
    render();
  }

  /* ===========================================================
     TAB 4 — the compromise stroke
     =========================================================== */
  function initCompromise() {
    var cv = document.getElementById('cs-canvas');
    var readout = document.getElementById('cs-readout');
    if (!cv) return;
    var EPS = 30;
    var a = { x: 430, y: 452 };     /* A wants the stroke here (page) */
    var b = { x: 550, y: 530 };     /* B wants it here (B's own frame) */
    var drag = null;

    function render() {
      var f = fitCanvas(cv), ctx = f.ctx, w = f.w, h = f.h;
      ctx.clearRect(0, 0, w, h);
      var box = { x: 20, y: 32, w: Math.min(w * 0.58, h - 56), h: h - 56 };
      var m = mapper(w, h, box);

      drawPageFrame(ctx, m, 'page');
      /* faint reference face */
      ctx.save();
      ctx.globalAlpha = 0.16;
      drawFace(ctx, m, { ink: INK });
      ctx.restore();

      var rb = { x: 1000 - b.x, y: 1000 - b.y };   /* R(b) on the page */
      var s = { x: (a.x + rb.x) / 2, y: (a.y + rb.y) / 2 };
      var dist = Math.hypot(rb.x - a.x, rb.y - a.y);
      var possible = dist <= 2 * EPS;

      ctx.save();
      /* the epsilon balls */
      ctx.fillStyle = 'rgba(178,63,38,.12)';
      ctx.strokeStyle = 'rgba(178,63,38,.75)';
      ctx.lineWidth = 1.8;
      ctx.beginPath(); ctx.arc(m.x(a.x), m.y(a.y), EPS * m.s, 0, Math.PI * 2); ctx.fill(); ctx.stroke();
      ctx.fillStyle = 'rgba(44,95,102,.12)';
      ctx.strokeStyle = 'rgba(44,95,102,.75)';
      ctx.beginPath(); ctx.arc(m.x(rb.x), m.y(rb.y), EPS * m.s, 0, Math.PI * 2); ctx.fill(); ctx.stroke();

      /* the segment a — R(b) */
      ctx.strokeStyle = possible ? 'rgba(63,107,70,.75)' : 'rgba(156,59,40,.8)';
      ctx.lineWidth = 2;
      ctx.setLineDash([6, 4]);
      ctx.beginPath();
      ctx.moveTo(m.x(a.x), m.y(a.y)); ctx.lineTo(m.x(rb.x), m.y(rb.y));
      ctx.stroke();
      ctx.setLineDash([]);

      /* targets */
      ctx.fillStyle = ACCENT;
      ctx.beginPath(); ctx.arc(m.x(a.x), m.y(a.y), 8, 0, Math.PI * 2); ctx.fill();
      ctx.fillStyle = TEAL;
      ctx.beginPath(); ctx.arc(m.x(rb.x), m.y(rb.y), 8, 0, Math.PI * 2); ctx.fill();

      /* the compromise point */
      if (possible) {
        ctx.fillStyle = '#fff';
        ctx.strokeStyle = INK;
        ctx.lineWidth = 2.4;
        ctx.beginPath(); ctx.arc(m.x(s.x), m.y(s.y), 8, 0, Math.PI * 2); ctx.fill(); ctx.stroke();
        ctx.fillStyle = INK;
        ctx.beginPath(); ctx.arc(m.x(s.x), m.y(s.y), 3.2, 0, Math.PI * 2); ctx.fill();
      }

      ctx.font = '600 12px ' + css('--sans', 'sans-serif');
      ctx.textAlign = 'right';
      ctx.fillStyle = ACCENT;
      ctx.fillText('a', m.x(a.x) - 12, m.y(a.y) + 4);
      ctx.textAlign = 'left';
      ctx.fillStyle = TEAL;
      ctx.fillText('R(b)', m.x(rb.x) + 12, m.y(rb.y) + 4);
      ctx.textAlign = 'center';
      ctx.fillStyle = INK;
      if (possible) ctx.fillText('s*', m.x(s.x), m.y(s.y) - 14);
      ctx.font = '10px ' + css('--mono', 'monospace');
      ctx.fillStyle = 'rgba(178,63,38,.85)';
      ctx.fillText('ε', m.x(a.x), m.y(a.y) - EPS * m.s - 5);
      ctx.fillStyle = 'rgba(44,95,102,.85)';
      ctx.fillText('ε', m.x(rb.x), m.y(rb.y) - EPS * m.s - 5);
      ctx.restore();

      /* side panel */
      var lx = box.x + box.w + 24, lw = Math.max(160, w - lx - 14);
      ctx.save();
      ctx.textAlign = 'left';
      ctx.font = '600 12px ' + css('--sans', 'sans-serif');
      ctx.fillStyle = ACCENT;
      ctx.fillText('a  (A target, on page)', lx, 56);
      ctx.fillStyle = TEAL;
      ctx.fillText('R(b)  (B target, on page)', lx, 76);
      ctx.font = '12px ' + css('--mono', 'monospace');
      ctx.fillStyle = 'rgba(27,25,23,.65)';
      ctx.fillText('a    = (' + Math.round(a.x) + ', ' + Math.round(a.y) + ')', lx, 98);
      ctx.fillText('b    = (' + Math.round(b.x) + ', ' + Math.round(b.y) + ')', lx, 116);
      ctx.fillText('R(b) = (' + Math.round(rb.x) + ', ' + Math.round(rb.y) + ')', lx, 134);
      ctx.fillText('s*   = (' + Math.round(s.x) + ', ' + Math.round(s.y) + ')', lx, 152);
      ctx.font = '10.5px ' + css('--sans', 'sans-serif');
      ctx.fillStyle = 'rgba(27,25,23,.5)';
      ctx.fillText('b em coordenadas de B', lx, 168);

      ctx.font = '600 12px ' + css('--sans', 'sans-serif');
      ctx.fillStyle = possible ? '#3f6b46' : '#9c3b28';
      ctx.fillText(possible ? '✓ placement feasible' : '✗ no shared placement', lx, 192);
      ctx.font = '11.5px ' + css('--sans', 'sans-serif');
      ctx.fillStyle = 'rgba(27,25,23,.6)';
      wrap(ctx, 'Drag both targets. If ‖a − R(b)‖ ≤ 2ε, the disks overlap and a shared point is geometrically possible.', lx, 214, lw, 15);
      ctx.restore();

      if (readout) {
        readout.innerHTML =
          '<div><span>‖a − R(b)‖</span><span>' + Math.round(dist) + ' px</span></div>' +
          '<div><span>2ε</span><span>' + (2 * EPS) + ' px</span></div>' +
          '<div><span>‖s* − a‖ = ‖s* − R(b)‖</span><span>' + Math.round(dist / 2) + ' px</span></div>' +
          '<div><span>teste</span><span class="' + (possible ? 'is-ok' : 'is-bad') + '">' +
          (possible ? 'passa ✓' : 'falha ✗') + '</span></div>';
      }
    }

    function wrap(ctx, text, x, y, maxw, lh) {
      var words = text.split(' '), line = '', yy = y;
      words.forEach(function (word) {
        var test = line ? line + ' ' + word : word;
        if (ctx.measureText(test).width > maxw && line) { ctx.fillText(line, x, yy); line = word; yy += lh; }
        else line = test;
      });
      if (line) ctx.fillText(line, x, yy);
    }

    function pos(e) {
      var r = cv.getBoundingClientRect();
      var box = { x: 20, y: 32, w: Math.min(r.width * 0.58, r.height - 56), h: r.height - 56 };
      var m = mapper(r.width, r.height, box);
      return { x: (e.clientX - r.left - m.ox) / m.s, y: (e.clientY - r.top - m.oy) / m.s };
    }

    function hit(q) {
      var rb = { x: 1000 - b.x, y: 1000 - b.y };
      var da = Math.hypot(q.x - a.x, q.y - a.y);
      var db = Math.hypot(q.x - rb.x, q.y - rb.y);
      return da < db ? 'a' : 'b';
    }

    cv.addEventListener('pointerdown', function (e) {
      var q = pos(e);
      drag = hit(q);
      cv.setPointerCapture(e.pointerId);
      apply(e); e.preventDefault();
    });
    cv.addEventListener('pointermove', function (e) { if (drag) apply(e); });
    cv.addEventListener('pointerup', function () { drag = null; });
    cv.addEventListener('pointercancel', function () { drag = null; });
    function apply(e) {
      var q = pos(e);
      q.x = Math.max(0, Math.min(1000, q.x));
      q.y = Math.max(0, Math.min(1000, q.y));
      if (drag === 'a') { a.x = q.x; a.y = q.y; }
      else if (drag === 'b') { b.x = 1000 - q.x; b.y = 1000 - q.y; }
      render();
    }

    window.rfbRenderCS = render;
    render();
  }

  window.rfbInitGeometry = function () {
    initHalfTurn();
    initDictionary();
    initCanon();
    initCompromise();
  };

  window.rfbRedrawGeometry = function () {
    if (window.rfbRenderHalfTurn) window.rfbRenderHalfTurn();
    if (window.rfbRenderDict) window.rfbRenderDict();
    if (window.rfbRenderCanon) window.rfbRenderCanon();
    if (window.rfbRenderCS) window.rfbRenderCS();
  };

  window.rfbDrawFace = drawFace;
  window.rfbCanon = CANON;
})();
