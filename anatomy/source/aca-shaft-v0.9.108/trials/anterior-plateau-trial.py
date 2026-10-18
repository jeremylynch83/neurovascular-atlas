from region import *
def smooth(x):
 x=np.clip(x,0,1);return x*x*x*(10+x*(-15+6*x))
def query(sd,pts):
 data=vtk.vtkPolyData();vp=vtk.vtkPoints();vp.SetData(numpy_to_vtk(pts.astype(float),deep=True));data.SetPoints(vp);op=vtk.vtkSampleImplicitFunctionFilter();op.SetInputData(data);op.SetImplicitFunction(sd);op.ComputeGradientsOff();op.Update();return vtk_to_numpy(op.GetOutput().GetPointData().GetScalars()).copy()
n='ACA A4 left';v,f=scene.mesh(n);p0=v.astype(float);ids=np.flatnonzero(np.any((p0[f,:,] if False else p0[f])[:,:,1]>-53.5,axis=1)&np.any(p0[f][:,:,1]<-37,axis=1));a=p0[f[ids]]
def samples(t):return np.vstack([t.reshape(-1,3),t.mean(1),((t+np.roll(t,-1,axis=1))/2).reshape(-1,3)])
aa=samples(a);core=(aa[:,1]>=-43)&(aa[:,1]<=-40.5);targets={}
for other in scene.nearby(v.min(0)-[0,0,2],v.max(0)+[3,0,0]):
 if scene.systems[other]not in ['brain','bone']or not scene.volume_topology(other)['closedOrientedManifold']:continue
 sd=vtk.vtkImplicitPolyDataDistance();sd.SetInput(poly(*scene.mesh(other)));targets[other]=(sd,query(sd,aa))
rows=[]
for start,plateau,x,z in [(-47,-43,2.5,-1),(-46,-43,2.5,-1),(-45,-42,2.5,-1),(-46,-43,2.5,0)]:
 w=smooth((p0[:,1]-start)/(plateau-start))*smooth((-37-p0[:,1])/3.5);p=p0.copy();p[:,0]+=x*w;p[:,2]+=z*w;p=p.astype('<f4');bb=samples(p[f[ids]].astype(float));depth=[]
 for other,(sd,before)in targets.items():
  after=query(sd,bb);extra=np.maximum(np.minimum(before,0)-np.minimum(after,0),0)
  if not np.any(before< -1e-5)and not np.any(after< -1e-5):continue
  j=int(extra.argmax());depth.append(dict(target=other,insideBefore=int((before< -1e-5).sum()),insideAfter=int((after< -1e-5).sum()),newInside=int(((before>=-1e-5)&(after< -1e-5)).sum()),extraDepth=float(extra.max()),worstSource=aa[j].tolist(),worstBefore=float(before[j]),worstAfter=float(after[j]),coreDepthBefore=float(max(0,-before[core].min())),coreDepthAfter=float(max(0,-after[core].min()))))
 row=dict(start=start,plateau=plateau,x=x,z=z,depth=depth,passed=all(r['newInside']==0 and r['extraDepth']<=.001 for r in depth));rows.append(row);print(row,flush=True)
(W/'anterior-plateau-trial.json').write_text(json.dumps(rows,indent=2)+'\n')
