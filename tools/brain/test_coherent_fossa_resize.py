"""Test one shared, ordered posterior fossa size map, with fixed skull/dura.

Recover exact source material facets and apply the same map to every brain
label. This is an authoring experiment, never a production publisher.
"""
import json
import numpy as np, trimesh
from fit_vessels import APP, read_glb, mesh_records, smoothstep
from reconcile_local_volume import VolumeMap
from refine_context_skin import save_replaced
from reconcile_brainstem import sha
W=APP/'.authoring/coherent-fossa22';W.mkdir(exist_ok=True)
v=np.load(APP/'.authoring/brainstem20-lower-final/volume-map.npz')
m=VolumeMap.__new__(VolumeMap);m.origin=v['origin'];m.shape=np.array(v['delta'].shape);m.mask=np.zeros(m.shape,bool)
x,y,z=np.meshgrid(*[np.arange(n)+o for n,o in zip(m.shape,m.origin)],indexing='ij')
w=smoothstep((z-10)/14)*(1-smoothstep((z-76)/15))
w*=1-smoothstep((abs(x-.65)-26)/18)
w*=1-smoothstep((y+44)/18)
proposal=.22*np.maximum(0,y+135)*w
# Retain existing registration where it already supplies more posterior space.
m.delta=np.maximum(v['delta'],proposal)
assert float(1-np.diff(m.delta,axis=1).max())>.45
doc,data=read_glb(APP/'.authoring/brainstem19-coordinated/brain-source-refined.glb')
records=mesh_records(doc,data)
old=VolumeMap.__new__(VolumeMap);old.origin=v['origin'];old.shape=m.shape;old.delta=v['delta']
base_doc,base_data=read_glb(APP/'public/anatomy/models/brain-context.glb')
replacements={};matched={};changes=[]
for k,r in records.items():
    if any(s in k for s in ['falx-cerebri','tentorium-cerebelli']):continue
    p,f=r['old'],r['faces'];a=old.apply(p);b=m.apply(p)
    amount=np.linalg.norm(a-b,axis=1).max()
    if amount<1e-5:continue
    before=trimesh.Trimesh(a,f,process=False);after=trimesh.Trimesh(b,f,process=False)
    replacements[k]=(b,f,after.vertex_normals);matched[k]=(a,f,before.vertex_normals)
    changes.append({'node':k,'additionalDisplacementMm':float(amount),'volumeChangeFraction':float(abs(after.volume)/abs(before.volume)-1) if before.is_watertight else None})
save_replaced(W/'brain-trial.glb',base_doc,base_data,replacements)
save_replaced(W/'brain-source.glb',base_doc,base_data,matched)
np.savez_compressed(W/'volume-map.npz',origin=m.origin,delta=m.delta,mask=m.mask)
report={'method':'common ordered AP size map on recovered material facets; fixed skull and dura','requestedAPReductionFraction':.22,'minimumAPJacobian':float(1-np.diff(m.delta,axis=1).max()),'brainSha256':sha(W/'brain-trial.glb'),'sourceSha256':sha(W/'brain-source.glb'),'baselineBrainSha256':sha(APP/'public/anatomy/models/brain-context.glb'),'changes':changes,'appliedToApp':False}
(W/'registration.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2),flush=True)
