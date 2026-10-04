import json
from pathlib import Path
import numpy as np
import vtk
from vtk.util.numpy_support import numpy_to_vtk, numpy_to_vtkIdTypeArray, vtk_to_numpy
APP=Path(__file__).resolve().parents[2]
ROOT=APP/'.authoring/venous'
records=json.loads((ROOT/'reference.json').read_text())
def arrays(rec):
 p=np.memmap(ROOT/'reference.bin',dtype='<f4',mode='r',offset=rec['positionOffset'],shape=(rec['vertices'],3))
 f=np.memmap(ROOT/'reference.bin',dtype='<u4',mode='r',offset=rec['indexOffset'],shape=(rec['indices']//3,3))
 return np.array(p),np.array(f)
def poly(p,f):
 out=vtk.vtkPolyData();points=vtk.vtkPoints();points.SetData(numpy_to_vtk(p.astype(float),deep=True));out.SetPoints(points)
 ca=vtk.vtkCellArray();ca.SetCells(len(f),numpy_to_vtkIdTypeArray(np.c_[np.full(len(f),3),f].astype(np.int64).ravel(),deep=True));out.SetPolys(ca);return out
def actor(pd,col=(.7,.7,.6),opacity=1):
 mapper=vtk.vtkPolyDataMapper();mapper.SetInputData(pd);mapper.ScalarVisibilityOff();a=vtk.vtkActor();a.SetMapper(mapper);a.GetProperty().SetColor(*col);a.GetProperty().SetOpacity(opacity);return a
def bone_surface():
 app=vtk.vtkAppendPolyData()
 for r in records:
  if r['name'] in ['bone.frontal','bone.parietal.left','bone.parietal.right','bone.occipital','bone.temporal.left','bone.temporal.right','bone.sphenoid']:
   app.AddInputData(poly(*arrays(r)))
 app.Update();return app.GetOutput()
def locator(pd):
 t=vtk.vtkOBBTree();t.SetDataSet(pd);t.BuildLocator();return t
def hits(loc,a,b):
 p=vtk.vtkPoints();loc.IntersectWithLine(a,b,p,None);return np.array([p.GetPoint(i) for i in range(p.GetNumberOfPoints())])
def render(items,path,view=(1,0,0),center=(0,-65,55),scale=155):
 ren=vtk.vtkRenderer();ren.SetBackground(.06,.07,.085)
 win=vtk.vtkRenderWindow();win.SetOffScreenRendering(1);win.SetSize(1200,1200);win.SetMultiSamples(0);win.AddRenderer(ren)
 for pd,col,op in items:ren.AddActor(actor(pd,col,op))
 cam=ren.GetActiveCamera();cam.SetPosition(*(np.array(center)+np.array(view)*600));cam.SetFocalPoint(*center);cam.SetViewUp(*( (0,0,1) if abs(view[2])<.9 else (0,1,0) ));cam.ParallelProjectionOn();cam.SetParallelScale(scale)
 ren.ResetCameraClippingRange();win.Render();w=vtk.vtkWindowToImageFilter();w.SetInput(win);w.Update();png=vtk.vtkPNGWriter();png.SetFileName(str(path));png.SetInputConnection(w.GetOutputPort());png.Write();win.Finalize()
if __name__=='__main__':
 skull=bone_surface(); loc=locator(skull)
 for y,z in [(10,80),(20,110),(0,145),(-50,170),(-100,160),(-140,125),(-150,85),(-145,65),(-120,50)]:
  start=np.array([.65,-65,105]);target=np.array([.65,y,z]);h=hits(loc,start,start+3*(target-start));print('target',y,z,'hits',h.tolist())
 items=[(skull,(.85,.81,.7),.18)]
 for r in records:
  if r['file']=='complete-circulation' and any(w in r['name'] for w in ['ICA cavernous','PCA P2','Basilar','ACA A','Vertebral V']):items.append((poly(*arrays(r)),(.9,.35,.25),1))
 render(items,ROOT/'reference-right.png',center=(0,-65,70),scale=115)
