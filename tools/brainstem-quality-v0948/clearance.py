"""Round-tube centreline clearance from the fixed pial and arterial surfaces."""
from common import *
from scipy.ndimage import gaussian_filter1d
obstacles=[]
for row in META:
 n=row['name']
 if not (n.startswith('brain.pons.') or row['file']=='complete-circulation.glb' or n=='vein.pontomesencephalic_sulcus.left'):continue
 v,f=load(n)
 if np.any(v.min(0)>np.array([25,-54,70])) or np.any(v.max(0)<np.array([-23,-78,45])):continue
 if n.startswith('brain.pons.'):
  # Exclude artificial flat label closures from the true exterior pial surface.
  t=v[f];cap=(np.ptp(t[:,:,0],axis=1)<.04)&(t[:,:,0].mean(1)>.5)&(t[:,:,0].mean(1)<.8);f=f[~cap]
 fn=vtk.vtkImplicitPolyDataDistance();fn.SetInput(poly(v,f));obstacles.append((n,fn,v.min(0),v.max(0)))
def correct(q,r):
 original=q.copy();movements=[]
 for iteration in range(12):
  delta=np.zeros_like(q)
  for n,fn,lo,hi in obstacles:
   active=np.flatnonzero(np.all(q>=lo-r.max()-.3,axis=1)&np.all(q<=hi+r.max()+.3,axis=1))
   for k in active:
    cp=[0.,0.,0.];d=fn.EvaluateFunctionAndGetClosestPoint(q[k],cp)
    if d>=r[k]+.16:continue
    normal=np.zeros(3);fn.EvaluateGradient(q[k],normal);normal/=max(np.linalg.norm(normal),1e-9)
    # Signed distance derivatives retain the exterior direction even inside tissue.
    delta[k]+=normal*min((r[k]+.16)-d,.6)
  if not np.any(delta):break
  delta=gaussian_filter1d(delta,1.1,axis=0)
  q=q+delta*.8
  movements.append(float(np.linalg.norm(q-original,axis=1).max()))
 return q,dict(maximumCentrelineAdjustmentMm=float(np.linalg.norm(q-original,axis=1).max()),iterations=len(movements))
