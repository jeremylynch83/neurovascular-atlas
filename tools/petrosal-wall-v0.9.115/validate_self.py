from common import *
from cache import BVH
from geometry import triangle_crosses
rows=[]
for spec in json.load(open(W/'spec.json'))['changes']:
 n=spec['node'];v,f=scene.mesh(n);p=np.fromfile(W/'replayed'/(n+'.positions.bin'),'<f4').reshape(-1,3);tree=BVH.build(p,f);pairs=[];checks=0
 for i,t in enumerate(p[f].astype(float)):
  lo=t.min(0)-1e-7;hi=t.max(0)+1e-7
  for j in tree.query(lo,hi):
   if j<=i:continue
   b=p[f[j]].astype(float)
   if np.any(b.max(0)<lo)or np.any(b.min(0)>hi):continue
   checks+=1
   if triangle_crosses(t,b):pairs.append([int(i),int(j)])
 expected={tuple(x)for x in spec['expectedRemainingSelfPairs']};actual=set(map(tuple,pairs));assert actual==expected
 remainingIds=np.unique(f[np.array(pairs).ravel()]);assert np.array_equal(v[remainingIds],p[remainingIds])
 rows.append({'node':n,'candidateFacesChecked':len(f),'trianglePairsChecked':checks,'sourceExactPairs':spec['sourceExactSelfPairs'],'candidateExactPairs':len(pairs),'removedExactPairs':spec['sourceExactSelfPairs']-len(pairs),'remainingPairs':sorted(pairs),'remainingContactTrianglesByteExact':True,'newSelfContacts':0,'passed':True})
(W/'self-validation.json').write_text(json.dumps({'passed':True,'changes':rows},indent=2)+'\n');print(rows)
