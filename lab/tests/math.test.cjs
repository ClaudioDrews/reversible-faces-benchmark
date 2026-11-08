const { test } = require('node:test');
const a=require('node:assert/strict');
const M=require('../math.js');
const eq=(x,y,e=1e-8)=>a.ok(Math.abs(x-y)<e,String(x)+' != '+y);

test('R is an involution and not reflection',()=>{const c=[500,500],p=[100,230];a.deepEqual(M.rotatePoint(M.rotatePoint(p,c),c),p);a.deepEqual(M.rotatePoint(p,c),[900,770]);});
test('conjugate B exactly once; midpoint and disks',()=>{a.deepEqual(M.compromise([450,520],[550,480],[500,500]),[450,520]);a.equal(M.disksIntersect([440,520],[550,480],[500,500],5),true);a.equal(M.disksIntersect([440,520],[550,480],[500,500],4),false);});
test('centre fitting from framed points',()=>{a.deepEqual(M.fittedCentre([{a:[400,450],b:[600,550]},{a:[500,500],b:[500,500]}]),[500,500]);});
test('C2 projections and rho / odd identity',()=>{const x=new Float32Array([9,2,4,3]),p=M.parity(x,2,2);eq(p.even[0],6);eq(p.odd[0],3);eq(p.odd[3],-3);eq(p.even[1],3);for(let i=0;i<4;i++){eq(p.even[i]+p.odd[i],x[i]);eq(p.even[i]-p.odd[i],p.rot[i]);}const norm=Math.hypot(...Array.from(x));const oddNorm=Math.hypot(...Array.from(p.odd));eq(M.rho(x,2,2),2*oddNorm/norm);});
test('nonnegative ink yields rho ≤ sqrt(2), self-C2 zero',()=>{eq(M.rho(new Float32Array([1,2,2,1]),2,2),0);a.ok(M.rho(new Float32Array([1,0,0,0]),2,2)<=Math.SQRT2+1e-9);});
test('coarse IoU handles blank controls',()=>{eq(M.iou([0,0],[0,0]),1);eq(M.iou([30,0],[0,30]),0);eq(M.iou([30,0],[30,0]),1);});
test('sector mass identifies opposite imbalance',()=>{const x=Array(81).fill(0);x[0]=200;const s=M.sectorMass(x,9,9);eq(s.normalized[0],1);eq(s.oppositeAsymmetry[0],1,1e-8);});
test('radial majorant preserves both silhouettes',()=>{const a0=[1,2,3,4],b=[3,1,4,2],out=M.radialEnvelope(a0,b);a.deepEqual(out,[4,2,3,4]);const sm=M.smoothMajorant(out,1);sm.forEach((v,i)=>a.ok(v>=out[i]));});
test('null z score and no-op pixels',()=>{eq(M.zScore(3,[1,2,3]).mean,2);a.equal(M.changedPixels([1,2],[1,2]).count,0);a.equal(M.changedPixels([1,2],[1,3]).count,1);});
test('invalid inputs reject',()=>{a.throws(()=>M.rotatePoint([1],[0,0]));a.throws(()=>M.fittedCentre([]));a.throws(()=>M.radialEnvelope([1,2,3],[4,5,6]));});
