"""Keep source folded/sulcal detail from gaining new triangle intersections.

Only small neighbourhoods of newly intersecting face pairs blend back toward
the preserved source mesh. Existing source folds are compared by face IDs.
This is geometry preservation, not a claim that source folds are anatomical.
"""
import sys,ast
from pathlib import Path
sys.path.insert(0,str(Path(__file__).parents[1]/'mma-v0952'))
from common import *
m=ast.parse((Path(__file__).parents[1]/'mma-v0952/self_check.py').read_text());exec(compile(ast.Module(body=[x for x in m.body if isinstance(x,ast.FunctionDef)and x.name=='intersections'],type_ignores=[]),'folds','exec'))
if '--fast'in sys.argv:
 from fold_engine import intersections
rev=json.loads((OUT/'revision.json').read_text());report=[]
prior=json.loads((OUT/'brain-self-intersections.json').read_text())
for row in prior['results']:
 if not row['newIntersections']:continue
 n=row['node'];sv,sf=load(n);v,f=load(n,OUT);before=intersections(sv,sf);initial=v.copy();steps=[]
 for it in range(6):
  new=intersections(v,f)-before
  if not new:break
  centres=sv[sf[np.unique(np.array(list(new)).ravel())]].mean(1);d=cKDTree(centres).query(sv)[0];radius=3.+it
  weight=smooth((d-1.0)/radius);v=sv+(v-sv)*weight[:,None];steps.append(dict(iteration=it,newPairs=len(new),centres=centres.tolist(),blendRadiusMm=radius))
  print(n,it,len(new),flush=True)
 remaining=intersections(v,f)-before;write(n,v,f)
 for r in rev['changed']:
  if r['node']==n:r.update(maxShiftMm=float(np.linalg.norm(v-sv,axis=1).max()),referenceDetailBlend=True)
 report.append(dict(node=n,passed=not remaining,remainingNewPairs=len(remaining),maximumRepairMm=float(np.linalg.norm(v-initial,axis=1).max()),steps=steps))
(OUT/'revision.json').write_text(json.dumps(rev,indent=2));(OUT/'reference-fold-repair.json').write_text(json.dumps(dict(method=__doc__,results=report),indent=2));print(json.dumps(report,indent=2))
