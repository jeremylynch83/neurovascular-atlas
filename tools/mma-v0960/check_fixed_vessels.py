"""Check moved neural references against every unmoved vascular label."""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).parents[1]/'mma-v0959'))
from route_tools import *
baseline=WORK.parent/'work-v0959/candidate';ref=json.loads((OUT/'tentorial-reference-correction-v0960.json').read_text());moved={r['node'] for r in ref['results']} if ref['installed'] else set()
brain_names=[n for n in moved if n.startswith('brain.')];fixed=[n for n in FILES if not n.startswith(('brain.','bone.')) and n not in moved]
mesh={n:current(n) for n in brain_names+fixed};rows=[]
for n in brain_names:
 v,f=mesh[n];lo,hi=v.min(0)-.05,v.max(0)+.05
 ov,of=load(n,baseline) if (baseline/(n+'.positions.bin')).exists() else load(n)
 for other in fixed:
  w,g=mesh[other]
  if np.any(w.max(0)<lo) or np.any(w.min(0)>hi):continue
  count=contacts(v,f,w,g)
  if not count:continue
  before=contacts(ov,of,w,g);row=dict(brain=n,vessel=other,triangleContacts=count,previousTriangleContacts=before,newContactPair=before==0);rows.append(row)
  if before==0:print('NEW',row,flush=True)
 print('CHECKED',n,flush=True)
(OUT/'fixed-vessel-reference-validation-v0960.json').write_text(json.dumps(dict(method=__doc__,checkedBrainLabels=brain_names,checkedFixedVascularLabels=len(fixed),contacts=rows,newContactPairs=[r for r in rows if r['newContactPair']],passed=not any(r['newContactPair'] for r in rows)),indent=2))
