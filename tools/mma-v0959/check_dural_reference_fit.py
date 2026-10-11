"""Audit cerebral cortex against the unchanged tentorial reference surfaces."""
from route_tools import *
categories={s['asset']['node']:s['anatomy']['category'] for s in json.loads((WORK.parent/'public/anatomy/brain-landmarks.json').read_text())['surfaces']}
rows=[]
for side in ['left','right']:
 tv,tf=current('brain.tentorium-cerebelli.'+side)
 for n in FILES:
  if categories.get(n)!='cerebral_cortex':continue
  v,f=current(n)
  if np.any(v.max(0)<tv.min(0)) or np.any(v.min(0)>tv.max(0)):continue
  count=contacts(v,f,tv,tf)
  if count:
   sv,sf=load(n);row=dict(brain=n,reference='brain.tentorium-cerebelli.'+side,sourceTriangleContacts=contacts(sv,sf,tv,tf),candidateTriangleContacts=count);rows.append(row);print(row,flush=True)
(OUT/'cortex-tentorial-reference-audit.json').write_text(json.dumps(dict(method=__doc__,passed=not rows,contacts=rows,interpretation='These contacts expose unresolved reference geometry relationships. They must not be resolved by treating neural cortex as a dural route or waiving the contacts.',brainModifiedInThisContinuation=False),indent=2))
