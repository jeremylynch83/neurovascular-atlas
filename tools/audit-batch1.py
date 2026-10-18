"""Read-only audit of the delivered, decoded RAS/mm surfaces."""
import sys,json,hashlib
from pathlib import Path
import numpy as np
from scipy.spatial import cKDTree
import vtk
from vtk.util.numpy_support import numpy_to_vtk,numpy_to_vtkIdTypeArray,vtk_to_numpy
ROOT=Path(sys.argv[1]).resolve(); DATA=ROOT/'decoded'
META=json.loads((DATA/'meshes.json').read_text()); cache={}
def load(n):
 if n not in cache:
  v=np.fromfile(DATA/(n+'.positions.bin'),'<f4').reshape(-1,3).astype(float);f=np.fromfile(DATA/(n+'.indices.bin'),'<u4').reshape(-1,3)
  p=vtk.vtkPolyData();pts=vtk.vtkPoints();pts.SetData(numpy_to_vtk(v,deep=True));p.SetPoints(pts);cells=vtk.vtkCellArray();cells.SetCells(len(f),numpy_to_vtkIdTypeArray(np.c_[np.full(len(f),3),f].astype(np.int64).ravel(),deep=True));p.SetPolys(cells)
  cache[n]=(v,f,p)
 return cache[n]
def contacts(a,b):
 av,af,ap=load(a);bv,bf,bp=load(b)
 if np.any(av.max(0)<bv.min(0)) or np.any(bv.max(0)<av.min(0)):return 0
 c=vtk.vtkCollisionDetectionFilter();c.SetInputData(0,ap);c.SetInputData(1,bp);t=vtk.vtkTransform();c.SetTransform(0,t);c.SetTransform(1,t);c.SetCollisionModeToHalfContacts();c.SetCellTolerance(1e-7);c.SetBoxTolerance(0);c.SetNumberOfCellsPerNode(2);c.Update();return c.GetNumberOfContacts()
def distance(a,b):
 v,_,_=load(a);_,_,p=load(b);loc=vtk.vtkStaticCellLocator();loc.SetDataSet(p);loc.BuildLocator();d=[];cp=[0.,0.,0.];cid=vtk.reference(0);sub=vtk.reference(0);d2=vtk.reference(0.)
 for q in v:loc.FindClosestPoint(q,cp,cid,sub,d2);d.append(float(d2)**.5)
 return {'minimumVertexToSurfaceMm':round(min(d),5),'medianVertexToSurfaceMm':round(float(np.median(d)),5)}
def pair(a,b):return {'a':a,'b':b,'surfaceContacts':contacts(a,b),**distance(a,b)}
def section(n,z):
 _,_,p=load(n);pl=vtk.vtkPlane();pl.SetOrigin(0,0,z);pl.SetNormal(0,0,1);c=vtk.vtkCutter();c.SetInputData(p);c.SetCutFunction(pl);c.Update();o=c.GetOutput();return vtk_to_numpy(o.GetPoints().GetData()) if o.GetNumberOfPoints() else np.empty((0,3))
def joins(a,b):
 v,f,_=load(a);w,_,_=load(b);d=cKDTree(w).query(v)[0];edges=np.sort(np.vstack([f[:,[0,1]],f[:,[1,2]],f[:,[2,0]]]),axis=1);e,c=np.unique(edges,axis=0,return_counts=True);boundary=np.unique(e[c==1]);matched=d<=1e-5
 return {'a':a,'parent':b,'sharedPositionVertices1e5Mm':int(matched.sum()),'boundaryVertices':len(boundary),'sharedBoundaryVertices1e5Mm':int(matched[boundary].sum()),**distance(a,b)}
PAIRS=[('Basilar','vein.anterior_pontomesencephalic'),('PCA P1 right','vein.lateral_mesencephalic.right'),('PCA P1 right','vein.posterior_communicating'),('PCA P2-P3 right','vein.posterior_communicating'),('Posterior communicating right','vein.posterior_communicating'),('SCA right','vein.anterior_pontomesencephalic'),('Thalamoperforator 2 right','vein.lateral_mesencephalic.right'),('Vertebral V4 left','vein.marginal'),('Vertebral V4 left','vein.pontomedullary.left'),('Vertebral V4 right','vein.anterior_medullary'),('Vertebral V4 right','vein.pontomedullary.right'),('Vertebral V4 right','vein.pontomedullary.left')]
report={'release':'0.9.83','units':'mm','coordinateSystem':'RAS','method':{'contacts':'VTK triangle/triangle half-contact count; tolerance 1e-7; count is not number of defects','distance':'All vertices of first surface to triangles of second surface; minimum is a sampled upper bound, not exact continuous clearance','sharedPositions':'Delivered positions within 1e-5 mm; proximity/shared coordinates alone do not prove an open lumen'},'assetHashes':json.loads((DATA/'source-assets.json').read_text()),'posteriorCrossings':[]}
for a,b in PAIRS:
 r=pair(a,b);report['posteriorCrossings'].append(r);print(r,flush=True)
depth=[]
for z in np.arange(40.,81.,5.):
 a=section('Basilar',z);b=section('vein.anterior_pontomesencephalic',z)
 if len(a) and len(b):depth.append({'zMm':z,'basilarMeanY':float(a[:,1].mean()),'veinMeanY':float(b[:,1].mean()),'veinMinusArteryY':float(b[:,1].mean()-a[:,1].mean())})
report['basilarVenousDepthSamples']=depth
report['pericallosal']=[]
targets=[m['name'] for m in META if m['name'].startswith('brain.') or m['name'].startswith('vein.')]
for side in ['left','right']:
 for seg in ['A2','A3','A4','A5']:
  n=f'ACA {seg} {side}';r={'vessel':n,'callosalDistance':distance(n,'brain.corpus-callosum'),'contacts':[]}
  for t in targets:
   c=contacts(n,t)
   if c:r['contacts'].append({'structure':t,'surfaceContacts':c})
  report['pericallosal'].append(r);print(r,flush=True)
report['pericallosalSeams']=[joins(f'ACA A{n} {side}',f'ACA A{n+1} {side}') for side in ['left','right'] for n in [2,3,4]]
report['falcineAttachments']=[]
for side in ['left','right']:
 for a,b in [('Anterior falcine','Anterior ethmoidal'),('MMA falcine terminal','MMA paramedian'),('ACA falcine branch','ACA A5'),('ACA falcine–MMA falcine','ACA falcine branch'),('ACA falcine–MMA falcine','MMA falcine terminal'),('Anterior falcine–MMA paramedian','Anterior falcine'),('Anterior falcine–MMA paramedian','MMA paramedian')]:
  r=joins(f'{a} {side}',f'{b} {side}');report['falcineAttachments'].append(r);print(r,flush=True)
report['falcineParentCandidates']=[joins('ACA falcine branch '+side,'ACA A'+str(n)+' '+side) for side in ['left','right'] for n in [2,3,4,5]]
(ROOT/'measurements.json').write_text(json.dumps(report,indent=2)+'\n')
