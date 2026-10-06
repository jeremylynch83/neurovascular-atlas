"""Hash-bound context checks for the continued, volume-constrained trial."""
import argparse,json,numpy as np,trimesh
from fit_vessels import APP,read_glb,mesh_records
from reconcile_local_volume import VolumeMap
from reconcile_brainstem import sha
from verify_fitting import collisions
from fit_brainstem_shear import SELECTED

def main():
 p=argparse.ArgumentParser();p.add_argument('--work',default='brainstem20-optimised');args=p.parse_args();work=APP/'.authoring'/args.work
 z=np.load(work/'volume-map.npz');m=VolumeMap.__new__(VolumeMap);m.origin=z['origin'];m.delta=z['delta'];m.mask=z['mask'];m.shape=np.array(m.delta.shape)
 source=trimesh.load(work/'brain-source-refined.glb',process=False);target=trimesh.load(work/'brain-trial.glb',process=False);bones=trimesh.load(APP/'.authoring/bones-baseline.glb',process=False);veins=trimesh.load(APP/'.authoring/brainstem19/veins-baseline.glb',process=False)
 changed=[k for k in target.geometry if not np.array_equal(target.geometry[k].vertices,source.geometry[k].vertices)]
 report={'brainCandidateSha256':sha(work/'brain-trial.glb'),'brainSourceSha256':sha(work/'brain-source-refined.glb'),'minimumYDerivative':float(1-np.diff(m.delta,axis=1).max()),'geometry':[],'brainBone':[],'retainedVeins':[],'clivalContacts':[],'failures':[]}
 for k in changed:
  a,b=source.geometry[k],target.geometry[k];assert np.array_equal(a.faces,b.faces)
  error=float(np.linalg.norm(m.apply(a.vertices)-b.vertices,axis=1).max());ref=any(t in k for t in ['sulc','ventricle','aqueduct','lat-fis'])
  for weights in [[1/3,1/3,1/3],[.5,.5,0],[0,.5,.5],[.5,0,.5]]:
   p=(a.triangles*np.array(weights)[None,:,None]).sum(1);q=(b.triangles*np.array(weights)[None,:,None]).sum(1);error=max(error,float(np.linalg.norm(m.apply(p)-q,axis=1).max()))
  vol=float(abs(b.volume)/abs(a.volume)-1) if a.is_watertight else None
  ratio=b.area_faces/np.maximum(a.area_faces,1e-30);robust=a.area_faces>5e-5;min_area=float(ratio[robust].min())
  report['geometry'].append({'node':k,'mapAgreementErrorMm':error,'volumeChangeFraction':vol,'minimumTriangleAreaRatio':min_area,'maximumDisplacementMm':float(np.linalg.norm(b.vertices-a.vertices,axis=1).max())})
  if not ref and error>2e-4:report['failures'].append([k,'map-interpolation-error',error])
  if vol is not None and not ref and abs(vol)>(.15001 if (args.work.startswith('brainstem20-lower') or args.work=='brainstem20-space') else .01001):report['failures'].append([k,'volume-change',vol])
  if not ref and min_area<.12:report['failures'].append([k,'local-shape-distortion',min_area])
  if ref:continue
  for label,bone in bones.geometry.items():
   n=collisions(b,bone)
   if n:
    o=collisions(a,bone);report['brainBone'].append([k,label,o,n])
    if n>o:report['failures'].append([k,'bone',label,o,n])
  for label,v in veins.geometry.items():
   if label in SELECTED or 'lateral_mesencephalic' in label:continue
   n=collisions(v,b);o=collisions(v,a)
   if o or n:report['retainedVeins'].append([label,k,o,n])
   if n>o:report['failures'].append([k,'retained-vein',label,o,n])
  print('Checked',k,error,vol,min_area,flush=True)
 stem=[k for k in target.geometry if any(t in k for t in ['pons.','midbrain.','medulla-oblongata','base-of-peduncle'])]
 for label in ['vein.basilar_plexus','vein.inferior_petrosal.left','vein.inferior_petrosal.right']:
  report['clivalContacts'].append([label,*[sum(collisions(veins.geometry[label],s.geometry[k]) for k in stem) for s in [source,target]]])
 report['passed']=not report['failures'];(work/'context-validation.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({'passed':report['passed'],'failures':report['failures'],'clival':report['clivalContacts']},indent=2),flush=True)
if __name__=='__main__':main()
