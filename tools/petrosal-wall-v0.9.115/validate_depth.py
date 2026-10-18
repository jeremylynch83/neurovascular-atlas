"""Paired source/candidate tissue-depth gate, including every changed face and its edges."""
from common import *
from regional_validation import enclosed_samples
from clearance import certify

def validate(spec):
 n=spec['node'];v,f=scene.mesh(n);p=np.fromfile(W/'replayed'/(n+'.positions.bin'),'<f4').reshape(-1,3);ids=np.flatnonzero(np.any(np.any(p[f]!=v[f],axis=2),axis=1));a=v[f[ids]].astype(float);b=p[f[ids]].astype(float)
 def samples(t):return np.vstack([t.reshape(-1,3),t.mean(1),((t+np.roll(t,-1,axis=1))/2).reshape(-1,3)])
 def query(sd,pts):
  data=vtk.vtkPolyData();vp=vtk.vtkPoints();vp.SetData(numpy_to_vtk(pts.astype(float),deep=True));data.SetPoints(vp);op=vtk.vtkSampleImplicitFunctionFilter();op.SetInputData(data);op.SetImplicitFunction(sd);op.ComputeGradientsOff();op.Update();return vtk_to_numpy(op.GetOutput().GetPointData().GetScalars()).copy()
 aa=samples(a);bb=samples(b);core=(aa[:,1]>=spec['coreY'][0])&(aa[:,1]<=spec['coreY'][1]);lo=np.minimum(a.min((0,1)),b.min((0,1)));hi=np.maximum(a.max((0,1)),b.max((0,1)));rows=[];issues=[]
 for other in scene.nearby(lo,hi):
  if scene.systems[other]not in ['brain','bone']:continue
  w,g=scene.mesh(other);sd=distance(other);top=scene.volume_topology(other)
  if top['closedOrientedManifold']:
   before=query(sd,aa);after=query(sd,bb);enclosed=enclosed_samples(w,g,bb);disagreement=int(np.sum((enclosed!=(after<0))&(np.abs(after)>1e-4)));extra=np.maximum(np.minimum(before,0)-np.minimum(after,0),0);newinside=int(((before>=-1e-5)&(after< -1e-5)).sum());row={'target':other,'method':'paired-signed-depth-and-closed-volume-parity','samples':len(aa),'insideBefore':int((before< -1e-5).sum()),'insideAfter':int((after< -1e-5).sum()),'maximumDepthBeforeMm':float(max(0,-before.min())),'maximumDepthAfterMm':float(max(0,-after.min())),'newInsideSamples':newinside,'maximumExtraDepthMm':float(extra.max()),'signedAndEnclosedDisagreements':disagreement,'coreInsideBefore':int((before[core]< -1e-5).sum()),'coreInsideAfter':int((after[core]< -1e-5).sum()),'coreMaximumDepthBeforeMm':float(max(0,-before[core].min())),'coreMaximumDepthAfterMm':float(max(0,-after[core].min()))};row['passed']=not newinside and row['maximumExtraDepthMm']<=spec['depthToleranceMm']and not disagreement
  else:
   distances=np.abs(query(sd,b[:,0]));radius=np.linalg.norm(b-b[:,:1],axis=2).max(1);margin=distances-radius;row={'target':other,'method':'open-target-empty-ball-separation','minimumClearanceMarginMm':float(margin.min()),'passed':bool(margin.min()>1e-5),'absoluteInsideCertified':False}
   if not row['passed']:
    refined=certify(b,lambda points:np.abs(query(sd,points)));row={'target':other,'method':'adaptive-open-target-empty-ball-separation','coarseMinimumClearanceMarginMm':float(margin.min()),'absoluteInsideCertified':False,**refined}
  rows.append(row)
  if not row['passed']:issues.append(row)
  if row.get('insideBefore')or not row['passed']:print(row,flush=True)
 report={'release':'0.9.115','passed':not issues,'node':n,'changedFaces':len(ids),'sampleDefinition':'All source/candidate changed-face corners, three edge midpoints and centroid, with matching original barycentric samples.','coreSourceY':spec['coreY'],'targets':rows,'issues':issues,'scope':'No new sampled entry, no extra depth over 0.001 mm, and signed-distance/parity agreement. Open targets require conservative empty-ball separation. Regional petrosal anatomy and full receiving lumens remain unresolved.'}
 return report

rows=[validate(s)for s in json.load(open(W/'spec.json'))['changes']]
report={'release':'0.9.115','passed':all(r['passed']for r in rows),'changes':rows}
(W/'depth-validation.json').write_text(json.dumps(report,indent=2)+'\n');assert report['passed']
