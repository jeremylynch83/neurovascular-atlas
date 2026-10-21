from pathlib import Path
import sys,json,numpy as np,hashlib
from scipy.spatial import cKDTree
from scipy.interpolate import RBFInterpolator
A=Path(__file__).resolve().parents[2];B=A.parent/'inr-anatomy-atlas-v0.9.155';sys.path.insert(0,str(A/'tools/foramina'));from geometry import Glb
m=json.load(open(A/'anatomy/generated/complete_manifest.json'));rows={r['id']:r for r in m['structures']};mb=json.load(open(B/'anatomy/generated/complete_manifest.json'));rb={r['id']:r for r in mb['structures']};surf=json.load(open(A/'public/anatomy/dsa-surfaces.json'));sb=json.load(open(B/'public/anatomy/dsa-surfaces.json'));flow=json.load(open(B/'public/anatomy/dsa-flow.json'));files=['models/complete-circulation.glb','models/complete-anastomoses.glb'];old={f:Glb(B/'public/anatomy'/f)for f in files};new={f:Glb(A/'public/anatomy'/f)for f in files};patch=[];original={};targets={}
for sid,r in rows.items():
 f=r.get('asset',{}).get('file')
 if f==files[0]:original[sid]=old[f].mesh(r['asset']['node'])[0];targets[sid]=new[f].mesh(r['asset']['node'])[0]
restored=['artery.amendment.mma_anterior_cavernous.'+side for side in ['left','right']]
for sid in restored:targets[sid]=original[sid].copy()
def field(controls,delta,outer=5):
 _,i=np.unique(np.round(controls,5),axis=0,return_index=True);controls=controls[i];delta=delta[i];tree=cKDTree(controls);fit=RBFInterpolator(controls,delta,kernel='linear',degree=0,smoothing=1e-12,neighbors=min(32,len(controls)))
 def move(p):
  p=np.asarray(p,float);d=tree.query(p)[0];t=np.clip((outer-d)/outer,0,1);w=t*t*(3-2*t);return p+w[:,None]*fit(p)
 return move
transforms={}
for side in ['left','right']:
 sid='artery.amendment.deep_recurrent_ophthalmic.'+side;parent='artery.anterior.ophthalmic_'+side;p=original[sid];d,ix=cKDTree(original[parent]).query(p);s=d<2e-5;assert s.any();move=field(p[s],targets[parent][ix[s]]-p[s]);transforms[sid]=move;targets[sid]=move(p);patch.append({'id':sid,'method':'Original155 branch course retained, with compact interpolation of the corrected parent cuff.','maximumMoveMm':float(np.linalg.norm(targets[sid]-p,axis=1).max())})
for sid in restored+[f'artery.amendment.deep_recurrent_ophthalmic.{s}'for s in ['left','right']]:
 r=rows[sid];f=r['asset']['file'];p,faces,n=old[f].mesh(r['asset']['node']);q=targets[sid];new[f].replace(r['asset']['node'],q,faces)
 surf['entries'][sid]=json.loads(json.dumps(sb['entries'][sid]))
 if sid in transforms:
  move=transforms[sid]
  if surf['entries'][sid].get('extra'):surf['entries'][sid]['extra']=move(surf['entries'][sid]['extra']).tolist()
  r['flowCourseGuide']={'points':move(flow['entries'][sid]['points']).tolist(),'geometrySha256':'pending'}
  r['vesselCourse']['fitting']['revision156']['branchScope']='Original155 course with a local cuff adjustment only.'
 else:
  if rb[sid].get('flowCourseGuide'):r['flowCourseGuide']=rb[sid]['flowCourseGuide']
  else:r.pop('flowCourseGuide',None)
  r['vesselCourse']=rb[sid]['vesselCourse'];patch.append({'id':sid,'method':'Original155 skull-base course restored without deformation.'})
# Connectors are independent meshes. Rebuild them from155 and move only cuffs
# that actually meet changed parent walls; preserve their other attachments.
pts=np.concatenate(list(original.values()));dst=np.concatenate([targets[sid]for sid in original]);tree=cKDTree(pts)
for sid,r in rows.items():
 if r.get('asset',{}).get('file')!=files[1]:continue
 p,faces,n=old[files[1]].mesh(r['asset']['node']);d,ix=tree.query(p);sel=d<2e-5
 if not sel.any():continue
 delta=dst[ix[sel]]-p[sel]
 if np.linalg.norm(delta,axis=1).max()<2e-5:move=lambda x:np.asarray(x,float)
 else:move=field(p[sel],delta,outer=5)
 q=move(p);new[files[1]].replace(r['asset']['node'],q,faces)
 if sid in sb['entries']:
  surf['entries'][sid]=json.loads(json.dumps(sb['entries'][sid]))
  if surf['entries'][sid].get('extra'):surf['entries'][sid]['extra']=move(surf['entries'][sid]['extra']).tolist()
 patch.append({'id':sid,'method':'Original155 connector with compact interpolation at coincident parent cuffs.'})
for f,g in new.items():
 h=g.save();surf['sourceHashes'][f]=h;surf['assetRevisions'][f]=h[:20]
 actual=Glb(A/'public/anatomy'/f)
 for sid,r in rows.items():
  if r.get('asset',{}).get('file')!=f:continue
  if r.get('vesselCourse'):r['vesselCourse']['geometrySha256']=h
  if r.get('flowCourseGuide'):
   p,faces,_=actual.mesh(r['asset']['node']);r['flowCourseGuide']['geometrySha256']=hashlib.sha256(np.asarray(p,'<f4').tobytes()+np.asarray(faces,'<u4').tobytes()).hexdigest()
(A/'anatomy/generated/complete_manifest.json').write_text(json.dumps(m,indent=2)+'\n');(A/'public/anatomy/dsa-surfaces.json').write_text(json.dumps(surf));v=json.load(open(A/'public/anatomy/vessel-courses.json'));v['courses']=[r['vesselCourse']for r in m['structures']if r.get('vesselCourse')];(A/'public/anatomy/vessel-courses.json').write_text(json.dumps(v,indent=2)+'\n');(A/'docs/revision156-final-attachments.json').write_text(json.dumps(patch,indent=2));print('Localised affected branch cuffs; restored ECA source courses',len(patch))
