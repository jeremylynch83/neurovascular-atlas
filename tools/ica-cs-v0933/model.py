from pathlib import Path
import os,json,numpy as np,vtk
from vtk.util.numpy_support import numpy_to_vtk,numpy_to_vtkIdTypeArray,vtk_to_numpy
ROOT=Path(__file__).resolve().parent
APP=ROOT/'release' if (ROOT/'release').exists() else ROOT.parents[1]
DATA=ROOT/'decoded';OUT=ROOT/'candidate';OUT.mkdir(exist_ok=True)
META=json.loads((DATA/'meshes.json').read_text())
def load(name,after=False):
 p=OUT/(name+'.positions.bin');ip=OUT/(name+'.indices.bin')
 if not after or not p.exists():p=DATA/(name+'.positions.bin')
 if not after or not ip.exists():ip=DATA/(name+'.indices.bin')
 return np.fromfile(p,'<f4').reshape(-1,3).astype(float),np.fromfile(ip,'<u4').reshape(-1,3)
def poly(v,f):
 p=vtk.vtkPolyData();pts=vtk.vtkPoints();pts.SetData(numpy_to_vtk(np.asarray(v,float),deep=True));p.SetPoints(pts);c=vtk.vtkCellArray();c.SetCells(len(f),numpy_to_vtkIdTypeArray(np.c_[np.full(len(f),3),f].astype(np.int64).ravel(),deep=True));p.SetPolys(c);return p
def arrays(p):
 return vtk_to_numpy(p.GetPoints().GetData()).copy(),vtk_to_numpy(p.GetPolys().GetData()).reshape(-1,4)[:,1:].copy()
def combine(names,after=False):
 vv=[];ff=[];o=0
 for n in names:
  v,f=load(n,after);vv.append(v);ff.append(f+o);o+=len(v)
 c=vtk.vtkCleanPolyData();c.SetInputData(poly(np.concatenate(vv),np.concatenate(ff)));c.SetTolerance(0);c.Update();return c.GetOutput()
def normals(p):
 n=vtk.vtkPolyDataNormals();n.SetInputData(p);n.SplittingOff();n.ConsistencyOn();n.Update();return n.GetOutput()
def save(n,v,f):
 v=v.astype('<f4');t=v[f];area=np.linalg.norm(np.cross(t[:,1]-t[:,0],t[:,2]-t[:,0]),axis=1);f=f[area>1e-12];ids,inv=np.unique(f,return_inverse=True);v=v[ids];f=inv.reshape(-1,3)
 nn=vtk_to_numpy(normals(poly(v,f)).GetPointData().GetNormals()).copy();bad=np.linalg.norm(nn,axis=1)<1e-8
 if bad.any():
  from scipy.spatial import cKDTree
  _,i=cKDTree(v[~bad]).query(v[bad]);nn[bad]=nn[~bad][i]
 v.tofile(OUT/(n+'.positions.bin'));f.astype('<u4').tofile(OUT/(n+'.indices.bin'));nn.astype('<f4').tofile(OUT/(n+'.normals.bin'))
def smooth(x):
 x=np.clip(x,0,1);return x*x*(3-2*x)
def locator(p):
 l=vtk.vtkStaticCellLocator();l.SetDataSet(p);l.BuildLocator();return l
def closest(l,p):
 q=[0.,0.,0.];ci=vtk.reference(0);sub=vtk.reference(0);d=vtk.reference(0.);l.FindClosestPoint(p,q,ci,sub,d);return np.array(q),float(d)**.5
def crop(p,lo,hi):
 v,f=arrays(p);t=v[f];k=np.all(t.max(1)>=lo,axis=1)&np.all(t.min(1)<=hi,axis=1);return poly(v,f[k])
def contacts(a,b):
 aa=np.array(a.GetBounds()).reshape(3,2);bb=np.array(b.GetBounds()).reshape(3,2);lo=np.maximum(aa[:,0],bb[:,0]);hi=np.minimum(aa[:,1],bb[:,1])
 if np.any(lo>hi):return 0
 ap=crop(a,lo,hi);bp=crop(b,lo,hi)
 if ap.GetNumberOfCells()==0 or bp.GetNumberOfCells()==0:return 0
 c=vtk.vtkCollisionDetectionFilter();c.SetInputData(0,ap);c.SetInputData(1,bp);t=vtk.vtkTransform();c.SetTransform(0,t);c.SetTransform(1,t);c.SetCellTolerance(1e-7);c.SetCollisionModeToHalfContacts();c.Update();return c.GetNumberOfContacts()
def clip(v,f,value,positive=True):
 pd=poly(v,f);pd.GetPointData().SetScalars(numpy_to_vtk(np.asarray(value,float),deep=True));c=vtk.vtkClipPolyData();c.SetInputData(pd);c.SetValue(0);c.SetInsideOut(not positive);c.Update();tr=vtk.vtkTriangleFilter();tr.SetInputConnection(c.GetOutputPort());tr.Update();return arrays(tr.GetOutput())
def closed(p):
 fill=vtk.vtkFillHolesFilter();fill.SetInputData(p);fill.SetHoleSize(1000);fill.Update();n=vtk.vtkPolyDataNormals();n.SetInputConnection(fill.GetOutputPort());n.AutoOrientNormalsOn();n.ConsistencyOn();n.SplittingOff();n.Update();return n.GetOutput()
def sample(p,lo,hi,dims):
 fn=vtk.vtkImplicitPolyDataDistance();fn.SetInput(p);s=vtk.vtkSampleFunction();s.SetImplicitFunction(fn);s.SetModelBounds(*[x for a,b in zip(lo,hi) for x in [a,b]]);s.SetSampleDimensions(*[int(x) for x in dims]);s.ComputeNormalsOff();s.Update();return vtk_to_numpy(s.GetOutput().GetPointData().GetScalars()).reshape(dims,order='F').copy()
def iso(sdf,lo,spacing):
 p=vtk.vtkImageData();p.SetDimensions(*sdf.shape);p.SetOrigin(*lo);p.SetSpacing(*spacing);p.GetPointData().SetScalars(numpy_to_vtk(sdf.astype('<f4').ravel(order='F'),deep=True));c=vtk.vtkFlyingEdges3D();c.SetInputData(p);c.SetValue(0,0);c.Update();v,f=arrays(c.GetOutput());t=v[f];return v,f[np.linalg.norm(np.cross(t[:,1]-t[:,0],t[:,2]-t[:,0]),axis=1)>1e-9]
def rings(v,f,ids=None):
 e=np.sort(np.concatenate([f[:,[0,1]],f[:,[1,2]],f[:,[2,0]]]),axis=1);e,c=np.unique(e,axis=0,return_counts=True);e=e[c==1]
 if ids is not None:e=e[np.all(np.isin(e,ids),axis=1)]
 adj={}
 for a,b in e:adj.setdefault(int(a),[]).append(int(b));adj.setdefault(int(b),[]).append(int(a))
 if any(len(ns)!=2 for ns in adj.values()):raise RuntimeError('Boundary is not a set of simple rings')
 unseen=set(adj);out=[]
 while unseen:
  start=next(iter(unseen));loop=[start];cur=start;prev=-1
  while True:
   nxt=next(n for n in adj[cur] if n!=prev)
   if nxt==start:break
   loop.append(nxt);prev,cur=cur,nxt
  unseen.difference_update(loop);out.append(np.array(loop))
 return out
def bridge(v,a,b):
 centre=v[np.r_[a,b]].mean(0);pa=v[a]-centre;pb=v[b]-centre
 if np.dot(np.cross(pa,np.roll(pa,-1,axis=0)).sum(0),np.cross(pb,np.roll(pb,-1,axis=0)).sum(0))<0:b=b[::-1]
 d=np.linalg.norm(v[a][:,None]-v[b][None,:],axis=2);i,j=np.unravel_index(d.argmin(),d.shape);a=np.roll(a,-i);b=np.roll(b,-j);n=len(a);m=len(b);av=v[np.r_[a,a[0]]];bv=v[np.r_[b,b[0]]];d=np.sum((av[:,None]-bv[None,:])**2,axis=2);cost=np.full((n+1,m+1),np.inf);move=np.zeros((n+1,m+1),np.uint8);cost[0,0]=0
 for i in range(n+1):
  for j in range(m+1):
   if not(i or j):continue
   ac=cost[i-1,j]+d[i,j]+d[i-1,j] if i else np.inf;bc=cost[i,j-1]+d[i,j]+d[i,j-1] if j else np.inf
   if ac<=bc:cost[i,j]=ac;move[i,j]=1
   else:cost[i,j]=bc;move[i,j]=2
 i=n;j=m;ff=[]
 while i or j:
  if move[i,j]==1:ff.append([a[(i-1)%n],a[i%n],b[j%m]]);i-=1
  else:ff.append([a[i%n],b[j%m],b[(j-1)%m]]);j-=1
 return np.array(ff,dtype=np.uint32)
