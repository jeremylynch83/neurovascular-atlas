"""Repair bounded Boolean slivers and preserve every original receiver collar.

Only sub-0.001 mm2 excess faces and new holes under 0.5 mm are repaired.
Missing native boundary vertices must lie on the unchanged output boundary,
where they are reinserted exactly. Larger changes reject the trial.
"""
from common import *
import ast
vtk.vtkLogger.SetStderrVerbosity(vtk.vtkLogger.VERBOSITY_OFF)
module=ast.parse((Path(__file__).parents[1]/'mma-v0953/geometry.py').read_text());fn=next(x for x in module.body if isinstance(x,ast.FunctionDef) and x.name=='rings');exec(compile(ast.Module(body=[fn],type_ignores=[]),'rings','exec'))
module=ast.parse((Path(__file__).parent/'self_check.py').read_text());fn=next(x for x in module.body if isinstance(x,ast.FunctionDef) and x.name=='intersections');exec(compile(ast.Module(body=[fn],type_ignores=[]),'self_check','exec'))
def edges(f):
    ee=np.sort(np.vstack([f[:,[0,1]],f[:,[1,2]],f[:,[2,0]]]),axis=1);return np.unique(ee,axis=0,return_counts=True)
def segment_distance(points,vertices,segments):
    aa=vertices[segments[:,0]];ab=vertices[segments[:,1]]-aa;den=np.maximum((ab*ab).sum(1),1e-20);pp=points[:,None]-aa[None];t=np.clip((pp*ab[None]).sum(2)/den[None],0,1);dist=np.linalg.norm(pp-t[...,None]*ab[None],axis=2);return dist,t
side=sys.argv[sys.argv.index('--side')+1] if '--side' in sys.argv else 'right';n='vein.sphenoparietal.'+side
sv,sf=load(n);_,first,inv=np.unique(sv,axis=0,return_index=True,return_inverse=True);sv=sv[first];sf=inv[sf]
tri=sv[sf];sf=sf[np.linalg.norm(np.cross(tri[:,1]-tri[:,0],tri[:,2]-tri[:,0]),axis=1)>1e-10]
_,unique=np.unique(np.sort(sf,axis=1),axis=0,return_index=True);sf=sf[np.sort(unique)]
ee,counts=edges(sf);nativeedges=ee[counts==1];nativeids=np.unique(nativeedges)
x=np.load(OUT/('receiver-union-'+side+'.npz'));v=x['v'].astype(float);f=x['f'].copy();removed=[];caps=[];inserted=[]
for _ in range(10):
    ee,c=edges(f);over=ee[c>2]
    if not len(over):break
    doomed=set()
    for edge in over:
        ids=np.flatnonzero(np.sum(np.isin(f,edge),axis=1)==2);t=v[f[ids]];area=np.linalg.norm(np.cross(t[:,1]-t[:,0],t[:,2]-t[:,0]),axis=1)/2
        for local in np.argsort(area)[:len(ids)-2]:
            assert area[local]<.001,'Union defect exceeds the bounded sliver policy'
            doomed.add(int(ids[local]));removed.append(float(area[local]))
    f=np.delete(f,sorted(doomed),axis=0)
for loop in rings(v,f):
    dd,_=segment_distance(v[loop],sv,nativeedges)
    if np.all(dd.min(1)<1e-4):continue
    diameter=float(np.linalg.norm(v[loop].max(0)-v[loop].min(0)))
    assert diameter<.5,'New union hole exceeds the bounded repair size'
    directed=set(map(tuple,np.vstack([f[:,[0,1]],f[:,[1,2]],f[:,[2,0]]]).tolist()))
    centre=len(v);v=np.vstack([v,v[loop].mean(0)]);cap=np.c_[loop,np.roll(loop,-1),np.full(len(loop),centre)]
    if (int(loop[0]),int(loop[1])) in directed:cap=cap[:,[1,0,2]]
    f=np.vstack([f,cap]);caps.append(diameter)
for point in sv[nativeids]:
    if cKDTree(v).query(point)[0]<1e-6:continue
    ee,c=edges(f);boundary=ee[c==1];dd,t=segment_distance(point[None],v,boundary);k=int(dd.argmin());edge=boundary[k];distance=float(dd[0,k]);assert distance<1e-4,'Native opening moved off its original surface'
    ids=np.flatnonzero(np.sum(np.isin(f,edge),axis=1)==2);assert len(ids)==1
    fi=int(ids[0]);tri=f[fi];a,b=edge;ci=int(next(p for p in tri if p not in edge));pi=len(v);v=np.vstack([v,point]);
    if any(tri[h]==a and tri[(h+1)%3]==b for h in range(3)):replacement=np.array([[a,pi,ci],[pi,b,ci]])
    else:replacement=np.array([[b,pi,ci],[pi,a,ci]])
    f=np.vstack([np.delete(f,fi,axis=0),replacement]);inserted.append(point.tolist())
# Restore floating-point copies of all source boundary coordinates.
d,k=cKDTree(sv[nativeids]).query(v);take=d<1e-5;v[take]=sv[nativeids[k[take]]];v=v.astype('<f4').astype(float)
ee,c=edges(f);gap=cKDTree(v).query(sv[nativeids])[0];folds=intersections(v,f);baseline=intersections(sv,sf)
con=vtk.vtkPolyDataConnectivityFilter();con.SetInputData(poly(v,f));con.SetExtractionModeToAllRegions();con.Update()
report=dict(side=side,removedSliverAreasMm2=removed,patchedHoleDiametersMm=caps,reinsertedNativeCollarVertices=len(inserted),boundaryEdges=int(np.sum(c==1)),baselineBoundaryEdges=len(nativeedges),nonManifoldEdges=int(np.sum(c>2)),components=int(con.GetNumberOfExtractedRegions()),nativeCollarMismatchMm=float(gap.max()),baselineReceiverSelfIntersections=len(baseline),unionSelfIntersections=len(folds),passed=not folds and np.sum(c==1)==len(nativeedges) and not np.sum(c>2) and gap.max()<1e-5 and con.GetNumberOfExtractedRegions()==1)
np.savez(OUT/('receiver-union-repaired-'+side+'.npz'),v=v.astype('<f4'),f=f.astype('<u4'))
(OUT/('receiver-union-repair-'+side+'.json')).write_text(json.dumps(report,indent=2));print(report,flush=True)
raise SystemExit(0 if report['passed'] else 2)

