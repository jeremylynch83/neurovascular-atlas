"""Put the lesser-wing receiving channel behind the orbital cortical margin.

The transverse source tube is displaced posteriorly under the lesser wing.
Its cavernous ports remain exact. The common exterior and both entering
channels move together, using a shear whose analytic Jacobian is one.
"""
import sys,ast
from pathlib import Path
sys.path.insert(0,str(Path(__file__).parents[1]/'mma-v0952'))
from common import *
vtk.vtkLogger.SetStderrVerbosity(vtk.vtkLogger.VERBOSITY_OFF)
m=ast.parse((Path(__file__).parents[1]/'mma-v0952/self_check.py').read_text());exec(compile(ast.Module(body=[x for x in m.body if isinstance(x,ast.FunctionDef)and x.name=='intersections'],type_ignores=[]),'folds','exec'))
rev=json.loads((OUT/'revision.json').read_text());changed={r['node']for r in rev['changed']}
brain=[(n,*load(n,OUT))if n in changed else(n,*load(n))for n in FILES if n.startswith('brain.')and not n.startswith(('brain.falx','brain.tentorium'))]
results=[]
for side in ['right','left']:
 n='vein.sphenoparietal.'+side;x=np.load(OUT/('receiver-seam-completed-'+side+'.npz'));v=x['v'].astype(float);f=x['f'];weight=smooth((abs(v[:,0])-18)/8)*(1-smooth((v[:,2]-86)/10));history=[];before=intersections(v,f)
 for i in range(21):
  distance=.25*i;w=v.copy();w[:,2 if '--inferior'in sys.argv else 1]-=distance*weight;lo=w.min(0);hi=w.max(0);rows=[]
  for bn,bv,bf in brain:
   if np.any(bv.max(0)<lo)or np.any(bv.min(0)>hi):continue
   tri=bv[bf];take=np.all(tri.max(1)>=lo,axis=1)&np.all(tri.min(1)<=hi,axis=1);count=contacts(w,f,bv,bf[take])
   if count:rows.append(dict(brain=bn,triangleContacts=count))
  history.append(dict(posteriorShiftMm=distance,contacts=rows));print(side,distance,rows,flush=True)
  if not rows:break
 after=intersections(w,f);new=after-before
 variant='inferior'if '--inferior'in sys.argv else 'posterior'
 np.savez_compressed(OUT/('receiver-'+variant+'-course-'+side+'.npz'),v=w.astype('<f4'),f=f.astype('<u4'))
 results.append(dict(side=side,passed=not rows and not new,newFoldPairs=len(new),posteriorShiftMm=distance,history=history,appliedToLabels=False))
(OUT/('receiver-'+variant+'-course-validation.json')).write_text(json.dumps(dict(method=__doc__,results=results),indent=2))
