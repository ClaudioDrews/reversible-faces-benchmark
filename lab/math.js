/* Pure, side-effect-free C2 and exploratory shape mathematics.
 * No psychophysical model or image-recognition claims. MIT.
 */
(function(root, factory) {
  var api = factory();
  if (typeof module !== 'undefined' && module.exports) module.exports = api;
  if (root) root.RFBLabMath = api;
})(typeof window !== 'undefined' ? window : null, function () {
  'use strict';
  function finite(v) { return typeof v === 'number' && Number.isFinite(v); }
  function checkPoint(p) { if (!Array.isArray(p) || p.length !== 2 || !p.every(finite)) throw new TypeError('2D point required'); }
  function rotatePoint(p, c) {
    checkPoint(p); checkPoint(c);
    return [2*c[0]-p[0], 2*c[1]-p[1]];
  }
  function compromise(a, b, c, wa, wb) {
    checkPoint(a); checkPoint(b); checkPoint(c);
    wa = wa === undefined ? 1 : wa; wb = wb === undefined ? 1 : wb;
    if (!(wa > 0 && wb > 0 && finite(wa) && finite(wb))) throw new RangeError('positive weights required');
    var q=rotatePoint(b,c);
    return [(wa*a[0]+wb*q[0])/(wa+wb),(wa*a[1]+wb*q[1])/(wa+wb)];
  }
  function fittedCentre(pairs) {
    if (!Array.isArray(pairs) || !pairs.length) throw new RangeError('nonempty pairs required');
    var x=0,y=0,total=0;
    pairs.forEach(function(p) {
      checkPoint(p.a); checkPoint(p.b);
      var w = p.weight === undefined ? 1 : p.weight;
      if (!finite(w) || w <= 0) throw new RangeError('positive weights required');
      x += w*(p.a[0]+p.b[0]); y += w*(p.a[1]+p.b[1]); total += w;
    });
    return [x/(2*total),y/(2*total)];
  }
  function disksIntersect(a, b, c, epsilon) {
    checkPoint(a); checkPoint(b); checkPoint(c);
    if (!finite(epsilon) || epsilon < 0) throw new RangeError('invalid epsilon');
    var t=rotatePoint(b,c);
    return Math.hypot(a[0]-t[0],a[1]-t[1]) <= 2*epsilon + 1e-9;
  }
  function checkGrid(ink,w,h) {
    if (!ink || !Number.isInteger(w) || !Number.isInteger(h) || w<1 || h<1 || ink.length !== w*h) throw new RangeError('bad raster grid');
  }
  function rotateGrid(ink,w,h) {
    checkGrid(ink,w,h);
    var out = new Float32Array(ink.length);
    for (var i=0; i<ink.length; i++) out[i]=ink[ink.length-1-i];
    return out;
  }
  function parity(ink,w,h) {
    var rot=rotateGrid(ink,w,h);
    var even=new Float32Array(ink.length), odd=new Float32Array(ink.length);
    for(var i=0;i<ink.length;i++) {even[i]=(ink[i]+rot[i])/2;odd[i]=(ink[i]-rot[i])/2;}
    return {rot:rot, even:even, odd:odd};
  }
  function rho(ink,w,h) {
    var rot=rotateGrid(ink,w,h), sum=0,den=0;
    for(var i=0;i<ink.length;i++) {var d=ink[i]-rot[i];sum+=d*d;den+=ink[i]*ink[i];}
    return den ? Math.sqrt(sum/den) : 0;
  }
  function inkFraction(ink, threshold) {
    if (!ink || !ink.length) return 0;
    var n=0,t=threshold===undefined?32:threshold;
    for(var i=0;i<ink.length;i++)if(ink[i]>t)n++;
    return n/ink.length;
  }
  function iou(a,b,threshold) {
    if (!a || !b || a.length!==b.length) throw new RangeError('same-size arrays required');
    var inter=0, union=0,t=threshold===undefined?16:threshold;
    for(var i=0;i<a.length;i++) {var x=a[i]>t,y=b[i]>t;if(x||y)union++;if(x&&y)inter++;}
    return union ? inter/union : 1;
  }
  function sectorMass(ink,w,h) {
    checkGrid(ink,w,h);
    var sectors=new Array(9).fill(0), n=0;
    for(var y=0;y<h;y++)for(var x=0;x<w;x++) {
      var id=Math.min(2,Math.floor(y*3/h))*3+Math.min(2,Math.floor(x*3/w));
      var value=Math.max(0,+ink[y*w+x]||0);
      sectors[id]+=value;n+=value;
    }
    var normalized=sectors.map(function(v){return n?v/n:0});
    var opp=[[0,8],[1,7],[2,6],[3,5]], asym=opp.map(function(p){return Math.abs(sectors[p[0]]-sectors[p[1]])/(sectors[p[0]]+sectors[p[1]]+1e-9)});
    return {sectors:sectors, normalized:normalized, oppositeAsymmetry:asym, total:n};
  }
  function distanceToRotated(a,b,c) {
    checkPoint(a);checkPoint(b);checkPoint(c);
    var p=rotatePoint(b,c);return Math.hypot(a[0]-p[0],a[1]-p[1]);
  }
  function radialEnvelope(a,b) {
    if(!Array.isArray(a)||!Array.isArray(b)||a.length!==b.length||a.length<2||a.length%2)throw new RangeError('equal even angular sample count');
    var n=a.length;return a.map(function(v,i) {if(!finite(v)||v<0||!finite(b[(i+n/2)%n])||b[(i+n/2)%n]<0)throw new RangeError('nonnegative radii required');return Math.max(v,b[(i+n/2)%n]);});
  }
  function smoothMajorant(r,rad) {
    if(!Array.isArray(r)||!r.length||!r.every(function(x){return finite(x)&&x>=0}))throw new RangeError('valid radial samples required');
    if(!Number.isInteger(rad)||rad<0||rad>r.length/2)throw new RangeError('valid smoothing radius required');
    return r.map(function(x,i){var s=0;for(var k=-rad;k<=rad;k++)s+=r[(i+k+r.length)%r.length];return Math.max(x,s/(2*rad+1));});
  }
  function zScore(value,samples) {
    if(!finite(value)||!Array.isArray(samples)||samples.length<2||!samples.every(finite)) throw new TypeError('numeric null sample required');
    var mean=samples.reduce(function(a,b){return a+b;},0)/samples.length;
    var variance=samples.reduce(function(a,b){return a+(b-mean)*(b-mean);},0)/samples.length;
    return {z:(value-mean)/Math.max(Math.sqrt(variance),1e-12),mean:mean,sd:Math.sqrt(variance)};
  }
  function changedPixels(a,b,epsilon) {
    if(!a||!b||a.length!==b.length)throw new RangeError('arrays must match');
    var count=0,delta=0,e=epsilon===undefined?0.5:epsilon;
    for(var i=0;i<a.length;i++){var diff=Math.abs(a[i]-b[i]); if(diff>e)count++;delta+=diff;}
    return {count:count,fraction:a.length?count/a.length:0,totalDelta:delta};
  }
  return {rotatePoint:rotatePoint,compromise:compromise,fittedCentre:fittedCentre,
    disksIntersect:disksIntersect,rotateGrid:rotateGrid,parity:parity,rho:rho,
    inkFraction:inkFraction,iou:iou,sectorMass:sectorMass,distanceToRotated:distanceToRotated,
    radialEnvelope:radialEnvelope,smoothMajorant:smoothMajorant,zScore:zScore,changedPixels:changedPixels};
});
