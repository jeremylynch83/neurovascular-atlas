"""Obstacle-aware CPA approach to the unsegmented porus reference."""
from common import *
from scipy.sparse import coo_matrix
from scipy.sparse.csgraph import dijkstra
from scipy.ndimage import gaussian_filter1d
vtk.vtkLogger.SetStderrVerbosity(vtk.vtkLogger.VERBOSITY_OFF)
import heapq
paths={}
for side,sign in [('right',1),('left',-1)]:
 lo=np.array([24.,-84.,43.]);hi=np.array([39.,-67.,59.]);sp=.5;shape=np.ceil((hi-lo)/sp).astype(int)+1
 grids=np.meshgrid(*[np.arange(n)*sp+lo[i] for i,n in enumerate(shape)],indexing='ij');pts=np.c_[tuple(g.ravel() for g in grids)];world=pts.copy();world[:,0]*=sign
 names=[];clear=np.full(len(pts),100.)
 for r in META:
  name=r['name']
  if name in ['Labyrinthine '+side,'Common cochlear '+side,'Anterior vestibular '+side]:continue
  v,f=load(name);mn=v.min(0);mx=v.max(0);wlo=world.min(0)-1;whi=world.max(0)+1
  if np.any(mx<wlo)|np.any(mn>whi):continue
  if r['file']=='complete-anastomoses.glb' or r['file']=='venous.glb' or r['file']=='complete-circulation.glb':
   if (v[:,2].max()<42):continue
  elif not name.startswith(('bone.','brain.')):continue
  pd=poly(v,f);implicit=vtk.vtkImplicitPolyDataDistance();implicit.SetInput(pd)
  vals=np.array([implicit.EvaluateFunction(p) for p in world])
  # True solids for bone and brain, surface wall exclusion for arteries/veins.
  signed=vals if name.startswith(('bone.','brain.')) else np.abs(vals)
  
  if name=='AICA '+side:
   root=np.array([sign*30.5,-76.4,44.05]);signed[np.linalg.norm(world-root,axis=1)<1.6]=100.
  clear=np.minimum(clear,signed);names.append(name)
 free=(clear>.48).reshape(shape)
 target=np.array([31.,-70.,57.]);start=np.array([30.9,-75.7,44.05]);distance=np.linalg.norm(pts-target,axis=1)
 valid=np.flatnonzero(free.ravel());end=valid[np.argmin(distance[valid])];ds=np.linalg.norm(pts-start,axis=1);begin=valid[np.argmin(ds[valid])]
 targetgrid=pts[end];print(side,'start',pts[begin], 'target',targetgrid,'target gap',distance[end], 'obstacles',len(names),flush=True)
 shifts=[np.array([x,y,z]) for x in [-1,0,1] for y in [-1,0,1] for z in [-1,0,1] if x or y or z];weights=[np.linalg.norm(d)*sp for d in shifts];b=tuple(np.unravel_index(begin,shape));e=tuple(np.unravel_index(end,shape));heap=[(0.,b)];cost={b:0.};prev={}
 while heap:
  _,cur=heapq.heappop(heap)
  if cur==e:break
  c=np.array(cur)
  for delta,length in zip(shifts,weights):
   q=c+delta
   if np.any(q<0)|np.any(q>=shape):continue
   t=tuple(q)
   if not free[t]:continue
   gap=clear[np.ravel_multi_index(t,shape)];new=cost[cur]+length*(1+.25/max(gap,.2)**2)
   if new<cost.get(t,1e20):cost[t]=new;prev[t]=cur;h=np.linalg.norm((q-np.array(e))*sp);heapq.heappush(heap,(new+h,t))
 assert e in prev,('No clear CPA approach',side)
 rev=[e]
 while rev[-1]!=b:rev.append(prev[rev[-1]])
 p=np.array([lo+np.array(t)*sp for t in rev[::-1]]);p[:,0]*=sign;p=gaussian_filter1d(p,.7,axis=0);p[0]=world[begin];p[-1]=world[end]
 paths[side]=dict(points=p.tolist(),obstacles=names,targetReference=[sign*31,-70,57],nearestClearEndpoint=world[end].tolist(),minimumGridClearanceMm=float(clear[np.ravel_multi_index(np.array(rev).T,shape)].min()),status='CPA approach to surface region, not a segmented IAC lumen')
 print(side,p.tolist(),flush=True)
(WORK/'acoustic-paths.json').write_text(json.dumps(paths,indent=2)+'\n')
