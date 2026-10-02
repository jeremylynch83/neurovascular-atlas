#!/usr/bin/env python3
"""Validate the INR anatomy catalogue and optionally build browser JSON.

v0.2 validates the data contract, asset references, legacy skull context and
seed atlas-derived vascular geometry. Medical-image segmentation remains a separate pipeline.
"""
from __future__ import annotations
import argparse, json, struct, shutil
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
CAT=ROOT/'anatomy'/'catalogue'
PUBLIC=ROOT/'public'/'anatomy'
FILES=('bones.json','arteries.json','veins.json','brain.json')
SIDES={'left','right','midline'}
SYSTEMS={'bone','artery','vein','brain'}


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

def validate(build=False):
    errors=[]; warnings=[]; structures=[]
    for fn in FILES:
        p=CAT/fn
        if not p.exists(): errors.append(f'missing catalogue {p}'); continue
        rows=read_json(p)
        if not isinstance(rows,list): errors.append(f'{p}: root must be a list'); continue
        structures.extend(rows)
    # Optional generated scan-derived overlay. The immutable hand-authored catalogue
    # remains separate from generated source-data products.
    generated_case=None
    gp=ROOT/'anatomy'/'generated'/'topbrain_patch.json'
    if gp.exists():
        g=read_json(gp); generated_case=g.get('case'); byid={x.get('id'):x for x in structures}
        for patch in g.get('patch',[]):
            sid=patch.get('id')
            if patch.get('new'):
                if sid not in byid:
                    row={k:v for k,v in patch.items() if k!='new'}; structures.append(row); byid[sid]=row
            elif sid in byid:
                byid[sid].update({k:v for k,v in patch.items() if k not in ('id','new')})
    ids=[s.get('id') for s in structures]; idset=set(ids)
    dup={i for i in ids if ids.count(i)>1}
    if dup: errors.append('duplicate IDs: '+', '.join(sorted(dup)))
    sources={x['id'] for x in read_json(ROOT/'anatomy'/'sources.json')}
    prov_schema=read_json(ROOT/'anatomy'/'metadata'/'provenance.json')
    allowed_source=set(prov_schema['sourceTypes']); allowed_review=set(prov_schema['reviewStatuses']); allowed_geom=set(prov_schema['geometryStatuses'])
    glb_cache={}
    for s in structures:
        i=s.get('id','<missing>'); p=s.get('parent')
        if not i or not isinstance(i,str): errors.append(f'{i}: invalid id'); continue
        if p is not None and p not in idset: errors.append(f'{i}: missing parent {p}')
        if s.get('side') not in SIDES: errors.append(f'{i}: invalid side {s.get("side")}')
        if s.get('system') not in SYSTEMS: errors.append(f'{i}: invalid system {s.get("system")}')
        if s.get('geometryStatus') not in allowed_geom: errors.append(f'{i}: invalid geometryStatus')
        pr=s.get('provenance',{})
        if pr.get('sourceType') not in allowed_source: errors.append(f'{i}: invalid provenance sourceType')
        if pr.get('reviewStatus') not in allowed_review: errors.append(f'{i}: invalid reviewStatus')
        for ref in pr.get('sourceRefs',[]):
            if ref not in sources: errors.append(f'{i}: unknown sourceRef {ref}')
        a=s.get('asset')
        if a:
            ap=PUBLIC/a.get('file','')
            if not ap.exists(): errors.append(f'{i}: missing asset file {ap}')
            else:
                try:
                    nodes=glb_cache.setdefault(ap,glb_nodes(ap))
                    if a.get('node') not in nodes: errors.append(f'{i}: node {a.get("node")} absent from {ap.name}')
                except Exception as e: errors.append(str(e))
    rels=read_json(ROOT/'anatomy'/'relationships.json')
    for r in rels:
        if r.get('from') not in idset: errors.append(f'relationship missing from: {r.get("from")}')
        if r.get('to') not in idset: errors.append(f'relationship missing to: {r.get("to")}')
        if r.get('from')==r.get('to'): errors.append(f'self relationship: {r.get("from")}')
    # Build children and a compact browser manifest only after validation.
    if build and not errors:
        children={i:[] for i in idset}
        for s in structures:
            if s.get('parent'): children[s['parent']].append(s['id'])
        built=[]
        for s in structures:
            row=dict(s); row['children']=sorted(children[s['id']]); built.append(row)
        PUBLIC.mkdir(parents=True,exist_ok=True)
        for fn in FILES:
            shutil.copy2(CAT/fn,PUBLIC/fn)
        for fn in ('relationships.json','sources.json'):
            shutil.copy2(ROOT/'anatomy'/fn,PUBLIC/fn)
        manifest={'schemaVersion':'0.3','release':'0.3.0','units':'scan-derived TopBrain assets use source NIfTI physical coordinates (mm); legacy atlas seed assets remain in their legacy coordinate frame and should not be interpreted as registered to the scan-derived reference','structures':built,'relationships':rels,'sources':read_json(ROOT/'anatomy'/'sources.json'),'roots':['bone','artery','vein','brain'],'warning':('v0.3 scan-derived reference case '+str(generated_case)+' loaded. Legacy atlas-derived ECA seed geometry is NOT registered to the TopBrain reference and should not be used for spatial comparison.' if generated_case else 'v0.3 source-data pipeline is ready, but no TopBrain reference case has been built yet. Run ./anatomy.sh download, inspect and build <case>.')}
        (PUBLIC/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf-8')
    return errors,warnings,len(structures),len(rels)

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--build',action='store_true'); args=ap.parse_args()
    errors,warnings,n,nr=validate(args.build)
    for w in warnings: print('WARNING:',w)
    if errors:
        for e in errors: print('ERROR:',e)
        raise SystemExit(f'Anatomy validation failed with {len(errors)} error(s).')
    print(f'Anatomy catalogue valid: {n} structures, {nr} explicit relationships.')
    if args.build: print('Browser manifest written to public/anatomy/manifest.json')
if __name__=='__main__': main()
