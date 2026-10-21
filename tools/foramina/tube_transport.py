"""Centreline projection and radial-offset transport shared by local arterial repairs."""
import numpy as np
from scipy.interpolate import splprep,splev,CubicSpline
from scipy.spatial import cKDTree
def smooth(x):
 x=np.clip(x,0,1);return x*x*(3-2*x)
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
