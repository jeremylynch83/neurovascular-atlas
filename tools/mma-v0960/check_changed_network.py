"""Audit every changed label against fixed and moved neighbour surfaces.

Compare complete label-pair contacts with the immutable v0.9.59 checkpoint.
Existing pairs are reported, not accepted as anatomically correct. Neural
vessel contacts are checked separately by the reference fit and MMA audit.
"""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).parents[1]/'mma-v0959'))
from route_tools import *
baseline=WORK.parent/'work-v0959/candidate'
mesh={n:current(n) for n in FILES};old={n:load(n,baseline) if (baseline/(n+'.positions.bin')).exists() else load(n) for n in FILES}
names=[n for n,(v,f) in mesh.items() if not np.array_equal(v,old[n][0]) or not np.array_equal(f,old[n][1])]
bounds={n:(v.min(0),v.max(0)) for n,(v,f) in mesh.items()};seen=set();rows=[]
for n in names:
 v,f=mesh[n];lo,hi=bounds[n]
 for other,(w,g) in mesh.items():
  if n==other:continue
  key=frozenset([n,other])
  if key in seen:continue
  seen.add(key);ol,oh=bounds[other]
  if np.any(oh<lo-.05) or np.any(ol>hi+.05):continue
  # Moved-vessel/neural pairs were exhaustively screened before installation.
  if (n.startswith('brain.') and not other.startswith(('brain.','bone.'))) or (other.startswith('brain.') and not n.startswith(('brain.','bone.'))):continue
  count=contacts(v,f,w,g)
  if not count:continue
  before=contacts(*old[n],*old[other]);row=dict(a=n,b=other,triangleContacts=count,previousTriangleContacts=before,newContactPair=before==0);rows.append(row)
  if row['newContactPair']:print('NEW',row,flush=True)
 print('CHECKED',n,flush=True)
(OUT/'changed-network-validation-v0960.json').write_text(json.dumps(dict(method=__doc__,checkedLabels=names,contacts=rows,newContactPairs=[r for r in rows if r['newContactPair']],passed=not any(r['newContactPair'] for r in rows)),indent=2));print('New pairs',sum(r['newContactPair'] for r in rows),flush=True)
