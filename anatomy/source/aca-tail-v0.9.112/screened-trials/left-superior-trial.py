from region import *
def smooth(x):
 x=np.clip(x,0,1);return x*x*x*(10+x*(-15+6*x))
def query(sd,pts):
 data=vtk.vtkPolyData();vp=vtk.vtkPoints();vp.SetData(numpy_to_vtk(pts.astype(float),deep=True));data.SetPoints(vp);op=vtk.vtkSampleImplicitFunctionFilter();op.SetInputData(data);op.SetImplicitFunction(sd);op.ComputeGradientsOff();op.Update();return vtk_to_numpy(op.GetOutput().GetPointData().GetScalars()).copy()
def samples(t):return np.vstack([t.reshape(-1,3),t.mean(1),((t+np.roll(t,-1,axis=1))/2).reshape(-1,3)])
n='ACA A5 left';v,f=scene.mesh(n);p0=v.astype(float);w=smooth((-94.3-p0[:,1])/0.8);ids=np.flatnonzero(np.any(w[f]>0,axis=1));aa=samples(p0[f[ids]]);targets={};rows=[]
lo=aa.min(0)-1.5;hi=aa.max(0)+1.5
for other in scene.nearby(lo,hi):
 if scene.systems[other]not in ['brain','bone']or not scene.volume_topology(other)['closedOrientedManifold']:continue
 sd=vtk.vtkImplicitPolyDataDistance();sd.SetInput(poly(*scene.mesh(other)));targets[other]=(sd,query(sd,aa))
for x,z in [(0,0.5),(0,1),(-0.25,0.75)]:
 p=p0.copy();p[:,0]+=x*w;p[:,2]+=z*w;p=p.astype('<f4');bb=samples(p[f[ids]].astype(float));depth=[]
 for other,(sd,before)in targets.items():
  after=query(sd,bb);extra=np.maximum(np.minimum(before,0)-np.minimum(after,0),0)
  if not np.any(before< -1e-5)and not np.any(after< -1e-5):continue
  j=int(extra.argmax());depth.append(dict(target=other,insideBefore=int((before< -1e-5).sum()),insideAfter=int((after< -1e-5).sum()),newInside=int(((before>=-1e-5)&(after< -1e-5)).sum()),extraDepth=float(extra.max()),worstSource=aa[j].tolist(),depthBefore=float(max(0,-before.min())),depthAfter=float(max(0,-after.min()))))
 a=p0[f[ids]];b=p[f[ids]].astype(float);ca=np.cross(a[:,1]-a[:,0],a[:,2]-a[:,0]);cb=np.cross(b[:,1]-b[:,0],b[:,2]-b[:,0]);flipped=int((np.einsum('ij,ij->i',ca,cb)<=0).sum())
 crossings=[];checks=0
 from cache import BVH
 from geometry import triangle_crosses
 tree=BVH.build(p,f)
 for i in ids:
  tri=p[f[i]].astype(float);lo=tri.min(0)-1e-7;hi=tri.max(0)+1e-7
  for other in sorted(set(scene.nearby(lo,hi))|{n}):
   q,g=(p,f)if other==n else scene.mesh(other)
   if scene.systems[other]in ['brain','bone']:continue
   bvh=tree if other==n else scene.bvh(other)
   for j in bvh.query(lo,hi):
    if n==other and i==j:continue
    b=q[g[j]].astype(float)
    if np.any(b.max(0)<lo)or np.any(b.min(0)>hi):continue
    checks+=1
    if triangle_crosses(tri,b):crossings.append({'face':int(i),'other':other,'otherFace':int(j)})
 row=dict(crossings=crossings,checks=checks,x=x,z=z,changedFaces=len(ids),flippedFaces=flipped,depth=depth,passed=not crossings and not flipped and all(r['newInside']==0 and r['extraDepth']<=.001 for r in depth));rows.append(row);print({k:v for k,v in row.items()if k!='crossings'},'crossings',len(crossings),sorted({x['other']for x in crossings}),flush=True)
(W/'left-superior-trial.json').write_text(json.dumps(rows,indent=2)+'\n')
