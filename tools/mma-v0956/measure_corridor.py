"""Measure the unwarped reference and candidate guide corridor."""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).parents[1]/'mma-v0952'))
from smooth_fields import *
vtk.vtkLogger.SetStderrVerbosity(vtk.vtkLogger.VERBOSITY_OFF)
guides=json.loads((WORK/'tree-guides.json').read_text())
brain=[]
for n in FILES:
    if not n.startswith('brain.') or n.startswith(('brain.falx','brain.tentorium')):continue
    v,f=load(n);fn=vtk.vtkImplicitPolyDataDistance();fn.SetInput(poly(v,f))
    brain.append((n,fn,v.min(0),v.max(0)))
def distances(points,margin=12):
    dd=np.full(len(points),np.inf);owners=np.full(len(points),-1)
    for j,(name,fn,lo,hi) in enumerate(brain):
        ids=np.flatnonzero(np.all(points>=lo-margin,axis=1)&np.all(points<=hi+margin,axis=1))
        if not len(ids):continue
        ds=np.array([fn.EvaluateFunction(p) for p in points[ids]])
        take=ds<dd[ids];dd[ids[take]]=ds[take];owners[ids[take]]=j
    return dd,owners

bonev=[];bonef=[];bones=[]
for n in ['bone.sphenoid','bone.frontal','bone.occipital','bone.parietal.right','bone.parietal.left','bone.temporal.right','bone.temporal.left']:
    v,f=load(n);tri=v[f];norm=np.cross(tri[:,1]-tri[:,0],tri[:,2]-tri[:,0]);c=tri.mean(1)
    outer=np.einsum('ij,ij->i',norm,c-[0,-60,95])>0
    bonef.append(f[outer]+sum(len(w) for w in bonev));bonev.append(v)
    unique,inv=np.unique(v,axis=0,return_inverse=True);g=inv[f]
    edges=np.sort(np.vstack([g[:,[0,1]],g[:,[1,2]],g[:,[2,0]]]),axis=1);_,cnt=np.unique(edges,axis=0,return_counts=True)
    bones.append(dict(node=n,boundaryEdges=int((cnt==1).sum()),nonManifoldEdges=int((cnt>2).sum())))
outerloc=locator(np.vstack(bonev),np.vstack(bonef))
af=arterial_field();rows=[];samples=[]
for g in guides:
    old=np.asarray(g['oldPoints'])[::3];q=af(old);radius=np.asarray(g['radiusMm'])[::3]
    n=np.asarray(g['innerTableNormals'])[::3];n/=np.linalg.norm(n,axis=1)[:,None]
    d,owner=distances(q)
    # Probe both the potential intracranial corridor and diploic room.
    steps=np.arange(-1,8.01,.25)
    p=q[:,None,:]-steps[None,:,None]*n[:,None,:]
    bd,_=distances(p.reshape(-1,3));bd=bd.reshape(len(q),-1)
    feasible=bd>=radius[:,None]+.2
    first=np.argmax(feasible,axis=1);shift=steps[first];shift[~feasible.any(1)]=np.nan
    target=q-shift[:,None]*n
    outer,od=closest(outerloc,np.nan_to_num(target,nan=0))
    # Outer point must remain outside the vessel centre along the probe normal.
    cover=np.einsum('ij,ij->i',target-outer,n)-radius
    active=old[:,2]>53
    row=dict(node=g['node'],stations=int(active.sum()),minimumNeuralDistanceMm=float(d[active].min()),
             collidingCentreStations=int(np.sum(d[active]<radius[active])),
             maximumNecessaryOutwardProbeMm=float(np.nanmax(shift[active])),
             noClearPointWithin8mm=int(np.isnan(shift[active]).sum()),
             negativeOuterCoverStations=int(np.sum(cover[active]<0)),
             minimumOuterCoverMm=float(np.nanmin(cover[active])))
    rows.append(row);print(row,flush=True)
    samples.append(dict(node=g['node'],q=q.tolist(),r=radius.tolist(),n=n.tolist(),neuralDistance=d.tolist(),clearanceShift=shift.tolist(),outerCover=cover.tolist()))
(WORK/'corridor-depth.json').write_text(json.dumps(dict(boneTopology=bones,results=rows,samples=samples),indent=2))
