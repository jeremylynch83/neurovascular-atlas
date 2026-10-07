"""Search small connected arterial and venous movements with collision gates."""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'anatomical-fixes-v0929'))
from geometry import *
OUT=ROOT.parent/'corrections-work';targets=json.loads((OUT/'targets.json').read_text())
def bump(v,centre,extent,delta,plateau=.4):
 d=np.linalg.norm((v-np.array(centre))/extent,axis=1);w=1-smooth((d-plateau)/(1-plateau));return w[:,None]*np.array(delta)
def field(v,file,upperA,upperV,lowerA,lowerV,ring):
 upper=upperA if file=='complete-circulation.glb' else upperV
 lower=lowerA if file=='complete-circulation.glb' else lowerV
 result=bump(v,[1,-56,73.5],[6,9,8],[0,upper,0],.6)+bump(v,[0,-72,42],[15,12,9],[0,lower,0],.55)
 if file=='complete-circulation.glb':result+=bump(v,[-9.4,-75.3,33.4],[5,5,4],[ring,0,0],.4)
 return result
results=[]
for config in [(2,-1,2,-1,.8),(2.5,-1.2,2.5,-1.2,.8),(3,-1.5,3,-1.5,.8),(3.5,-1.5,2.5,-1,.8),(3,-.8,2.5,-.7,.8)]:
 candidates={};bounds={}
 for n,m in meshes.items():
  if m.file not in ['venous.glb','complete-circulation.glb']:continue
  delta=field(m.v,m.file,*config)
  if np.max(np.linalg.norm(delta,axis=1))<1e-7:continue
  v=m.v+delta;candidates[n]=poly(v,m.f);bounds[n]=np.array([v.min(0),v.max(0)])
 hits=[contacts(candidates.get(r['one'],meshes[r['one']].pd),candidates.get(r['two'],meshes[r['two']].pd)) for r in targets]
 new=[]
 for n,p in candidates.items():
  a=bounds[n]
  for other,m in meshes.items():
   if m.file==meshes[n].file or m.file=='complete-anastomoses.glb':continue
   b=bounds.get(other,m.bounds)
   if np.any(a[1]<b[0]) or np.any(b[1]<a[0]):continue
   if contacts(p,candidates.get(other,m.pd),True) and not contacts(meshes[n].pd,m.pd,True):new.append([n,other])
 print('TRIAL',config,'changed',len(candidates),'remaining',hits,'new contacts',new,flush=True)
 results.append({'config':config,'changed':list(candidates),'contacts':hits,'newContacts':new})
(OUT/'local-field-trials.json').write_text(json.dumps(results,indent=2)+'\n')
