"""An injective smooth flow replaces a candidate whose transition folds."""
import sys,itertools
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'anatomical-fixes-v0929'))
from geometry import *
OUT=ROOT.parent/'corrections-work';targets=json.loads((OUT/'targets.json').read_text())[:2]
def flow(v,delta,extent,centre):
 v=v.copy()
 for j in range(48):
  c=np.array(centre)+np.array(delta)*j/48;d=np.linalg.norm((v-c)/extent,axis=1);w=1-smooth((d-.35)/.65);v+=w[:,None]*np.array(delta)/48
 return v
results=[]
for delta,extent,centre in itertools.product([[3,-4,0],[3,-5,0],[4,-4,0],[4,-5,-.5],[-3,-4,0],[-4,-4,0],[3,-5,1]],[[4.5,7,3.8],[5.5,8,4.5]],[[1.6,-54.5,73]]):
 candidate={};bounds={};vertices={}
 for n,m in meshes.items():
  if m.file!='venous.glb':continue
  v=flow(m.v,delta,extent,centre)
  if np.max(abs(v-m.v))<1e-7:continue
  candidate[n]=poly(v,m.f);bounds[n]=np.array([v.min(0),v.max(0)]);vertices[n]=v
 hits=[contacts(meshes[r['one']].pd,candidate.get(r['two'],meshes[r['two']].pd)) for r in targets]
 if any(hits):print('FLOW',delta,extent,'hits',hits,flush=True);continue
 new=[]
 for n,p in candidate.items():
  for other,m in meshes.items():
   if m.file in ['venous.glb','complete-anastomoses.glb']:continue
   if np.any(bounds[n][1]<m.bounds[0]) or np.any(m.bounds[1]<bounds[n][0]):continue
   if contacts(p,m.pd,True) and not contacts(meshes[n].pd,m.pd,True):new.append([n,other])
 r={'delta':delta,'extent':extent,'centre':centre,'plateau':.35,'steps':48,'hits':hits,'newContacts':new,'changed':list(candidate)};results.append(r);print('FLOW CLEAR',r,flush=True)
 (OUT/'upper-flow-trials.json').write_text(json.dumps(results,indent=2)+'\n')
 if not new:
  C=OUT/'upper-flow';C.mkdir(exist_ok=True)
  for n,v in vertices.items():v.astype('<f4').tofile(C/(n+'.positions.bin'))
  (C/'revision.json').write_text(json.dumps(r,indent=2)+'\n');break
