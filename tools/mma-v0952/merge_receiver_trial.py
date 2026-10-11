"""Try exact Boolean exterior unions at the native lesser-wing receivers.

Native endpoints are temporarily capped for the solid Boolean operation, then
the exact cap faces are removed. The resulting labelled exterior must retain
all original receiver openings. No failed union replaces candidate geometry.
"""
from common import *
import ast
vtk.vtkLogger.SetStderrVerbosity(vtk.vtkLogger.VERBOSITY_OFF)
def arrays(pd):
    return vtk_to_numpy(pd.GetPoints().GetData()).copy(),vtk_to_numpy(pd.GetPolys().GetData()).reshape(-1,4)[:,1:].copy()
def clean(pd):
    c=vtk.vtkCleanPolyData();c.SetInputData(pd);c.SetToleranceIsAbsolute(True);c.SetAbsoluteTolerance(1e-7);c.Update();t=vtk.vtkTriangleFilter();t.SetInputConnection(c.GetOutputPort());t.Update();p=vtk.vtkPolyData();p.DeepCopy(t.GetOutput());return p
def topology(v,f):
    e=np.sort(np.vstack([f[:,[0,1]],f[:,[1,2]],f[:,[2,0]]]),axis=1);edges,counts=np.unique(e,axis=0,return_counts=True)
    c=vtk.vtkPolyDataConnectivityFilter();c.SetInputData(poly(v,f));c.SetExtractionModeToAllRegions();c.Update()
    return dict(boundaryEdges=int(np.sum(counts==1)),nonManifoldEdges=int(np.sum(counts>2)),components=int(c.GetNumberOfExtractedRegions()))
rev=json.loads((OUT/'revision.json').read_text());reports=[]
module=ast.parse((Path(__file__).parents[1]/'mma-v0953/geometry.py').read_text())
ringsdef=next(x for x in module.body if isinstance(x,ast.FunctionDef) and x.name=='rings')
exec(compile(ast.Module(body=[ringsdef],type_ignores=[]),'rings','exec'))
for side in ['right','left']:
    if '--side' in sys.argv and side!=sys.argv[sys.argv.index('--side')+1]:continue
    receiver='vein.sphenoparietal.'+side;names=[receiver]+['vein.middle_meningeal.'+x+'.'+side for x in ['anterior','posterior']]
    v,f=load(receiver);pd=clean(poly(v,f));nv,nf=arrays(pd)
    cv=nv.copy();cf=nf.copy()
    directed=set(map(tuple,np.vstack([nf[:,[0,1]],nf[:,[1,2]],nf[:,[2,0]]]).tolist()))
    try:loops=rings(nv,nf)
    except RuntimeError as exc:
        reports.append(dict(side=side,passed=False,reason=str(exc)));continue
    for loop in loops:
        centre=len(cv);cv=np.vstack([cv,nv[loop].mean(0)])
        cap=np.c_[loop,np.roll(loop,-1),np.full(len(loop),centre)]
        if (int(loop[0]),int(loop[1])) in directed:cap=cap[:,[1,0,2]]
        cf=np.vstack([cf,cap])
    closed=poly(cv,cf)
    # Faces not present in the source are temporary cap triangles.
    sourcekeys={tuple(sorted(np.ascontiguousarray(nv[t]).view(np.dtype((np.void,24))).ravel().tolist())) for t in nf}
    caps=[]
    for face in cf:
        key=tuple(sorted(np.ascontiguousarray(cv[face]).view(np.dtype((np.void,24))).ravel().tolist()))
        if key not in sourcekeys:caps.append(face)
    caps=np.asarray(caps,dtype=np.uint32)
    print(side,'source',topology(nv,nf),'closed',topology(cv,cf),'cap faces',len(caps),flush=True)
    if topology(cv,cf)['boundaryEdges']:reports.append(dict(side=side,passed=False,reason='Native receiver could not be capped'));continue
    original=closed;inputs=[(nv,nf)]
    for name in names[1:]:
        w,g=load(name,OUT);inputs.append((w,g));op=vtk.vtkBooleanOperationPolyDataFilter();op.SetOperationToUnion();op.SetInputData(0,original);op.SetInputData(1,clean(poly(w,g)));op.SetTolerance(1e-6);op.Update();original=clean(op.GetOutput());print(side,name,'union points',original.GetNumberOfPoints(),flush=True)
        if not original.GetNumberOfPoints():break
    if not original.GetNumberOfPoints():reports.append(dict(side=side,passed=False,reason='Boolean union returned empty geometry'));continue
    uv,uf=arrays(original);caploc=locator(cv,caps);capdist=closest(caploc,uv)[1];uf=uf[~np.all(capdist[uf]<2e-5,axis=1)]
    # Keep the original coordinates at native openings exactly.
    e=np.sort(np.vstack([nf[:,[0,1]],nf[:,[1,2]],nf[:,[2,0]]]),axis=1);edges,counts=np.unique(e,axis=0,return_counts=True);boundary=np.unique(edges[counts==1]);d,k=cKDTree(nv[boundary]).query(uv);snap=d<2e-5;uv[snap]=nv[boundary[k[snap]]]
    ids,inv=np.unique(uf,return_inverse=True);uv=uv[ids];uf=inv.reshape(-1,3);top=topology(uv,uf)
    np.savez(OUT/('receiver-union-'+side+'.npz'),v=uv.astype('<f4'),f=uf.astype('<u4'))
    preserved=cKDTree(uv).query(nv[boundary])[0]
    report=dict(side=side,vertices=len(uv),triangles=len(uf),topology=top,originalBoundaryEdges=topology(nv,nf)['boundaryEdges'],nativeOpeningMaximumMismatchMm=float(preserved.max()),passed=top['nonManifoldEdges']==0 and top['components']==1 and top['boundaryEdges']==topology(nv,nf)['boundaryEdges'] and preserved.max()<1e-5)
    reports.append(report);print(report,flush=True)
(OUT/'receiver-union-trial.json').write_text(json.dumps(reports,indent=2))

