from common import *
from scipy.ndimage import gaussian_filter1d
vtk.vtkLogger.SetStderrVerbosity(vtk.vtkLogger.VERBOSITY_OFF)
def inner(side):
 vv=[];ff=[]
 for name in ['bone.sphenoid','bone.temporal.'+side,'bone.parietal.'+side,'bone.frontal','bone.occipital']:
  v,f=load(name);tri=v[f];normal=np.cross(tri[:,1]-tri[:,0],tri[:,2]-tri[:,0]);c=tri.mean(1);keep=np.einsum('ij,ij->i',normal,c-[0,-60,95])<0
  ff.append(f[keep]+sum(len(x) for x in vv));vv.append(v)
 v=np.concatenate(vv);f=np.concatenate(ff);normal=np.cross(v[f[:,1]]-v[f[:,0]],v[f[:,2]]-v[f[:,0]]);normal/=np.maximum(np.linalg.norm(normal,axis=1)[:,None],1e-12)
 return v,f,normal
rows=[]
for side in ['right','left']:
 bv,bf,ns=inner(side);l=locator(bv,bf);cp=[0.,0.,0.];cid=vtk.reference(0);sub=vtk.reference(0);d2=vtk.reference(0.)
 q=np.concatenate([np.load(WORK/(n+(' left' if side=='left' else '')+'.curve.npz'))['q'] for n in ['Middle meningeal','MMA frontal']]);q=q[np.argsort(q[:,2])];sample=q[::8];pts=[];nn=[]
 for p in sample:l.FindClosestPoint(p,cp,cid,sub,d2);pts.append(cp.copy());nn.append(ns[int(cid)])
 pts=np.array(pts);nn=np.array(nn);rows.append(dict(side=side,old=sample.tolist(),skull=pts.tolist(),normal=nn.tolist()))
 print(side,'controls',np.round(pts[::8],2).tolist(),np.round(nn[::8],2).tolist(),flush=True)
(WORK/'corridor-controls.json').write_text(json.dumps(rows))
