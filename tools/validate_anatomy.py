#!/usr/bin/env python3
"""Validate the INR anatomy catalogue and optionally build browser JSON.

v0.2 validates the data contract, asset references, legacy skull context and
seed atlas-derived vascular geometry. Medical-image segmentation remains a separate pipeline.
"""
from __future__ import annotations
import argparse, json, struct, shutil, hashlib, math
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
CAT=ROOT/'anatomy'/'catalogue'
PUBLIC=ROOT/'public'/'anatomy'
FILES=('bones.json','arteries.json','veins.json','brain.json')
SIDES={'left','right','midline'}
SYSTEMS={'bone','artery','vein','brain'}
RELEASE=json.loads((ROOT/'package.json').read_text())['version']


def read_json(p:Path):
    with p.open(encoding='utf-8') as f:return json.load(f)

def glb_nodes(p:Path)->set[str]:
    data=p.read_bytes()
    if len(data)<20 or data[:4]!=b'glTF': raise ValueError(f'{p}: not a GLB')
    _,version,total=struct.unpack_from('<4sII',data,0)
    if version!=2 or total!=len(data): raise ValueError(f'{p}: unsupported/corrupt GLB')
    off=12; doc=None
    while off<len(data):
        ln,typ=struct.unpack_from('<II',data,off); off+=8
        chunk=data[off:off+ln]; off+=ln
        if typ==0x4E4F534A: doc=json.loads(chunk.decode('utf-8').rstrip('\x00 \t\r\n')); break
    if doc is None: raise ValueError(f'{p}: missing JSON chunk')
    return {n.get('name','') for n in doc.get('nodes',[]) if n.get('name')}

def validate_eca(build=False, filename="eca_manifest.json", output="eca-manifest.json"):
    """Validate the separate reference reconstruction, including its exact hierarchy."""
    manifest=read_json(ROOT/'anatomy/generated'/filename)
    rows=manifest['structures']; byid={s['id']:s for s in rows}; errors=[]; assets={}
    schema=read_json(ROOT/'anatomy/metadata/provenance.json')
    sources={s['id'] for s in manifest['sources']}
    if len(byid)!=len(rows): errors.append('ECA: duplicate structure IDs')
    if manifest.get('coordinateSystem')!='RAS' or manifest.get('units')!='mm':
        errors.append('ECA: expected RAS millimetres')
    for s in rows:
        sid=s['id']; parent=s.get('parent')
        if parent and parent not in byid: errors.append(f'ECA {sid}: missing parent {parent}')
        if s.get('side') not in SIDES or s.get('system') not in SYSTEMS:
            errors.append(f'ECA {sid}: invalid side/system')
        if s.get('geometryStatus') not in schema['geometryStatuses']:
            errors.append(f'ECA {sid}: invalid geometryStatus')
        pr=s.get('provenance',{})
        if pr.get('sourceType') not in schema['sourceTypes'] or pr.get('reviewStatus') not in schema['reviewStatuses']:
            errors.append(f'ECA {sid}: invalid provenance')
        if any(ref not in sources for ref in pr.get('sourceRefs',[])):
            errors.append(f'ECA {sid}: unknown source reference')
        expected={r['id'] for r in rows if r.get('parent')==sid}
        if set(s.get('children',[]))!=expected or len(s.get('children',[]))!=len(expected):
            errors.append(f'ECA {sid}: inconsistent children')
        seen=set(); node=sid
        while node in byid:
            if node in seen:
                errors.append(f'ECA {sid}: cyclic hierarchy'); break
            seen.add(node); node=byid[node].get('parent')
        if s.get('color') and (len(s['color'])!=7 or not s['color'].startswith('#') or any(c not in '0123456789abcdefABCDEF' for c in s['color'][1:])):
            errors.append(f'ECA {sid}: invalid colour')
        if s.get('asset'):
            a=s['asset']; p=PUBLIC/a['file']
            try:
                if p not in assets: assets[p]=glb_nodes(p)
                if a['node'] not in assets[p]: errors.append(f'ECA {sid}: missing GLB node {a["node"]}')
            except Exception as e: errors.append(f'ECA {sid}: {e}')
        if 'landmark' in s:
            lm=s['landmark']; point=lm.get('point'); course=lm.get('course',[])
            if lm.get('status') not in {'visible','partial','regional','unresolved','variant-unresolved','bone-unavailable'}:
                errors.append(f'{sid}: invalid landmark status')
            for xyz in ([point] if point is not None else []) + course:
                if not isinstance(xyz,list) or len(xyz)!=3 or not all(isinstance(v,(int,float)) and math.isfinite(v) for v in xyz):
                    errors.append(f'{sid}: invalid landmark coordinates')
            if point is None and course: errors.append(f'{sid}: unlocated landmark has a course')
            if lm.get('status') in {'unresolved','variant-unresolved','bone-unavailable'} and point is not None:
                errors.append(f'{sid}: unresolved landmark must not invent a point')
    if set(manifest['roots'])!={s['id'] for s in rows if s.get('parent') is None}:
        errors.append('ECA: inconsistent roots')
    bindings=[(s['asset']['file'],s['asset']['node']) for s in rows if s.get('asset')]
    if len(bindings)!=len(set(bindings)): errors.append('ECA: duplicate asset bindings')
    for r in manifest['relationships']:
        if r['from'] not in byid or r['to'] not in byid:
            errors.append('ECA: relationship references an unknown structure')
        elif r['type']=='branches_to' and byid[r['to']]['parent']!=r['from']:
            errors.append('ECA: branching relationship differs from hierarchy')
    if build and not errors:
        manifest['release']=RELEASE
        manifest['assetRevisions']={str(p.relative_to(PUBLIC)):hashlib.sha256(p.read_bytes()).hexdigest()[:20] for p in assets}
        (PUBLIC/output).write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf-8')
    return errors,len(bindings)

if __name__ == '__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--build',action='store_true');args=parser.parse_args()
    errors,count=validate_eca(args.build, 'complete_manifest.json', 'manifest.json')
    manifest=read_json(ROOT/'anatomy/generated/complete_manifest.json')
    required={s['asset']['file'] for s in manifest['structures'] if s.get('asset')}
    actual={str(p.relative_to(PUBLIC)) for p in (PUBLIC/'models').glob('*.glb')}
    if required != actual: errors.append(f'Unexpected or missing production assets: {required ^ actual}')
    if errors:
        print('\n'.join(errors));raise SystemExit(1)
    print(f'Validated one combined scene, {count} named parts, {len(required)} assets.')
