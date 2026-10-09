"""Utilities for the v0.9.46 anterior brainstem venous placement audit."""
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
def shift(v, amount=1.2):
    # A common spatial field keeps identical collar vertices identical.
    # Full translation over the median vessels, smoothly tapering into branches.
    x,y,z=v.T
    w=smooth((x+5)/5)*(1-smooth((x-4.5)/3.5))*smooth((y+90)/5)*(1-smooth((y+52)/8))
    w*=smooth((z+34)/9)*(1-smooth((z-78)/8))
    lower=1-smooth((z-39)/4)
    dx=(amount+.5*lower)*(1-smooth((z-70)/5))
    dx-=.7*np.exp(-((z-65.7)/3.2)**4)
    dx-=.7*np.maximum(np.exp(-((z-45.5)/4.5)**4),np.exp(-((z-50.4)/3.5)**4))
    dy=.8*lower
    dy+=.7*np.exp(-((z-31)/3.5)**4-((x-4)/5)**4-((y+74)/5)**4)
    dy+=1.5*np.exp(-((z-34)/7)**4-((x-5.5)/2.4)**4-((y+76.5)/5.5)**4)
    dy+=.65*np.exp(-((z-56)/2)**4-((x-.5)/4.5)**4-((y+60)/4)**4)
    dy+=1.5*np.exp(-((z-63)/2)**4-((x-3)/4)**4-((y+59.5)/4)**4)
    dx-=1.4*np.exp(-((z-27.6)/2.1)**4-((x-5.1)/1.4)**4-((y+77)/4)**4)
    q=v.copy(); q[:,0]-=dx*w; q[:,1]+=dy*w
    # Apply the clival clearance as a monotone second map. Its y derivative
    # stays positive; a narrow single-step compression would fold the arch.
    q[:,1]-=.8*np.exp(-((x-.4)/4)**4-((z-55.6)/2.5)**4)*smooth((q[:,1]+59)/2)*w
    return q
def normals(v,f):
    n=vtk.vtkPolyDataNormals(); n.SetInputData(poly(v,f)); n.SplittingOff(); n.ConsistencyOn(); n.Update()
    return vtk_to_numpy(n.GetOutput().GetPointData().GetNormals())
