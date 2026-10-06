"""Verify the additional staged context against the delivered v0.9.19 context."""
import json
import numpy as np
import trimesh
from fit_vessels import APP,read_glb,mesh_records
from refit_connected_brainstem_skin import WORK
from refit_brainstem_sections import KEYS
from verify_fitting import collisions
from verify_central_rebuild import self_contacts
from reconcile_local_volume import VolumeMap
from reconcile_brainstem import sha

before=trimesh.load(WORK/'brain-matched-source.glb',process=False)
after=trimesh.load(WORK/'brain-trial.glb',process=False)
bones=trimesh.load(APP/'.authoring/bones-baseline.glb',process=False)
veins=trimesh.load(APP/'.authoring/brainstem19/veins-baseline.glb',process=False)
arteries=trimesh.load(APP/'.authoring/brainstem19/arteries-baseline.glb',process=False)
raw=trimesh.load(APP/'.authoring/brainstem19-coordinated/brain-source-refined.glb',process=False)
z=np.load(WORK/'volume-map.npz');mapping=VolumeMap.__new__(VolumeMap)
mapping.origin=z['origin'];mapping.delta=z['delta'];mapping.shape=np.array(mapping.delta.shape)
report={'brainSha256':sha(WORK/'brain-trial.glb'),'baselineSha256':sha(APP/'public/anatomy/models/brain-context.glb'),
        'geometry':[],'contacts':[],'failures':[],'appliedToApp':False}
changed=[]
for k,b in after.geometry.items():
 a=before.geometry[k]
 if np.array_equal(a.vertices,b.vertices) and np.array_equal(a.faces,b.faces):continue
 changed.append(k)
 ref=any(t in k for t in ['ventricle','aqueduct','sulc','lat-fis'])
 r=raw.geometry[k];error=0.
 for w in [[1,0,0],[0,1,0],[0,0,1],[1/3]*3,[.5,.5,0],[0,.5,.5],[.5,0,.5]]:
  p=(r.triangles*np.array(w)[None,:,None]).sum(1)
  q=(b.triangles*np.array(w)[None,:,None]).sum(1)
  error=max(error,float(np.linalg.norm(mapping.apply(p)-q,axis=1).max()))
 volume=abs(b.volume)/abs(a.volume)-1 if a.is_watertight else None
 row={'node':k,'mapInterpolationErrorMm':error,'volumeChangeFraction':volume}
 report['geometry'].append(row)
 if not ref and error>2e-4:report['failures'].append([k,'map-error',error])
 if not ref and volume is not None and abs(volume)>.15:report['failures'].append([k,'volume-change',volume])
 if ref:continue
 self_=[self_contacts(m) for m in [a,b]]
 row['selfContacts']=self_
 if self_[1]>self_[0]:report['failures'].append([k,'self',*self_])
 for domain,scene in [('bone',bones),('retained-vein',veins),('artery',arteries)]:
  for target,m in scene.geometry.items():
   if domain=='retained-vein' and target in KEYS:continue
   counts=[collisions(m,context) for context in [a,b]]
   if any(counts):report['contacts'].append([k,domain,target,*counts])
   if counts[1]>counts[0]:report['failures'].append([k,domain,target,*counts])
 print('Checked additional context',k,flush=True)
 (WORK/'corridor-acceptance-progress.json').write_text(json.dumps(report,indent=2)+'\n')
for k in changed:
 a,b=before.geometry[k],after.geometry[k]
 if any(t in k for t in ['ventricle','aqueduct','sulc','lat-fis']):continue
 for target in after.geometry:
  if target==k or (target in changed and target<k) or any(t in target for t in ['ventricle','aqueduct','sulc','lat-fis']):continue
  counts=[collisions(scene.geometry[k],scene.geometry[target]) for scene in [before,after]]
  if counts[1]>counts[0]:report['failures'].append([k,'tissue',target,*counts])
report['minimumYDerivative']=float(1-np.diff(mapping.delta,axis=1).max())
report['passed']=not report['failures']
(WORK/'corridor-acceptance.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({'passed':report['passed'],'failures':report['failures']},indent=2),flush=True)
raise SystemExit(0 if report['passed'] else 1)
