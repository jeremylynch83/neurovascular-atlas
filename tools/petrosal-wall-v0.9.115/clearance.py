"""Cover unchanged triangles with certified balls, refining only inconclusive balls."""
import numpy as np

def certify(triangles,distance,threshold=1e-5,max_depth=10):
    pending=np.asarray(triangles,dtype=float)
    original_area=areas(pending).sum()
    certified_area=0.;leaf_count=0;minimum=float('inf');evaluated=0;deepest=0
    unresolved=0;unresolved_margin=None
    for depth in range(max_depth+1):
        if not len(pending):break
        deepest=depth;centres=pending.mean(axis=1)
        radius=np.linalg.norm(pending-centres[:,None],axis=2).max(axis=1)+1e-10
        margin=np.asarray(distance(centres),float)-radius;evaluated+=len(pending)
        safe=margin>threshold
        if safe.any():
            minimum=min(minimum,float(margin[safe].min()))
            certified_area+=float(areas(pending[safe]).sum());leaf_count+=int(safe.sum())
        pending=pending[~safe]
        if not len(pending):break
        if depth==max_depth:
            unresolved=len(pending);unresolved_margin=float(margin[~safe].min());break
        a,b,c=pending[:,0],pending[:,1],pending[:,2];ab=(a+b)/2;bc=(b+c)/2;ca=(c+a)/2
        pending=np.concatenate([np.stack([a,ab,ca],axis=1),np.stack([ab,b,bc],axis=1),np.stack([ca,bc,c],axis=1),np.stack([ab,bc,ca],axis=1)])
    retained_area=certified_area+float(areas(pending).sum())
    assert abs(retained_area-original_area)<=max(1e-12,original_area*1e-10)
    return {'passed':unresolved==0,'sourceTriangles':len(triangles),'evaluatedBalls':evaluated,'certifiedLeafTriangles':leaf_count,'maximumSubdivisionDepth':deepest,'unresolvedLeafTriangles':unresolved,'minimumCertifiedClearanceMarginMm':minimum if np.isfinite(minimum)else None,'minimumUnresolvedMarginMm':unresolved_margin,'sourceTriangleAreaMm2':float(original_area),'certifiedAreaMm2':certified_area,'areaCoverageChecked':True,'clearanceThresholdMm':threshold,'maximumPermittedSubdivisionDepth':max_depth}

def areas(t):
    return .5*np.linalg.norm(np.cross(t[:,1]-t[:,0],t[:,2]-t[:,0]),axis=1)
