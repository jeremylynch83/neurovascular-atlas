"""Report bone and arterial contacts for this continuation without waivers."""
from route_tools import *
baseline=WORK.parent/'work-v0958/candidate';geometry=json.loads((OUT/'continuation-geometry-validation.json').read_text())['results'];names=[r['node'] for r in geometry];mf=json.loads((WORK.parent/'public/anatomy/manifest.json').read_text());by={s['id']:s for s in mf['structures']};cat={s.get('asset',{}).get('node'):s for s in by.values()};rows=[];seen=set()
native={frozenset([r['a'],r['b']]) for r in interfaces}
for n in names:
 v,f=current(n);lo=v.min(0)-.05;hi=v.max(0)+.05
 endpoints={by.get(i,{}).get('asset',{}).get('node') for i in cat.get(n,{}).get('endpoints',[])}
 for other in FILES:
  if other==n or other.startswith(('brain.','vein.')):continue
  key=frozenset([n,other])
  if key in seen:continue
  seen.add(key);w,g=current(other)
  if np.any(w.max(0)<lo) or np.any(w.min(0)>hi):continue
  count=contacts(v,f,w,g)
  if not count:continue
  ov,of=load(n,baseline);ow,og=load(other,baseline) if (baseline/(other+'.positions.bin')).exists() else load(other);previous=contacts(ov,of,ow,og)
  row=dict(a=n,b=other,domain='bone' if other.startswith('bone.') else 'arterial',triangleContacts=count,previousCandidateTriangleContacts=previous,newContactPair=previous==0,nativeSharedInterface=key in native,catalogueEndpoint=other in endpoints,anatomicallyReviewed=False);rows.append(row);print(row,flush=True)
(OUT/'continuation-relationship-validation.json').write_text(json.dumps(dict(method=__doc__,checkedLabels=names,contacts=rows,newContactPairs=[r for r in rows if r['newContactPair']],passedAnatomicalRelationships=False),indent=2))
