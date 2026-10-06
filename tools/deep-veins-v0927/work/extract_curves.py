"""Geodesic sections retain vessel loops without relying on a world axis."""
from geometry import *
from scipy.sparse import coo_matrix
from scipy.sparse.csgraph import dijkstra,connected_components
from scipy.ndimage import gaussian_filter1d,median_filter
from scipy.spatial import cKDTree
import json,time
OUT=ROOT/'candidate'

def extract(m):
 v=m.v;f=m.f;_,first,inv=np.unique(v,axis=0,return_index=True,return_inverse=True);v=v[first];f=inv[f];edges=np.unique(np.sort(np.vstack([f[:,[0,1]],f[:,[1,2]],f[:,[2,0]]]),1),axis=0);weights=np.linalg.norm(v[edges[:,0]]-v[edges[:,1]],axis=1);G=coo_matrix((np.r_[weights,weights],(np.r_[edges[:,0],edges[:,1]],np.r_[edges[:,1],edges[:,0]])),shape=(len(v),len(v))).tocsr();_,cc=connected_components(G,directed=False);group=np.argmax(np.bincount(cc));start=np.flatnonzero(cc==group)[0];d=dijkstra(G,indices=start);a=np.argmax(np.where(np.isfinite(d),d,-1));da=dijkstra(G,indices=a);b=np.argmax(np.where(np.isfinite(da),da,-1));db=dijkstra(G,indices=b);valid=np.isfinite(da)&np.isfinite(db);scalar=np.zeros(len(v));scalar[valid]=(da[valid]-db[valid]+da[b])/2
 if not valid.all():scalar[~valid]=scalar[valid][cKDTree(v[valid]).query(v[~valid])[1]]
 data=poly(v,f[np.all(valid[f],1)]);arr=numpy_to_vtk(scalar);arr.SetName('arc');data.GetPointData().SetScalars(arr);contour=vtk.vtkContourFilter();contour.SetInputData(data);tt=np.linspace(.05,da[b]-.05,max(60,int(da[b]/.2)));points=[]
 for t in tt:
  contour.SetValue(0,float(t));contour.Update();pd=contour.GetOutput();p=vtk_to_numpy(pd.GetPoints().GetData());line=vtk_to_numpy(pd.GetLines().GetData()).reshape(-1,3)[:,1:];length=np.linalg.norm(p[line[:,0]]-p[line[:,1]],axis=1);mid=(p[line[:,0]]+p[line[:,1]])/2;points.append(np.average(mid,weights=np.maximum(length,1e-12),axis=0))
 q=gaussian_filter1d(np.array(points),2.,axis=0);param=scalar[inv];p=np.column_stack([np.interp(param,tt,q[:,j]) for j in range(3)]);rad=np.linalg.norm(m.v-p,axis=1);profile=[]
 for t in tt:
  mask=abs(param-t)<.35;profile.append(np.median(rad[mask]) if mask.any() else np.median(rad[np.argsort(abs(param-t))[:20]]))
 return q,np.array(profile),param,tt
