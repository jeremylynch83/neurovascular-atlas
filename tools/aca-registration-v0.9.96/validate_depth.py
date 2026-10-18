from common import *
from regional_validation import face_key,enclosed_samples
from vtk.util.numpy_support import vtk_to_numpy
T=W/'accepted';rows=[];issues=[]
def sample_dist(sd,points):
 if not len(points):return np.array([])
 data=vtk.vtkPolyData();vp=vtk.vtkPoints();vp.SetData(numpy_to_vtk(points.astype(float),deep=True));data.SetPoints(vp);op=vtk.vtkSampleImplicitFunctionFilter();op.SetInputData(data);op.SetImplicitFunction(sd);op.ComputeGradientsOff();op.Update();return vtk_to_numpy(op.GetOutput().GetPointData().GetScalars()).copy()
def samples(t):
 if not len(t):return np.empty((0,3))
 return np.vstack([t.reshape(-1,3),t.mean(1),((t+np.roll(t,-1,axis=1))/2).reshape(-1,3)])
for n in ['ACA A5 right','Precuneal right','ACA falcine branch right']:
 v,f=scene.mesh(n);p=np.fromfile(T/(n+'.positions.bin'),'<f4').reshape(-1,3);g=np.fromfile(T/(n+'.indices.bin'),'<u4').reshape(-1,3);predicted=np.fromfile(W/'sheared'/(n+'.positions.bin'),'<f4').reshape(-1,3)if n!='ACA falcine branch right'else v
 source={face_key(v[t])for t in f};origins={face_key(predicted[t]):{tuple(predicted[i]):v[i]for i in t}for t in f};ids=[i for i,t in enumerate(g)if face_key(p[t])not in source];new=p[g[ids]].astype(float);matched=[];old=[];fresh=[]
 for i,t in enumerate(new):
  r=origins.get(face_key(t))
  if r:matched.append(i);old.append([r[tuple(x)]for x in t])
  else:fresh.append(i)
 aa=samples(np.array(old));bb=samples(new[matched]);freshsamples=samples(new[fresh])if fresh else np.empty((0,3));lo=np.minimum(new.min((0,1)),aa.min(0))if len(aa)else new.min((0,1));hi=np.maximum(new.max((0,1)),aa.max(0))if len(aa)else new.max((0,1));print('DEPTH',n,len(ids),'new topology faces',len(fresh),flush=True)
 for other in scene.nearby(lo,hi):
  if scene.systems[other]not in ['brain','bone']or any(x in other for x in ['.falx-','.tentorium-','.petroclinoid-']):continue
  top=scene.volume_topology(other);sd=distance(other);w,h=scene.mesh(other)
  if not top['closedOrientedManifold']:
   distances=np.abs(sample_dist(sd,new[:,0]));radius=np.linalg.norm(new-new[:,:1],axis=2).max(1);margin=distances-radius;row={'node':n,'other':other,'method':'open-target-empty-ball','minimumClearanceMarginMm':float(margin.min()),'passed':bool(margin.min()>1e-5),'absoluteInsideCertified':False}
   if not row['passed']:issues.append(row)
  else:
   before=sample_dist(sd,aa);after=sample_dist(sd,bb);added=sample_dist(sd,freshsamples)if len(freshsamples)else np.array([]);newin=(before>=-1e-5)&(after< -1e-5);deeper=np.maximum(np.minimum(before,0)-np.minimum(after,0),0);normalcheck=np.r_[after,added];enclosed=enclosed_samples(w,h,np.vstack([bb,freshsamples]));inconsistent=int(np.sum((enclosed!=(normalcheck<0))&(np.abs(normalcheck)>1e-4)));row={'node':n,'other':other,'method':'paired-signed-depth-and-closed-volume-check','pairedSamples':len(aa),'newTriangleSamples':len(added),'insideBefore':int(sum(before<0)),'insideAfter':int(sum(after<0)),'maximumDepthBeforeMm':float(max(0,-before.min()))if len(before)else 0,'maximumDepthAfterMm':float(max(0,-after.min()))if len(after)else 0,'newInsideSamples':int(sum(newin)),'maximumExtraDepthMm':float(deeper.max())if len(deeper)else 0,'newTriangleInsideSamples':int(sum(added< -1e-5)),'signedAndEnclosedDisagreements':inconsistent};row['passed']=bool(not row['newInsideSamples']and row['maximumExtraDepthMm']<=.001 and not row['newTriangleInsideSamples']and not inconsistent)
   if not row['passed']:issues.append(row)
  rows.append(row)
  if not row['passed']or row.get('insideBefore')or row.get('insideAfter'):print(row,flush=True)
(T/'depth-validation.json').write_text(json.dumps({'passed':not issues,'issues':issues,'targets':rows,'scope':'No new sampled entry or extra depth over 0.001 mm at existing cortical embeddings. New triangles must remain outside closed neural/bone targets; open targets require conservative surface separation. Existing remote embeddings remain unresolved.'},indent=2)+'\n');print('PASS',not issues,flush=True)

sys.exit(0 if not issues else 1)
