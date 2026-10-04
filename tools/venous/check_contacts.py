import json
import numpy as np
from scipy.spatial import cKDTree
from reference import *
APP=ROOT.parents[1]
paths=json.loads((APP/'anatomy/source/venous/fitted-paths.json').read_text())
spec=json.loads((APP/'anatomy/source/venous/courses.json').read_text())
links={frozenset((r['from'],r['to'])) for r in spec['relationships']}
for row in spec['structures']:
 for v in row['points']:
  if isinstance(v,dict):links.add(frozenset((row['id'],v['structure'])))
collisions=[]
for i,a in enumerate(paths):
 q=np.array(a['points']);r=np.array(a['radii']);tree=cKDTree(q)
 for b in paths[i+1:]:
  if a['id']==b['id'] or frozenset((a['id'],b['id'])) in links:continue
  w=np.array(b['points']);s=np.array(b['radii']);d,j=tree.query(w);overlap=r[j]+s-d;bad=overlap>.35
  # Adjacent tributaries legitimately meet within their shared collector.
  if not np.any(bad):continue
  shared={x for e in links if a['id'] in e for x in e}-{a['id']}
  shared&={x for e in links if b['id'] in e for x in e}-{b['id']}
  if shared:
   for c in paths:
    if c['id'] in shared:
     dist,k=cKDTree(np.array(c['points'])).query(w);bad&=dist>(np.array(c['radii'])[k]+s+1.5)
  if np.any(bad):
   k=np.where(bad)[0][np.argmax(overlap[bad])];collisions.append({'a':a['id'],'b':b['id'],'overlap_mm':round(float(overlap[k]),3),'point':w[k].round(2).tolist(),'samples':int(bad.sum())})
(ROOT/'venous-unintended-contacts.json').write_text(json.dumps(collisions,indent=2));print(json.dumps(collisions,indent=2),flush=True)
# Screen against retained arterial surface vertices; conservative candidates
# are inspected by triangle distance in the following authoring review.
vertices=[];names=[];owner=[]
for rec in records:
 if rec['file']!='complete-circulation':continue
 p,_=arrays(rec);names.append(rec['name']);vertices.append(p);owner.append(np.full(len(p),len(names)-1,np.int32))
v=np.concatenate(vertices);owner=np.concatenate(owner);tree=cKDTree(v)
conflicts=[]
for a in paths:
 if a['id'].startswith('vein.cavernous'):continue
 q=np.array(a['points']);r=np.array(a['radii']);d,j=tree.query(q);bad=d<r-.15
 if np.any(bad):
  counts={names[int(k)]:int(np.sum(owner[j[bad]]==k)) for k in np.unique(owner[j[bad]])}
  conflicts.append({'id':a['id'],'arteries':counts,'max_overlap':round(float((r-d).max()),3),'point':q[np.argmin(d-r)].round(2).tolist()})
(ROOT/'venous-arterial-candidates.json').write_text(json.dumps(conflicts,indent=2));print('ARTERIAL',json.dumps(conflicts,indent=2),flush=True)
