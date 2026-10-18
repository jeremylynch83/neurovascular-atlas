"""Certify the entire right A5 wall outside two closed posterior cortical bodies."""
from common import *
from clearance import certify
from regional_validation import enclosed_samples

def query(sd,points):
 data=vtk.vtkPolyData();vp=vtk.vtkPoints();vp.SetData(numpy_to_vtk(points.astype(float),deep=True));data.SetPoints(vp);op=vtk.vtkSampleImplicitFunctionFilter();op.SetInputData(data);op.SetImplicitFunction(sd);op.ComputeGradientsOff();op.Update();return vtk_to_numpy(op.GetOutput().GetPointData().GetScalars()).copy()
def samples(t):return np.vstack([t.reshape(-1,3),t.mean(1),((t+np.roll(t,-1,axis=1))/2).reshape(-1,3)])
n='ACA A5 right';v,f=scene.mesh(n);p=np.fromfile(W/'replayed'/(n+'.positions.bin'),'<f4').reshape(-1,3);old=v[f].astype(float);new=p[f].astype(float);source_samples=samples(old);candidate_samples=samples(new);centres=new.mean(1);rows=[]
for target in ['brain.cingulate-gyrus-and-sulcus-posterior-dorsal-part.right','brain.cingulate-gyrus-posteroventral-part.right']:
 assert scene.volume_topology(target)['closedOrientedManifold'];sd=distance(target);w,g=scene.mesh(target);before=query(sd,source_samples);after=query(sd,candidate_samples);signed=query(sd,centres);enclosed=enclosed_samples(w,g,centres);disagreements=int(((enclosed!=(signed<0))&(np.abs(signed)>1e-4)).sum());proof=certify(new,lambda points:query(sd,points));row={'node':n,'target':target,'targetClosedAndOriented':True,'method':'positive-signed-distance-enclosing-balls-over-every-source-face','wholeLabelSamples':len(before),'insideBefore':int((before< -1e-5).sum()),'insideAfter':int((after< -1e-5).sum()),'maximumDepthBeforeMm':float(max(0,-before.min())),'maximumDepthAfterMm':float(max(0,-after.min())),'signedAndEnclosedCentreDisagreements':disagreements,'proof':proof,'passed':proof['passed']and not disagreements and not np.any(after< -1e-5)};rows.append(row);print(row,flush=True)
report={'release':'0.9.111','passed':all(r['passed']for r in rows),'node':n,'wallTrianglesCheckedPerTarget':len(f),'targets':rows,'scope':'Continuous numerical separation from the two named closed surfaces only, across the complete A5 wall. Bound margins are conservative certificates, not measured anatomical clearances. Other ACA/cortical relationships remain open.'};(W/'full-clearance-validation.json').write_text(json.dumps(report,indent=2)+'\n');assert report['passed']
