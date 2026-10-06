"""Complete hash-bound checks on transported arterial walls and junctions."""
import json,numpy as np,trimesh
from scipy.spatial import cKDTree
from fit_vessels import APP,read_glb,mesh_records,accessor
from reconcile_local_volume import VolumeMap
from reconcile_brainstem import sha
from verify_fitting import collisions
from verify_central_rebuild import outside_join_contacts
W=APP/'.authoring/brainstem20-lower-final';P=APP/'.authoring/brainstem19'
old=trimesh.load(W/'arteries-source-refined.glb',process=False);new=trimesh.load(W/'arteries-trial.glb',process=False);brains=[trimesh.load(W/'brain-source-refined.glb',process=False),trimesh.load(W/'brain-trial.glb',process=False)];bones=trimesh.load(APP/'.authoring/bones-baseline.glb',process=False)
v=np.load(W/'arterial-map.npz');m=VolumeMap.__new__(VolumeMap);m.origin=v['origin'];m.delta=v['delta'];m.mask=v['mask'];m.shape=np.array(m.delta.shape)
report={'arterySha256':sha(W/'arteries-trial.glb'),'brainSha256':sha(W/'brain-trial.glb'),'minimumYDerivative':float(1-np.diff(m.delta,axis=1).max()),'geometry':[],'brainContacts':[],'boneContacts':[],'arterialContacts':[],'failures':[]}
changed=[k for k in old.geometry if not np.array_equal(old.geometry[k].vertices,new.geometry[k].vertices)]
for k in changed:
 a,b=old.geometry[k],new.geometry[k];error=float(np.linalg.norm(m.apply(a.vertices)-b.vertices,axis=1).max());area0=a.area_faces;ratio=b.area_faces/np.maximum(area0,1e-30);minimum=float(ratio[area0>5e-5].min())
 report['geometry'].append({'node':k,'mapAgreementErrorMm':error,'minimumTriangleAreaRatio':minimum,'maximumDisplacementMm':float(np.linalg.norm(b.vertices-a.vertices,axis=1).max())})
 if error>2e-4 or minimum<.15:report['failures'].append([k,'wall-map-or-area',error,minimum])
 for label,bone in bones.geometry.items():
  n=collisions(b,bone);o=collisions(a,bone)
  if o or n:report['boneContacts'].append([k,label,o,n])
  if n>o:report['failures'].append([k,'bone',label,o,n])
 for label,target in brains[1].geometry.items():
  if any(t in label for t in ['ventricle','aqueduct','sulc','lat-fis']):continue
  n=collisions(b,target);o=collisions(a,brains[0].geometry[label])
  if o or n:report['brainContacts'].append([k,label,o,n])
  if n>o:report['failures'].append([k,'tissue',label,o,n])
 for other,target in new.geometry.items():
  if other==k or (other in changed and other<k):continue
  n=outside_join_contacts(b,target,a,old.geometry[other]);o=outside_join_contacts(a,old.geometry[other],a,old.geometry[other])
  if o or n:report['arterialContacts'].append([k,other,o,n])
  if n>o:report['failures'].append([k,'arterial',other,o,n])
 print('Verified artery',k,flush=True)
p=np.concatenate([r.vertices for r in old.geometry.values()]);q=np.concatenate([r.vertices for r in new.geometry.values()]);_,inv=np.unique(np.round(p,5),axis=0,return_inverse=True);order=np.argsort(inv);same=np.diff(inv[order])==0;gap=np.linalg.norm(np.diff(q[order],axis=0)[same],axis=1).max(initial=0);report['maximumSharedLabelBoundaryGapMm']=float(gap)
if gap>2e-4:report['failures'].append(['shared-junction',float(gap)])
report['protectedAnteriorLabelsRetained']=not any(k.startswith(('ICA ','MCA ','Central')) for k in changed);report['passed']=not report['failures'] and report['protectedAnteriorLabelsRetained'];(W/'arterial-validation.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({'passed':report['passed'],'failures':report['failures']},indent=2),flush=True)
