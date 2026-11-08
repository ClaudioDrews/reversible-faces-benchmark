/* Experimental, geometry-only display perturbations. No recognizer. */
(function () {
  'use strict';
  var M=window.RFBLabMath, C=window.RFBCompletion, manifest=window.RFB_MANIFEST, art=window.RFB_ART||{};
  var $=function(id){ return document.getElementById(id); };
  if (!M||!C||!manifest) { $('diagnosis').textContent='Missing modules: serve the repository root locally.';return; }
  var sel=$('art'), source='', parts=[], sourceInk=null, version=0, renderVersion=0;
  function imageURL(svg){return 'data:image/svg+xml;charset=utf-8,'+encodeURIComponent(svg);}
  function toDom(svg){var d=new DOMParser().parseFromString(svg,'image/svg+xml');if(d.querySelector('parsererror'))throw Error('Invalid archived SVG');return d;}
  function primitives(d){
    return Array.from(d.querySelectorAll('path,line,polyline,polygon,rect,circle,ellipse')).filter(function(el){
      return !(el.localName==='rect' && +el.getAttribute('width')>=990 && +el.getAttribute('height')>=990);
    });
  }
  function getInherited(el,name) {
    for(var x=el;x&&x.nodeType===1;x=x.parentElement) {
      var v=x.getAttribute(name);if(v!==null)return v;
      var style=x.getAttribute('style')||'',m=style.match(new RegExp('(?:^|;)\\s*'+name+'\\s*:\\s*([^;]+)','i'));
      if(m)return m[1];
    }
    return null;
  }
  function edited(){
    var dom=toDom(source), target=primitives(dom)[+$('primitive').value];
    if(!target)throw Error('No editable primitive');
    var omission=+$('gaps').value/100, weight=+$('weight').value/100;
    var dash=C.dash(omission,32);
    if(dash!==null)target.setAttribute('stroke-dasharray',dash);
    if(weight!==1){
      var w=parseFloat(getInherited(target,'stroke-width')||'3');
      if(!Number.isFinite(w)||w<=0)w=3;
      target.setAttribute('stroke-width',String((w*weight).toFixed(3)));
    }
    return new XMLSerializer().serializeToString(dom.documentElement);
  }
  function raster(src){
    return new Promise(function(resolve,reject){
      var im=new Image();
      im.onload=function(){
        try{
          var n=240,cv=document.createElement('canvas');cv.width=n;cv.height=n;
          var ctx=cv.getContext('2d',{willReadFrequently:true});ctx.fillStyle='#fff';ctx.fillRect(0,0,n,n);ctx.drawImage(im,0,0,n,n);
          var rgb=ctx.getImageData(0,0,n,n).data,ink=new Float32Array(n*n);
          for(var i=0;i<ink.length;i++){var j=i*4;ink[i]=255-(.299*rgb[j]+.587*rgb[j+1]+.114*rgb[j+2]);}
          resolve(ink);
        }catch(err){reject(err);}
      };
      im.onerror=function(){reject(Error('Image could not be rendered'));};im.src=src;
    });
  }
  function pose(){
    var a=+$('poseA').value,b=+$('poseB').value;
    $('poseA-label').textContent=a+'°';$('poseB-label').textContent=b+'°';
    $('axis-a').style.transform='translate(-50%,-50%) rotate('+a+'deg)';
    $('axis-b').style.transform='translate(-50%,-50%) rotate('+b+'deg)';
    $('tilt-delta').textContent=C.poseDifference(a,b)+'°';
    ['yawA','yawB','pitchA','pitchB'].forEach(function(id){
      if($(id)&&$(id+'-label'))$(id+'-label').textContent=$(id).value+'°';
    });
    var ya=$('yawA')?+$('yawA').value:0,yb=$('yawB')?+$('yawB').value:0;
    var pa=$('pitchA')?+$('pitchA').value:0,pb=$('pitchB')?+$('pitchB').value:0;
    if($('pose-summary'))$('pose-summary').textContent=
      'A hypothesis — roll '+a+'°, yaw '+ya+'°, pitch '+pa+'°. '+
      'B hypothesis — roll '+b+'°, yaw '+yb+'°, pitch '+pb+'°. '+
      'These are manually specified perceptual interpretations, not rotations of the SVG or measured head poses.';
  }
  async function perturb(){
    if(!source||!sourceInk)return;
    var token=++renderVersion;
    $('gaps-label').textContent=$('gaps').value+'%';
    $('weight-label').textContent=(+$('weight').value/100).toFixed(2)+'×';
    try{
      var variant=edited(),u=imageURL(variant);
      $('view-a').src=u;$('view-b').src=u;
      var ink=await raster(u);
      if(token!==renderVersion)return;
      var change=M.changedPixels(sourceInk,ink,.5);
      $('changed').textContent=(100*change.fraction).toFixed(2)+'%';
      $('rho-change').textContent=M.rho(sourceInk,240,240).toFixed(3)+' → '+M.rho(ink,240,240).toFixed(3);
      $('diagnosis').textContent=change.count===0
        ? 'NO-OP: the temporary stroke edit did not change measured raster pixels. The selected primitive may be filled or have no visible stroke.'
        : 'Changed '+change.count+' of '+ink.length+' raster pixels ('+(100*change.fraction).toFixed(2)+'%). This measures a physical edit, NOT a perceptual improvement.';
    }catch(e){$('diagnosis').textContent='Edit failed: '+e.message;}
  }
  async function loadArt(){
    var token=++version;renderVersion++;
    var id=sel.value;source=art[id]||'';
    if(!source){$('diagnosis').textContent='SVG source unavailable';return;}
    try{
      parts=primitives(toDom(source));sourceInk=null;
      if(!parts.length)throw Error('No editable primitives');
      $('primitive').max=parts.length-1;$('primitive').value=0;
      $('primitive-label').textContent='1 / '+parts.length+' · '+parts[0].tagName;
      var u=imageURL(source);$('reference').src=u;
      var ink=await raster(u);if(token!==version)return;
      sourceInk=ink;perturb();
    }catch(e){if(token===version)$('diagnosis').textContent='Source error: '+e.message;}
  }
  function selectPrimitive(){
    var i=+$('primitive').value;
    $('primitive-label').textContent=(i+1)+' / '+parts.length+' · '+(parts[i]?parts[i].tagName:'');
    perturb();
  }
  function feasibility(){
    var fields=['ax','ay','bx','by'],v=fields.map(function(x){return +$(x).value;});
    if(v.some(function(x){return !Number.isFinite(x)||x<0||x>1000;})){
      $('feasible-text').textContent='Point coordinates must be within [0,1000].';return;
    }
    var eps=+$('eps').value,res=C.feasible(v.slice(0,2),v.slice(2),eps);
    $('eps-label').textContent=eps+' px';
    function cp(id,p){$(id).setAttribute('cx',p[0]);$(id).setAttribute('cy',p[1]);}
    cp('disk-a',v.slice(0,2));cp('disk-b',res.transformed);
    $('disk-a').setAttribute('r',eps);$('disk-b').setAttribute('r',eps);
    cp('point-a',v.slice(0,2));cp('point-b',res.transformed);cp('midpoint',res.midpoint);
    $('connector').setAttribute('x1',v[0]);$('connector').setAttribute('y1',v[1]);
    $('connector').setAttribute('x2',res.transformed[0]);$('connector').setAttribute('y2',res.transformed[1]);
    $('feasible-text').textContent='Distance '+res.distance.toFixed(1)+' px, allowance '+res.diameter.toFixed(1)+
      ' px. '+(res.intersect?'Intersecting':'Disjoint')+
      ' Euclidean disks only: NOT a facial recognition test.';
  }
  manifest.artifacts.filter(function(a){return a.kind==='svg'&&!!art[a.id];}).forEach(function(a){
    var opt=document.createElement('option');opt.value=a.id;opt.textContent=a.modelLabel+' · '+(a.roundLabel||'Baseline');sel.appendChild(opt);
  });
  if(!sel.options.length){$('diagnosis').textContent='No SVG records loaded';return;}
  var preferred=Array.from(sel.options).find(function(o){return o.value==='r04-glm-5.3-flash';});
  sel.value=preferred?preferred.value:sel.options[0].value;
  sel.addEventListener('change',loadArt);
  $('primitive').addEventListener('input',selectPrimitive);
  $('gaps').addEventListener('input',perturb);$('weight').addEventListener('input',perturb);
  ['poseA','poseB','yawA','yawB','pitchA','pitchB'].forEach(function(id){if($(id))$(id).addEventListener('input',pose);});
  $('baseline').addEventListener('click',function(){$('gaps').value=0;$('weight').value=100;perturb();});
  ['ax','ay','bx','by','eps'].forEach(function(id){$(id).addEventListener('input',feasibility);});
  if($('pose-preset'))$('pose-preset').addEventListener('change',function(){
    var v=this.value;
    if(v==='down-side'){$('poseA').value=-5;$('pitchA').value=-25;$('yawA').value=0;$('poseB').value=10;$('pitchB').value=0;$('yawB').value=55;}
    if(v==='frontal'){$('poseA').value=0;$('pitchA').value=0;$('yawA').value=0;$('poseB').value=0;$('pitchB').value=0;$('yawB').value=0;}
    if(v==='mixed'){$('poseA').value=-18;$('pitchA').value=15;$('yawA').value=-40;$('poseB').value=15;$('pitchB').value=-20;$('yawB').value=25;}
    pose();
  });
  pose();feasibility();loadArt();
})();