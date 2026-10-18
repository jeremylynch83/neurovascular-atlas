from common import *
from collections import Counter,defaultdict
from regional_validation import enclosed_samples,validate_regional
from geometry import patch_mesh
rows=json.load(open(W/'remaining-gap-trials.json'));out=[]
for r in rows:
 if not r['candidates']:continue
 q=np.array(r['boundary'],dtype='<f4');bad=[]
 for n in scene.nearby(q.min(0),q.max(0)):
  if scene.systems[n]not in ['brain','bone']or not scene.volume_topology(n)['closedOrientedManifold']:continue
  v,f=scene.mesh(n);inside=enclosed_samples(v,f,q)
  if inside.any():bad.append({'target':n,'insideBoundaryVertices':int(inside.sum())})
 result={'id':r['id'],'labels':r['labels'],'tissueCornerFailures':bad,'passed':False}
 if not bad:
  keys=set(map(tuple,q));inc=Counter();bal=Counter()
  for n in scene.rows:
   if scene.systems[n]!='artery':continue
   v,f=scene.mesh(n);mask=np.isin(np.asarray(v).view(np.dtype([('x','<f4'),('y','<f4'),('z','<f4')])).reshape(-1),q.view(np.dtype([('x','<f4'),('y','<f4'),('z','<f4')])).reshape(-1))
   if not mask.any():continue
   for a,b in [(0,1),(1,2),(2,0)]:
    for i in np.flatnonzero(mask[f[:,a]]&mask[f[:,b]]):
     x,y=map(tuple,v[f[i,[a,b]]]);e=tuple(sorted((x,y)));inc[e]+=1;bal[e]+=1 if x<y else-1
  for candidate in r['candidates']:
   extra=Counter();eb=Counter()
   for t in q[candidate['triangles']]:
    for x,y in zip(t,np.roll(t,-1,axis=0)):
     x,y=tuple(x),tuple(y);e=tuple(sorted((x,y)));extra[e]+=1;eb[e]+=1 if x<y else-1
   if any(inc[e]+c!=2 or bal[e]+eb[e]!=0 for e,c in extra.items()):continue
   target=r['labels'][0];proposal={'id':r['id'],'boundaryLabels':r['labels'],'boundaryCoordinates':r['boundary'],'triangles':candidate['triangles']};p,g,appended=patch_mesh(scene,target,[proposal]);validation=validate_regional(scene,{target:(p,g)},[{'id':r['id'],'nodes':r['labels']}]);result['validation']=validation
   if validation['passed']:
    result.update(passed=True,target=target,proposal=proposal,areaMm2=candidate['areaMm2'],spanMm=r['spanMm']);break
 out.append(result);print({k:v for k,v in result.items()if k not in ['validation','proposal']},flush=True)
(W/'remaining-gap-gates.json').write_text(json.dumps(out,indent=2)+'\n')
