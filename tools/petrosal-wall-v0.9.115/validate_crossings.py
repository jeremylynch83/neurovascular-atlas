from common import *
from cache import BVH
from geometry import triangle_crosses
C={};changed={};trees={};rows=[]
for r in json.load(open(W/'spec.json'))['changes']:
 n=r['node'];v,f=scene.mesh(n);p=np.fromfile(W/'replayed'/(n+'.positions.bin'),'<f4').reshape(-1,3);C[n]=(p,f);trees[n]=BVH.build(p,f);changed[n]=np.flatnonzero(np.any(np.any(p[f]!=v[f],axis=2),axis=1))
checks=0;crossings=[];depth=[];inherited=[]
for n,(p,f)in C.items():
 v,_=scene.mesh(n)
 for i in changed[n]:
  a=p[f[i]].astype(float);lo=a.min(0)-1e-7;hi=a.max(0)+1e-7
  for other in sorted(set(scene.nearby(lo,hi))|set(C)):
   w,g=C.get(other,scene.mesh(other));tree=trees.get(other)or scene.bvh(other)
   for j in tree.query(lo,hi):
    if n==other and i==j:continue
    b=w[g[j]].astype(float)
    if np.any(b.max(0)<lo)or np.any(b.min(0)>hi):continue
    checks+=1
    if not triangle_crosses(a,b):continue
    row={'node':n,'face':int(i),'other':other,'otherFace':int(j)}
    if scene.systems[other]in ['brain','bone']and scene.volume_topology(other)['closedOrientedManifold']:
     depth.append(row);continue
    ov,of=scene.mesh(other)
    if triangle_crosses(v[f[i]].astype(float),ov[of[j]].astype(float)):inherited.append(row)
    else:crossings.append(row)
 print(n,'checked',checks,'new',len(crossings),'closed-depth',len(depth),'inherited',len(inherited),flush=True)
report={'passedNoNewNonNeuralCrossings':not crossings,'trianglePairsChecked':checks,'crossings':crossings,'closedTargetContactsForPairedDepthGate':depth,'inheritedSourceCrossings':inherited};(W/'crossing-validation.json').write_text(json.dumps(report,indent=2)+'\n')
