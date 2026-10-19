"""Optional local reconstruction QA: NumPy, VTK and python-fcl required."""
from pathlib import Path
import json,numpy as np,fcl,vtk
from vtk.util.numpy_support import vtk_to_numpy,numpy_to_vtk,numpy_to_vtkIdTypeArray
from geometry import Glb
from whole_surface_contacts import contacts
A=Path(__file__).resolve().parents[2];M=json.load(open(A/'public/anatomy/manifest.json'));R=json.load(open(A/'docs/temporal-surface-repair-validation.json'));g=Glb(A/'public/anatomy/models/craniofacial.glb');p,f,n=g.mesh('bone.temporal.left');start=R['newSurfaceFaceStart'];ff=f[start:];old=f[:start];assert len(ff)==R['newSurfaceFaceCount']
def poly(p,f):
 pts=vtk.vtkPoints();pts.SetData(numpy_to_vtk(p,deep=True));cells=vtk.vtkCellArray();cells.SetCells(len(f),numpy_to_vtkIdTypeArray(np.c_[np.full(len(f),3),f].ravel().astype('int64'),deep=True));o=vtk.vtkPolyData();o.SetPoints(pts);o.SetPolys(cells);return o
pairs,b=contacts(p,ff);assert not(b>.002).any(),'New surface folds'
c=vtk.vtkCollisionDetectionFilter();c.SetInputData(0,poly(p,ff));c.SetInputData(1,poly(p,old));t=vtk.vtkTransform();t.Identity();c.SetTransform(0,t);c.SetTransform(1,t);c.SetCollisionModeToAllContacts();c.SetBoxTolerance(0);c.SetCellTolerance(0);c.SetNumberOfCellsPerNode(2);c.Update();a=vtk_to_numpy(c.GetContactCells(0));b=vtk_to_numpy(c.GetContactCells(1));_,ix=np.unique(np.round(p,5),axis=0,return_inverse=True);sel=~(ix[ff[a]][:,:,None]==ix[old[b]][:,None,:]).any((1,2));a=a[sel];b=b[sel];aa=p[ff[a]];bb=p[old[b]];nn=np.cross(aa[:,1]-aa[:,0],aa[:,2]-aa[:,0]);mm=np.cross(bb[:,1]-bb[:,0],bb[:,2]-bb[:,0]);nn/=np.maximum(np.linalg.norm(nn,axis=1)[:,None],1e-20);mm/=np.maximum(np.linalg.norm(mm,axis=1)[:,None],1e-20);d=np.sum((aa-bb[:,0,None])*mm[:,None],axis=2);e=np.sum((bb-aa[:,0,None])*nn[:,None],axis=2);bound=np.minimum(np.maximum(0,np.minimum(d.max(1),-d.min(1))),np.maximum(0,np.minimum(e.max(1),-e.min(1))));assert not(bound>.002).any(),'New surface intersects source bone'
edges=np.sort(np.concatenate([f[:,[0,1]],f[:,[1,2]],f[:,[2,0]]]),axis=1);_,count=np.unique(edges,axis=0,return_counts=True);assert count.max()<=2
lo=p[ff].min((0,1));hi=p[ff].max((0,1))
def ob(p,f):
 m=fcl.BVHModel();m.beginModel();m.addSubModel(p,f);m.endModel();return fcl.CollisionObject(m)
patch=ob(p,ff);tested=0
for file in ['complete-circulation','complete-anastomoses','venous']:
 g=Glb(A/f'public/anatomy/models/{file}.glb')
 for s in M['structures']:
  if s.get('asset',{}).get('file')!='models/'+file+'.glb':continue
  q,t,n=g.mesh(s['asset']['node'])
  if not((q.min(0)<=hi)&(q.max(0)>=lo)).all():continue
  tested+=1;r=fcl.CollisionResult();number=fcl.collide(patch,ob(q,t),fcl.CollisionRequest(num_max_contacts=1000,enable_contact=True),r);assert number==0,s['id']
print(json.dumps({'release':M['release'],'newSurfaceTriangles':len(ff),'overlappingVascularMeshesTested':tested,'newSurfaceSelfContacts':0,'newSurfaceSourceContacts':0,'newSurfaceVascularContacts':0,'nonManifoldEdges':0}))
