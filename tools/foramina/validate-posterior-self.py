from pathlib import Path
import sys,json,numpy as np,vtk
from vtk.util.numpy_support import vtk_to_numpy,numpy_to_vtk,numpy_to_vtkIdTypeArray
A=Path(__file__).resolve().parents[2];B=A/'docs';sys.path.insert(0,str(A/'tools/foramina'));from geometry import Glb
M=json.load(open(A/'public/anatomy/manifest.json'));rows={s['id']:s for s in M['structures']};changes=json.load(open(A/'anatomy/source/foramina/posterior-changes.json'));changes.update(json.load(open(A/'anatomy/source/foramina/posterior-vein-slices.json')));loaded={};report=[]
def pd(p,f):
 pts=vtk.vtkPoints();pts.SetData(numpy_to_vtk(p,deep=True));cells=vtk.vtkCellArray();cells.SetCells(len(f),numpy_to_vtkIdTypeArray(np.column_stack([np.full(len(f),3),f]).ravel().astype(np.int64),deep=True));o=vtk.vtkPolyData();o.SetPoints(pts);o.SetPolys(cells);return o
for sid in changes:
 s=rows[sid];file=s['asset']['file']
 if file not in loaded:loaded[file]=Glb(A/'public/anatomy'/file)
 p,f,n=loaded[file].mesh(s['asset']['node']);cc=p[f].mean(1);f=f[(np.abs(cc[:,0])>8)&(np.abs(cc[:,0])<50)&(cc[:,1]>-85)&(cc[:,1]<-44)&(cc[:,2]>24)&(cc[:,2]<64)]
 o=pd(p,f);c=vtk.vtkCollisionDetectionFilter();c.SetInputData(0,o);c.SetInputData(1,o);t=vtk.vtkTransform();t.Identity();c.SetTransform(0,t);c.SetTransform(1,t);c.SetCollisionModeToAllContacts();c.SetBoxTolerance(0);c.SetCellTolerance(0);c.SetNumberOfCellsPerNode(2);c.Update();a=vtk_to_numpy(c.GetContactCells(0));b=vtk_to_numpy(c.GetContactCells(1));sel=a<b;a=a[sel];b=b[sel];_,ix=np.unique(np.round(p,5),axis=0,return_inverse=True);uf=ix[f];sel=~(uf[a,:,None]==uf[b,None,:]).any((1,2));a=a[sel];b=b[sel];bounds=[]
 for start in range(0,len(a),20000):
  aa=p[f[a[start:start+20000]]];bb=p[f[b[start:start+20000]]];nn=np.cross(aa[:,1]-aa[:,0],aa[:,2]-aa[:,0]);mm=np.cross(bb[:,1]-bb[:,0],bb[:,2]-bb[:,0]);nn/=np.maximum(np.linalg.norm(nn,axis=1)[:,None],1e-20);mm/=np.maximum(np.linalg.norm(mm,axis=1)[:,None],1e-20);d=np.sum((aa-bb[:,0,None])*mm[:,None],axis=2);e=np.sum((bb-aa[:,0,None])*nn[:,None],axis=2);bounds.extend(np.minimum(np.maximum(0,np.minimum(d.max(1),-d.min(1))),np.maximum(0,np.minimum(e.max(1),-e.min(1)))))
 r={'id':sid,'triangles':len(f),'nonAdjacentContacts':len(bounds),'materialContacts':int(sum(np.array(bounds)>.001)),'maxPenetrationBoundMm':float(max(bounds,default=0))};report.append(r);print(r,flush=True)
(B/'foramina-batch3-self-contact-validation.json').write_text(json.dumps(report,indent=2))

assert all(r['materialContacts']==0 for r in report), 'New material self intersections in corrected vessels'
