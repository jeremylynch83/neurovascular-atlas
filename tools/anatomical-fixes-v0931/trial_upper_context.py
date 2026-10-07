import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'anatomical-fixes-v0929'))
from geometry import *
OUT=ROOT.parent/'corrections-work';C=OUT/'upper-context';C.mkdir(exist_ok=True)
delta=np.array([3,-5,1]);extent=np.array([4.5,7,3.8]);centre=np.array([1.6,-54.5,73])
def flow(v):
 v=v.copy()
 for j in range(48):
  d=np.linalg.norm((v-(centre+delta*j/48))/extent,axis=1);w=1-smooth((d-.35)/.65);v+=w[:,None]*delta/48
 return v
candidate={};bounds={};changed=[]
for n,m in meshes.items():
 if m.file not in ['venous.glb','brain-context.glb']:continue
 v=flow(m.v)
 if np.max(abs(v-m.v))<1e-7:continue
 candidate[n]=poly(v,m.f);bounds[n]=np.array([v.min(0),v.max(0)]);v.astype('<f4').tofile(C/(n+'.positions.bin'));changed.append({'node':n,'maximumDisplacementMm':float(np.linalg.norm(v-m.v,axis=1).max())})
new=[]
for n,p in candidate.items():
 for o,m in meshes.items():
  if m.file==meshes[n].file or m.file=='complete-anastomoses.glb':continue
  b=bounds.get(o,m.bounds)
  if np.any(bounds[n][1]<b[0]) or np.any(b[1]<bounds[n][0]):continue
  if contacts(p,candidate.get(o,m.pd),True) and not contacts(meshes[n].pd,m.pd,True):new.append([n,o])
r={'delta':delta.tolist(),'extent':extent.tolist(),'centre':centre.tolist(),'plateau':.35,'steps':48,'changed':changed,'newContacts':new};(C/'revision.json').write_text(json.dumps(r,indent=2)+'\n');print('UPPER CONTEXT',r,flush=True)
