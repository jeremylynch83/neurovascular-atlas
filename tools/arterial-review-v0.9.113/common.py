from pathlib import Path
import sys,json,numpy as np
import vtk
from vtk.util.numpy_support import numpy_to_vtk,numpy_to_vtkIdTypeArray,vtk_to_numpy
A=Path(__file__).resolve().parents[2];W=Path(sys.argv[1]).resolve();W.mkdir(parents=True,exist_ok=True);CACHE=Path(sys.argv[2]).resolve();sys.path.insert(0,str(A/'tools/repair'))
from check_deferred import check_assets
registry=json.load(open(A/'anatomy/source/arterial-review-v0.9.113/deferred-repairs.json'))
if check_assets(A,registry):raise ValueError('Source asset hashes changed. This recorded search requires its v0.9.112 baseline, also retained in v0.9.113.')
from cache import Scene,BVH
from geometry import edge_table,cycles,triangle_crosses
scene=Scene(A,CACHE)
def poly(v,f):
 out=vtk.vtkPolyData();p=vtk.vtkPoints();p.SetData(numpy_to_vtk(np.asarray(v,float),deep=True));out.SetPoints(p);c=vtk.vtkCellArray();c.SetCells(len(f),numpy_to_vtkIdTypeArray(np.c_[np.full(len(f),3),f].astype(np.int64).ravel(),deep=True));out.SetPolys(c);return out
