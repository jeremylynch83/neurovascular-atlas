from pathlib import Path
import json
import numpy as np
import vtk
from vtk.util.numpy_support import numpy_to_vtk,numpy_to_vtkIdTypeArray,vtk_to_numpy
ROOT=Path(__file__).resolve().parents[3]/'fixes-work'
DATA=ROOT.parent/'audit-work/decoded'
def poly(v,f):
 pts=vtk.vtkPoints();pts.SetData(numpy_to_vtk(np.asarray(v,dtype=float),deep=True))
 cells=vtk.vtkCellArray();cells.SetCells(len(f),numpy_to_vtkIdTypeArray(np.c_[np.full(len(f),3),f].astype(np.int64).ravel(),deep=True))
 p=vtk.vtkPolyData();p.SetPoints(pts);p.SetPolys(cells);return p
class Mesh:
 def __init__(self,row):
  self.name=row['name'];self.file=row['file'];self.v=np.fromfile(DATA/(self.name+'.positions.bin'),'<f4').reshape(-1,3).astype(float);self.f=np.fromfile(DATA/(self.name+'.indices.bin'),'<u4').reshape(-1,3);self.new=self.v.copy();self._poly=None
 @property
 def pd(self):
  if self._poly is None:self._poly=poly(self.v,self.f)
  return self._poly
 @property
 def bounds(self):return np.array([self.v.min(0),self.v.max(0)])
meshes={r['name']:Mesh(r) for r in json.loads((DATA/'meshes.json').read_text())}
def combine(names,after=False):
 vv=[];ff=[];offset=0
 for k in names:
  m=meshes[k];v=m.new if after else m.v;vv.append(v);ff.append(m.f+offset);offset+=len(v)
 return poly(np.concatenate(vv),np.concatenate(ff))
def locator(pd):
 loc=vtk.vtkStaticCellLocator();loc.SetDataSet(pd);loc.BuildLocator();return loc

def ray(loc,x,z,lo=-150,hi=-25):
 pts=vtk.vtkPoints();ids=vtk.vtkIdList();loc.IntersectWithLine([x,lo,z],[x,hi,z],1e-7,pts,ids)
 return sorted([pts.GetPoint(i)[1] for i in range(pts.GetNumberOfPoints())])
def close(loc,p):
 q=[0.,0.,0.];ci=vtk.reference(0);sub=vtk.reference(0);d=vtk.reference(0.);loc.FindClosestPoint(p,q,ci,sub,d);return np.array(q),float(d)**.5

_triangle_cache={}
def triangle_data(pd):
 key=id(pd)
 if key not in _triangle_cache:
  v=vtk_to_numpy(pd.GetPoints().GetData());f=vtk_to_numpy(pd.GetPolys().GetData()).reshape(-1,4)[:,1:];tri=v[f];_triangle_cache[key]=(pd,v,f,tri.min(1),tri.max(1))
 return _triangle_cache[key][1:]
def crop(pd,lo,hi):
 v,f,tlo,thi=triangle_data(pd);keep=np.all(thi>=lo-1e-6,axis=1)&np.all(tlo<=hi+1e-6,axis=1)
 if not np.any(keep):return None
 if np.all(keep):return pd
 pts=pd.GetPoints();cells=vtk.vtkCellArray();selected=f[keep];cells.SetCells(len(selected),numpy_to_vtkIdTypeArray(np.c_[np.full(len(selected),3),selected].astype(np.int64).ravel(),deep=True));out=vtk.vtkPolyData();out.SetPoints(pts);out.SetPolys(cells);return out
def contacts(a,b,first=False):
 aa=np.array(a.GetBounds()).reshape(3,2);bb=np.array(b.GetBounds()).reshape(3,2)
 if np.any(aa[:,1]<bb[:,0]) or np.any(bb[:,1]<aa[:,0]):return 0
 lo=np.maximum(aa[:,0],bb[:,0]);hi=np.minimum(aa[:,1],bb[:,1]);a=crop(a,lo,hi);b=crop(b,lo,hi)
 if a is None or b is None:return 0
 coll=vtk.vtkCollisionDetectionFilter();coll.SetInputData(0,a);coll.SetInputData(1,b);t=vtk.vtkTransform();coll.SetTransform(0,t);coll.SetTransform(1,t);coll.SetBoxTolerance(0);coll.SetCellTolerance(1e-7);coll.SetNumberOfCellsPerNode(2)
 if first:coll.SetCollisionModeToFirstContact()
 else:coll.SetCollisionModeToHalfContacts()
 coll.Update();return coll.GetNumberOfContacts()

def smooth(x):
 x=np.clip(x,0,1);return x*x*(3-2*x)
