import numpy as np
from scipy.spatial import cKDTree

def curve_distance(p,curve):
 c=np.asarray(curve);v=c[1:]-c[:-1];_,ii=cKDTree((c[1:]+c[:-1])/2).query(p,k=min(5,len(v)))
 if ii.ndim==1:ii=ii[:,None]
 a=c[ii];vv=v[ii];t=np.clip(np.sum((p[:,None]-a)*vv,axis=2)/np.maximum(np.sum(vv*vv,axis=2),1e-20),0,1);return np.min(np.linalg.norm(p[:,None]-a-t[:,:,None]*vv,axis=2),axis=1)
def petrous_warp(points,fields):
 q=np.array(points,dtype=float).copy();steps=96
 for step in range(steps):
  shift=np.zeros_like(q)
  for f in fields:
   de=np.array(f['delta']);old=np.array(f['old'])+de*step/steps;lo=old.min(0)-f['outer'];hi=old.max(0)+f['outer'];sel=((q>=lo)&(q<=hi)).all(1)
   if not any(sel):continue
   d=curve_distance(q[sel],f['protectedIcaCourse']);w=np.clip((d-2.85)/2,0,1);w=w*w*(3-2*w)
   # Smooth velocity interpolation avoids discontinuities at the medial
   # axis between non-adjacent bends of the original tiny branch.
   arc=np.r_[0,np.cumsum(np.linalg.norm(np.diff(old,axis=0),axis=1))];tt=np.linspace(0,arc[-1],max(12,int(arc[-1]/.35)+1));c=np.column_stack([np.interp(tt,arc,old[:,i]) for i in range(3)]);vel=np.column_stack([np.interp(tt,arc,de[:,i]) for i in range(3)]);qq=q[sel];out=np.zeros_like(qq)
   for start in range(0,len(qq),2048):
    pp=qq[start:start+2048];dd=np.sum((pp[:,None]-c[None])**2,axis=2);ww=np.exp(-(dd-dd.min(1)[:,None])/(2*.9**2));out[start:start+2048]=ww@vel/ww.sum(1)[:,None]
   distance=curve_distance(qq,old);fall=np.clip((f['outer']-distance)/(f['outer']-f['core']),0,1);fall=fall*fall*(3-2*fall)
   shift[sel]+=out*w[:,None]*fall[:,None]/steps
  q+=shift
 return q
