#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Experimental two-stage plan-to-SVG LLM harness. No model code is executed.

Offline prepare mode writes the prompts. Generate mode explicitly sends requests
to a user-supplied OpenAI-compatible endpoint and validates the final SVG with
the parent benchmark's safety/structure validator. No perceptual claims.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import sys
import urllib.error
import urllib.parse
import urllib.request

ROOT = Path(__file__).resolve().parents[1]

PLAN_SYSTEM = """Act as a mathematical illustrator, Gestalt researcher, semiotician,
and exacting original pen-and-ink artist. Return ONLY a JSON object, no markdown.
Plan ONE reversible portrait with two genuinely DISTINCT human facial interpretations
at 0 and 180 degrees. No separate independently complete faces stacked/overlaid.
The two upright interpretations may show DIFFERENT projected head poses (front view, profile, three-quarter, downward tilt, sideways gaze), not just different expression. No hard-coded requirement that both eye centres be visible or coincident. Both characters need different expression and personality, a coherent original
nonverbal story or joke, meaningful accessory and anatomical contour reuse,
controlled negative space, selectively suggestive and incomplete contours, variable ink weight, and purposeful high-level engraving detail.
JSON required keys: intent; face_a and face_b (each identity and expression);
optional shared_eyes (zero to two visible common anchors, each x,y in [0,1000]); pose_a and pose_b (each has yaw_degrees, pitch_degrees, roll_degrees and viewing_direction);
role_pairs (at least FIVE objects: role_a, role_b, point_a [x,y], point_b [x,y]);
silhouette (string); failure_risks (array of strings). Optional negative_space
and detail_budget. For each role pair, point_a is A in PAGE coordinates and
point_b is B in its OWN UPRIGHT frame. The exact page partner of B is
R(point_b)=(1000-x,1000-y). Apply R EXACTLY ONCE. Do not invent evidence
of human readability. Indicate structural risks and linework plan."""

SVG_SYSTEM = """Return ONLY a complete standalone, original SVG document.
Root: xmlns="http://www.w3.org/2000/svg", viewBox="0 0 1000 1000",
width="1000", height="1000", max size 300 KB. No text, scripts, animations,
images, external references, filters, gradients, network access, or metadata.
Use safe standard SVG path/circle/ellipse/line/polygon/rect/g elements.
A single coherent silhouette with two different understandable faces under
the exact 180-degree turn around (500,500). Shared feature roles and eyes
must be planned first, then robust contour design, and only then original,
expressive, fine engraving craftsmanship. Use controlled line weights, hatching,
organic contour nuance, fabric/hair/beard texture, asymmetry with purpose,
negative-space clarity and ornaments with dual function. Protect the weakest
reading and the visual joke. Not a collage of two separate faces. Do not copy
Rex Whistler's artwork; aim instead for historically sophisticated craftsmanship.
The A/B views may require different apparent yaw, pitch and roll even though the physical drawing turns by exactly 180 degrees. A front-facing symmetrical template is ONE hypothesis, not a constraint. Use selectively omitted contour segments, contextual facial configuration, figure-ground balance and varied ink weight only when they improve BOTH readings. A syntactically valid SVG is not proof of recognizable dual faces."""

def sha(s: str) -> str:
    return hashlib.sha256(s.encode("utf-8")).hexdigest()

def prep_prompts(brief: str) -> tuple[str,str]:
    if not brief.strip(): raise ValueError("empty brief")
    return (PLAN_SYSTEM + "\n\nUSER BRIEF:\n" + brief.strip(),
            SVG_SYSTEM + "\n\nDESIGN PLAN:\n{PLAN_JSON}\n")

def strip_fences(s: str) -> str:
    s=s.strip()
    tick=chr(96)
    m=re.fullmatch(re.escape(tick)*3+r"(?:json)?\s*([\s\S]*?)\s*"+re.escape(tick)*3,s,re.I)
    return m.group(1).strip() if m else s

def parse_plan(text: str) -> dict:
    plan=json.loads(strip_fences(text))
    if not isinstance(plan,dict): raise ValueError("planning response is not an object")
    for name in ("intent","face_a","face_b","role_pairs","silhouette","failure_risks"):
        if name not in plan: raise ValueError("missing planning field: "+name)
    for name in ("face_a","face_b"):
        f=plan[name]
        if not isinstance(f,dict) or not all(isinstance(f.get(n),str) and f[n].strip() for n in ("identity","expression")):
            raise ValueError("both faces need distinct descriptions")
    if not isinstance(plan.get("shared_eyes",[]),list) or len(plan.get("shared_eyes",[]))>2:
        raise ValueError("shared_eyes must contain zero to two optional anchors")
    for eye in plan.get("shared_eyes",[]):
        # When an eye anchor is absent, no assumption about a frontal face is imposed.
        if not isinstance(eye,dict) or not all(type(eye.get(n)) in (int,float) and 0<=eye[n]<=1000 for n in ("x","y")):
            raise ValueError("invalid eye point")
    if not isinstance(plan["role_pairs"],list) or len(plan["role_pairs"])<5:
        raise ValueError("at least five role pairs required")
    for p in plan["role_pairs"]:
        if not isinstance(p,dict) or not all(isinstance(p.get(n),str) for n in ("role_a","role_b")):
            raise ValueError("roles missing")
        for frame in ("point_a","point_b"):
            v=p.get(frame)
            if not isinstance(v,list) or len(v)!=2 or not all(type(x) in (float,int) and 0<=x<=1000 for x in v):
                raise ValueError("invalid coordinates: "+frame)
    for name in ("pose_a","pose_b"):
        if name in plan:
            p=plan[name]
            if not isinstance(p,dict) or not isinstance(p.get("viewing_direction",""),str):
                raise ValueError(name+" must be a pose description object")
            for axis in ("yaw_degrees","pitch_degrees","roll_degrees"):
                val=p.get(axis,0)
                if type(val) not in (int,float) or not -180<=val<=180:
                    raise ValueError("invalid "+name+" "+axis)
    return plan

def residuals(plan: dict) -> list[float]:
    return [round(((p["point_a"][0]+p["point_b"][0]-1000)**2+
                    (p["point_a"][1]+p["point_b"][1]-1000)**2)**.5,3)
            for p in plan["role_pairs"]]

def extract_svg(response: str) -> str:
    a=response.find("<svg")
    b=response.rfind("</svg>")
    if a<0 or b<a: raise ValueError("model returned no complete SVG")
    return response[a:b+len("</svg>")].strip()

def check_svg(svg: str) -> tuple[list[str],list[str]]:
    sys.path.insert(0,str(ROOT/"scripts"))
    from validate_svg import check_bytes
    errors,warnings,_=check_bytes(svg.encode("utf-8"))
    return errors,warnings

def allowed_endpoint(url: str) -> None:
    u=urllib.parse.urlparse(url)
    if u.scheme=="https" and u.hostname and not u.username and not u.password:return
    if u.scheme=="http" and u.hostname in ("127.0.0.1","localhost","::1") and not u.username and not u.password:return
    raise ValueError("HTTPS is required except loopback HTTP")

def ask(endpoint: str, model: str, system: str, user: str, max_tokens: int, timeout: int) -> str:
    allowed_endpoint(endpoint)
    if not model.strip(): raise ValueError("model name required")
    key=os.environ.get("RFB_LAB_API_KEY","")
    headers={"Content-Type":"application/json","Accept":"application/json"}
    if key:headers["Authorization"]="Bearer "+key
    body=json.dumps({"model":model,"messages":[{"role":"system","content":system},{"role":"user","content":user}],
                     "temperature":.65,"max_tokens":max_tokens}).encode("utf-8")
    req=urllib.request.Request(endpoint,body,headers,method="POST")
    try:
        with urllib.request.urlopen(req,timeout=timeout) as response:raw=response.read(8000001)
    except urllib.error.HTTPError as error:
        raise RuntimeError("provider HTTP "+str(error.code)) from None
    if len(raw)>8000000:raise ValueError("oversize provider response")
    obj=json.loads(raw)
    try:c=obj["choices"][0]["message"]["content"]
    except (KeyError,IndexError,TypeError):raise ValueError("missing response content") from None
    if isinstance(c,list):c="".join(x.get("text","") for x in c if isinstance(x,dict) and x.get("type")=="text")
    if not isinstance(c,str) or not c.strip():raise ValueError("provider returned empty text")
    return c

def save(p: Path,s: str) -> None:p.write_text(s,encoding="utf-8")

def prepare(brief: str,out: Path) -> None:
    out.mkdir(parents=True,exist_ok=True)
    p,s=prep_prompts(brief)
    save(out/"brief.txt",brief.strip()+"\n")
    save(out/"prompt-plan.txt",p+"\n")
    save(out/"prompt-svg-template.txt",s+"\n")

def generate(a: argparse.Namespace) -> int:
    out=Path(a.out)
    if out.exists() and any(out.iterdir()) and not a.overwrite:
        raise ValueError("output exists: choose new directory or --overwrite")
    prepare(a.brief,out)
    planraw=ask(a.endpoint,a.model,PLAN_SYSTEM,a.brief,a.max_tokens,a.timeout)
    save(out/"plan-model-raw.txt",planraw)
    plan=parse_plan(planraw)
    save(out/"plan.json",json.dumps(plan,indent=2,ensure_ascii=False)+"\n")
    errors=["candidate absent"];warnings=[];text=""
    for step in range(a.repair_rounds+1):
        if step==0:message="BRIEF:\n"+a.brief+"\n\nPLAN:\n"+json.dumps(plan,ensure_ascii=False)
        else:message="Repair structural validation only; retain all artistic intentions.\nErrors: "+repr(errors)+"\n\n"+text[:240000]
        raw=ask(a.endpoint,a.model,SVG_SYSTEM,message,a.max_tokens,a.timeout)
        save(out/("svg-model-raw-%02d.txt"%step),raw)
        try:
            text=extract_svg(raw);errors,warnings=check_svg(text)
        except ValueError as error:errors=[str(error)];warnings=[]
        if not errors:break
    report={"state":"structural_validation_only","model":a.model,
            "endpoint_host":urllib.parse.urlparse(a.endpoint).hostname,
            "brief_sha256":sha(a.brief),
            "plan_sha256":sha(json.dumps(plan,sort_keys=True,ensure_ascii=False)),
            "role_residuals_px":residuals(plan),"residuals_not_perceptually_calibrated":True,
            "attempts":step+1,"svg_valid":not bool(errors),"errors":errors,"warnings":warnings,
            "independent_human_reading_validated":False,"artistic_quality_validated":False}
    save(out/"report.json",json.dumps(report,indent=2,ensure_ascii=False)+"\n")
    if errors:
        print("Structural validation FAIL; no candidate.svg saved.",file=sys.stderr)
        return 1
    save(out/"candidate.svg",text+"\n")
    print("Structural validation PASS; perceptual quality NOT tested:",out/"candidate.svg")
    return 0

def main(argv=None):
    parser=argparse.ArgumentParser(description=__doc__)
    sub=parser.add_subparsers(dest="command",required=True)
    p=sub.add_parser("prepare");p.add_argument("--brief",required=True);p.add_argument("--out",default="output/dual-face-lab")
    p=sub.add_parser("generate");p.add_argument("--brief",required=True);p.add_argument("--out",default="output/dual-face-lab")
    p.add_argument("--endpoint",required=True);p.add_argument("--model",required=True)
    p.add_argument("--max-tokens",type=int,default=16000);p.add_argument("--timeout",type=int,default=120)
    p.add_argument("--repair-rounds",type=int,default=1);p.add_argument("--overwrite",action="store_true")
    p=sub.add_parser("review");p.add_argument("--svg",required=True)
    a=parser.parse_args(argv)
    try:
        if a.command=="prepare":
            prepare(a.brief,Path(a.out));print("Prepared offline:",a.out);return 0
        if a.command=="review":
            errors,warnings=check_svg(Path(a.svg).read_text(encoding="utf-8"))
            print(json.dumps({"errors":errors,"warnings":warnings,"valid":not errors,
                              "facial_recognition_validated":False},indent=2))
            return int(bool(errors))
        if not 512<=a.max_tokens<=60000 or not 0<=a.repair_rounds<=3 or not 5<=a.timeout<=300:
            raise ValueError("max-tokens / repair-rounds / timeout outside bounds")
        return generate(a)
    except (ValueError,RuntimeError,OSError,ImportError) as exc:
        print("ERROR:",str(exc),file=sys.stderr);return 2

if __name__=="__main__":raise SystemExit(main())
