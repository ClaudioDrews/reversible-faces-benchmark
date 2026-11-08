/* Exploratory interface; never mutates the archived SVG sources.
 * Source art is already bundled in the RFB site after safety review. No uploads,
 * no network model calls, no external renderer. This is NOT a human recognizer.
 */
(function() {
'use strict';
var M=window.RFBLabMath, manifest=window.RFB_MANIFEST, artwork=window.RFB_ART||{};
var $=function(id){return document.getElementById(id);};
if(!M||!manifest) {document.body.insertAdjacentHTML('afterbegin','<p class="warning">Missing benchmark manifest or mathematical module. Serve the repository root locally.</p>');return;}
var state={item:null,url:null,svg:null,primitives:[],ink:null,parity:null,angle:0,cx:500,cy:500};
var roles=[
 ['brow',452,'under-eye bag',548],
 ['hairline / fringe',380,'nose bridge',620],
 ['hat brim',350,'nose tip',650],
 ['hat / hair dome',320,'mouth',680],
 ['crown / top of hat',200,'chin',800],
 ['pompom',110,'collar / bow',890]
];
var sel=$('artifact');
manifest.artifacts.forEach(function(a){var o=document.createElement('option');o.value=a.id;o.textContent=a.modelLabel+' · '+(a.roundLabel||'Baseline')+' · '+(a.kind||'');sel.appendChild(o);});
function imageURL(s){return 'data:image/svg+xml;charset=utf-8,'+encodeURIComponent(s);}
function rasterURL(art){return '../site/'+art.file;}
function sourceURL(a){return artwork[a.id]?imageURL(artwork[a.id]):rasterURL(a);}
function updateAngle(){
 state.angle=+$('angle').value;state.cx=500+(+$('cx').value);state.cy=500+(+$('cy').value);
 $('angle-value').textContent=state.angle+'°';$('cx-value').textContent=(state.cx-500)+' px';$('cy-value').textContent=(state.cy-500)+' px';
 var art=$('main-art');
 art.style.transformOrigin=(state.cx/10)+'% '+(state.cy/10)+'%';
 art.style.transform='rotate('+state.angle+'deg)';
 $('centre-cross').style.left=(state.cx/10)+'%';$('centre-cross').style.top=(state.cy/10)+'%';
 $('landmarks').hidden=!$('guides').checked;
 art.style.filter=$('checker').checked?'invert(1)':'none';
 $('second-art').style.filter=$('checker').checked?'invert(1)':'none';
}
function loadImage(src,size) {
 return new Promise(function(resolve,reject){
  var img=new Image();
  img.onload=function(){try {
   var cv=document.createElement('canvas');cv.width=size;cv.height=size;
   var ctx=cv.getContext('2d',{willReadFrequently:true});ctx.fillStyle='#fff';ctx.fillRect(0,0,size,size);
   ctx.drawImage(img,0,0,size,size);var pixels=ctx.getImageData(0,0,size,size).data;
   var ink=new Float32Array(size*size);
   for(var i=0;i<ink.length;i++){var j=i*4;var gray=.299*pixels[j]+.587*pixels[j+1]+.114*pixels[j+2];ink[i]=255-gray;}
   resolve(ink);
  }catch(e){reject(e);}};
  img.onerror=reject;img.src=src;
 });
}
function drawingPrimitives(svg) {
 var dom=new DOMParser().parseFromString(svg,'image/svg+xml');
 if(dom.querySelector('parsererror'))throw new Error('Could not parse SVG');
 var elems=Array.from(dom.querySelectorAll('path,circle,ellipse,line,polyline,polygon,rect'));
 return elems.filter(function(el){
  // Background rectangle is not a facial primitive; never hide it.
  if(el.localName!=='rect')return true;
  return !((+el.getAttribute('width')>=990)&&(+el.getAttribute('height')>=990));
 });
}
function elementAblated(svg, index) {
 var dom=new DOMParser().parseFromString(svg,'image/svg+xml');
 var elems=drawingPrimitivesAsNodes(dom);
 if(!elems.length)return svg;
 var el=elems[Math.max(0,Math.min(elems.length-1,index))];
 el.parentNode.removeChild(el);
 return new XMLSerializer().serializeToString(dom.documentElement);
}
function drawingPrimitivesAsNodes(dom) {
 return Array.from(dom.querySelectorAll('path,circle,ellipse,line,polyline,polygon,rect')).filter(function(el){
  return el.localName!=='rect'||!(+el.getAttribute('width')>=990&&+el.getAttribute('height')>=990);
 });
}
function paint(arr,mode){
 var cv=$('analysis'),ctx=cv.getContext('2d'),data=ctx.createImageData(240,240);
 for(var i=0;i<arr.length;i++){
  var v;
  if(mode==='odd')v=128-arr[i];
  else if(mode==='negative')v=arr[i];
  else if(mode==='difference')v=255-Math.abs(arr[i]);
  else v=255-arr[i];
  v=Math.max(0,Math.min(255,Math.round(v)));
  var p=i*4;data.data[p]=v;data.data[p+1]=v;data.data[p+2]=v;data.data[p+3]=255;
 }
 ctx.putImageData(data,0,0);
}
function view() {
 if(!state.ink)return;
 var mode=$('viewmode').value,p=state.parity,arr=mode==='rotated'?p.rot:mode==='even'?p.even:mode==='odd'?p.odd:state.ink;
 paint(arr,mode);
}
function sectors() {
 if(!state.ink)return;
 var s=M.sectorMass(state.ink,240,240),elem=$('sectors');elem.textContent='';
 s.normalized.forEach(function(m){
  var cell=document.createElement('div');cell.className='sector';cell.textContent=(m*100).toFixed(1)+'%';
  cell.style.background='rgba(186,83,45,'+Math.min(.72,.06+2.3*m).toFixed(3)+')';
  elem.appendChild(cell);
 });
 $('balance').textContent=s.oppositeAsymmetry.map(function(x,i){return 'Sector '+i+' ↔ '+(8-i)+': '+x.toFixed(3);}).join('\n');
}
function stats() {
 if(!state.ink)return;
 var ink=state.ink,p=state.parity;
 $('rho').textContent=M.rho(ink,240,240).toFixed(3);
 $('ink').textContent=(M.inkFraction(ink)*100).toFixed(1)+'%';
 $('iou').textContent=M.iou(ink,p.rot).toFixed(3);
 $('count').textContent=state.svg?String(state.primitives.length):'raster';
 sectors();view();
}
var sequence=0;
async function loadArt(){
 var mine=++sequence,id=sel.value,art=manifest.artifacts.find(function(x){return x.id===id;});
 if(!art)return;state.item=art;state.svg=artwork[id]||null;state.primitives=[];
 if(state.svg){try{state.primitives=drawingPrimitives(state.svg);}catch(e){$('caption').textContent='SVG parse: '+e.message;return;}}
 var src=sourceURL(art);
 $('main-art').src=src;$('second-art').src=src;
 $('caption').textContent=art.modelLabel+' · '+(art.roundLabel||'Baseline')+' · '+art.kind+' · visual artifact, not verified facial semantics';
 $('stroke').disabled=!state.svg||!state.primitives.length;
 $('stroke').max=Math.max(0,state.primitives.length-1);$('stroke').value=0;
 $('stroke-value').textContent=state.primitives.length?'1 / '+state.primitives.length:'not available';
 $('ablation-result').textContent=state.svg?'Select a primitive to measure actual raster change.':'Raster stimulus: individual paths unavailable; segmentation requires an independent method.';
 $('ablated').src=src;
 state.ink=null;state.parity=null;
 try {
  var ink=await loadImage(src,240);
  if(mine!==sequence)return;
  state.ink=ink;state.parity=M.parity(ink,240,240);stats();if(state.svg)ablate();
 } catch(e){if(mine===sequence)$('caption').textContent='Failed to rasterize source; see browser console.';console.error(e);}
 updateAngle();
}
var ablId=0;
async function ablate(){
 if(!state.svg||!state.ink)return;
 var local=++ablId,token=sequence;
 var idx=+$('stroke').value;
 $('stroke-value').textContent=(idx+1)+' / '+state.primitives.length;
 try{
  var modified=elementAblated(state.svg,idx),url=imageURL(modified);
  $('ablated').src=url;
  var ink=await loadImage(url,240);
  if(local!==ablId||token!==sequence)return;
  var delta=M.changedPixels(state.ink,ink,.5);
  $('ablation-result').textContent='Changed raster pixels: '+delta.count+' / '+ink.length+' ('+(delta.fraction*100).toFixed(2)+'%).\nTotal grayscale-ink delta: '+Math.round(delta.totalDelta)+'.\nNo recognized-face or semantic role is inferred.';
 } catch(e){$('ablation-result').textContent='Ablation unavailable: '+e.message;}
}
roles.forEach(function(r){
 var tr=document.createElement('tr');
 var a=document.createElement('td');a.textContent=r[0]+' · '+r[1];
 var b=document.createElement('td');b.textContent=r[2]+' · '+r[3];
 var c=document.createElement('td');c.textContent=(r[1]-(1000-r[3]))+' px';
 tr.append(a,b,c);$('roles').appendChild(tr);
});
$('fit').onclick=function(){
 var a=[+$('ax').value,+$('ay').value],b=[+$('bx').value,+$('by').value];
 try{var c=M.fittedCentre([{a:a,b:b}]),d=M.distanceToRotated(a,b,[500,500]);$('fit-result').textContent='Fitted centre: ('+c.map(function(x){return x.toFixed(1);}).join(', ')+') · official-centre residual '+d.toFixed(1)+' px.\nThis one-pair fit cannot establish facial alignment.';}
 catch(e){$('fit-result').textContent=e.message;}
};
$('copy-prompt').onclick=function(){
 var brief=$('brief').value.trim(),t='Create ONE original high-detail reversible-face SVG. Creative brief: '+brief+'\n\n'+
 'First produce a semantic plan: distinct face A/B, expressions, nonverbal story, shared eyes, 5+ role correspondences, negative-space and silhouette constraints. Each B target b is upright; map to page with R(b)=(1000-x,1000-y) exactly once.\n'+
 'Second draw ONE coherent SVG (viewBox 0 0 1000 1000, width/height 1000). Prioritize dual-legible contour graph, then purposefully differentiated line weight and fine engraving (hatch, wrinkles, fabrics, ornaments) that preserve B. No two independent portraits, text, external images, scripts, gradients or filters.\n'+
 'Third inspect the source structurally; a visual render/critic is required for perceptual claims. Never claim observer recognition without evidence.';
 if(navigator.clipboard&&navigator.clipboard.writeText)navigator.clipboard.writeText(t).then(function(){$('copy-prompt').textContent='Copied ✓';setTimeout(function(){$('copy-prompt').textContent='Copy structured prompt';},1400);}).catch(function(){$('copy-prompt').textContent='Copy unavailable';});
 else $('copy-prompt').textContent='Clipboard unavailable';
};
sel.onchange=loadArt;$('angle').oninput=updateAngle;$('cx').oninput=updateAngle;$('cy').oninput=updateAngle;$('checker').onchange=updateAngle;$('guides').onchange=updateAngle;
$('upright').onclick=function(){$('angle').value=0;updateAngle();};
$('inverted').onclick=function(){$('angle').value=180;updateAngle();};
$('reset').onclick=function(){$('cx').value=0;$('cy').value=0;updateAngle();};
$('viewmode').onchange=view;$('stroke').oninput=ablate;
$('sector-details').onclick=function(){var e=$('balance');e.hidden=!e.hidden;};
$('balance').hidden=true;
sel.value=(manifest.artifacts.find(function(a){return a.id==='r04-glm-5.3-flash';})||manifest.artifacts[0]).id;
loadArt();
})();
