/* Conditional landmark tolerance models: SYNTHETIC geometric assumptions only.
 * No parameters inferred from humans; NOT a face recognition classifier. */
(function(root,make){var api=make();if(typeof module!=='undefined'&&module.exports)module.exports=api;if(root)root.RFBSpatial=api;})(typeof window!=='undefined'?window:null,function(){
'use strict';
function finite(n){return typeof n==='number'&&Number.isFinite(n);}
function point(p){if(!Array.isArray(p)||p.length!==2||!p.every(finite))throw new TypeError('2D finite point required');}
function rot(p){point(p);return [1000-p[0],1000-p[1]];}
function cov(sx,sy,corr){
 if(!finite(sx)||!finite(sy)||sx<=0||sy<=0||!finite(corr)||Math.abs(corr)>=1)throw new RangeError('positive sigma and |correlation|<1 required');
 return [[sx*sx,corr*sx*sy],[corr*sx*sy,sy*sy]];
}
function mahal(p,mu,cv){
 point(p);point(mu);
 if(!Array.isArray(cv)||cv.length!==2||!Array.isArray(cv[0])||!Array.isArray(cv[1]))throw new TypeError('2x2 covariance required');
 var a=cv[0][0],b=cv[0][1],d=cv[1][1],off=cv[1][0];
 if(![a,b,d,off].every(finite)||Math.abs(b-off)>1e-6)throw new RangeError('symmetric finite covariance required');
 var det=a*d-b*b;
 if(det<=1e-12||a<=0||d<=0)throw new RangeError('positive-definite covariance required');
 var x=p[0]-mu[0],y=p[1]-mu[1];
 return Math.max(0,(d*x*x-2*b*x*y+a*y*y)/det);
}
function ellipseContains(p,mu,cv,threshold){if(!finite(threshold)||threshold<0)throw new RangeError('threshold');return mahal(p,mu,cv)<=threshold+1e-9;}
function radial(p,center,radius){point(p);point(center);if(!finite(radius)||radius<=0)throw new RangeError('radius');return Math.hypot(p[0]-center[0],p[1]-center[1])/radius;}
function scaleSigma(base,beta,r){
 if(!finite(base)||base<=0||!finite(beta)||!finite(r)||r<0)throw new RangeError('invalid dispersion hypothesis');
 return base*Math.exp(beta*r);
}
function makeFeature(mu,sx,sy,corr,centre,beta,radius){
 point(mu);point(centre);var r=radial(mu,centre,radius);
 return {mean:mu.slice(),cov:cov(scaleSigma(sx,beta,r),scaleSigma(sy,beta,r),corr),radius:r,
   sigma:[scaleSigma(sx,beta,r),scaleSigma(sy,beta,r)]};
}
function joint(p,a,b){
 if(!a||!b||!a.mean||!b.mean||!a.cov||!b.cov)throw new TypeError('two features required');
 var dA=mahal(p,a.mean,a.cov),dB=mahal(rot(p),b.mean,b.cov);
 return {dA:dA,dB:dB,compatibility:Math.exp(-.5*(dA+dB)),withinA:dA<=5.991,withinB:dB<=5.991};
}
function quadrant(p,centre){
 point(p);point(centre);
 return (p[1]<centre[1]?'top':'bottom')+'-'+(p[0]<centre[0]?'left':'right');
}
function sampleOverlap(a,b,threshold,step){
 if(!finite(threshold)||threshold<0||!finite(step)||step<2||step>100)throw new RangeError('invalid sampling');
 var qa=[0,0,0,0],total=0;
 for(var y=step/2;y<1000;y+=step)for(var x=step/2;x<1000;x+=step){
   var p=[x,y];
   if(ellipseContains(p,a.mean,a.cov,threshold)&&ellipseContains(rot(p),b.mean,b.cov,threshold)){
     total++;qa[(y<500?0:2)+(x<500?0:1)]++;
   }
 }
 return {cells:total,areaApprox:total*step*step,quadrants:qa,step:step,warning:'Numeric geometric overlap only; parameters synthetic'};
}
function formatAngle(v){if(!finite(v))throw new TypeError('finite angle required');return ((v%360)+360)%360;}
return {rot:rot,cov:cov,mahal:mahal,ellipseContains:ellipseContains,radial:radial,scaleSigma:scaleSigma,makeFeature:makeFeature,joint:joint,quadrant:quadrant,sampleOverlap:sampleOverlap,formatAngle:formatAngle};
});
