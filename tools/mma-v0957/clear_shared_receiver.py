"""A local common-exterior trial, preserving exact native receiver openings.

The shared receiving tube is translated coherently below the orbital cortex,
with compact taper away from its lateral segment. Full mesh and collar checks
are mandatory; no automatic installation or export occurs here.
"""
import sys,ast
from pathlib import Path
sys.path.insert(0,str(Path(__file__).parents[1]/'mma-v0956'))
from clear_neural import *
m=ast.parse((Path(__file__).parents[1]/'mma-v0952/self_check.py').read_text())
exec(compile(ast.Module(body=[x for x in m.body if isinstance(x,ast.FunctionDef)and x.name=='intersections'],type_ignores=[]),'folds','exec'))
m=ast.parse((Path(__file__).parents[1]/'mma-v0952/finish_receiver_seams.py').read_text())
exec(compile(ast.Module(body=[x for x in m.body if isinstance(x,ast.FunctionDef)and x.name=='triangle_keys'],type_ignores=[]),'keys','exec'))
reports=[]
for side in ['right','left']:
 n='vein.sphenoparietal.'+side;sv,sf=load(n);x=np.load(OUT/('receiver-seam-completed-'+side+'.npz'));v=x['v'].astype(float);f=x['f'];initial=v.copy();sign=1 if side=='right'else -1
 sourcekeys=set(triangle_keys(sv,sf));generated=np.array([k not in sourcekeys for k in triangle_keys(v,f)]);checkf=f[generated]
 patch=sv[(sign*sv[:,0]>=40)&(sign*sv[:,0]<=46)];dd=cKDTree(patch).query(v)[0]
 u=(sign*v[:,0]-40)/6;weight=np.sin(np.pi*np.clip(u,0,1))**2*np.exp(-dd**2/(2*2.5**2));weight[(u<=0)|(u>=1)]=0
 bv,bf=load('brain.orbital-gyri.'+side);bp=poly(bv,bf);history=[]
 for i in range(22):
  count=contacts(v,checkf,bv,bf);history.append(dict(iteration=i,triangleContacts=count,maximumAdditionalShiftMm=float(np.linalg.norm(v-initial,axis=1).max())));print(side,history[-1],flush=True)
  if count==0:break
  if '--lateral' in sys.argv:v[:,0]+=.07*sign*weight
  else:v[:,2]-=.12*weight
 folds=intersections(v,f);passed=not history[-1]['triangleContacts']and not folds
 np.savez_compressed(OUT/('receiver-local-clearance-'+side+'.npz'),v=v.astype('<f4'),f=f.astype('<u4'))
 reports.append(dict(side=side,passed=passed,newSelfIntersections=len(folds),history=history,appliedToLabels=False))
(OUT/'receiver-local-clearance-trial.json').write_text(json.dumps(dict(method=__doc__,results=reports),indent=2))
