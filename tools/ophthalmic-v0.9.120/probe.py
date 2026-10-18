from pathlib import Path
import os,sys,json,numpy as np,vtk
from vtk.util.numpy_support import numpy_to_vtk,numpy_to_vtkIdTypeArray
A=Path(os.environ['ATLAS_BASELINE_ROOT']).resolve();W=Path(os.environ['ATLAS_ORBITAL_WORK']).resolve();R=W.parent;sys.path.insert(0,str(A/'tools/repair'))
from cache import Scene
scene=Scene(A,W/'cache')
def poly(v,f):
 p=vtk.vtkPolyData();q=vtk.vtkPoints();q.SetData(numpy_to_vtk(np.asarray(v,float),deep=True));p.SetPoints(q);c=vtk.vtkCellArray();c.SetCells(len(f),numpy_to_vtkIdTypeArray(np.c_[np.full(len(f),3),f].astype(np.int64).ravel(),deep=True));p.SetPolys(c);return p
def locator(v,f):
 l=vtk.vtkStaticCellLocator();l.SetDataSet(poly(v,f));l.BuildLocator();return l
def distance(l,p):
 q=[0.,0.,0.];a=vtk.reference(0);b=vtk.reference(0);d=vtk.reference(0.);l.FindClosestPoint(p,q,a,b,d);return float(d)**.5,q
if __name__=='__main__':
 for side,sign in [('right',1),('left',-1)]:
  pts=np.array([[29,-9,47.5],[28,-15,51],[25,-22,57],[23,-27,62],[21,-30.5,66]],float);pts[:,0]=pts[:,0] if sign==1 else -pts[:,0]+1.3
  for pt in pts:
   rows=[]
   for n in scene.nearby(pt-3,pt+3):
    if not scene.systems[n]in ['bone','artery','brain']:continue
    d,q=distance(locator(*scene.mesh(n)),pt)
    if d<3:rows.append([n,round(d,3),q])
   print(side,pt.tolist(),sorted(rows,key=lambda x:x[1]),flush=True)
 print(scene.stats,flush=True)
