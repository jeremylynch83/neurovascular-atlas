"""Smooth local fitting to lower optic canals, preserving arterial junctions."""
from pathlib import Path
import sys,json,numpy as np,hashlib
from scipy.interpolate import CubicSpline,PchipInterpolator
from scipy.spatial import cKDTree
from scipy.spatial.transform import Rotation
A=Path(__file__).resolve().parents[2];sys.path.insert(0,str(A/'tools/foramina'));from geometry import Glb,normals
B=A.parent/'inr-anatomy-atlas-v0.9.146';flow0=json.load(open(B/'public/anatomy/dsa-flow.json'));S=json.load(open(A/'anatomy/source/foramina/revision147-optic.json'));manifest0=json.load(open(B/'anatomy/generated/complete_manifest.json'));parents={r['id']:r.get('parent')for r in manifest0['structures']}
def descendant(sid,root):
 seen=set()
 while sid and sid not in seen:
  if sid==root:return True
  seen.add(sid);sid=parents.get(sid)
 return False
def smooth(w):
 w=np.clip(w,0,1);return w*w*(3-2*w)
def arc_fraction(p,cl):
 ss=np.r_[0,np.linalg.norm(np.diff(cl,axis=0),axis=1).cumsum()];dd,near=cKDTree(cl).query(p,k=2);best=np.full(len(p),np.inf);param=np.zeros(len(p))
 for k in range(2):
  for offset in [-1,0]:
   ids=np.clip(near[:,k]+offset,0,len(cl)-2);a=cl[ids];d=cl[ids+1]-a;w=np.clip(((p-a)*d).sum(1)/(d*d).sum(1),0,1);dd=((p-a-w[:,None]*d)**2).sum(1);sel=dd<best;best[sel]=dd[sel];param[sel]=(ss[ids]+w*(ss[ids+1]-ss[ids]))[sel]
 return param/ss[-1]
class Course:
 def __init__(self,side):
  pp=np.array(flow0['entries']['artery.anterior.ophthalmic_'+side]['points']);order=np.argsort(pp[:,1]);yy=pp[order,1];keep=np.r_[True,np.diff(yy)>1e-5];pp=pp[order][keep];yy=pp[:,1];self.fx=PchipInterpolator(yy,pp[:,0],extrapolate=True);self.fz=PchipInterpolator(yy,pp[:,2],extrapolate=True);self.root=np.array(flow0['entries']['artery.anterior.ophthalmic_'+side]['points'][0]);fitpath=A/'anatomy/source/foramina/revision147-optic-artery-controls.json';fit=json.load(open(fitpath))[side]if fitpath.exists()else {'posteriorMm':3.5,'uMm':0,'vMm':0};self.posterior=fit['posteriorMm'];q=S[side];mid,axis,u,v=[np.array(q[k])for k in ['mid','axis','u','v']];off=(fit['uMm']if side=='right'else -fit['uMm'])*u+fit['vMm']*v
  def canal(y):return mid+off+axis*((y-mid[1]-off[1])/axis[1])
  knots=np.array([-50,-40,-35,-33,-32.4,-31.9,-31,-30,-29,-27,-25,-23,-21,-18,-15,-13,30.]);dy=np.array([0,0,-self.posterior,-self.posterior,-self.posterior,-self.posterior,-self.posterior,-self.posterior-.3,-self.posterior-.3,-1.5,-.5,0,0,0,0,0,0.]);delta=[]
  for y,shift in zip(knots,dy):
   old=np.array([self.fx(y),y,self.fz(y)]);newy=y+shift
   if y<=-31.9 or y>=-13:target=old+np.array([0,shift,0])
   elif y==-31:target=np.array([old[0],newy,73.0])
   elif y==-30:target=canal(newy);target[2]+=.5
   elif y==-18:target=np.array([19.4 if side=='right'else -18.1,newy,67.7])
   elif y==-15:target=np.array([20.1 if side=='right'else -18.8,newy,68.0])
   else:target=canal(newy)
   delta.append(target-old)
  self.delta=PchipInterpolator(knots,np.array(delta),axis=0)
 def transport(self,p,branch=False):
  p=np.asarray(p,float);y=p[:,1];r=np.hypot(p[:,0]-self.fx(y),p[:,2]-self.fz(y));w=smooth((16-r)/14);return p+w[:,None]*self.delta(y)
 def root_warp(self,p):
  r=np.linalg.norm(p-self.root,axis=1);w=smooth((8-r)/6);return np.c_[np.zeros(len(p)),-self.posterior*w,np.zeros(len(p))]
courses={s:Course(s)for s in ['left','right']}
def warp(p,sid):
 q=np.asarray(p,float).copy();matched=False
 for side,c in courses.items():
  root='artery.anterior.ophthalmic_'+side
  if descendant(sid,root):q=c.transport(q,branch=sid!=root);matched=True
 if not matched:
  for c in courses.values():q+=c.root_warp(np.asarray(p,float))
 cfg=A/'anatomy/source/foramina/revision147-sof-controls.json'
 if cfg.exists():
  for c in json.load(open(cfg)):
   r=np.linalg.norm(q-np.array(c['centre']),axis=1);q+=smooth((c['outer']-r)/(c['outer']-c['core']))[:,None]*np.array(c['delta'])
 if 'artery.amendment.deep_recurrent_ophthalmic.' in sid:
  cfg=A/'anatomy/source/foramina/revision147-deep-controls.json'
  if cfg.exists():
   side=sid.rsplit('.',1)[-1];control=next(x for x in json.load(open(cfg))if x['side']==side);w=smooth((np.abs(q[:,0])-18.15)/1.15)*smooth((q[:,1]+32)/1.5)*(1-smooth((q[:,1]+22.5)/1.5));q[:,2]+=control['liftMm']*w
 return q
if __name__=='__main__':
 manifest=json.loads(json.dumps(manifest0));rows={(r.get('asset',{}).get('file'),r.get('asset',{}).get('node')):r for r in manifest['structures']};surface=json.load(open(B/'public/anatomy/dsa-surfaces.json'));rec=[];ids=[]
 for file in ['models/complete-circulation.glb','models/complete-anastomoses.glb']:
  g=Glb(B/'public/anatomy'/file);g.path=A/'public/anatomy'/file
  for name in g.nodes:
   row=rows[(file,name)];sid=row['id'];p,f,n=g.mesh(name);q=warp(p,sid);move=np.linalg.norm(q-p,axis=1)
   if move.max()<1e-6:continue
   eps=1e-4;J=np.stack([(warp(p+np.eye(3)[k]*eps,sid)-warp(p-np.eye(3)[k]*eps,sid))/(2*eps)for k in range(3)],axis=2);det=np.linalg.det(J);assert det.min()>.05,(name,float(det.min()));n=np.linalg.solve(np.swapaxes(J,1,2),n[...,None])[...,0];n/=np.maximum(np.linalg.norm(n,axis=1)[:,None],1e-20);g.replace(name,q,f,n);rec.append({'id':sid,'node':name,'file':file,'maximumDisplacementMm':float(move.max())})
   if row.get('vesselCourse'):
    row['vesselCourse']['reviewStatus']='requires-anatomical-target'if row['vesselCourse'].get('missingTargets')else 'requires-anatomical-review';row['vesselCourse']['radiusPolicy']='preserve-source-profile-with-measured-wall-deformation';singular=np.linalg.svd(J,compute_uv=False);row['vesselCourse'].setdefault('fitting',{})['calibreCheck']={'method':'Conservative deformation-Jacobian singular-value bounds, including axial stretch; not a direct lumen radius measurement.','ratioP05MedianP95':np.percentile(singular.ravel(),[5,50,95]).tolist(),'p95AbsoluteFractionalRadiusChange':float(np.percentile(abs(singular-1),95))};row['vesselCourse']['fitting']['revision147']={'method':'Smooth monotonic orbital fitting; short ICA attachment shifted posteriorly by 3 mm with shared local support. Branch ports carried with parent. Teaching reconstruction.'}
   if sid in surface['entries']and surface['entries'][sid].get('extra'):surface['entries'][sid]['extra']=warp(surface['entries'][sid]['extra'],sid).tolist()
   if sid in flow0['entries']and len(flow0['entries'][sid].get('points',[]))>=2:
    ids.append(sid);row['flowCourseGuide']={'geometrySha256':hashlib.sha256(np.asarray(q,'<f4').tobytes()+np.asarray(f,'<u4').tobytes()).hexdigest(),'points':warp(flow0['entries'][sid]['points'],sid).tolist()}
  g.save()
 (A/'anatomy/generated/complete_manifest.json').write_text(json.dumps(manifest,indent=2)+'\n');(A/'public/anatomy/dsa-surfaces.json').write_text(json.dumps(surface));(A/'anatomy/source/foramina/revision147-arteries.json').write_text(json.dumps(rec,indent=2)+'\n');(A/'anatomy/source/foramina/revision147-flow-changes.json').write_text(json.dumps(ids,indent=2)+'\n');print('Changed nodes',len(rec),'courses',len(ids),flush=True)
