"""Regression checks for the local context and skull-constrained fitting batch."""
import json,hashlib
import numpy as np,trimesh
from fit_vessels import APP,PUB,read_glb,mesh_records,accessor
from fit_dura import adjust,adjust_stem
from verify_fitting import collisions

def main():
 old=trimesh.load(APP/'.authoring/brain-baseline.glb',process=False);new=trimesh.load(PUB/'models/brain-context.glb',process=False)
 changes=[];unchanged=[]
 for key,m in old.geometry.items():
  n=new.geometry[key];assert np.array_equal(m.faces,n.faces)
  delta=np.linalg.norm(m.vertices-n.vertices,axis=1)
  if delta.max()<1e-6:unchanged.append(key);continue
  fun=adjust if any(t in key for t in ['falx','tentorium']) else adjust_stem
  p=m.vertices[::max(1,len(m.vertices)//1000)];eps=1e-3
  j=np.stack([(fun(p+np.eye(3)[i]*eps)-fun(p-np.eye(3)[i]*eps))/(2*eps) for i in range(3)],axis=2)
  det=float(np.linalg.det(j).min());assert det>.15
  volume=float((abs(n.volume)/abs(m.volume)-1)*100) if m.is_watertight else None
  if 'medulla' in key:assert abs(volume)<1
  changes.append({'id':key,'maximumDisplacementMm':float(delta.max()),'minimumSampledJacobianDeterminant':det,'closedSurface':m.is_watertight,'enclosedMeshVolumeChangePercent':volume,'volumeInterpretation':'Thin tentorial shell volume is not brain tissue volume.' if 'tentorium' in key else 'Enclosed volume is reported only for watertight meshes.'})
 # All raw accessor buffers of protected labels, including normals, remain exact.
 protected=[]
 for kind in ['veins','arteries']:
  od,ob=read_glb(APP/f'.authoring/{kind}-baseline.glb');nd,nb=read_glb(APP/f'.authoring/{kind}-fitted.glb');a=mesh_records(od,ob);b=mesh_records(nd,nb)
  keys=[k for k in a if 'cavernous' in k or 'intercavernous' in k or (kind=='arteries' and (k.startswith('ICA ') or (k.endswith('right') and any(v in k for v in ['Central','MCA superior division']))))]
  for key in keys:
   for attribute in ['POSITION','NORMAL']:
    assert np.array_equal(accessor(od,ob,a[key]['primitive']['attributes'][attribute]),accessor(nd,nb,b[key]['primitive']['attributes'][attribute])),key
   assert np.array_equal(a[key]['faces'],b[key]['faces']);protected.append(key)
  if kind=='veins':
   blocked=['vein.anterior_medullary','vein.anterior_pontine','vein.anterior_pontomesencephalic']+[f'vein.{k}.{side}' for k in ['lateral_mesencephalic','transverse_pontine','pontomedullary'] for side in ['left','right']]
   for key in blocked:
    for attribute in ['POSITION','NORMAL']:
     assert np.array_equal(accessor(od,ob,a[key]['primitive']['attributes'][attribute]),accessor(nd,nb,b[key]['primitive']['attributes'][attribute])),key
    protected.append(key)
 bones=trimesh.load(APP/'.authoring/bones-baseline.glb',process=False);bone=trimesh.util.concatenate(list(bones.geometry.values()))
 vascular={k:[trimesh.load(APP/f'.authoring/{k}-{state}.glb',process=False) for state in ['baseline','fitted']] for k in ['veins','arteries']}
 keys=['vein.straight','vein.galen','vein.inferior_sagittal','vein.confluence','vein.transverse.left','vein.transverse.right','vein.anterior_medullary','vein.anterior_pontine','vein.anterior_pontomesencephalic']+[f'vein.{k}.{s}' for k in ['lateral_mesencephalic','transverse_pontine','pontomedullary'] for s in ['left','right']]
 checks=[]
 edited_arteries=[key for key,m in vascular['arteries'][0].geometry.items() if not np.array_equal(m.vertices,vascular['arteries'][1].geometry[key].vertices)]
 for key in keys+edited_arteries:
  scenes=vascular['veins' if key.startswith('vein.') else 'arteries'];counts=[collisions(scene.geometry[key],bone) for scene in scenes]
  checks.append({'id':key,'beforeTriangleContactsWithSkull':counts[0],'afterTriangleContactsWithSkull':counts[1],'noIncreasedContacts':counts[1]<=counts[0]})
 brainbone=[]
 for c in changes:
  key=c['id'];counts=[collisions(scene.geometry[key],bone) for scene in [old,new]];brainbone.append({'id':key,'beforeTriangleContacts':counts[0],'afterTriangleContacts':counts[1]})
 report={'release':'0.9.17','authoringGeometryHashes':{k:hashlib.sha256((APP/f'.authoring/{k}-fitted.glb').read_bytes()).hexdigest() for k in ['veins','arteries']},'brainAssetSha256':hashlib.sha256((PUB/'models/brain-context.glb').read_bytes()).hexdigest(),'unchangedBrainSurfaces':len(unchanged),'unchangedSurfaceIds':unchanged,'changes':changes,'protectedVascularAccessorBuffersExact':protected,'skullChecks':checks,'adjustedContextSkullChecks':brainbone,'notes':['Bone meshes remain unchanged. Baseline skull contacts are reported rather than concealed.','A sampled positive coordinate Jacobian does not prove absence of every vessel self-intersection.','Open brain surfaces do not provide valid solid-volume containment tests.']}
 (APP/'docs/validation/fitting-context-v0.9.17.json').write_text(json.dumps(report,indent=2)+'\n')
 assert all(r['noIncreasedContacts'] for r in checks),'Edited geometry introduced skull contacts'
 assert len(unchanged)==188,'Rejected context trial must not be applied'
 print(json.dumps({'skullChecks':checks,'contextChanges':changes,'adjustedContextSkullChecks':brainbone},indent=2))
if __name__=='__main__':main()
