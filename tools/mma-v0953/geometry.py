from common import *
def arrays(p):
 return vtk_to_numpy(p.GetPoints().GetData()).copy(),vtk_to_numpy(p.GetPolys().GetData()).reshape(-1,4)[:,1:].copy()

def clip(v,f,value,positive=True):
 pd=poly(v,f);pd.GetPointData().SetScalars(numpy_to_vtk(np.asarray(value,float),deep=True));c=vtk.vtkClipPolyData();c.SetInputData(pd);c.SetValue(0);c.SetInsideOut(not positive);c.Update();tr=vtk.vtkTriangleFilter();tr.SetInputConnection(c.GetOutputPort());tr.Update();return arrays(tr.GetOutput())

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
