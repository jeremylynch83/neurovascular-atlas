"""Use the authorised regional brain-context adjustment with pial vein routes."""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'anatomical-fixes-v0929'))
from geometry import *
OUT=ROOT.parent/'corrections-work';targets=json.loads((OUT/'targets.json').read_text())
def field(v,delta,extent):
 d=np.linalg.norm((v-np.array([1,-71,42]))/extent,axis=1);w=1-smooth((d-.35)/.65);return w[:,None]*np.array(delta)
movable={'vein.anterior_pontine','vein.anterior_medullary','vein.pontomedullary.right','vein.pontomedullary.left','vein.lateral_medullary.right','vein.lateral_medullary.left','vein.lateral_anterior_pontomesencephalic.left','vein.lateral_anterior_pontomesencephalic.right','vein.preolivary.left','vein.preolivary.right','vein.transverse_medullary.left','vein.transverse_medullary.right','vein.posterior_medullary','vein.posterolateral_medullary.left','vein.posterolateral_medullary.right'}
results=[]
for delta,extent in [([0,-2,3],[10,12,12]),([0,-2.5,2.5],[10,12,12]),([0,-3,2],[10,12,12]),([0,-2,3],[12,12,12])]:
 C=OUT/('common-'+str(len(results)));C.mkdir(exist_ok=True);candidate={};bounds={};changed=[]
 for n,m in meshes.items():
  if m.file!='brain-context.glb' and n not in movable:continue
  change=field(m.v,delta,extent)
  if np.max(abs(change))<1e-7:continue
  v=m.v+change;candidate[n]=poly(v,m.f);bounds[n]=np.array([v.min(0),v.max(0)]);v.astype('<f4').tofile(C/(n+'.positions.bin'));changed.append(n)
 hits=[contacts(meshes[r['one']].pd,candidate.get(r['two'],meshes[r['two']].pd)) for r in targets[3:]];new=[]
 for n,p in candidate.items():
  for other,m in meshes.items():
   if m.file==meshes[n].file or m.file=='complete-anastomoses.glb':continue
   b=bounds.get(other,m.bounds)
   if np.any(bounds[n][1]<b[0]) or np.any(b[1]<bounds[n][0]):continue
   if contacts(p,candidate.get(other,m.pd),True) and not contacts(meshes[n].pd,m.pd,True):new.append([n,other])
 entry={'delta':delta,'extent':extent,'centre':[1,-71,42],'plateau':.35,'changed':changed,'hits':hits,'newContacts':new,'directory':C.name};results.append(entry);print('COMMON CONTEXT',entry,flush=True)
 (OUT/'common-context-trials.json').write_text(json.dumps(results,indent=2)+'\n')
 if not any(hits) and not new:break
