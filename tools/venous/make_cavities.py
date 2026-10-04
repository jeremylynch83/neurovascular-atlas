"""Local geometric exclusion masks for the cavernous sinus authoring envelope."""
import numpy as np
import manifold3d as mf
import vtk
from vtk.util.numpy_support import vtk_to_numpy
from reference import ROOT,records,arrays,poly
def export_field(function,lo,hi,step,name):
 sample=vtk.vtkSampleFunction();sample.SetImplicitFunction(function);sample.SetModelBounds(*np.column_stack([lo,hi]).ravel());sample.SetSampleDimensions(*np.ceil((hi-lo)/step).astype(int));sample.ComputeNormalsOff();sample.Update()
 im=sample.GetOutput();v=vtk_to_numpy(im.GetPointData().GetScalars()).reshape(im.GetDimensions()[::-1]);v[[0,-1],:,:]=10;v[:,[0,-1],:]=10;v[:,:,[0,-1]]=10
 contour=vtk.vtkFlyingEdges3D();contour.SetInputData(im);contour.SetValue(0,.3 if name.startswith('ica') else .35);contour.Update();pd=contour.GetOutput()
 p=vtk_to_numpy(pd.GetPoints().GetData()).astype(np.float32);f=vtk_to_numpy(pd.GetPolys().GetData()).reshape(-1,4)[:,1:].astype(np.uint32);m=mf.Manifold(mf.Mesh(p,f));assert m.status()==mf.Error.NoError
 if m.volume()<0:f=f[:,[0,2,1]]
 np.savez_compressed(ROOT/(name+'.npz'),positions=p,faces=f);print(name,len(f),flush=True)
for side in ['right','left']:
 rec=next(r for r in records if r['name']=='ICA cavernous '+side);p,f=arrays(rec);sdf=vtk.vtkImplicitPolyDataDistance();sdf.SetInput(poly(p,f))
 export_field(sdf,p.min(0)-.8,p.max(0)+.8,.28,'ica-cavity-'+side)
 union=vtk.vtkImplicitBoolean();union.SetOperationTypeToUnion()
 for rec in records:
  if rec['name'] in ['bone.sphenoid','bone.temporal.'+side]:
   sdf=vtk.vtkImplicitPolyDataDistance();sdf.SetInput(poly(*arrays(rec)));union.AddFunction(sdf)
 lo=np.array([4 if side=='right' else -26,-59,43]);hi=np.array([27 if side=='right' else -2,-28,81])
 export_field(union,lo,hi,.35,'cavernous-bone-'+side)
