from common import *
from collections import defaultdict,Counter
from functools import lru_cache
from itertools import combinations
hist=json.load(open(A/'anatomy/source/arterial-junctions-v0.9.100/small-boundary-components.json'));loops=[]
for ri,r in enumerate(hist):
 if len(r['labels'])<2 or r.get('touchesBadEdge')or r['vertices']>8 or r['spanMm']>.3 or r['labels']==['SCA right','Wollschlaeger and Wollschlaeger artery right']:continue
 for k,q in enumerate(r.get('loops',[])):loops.append({'id':f'component-{ri}-loop-{k}','labels':r['labels'],'boundary':q,'spanMm':r['spanMm']})
keys={tuple(p)for r in loops for p in r['boundary']};coords=np.asarray(sorted(keys),dtype='<f4');dt=np.dtype([('x','<f4'),('y','<f4'),('z','<f4')]);match=coords.view(dt).reshape(-1);inc=defaultdict(list)
for n in scene.rows:
 if scene.systems[n]!='artery':continue
 v,f=scene.mesh(n);mask=np.isin(np.asarray(v).view(dt).reshape(-1),match)
 if not mask.any():continue
 for a,b in [(0,1),(1,2),(2,0)]:
  for i in np.flatnonzero(mask[f[:,a]]&mask[f[:,b]]):
   x,y=map(tuple,v[f[i,[a,b]]]);e=tuple(sorted([x,y]));inc[e].append({'node':n,'face':int(i),'direction':1 if x<y else-1})
@lru_cache(None)
def triangulations(ids):
 if len(ids)<3:return [()]
 out=[]
 for k in range(1,len(ids)-1):
  for a in triangulations(ids[:k+1]):
   for b in triangulations(ids[k:]):out.append(a+b+((ids[0],ids[k],ids[-1]),))
 return out
rows=[]
for r in loops:
 q=np.asarray(r['boundary'],dtype='<f4');edges=[inc[tuple(sorted([tuple(x),tuple(y)]))]for x,y in zip(q,np.roll(q,-1,axis=0))]
 if any(len(e)!=1 for e in edges):continue
 if (1 if tuple(q[0])<tuple(q[1])else -1)==edges[0][0]['direction']:q=q[::-1].copy()
 assert all(inc[tuple(sorted([tuple(x),tuple(y)]))][0]['direction']!=(1 if tuple(x)<tuple(y)else-1)for x,y in zip(q,np.roll(q,-1,axis=0)))
 near=scene.nearby(q.min(0)-1e-6,q.max(0)+1e-6);info={};checks=0
 for ids in combinations(range(len(q)),3):
  t=q[list(ids)].astype(float);area=float(np.linalg.norm(np.cross(t[1]-t[0],t[2]-t[0]))/2);contacts=[]
  if area>=1e-10:
   lo=t.min(0)-1e-7;hi=t.max(0)+1e-7
   for n in near:
    v,f=scene.mesh(n)
    for j in scene.bvh(n).query(lo,hi):
     b=v[f[j]].astype(float)
     if np.any(b.max(0)<lo)or np.any(b.min(0)>hi):continue
     if np.linalg.norm(np.cross(b[1]-b[0],b[2]-b[0]))==0:continue
     checks+=1
     if triangle_crosses(t,b):contacts.append({'node':n,'face':int(j)})
  info[ids]={'areaMm2':area,'contacts':contacts,'passed':area>=1e-10 and not contacts}
 candidates=[]
 for ts in triangulations(tuple(range(len(q)))):
  if not all(info[tuple(sorted(t))]['passed']for t in ts):continue
  if any(triangle_crosses(q[list(a)].astype(float),q[list(b)].astype(float))for a,b in combinations(ts,2)):continue
  candidates.append({'triangles':[list(t)for t in ts],'areaMm2':sum(info[tuple(sorted(t))]['areaMm2']for t in ts)})
 row={**r,'boundary':q.tolist(),'passedCandidates':len(candidates),'trianglePairsChecked':checks,'triangulationsEnumerated':len(triangulations(tuple(range(len(q))))),'candidates':candidates,'triangleScreen':[{'triangle':list(k),**x}for k,x in info.items()]};rows.append(row);print({k:x for k,x in row.items()if k not in ['boundary','candidates','triangleScreen']},flush=True)
(W/'remaining-gap-trials.json').write_text(json.dumps(rows,indent=2)+'\n')
