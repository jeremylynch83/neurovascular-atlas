from pathlib import Path
import sys,json,numpy as np
R=Path('/workspace/scratch/3da1329b983b');A=R/'atlas/inr-anatomy-atlas-v0.9.91';W=R/'batch17-work';sys.path.insert(0,str(A/'tools/repair'))
from cache import Scene
from geometry import edge_table,cycles
import vtk
from vtk.util.numpy_support import numpy_to_vtk,numpy_to_vtkIdTypeArray,vtk_to_numpy
scene=Scene(A,R/'repair-benchmark-final/cache')
def poly(v,f):
 out=vtk.vtkPolyData();p=vtk.vtkPoints();p.SetData(numpy_to_vtk(np.asarray(v,float),deep=True));out.SetPoints(p);c=vtk.vtkCellArray();c.SetCells(len(f),numpy_to_vtkIdTypeArray(np.c_[np.full(len(f),3),f].astype(np.int64).ravel(),deep=True));out.SetPolys(c);return out
