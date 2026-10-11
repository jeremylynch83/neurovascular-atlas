"""Refit paired channel walls against exact neighbouring surfaces.

Uses dense path samples and local signed wall normals, retaining receiver
endpoints and native arterial geometry. A subsequent exact triangle audit
is mandatory; path clearance alone never grants acceptance.
"""
from smooth_fields import *
import ast
from scipy.ndimage import gaussian_filter1d
module=ast.parse((Path(__file__).parent/'build_paired_veins.py').read_text())
soliddef=next(x for x in module.body if isinstance(x,ast.FunctionDef) and x.name=='solid')
from scipy.ndimage import gaussian_filter
exec(compile(ast.Module(body=[soliddef],type_ignores=[]),'solid','exec'))
vtk.vtkLogger.SetStderrVerbosity(vtk.vtkLogger.VERBOSITY_OFF)
rev=json.loads((OUT/'revision.json').read_text());changed={r['node'] for r in rev['changed']}
rows=json.loads((OUT/'paired-channel-candidates.json').read_text())['channels']
selected=None if '--nodes' not in sys.argv else set(sys.argv[sys.argv.index('--nodes')+1].split(','))
mesh={n:load(n,OUT) if n in changed else load(n) for n in FILES};reports=[]
for row in rows:
    if selected and row['node'] not in selected:continue
    n=row['node'];source=np.load(OUT/(n+'.curve.npz'));q=source['q'].copy();radius=source['r'].copy();stem=source['stem'].copy();j=cKDTree(q).query(stem[0])[1]
    original=q.copy();initialstem=stem.copy();lo=np.concatenate([q,stem]).min(0)-5;hi=np.concatenate([q,stem]).max(0)+5;obstacles=[]
    for other,(v,f) in mesh.items():
        if other==row['receiver'] or other.startswith(('bone.','tooth')):continue
        if np.any(v.max(0)<lo) or np.any(v.min(0)>hi):continue
        if not (other.startswith(('brain.','vein.')) or FILES[other] in ['complete-circulation.glb','complete-anastomoses.glb']):continue
        fn=vtk.vtkImplicitPolyDataDistance();fn.SetInput(poly(v,f));obstacles.append((other,fn,v.min(0),v.max(0)))
    def correction(p,rr):
        delta=np.zeros_like(p);worst=0.;count=0
        for other,fn,low,high in obstacles:
            indices=np.flatnonzero(np.all(p>=low-rr[:,None]-.6,axis=1)&np.all(p<=high+rr[:,None]+.6,axis=1))
            for k in indices:
                clearance=float(sys.argv[sys.argv.index('--clearance')+1]) if '--clearance' in sys.argv else .16
                cp=[0.,0.,0.];dist=fn.EvaluateFunctionAndGetClosestPoint(p[k],cp);clear=rr[k]+clearance
                # Local wall distances outside a tubular patch do not establish
                # solid containment. Discard remote negative cap projections.
                if abs(dist)>max(clear+1.,1.5):continue
                if dist>=clear-1e-5:continue
                direction=p[k]-cp
                if dist<0:direction=-direction
                length=np.linalg.norm(direction)
                if length<1e-10:
                    fn.EvaluateGradient(p[k],direction);length=np.linalg.norm(direction)
                direction/=max(length,1e-10)
                penetration=clear-dist;delta[k]+=direction*min(penetration,.22)
                worst=max(worst,penetration);count+=1
        length=np.linalg.norm(delta,axis=1);delta*=np.minimum(1,.24/np.maximum(length,1e-12))[:,None]
        return delta,worst,count
    last=None
    for iteration in range(180):
        dq,worst,count=correction(q,radius);ds,sw,sc=correction(stem,np.full(len(stem),.23));worst=max(worst,sw)
        dq=gaussian_filter1d(dq,1.2,axis=0);ds=gaussian_filter1d(ds,1.2,axis=0)
        q+=dq*.6;stem+=ds*.6;stem[0]=q[j];stem[-1]=initialstem[-1]
        if iteration%30==0:print(n,iteration,'path collisions',count+sc,'maximum wall deficit',round(worst,4),flush=True)
        last=dict(iterations=iteration+1,pathWallViolations=count+sc,maximumWallDeficitMm=worst)
        if count+sc==0:break
    v,f=solid([(q,radius),(stem,np.full(len(stem),.23))]);write(n,v,f)
    np.savez(OUT/(n+'.curve.npz'),q=q,r=radius,stem=stem)
    row.update(vertices=len(v),triangles=len(f),maxRouteAdjustmentMm=float(np.linalg.norm(q-original,axis=1).max()))
    edges=np.sort(np.vstack([f[:,[0,1]],f[:,[1,2]],f[:,[2,0]]]),axis=1);_,counts=np.unique(edges,axis=0,return_counts=True)
    conn=vtk.vtkPolyDataConnectivityFilter();conn.SetInputData(poly(v,f));conn.SetExtractionModeToAllRegions();conn.Update()
    row.update(boundaryEdges=int(np.sum(counts==1)),nonManifoldEdges=int(np.sum(counts>2)),components=conn.GetNumberOfExtractedRegions())
    reports.append(dict(node=n,**last,maxRouteAdjustmentMm=row['maxRouteAdjustmentMm'],obstacleCount=len(obstacles)))
    for r in rev['changed']:
        if r['node']==n:r.update(row)
    print(reports[-1],flush=True)
(OUT/'paired-channel-candidates.json').write_text(json.dumps(dict(status='provisional-not-exported',channels=rows,duplicatedLesserWingChannel=False,receiverExteriorMerged=False),indent=2))
(OUT/'revision.json').write_text(json.dumps(rev,indent=2))
(OUT/'paired-route-refit.json').write_text(json.dumps(dict(method='Dense exact-surface local wall clearance iteration',results=reports,requiresExactTriangleAudit=True),indent=2))

