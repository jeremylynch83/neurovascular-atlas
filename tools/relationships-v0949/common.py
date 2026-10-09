from pathlib import Path
import sys,json,numpy as np,vtk
from vtk.util.numpy_support import numpy_to_vtk,numpy_to_vtkIdTypeArray,vtk_to_numpy
from scipy.spatial import cKDTree
WORK=Path(sys.argv[1]).resolve();DATA=WORK/'decoded';OUT=WORK/'candidate';OUT.mkdir(exist_ok=True)
META=json.loads((DATA/'meshes.json').read_text());FILES={r['name']:r['file'] for r in META}
cache={}
def load(name,directory=DATA):
 p=directory/(name+'.positions.bin');f=directory/(name+'.indices.bin')
 return np.fromfile(p,'<f4').reshape(-1,3).astype(float),np.fromfile(f,'<u4').reshape(-1,3)
def poly(v,f):
 p=vtk.vtkPolyData();pts=vtk.vtkPoints();pts.SetData(numpy_to_vtk(v,deep=True));p.SetPoints(pts);c=vtk.vtkCellArray();c.SetCells(len(f),numpy_to_vtkIdTypeArray(np.c_[np.full(len(f),3),f].astype(np.int64).ravel(),deep=True));p.SetPolys(c);return p
def normals(v,f):
 n=vtk.vtkPolyDataNormals();n.SetInputData(poly(v,f));n.SplittingOff();n.ConsistencyOn();n.Update();return vtk_to_numpy(n.GetOutput().GetPointData().GetNormals())
def contacts(v,f,w,g):
 c=vtk.vtkCollisionDetectionFilter();c.SetInputData(0,poly(v,f));c.SetInputData(1,poly(w,g));t=vtk.vtkTransform();c.SetTransform(0,t);c.SetTransform(1,t);c.SetCollisionModeToHalfContacts();c.SetCellTolerance(1e-7);c.Update();return c.GetNumberOfContacts()
def locator(v,f):
 l=vtk.vtkStaticCellLocator();l.SetDataSet(poly(v,f));l.BuildLocator();return l
def closest(l,pts):
 out=[];ds=[];cp=[0.,0.,0.];cid=vtk.reference(0);sub=vtk.reference(0);d2=vtk.reference(0.)
 for p in pts:l.FindClosestPoint(p,cp,cid,sub,d2);out.append(cp.copy());ds.append(float(d2)**.5)
 return np.array(out),np.array(ds)
def smooth(t):
 t=np.clip(t,0,1);return t*t*(3-2*t)
def section(v,f,axis,val):
 plane=vtk.vtkPlane();origin=[0,0,0];origin[axis]=val;normal=[0,0,0];normal[axis]=1;plane.SetOrigin(origin);plane.SetNormal(normal);c=vtk.vtkCutter();c.SetInputData(poly(v,f));c.SetCutFunction(plane);c.Update();p=c.GetOutput();return vtk_to_numpy(p.GetPoints().GetData()) if p.GetNumberOfPoints() else np.empty((0,3))
def write(name,v,f):
 v.astype('<f4').tofile(OUT/(name+'.positions.bin'));f.astype('<u4').tofile(OUT/(name+'.indices.bin'));normals(v,f).astype('<f4').tofile(OUT/(name+'.normals.bin'))
