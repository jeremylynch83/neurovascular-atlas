"""Keep vascular entrances and posterior-fossa references in their native frame.

Cortical skull/falx corrections do not justify deforming brainstem,
cerebellum or complex carotid/SCA root collars. A source-coordinate taper
protects these entrances coherently across every arterial daughter mesh.
The basal MMA collar also remains in its previously validated source frame.
"""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).parents[1]/'mma-v0952'))
from common import *
rev=json.loads((OUT/'revision.json').read_text());rows={r['node']:r for r in rev['changed']};base=WORK.parent/'work-v0957/candidate';cats={s['asset']['node']:s['anatomy']['category']for s in json.loads((WORK.parent/'public/anatomy/brain-landmarks.json').read_text())['surfaces']}
protected=lambda n:n.startswith(('SCA ','AICA ','PICA ','Basilar','Vertebral V','Pontine ','VA medullary','Anterior spinal','Posterior spinal','Labyrinthine','Common cochlear','Anterior vestibular'))
roots=[n for n in FILES if protected(n)or n.startswith(('ICA paraophthalmic','ICA posterior communicating','ICA anterior choroidal','ICA terminus'))]
cloud=np.vstack([load(n)[0][::4]for n in roots]);tree=cKDTree(cloud);reports=[]
for n in FILES:
 posterior_brain=cats.get(n)in ['brainstem','cerebellum','ventricular_system']
 arterial=FILES[n]in ['complete-circulation.glb','complete-anastomoses.glb']
 if not(arterial or posterior_brain):continue
 sv,sf=load(n);v,f=load(n,OUT)if n in rows else(sv,sf);b,_=load(n,base)if(base/(n+'.positions.bin')).exists()else(sv,sf)
 if posterior_brain or protected(n):q=b.copy()
 else:
  distance=tree.query(sv)[0];root=1-smooth((distance-.7)/5.)
  basal=(1-smooth((sv[:,2]-50.5)/4.))*(1-smooth((np.linalg.norm(sv[:,:2]-np.array([-28.,-49.]),axis=1)-6)/6))
  weight=np.maximum(root,basal);q=v+(b-v)*weight[:,None]
 if np.max(np.linalg.norm(q-v,axis=1))<1e-8:continue
 write(n,q,f);row=rows.get(n,dict(node=n,file=FILES[n],vertices=len(v),triangles=len(f),topologyExact=True));row.update(field='protected-native-vascular-roots',maxShiftMm=float(np.linalg.norm(q-sv,axis=1).max()));rows[n]=row;reports.append(dict(node=n,maximumRestorationMm=float(np.linalg.norm(q-v,axis=1).max())));print(reports[-1],flush=True)
rev['changed']=list(rows.values());(OUT/'revision.json').write_text(json.dumps(rev,indent=2));(OUT/'native-root-protection.json').write_text(json.dumps(dict(method=__doc__,protectedRootLabels=roots,results=reports),indent=2))
