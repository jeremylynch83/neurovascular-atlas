from pathlib import Path
import sys,json,numpy as np,vtk,trimesh
from scipy.spatial import cKDTree
from vtk.util.numpy_support import numpy_to_vtk,numpy_to_vtkIdTypeArray
A=Path(__file__).resolve().parents[2];sys.path.insert(0,str(A/'tools/foramina'));from geometry import Glb
M=json.load(open(A/'public/anatomy/manifest.json'));g=Glb(A/'public/anatomy/models/craniofacial.glb');loc={};meshes={};C=json.load(open(A/'anatomy/source/foramina/small-canals.json'));rows={r['id']:r for r in M['structures']}
for s in M['structures']:
 if s.get('asset',{}).get('file')!='models/craniofacial.glb':continue
 p,f,n=g.mesh(s['asset']['node']);meshes[s['id']]=(p,f,n);pts=vtk.vtkPoints();pts.SetData(numpy_to_vtk(p,deep=True));ca=vtk.vtkCellArray();ca.SetCells(len(f),numpy_to_vtkIdTypeArray(np.c_[np.full(len(f),3),f].ravel().astype('int64'),deep=True));pd=vtk.vtkPolyData();pd.SetPoints(pts);pd.SetPolys(ca);l=vtk.vtkOBBTree();l.SetDataSet(pd);l.BuildLocator();loc[s['id']]=l
def hits(a,b,names=None):
 result=[]
 for sid in (names or loc):
  pp=vtk.vtkPoints();loc[sid].IntersectWithLine(a,b,pp,None)
  for j in range(pp.GetNumberOfPoints()):result.append((sid,np.array(pp.GetPoint(j))))
 return result
report={'release':M['release'],'olfactoryPerforations':[],'openNotches':[],'carriedPassages':[]}
for side in ['right','left']:
 for h in C['cribriform.'+side]['holes']:
  a,b=np.array(h['course']);blocked=hits(a,b);assert not blocked,(h['id'],'blocked',blocked);z=h['roofZ']-.45;t=(z-a[2])/(b[2]-a[2]);centre=a+t*(b-a);tan=(b-a)/np.linalg.norm(b-a);u=np.cross(tan,[0,1,0]);u/=np.linalg.norm(u);v=np.cross(tan,u);dist=[]
  for angle in np.arange(16)*np.pi/8:
   d=np.cos(angle)*u+np.sin(angle)*v;hh=hits(centre,centre+d*2,['bone.ethmoid']);dist.append(min([np.linalg.norm(p-centre)for _,p in hh],default=None))
  assert all(d is not None for d in dist),(h['id'],'unbounded wall',dist)
  assert min(dist)>h['radiusMm']*.97,(h['id'],'undersize',dist)
  q=[centre[0],centre[1],56.5];out=[centre[0],12.0,56.5];assert not hits(a,q),(h['id'],'blocked subplate');assert not hits(q,out),(h['id'],'no nasal communication',hits(q,out));report['olfactoryPerforations'].append({'id':h['id'],'clearThroughAxis':True,'boundedRays':16,'minimumSampledRadiusMm':min(dist),'maximumSampledRadiusMm':max(dist),'nasalCommunicationClear':True})
 for family in ['supraorbital','supratrochlear']:
  rec=C[family+'.'+side];centre=np.array(rec['point']);route=np.array(rec['course']);i=np.argmin(np.linalg.norm(route-centre,axis=1));i=np.clip(i,1,len(route)-2);tan=route[i+1]-route[i-1];tan/=np.linalg.norm(tan);u=np.cross(tan,[1,0,0]);u/=np.linalg.norm(u);v=np.cross(tan,u);dd=[]
  for angle in np.arange(32)*np.pi/16:
   d=np.cos(angle)*u+np.sin(angle)*v;hh=hits(centre,centre+d*5,['bone.frontal']);dd.append(min([np.linalg.norm(p-centre)for _,p in hh],default=None))
  bounded=sum(x is not None for x in dd);assert 0<bounded<32,(family,side,'not an open bounded notch',bounded);report['openNotches'].append({'id':family+'.'+side,'boundedDirections':bounded,'openDirections':32-bounded,'point':centre.tolist()})
r=rows['landmark.superior-alveolar.left'];assert r['landmark']['status']=='visible';p=r['landmark']['course']
for a,b in zip(p,p[1:]):assert not hits(a,b),(r['id'],'blocked',hits(a,b))
report['carriedPassages'].append({'id':r['id'],'clearCentreline':True})
(A/'docs/foramina-batch7-passage-validation.json').write_text(json.dumps(report,indent=2));print(json.dumps(report,indent=2))
