import sys,json,hashlib
from pathlib import Path
from fit_vessels import *
from reconcile_brainstem import WORK
from verify_fitting import collisions
from verify_central_rebuild import self_contacts
old=trimesh.load(WORK/'brain-source-refined.glb',process=False);new=trimesh.load(WORK/'brain-trial.glb',process=False);bones=trimesh.load(APP/'.authoring/bones-baseline.glb',process=False)
veins=trimesh.load(WORK/'veins-baseline.glb',process=False)
changed=[k for k in new.geometry if not np.array_equal(new.geometry[k].vertices,old.geometry[k].vertices)]
out={'sha':hashlib.sha256((WORK/'brain-trial.glb').read_bytes()).hexdigest(),'sourceSha256':hashlib.sha256((WORK/'brain-source-refined.glb').read_bytes()).hexdigest(),'self':[],'bone':[],'tissue':[],'clival':[],'volume':[]}
refs=['ventricle','sulc','lat-fis','aqueduct']
for k in changed:
 a,b=old.geometry[k],new.geometry[k]
 if any(t in k for t in refs):continue
 print('Checking',k,flush=True)
 out['self'].append([k,self_contacts(a),self_contacts(b)])
 if a.is_watertight:out['volume'].append([k,float(abs(b.volume)/abs(a.volume)-1)])
 for bk,bm in bones.geometry.items():
  after=collisions(b,bm)
  if after:out['bone'].append([k,bk,collisions(a,bm),after])
 for kk,aa in old.geometry.items():
  if kk==k or (kk in changed and kk<k) or any(t in kk for t in refs):continue
  after=collisions(b,new.geometry[kk])
  if after:out['tissue'].append([k,kk,collisions(a,aa),after])
 print(out['self'][-1],flush=True)
stem=[k for k in old.geometry if any(t in k for t in ['pons.','midbrain.','medulla-oblongata','base-of-peduncle'])]
for k in ['vein.basilar_plexus','vein.inferior_petrosal.left','vein.inferior_petrosal.right']:
 out['clival'].append([k,*[sum(collisions(veins.geometry[k],s.geometry[kk]) for kk in stem) for s in [old,new]]])
(WORK/'brain-check.json').write_text(json.dumps(out,indent=2))
print(json.dumps(out,indent=2),flush=True)
