#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Download four public-domain Whistler reproductions; produce an auditable
single-source raster/vector geometry corpus. This is NOT a face recognizer.
All derived source images are kept in workflow artifacts, not repository code.
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import html
import io
import json
from pathlib import Path
import re
import shutil
import sys
import time
from urllib import parse, request
import warnings

import numpy as np
import cv2
from PIL import Image, ImageOps
from skimage.metrics import structural_similarity
import cairosvg

REPO = Path(__file__).resolve().parents[2]
UA = "ReversibleFacesBenchmarkResearch/0.1 (https://github.com/ClaudioDrews/reversible-faces-benchmark)"
Image.MAX_IMAGE_PIXELS = 40_000_000
SQUARE = 512
MAX_BYTES = 16_000_000

def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()

def write_json(path: Path, obj) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=2, ensure_ascii=False, sort_keys=True)+"\n", encoding="utf-8")

def commons_hashed_url(name: str) -> str:
    """Documented Wikimedia upload hashing convention, deterministic fallback."""
    key = name.replace(" ","_")
    md5 = hashlib.md5(key.encode("utf-8")).hexdigest()
    return "https://upload.wikimedia.org/wikipedia/commons/"+md5[0]+"/"+md5[:2]+"/"+parse.quote(key, safe="()_-.~")

def mediawiki_info(name: str) -> dict:
    params=parse.urlencode({"action":"query","format":"json","prop":"imageinfo",
                             "iiprop":"url|size|sha1|mime|extmetadata",
                             "titles":"File:"+name})
    endpoint="https://commons.wikimedia.org/w/api.php?"+params
    req=request.Request(endpoint,headers={"User-Agent":UA,"Accept":"application/json"})
    with request.urlopen(req,timeout=40) as resp:
        raw=resp.read(2_000_001)
    if len(raw)>2_000_000:raise ValueError("oversize Commons metadata")
    page=next(iter(json.loads(raw)["query"]["pages"].values()))
    if "imageinfo" not in page:raise ValueError("file not found in Commons API: "+name)
    return page["imageinfo"][0]

def download_exact(entry: dict, out: Path) -> tuple[bytes,dict]:
    name=entry["commons_file"]
    meta_error=None
    info={}
    try:
        info=mediawiki_info(name)
        source_url=info["url"]
    except Exception as exc:
        meta_error=str(exc)
        source_url=commons_hashed_url(name)
    if not source_url.startswith("https://upload.wikimedia.org/wikipedia/commons/"):
        raise ValueError("refusing non-Wikimedia source URL: "+source_url)
    last_err=None
    for i in range(3):
        try:
            req=request.Request(source_url,headers={"User-Agent":UA,
                "Accept":"image/jpeg,image/png;q=0.9,*/*;q=0.2"})
            with request.urlopen(req,timeout=65) as response:
                final_url=response.geturl()
                if parse.urlparse(final_url).hostname!="upload.wikimedia.org":
                    raise ValueError("unexpected source redirect "+final_url)
                original=response.read(MAX_BYTES+1)
                if len(original)>MAX_BYTES or len(original)<2000:
                    raise ValueError("source file too small or exceeds 16 MB")
                mime=response.headers.get("Content-Type","")
            img=Image.open(io.BytesIO(original))
            img.verify()
            break
        except Exception as exc:
            last_err=exc
            if i<2:time.sleep(2**i)
    else:
        raise RuntimeError("Commons download failed for "+name+": "+str(last_err))
    out.parent.mkdir(parents=True,exist_ok=True)
    out.write_bytes(original)
    return original,{"commons_title":name,"source_page":entry["source_page"],
        "resolved_file_url":source_url,"source_sha256":digest(original),
        "source_bytes":len(original),"source_content_type":mime,
        "wiki_sha1":info.get("sha1"),"wiki_size":info.get("size"),
        "wiki_mime":info.get("mime"),"wiki_license_short":
            info.get("extmetadata",{}).get("LicenseShortName",{}).get("value"),
        "wiki_license_url":info.get("extmetadata",{}).get("LicenseUrl",{}).get("value"),
        "metadata_error":meta_error,
        "fetched_utc":datetime.now(timezone.utc).isoformat()}

def crop_and_square(panel: Image.Image, size: int=SQUARE) -> tuple[Image.Image,dict]:
    """Choose dominant connected ink region, with explicit fallback.
    This is an automated candidate crop, NEVER a perceptual verification."""
    p=ImageOps.exif_transpose(panel).convert("RGB")
    gray=cv2.cvtColor(np.asarray(p),cv2.COLOR_RGB2GRAY)
    mask=(gray<227).astype(np.uint8)
    kernel=cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(5,5))
    dilated=cv2.morphologyEx(mask,cv2.MORPH_CLOSE,kernel)
    n,_,stats,_=cv2.connectedComponentsWithStats(dilated,8)
    candidates=sorted((stats[i] for i in range(1,n)),key=lambda row:int(row[4]),reverse=True)
    bounds=None
    if candidates and candidates[0][4]>max(100,gray.size*.006):
        # Ignore isolated page signatures; keep multiple sizeable art components.
        main=int(candidates[0][4])
        big=[s for s in candidates if s[4]>max(80,main*.10)]
        l=min(int(s[0]) for s in big);t=min(int(s[1]) for s in big)
        r=max(int(s[0]+s[2]) for s in big);b=max(int(s[1]+s[3]) for s in big)
        padx=int(max(r-l,b-t)*.055)
        l=max(0,l-padx);t=max(0,t-padx)
        r=min(p.width,r+padx);b=min(p.height,b+padx)
        if (r-l)>p.width*.20 and (b-t)>p.height*.20:
            bounds=(l,t,r,b)
    if bounds is None:bounds=(0,0,p.width,p.height)
    crop=p.crop(bounds)
    side=int(max(crop.size)*1.08)
    square=Image.new("RGB",(side,side),"white")
    square.paste(crop,((side-crop.width)//2,(side-crop.height)//2))
    norm=square.resize((size,size),Image.Resampling.LANCZOS)
    return norm,{"panel_original_size":p.size,"crop_box":bounds,
                "square_side_before_resize":side,"normalized_size":size}

def panels(img: Image.Image, size: int=SQUARE) -> tuple[Image.Image,Image.Image,dict]:
    src=ImageOps.exif_transpose(img).convert("RGB")
    w,h=src.size
    if w<1.16*h:raise ValueError("source not obviously two-up, require manual crop: "+str(src.size))
    mid=w//2
    left,a=crop_and_square(src.crop((0,0,mid,h)),size)
    right,b=crop_and_square(src.crop((mid,0,w,h)),size)
    return left,right,{"source_size":src.size,"split_x":mid,"left_transform":a,"right_transform":b,
                       "warning":"Estimated split/crop: visually inspect against source."}

def normalized_correlation(a: np.ndarray,b: np.ndarray)->float:
    aa=a.astype(np.float64).ravel();bb=b.astype(np.float64).ravel()
    aa-=aa.mean();bb-=bb.mean()
    den=np.linalg.norm(aa)*np.linalg.norm(bb)
    return float(aa.dot(bb)/den) if den>1e-10 else 0.0

def best_shift(a: np.ndarray,b: np.ndarray,maxshift: int=12,step: int=4) -> dict:
    """Only small, predeclared translational registration; no deformation."""
    best=(-2.0,0,0)
    for dy in range(-maxshift,maxshift+1,step):
        for dx in range(-maxshift,maxshift+1,step):
            mm=np.float32([[1,0,dx],[0,1,dy]])
            trial=cv2.warpAffine(b,mm,(a.shape[1],a.shape[0]),flags=cv2.INTER_LINEAR,
                                 borderMode=cv2.BORDER_CONSTANT,borderValue=255)
            corr=normalized_correlation(255-a,255-trial)
            if corr>best[0]:best=(corr,dx,dy)
    return {"correlation":round(float(best[0]),5),"dx":int(best[1]),"dy":int(best[2])}

def compare_panels(a: Image.Image,b: Image.Image) -> dict:
    aa=np.asarray(a.convert("L"))
    bb=np.asarray(b.convert("L"))
    upright=best_shift(aa,bb)
    rotated=best_shift(aa,cv2.rotate(bb,cv2.ROTATE_180))
    better="180" if rotated["correlation"]>=upright["correlation"] else "0"
    return {"no_rotation":upright,"rotate_right_180":rotated,
            "higher_correlation_alignment":better,
            "caveat":"Crop/scan alignment test, not proof of dual interpretation."}

def trace_paths(mask: np.ndarray,closed: bool=True, min_area: float=3,
                min_arc: float=9, tolerance: float=.70, cap: int=12000) -> tuple[list[str],int]:
    """Trace boundaries at SVG/ink level, NOT semantic strokes."""
    mode=cv2.RETR_LIST
    contours,_=cv2.findContours(mask.astype(np.uint8),mode,cv2.CHAIN_APPROX_SIMPLE)
    contours=sorted(contours,key=lambda c:cv2.arcLength(c,closed),reverse=True)
    out=[]
    for c in contours:
        if closed and abs(cv2.contourArea(c))<min_area:continue
        if cv2.arcLength(c,closed)<min_arc:continue
        a=cv2.approxPolyDP(c,tolerance,closed)[:,0,:]
        if len(a)<(3 if closed else 2):continue
        d="M"+" ".join(str(int(a[0,i])) for i in (0,1))
        d+=" "+" ".join("L"+str(int(p[0]))+" "+str(int(p[1])) for p in a[1:])
        if closed:d+=" Z"
        out.append(d)
        if len(out)>=cap:break
    return out,len(contours)

def svg_header(w: int,h: int)->str:
    return ('<svg xmlns="http://www.w3.org/2000/svg" '
            'width="1000" height="1000" viewBox="0 0 1000 1000">\n'
            '<rect width="1000" height="1000" fill="#ffffff"/>\n'
            '<g transform="scale('+format(1000/w,'.8g')+' '+format(1000/h,'.8g')+')">\n')

def svg_from_raster(gray: np.ndarray,kind: str) -> tuple[str,dict]:
    """Produce three contrasting *derived* SVG representations, same canonical A."""
    h,w=gray.shape
    source=svg_header(w,h)
    total=0;detected=0
    if kind in ("binary","tonal"):
        layers=[(150,"#262626")] if kind=="binary" else [
            (235,"#ededed"),(200,"#cacaca"),(155,"#999999"),
            (110,"#6c6c6c"),(65,"#353535"),(28,"#101010")]
        for threshold,color in layers:
            paths,count=trace_paths(np.uint8(gray<=threshold)*255,True,3,9,.65)
            total+=len(paths);detected+=count
            if paths:
                source+='<path fill="'+color+'" fill-rule="evenodd" d="'+' '.join(paths)+'"/>\n'
    elif kind=="contours":
        edges=cv2.Canny(gray,60,150,L2gradient=True)
        paths,count=trace_paths(edges,False,0,13,.9)
        total+=len(paths);detected+=count
        for d in paths:
            source+='<path d="'+d+'" fill="none" stroke="#242424" stroke-width="1.2" stroke-linecap="round"/>\n'
    else:raise ValueError("unknown representation "+kind)
    source+='</g>\n</svg>\n'
    return source,{"primitive_count":total,"detected_contour_count":detected,
                   "threshold_semantics":"binary 150; tonal levels 235/200/155/110/65/28; edges Canny 60/150",
                   "raster_size":(w,h),"raster_derivation":"opencv contours"}

def grayscale(img: Image.Image)->np.ndarray:
    return np.asarray(img.convert("L")).copy()

def fidelity(ref: np.ndarray,approx: np.ndarray)->dict:
    if ref.shape!=approx.shape:raise ValueError("grayscale comparison shapes differ")
    diff=(ref.astype(np.float64)-approx.astype(np.float64))
    mse=float((diff**2).mean())
    mae=float(np.abs(diff).mean())
    ssim=float(structural_similarity(ref,approx,data_range=255))
    frac=float((np.abs(diff)>5).mean())
    hist_ref=np.histogram(ref,bins=[0,64,128,192,240,256])[0]
    hist_approx=np.histogram(approx,bins=[0,64,128,192,240,256])[0]
    psnr=None if mse==0 else float(10*np.log10(255**2/mse))
    return {"MAE":round(mae,4),"SSIM":round(ssim,5),
            "PSNR_dB":round(psnr,3) if psnr is not None else "identical / infinity",
            "changed_fraction_at_5_gray":round(frac,5),
            "gray_bins_ref":hist_ref.tolist(),"gray_bins_svg":hist_approx.tolist(),
            "source_dark_ink_fraction":round(float((ref<190).mean()),5),
            "svg_dark_ink_fraction":round(float((approx<190).mean()),5)}

def render_svg(svg: str,size: int=SQUARE)->np.ndarray:
    raster=cairosvg.svg2png(bytestring=svg.encode("utf-8"),output_width=size,output_height=size)
    return np.asarray(Image.open(io.BytesIO(raster)).convert("L"))

def region_mask(shape,region: str)->np.ndarray:
    h,w=shape
    yy,xx=np.indices((h,w))
    r=np.sqrt(((xx+.5-w/2)/(w*.5))**2+((yy+.5-h/2)/(h*.5))**2)
    return (r<.46) if region=="centre" else (r>.65)

def perturb_variant(gray: np.ndarray,region: str,operation: str,seed=20261108)->np.ndarray:
    mask=region_mask(gray.shape,region)
    altered=gray.copy()
    if operation=="blur":
        blurred=cv2.GaussianBlur(gray,(9,9),2.4)
        altered[mask]=blurred[mask]
    elif operation=="dilate-ink":
        ink=255-gray
        grown=cv2.dilate(ink,cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(3,3)))
        altered[mask]=255-grown[mask]
    elif operation=="erode-ink":
        ink=255-gray
        reduced=cv2.erode(ink,cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(3,3)))
        altered[mask]=255-reduced[mask]
    elif operation=="gaps":
        ink=np.uint8(gray<185)
        eligible=np.argwhere(mask & (ink>0))
        if eligible.size:
            rng=np.random.default_rng(seed)
            choices=eligible[rng.choice(len(eligible),size=min(26,len(eligible)),replace=False)]
            holes=np.zeros_like(gray,np.uint8)
            for y,x in choices:
                cv2.ellipse(holes,(int(x),int(y)),(int(rng.integers(2,6)),int(rng.integers(2,5))),
                            int(rng.integers(0,180)),0,360,255,-1)
            altered[(holes>0)&mask]=255
    else:raise ValueError("unknown operation")
    return altered

def source_processor(record:dict,out:Path,download=download_exact, size=SQUARE)->dict:
    ident=record["id"]
    raw,info=download(record,out/"source"/(ident+".jpg"))
    im=Image.open(io.BytesIO(raw)).convert("RGB")
    a,b,layout=panels(im,size)
    (out/"canonical").mkdir(parents=True,exist_ok=True)
    a.save(out/"canonical"/(ident+"-single-source.png"))
    b.save(out/"canonical"/(ident+"-opposite-panel.png"))
    registration=compare_panels(a,b)
    g=grayscale(a)
    item={"id":ident,"title":record["description"],"provenance":info,
          "layout":layout,"registration":registration,"vectors":{},"perturbations":{}}
    (out/"vector").mkdir(parents=True,exist_ok=True)
    (out/"preview").mkdir(parents=True,exist_ok=True)
    for kind in ("binary","tonal","contours"):
        svg,stats=svg_from_raster(g,kind)
        p=out/"vector"/(ident+"-"+kind+".svg")
        p.write_text(svg,encoding="utf-8")
        preview=render_svg(svg,size)
        Image.fromarray(preview).save(out/"preview"/(ident+"-"+kind+".png"))
        item["vectors"][kind]={"svg_path":str(p.relative_to(out)),
            "source":str((out/"canonical"/(ident+"-single-source.png")).relative_to(out)),
            "source_is_single_canonical_panel":True,"bytes":p.stat().st_size,
            "sha256":digest(p.read_bytes()),"strict_300KB_limit":p.stat().st_size<=300*1024,
            "trace":stats,"raster_fidelity":fidelity(g,preview)}
    for region in ("centre","outer"):
        for operation in ("blur","gaps","dilate-ink","erode-ink"):
            variant=perturb_variant(g,region,operation)
            folder=out/"perturbations"/ident
            folder.mkdir(parents=True,exist_ok=True)
            name=region+"-"+operation+".png"
            Image.fromarray(variant).save(folder/name)
            item["perturbations"][region+"-"+operation]={
                "file":str((folder/name).relative_to(out)),
                "sha256":digest((folder/name).read_bytes()),
                "MAE_to_canonical":round(float(np.abs(g.astype(np.float32)-variant.astype(np.float32)).mean()),5),
                "changed_pixels":int((np.abs(g.astype(np.int16)-variant.astype(np.int16))>1).sum()),
                "region":"page-radius-centre" if region=="centre" else "page-radius-outer",
                "operation":operation,"seed":20261108}
    return item

def contact_sheet(out:Path,records:list[dict])->None:
    cells=[]
    for r in records:
        ident=r["id"]
        files=["canonical/"+ident+"-single-source.png",
              "canonical/"+ident+"-opposite-panel.png",
              "preview/"+ident+"-binary.png","preview/"+ident+"-tonal.png",
              "preview/"+ident+"-contours.png"]
        cells.append("<section><h2>"+html.escape(r["title"])+"</h2><p>Panel rotation correlation: "+
             str(r["registration"]["rotate_right_180"]["correlation"])+
             "; preferred orientation: "+html.escape(r["registration"]["higher_correlation_alignment"])+"</p>"+
             "<div class='grid'>"+''.join("<figure><img src='"+html.escape(path)+"' alt='"+html.escape(path)+"'><figcaption>"+html.escape(path.split("/")[-1])+"</figcaption></figure>" for path in files)+"</div></section>")
    body="<!doctype html><html lang='en'><meta charset='utf-8'><title>Whistler reference corpus</title>"
    body+="<style>body{font:16px system-ui;margin:2em;background:#faf8f3;color:#282524}section{margin-bottom:4em}h1,h2{font-family:Georgia,serif}.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(180px,1fr));gap:15px}figure{margin:0;border:1px solid #ddd;padding:10px;background:white}img{width:100%;height:auto}figcaption{font-size:12px;overflow-wrap:anywhere}</style>"
    body+="<h1>Whistler · historical single-source vectorization</h1><p>Geometric inspection; no perceptual validation. Art sources: Wikimedia Commons public domain file pages; see report.json for provenance.</p>"
    body+="".join(cells)+"</html>"
    (out/"index.html").write_text(body,encoding="utf-8")

def main(argv=None)->int:
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--catalog",default=str(Path(__file__).with_name("catalog.json")))
    ap.add_argument("--out",default=str(REPO/"output"/"whistler-corpus"))
    ap.add_argument("--limit",type=int,default=4)
    a=ap.parse_args(argv)
    catalog=json.loads(Path(a.catalog).read_text(encoding="utf-8"))
    if a.limit<1 or a.limit>4:ap.error("limit must be in 1..4")
    out=Path(a.out)
    out.mkdir(parents=True,exist_ok=True)
    results=[];errors=[]
    for record in catalog["records"][:a.limit]:
        try:
            result=source_processor(record,out)
            results.append(result)
            print("OK",result["id"],result["provenance"]["source_sha256"][:12],
                  "rotation correlation",result["registration"]["rotate_right_180"]["correlation"],
                  "tonal SSIM",result["vectors"]["tonal"]["raster_fidelity"]["SSIM"],flush=True)
        except Exception as exc:
            errors.append({"id":record["id"],"reason":str(exc)})
            print("FAILED",record["id"],repr(exc),file=sys.stderr,flush=True)
    summary={"method":"Original Commons image > split-check > one canonical raster >"
              " original-source-only three SVG representations and controlled image perturbations",
             "retrieval_utc":datetime.now(timezone.utc).isoformat(),
             "source_catalog_sha256":digest(Path(a.catalog).read_bytes()),
             "size":SQUARE,"results":results,"failures":errors,
             "perceptual_faces_validated":False,
             "historical_art_is_ground_truth_for_effectiveness":False,
             "automated_crop_human_verified":False}
    write_json(out/"report.json",summary)
    contact_sheet(out,results)
    if errors or not results:return 1
    return 0

if __name__=="__main__":
    raise SystemExit(main())
