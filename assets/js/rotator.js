/* ============================================================
   Rotator — a draggable half-turn widget.
   Shared by the hero, the playground, the timeline and the failure atlas.

   The rotation is driven through a CSS custom property (--rot) on the
   element, so the very same angle can drive several images at once
   (e.g. the A|B split and the overlay mode).
   ============================================================ */

(function () {
  'use strict';

  function clamp(v, lo, hi) { return v < lo ? lo : (v > hi ? hi : v); }

  function Rotator(el, opts) {
    opts = opts || {};
    this.el = el;
    this.angle = opts.angle || 0;
    this.min = opts.min !== undefined ? opts.min : 0;
    this.max = opts.max !== undefined ? opts.max : 180;
    this.wrap = opts.wrap !== undefined ? opts.wrap : true;
    this.onChange = opts.onChange || null;
    this.onStart = opts.onStart || null;
    this.onEnd = opts.onEnd || null;
    this._dragging = false;
    this._raf = null;

    this._apply();

    var self = this;
    this._down = function (e) { self._start(e); };
    this._move = function (e) { self._move(e); };
    this._up = function (e) { self._end(e); };

    el.addEventListener('pointerdown', this._down);
    el.addEventListener('keydown', function (e) { self._key(e); });
    el.setAttribute('tabindex', el.getAttribute('tabindex') || '0');
    if (el.getAttribute('role') !== 'slider') el.setAttribute('role', 'slider');
    el.setAttribute('aria-valuemin', String(this.min));
    el.setAttribute('aria-valuemax', String(this.max));
  }

  Rotator.prototype._apply = function () {
    this.el.style.setProperty('--rot', this.angle.toFixed(2) + 'deg');
    this.el.setAttribute('aria-valuenow', String(Math.round(this.angle)));
    if (this.onChange) this.onChange(this.angle);
  };

  Rotator.prototype.set = function (deg, silent) {
    var a = deg;
    if (this.wrap) {
      while (a < this.min) a += 360;
      while (a > this.max) a -= 360;
    }
    this.angle = clamp(a, this.min, this.max);
    if (!silent) this._apply();
    else this.el.style.setProperty('--rot', this.angle.toFixed(2) + 'deg');
    return this.angle;
  };

  /* angle from the pointer position around the centre of the element */
  Rotator.prototype._angleFromEvent = function (e) {
    var r = this.el.getBoundingClientRect();
    var cx = r.left + r.width / 2;
    var cy = r.top + r.height / 2;
    var dx = e.clientX - cx;
    var dy = e.clientY - cy;
    /* screen angle, measured clockwise from "up" */
    var deg = Math.atan2(dx, -dy) * 180 / Math.PI;
    if (deg < 0) deg += 360;
    /* The drawing's own angle is the screen angle minus the 180 degree
       offset, so that "pointing up" reads as 0 degrees. */
    var a = deg - 180;
    if (a < 0) a += 360;
    if (a > 180) a -= 360;
    return a;
  };

  Rotator.prototype._start = function (e) {
    if (e.button !== undefined && e.button !== 0) return;
    this._dragging = true;
    this.el.classList.add('no-anim');
    if (this.el.setPointerCapture && e.pointerId !== undefined) {
      try { this.el.setPointerCapture(e.pointerId); } catch (err) { /* noop */ }
    }
    window.addEventListener('pointermove', this._move);
    window.addEventListener('pointerup', this._up);
    window.addEventListener('pointercancel', this._up);
    if (this.onStart) this.onStart();
    e.preventDefault();
  };

  Rotator.prototype._move = function (e) {
    if (!this._dragging) return;
    this.set(this._angleFromEvent(e));
    e.preventDefault();
  };

  Rotator.prototype._end = function () {
    if (!this._dragging) return;
    this._dragging = false;
    this.el.classList.remove('no-anim');
    window.removeEventListener('pointermove', this._move);
    window.removeEventListener('pointerup', this._up);
    window.removeEventListener('pointercancel', this._up);
    if (this.onEnd) this.onEnd();
  };

  Rotator.prototype._key = function (e) {
    var step = e.shiftKey ? 15 : 5;
    if (e.key === 'ArrowLeft' || e.key === 'ArrowDown') {
      this.set(this.angle - step); e.preventDefault();
    } else if (e.key === 'ArrowRight' || e.key === 'ArrowUp') {
      this.set(this.angle + step); e.preventDefault();
    } else if (e.key === 'Home') {
      this.set(this.min); e.preventDefault();
    } else if (e.key === 'End') {
      this.set(this.max); e.preventDefault();
    }
  };

  /* smooth animated sweep between two angles */
  Rotator.prototype.animateTo = function (deg, ms) {
    var self = this;
    var from = this.angle;
    var to = deg;
    while (to < from) to += 360;
    var dur = ms || 620;
    var start = null;
    if (this._raf) cancelAnimationFrame(this._raf);
    this.el.classList.add('no-anim');

    function step(ts) {
      if (start === null) start = ts;
      var p = Math.min(1, (ts - start) / dur);
      var eased = p < 0.5 ? 4 * p * p * p : 1 - Math.pow(-2 * p + 2, 3) / 2;
      var a = from + (to - from) * eased;
      if (a > 180) a -= 360;
      self.angle = a;
      self.el.style.setProperty('--rot', a.toFixed(2) + 'deg');
      self.el.setAttribute('aria-valuenow', String(Math.round(a)));
      if (p < 1) {
        self._raf = requestAnimationFrame(step);
      } else {
        self._raf = null;
        self.el.classList.remove('no-anim');
        if (self.onChange) self.onChange(self.angle);
      }
    }
    this._raf = requestAnimationFrame(step);
  };

  /* continuous ping-pong spin */
  Rotator.prototype.spin = function (on) {
    var self = this;
    if (this._spinRaf) { cancelAnimationFrame(this._spinRaf); this._spinRaf = null; }
    if (!on) return;
    var dir = 1;
    var last = null;
    this.el.classList.add('no-anim');
    function tick(ts) {
      if (last === null) last = ts;
      var dt = (ts - last) / 1000;
      last = ts;
      var a = self.angle + dir * 42 * dt;
      if (a >= 180) { a = 180; dir = -1; }
      if (a <= 0) { a = 0; dir = 1; }
      self.angle = a;
      self.el.style.setProperty('--rot', a.toFixed(2) + 'deg');
      self.el.setAttribute('aria-valuenow', String(Math.round(a)));
      if (self.onChange) self.onChange(a);
      self._spinRaf = requestAnimationFrame(tick);
    }
    this._spinRaf = requestAnimationFrame(tick);
  };

  window.Rotator = Rotator;
  window.rfbClamp = clamp;
})();
