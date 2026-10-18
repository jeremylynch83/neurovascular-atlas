from common import *
from collections import Counter,defaultdict
from itertools import combinations
import heapq
q0=np.array(json.load(open(W/'gap-trials.json'))['boundary'],dtype='<f4');v,f=scene.mesh('SCA right');removed=[23440,23558,23559];q=np.vstack([q0,v[11566]]);lookup={tuple(x):i for i,x in enumerate(q)}
seed=json.load(open(W/'gap-trials.json'))['candidates'];best=min(seed,key=lambda x:(x['badArea'],len(x['sourceContacts']),x['selfCrossings']));triangles=[tuple(t)for t in best['triangles']]+[tuple(lookup[tuple(x)]for x in t)for t in v[f[removed]]]
def canonical(t):return min(tuple(t[i:]+t[:i])for i in range(3))
def state(ts):return tuple(sorted(canonical(list(t))for t in ts))
start=state(triangles);boundary=Counter()
for t in start:
 for a,b in zip(t,t[1:]+t[:1]):boundary[tuple(sorted((a,b)))]+=1
assert sum(c==1 for c in boundary.values())==7 and all(c in [1,2]for c in boundary.values());print('domain',len(q),'points',len(start),'faces',flush=True)
near=scene.nearby(q.min(0)-1e-6,q.max(0)+1e-6);info={};checks=0
for ids in combinations(range(len(q)),3):
 t=q[list(ids)].astype(float);area=float(np.linalg.norm(np.cross(t[1]-t[0],t[2]-t[0]))/2);contacts=[]
 if area>=1e-10:
  lo=t.min(0)-1e-7;hi=t.max(0)+1e-7
  for n in near:
   vv,ff=scene.mesh(n)
   for j in scene.bvh(n).query(lo,hi):
    if n=='SCA right'and j in removed:continue
    b=vv[ff[j]].astype(float)
    if np.any(b.max(0)<lo)or np.any(b.min(0)>hi):continue
    if np.linalg.norm(np.cross(b[1]-b[0],b[2]-b[0]))==0:continue
    checks+=1
    if triangle_crosses(t,b):contacts.append({'node':n,'face':int(j)})
 info[ids]={'areaMm2':area,'contacts':contacts,'passed':area>=1e-10 and not contacts}
def score(s):return sum(not info[tuple(sorted(t))]['passed']for t in s)
seen={start};todo=[(score(start),start)];tested=0;accepted=None;bestcost=100;selfchecks=0
while todo and tested<20000:
 cost,s=heapq.heappop(todo);tested+=1;bestcost=min(bestcost,cost)
 if cost==0:
  selfchecks+=1
  if all(not triangle_crosses(q[list(a)].astype(float),q[list(b)].astype(float))for a,b in combinations(s,2)):
   accepted=s;break
 inc=defaultdict(list)
 for i,t in enumerate(s):
  for k in range(3):a,b,c=t[k],t[(k+1)%3],t[(k+2)%3];inc[tuple(sorted((a,b)))].append((i,a,b,c))
 for e,rr in inc.items():
  if len(rr)!=2:continue
  (i,a,b,c),(j,bb,aa,d)=rr
  assert bb==b and aa==a
  if c==d or tuple(sorted((c,d)))in inc:continue
  new=state([t for k,t in enumerate(s)if k not in [i,j]]+[(c,a,d),(c,d,b)])
  if new in seen:continue
  seen.add(new);heapq.heappush(todo,(score(new),new))
r={'passed':accepted is not None,'boundaryLabels':['SCA right','Wollschlaeger and Wollschlaeger artery right'],'points':q.tolist(),'removedPositiveSourceFaces':removed,'triangles':accepted,'statesTested':tested,'statesDiscovered':len(seen),'bestSourceConflictTriangleCount':bestcost,'sourceClearStatesSelfChecked':selfchecks,'uniqueTrianglesScreened':len(info),'trianglePairsChecked':checks,'triangleScreen':[{'triangle':list(k),**val}for k,val in info.items()]};(W/'local-retriangulation.json').write_text(json.dumps(r,indent=2)+'\n');print({k:v for k,v in r.items()if k not in ['points','triangles','triangleScreen']},flush=True)
