"""Recover distinct guides for all convexity branches, not only the trunk."""
from common import *
from scipy.sparse import coo_matrix
from scipy.sparse.csgraph import dijkstra,connected_components
from scipy.ndimage import gaussian_filter1d
vtk.vtkLogger.SetStderrVerbosity(vtk.vtkLogger.VERBOSITY_OFF)
def extract(n):
 v,f=load(n);v,inv=np.unique(v,axis=0,return_inverse=True);f=inv[f];e=np.unique(np.sort(np.vstack([f[:,[0,1]],f[:,[1,2]],f[:,[2,0]]]),axis=1),axis=0);w=np.linalg.norm(v[e[:,0]]-v[e[:,1]],axis=1);g=coo_matrix((np.r_[w,w],(np.r_[e[:,0],e[:,1]],np.r_[e[:,1],e[:,0]])),shape=(len(v),len(v))).tocsr();_,cc=connected_components(g,directed=False);s=np.flatnonzero(cc==np.argmax(np.bincount(cc)))[0];ds=dijkstra(g,indices=s);a=np.argmax(np.where(np.isfinite(ds),ds,-1));da=dijkstra(g,indices=a);b=np.argmax(np.where(np.isfinite(da),da,-1));db=dijkstra(g,indices=b);ok=np.isfinite(da)&np.isfinite(db);arc=np.zeros(len(v));arc[ok]=(da[ok]-db[ok]+da[b])/2
 pd=poly(v,f[np.all(ok[f],axis=1)]);pd.GetPointData().SetScalars(numpy_to_vtk(arc));cut=vtk.vtkContourFilter();cut.SetInputData(pd);q=[];r=[]
 for t in np.linspace(.2,da[b]-.2,max(50,int(da[b]/.35))):
  cut.SetValue(0,float(t));cut.Update();p=cut.GetOutput()
  if not p.GetNumberOfPoints():continue
  pts=vtk_to_numpy(p.GetPoints().GetData());ln=vtk_to_numpy(p.GetLines().GetData()).reshape(-1,3)[:,1:];w=np.linalg.norm(pts[ln[:,1]]-pts[ln[:,0]],axis=1);c=np.average((pts[ln[:,0]]+pts[ln[:,1]])/2,weights=np.maximum(w,1e-10),axis=0);q.append(c);r.append(np.median(np.linalg.norm(pts-c,axis=1)))
 return gaussian_filter1d(q,2,axis=0),gaussian_filter1d(np.clip(r,.15,1.0),2)
for base in ['MMA frontal anterior division','MMA frontal posterior division','MMA posterior convexity','MMA parietal ascending','MMA posterior terminal']:
 for side in ['right','left']:
  n=base+(' left' if side=='left' else '');q,r=extract(n);np.savez(WORK/(n+'.curve.npz'),q=q,r=r);print(n,len(q),flush=True)
