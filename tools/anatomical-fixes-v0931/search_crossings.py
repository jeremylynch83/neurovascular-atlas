"""Local constrained candidate search; successful wall gates are explicit."""
import sys,itertools
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'anatomical-fixes-v0929'))
from geometry import *
OUT=ROOT.parent/'corrections-work';targets=json.loads((OUT/'targets.json').read_text())
def bump(v,centre,extent,delta,plateau=.6):
 d=np.linalg.norm((v-np.array(centre))/extent,axis=1);w=1-smooth((d-plateau)/(1-plateau));return w[:,None]*np.array(delta)
def overlaps(a,b):return not (np.any(a[1]<b[0]) or np.any(b[1]<a[0]))
def evaluate(centre,extent,delta,pairs):
 field=lambda v:bump(v,centre,extent,delta)
 candidates={};bounds={}
 for n,m in meshes.items():
  if m.file!='venous.glb':continue
  d=field(m.v)
  if np.max(abs(d))<1e-7:continue
  v=m.v+d;candidates[n]=poly(v,m.f);bounds[n]=np.array([v.min(0),v.max(0)])
 hits=[contacts(meshes[r['one']].pd,candidates.get(r['two'],meshes[r['two']].pd)) for r in pairs]
 if any(hits):return None
 new=[]
 for n,p in candidates.items():
  for other,m in meshes.items():
   if m.file in ['venous.glb','complete-anastomoses.glb'] or not overlaps(bounds[n],m.bounds):continue
   if contacts(p,m.pd,True) and not contacts(meshes[n].pd,m.pd,True):new.append([n,other])
 return {'centre':centre,'extent':extent,'delta':delta,'changed':list(candidates),'newContacts':new,'hits':hits}
results={}
configs={
 'upper':([1.6,-54.5,73.8],[3.6,6,5.4],list(itertools.product([-3,-2,-1,0,1,2,3],[-4,-3,-2,-1,0],[0,1,-1])),targets[:2]),
 'lower':([1,-71,42.2],[16,12,5.7],list(itertools.product([0],[-1,0,1],[2,3,4,-2,-3])),targets[3:]),
 'ring':([-9.4,-75.3,33.4],[5,5,4],list(itertools.product([-1.2,-.8,0,.8,1.2],[-1.2,-.8,0,.8,1.2],[0])),targets[2:3])
}
for region,(centre,extent,deltas,pairs) in configs.items():
 accepted=[];best=None
 for delta in sorted(deltas,key=lambda v:np.linalg.norm(v)):
  if np.linalg.norm(delta)<.1:continue
  result=evaluate(centre,extent,delta,pairs)
  if result is None:continue
  print('CANDIDATE',region,delta,'new',result['newContacts'],flush=True)
  accepted.append(result)
  if best is None or len(result['newContacts'])<len(best['newContacts']):best=result
  if not result['newContacts']:break
 results[region]={'best':best,'zeroTargetCandidates':accepted}
 print('REGION COMPLETE',region,'best',best,flush=True)
 (OUT/'local-crossing-search.json').write_text(json.dumps(results,indent=2)+'\n')
