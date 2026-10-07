"""Evaluate compact venous overpasses before exporting any candidate."""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'anatomical-fixes-v0929'))
from geometry import *
OUT=ROOT.parent/'corrections-work'
targets=json.loads((OUT/'targets.json').read_text())
def bump(v,centre,extent,delta,plateau=.4):
 d=np.linalg.norm((v-np.array(centre))/extent,axis=1);w=1-smooth((d-plateau)/(1-plateau));return w[:,None]*np.array(delta)
def field(v,upper,lower,ring):
 return bump(v,[1.5,-54.5,74],[7,9,9],[0,upper,0])+bump(v,[1,-70.5,42],[16,12,10],[0,lower,0])+bump(v,[-9.4,-75.3,33.4],[5,5,4],[0,ring,0])
for n in ['brain.midbrain.right','brain.midbrain.left','brain.pons.right','brain.pons.left','brain.medulla-oblongata.right','brain.medulla-oblongata.left']:
 m=meshes[n];loc=locator(m.pd)
 print('SURFACE',n,[(r['two'],close(loc,np.array(r['centroid']))[0].round(2).tolist(),round(close(loc,np.array(r['centroid']))[1],2)) for r in targets],flush=True)
trials=[]
for upper,lower,ring in [(-2.5,-3.5,-1),(-3,-4,-1.2),(-2.5,-4.5,1),(-3.5,-4,1.2),(-2.5,-3,0)]:
 candidates={n:poly(m.v+field(m.v,upper,lower,ring),m.f) for n,m in meshes.items() if m.file=='venous.glb' and np.max(np.linalg.norm(field(m.v,upper,lower,ring),axis=1))>1e-6}
 hits=[contacts(meshes[r['one']].pd,candidates.get(r['two'],meshes[r['two']].pd)) for r in targets]
 brain=[]
 for n,p in candidates.items():
  for other,m in meshes.items():
   if m.file!='brain-context.glb':continue
   if contacts(p,m.pd,True) and not contacts(meshes[n].pd,m.pd,True):brain.append([n,other])
 print('TRIAL',upper,lower,ring,'remaining',hits,'new brain',brain,flush=True)
 trials.append({'upper':upper,'lower':lower,'ring':ring,'contacts':hits,'newBrainContacts':brain})
(OUT/'crossing-trials.json').write_text(json.dumps(trials,indent=2)+'\n')
