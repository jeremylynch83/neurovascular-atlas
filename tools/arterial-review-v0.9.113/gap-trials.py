from common import *
from functools import lru_cache
from itertools import combinations
from collections import Counter
b=json.load(open(W/'gap-baseline.json'));q=np.array(b['loop'],dtype='<f4')
# Orient the added patch opposite each source wall edge.
if b['edges'][0]['loopDirection']==b['edges'][0]['source'][0]['direction']:q=q[::-1].copy()
for i in range(len(q)):
 x,y=q[i],q[(i+1)%len(q)];row=next(r for r in b['edges']if set(map(tuple,r['edge']))=={tuple(x),tuple(y)});assert len(row['source'])==1 and row['source'][0]['direction']!= (1 if tuple(x)<tuple(y)else -1)
@lru_cache(None)
def triangulations(ids):
 if len(ids)<3:return [()]
 if len(ids)==3:return [((ids[0],ids[1],ids[2]),)]
 out=[]
 for k in range(1,len(ids)-1):
  for a in triangulations(ids[:k+1]):
   for c in triangulations(ids[k:]):out.append(a+c+((ids[0],ids[k],ids[-1]),))
 return out
near=scene.nearby(q.min(0)-1e-6,q.max(0)+1e-6);triinfo={};checks=0
for ids in combinations(range(len(q)),3):
 tri=q[list(ids)].astype(float);area=float(np.linalg.norm(np.cross(tri[1]-tri[0],tri[2]-tri[0]))/2);contacts=[]
 if area>=1e-10:
  lo=tri.min(0)-1e-7;hi=tri.max(0)+1e-7
  for n in near:
   v,f=scene.mesh(n)
   for j in scene.bvh(n).query(lo,hi):
    t=v[f[j]].astype(float)
    if np.any(t.max(0)<lo)or np.any(t.min(0)>hi):continue
    if np.linalg.norm(np.cross(t[1]-t[0],t[2]-t[0]))==0:continue
    checks+=1
    if triangle_crosses(tri,t):contacts.append({'node':n,'face':int(j)})
 triinfo[ids]={'areaMm2':area,'contacts':contacts}
rows=[]
for ts in triangulations(tuple(range(len(q)))):
 contacts=[x for t in ts for x in triinfo[tuple(sorted(t))]['contacts']];badarea=any(triinfo[tuple(sorted(t))]['areaMm2']<1e-10 for t in ts);selfcross=sum(triangle_crosses(q[list(a)].astype(float),q[list(c)].astype(float))for a,c in combinations(ts,2))if not badarea else -1
 rows.append({'triangles':[list(t)for t in ts],'sourceContacts':contacts,'badArea':badarea,'selfCrossings':selfcross,'passed':not contacts and not badarea and selfcross==0})
report={'boundary':q.tolist(),'enumeratedTriangulations':len(rows),'trianglePairsChecked':checks,'uniqueTrianglesChecked':len(triinfo),'nearbyLabels':near,'passedCandidates':sum(r['passed']for r in rows),'candidates':rows};(W/'gap-trials.json').write_text(json.dumps(report,indent=2)+'\n');print({k:v for k,v in report.items()if k not in ['boundary','candidates']},flush=True)
for r in rows:
 if r['passed']:print('ACCEPTABLE',r)
