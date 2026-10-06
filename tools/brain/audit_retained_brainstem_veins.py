"""Check retained venous walls against changed brain context before publishing."""
import json,numpy as np,trimesh
from fit_vessels import APP
from reconcile_local_volume import WORK
from fit_brainstem_volume import SELECTED
from verify_fitting import collisions
from reconcile_brainstem import sha

before=trimesh.load(WORK/'brain-source-refined.glb',process=False)
after=trimesh.load(WORK/'brain-trial.glb',process=False)
veins=trimesh.load(WORK/'veins-baseline.glb',process=False)
changed=[k for k,m in after.geometry.items() if not np.array_equal(m.vertices,before.geometry[k].vertices)]
report={'brainCandidateSha256':sha(WORK/'brain-trial.glb'),'brainSourceSha256':sha(WORK/'brain-source-refined.glb'),'contacts':[],'failures':[]}
for k,v in veins.geometry.items():
 if k in SELECTED:continue
 for key in changed:
  if any(t in key for t in ['ventricle','sulc','lat-fis','aqueduct']):continue
  n=collisions(v,after.geometry[key]);o=collisions(v,before.geometry[key])
  if o or n:report['contacts'].append([k,key,o,n])
  if n>o:report['failures'].append([k,key,o,n])
 print('Retained vein',k,flush=True)
report['passed']=not report['failures'];(WORK/'retained-vein-context.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report['failures'],indent=2),flush=True)
