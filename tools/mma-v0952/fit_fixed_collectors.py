"""Keep native dural collector junctions fixed during cortical vessel transport.

One common receiver mask is used for all cortical venous labels so that nearby
native tributary junctions agree. It refits drainage stems, rather than moving
the bone-bound collector with the cortex. Subsequent full vessel checks remain
required; this operation alone cannot grant acceptance.
"""
from common import *
revision=json.loads((OUT/'revision.json').read_text())
changed={r['node']:r for r in revision['changed']}
before=json.loads((OUT/'field-interface-check.json').read_text())
anchors={'venous':[],'arterial':[]}
for row in before['exactSharedInterfaces']:
    if row['maxMismatchMm']<=1e-4:continue
    a,b=row['a'],row['b'];v,f=load(a);w,g=load(b)
    dd=cKDTree(w).query(v)[0];shared=v[dd<1e-5]
    category='venous' if a.startswith('vein.') and b.startswith('vein.') else 'arterial'
    anchors[category].extend(shared.tolist())
trees={key:cKDTree(np.unique(np.asarray(value),axis=0)) for key,value in anchors.items() if value}
updates=[]
for n,row in changed.items():
    if n not in FILES or row.get('file') not in ['venous.glb','complete-circulation.glb','complete-anastomoses.glb']:continue
    category='venous' if n.startswith('vein.') else 'arterial'
    if category not in trees:continue
    v,f=load(n);q,g=load(n,OUT)
    if not np.array_equal(f,g):continue
    distance=trees[category].query(v)[0]
    width=25. if category=='venous' else 4.
    weight=smooth(distance/width)
    target=v+(q-v)*weight[:,None]
    correction=np.linalg.norm(target-q,axis=1)
    if correction.max()<1e-7:continue
    write(n,target,g);row['maxShiftMm']=float(np.linalg.norm(target-v,axis=1).max())
    updates.append(dict(node=n,maxCollectorCorrectionMm=float(correction.max()),maskWidthMm=width))
    print(updates[-1],flush=True)
(OUT/'collector-stem-fit.json').write_text(json.dumps(dict(status='candidate-only-awaiting-surface-validation',anchors={key:value for key,value in anchors.items()},updates=updates,method='Common smooth distance mask restores exact native receiver boundaries and progressively transports the remaining drainage stem.'),indent=2))
(OUT/'revision.json').write_text(json.dumps(revision,indent=2))
