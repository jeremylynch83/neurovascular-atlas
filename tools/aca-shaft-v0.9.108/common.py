from pathlib import Path
import sys,json,hashlib,numpy as np
import vtk
from vtk.util.numpy_support import numpy_to_vtk,numpy_to_vtkIdTypeArray,vtk_to_numpy
A=Path(__file__).resolve().parents[2];sys.path.insert(0,str(A/'tools/repair'))
from cache import Scene
from geometry import edge_table,cycles
W=Path(sys.argv[1]).resolve();CACHE=Path(sys.argv[2]).resolve();baseline_overrides={}
for p in (W/'decoded').glob('*.positions.bin'):
 n=p.name[:-len('.positions.bin')];q=W/'decoded'/(n+'.indices.bin');baseline_overrides[n]={'positions':str(p),'indices':str(q),'positionSha256':hashlib.sha256(p.read_bytes()).hexdigest(),'indicesSha256':hashlib.sha256(q.read_bytes()).hexdigest()}
scene=Scene(A,CACHE,baseline_overrides)
def poly(v,f):
 p=vtk.vtkPolyData();pts=vtk.vtkPoints();pts.SetData(numpy_to_vtk(v.astype(float),deep=True));p.SetPoints(pts);c=vtk.vtkCellArray();c.SetCells(len(f),numpy_to_vtkIdTypeArray(np.c_[np.full(len(f),3),f].astype(np.int64).ravel(),deep=True));p.SetPolys(c);return p
def distance(n):
 d=vtk.vtkImplicitPolyDataDistance();d.SetInput(poly(*scene.mesh(n)));return d
