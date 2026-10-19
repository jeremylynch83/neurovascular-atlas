"""Non-adjacent triangle contacts, retaining original face identifiers."""
import numpy as np,vtk
from vtk.util.numpy_support import vtk_to_numpy,numpy_to_vtk,numpy_to_vtkIdTypeArray

def contacts(p,f):
 centre=p[f].mean(1);mask=np.ones(len(f),dtype=bool);face_ids=np.where(mask)[0];f=f[mask]
 pts=vtk.vtkPoints();pts.SetData(numpy_to_vtk(p,deep=True));cells=vtk.vtkCellArray();cells.SetCells(len(f),numpy_to_vtkIdTypeArray(np.c_[np.full(len(f),3),f].ravel().astype('int64'),deep=True));o=vtk.vtkPolyData();o.SetPoints(pts);o.SetPolys(cells)
 c=vtk.vtkCollisionDetectionFilter();c.SetInputData(0,o);c.SetInputData(1,o);t=vtk.vtkTransform();t.Identity();c.SetTransform(0,t);c.SetTransform(1,t);c.SetCollisionModeToAllContacts();c.SetBoxTolerance(0);c.SetCellTolerance(0);c.SetNumberOfCellsPerNode(2);c.Update();a=vtk_to_numpy(c.GetContactCells(0));b=vtk_to_numpy(c.GetContactCells(1));sel=a<b;a=a[sel];b=b[sel];_,ix=np.unique(np.round(p,5),axis=0,return_inverse=True);uf=ix[f];sel=~(uf[a,:,None]==uf[b,None,:]).any((1,2));a=a[sel];b=b[sel]
 aa=p[f[a]];bb=p[f[b]];nn=np.cross(aa[:,1]-aa[:,0],aa[:,2]-aa[:,0]);mm=np.cross(bb[:,1]-bb[:,0],bb[:,2]-bb[:,0]);nn/=np.maximum(np.linalg.norm(nn,axis=1)[:,None],1e-20);mm/=np.maximum(np.linalg.norm(mm,axis=1)[:,None],1e-20);d=np.sum((aa-bb[:,0,None])*mm[:,None],axis=2);e=np.sum((bb-aa[:,0,None])*nn[:,None],axis=2);bound=np.minimum(np.maximum(0,np.minimum(d.max(1),-d.min(1))),np.maximum(0,np.minimum(e.max(1),-e.min(1))))
 return np.c_[face_ids[a],face_ids[b]],bound
