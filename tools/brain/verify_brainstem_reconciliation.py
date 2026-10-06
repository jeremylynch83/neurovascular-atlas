"""Report complete trial relationships. A failed trial cannot become a release.

The source and candidate have matching refined material triangles. Contact
counts therefore compare the same tessellation before and after displacement.
Open atlas cuts and existing contacts are reported without blanket exemptions.
"""
import argparse,json,hashlib
import numpy as np,trimesh
from fit_vessels import APP
from reconcile_brainstem import WORK,sha
from verify_fitting import collisions
from verify_central_rebuild import self_contacts,outside_join_contacts

def verify():
 context=json.loads((WORK/'brain-check.json').read_text())
 assert context['sha']==sha(WORK/'brain-trial.glb'),'Stale brain check'
 assert context['sourceSha256']==sha(WORK/'brain-source-refined.glb'),'Stale source brain check'
 source=trimesh.load(WORK/'veins-source-refined.glb',process=False);candidate=trimesh.load(WORK/'veins-trial.glb',process=False)
 brains=[trimesh.load(WORK/f'brain-{s}.glb',process=False) for s in ['source-refined','trial']]
 bones=trimesh.load(APP/'.authoring/bones-baseline.glb',process=False)
 changed=[k for k in candidate.geometry if not np.array_equal(source.geometry[k].vertices,candidate.geometry[k].vertices)]
 rows=[];joins=[]
 for k in changed:
  before,after=source.geometry[k],candidate.geometry[k];assert np.array_equal(before.faces,after.faces)
  row={'node':k,'selfContacts':[self_contacts(before),self_contacts(after)],'tissue':[],'bone':[]}
  for label,target in brains[1].geometry.items():
   if any(t in label for t in ['ventricle','sulc','lat-fis','aqueduct']):continue
   a=collisions(after,target);b=collisions(before,brains[0].geometry[label])
   if a or b:row['tissue'].append([label,b,a])
  for label,target in bones.geometry.items():
   a=collisions(after,target);b=collisions(before,target)
   if a or b:row['bone'].append([label,b,a])
  for other in candidate.geometry:
   if other==k or (other in changed and other<k):continue
   b=outside_join_contacts(before,source.geometry[other],before,source.geometry[other]);a=outside_join_contacts(after,candidate.geometry[other],before,source.geometry[other])
   if a or b:joins.append([k,other,b,a])
  rows.append(row);print('Verified',k,flush=True)
 failures=[]
 for category in ['self','bone','tissue']:
  for r in context[category]:
   if r[-1]>r[-2]:failures.append({'domain':'brain','check':category,'detail':r})
 for r in rows:
  if r['selfContacts'][1]>r['selfContacts'][0]:failures.append({'domain':'veins','check':'self','detail':[r['node'],*r['selfContacts']]})
  for category in ['tissue','bone']:
   for pair in r[category]:
    if pair[-1]>pair[-2]:failures.append({'domain':'veins','check':category,'detail':[r['node'],*pair]})
 for pair in joins:
  if pair[-1]>pair[-2]:failures.append({'domain':'veins','check':'outside-source-join','detail':pair})
 result={'baselineRelease':'0.9.18','status':'rejected-trial','appliedToApp':False,'passed':False,'brainCandidateSha256':sha(WORK/'brain-trial.glb'),'veinCandidateSha256':sha(WORK/'veins-trial.glb'),'brainSourceSha256':sha(WORK/'brain-source-refined.glb'),'veinSourceSha256':sha(WORK/'veins-source-refined.glb'),'brainChecks':context,'veinChecks':rows,'venousJoinChecks':joins,'failures':failures,'limitations':['Triangle contacts do not establish containment in open atlas surfaces.','Refinement preserves the source facet surfaces; edited triangle and vertex counts change.','A reduction in one contact count cannot compensate for a new crossing elsewhere.','The posterior arterial transport is exploratory and has not passed complete acceptance. It is excluded from the accepted app and this candidate comparison.','No corrected asset bindings or landmarks are published for the rejected candidate.']}
 result['passed']=not failures
 if result['passed']:result['status']='geometry-checks-passed-additional-arterial-and-anchor-validation-required'
 (WORK/'acceptance.json').write_text(json.dumps(result,indent=2)+'\n')
 print(json.dumps({'passed':result['passed'],'failures':len(failures),'clivalContacts':context['clival']},indent=2),flush=True)
 return result
if __name__=='__main__':
 result=verify()
 raise SystemExit(0 if result['passed'] else 1)
