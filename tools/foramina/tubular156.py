"""Calibre-preserving transport for the ICA/ophthalmic region.
Preview generator. apply156.py writes the initial source repair; the local attachment pass retains the reviewed skull-base branches.
"""
from pathlib import Path
import sys,json,hashlib,numpy as np
from scipy.interpolate import splprep,splev,CubicSpline
from scipy.spatial import cKDTree
A=Path(__file__).resolve().parents[2];B=A.parent/'inr-anatomy-atlas-v0.9.146';sys.path.insert(0,str(A/'tools/foramina'))
from geometry import Glb,normals
import arteries146 as v146
import arteries147 as v147
M=json.load(open(A/'anatomy/generated/complete_manifest.json'));rows={s['id']:s for s in M['structures']};flow=json.load(open(B/'public/anatomy/dsa-flow.json'))
def smooth(x):
 x=np.clip(x,0,1);return x*x*(3-2*x)
def inverse146(q):
 p=np.asarray(q,float).copy()
 for _ in range(80):
  e=q-v146.warp(p)
  if abs(e).max(initial=0)<2e-7:break
  p+=e*.75
 assert abs(q-v146.warp(p)).max(initial=0)<2e-5
 return p
class Curve:
 def __init__(self,points,smoothing=.12):
  p=np.asarray(points,float);p=p[np.r_[True,np.linalg.norm(np.diff(p,axis=0),axis=1)>1e-4]]
  u=np.r_[0,np.linalg.norm(np.diff(p,axis=0),axis=1).cumsum()]
  tck,_=splprep(p.T,u=u,s=smoothing,k=3)
  self.u=np.linspace(u[0],u[-1],max(100,int(u[-1]/.12)));self.p=np.array(splev(self.u,tck)).T
  self.t=np.array(splev(self.u,tck,der=1)).T;self.t/=np.linalg.norm(self.t,axis=1)[:,None];self.tree=cKDTree(self.p);self.spline=CubicSpline(self.u,self.p)
 def project(self,p):
  p=np.asarray(p,float);near=self.tree.query(p,k=2)[1];best=np.full(len(p),np.inf);out=np.zeros(len(p));off=np.zeros_like(p);tang=np.zeros_like(p)
  for k in range(2):
   for delta in [-1,0]:
    i=np.clip(near[:,k]+delta,0,len(self.p)-2);a=self.p[i];d=self.p[i+1]-a;v=np.clip(((p-a)*d).sum(1)/(d*d).sum(1),0,1);c=a+v[:,None]*d;dist=((p-c)**2).sum(1);sel=dist<best;best[sel]=dist[sel];out[sel]=(self.u[i]+v*(self.u[i+1]-self.u[i]))[sel];off[sel]=(p-c)[sel];tang[sel]=(self.t[i]*(1-v[:,None])+self.t[i+1]*v[:,None])[sel]
  tang/=np.linalg.norm(tang,axis=1)[:,None]
  return out,off,tang,np.sqrt(best)
class Transport:
 def __init__(self,source,target):
  self.source=source;self.c=CubicSpline(source.u,target);self.t=self.c(source.u,1);self.t/=np.linalg.norm(self.t,axis=1)[:,None]
 def move(self,p,inner=5,outer=9):
  p=np.asarray(p,float);u,off,t0,r=self.source.project(p);off=p-self.source.spline(u);t0=self.source.spline(u,1);t0/=np.linalg.norm(t0,axis=1)[:,None];t1=self.c(u,1);t1/=np.linalg.norm(t1,axis=1)[:,None];v=np.cross(t0,t1);cos=(t0*t1).sum(1)
  rotated=off+np.cross(v,off)+np.cross(v,np.cross(v,off))/np.maximum(1+cos,1e-5)[:,None]
  q=self.c(u)+rotated;w=smooth((outer-r)/(outer-inner));return p+w[:,None]*(q-p)
segments=['petrous','cavernous','paraophthalmic','posterior-communicating','anterior-choroidal','terminus'];ica={};oph={};axis={}
for side in ['left','right']:
 pts=np.concatenate([np.array(flow['entries'][f'artery.anterior.internal_carotid_{side}.segment.{k}']['points'])for k in segments])
 c=Curve(inverse146(pts),smoothing=.25);root=inverse146(np.array(flow['entries']['artery.anterior.ophthalmic_'+side]['points'][:1]));at=c.project(root)[0][0]
 w=smooth((13-abs(c.u-at))/9);target=v146.warp(c.p)+np.c_[np.zeros(len(w)),-3*w,np.zeros(len(w))];ica[side]=Transport(c,target);axis[side]=(c,target)
currentFlow=json.load(open(A/'public/anatomy/dsa-flow.json'))
roots={};deltas={}
for side in ['left','right']:
 sid='artery.anterior.ophthalmic_'+side
 roots[side]=inverse146(np.array(flow['entries'][sid]['points'][:1]))[0]
 deltas[side]=np.array(currentFlow['entries'][sid]['points'][0])-roots[side]
def primary(p):
 p=np.asarray(p,float);weights=np.stack([smooth((25-np.linalg.norm(p-roots[side],axis=1))/18) for side in ['left','right']],axis=1)
 total=weights.sum(1);coverage=1-(1-weights[:,0])*(1-weights[:,1]);delta=weights@np.array([deltas[s]for s in ['left','right']]);return p+delta*(coverage/np.maximum(total,1e-20)*(1-smooth((p[:,2]-80)/9)))[:,None]
for side in ['left','right']:
 sid='artery.anterior.ophthalmic_'+side
 rest=inverse146(np.array(flow['entries'][sid]['points']));source=Curve(rest,smoothing=.08)
 # Existing course through the lower canal, transported from its centreline
 # instead of shearing each wall vertex according to its y coordinate.
 desired=v147.warp(v146.warp(rest),sid);desiredCurve=Curve(desired,smoothing=.12)
 # Parameterise source/target by the same original source arc progression.
 # Use corresponding original stations, avoiding nearest-path shortcuts.
 u=np.r_[0,np.linalg.norm(np.diff(rest,axis=0),axis=1).cumsum()];u/=u[-1]
 raw=CubicSpline(u,desired);target=raw((source.u-source.u[0])/(source.u[-1]-source.u[0]))
 weight=smooth((source.u-1)/2);near=primary(source.p);target=near+weight[:,None]*(target-near)
 canal=v147.S[side];mid=np.array(canal['mid']);direction=np.array(canal['axis']);centre=mid+(target[:,1]-mid[1])[:,None]/direction[1]*direction;cw=smooth((target[:,1]+36)/3)*(1-smooth((target[:,1]+20)/3));target+=cw[:,None]*(centre-target)
 # A mild spline regularisation removes the short transition's tangent kink.
 target=Curve(target,smoothing=.05).p if False else target
 oph[side]=Transport(source,target)
def descendant(sid,root):
 seen=set()
 while sid and sid not in seen:
  if sid==root:return True
  seen.add(sid);sid=rows.get(sid,{}).get('parent')
 return False
def transform(p146,sid):
 base=inverse146(np.asarray(p146,float));q=primary(base)
 for side,tr in oph.items():
  if descendant(sid,'artery.anterior.ophthalmic_'+side):
   u,_,_,rr=tr.source.project(base);w=smooth((u-1)/2)*smooth((7-rr)/5);tube=tr.move(base,inner=100,outer=101);q+=w[:,None]*(tube-q)
 # Retain the reviewed SOF/deep recurrent finishing controls from revision147.
 cfg=json.load(open(A/'anatomy/source/foramina/revision147-sof-controls.json'))
 for c in cfg:
  rr=np.linalg.norm(q-np.array(c['centre']),axis=1);q+=smooth((c['outer']-rr)/(c['outer']-c['core']))[:,None]*np.array(c['delta'])
 if 'artery.amendment.deep_recurrent_ophthalmic.'in sid:
  side=sid.rsplit('.',1)[-1];control=next(c for c in json.load(open(A/'anatomy/source/foramina/revision147-deep-controls.json'))if c['side']==side);w=smooth((abs(q[:,0])-18.15)/1.15)*smooth((q[:,1]+32)/1.5)*(1-smooth((q[:,1]+22.5)/1.5));q[:,2]+=control['liftMm']*w
 return q
if __name__=='__main__':
 out={};ref={};changed=[];current=Glb(A/'public/anatomy/models/complete-circulation.glb');old=Glb(B/'public/anatomy/models/complete-circulation.glb')
 for side in ['left','right']:
  for kind in ['ophthalmic_'+side]+['internal_carotid_'+side+'.segment.'+x for x in segments]:
   sid='artery.anterior.'+kind;s=rows[sid];p,f,n=old.mesh(s['asset']['node']);q=transform(p,sid);pp,ff,nn=current.mesh(s['asset']['node']);assert np.array_equal(f,ff)
   for tag,points in [('before',pp),('after',q),('rest',inverse146(p))]:out[sid+'_'+tag]=points
   out[sid+'_f']=f;print(sid,'move',np.linalg.norm(q-pp,axis=1).max(),flush=True)
 for side,(c,target)in axis.items():out['ica_'+side+'_axis']=primary(c.p)
 for side,tr in oph.items():out['oph_'+side+'_axis']=tr.c(tr.source.u)
 np.savez(A/'anatomy/source/foramina/revision156-preview.npz',**out)
