/* ============================================================
   Symmetry decomposition lab.

   Computes, in the browser and from the real SVG:
     I    — the drawing
     R·I  — the half-turn
     I₊   = ½(I + R·I)   the even part (what the turn preserves)
     I₋   = ½(I − R·I)   the odd part  (what changes sign)
   and the advisory diagnostic
     ρ = ‖I − R·I‖ / ‖I‖
   measured on a 200 px grayscale ink image, exactly as the repository's
   scripts/perceptual.py does it.
   ============================================================ */

(function () {
  'use strict';

  var ART = window.RFB_ART || {};
  var RHO_REF = window.RFB_RHO || {};
  var M = window.RFB_MANIFEST;

  var WORK = 320;     /* resolution of the displayed panels */
  var RHO_N = 200;    /* resolution used for ρ, as in perceptual.py */

  function css(name, fallback) {
    var v = getComputedStyle(document.documentElement).getPropertyValue(name);
    return (v && v.trim()) || fallback;
  }

  /* ---------------------------------------------------------------
     helpers
     --------------------------------------------------------------- */
  function rasterize(src, size) {
    /* returns a Promise<ImageData> */
    return new Promise(function (resolve, reject) {
      var img = new Image();
      img.onload = function () {
        var cv = document.createElement('canvas');
        cv.width = size; cv.height = size;
        var ctx = cv.getContext('2d', { willReadFrequently: true });
        ctx.fillStyle = '#ffffff';
        ctx.fillRect(0, 0, size, size);
        ctx.imageSmoothingEnabled = true;
        ctx.imageSmoothingQuality = 'high';
        ctx.drawImage(img, 0, 0, size, size);
        try {
          resolve(ctx.getImageData(0, 0, size, size));
        } catch (err) {
          reject(err);
        }
      };
      img.onerror = function () { reject(new Error('image load failed')); };
      img.src = src.url;
    });
  }

  function toInk(data) {
    /* grayscale "ink" = 255 - gray, matching perceptual.py */
    var n = data.width * data.height;
    var px = data.data;
    var ink = new Float32Array(n);
    for (var i = 0; i < n; i++) {
      var o = i * 4;
      var g = 0.299 * px[o] + 0.587 * px[o + 1] + 0.114 * px[o + 2];
      ink[i] = 255 - g;
    }
    return ink;
  }

  function rot180(ink, w, h) {
    var out = new Float32Array(ink.length);
    for (var y = 0; y < h; y++) {
      for (var x = 0; x < w; x++) {
        out[y * w + x] = ink[(h - 1 - y) * w + (w - 1 - x)];
      }
    }
    return out;
  }

  function rhoOf(ink, w, h) {
    var rot = rot180(ink, w, h);
    var num = 0, den = 0;
    for (var i = 0; i < ink.length; i++) {
      var d = ink[i] - rot[i];
      num += d * d;
      den += ink[i] * ink[i];
    }
    return Math.sqrt(num) / (Math.sqrt(den) + 1e-9);
  }

  function inkFraction(data) {
    var n = data.width * data.height, px = data.data, cnt = 0;
    for (var i = 0; i < n; i++) {
      var o = i * 4;
      var g = 0.299 * px[o] + 0.587 * px[o + 1] + 0.114 * px[o + 2];
      if (g < 200) cnt++;
    }
    return cnt / n;
  }

  function paint(canvas, arr, w, h, mode) {
    var ctx = canvas.getContext('2d');
    var img = ctx.createImageData(w, h);
    for (var i = 0; i < arr.length; i++) {
      var v;
      if (mode === 'odd') {
        v = 128 - arr[i];            /* signed: negative ink goes above mid-grey */
        v = v < 0 ? 0 : (v > 255 ? 255 : v);
      } else {
        v = 255 - arr[i];            /* positive ink goes dark */
        v = v < 0 ? 0 : (v > 255 ? 255 : v);
      }
      var o = i * 4;
      img.data[o] = v; img.data[o + 1] = v; img.data[o + 2] = v; img.data[o + 3] = 255;
    }
    ctx.putImageData(img, 0, 0);
  }

  /* ---------------------------------------------------------------
     the lab
     --------------------------------------------------------------- */
  function init() {
    var sel = document.getElementById('sym-select');
    var panels = document.getElementById('sym-panels');
    var readout = document.getElementById('sym-readout');
    if (!sel || !panels) return;

    var svgs = M.artifacts.filter(function (a) { return a.kind === 'svg'; });

    svgs.forEach(function (a) {
      var o = document.createElement('option');
      o.value = a.id;
      o.textContent = a.modelLabel + ' · ' + (a.roundLabel || 'Baseline');
      sel.appendChild(o);
    });

    var boxIds = ['sym-show-i', 'sym-show-r', 'sym-show-p', 'sym-show-m'];
    var boxes = boxIds.map(function (id) { return document.getElementById(id); });

    var cache = {};
    var current = null;

    function panelDefs() {
      return [
        { key: 'i', head: 'sym.hI', explain: 'sym.eI', show: boxes[0] },
        { key: 'r', head: 'sym.hR', explain: 'sym.eR', show: boxes[1] },
        { key: 'p', head: 'sym.hP', explain: 'sym.eP', show: boxes[2] },
        { key: 'm', head: 'sym.hM', explain: 'sym.eM', show: boxes[3] }
      ];
    }

    function buildPanels() {
      panels.innerHTML = '';
      panelDefs().forEach(function (def) {
        var panel = document.createElement('div');
        panel.className = 'sym-panel';
        panel.dataset.key = def.key;
        panel.innerHTML = '<h4></h4><canvas width="' + WORK + '" height="' + WORK + '"></canvas><p class="sym-explain"></p>';
        panel.querySelector('h4').textContent = window.t(def.head);
        panel.querySelector('.sym-explain').textContent = window.t(def.explain);
        panels.appendChild(panel);
      });
      panelDefs().forEach(function (def) {
        var panel = panels.querySelector('.sym-panel[data-key="' + def.key + '"]');
        if (panel) panel.hidden = !(def.show && def.show.checked);
      });
    }

    function load(id) {
      var art = null;
      for (var i = 0; i < M.artifacts.length; i++) if (M.artifacts[i].id === id) art = M.artifacts[i];
      if (!art) return;
      current = art;

      if (readout) {
        readout.innerHTML = '<div><span>' + window.t('sym.loading') + '</span><span>…</span></div>';
      }

      var src = ART[id];
      var url;
      if (src) {
        var blob = new Blob([src], { type: 'image/svg+xml;charset=utf-8' });
        url = URL.createObjectURL(blob);
      } else {
        url = art.file;  /* raster baseline: a plain same-origin image */
      }

      Promise.all([rasterize({ url: url }, WORK), rasterize({ url: url }, RHO_N)])
        .then(function (res) {
          var big = res[0], small = res[1];
          var ink = toInk(big);
          var w = big.width, h = big.height;
          var r = rot180(ink, w, h);
          var even = new Float32Array(ink.length);
          var odd = new Float32Array(ink.length);
          for (var i = 0; i < ink.length; i++) {
            even[i] = 0.5 * (ink[i] + r[i]);
            odd[i] = 0.5 * (ink[i] - r[i]);
          }

          var panelsByKey = { i: ink, r: r, p: even, m: odd };
          panelDefs().forEach(function (def) {
            var wrap = panels.querySelector('.sym-panel[data-key="' + def.key + '"]');
            if (!wrap) return;
            var cv = wrap.querySelector('canvas');
            paint(cv, panelsByKey[def.key], w, h, def.key === 'm' ? 'odd' : 'ink');
          });

          var inkSmall = toInk(small);
          var rhoLive = rhoOf(inkSmall, small.width, small.height);
          var ref = RHO_REF[id];
          var frac = inkFraction(small);

          if (readout) {
            var delta = ref ? Math.abs(rhoLive - ref.rho) : null;
            var agree = (delta !== null && delta <= 0.02);
            readout.innerHTML =
              '<div><span>' + window.t('sym.rho') + '</span><span>' + rhoLive.toFixed(4) + '</span></div>' +
              '<div><span>' + window.t('sym.rhoRef') + '</span><span>' +
              (ref ? ref.rho.toFixed(4) : '—') + '</span></div>' +
              '<div><span>' + window.t('sym.ink') + '</span><span>' + frac.toFixed(4) + '</span></div>' +
              '<div><span>' + window.t('sym.px') + '</span><span>' + RHO_N + ' px</span></div>' +
              (ref ? '<div><span>' + (agree ? window.t('sym.agree') : window.t('sym.differ')) +
                '</span><span class="' + (agree ? 'is-ok' : '') + '">Δ ' + delta.toFixed(4) + '</span></div>' : '');
          }

          if (src) URL.revokeObjectURL(url);
        })
        .catch(function (err) {
          if (readout) {
            readout.innerHTML = '<div><span>' + window.t('sym.loading') + '</span><span>' +
              (err && err.name === 'SecurityError' ? 'tainted canvas' : 'error') + '</span></div>';
          }
        });
    }

    buildPanels();

    sel.addEventListener('change', function () { load(sel.value); });
    boxes.forEach(function (b) {
      if (!b) return;
      b.addEventListener('change', function () {
        panelDefs().forEach(function (def) {
          var wrap = panels.querySelector('.sym-panel[data-key="' + def.key + '"]');
          if (wrap) wrap.hidden = !def.show.checked;
        });
      });
    });

    window.rfbReloadSymmetry = function () {
      buildPanels();
      if (current) load(current.id);
    };

    /* default selection: the cleanest round-4 GLM drawing */
    var def = 'r04-glm-5.3-flash';
    sel.value = def;
    load(def);
  }

  window.rfbInitSymmetry = init;
})();
