from pathlib import Path
import numpy as np,json,vtk,sys
from vtk.util.numpy_support import numpy_to_vtk,numpy_to_vtkIdTypeArray
A=Path(__file__).resolve().parents[2];B=A/'docs';sys.path.insert(0,str(A/'tools/foramina'));from geometry import Glb
M=json.load(open(A/'public/anatomy/manifest.json'));g=Glb(A/'public/anatomy/models/craniofacial.glb');loc={};C=json.load(open(A/'anatomy/source/foramina/facial-canals.json'))
for s in M['structures']:
 if s.get('asset',{}).get('file')!='models/craniofacial.glb':continue
 p,f,n=g.mesh(s['asset']['node']);pts=vtk.vtkPoints();pts.SetData(numpy_to_vtk(p,deep=True));ca=vtk.vtkCellArray();ca.SetCells(len(f),numpy_to_vtkIdTypeArray(np.c_[np.full(len(f),3),f].ravel().astype('int64'),deep=True));pd=vtk.vtkPolyData();pd.SetPoints(pts);pd.SetPolys(ca);l=vtk.vtkOBBTree();l.SetDataSet(pd);l.BuildLocator();loc[s['id']]=l
report=[]
for side in ['right','left']:
 for family,stationKey,stations in [('mandibular-canal',1,[-34,-25,-15,-3]),('mandibular-incisive',0,[12 if side=='right'else-12,4 if side=='right'else-4]),('infraorbital-canal',1,[1,5,9]),('nasolacrimal',2,[47,42,37])]:
  p=np.array(C[side][family]['course']);names=['bone.mandible','bone.mandibular-alveolar-process']if family.startswith('mandibular')else['bone.maxilla.'+side,'bone.lacrimal.'+side,'bone.inferior_nasal_concha.'+side]
  for station in stations:
   i=np.argmin(abs(p[:,stationKey]-station));i=np.clip(i,1,len(p)-2);centre=p[i];tan=p[i+1]-p[i-1];tan/=np.linalg.norm(tan);u=np.cross(tan,[0,0,1]if abs(tan[2])<.8 else[0,1,0]);u/=np.linalg.norm(u);v=np.cross(tan,u);rays=[]
   for angle in np.arange(16)*2*np.pi/16:
    d=np.cos(angle)*u+np.sin(angle)*v;dist=[]
    for name in names:
     hits=vtk.vtkPoints();loc[name].IntersectWithLine(centre,centre+d*5,hits,None)
     for j in range(hits.GetNumberOfPoints()):
      dd=np.linalg.norm(np.array(hits.GetPoint(j))-centre)
      if dd>1e-5:dist.append(float(dd))
    rays.append(min(dist,default=None))
   r={'side':side,'family':family,'station':station,'centre':centre.tolist(),'boundedRays':sum(x is not None for x in rays),'distancesMm':rays};report.append(r);print(r,flush=True)
assert all(r['boundedRays']==16 for r in report),'A sampled core lacks a surrounding wall'
(B/'foramina-batch6-section-validation.json').write_text(json.dumps(report,indent=2))
