"""Exact global incidence gate for append-only native wall patches."""
from collections import Counter
import numpy as np

def edge_delta(proposal):
 p=list(map(tuple,proposal['boundaryCoordinates']));counts=Counter();balances=Counter()
 for tri in proposal['triangles']:
  q=[p[i]for i in tri]
  for a,b in zip(q,q[1:]+q[:1]):
   edge=tuple(sorted([a,b]));counts[edge]+=1;balances[edge]+=1 if a<b else -1
 return counts,balances

def source_incidence(scene,proposals):
 wanted={edge for p in proposals for edge in edge_delta(p)[0]};points=np.asarray(sorted({x for edge in wanted for x in edge}),dtype='<f4');dt=np.dtype([('x','<f4'),('y','<f4'),('z','<f4')]);keys=points.view(dt).reshape(-1);counts=Counter();balances=Counter();names=sorted(n for n in scene.rows if scene.systems[n]=='artery');touched=[]
 for n in names:
  v,f=scene.mesh(n);mask=np.isin(np.asarray(v).view(dt).reshape(-1),keys)
  if not mask.any():continue
  hits=0
  for a,b in [(0,1),(1,2),(2,0)]:
   ids=f[mask[f[:,a]]&mask[f[:,b]]]
   for i,j in ids[:,[a,b]]:
    x,y=tuple(v[i]),tuple(v[j]);edge=tuple(sorted([x,y]))
    if edge in wanted:counts[edge]+=1;balances[edge]+=1 if x<y else -1;hits+=1
  if hits:touched.append({'node':n,'edgeIncidences':hits})
 return counts,balances,{'reviewedArterialMeshes':len(names),'changedCoordinateEdges':len(wanted),'sourceContributors':touched}

def assess(proposals,counts,balances,metadata):
 delta=Counter();db=Counter()
 for p in proposals:
  c,b=edge_delta(p);delta.update(c);db.update(b)
 issues=[];rows=[]
 for edge in sorted(delta):
  before=counts[edge];balance=balances[edge];after=before+delta[edge];afterbalance=balance+db[edge];row={'edge':[list(x)for x in edge],'sourceIncidences':before,'sourceBalance':balance,'addedIncidences':delta[edge],'candidateIncidences':after,'candidateBalance':afterbalance};rows.append(row)
  if before>2 or(before==2 and balance!=0)or after!=2 or afterbalance!=0:issues.append(row)
 return {'passed':not issues,**metadata,'edgesChecked':len(rows),'boundaryEdgesClosed':sum(r['sourceIncidences']==1 for r in rows),'issues':issues,'edges':rows,'scope':'Every appended coordinate edge checked against every named arterial mesh; all must finish with exactly two opposite incidences.'}
