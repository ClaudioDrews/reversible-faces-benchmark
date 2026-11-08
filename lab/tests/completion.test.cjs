const {test}=require('node:test'),a=require('node:assert/strict'),C=require('../completion-core.js');
test('gap fraction zero leaves stroke continuous',()=>a.equal(C.dash(0),null));
test('gap fraction partitions one period',()=>{let q=C.dash(.25,40).split(' ').map(Number);a.deepEqual(q,[30,10]);});
test('invalid omissions are rejected',()=>{a.throws(()=>C.dash(1));a.throws(()=>C.dash(-.5));});
test('paired upright frames rotated exactly once',()=>{let x=C.feasible([450,350],[550,650],30);a.equal(x.distance,0);a.equal(x.intersect,true);a.deepEqual(x.midpoint,[450,350]);});
test('adjustable point-disk intersection is geometry, not recognition',()=>{let x=C.feasible([450,350],[570,650],10);a.equal(x.distance,20);a.equal(x.intersect,true);a.equal(C.feasible([450,350],[571,650],10).intersect,false);});
test('manual head axes need not be equal',()=>{a.equal(C.poseDifference(-12,18),30);a.equal(C.poseDifference(20,20),0);});
