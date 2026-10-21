"""Shared compact deformation lifts proximal orbital arterial segments clear of bone.
All nearby arterial nodes and connection meshes receive the same map. Surface
projection caps and geometry-bound injection guides are updated with that map.
"""
from pathlib import Path
import sys,json,numpy as np,hashlib
A=Path(__file__).resolve().parents[2];sys.path.insert(0,str(A/'tools/foramina'));from geometry import Glb
controls=json.load(open(A/'anatomy/source/foramina/revision146-arterial-controls.json'));centres=np.array([controls[k]['center']for k in ['left','right']]);deltas=np.array([controls[k]['delta']for k in ['left','right']])
def warp(p):
 p=np.asarray(p,float).copy()
 for c,delta in zip(centres,deltas):
  r=np.linalg.norm(p-c,axis=1);w=np.clip((7-r)/5.5,0,1);w=w*w*(3-2*w);p+=w[:,None]*delta
 return p
if __name__=='__main__':
 source=A/'anatomy/generated/complete_manifest.json';manifest=json.load(open(source));rows={(r.get('asset',{}).get('file'),r.get('asset',{}).get('node')):r for r in manifest['structures']};flow=json.load(open(A/'public/anatomy/dsa-flow.json'));surface=json.load(open(A/'public/anatomy/dsa-surfaces.json'));rec=[];ids=[]
 for file in ['models/complete-circulation.glb','models/complete-anastomoses.glb']:
  g=Glb(A/'public/anatomy'/file)
  for name in g.nodes:
   p,f,n=g.mesh(name);q=warp(p);move=np.linalg.norm(q-p,axis=1)
   if move.max()<1e-7:continue
   eps=1e-4;J=np.stack([(warp(p+np.eye(3)[k]*eps)-warp(p-np.eye(3)[k]*eps))/(2*eps)for k in range(3)],axis=2);assert np.linalg.det(J).min()>.2;n=np.linalg.solve(np.swapaxes(J,1,2),n[...,None])[...,0];n/=np.maximum(np.linalg.norm(n,axis=1)[:,None],1e-20);g.replace(name,q,f,n);row=rows[(file,name)];sid=row['id'];
   if row.get('vesselCourse'):
    c=row['vesselCourse'];singular=np.linalg.svd(J,compute_uv=False);c['radiusPolicy']='preserve-source-profile-with-measured-wall-deformation';c['reviewStatus']='requires-anatomical-review';c.setdefault('fitting',{})['calibreCheck']={'method':'Conservative local deformation-Jacobian singular-value bounds; includes axial stretch and is not a direct patient lumen measurement.','ratioP05MedianP95':np.percentile(singular.ravel(),[5,50,95]).tolist(),'p95AbsoluteFractionalRadiusChange':float(np.percentile(abs(singular-1),95))};
   rec.append({'id':sid,'node':name,'file':file,'maximumDisplacementMm':float(move.max())})
   if sid in surface['entries']:
    e=surface['entries'][sid]
    if e.get('extra'):e['extra']=warp(e['extra']).tolist()
   if sid in flow['entries']:
    ids.append(sid);old=flow['entries'][sid]
    if len(old.get('points',[]))>=2:
     row['flowCourseGuide']={'geometrySha256':hashlib.sha256(np.asarray(q,'<f4').tobytes()+np.asarray(f,'<u4').tobytes()).hexdigest(),'points':warp(old['points']).tolist()}
  g.save()
 source.write_text(json.dumps(manifest,indent=2)+'\n');(A/'public/anatomy/dsa-surfaces.json').write_text(json.dumps(surface));(A/'anatomy/source/foramina/revision146-flow-changes.json').write_text(json.dumps(ids,indent=2)+'\n');(A/'anatomy/source/foramina/revision146-arteries.json').write_text(json.dumps({'method':'Shared smooth local inferomedial fitting of short arterial segments into the corrected canal entrance. No connection topology or indices changed.','maximumControlDisplacementMm':float(np.linalg.norm(deltas,axis=1).max()),'centres':centres.tolist(),'changed':rec},indent=2)+'\n');print('Changed arterial nodes',len(rec),'flow courses',len(ids),flush=True)
