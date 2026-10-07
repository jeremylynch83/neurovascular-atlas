import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'anatomical-fixes-v0929'))
from geometry import *
OUT=ROOT.parent/'corrections-work';curves=json.loads((OUT/'curves.json').read_text());cl=locator(meshes['brain.corpus-callosum'].pd);tl=locator(combine(['brain.tentorium-cerebelli.right','brain.tentorium-cerebelli.left']))
for n in [f'ACA {s} {side}' for side in ['right','left'] for s in ['A2','A3','A4','A5']]:
 q=np.array(curves[n]['points']);r=np.array(curves[n]['radii']);near=np.array([close(cl,p)[0] for p in q]);d=np.linalg.norm(q-near,axis=1)
 print(n,'distance p5/50/95',np.percentile(d,[5,50,95]).round(2),'wall gap',np.percentile(d-r,[5,50,95]).round(2),'stations',np.c_[q[::max(1,len(q)//5)],near[::max(1,len(q)//5)]].round(2).tolist(),flush=True)
q=np.array(curves['vein.straight']['points']);near=np.array([close(tl,p)[0] for p in q]);d=np.linalg.norm(q-near,axis=1)
print('STRAIGHT', 'distance p5/50/95',np.percentile(d,[5,50,95]).round(2),'stations',np.c_[q[::max(1,len(q)//10)],near[::max(1,len(q)//10)]].round(2).tolist(),flush=True)
for n in ['brain.tentorium-cerebelli.right','brain.falx-cerebri']:
 v=meshes[n].v;sel=v[abs(v[:,0]-.636)<3]
 print('MEDIAL',n,[(float(y),np.round(sel[(sel[:,1]>=y-2)&(sel[:,1]<y+2),2],1).tolist()) for y in np.arange(-142,-94,4)],flush=True)
