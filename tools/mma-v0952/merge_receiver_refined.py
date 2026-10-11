"""A smooth implicit union limited to the native lateral receiver segment.

The original cavernous collar and medial receiver remain outside the remesh.
Two plane-bound annuli connect the new shared exterior to exact native cut
rings. This avoids unstable solid Booleans on the broad cavernous collar.
Candidate-only: topology, intersections and neighbouring contacts must pass.
"""
from common import *
import ast
from scipy.ndimage import gaussian_filter
vtk.vtkLogger.SetStderrVerbosity(vtk.vtkLogger.VERBOSITY_OFF)
module=ast.parse((Path(__file__).parents[1]/'mma-v0953/geometry.py').read_text());definitions=[x for x in module.body if isinstance(x,ast.FunctionDef) and x.name in ['arrays','clip','rings','bridge','iso']];exec(compile(ast.Module(body=definitions,type_ignores=[]),'geometry','exec'))
def clean(v,f):
    c=vtk.vtkCleanPolyData();c.SetInputData(poly(v,f));c.SetToleranceIsAbsolute(True);c.SetAbsoluteTolerance(1e-6);c.Update();t=vtk.vtkTriangleFilter();t.SetInputConnection(c.GetOutputPort());t.Update();return arrays(t.GetOutput())
def boundaries(f):
    e=np.sort(np.vstack([f[:,[0,1]],f[:,[1,2]],f[:,[2,0]]]),axis=1);ee,c=np.unique(e,axis=0,return_counts=True);return ee[c==1],int(np.sum(c>2))
reports=[]
for side in ['right','left']:
    sign=1 if side=='right' else -1;receiver='vein.sphenoparietal.'+side;sourcev,sourcef=load(receiver)
    localv,localf=clip(sourcev,sourcef,sign*sourcev[:,0]-39.5);localv,localf=clip(localv,localf,46.5-sign*localv[:,0]);localv,localf=clean(localv,localf)
    closedv=localv.copy();closedf=localf.copy();directed=set(map(tuple,np.vstack([localf[:,[0,1]],localf[:,[1,2]],localf[:,[2,0]]]).tolist()))
    for loop in rings(localv,localf):
        centre=len(closedv);closedv=np.vstack([closedv,localv[loop].mean(0)]);cap=np.c_[loop,np.roll(loop,-1),np.full(len(loop),centre)]
        if (int(loop[0]),int(loop[1])) in directed:cap=cap[:,[1,0,2]]
        closedf=np.vstack([closedf,cap])
    paths=[]
    for label in ['anterior','posterior']:
        x=np.load(OUT/('vein.middle_meningeal.'+label+'.'+side+'.curve.npz'));paths.extend([(x['q'],x['r']),(x['stem'],np.full(len(x['stem']),.23))])
    allq=np.vstack([closedv]+[p for p,r in paths]);lo=allq.min(0)-.7;hi=allq.max(0)+.7;spacing=.12;dims=np.ceil((hi-lo)/spacing).astype(int)+1;sp=(hi-lo)/(dims-1);field=np.full(dims,3.,np.float32)
    for q,r in paths:
        for a,b,ra,rb in zip(q[:-1],q[1:],r[:-1],r[1:]):
            pad=max(ra,rb)+.35;low=np.maximum(np.floor((np.minimum(a,b)-pad-lo)/sp).astype(int),0);high=np.minimum(np.ceil((np.maximum(a,b)+pad-lo)/sp).astype(int)+1,dims);sl=tuple(slice(int(a),int(b)) for a,b in zip(low,high));p=np.stack(np.meshgrid(*[lo[k]+np.arange(low[k],high[k])*sp[k] for k in range(3)],indexing='ij'),axis=-1);ab=b-a;t=np.clip(np.sum((p-a)*ab,axis=-1)/max(np.dot(ab,ab),1e-12),0,1);d=np.linalg.norm(p-a-t[...,None]*ab,axis=-1)-(ra*(1-t)+rb*t);field[sl]=np.minimum(field[sl],d)
    fn=vtk.vtkImplicitPolyDataDistance();fn.SetInput(poly(closedv,closedf));low=np.maximum(np.floor((closedv.min(0)-.4-lo)/sp).astype(int),0);high=np.minimum(np.ceil((closedv.max(0)+.4-lo)/sp).astype(int)+1,dims);sl=tuple(slice(int(a),int(b)) for a,b in zip(low,high));p=np.stack(np.meshgrid(*[lo[k]+np.arange(low[k],high[k])*sp[k] for k in range(3)],indexing='ij'),axis=-1);d=np.array([fn.EvaluateFunction(point) for point in p.reshape(-1,3)]).reshape(p.shape[:-1]);field[sl]=np.minimum(field[sl],d)
    field=gaussian_filter(field,.55);v,f=iso(field,lo,sp);del field
    outsidev=[];outsidef=[];targets=[]
    for bound,is_low,new_bound in [(40.,True,40.05),(46.,False,45.95)]:
        vv,ff=clip(sourcev,sourcef,(bound-sign*sourcev[:,0]) if is_low else (sign*sourcev[:,0]-bound));vv,ff=clean(vv,ff);cutids=np.flatnonzero(abs(sign*vv[:,0]-bound)<1e-4);loop=rings(vv,ff,cutids)[0];target=vv[loop];centre=target.mean(0);rad=float(np.linalg.norm(target[:,1:]-centre[1:],axis=1).max())+.25
        value=(sign*v[:,0]-new_bound) if is_low else (new_bound-sign*v[:,0]);value=np.maximum(value,np.linalg.norm(v[:,1:]-centre[1:],axis=1)-rad);v,f=clip(v,f,value)
        targets.append(dict(points=target,centre=centre,newPlane=new_bound));outsidef.append(ff+sum(len(x) for x in outsidev));outsidev.append(vv)
    nv=v.copy();nf=f.copy();newloops=rings(nv,nf);offset=len(nv);vv=np.vstack([nv]+outsidev);ff=np.vstack([nf]+[a+offset for a in outsidef])
    for target in targets:
        loop=min(newloops,key=lambda loop:np.linalg.norm(nv[loop].mean(0)-target['centre']));port=target['points'];ids=[]
        for point in port:ids.append(int(cKDTree(vv).query(point)[1]))
        ff=np.vstack([ff,bridge(vv,loop,np.asarray(ids))])
    vv,ff=clean(vv,ff);normal=vtk.vtkPolyDataNormals();normal.SetInputData(poly(vv,ff));normal.SplittingOff();normal.ConsistencyOn();normal.Update();vv,ff=arrays(normal.GetOutput());vv=vv.astype('<f4').astype(float)
    bd,non=boundaries(ff);sv,sf=clean(sourcev,sourcef);sbd,_=boundaries(sf);con=vtk.vtkPolyDataConnectivityFilter();con.SetInputData(poly(vv,ff));con.SetExtractionModeToAllRegions();con.Update();gap=cKDTree(vv).query(sourcev[np.unique(boundaries(sourcef)[0])])[0]
    report=dict(side=side,vertices=len(vv),triangles=len(ff),boundaryEdges=len(bd),baselineBoundaryEdges=len(sbd),nonManifoldEdges=non,components=int(con.GetNumberOfExtractedRegions()),nativeCollarMismatchMm=float(gap.max()),passed=non==0 and len(bd)==len(sbd) and con.GetNumberOfExtractedRegions()==1 and gap.max()<1e-5,method='Local signed-distance union with native plane-bound exterior annuli')
    np.savez(OUT/('receiver-implicit-union-'+side+'.npz'),v=vv.astype('<f4'),f=ff.astype('<u4'));reports.append(report);print(report,flush=True)
(OUT/'receiver-implicit-union-trial.json').write_text(json.dumps(reports,indent=2))

