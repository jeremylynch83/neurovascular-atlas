"""Join paired channels through a bounded receiver patch.

Only the lateral lesser-wing segment is included in the solid Boolean step.
The native cavernous receiver collar stays outside that operation. Local
plane cuts are rejoined to unchanged source faces, retaining named labels
through a common exterior if the complete topology checks pass.
"""
from common import *
import ast
vtk.vtkLogger.SetStderrVerbosity(vtk.vtkLogger.VERBOSITY_OFF)
module=ast.parse((Path(__file__).parents[1]/'mma-v0953/geometry.py').read_text());definitions=[x for x in module.body if isinstance(x,ast.FunctionDef) and x.name in ['arrays','clip','rings']];exec(compile(ast.Module(body=definitions,type_ignores=[]),'geometry','exec'))
def clean(v,f):
    c=vtk.vtkCleanPolyData();c.SetInputData(poly(v,f));c.SetToleranceIsAbsolute(True);c.SetAbsoluteTolerance(1e-6);c.Update();tr=vtk.vtkTriangleFilter();tr.SetInputConnection(c.GetOutputPort());tr.Update();return arrays(tr.GetOutput())
def boundary(v,f):
    e=np.sort(np.vstack([f[:,[0,1]],f[:,[1,2]],f[:,[2,0]]]),axis=1);ee,c=np.unique(e,axis=0,return_counts=True);return ee[c==1],int(np.sum(c>2))
reports=[]
for side in ['right','left']:
    if '--side' in sys.argv and side!=sys.argv[sys.argv.index('--side')+1]:continue
    sign=1 if side=='right' else -1;receiver='vein.sphenoparietal.'+side;v,f=load(receiver)
    # These bounds contain both receiver-wall entry points, while keeping the
    # native cavernous and medial collars outside the Boolean operation.
    lv,lf=clip(v,f,sign*v[:,0]-39.5);lv,lf=clip(lv,lf,46.5-sign*lv[:,0]);lv,lf=clean(lv,lf)
    ov,of=clip(v,f,39.5-sign*v[:,0]);ev,ef=clip(v,f,sign*v[:,0]-46.5);outerv=np.vstack([ov,ev]);outerf=np.vstack([of,ef+len(ov)])
    cv=lv.copy();cf=lf.copy();caps=[];directed=set(map(tuple,np.vstack([lf[:,[0,1]],lf[:,[1,2]],lf[:,[2,0]]]).tolist()))
    loops=rings(lv,lf);print(side,'local receiver rings',len(loops),[len(x) for x in loops],flush=True)
    for loop in loops:
        centre=len(cv);cv=np.vstack([cv,lv[loop].mean(0)]);cap=np.c_[loop,np.roll(loop,-1),np.full(len(loop),centre)]
        if (int(loop[0]),int(loop[1])) in directed:cap=cap[:,[1,0,2]]
        cf=np.vstack([cf,cap]);caps.extend(cap.tolist())
    caps=np.asarray(caps,dtype=np.uint32);current=poly(cv,cf)
    for label in ['anterior','posterior']:
        name='vein.middle_meningeal.'+label+'.'+side;w,g=load(name,OUT);w,g=clean(w,g);op=vtk.vtkBooleanOperationPolyDataFilter();op.SetOperationToUnion();op.SetTolerance(1e-7);op.SetInputData(0,current);op.SetInputData(1,poly(w,g));op.Update();p=op.GetOutput()
        if not p.GetNumberOfPoints():raise RuntimeError('Local Boolean union returned no mesh')
        uv,uf=clean(*arrays(p));current=poly(uv,uf);print(side,label,len(uv),len(uf),flush=True)
    uv,uf=arrays(current);d=closest(locator(cv,caps),uv)[1];uf=uf[~np.all(d[uf]<2e-5,axis=1)]
    vv=np.vstack([outerv,uv]);ff=np.vstack([outerf,uf+len(outerv)]);vv,ff=clean(vv,ff)
    b,non=boundary(vv,ff);sourceb,_=boundary(v,f);mismatch=cKDTree(vv).query(v[np.unique(sourceb)])[0]
    con=vtk.vtkPolyDataConnectivityFilter();con.SetInputData(poly(vv,ff));con.SetExtractionModeToAllRegions();con.Update()
    row=dict(side=side,vertices=len(vv),triangles=len(ff),boundaryEdges=len(b),baselineBoundaryEdges=len(boundary(*clean(v,f))[0]),nonManifoldEdges=non,components=int(con.GetNumberOfExtractedRegions()),nativeCollarMismatchMm=float(mismatch.max()),passed=non==0 and len(b)==len(boundary(*clean(v,f))[0]) and con.GetNumberOfExtractedRegions()==1 and mismatch.max()<1e-5)
    np.savez(OUT/('receiver-local-union-'+side+'.npz'),v=vv.astype('<f4'),f=ff.astype('<u4'));reports.append(row);print(row,flush=True)
(OUT/'receiver-local-union-trial.json').write_text(json.dumps(reports,indent=2))

