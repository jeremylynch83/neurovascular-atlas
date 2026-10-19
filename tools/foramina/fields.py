"""Smooth local velocity fields used for the v0.9.134 passage repairs.

Requires NumPy/SciPy for authoring only. Ordinary application builds reuse the
delivered GLBs and have no new dependency.
"""
import numpy as np
from scipy.spatial import cKDTree

def nearest_velocity(points,old,delta,core,outer):
    seg=old[1:]-old[:-1];mid=(old[1:]+old[:-1])/2
    _,nearest=cKDTree(mid).query(points,k=min(5,len(seg)))
    if nearest.ndim==1:nearest=nearest[:,None]
    a=old[nearest];v=seg[nearest]
    t=np.clip(np.sum((points[:,None,:]-a)*v,axis=2)/np.maximum(np.sum(v*v,axis=2),1e-20),0,1)
    q=a+t[:,:,None]*v;dd=np.linalg.norm(points[:,None,:]-q,axis=2);best=np.argmin(dd,axis=1)
    index=nearest[np.arange(len(points)),best];t=t[np.arange(len(points)),best];distance=dd[np.arange(len(points)),best]
    shift=delta[index]*(1-t[:,None])+delta[index+1]*t[:,None]
    w=np.clip((outer-distance)/(outer-core),0,1);w=w*w*(3-2*w)
    return shift*w[:,None]

def artery_warp(points,fields):
    q=np.asarray(points,dtype=float).copy();steps=24
    for step in range(steps):
        shift=np.zeros_like(q)
        for f in fields:
            delta=np.asarray(f['delta']);old=np.asarray(f['old'])+delta*(step/steps)
            lo=old.min(0)-f['outer'];hi=old.max(0)+f['outer'];sel=((q>=lo)&(q<=hi)).all(1)
            if np.any(sel):shift[sel]+=nearest_velocity(q[sel],old,delta,f['core'],f['outer'])/steps
        q+=shift
    return q

def section_warp(points,section_map):
    """Map vertices only after splitting triangles along every z boundary.

    Within each slab this is exactly affine. The positive axial derivative
    recorded in the validation report prevents local folding.
    """
    p=np.asarray(points,dtype=float);q=p.copy();delta=np.asarray(section_map['delta'])
    for k in range(3):q[:,k]+=np.interp(p[:,2],section_map['z'],delta[:,k],left=delta[0,k],right=0)
    return q
