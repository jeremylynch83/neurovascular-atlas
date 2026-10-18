from repair import *
from vtk.util.numpy_support import numpy_to_vtk,vtk_to_numpy
surfaces=json.load(open(D.parent/'baseline-surface-recipes.json'));ids=surfaces['nodeIds']
def closed(n):
 v,f=mesh(n);r=surfaces['entries'][ids[n]];verts=np.vstack([v,r['extra']]);removed=set(r['removed']);flips=set(r['flips']);faces=np.array([t[::-1]if(r['reverse']!=(i in flips))else t for i,t in enumerate(f)if i not in removed]);native=len(faces);faces=np.vstack([faces,np.array(r['caps']).reshape(-1,3)]);p=poly(verts,faces);arr=numpy_to_vtk(np.r_[np.ones(native,np.int32),np.zeros(len(faces)-native,np.int32)],deep=True);arr.SetName('Native');p.GetCellData().AddArray(arr);clean=vtk.vtkCleanPolyData();clean.SetInputData(p);clean.SetTolerance(0.);clean.Update();return clean.GetOutput()
if __name__=='__main__':
 for side in ['left','right']:
  parent='MMA frontal'+(' left'if side=='left'else'');child='MMA paramedian '+side;p=closed(parent);c=closed(child);op=vtk.vtkIntersectionPolyDataFilter();op.SetInputData(0,p);op.SetInputData(1,c);op.SplitFirstOutputOn();op.SplitSecondOutputOn();op.Update();print(side,'intersection',op.GetOutput(0).GetNumberOfPoints(),'status',op.GetStatus(),flush=True)
  for i in [1,2]:
   o=op.GetOutput(i);print('split',i,o.GetNumberOfPoints(),o.GetNumberOfCells(),'arrays',[o.GetCellData().GetArrayName(j)for j in range(o.GetCellData().GetNumberOfArrays())],flush=True)
   wr=vtk.vtkXMLPolyDataWriter();wr.SetFileName(str(D.parent/(side+'-split'+str(i)+'.vtp')));wr.SetInputData(o);wr.Write()
