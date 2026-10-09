"""Utilities for the v0.9.48 anterior brainstem venous placement audit."""
from pathlib import Path
import json, sys
import numpy as np
import vtk
from vtk.util.numpy_support import numpy_to_vtk, numpy_to_vtkIdTypeArray, vtk_to_numpy
WORK = Path(sys.argv[1]).resolve()
DATA = WORK / 'decoded'
OUT = WORK / 'candidate'
OUT.mkdir(exist_ok=True)
META = json.loads((DATA / 'meshes.json').read_text())
MEDIAN = ['vein.anterior_pontomesencephalic', 'vein.anterior_pontine',
          'vein.anterior_medullary', 'vein.anterior_spinal']
def load(name, directory=DATA):
    return (np.fromfile(directory / (name+'.positions.bin'), '<f4').reshape(-1,3),
            np.fromfile(directory / (name+'.indices.bin'), '<u4').reshape(-1,3))
def poly(v,f):
    p=vtk.vtkPolyData(); points=vtk.vtkPoints()
    points.SetData(numpy_to_vtk(v.astype(float),deep=True)); p.SetPoints(points)
    cells=vtk.vtkCellArray()
    cells.SetCells(len(f),numpy_to_vtkIdTypeArray(np.c_[np.full(len(f),3),f].astype(np.int64).ravel(),deep=True))
    p.SetPolys(cells); return p
def contacts(a,b):
    c=vtk.vtkCollisionDetectionFilter(); c.SetInputData(0,a); c.SetInputData(1,b)
    t=vtk.vtkTransform(); c.SetTransform(0,t); c.SetTransform(1,t)
    c.SetCollisionModeToHalfContacts(); c.SetCellTolerance(1e-7); c.Update()
    return c.GetNumberOfContacts()
def combine(names):
    a=vtk.vtkAppendPolyData()
    for name in names: a.AddInputData(poly(*load(name)))
    a.Update(); return a.GetOutput()
def smooth(t):
    t=np.clip(t,0,1); return t*t*(3-2*t)
def vein_shift(v):
    from scipy.interpolate import PchipInterpolator
    x,y,z=v.T
    stations=[-10,-8,-7,-6,-4,-3,-2,-1,0,.5,1,1.5,2,2.8,4]
    offsets=[0,0,0,-.8,-4.3,-6.5,-7.,-6.6,-6.3,-4.8,-4.5,-2.3,-1.2,0,0]
    delta=PchipInterpolator(stations,offsets)(np.clip(x,stations[0],stations[-1]))
    delta=np.where((x>=1.5)&(x<=2),-2.3+2.2*(x-1.5),delta)
    wz=smooth((z-52)/1.8)*(1-smooth((z-56.8)/.4))
    q=v.copy();q[:,1]+=delta*wz
    return q
def brain_shift(v):
    x,y,z=v.T
    wx=smooth((x+9)/5)*(1-smooth((x-1)/5))
    wy=smooth((y+77)/10)*(1-smooth((y+60)/4))
    wz=smooth((z-51.8)/2)*(1-smooth((z-58.5)/2.5))
    q=v.copy();q[:,1]-=3.5*wx*wy*wz
    return q
def normals(v,f):
    n=vtk.vtkPolyDataNormals(); n.SetInputData(poly(v,f)); n.SplittingOff(); n.ConsistencyOn(); n.Update()
    return vtk_to_numpy(n.GetOutput().GetPointData().GetNormals())
