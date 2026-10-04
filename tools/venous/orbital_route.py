"""Authoring-only constrained passage route within the observed SOF region."""
import heapq,itertools
from scipy.spatial import cKDTree
from scipy.ndimage import gaussian_filter1d
from reference import *
APP=ROOT.parents[1];result={}
fields=[]
for rec in records:
 if rec['name'] in ['bone.sphenoid','bone.frontal','bone.maxilla.right','bone.maxilla.left']:
  sdf=vtk.vtkImplicitPolyDataDistance();sdf.SetInput(poly(*arrays(rec)));fields.append(sdf)
for side,sg in [('right',1),('left',-1)]:
 def xyz(v):a=np.array(v,float);a[0]=a[0] if sg==1 else 1.3-a[0];return a
 axes=[np.arange(16,27.1,.5),np.arange(-34,-18.9,.5),np.arange(63,74.1,.5)];shape=tuple(len(a) for a in axes)
 points=np.stack(np.meshgrid(*axes,indexing='ij'),axis=-1).reshape(-1,3)
 if sg<0:points[:,0]=1.3-points[:,0]
 d=np.array([min(f.EvaluateFunction(p) for f in fields) for p in points]);free=d>=1.0
 tree=cKDTree(points[free]);inds=np.flatnonzero(free)
 start=int(inds[tree.query(xyz([23,-20,70]))[1]]);end=int(inds[tree.query(xyz([20,-33,67]))[1]])
 offsets=[o for o in itertools.product([-1,0,1],repeat=3) if o!=(0,0,0)]
 todo=[(0.,start)];cost={start:0.};prev={};visited=set()
 while todo:
  _,i=heapq.heappop(todo)
  if i in visited:continue
  visited.add(i)
  if i==end:break
  ijk=np.array(np.unravel_index(i,shape))
  for off in offsets:
   cell=ijk+off
   if np.any(cell<0) or np.any(cell>=shape):continue
   j=int(np.ravel_multi_index(cell,shape))
   if not free[j]:continue
   step=np.linalg.norm(np.array(off))*.5
   c=cost[i]+step*(1+.06/(d[j]-.8))
   if c<cost.get(j,float('inf')):cost[j]=c;prev[j]=i;heapq.heappush(todo,(c+np.linalg.norm(points[j]-points[end]),j))
 assert end in prev,(side,'No SOF route')
 route=[end]
 while route[-1]!=start:route.append(prev[route[-1]])
 q=points[route[::-1]]
 for _ in range(6):
  candidate=gaussian_filter1d(q,1,axis=0,mode='nearest');candidate[[0,-1]]=q[[0,-1]]
  for i,p in enumerate(candidate):
   if min(f.EvaluateFunction(p) for f in fields)>.98:q[i]=p
 result[side]=q.round(5).tolist();print(side,len(q),q[0],q[-1],flush=True)
(APP/'anatomy/source/venous/orbital-corridors.json').write_text(json.dumps(result,indent=2)+'\n')
