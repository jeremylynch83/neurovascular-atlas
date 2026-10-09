"""Transport original shaft offsets while retaining shared branch collars."""
from common import *
from extract_curves import extract
from types import SimpleNamespace
from scipy.spatial import cKDTree
from scipy.ndimage import gaussian_filter1d
def recover(v,f,stage,other_vertices):
    q,rad,param,tt=extract(SimpleNamespace(v=v,f=f))
    centres=[]
    for t in tt:
        mask=abs(param-t)<.3
        centres.append((stage[mask]-v[mask]).mean(0) if mask.any() else (stage-v)[np.argsort(abs(param-t))[:16]].mean(0))
    qn=q+gaussian_filter1d(np.asarray(centres),2.,axis=0)
    def interp(a):return np.column_stack([np.interp(param,tt,a[:,j]) for j in range(3)])
    a=interp(np.gradient(q,tt,axis=0));b=interp(np.gradient(qn,tt,axis=0))
    a/=np.maximum(np.linalg.norm(a,axis=1)[:,None],1e-9);b/=np.maximum(np.linalg.norm(b,axis=1)[:,None],1e-9)
    cross=np.cross(a,b);dot=(a*b).sum(1);offset=v-interp(q)
    rotated=offset+np.cross(cross,offset)+np.cross(cross,np.cross(cross,offset))/np.maximum(1+dot,1e-6)[:,None]
    target=interp(qn)+rotated
    distance=cKDTree(other_vertices).query(v)[0]
    weight=smooth((np.minimum(param-tt[0],tt[-1]-param)-1)/1.5)*smooth(distance/1.0)
    # Protect the legacy folded junction neighbourhoods. Re-sweeping those
    # small union facets would introduce extra intersections at the collar.
    t=v[f].astype(float);cent=t.mean(1);radius=np.linalg.norm(t-cent[:,None],axis=2).max(1)
    tree=cKDTree(cent);lo=t.min(1);hi=t.max(1);fold=set()
    _,ids=np.unique(v,axis=0,return_inverse=True);welded=ids[f]
    for i,near in enumerate(tree.query_ball_point(cent,radius+radius.max())):
        for j in near:
            if j<=i or np.any(welded[i,:,None]==welded[j,None,:]):continue
            if np.any(lo[i]>hi[j]+1e-8) or np.any(lo[j]>hi[i]+1e-8):continue
            if vtk.vtkTriangle.TrianglesIntersect(*t[i],*t[j]):fold.update(f[i]);fold.update(f[j])
    if fold:
        d=cKDTree(v[list(fold)]).query(v)[0]
        weight*=smooth((d-2)/2)
    weight[distance<1e-5]=0
    after=(stage+(target-stage)*weight[:,None]).astype('<f4')
    assert np.array_equal(after[distance<1e-5],stage[distance<1e-5])
    return after,float(np.linalg.norm(after-stage,axis=1).max())
