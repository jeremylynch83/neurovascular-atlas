"""Use catalogue ancestry to carry the reference fit through pial branches.

Prefix matching omits named daughter vessels. Catalogue ancestry supplies the
complete pial families. Fixed dural collars are reconciled in a separate pass.
"""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).parents[1]/'mma-v0952'))
from common import *
from scipy.spatial.distance import cdist
rev=json.loads((OUT/'revision.json').read_text());changed={r['node']for r in rev['changed']}
mf=json.loads((WORK.parent/'public/anatomy/manifest.json').read_text());by={s['id']:s for s in mf['structures']}
roots={s['id']for s in by.values()if s.get('asset',{}).get('node')in ['ICA terminus right','ICA terminus left','ICA posterior communicating right','ICA posterior communicating left','ICA anterior choroidal right','ICA anterior choroidal left','Basilar','Vertebral V4 right','Vertebral V4 left']}
def pial(s):
 if s.get('displayGroup')=='anastomoses'or s.get('asset',{}).get('node','').startswith(('Davidoff','Wollschlaeger','Posterior meningeal','VA anterior meningeal')):return False
 if s['system']=='vein':
  return s['id'].startswith(('vein.deep','vein.cortical','vein.superficial'))or s['id']in ['vein.galen','vein.basal.right','vein.basal.left','vein.internal_cerebral.right','vein.internal_cerebral.left']
 while s:
  if s['id']in roots:return True
  s=by.get(s['parent'])
 return False
targets={s['asset']['node']for s in by.values()if s.get('asset')and pial(s)}
already=set(json.loads((OUT/'reference-fit-audit.json').read_text())['affectedLabels'])
fields=[(np.load(WORK/'reference-fit-field-pass1.npz'),.2),(np.load(WORK/'reference-fit-field.npz'),.02)]
def field(v,x,width):
 points=x['points'];vectors=x['vectors'];sigma=float(x['sigma']);support=float(x['support']);fp=x['falxPoints'];fv=x['falxAmplitudes'];out=np.zeros_like(v)
 for start in range(0,len(v),1000):
  p=v[start:start+1000];dd=cdist(p,points);w=np.exp(-dd**2/(2*sigma**2));taper=smooth((support-dd.min(1))/(support-sigma));d=(w@vectors)/np.maximum(w.sum(1)[:,None],1e-30)*taper[:,None];fd=cdist(p,fp);fw=np.exp(-fd**2/50.);amp=(fw@fv)/np.maximum(fw.sum(1),1e-30)*smooth((15-fd.min(1))/10);d[:,0]+=np.tanh((p[:,0]-.624)/width)*amp;out[start:start+len(p)]=d
 return out
reports=[]
for n in sorted(targets-already):
 if n not in FILES:continue
 v,f=load(n,OUT)if n in changed else load(n);q=v.copy()
 for x,width in fields:q+=field(q,x,width)
 if np.linalg.norm(q-v,axis=1).max()<1e-5:continue
 write(n,q,f);sv,sf=load(n);row=dict(node=n,file=FILES[n],vertices=len(v),triangles=len(f),topologyExact=True,field='catalogue-complete-pial-reference-fit',maxShiftMm=float(np.linalg.norm(q-sv,axis=1).max()))
 for i,r in enumerate(rev['changed']):
  if r['node']==n:rev['changed'][i]=row;break
 else:rev['changed'].append(row)
 reports.append(dict(node=n,maximumAdditionalShiftMm=float(np.linalg.norm(q-v,axis=1).max())));print(reports[-1],flush=True)
(OUT/'revision.json').write_text(json.dumps(rev,indent=2));(OUT/'pial-reference-fit-completion.json').write_text(json.dumps(dict(method=__doc__,results=reports),indent=2))
