/* Pure hypotheses-to-geometry utilities. NO human perceptual threshold encoded. */
(function(root,make){var api=make();if(typeof module!=='undefined'&&module.exports)module.exports=api;if(root)root.RFBCompletion=api;})(typeof window!=='undefined'?window:null,function(){
'use strict';
function finite(x){return typeof x==='number'&&Number.isFinite(x);}
function dash(gapFraction,period){
 period=period===undefined?32:period;
 if(!finite(gapFraction)||gapFraction<0||gapFraction>=1||!finite(period)||period<=0)throw new RangeError('invalid dash controls');
 if(gapFraction===0)return null;
 return [(period*(1-gapFraction)).toFixed(2),(period*gapFraction).toFixed(2)].join(' ');
}
function feasible(a,b,epsilon,centre){
 centre=centre||[500,500];
 if(!Array.isArray(a)||!Array.isArray(b)||a.length!==2||b.length!==2||!a.every(finite)||!b.every(finite)||!finite(epsilon)||epsilon<0)throw new RangeError('invalid feature positions');
 var target=[2*centre[0]-b[0],2*centre[1]-b[1]];
 var d=Math.hypot(a[0]-target[0],a[1]-target[1]);
 return {distance:d,diameter:2*epsilon,slack:2*epsilon-d,intersect:d<=2*epsilon,transformed:target,midpoint:[(a[0]+target[0])/2,(a[1]+target[1])/2]};
}
function poseDifference(angleA,angleB) {
 if(!finite(angleA)||!finite(angleB))throw new RangeError('invalid manual pose angles');
 // Both angles are annotated in their OWN UPRIGHT viewer frames.
 return ((angleB-angleA+180)%360+360)%360-180;
}
return {dash:dash,feasible:feasible,poseDifference:poseDifference};
});
