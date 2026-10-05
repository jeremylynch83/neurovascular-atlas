"""Matched cross-section skin-envelope areas; not a segmented lumen test."""
import json
import numpy as np,trimesh,vtk
from scipy.spatial import ConvexHull
from vtk.util.numpy_support import vtk_to_numpy
from fit_vessels import APP
from build_targets import poly

def areas(m,axis,stations):
 data=poly(m);out=[]
 for station in stations:
  plane=vtk.vtkPlane();origin=np.zeros(3);origin[axis]=station;normal=np.zeros(3);normal[axis]=1;plane.SetOrigin(*origin);plane.SetNormal(*normal)
  cut=vtk.vtkCutter();cut.SetInputData(data);cut.SetCutFunction(plane);cut.Update();points=cut.GetOutput().GetPoints()
  if not points or points.GetNumberOfPoints()<3:out.append(None);continue
  p=vtk_to_numpy(points.GetData())[:,[k for k in range(3) if k!=axis]]
  out.append(float(ConvexHull(p).volume))
 return out

def main():
 rows=[]
 for asset,key,axis in [('veins','vein.straight',1),('arteries','Central left',2),('arteries','Central right',2)]:
  old=trimesh.load(APP/f'.authoring/{asset}-baseline.glb',process=False).geometry[key];new=trimesh.load(APP/f'.authoring/{asset}-fitted.glb',process=False).geometry[key]
  lo,hi=old.bounds[:,axis]
  lo,hi=lo+.15*(hi-lo),hi-.15*(hi-lo)
  if asset=='arteries':lo=max(lo,125)
  stations=np.linspace(lo,hi,35);before=areas(old,axis,stations);after=areas(new,axis,stations)
  ratio=np.array(after)/np.array(before)
  rows.append({'node':key,'axis':axis,'stationsMm':stations.tolist(),'beforeSkinEnvelopeAreaMm2':before,'afterSkinEnvelopeAreaMm2':after,'minimumAreaRatio':float(ratio.min()),'medianAreaRatio':float(np.median(ratio)),'maximumAreaRatio':float(ratio.max())})
 out={'release':'0.9.17','method':'Convex hull of the actual GLB skin intersection with matched station planes in the central 70% of the primary course. Cortical stations additionally exclude the proximal phase below z = 125 mm.','interpretation':'Cross-section envelope-area proxy, not an internal lumen segmentation or proof of patency. Matched plane areas also reflect changed vessel inclination. They must not be interpreted as direct lumen diameter ratios. Shared branch junctions and retained attachment collars require visual review.','checks':rows}
 (APP/'docs/validation/fitting-calibre-v0.9.17.json').write_text(json.dumps(out,indent=2)+'\n')
 print(json.dumps([{k:r[k] for k in ['node','minimumAreaRatio','medianAreaRatio','maximumAreaRatio']} for r in rows],indent=2))
if __name__=='__main__':main()
