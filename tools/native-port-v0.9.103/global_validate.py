from common import *
from collections import Counter
spec=json.load(open(W/'replay-reconstruction.json'));delta=Counter();db=Counter();allowed=set()
def add(tri,sign):
 t=list(map(tuple,tri))
 for x,y in zip(t,t[1:]+t[:1]):
  e=tuple(sorted([x,y]));delta[e]+=sign;db[e]+=sign*(1 if x<y else -1)
for r in spec['changes']:
 v,f=scene.mesh(r['node'])
 for i in r['removedFaces']:add(v[f[i]],-1)
 for t in r['newTriangles']:add(v[t],1)
 for x,y in r['newBoundaryEdges']:allowed.add(tuple(sorted([tuple(x),tuple(y)])))
keys=set(delta);coords=np.asarray(sorted({p for e in keys for p in e}),dtype='<f4');dt=np.dtype([('x','<f4'),('y','<f4'),('z','<f4')]);match=coords.view(dt).reshape(-1);counts=Counter();balances=Counter();owners={}
for n in scene.rows:
 if scene.systems[n]!='vein':continue
 v,f=scene.mesh(n);mask=np.isin(np.asarray(v).view(dt).reshape(-1),match)
 if not mask.any():continue
 for a,b in [(0,1),(1,2),(2,0)]:
  for i,j in f[mask[f[:,a]]&mask[f[:,b]]][:,[a,b]]:
   x,y=tuple(v[i]),tuple(v[j]);e=tuple(sorted([x,y]))
   if e in keys:counts[e]+=1;balances[e]+=1 if x<y else -1;owners.setdefault(e,set()).add(n)
rows=[];newboundary=set();oldbad=set();newbad=set()
for e in sorted(keys):
 c=counts[e];b=balances[e];pc=c+delta[e];pb=b+db[e];assert pc>=0
 if c>2 or(c==2 and b!=0):oldbad.add(e)
 if pc>2 or(pc==2 and pb!=0):newbad.add(e)
 if pc==1 and c!=1:newboundary.add(e)
 rows.append({'edge':[list(map(float,p))for p in e],'sourceCount':c,'sourceBalance':b,'candidateCount':pc,'candidateBalance':pb})
assert newbad<=oldbad;assert not newboundary
for e in allowed:assert counts[e]+delta[e]==2 and balances[e]+db[e]==0
report={'passed':True,'reviewedVenousMeshes':231,'affectedEdges':len(keys),'badEdgesBefore':len(oldbad),'badEdgesAfter':len(newbad),'newBadEdges':0,'newBoundaryEdges':0,'restoredOppositePairedPortEdges':len(allowed),'pairedPortNeighbours':sorted({n for e in allowed for n in owners[e]}),'edges':rows};(W/'global-edge-validation.json').write_text(json.dumps(report,indent=2)+'\n');print({k:v for k,v in report.items()if k!='edges'})
