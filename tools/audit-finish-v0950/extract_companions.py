"""Extract reference canal courses from the current arterial tube surfaces."""
from common import *
from scipy.sparse import coo_matrix
from scipy.sparse.csgraph import dijkstra,connected_components
from scipy.ndimage import gaussian_filter1d
vtk.vtkLogger.SetStderrVerbosity(vtk.vtkLogger.VERBOSITY_OFF)
def extract(name):
 v,f=load(name);v,inv=np.unique(v,axis=0,return_inverse=True);f=inv[f]
 edges=np.unique(np.sort(np.vstack([f[:,[0,1]],f[:,[1,2]],f[:,[2,0]]]),1),axis=0);weight=np.linalg.norm(v[edges[:,0]]-v[edges[:,1]],axis=1)
 g=coo_matrix((np.r_[weight,weight],(np.r_[edges[:,0],edges[:,1]],np.r_[edges[:,1],edges[:,0]])),shape=(len(v),len(v))).tocsr();_,cc=connected_components(g,directed=False);start=np.flatnonzero(cc==np.argmax(np.bincount(cc)))[0];dd=dijkstra(g,indices=start);a=np.argmax(np.where(np.isfinite(dd),dd,-1));da=dijkstra(g,indices=a);b=np.argmax(np.where(np.isfinite(da),da,-1));db=dijkstra(g,indices=b);valid=np.isfinite(da)&np.isfinite(db);arc=np.zeros(len(v));arc[valid]=(da[valid]-db[valid]+da[b])/2
 pd=poly(v,f[np.all(valid[f],1)]);arr=numpy_to_vtk(arc);arr.SetName('arc');pd.GetPointData().SetScalars(arr);cut=vtk.vtkContourFilter();cut.SetInputData(pd);stations=np.linspace(.15,da[b]-.15,max(40,int(da[b]/.35)));q=[];r=[]
 for t in stations:
  cut.SetValue(0,float(t));cut.Update();p=cut.GetOutput();pts=vtk_to_numpy(p.GetPoints().GetData());lines=vtk_to_numpy(p.GetLines().GetData()).reshape(-1,3)[:,1:];w=np.linalg.norm(pts[lines[:,1]]-pts[lines[:,0]],axis=1);c=np.average((pts[lines[:,0]]+pts[lines[:,1]])/2,weights=np.maximum(w,1e-12),axis=0);q.append(c);r.append(np.median(np.linalg.norm(pts-c,axis=1)))
 return gaussian_filter1d(np.array(q),1.7,axis=0),gaussian_filter1d(np.array(r),2)
for side in ['right','left']:
 for base in ['Inferior alveolar','Infraorbital','Vertebral V2','Central retinal','Middle meningeal','MMA frontal']:
  name=(base+' '+side) if base in ['Vertebral V2','Central retinal'] else base+(' left' if side=='left' else '')
  q,r=extract(name);np.savez(WORK/(name+'.curve.npz'),q=q,r=r)
  print(name,'sample controls',np.round(q[::max(1,len(q)//9)],2).tolist(),'radius',np.round(np.percentile(r,[5,50,95]),2).tolist(),flush=True)
