import sys,itertools
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'anatomical-fixes-v0929'))
from geometry import *
OUT=ROOT.parent/'corrections-work';targets=json.loads((OUT/'targets.json').read_text())
def bump(v,centre,extent,delta,plateau):
 d=np.linalg.norm((v-np.array(centre))/extent,axis=1);w=1-smooth((d-plateau)/(1-plateau));return w[:,None]*np.array(delta)
def overlaps(a,b):return not (np.any(a[1]<b[0]) or np.any(b[1]<a[0]))
regions={
 'upper':([[1.6,-54.5,z] for z in [73,73.5]],[[3.8,6,3.8],[5,7,4.2]],list(itertools.product([0,1,2,3],[-3,-2,-1],[0,.5,1,-.5])),targets[:2]),
 'lower':([[1,-71,42],[1,-72,40]],[[16,13,12],[18,16,16]],list(itertools.product([0],[-2,-1,0,1],[0,2,3,4,5])),targets[3:])
}
results={}
for region,(centres,extents,deltas,pairs) in regions.items():
 best=None;passed=None;attempt=0
 for centre,extent,delta in itertools.product(centres,extents,sorted(deltas,key=lambda v:np.linalg.norm(v))):
  if np.linalg.norm(delta)<.1:continue
  attempt+=1;field=lambda v:bump(v,centre,extent,delta,.35)
  relevant={r['two'] for r in pairs};pre={n:poly(meshes[n].v+field(meshes[n].v),meshes[n].f) for n in relevant}
  hits=[contacts(meshes[r['one']].pd,pre[r['two']]) for r in pairs]
  score=sum(hits)
  if best is None or score<best['score']:
   best={'centre':centre,'extent':extent,'delta':delta,'hits':hits,'score':score};print('BEST',region,best,flush=True)
  if score:continue
  candidate={};bounds={}
  for n,m in meshes.items():
   if m.file!='venous.glb':continue
   d=field(m.v)
   if np.max(abs(d))<1e-7:continue
   v=m.v+d;candidate[n]=poly(v,m.f);bounds[n]=np.array([v.min(0),v.max(0)])
  new=[]
  for n,p in candidate.items():
   for other,m in meshes.items():
    if m.file in ['venous.glb','complete-anastomoses.glb'] or not overlaps(bounds[n],m.bounds):continue
    if contacts(p,m.pd,True) and not contacts(meshes[n].pd,m.pd,True):new.append([n,other])
  entry={**best,'centre':centre,'extent':extent,'delta':delta,'hits':hits,'newContacts':new,'changed':list(candidate),'plateau':.35}
  print('ZERO TARGET',region,entry,flush=True)
  if not new:passed=entry;break
 results[region]={'best':best,'passed':passed,'attempts':attempt};(OUT/'route-search.json').write_text(json.dumps(results,indent=2)+'\n');print('ROUTE COMPLETE',region,results[region],flush=True)
