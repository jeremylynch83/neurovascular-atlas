"""Small local dural reconciliation at the posterior falcotentorial attachment.

The overall skull registration remains exact. Reconcile anterior brainstem
clearance locally and the posterior medial dura to reconcile the atlas seam with the retained skull and
bone-apposed torcular region. Refresh every asset-bound guide afterwards.
"""
import json,hashlib,argparse
import numpy as np
from fit_vessels import APP,PUB,read_glb,write_glb,mesh_records,smoothstep

def adjust(p):
 w=smoothstep((-p[:,1]-125)/16)*(1-smoothstep((-p[:,1]-139)/9))*(1-smoothstep((np.abs(p[:,0]-.65)-6)/18))*(1-smoothstep((p[:,2]-88)/28))
 q=p.copy();q[:,1]-=5*w;q[:,2]+=6*w;return q

def adjust_stem(p):
 w=smoothstep((p[:,2]-22)/8)*(1-smoothstep((p[:,2]-66)/14))*(1-smoothstep((np.abs(p[:,0]-.65)-14)/12))
 q=p.copy();q[:,1]-=6*w;return q

def main():
 parser=argparse.ArgumentParser();parser.add_argument('--include-dural-experiment',action='store_true');parser.add_argument('--include-brainstem-experiment',action='store_true');args=parser.parse_args()
 if not args.include_dural_experiment and not args.include_brainstem_experiment:
  print('Context trials are rejected; no changes applied. Use an explicit experiment flag in a disposable authoring copy.');return
 manifest=json.loads((APP/'.authoring/manifest-baseline.json').read_text())
 doc,data=read_glb(APP/'.authoring/brain-baseline.glb');rec=mesh_records(doc,data);changes=[]
 keys=['brain.falx-cerebri','brain.tentorium-cerebelli.left','brain.tentorium-cerebelli.right']+[f'brain.{k}.{side}' for k in ['medulla-oblongata','pons','midbrain','base-of-peduncle'] for side in ['left','right']]+['brain.fourth-ventricle','brain.superior-cerebellar-peduncle.left','brain.superior-cerebellar-peduncle.right']
 if not args.include_brainstem_experiment:keys=keys[:3]
 for key in keys:
  r=rec[key];old=r['old'];p=adjust(old) if key in keys[:3] else adjust_stem(old);r['positions'][:]=p;f=r['faces']
  fn=np.cross(p[f[:,1]]-p[f[:,0]],p[f[:,2]]-p[f[:,0]])
  normals=np.zeros_like(p)
  for k in range(3):np.add.at(normals,f[:,k],fn)
  normals/=np.maximum(np.linalg.norm(normals,axis=1)[:,None],1e-12)
  from fit_vessels import accessor
  accessor(doc,data,r['primitive']['attributes']['NORMAL'])[:]=normals
  doc['accessors'][r['primitive']['attributes']['POSITION']].update(min=p.min(0).tolist(),max=p.max(0).tolist())
  changes.append({'id':key,'maximumDisplacementMm':float(np.linalg.norm(p-old,axis=1).max()),'movedVertices':int((np.linalg.norm(p-old,axis=1)>1e-6).sum()),'volumeInterpretation':'Local coordinate deformation; tissue volume and clearance are checked separately.'})
 write_glb(PUB/'models/brain-context.glb',doc,data);sha=hashlib.sha256((PUB/'models/brain-context.glb').read_bytes()).hexdigest()
 manifest['brainRegistration']['registeredAssetSha256']=sha
 manifest['brainRegistration']['localAdjustmentId']='dural-and-brainstem-trial-v0.9.17' if args.include_brainstem_experiment else 'posterior-falcotentorial-v0.9.17'
 manifest['brainRegistration']['localAdjustments']=changes
 rows={s['id']:s for s in manifest['structures']}
 for s in rows.values():
  if s.get('anatomy') and s['id'] in rec:
   p=rec[s['id']]['positions'];s['anatomy']['bounds']=[p.min(0).tolist(),p.max(0).tolist()];s['anatomy']['centroid']=p.mean(0).tolist()
  anchors=([s['surfaceAnchor']] if s.get('surfaceAnchor') else [])+s.get('secondarySurfaceAnchors',[])
  for anchor in anchors:
   r=rec[anchor['structureId']];tri=r['faces'][anchor['triangleIndex']]
   anchor['position']=(np.array(anchor['barycentric'])@r['positions'][tri]).tolist();anchor['assetSha256']=sha
  if s.get('surfaceAnchor') and s.get('landmark'):s['landmark']['point']=s['surfaceAnchor']['position']
  if s.get('vesselCourse'):s['vesselCourse']['brainAssetSha256']=sha
 for s in rows.values():
  if s.get('vesselGuide',{}).get('anchorIds'):
   points=[rows[k]['surfaceAnchor']['position'] for k in s['vesselGuide']['anchorIds']]
   s['landmark']['point']=points[0];s['landmark']['course']=points
 for s in rows.values():
  if s.get('targetValidation') and s.get('vesselGuide',{}).get('anchorIds'):
   stations=[rows[k] for k in s['vesselGuide']['anchorIds']]
   if all(x.get('secondarySurfaceAnchors') for x in stations):
    distances=np.array([[np.linalg.norm(np.array(x['surfaceAnchor']['position'])-a['position']) for a in x['secondarySurfaceAnchors']] for x in stations])
    s['targetValidation']['rightTentoriumDistanceMm']=distances[:,0].tolist();s['targetValidation']['falxDistanceMm']=distances[:,1].tolist()
 manifest['brainAdjustmentReport']='docs/validation/dural-adjustment-v0.9.17.json'
 (APP/'anatomy/generated/complete_manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
 export=json.loads((PUB/'vessel-courses.json').read_text());export['brainRegistration']=manifest['brainRegistration'];export['courses']=[s['vesselCourse'] for s in rows.values() if s.get('vesselCourse')];(PUB/'vessel-courses.json').write_text(json.dumps(export,indent=2)+'\n')
 manifest['brainAdjustmentPolicy']['appliedAdjustments']=changes
 (APP/'anatomy/generated/complete_manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
 landmarks=json.loads((PUB/'brain-landmarks.json').read_text())
 for key in ['brainRegistration','registration']:
  if key in landmarks:landmarks[key]=manifest['brainRegistration']
 # This JSON export is a catalogue subset, as generated by build_targets.py.
 landmarks['anchors']=[s for s in rows.values() if s.get('landmark') and s['system']=='brain']
 landmarks['surfaces']=[{'id':s['id'],'name':s['name'],'asset':s['asset'],'anatomy':s['anatomy']} for s in rows.values() if s.get('anatomy') and s.get('asset')]
 (PUB/'brain-landmarks.json').write_text(json.dumps(landmarks,indent=2)+'\n')
 (APP/'docs/validation/dural-adjustment-v0.9.17.json').write_text(json.dumps({'release':'0.9.17','changes':changes,'unchangedBrainSurfaces':188-len(keys),'parenchymalSurfacesRetainedExactly':not args.include_brainstem_experiment,'overallSkullRegistrationMatrixRetained':True,'maximumRequestedDisplacementMm':float(np.hypot(5,6)),'purpose':'Rejected brainstem context trial.' if args.include_brainstem_experiment else 'Reconcile the posterior medial dural seam with the unchanged bony torcular region; all parenchymal surfaces remain exact.'},indent=2)+'\n')
 print(json.dumps(changes))
if __name__=='__main__':main()
