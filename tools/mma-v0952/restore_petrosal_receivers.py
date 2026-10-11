"""Restore native superior-petrosal receiver geometry with a common donor mask.

The experimental cortical field moved a skull-base collector and introduced
seven new face-pair intersections. Keep both native receivers fixed and fade
all connected venous displacement over the same source-coordinate mask.
This is candidate-only and requires full subsequent surface validation.
"""
from common import *
rev=json.loads((OUT/'revision.json').read_text())
receivers=['vein.superior_petrosal_vein.left','vein.superior_petrosal_vein.right']
anchors=np.concatenate([load(n)[0] for n in receivers]);tree=cKDTree(anchors)
rows=[]
for row in rev['changed']:
    n=row['node']
    if n not in FILES or row['file']!='venous.glb':continue
    v,f=load(n);q,g=load(n,OUT)
    if q.shape!=v.shape or not np.array_equal(f,g):
        raise RuntimeError('Native receiver repair requires unchanged topology: '+n)
    weight=smooth(tree.query(v)[0]/18.)
    if n in receivers:weight[:]=0
    target=v+(q-v)*weight[:,None]
    change=np.linalg.norm(target-q,axis=1)
    if change.max()<1e-7:continue
    write(n,target,f)
    row['maxShiftMm']=float(np.linalg.norm(target-v,axis=1).max())
    row['receiverRepair']='common-source-coordinate-petrosal-mask'
    rows.append(dict(node=n,maxCorrectionMm=float(change.max()),maxRemainingDisplacementMm=row['maxShiftMm']))
    print(rows[-1],flush=True)
rev['release']='0.9.54'
(OUT/'revision.json').write_text(json.dumps(rev,indent=2))
(OUT/'petrosal-receiver-repair.json').write_text(json.dumps(dict(receivers=receivers,transitionWidthMm=18,updates=rows,requiresFullSurfaceValidation=True),indent=2))

