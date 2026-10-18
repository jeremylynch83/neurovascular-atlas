from pathlib import Path
import sys,json,numpy as np
A=Path(__file__).resolve().parents[2];sys.path.insert(0,str(A/'tools/repair'))
from cache import Scene
from geometry import edge_table,cycles
W=Path(sys.argv[1]).resolve();W.mkdir(parents=True,exist_ok=True)
if (W/'native-scan.json').exists()or(W/'accepted-patches.json').exists():raise ValueError('Use a fresh scan output directory')
scene=Scene(A,Path(sys.argv[2]).resolve())
from collections import defaultdict
names=sorted(n for n in scene.rows if scene.systems[n]=='artery');directions=[];edgeowners=[];badcoords=set();stats=[]
for n in names:
 v,f=scene.mesh(n);u,e,c,b,d,first=edge_table(v,f);mask=(c>2)|((c==2)&(b!=0));badcoords.update(map(tuple,u[np.unique(e[mask])]))
 directions.append(u[d[c==1]]);edgeowners.extend([n]*int(sum(c==1)));stats.append({'node':n,'asset':scene.rows[n]['asset'],'vertices':len(v),'triangles':len(f),'boundaryEdges':int(sum(c==1)),'badEdges':int(sum(mask))})
 if len(stats)%100==0:print('scanned',len(stats),flush=True)
pts=np.vstack(directions);u,inv=np.unique(pts.reshape(-1,3),axis=0,return_inverse=True);d=inv.reshape(-1,2);physical=np.sort(d,axis=1);e,first,which,c=np.unique(physical,axis=0,return_index=True,return_inverse=True,return_counts=True);b=np.bincount(which,weights=np.where(d[:,0]<d[:,1],1,-1),minlength=len(e));mask=(c>2)|((c==2)&(b!=0));badcoords.update(map(tuple,u[np.unique(e[mask])]))
bd=d[first[c==1]];owners=np.array(edgeowners)[first[c==1]];owner={tuple(x):n for x,n in zip(bd,owners)};adj=defaultdict(set)
for a,b in bd:adj[a].add(b);adj[b].add(a)
pending=set(adj);rows=[];skipped=0
while pending:
 todo=[min(pending)];comp=set()
 while todo:
  i=todo.pop()
  if i in comp:continue
  comp.add(i);pending.discard(i);todo.extend(adj[i]-comp)
 if len(comp)>40:skipped+=1;continue
 ed=np.array([x for x in bd if x[0]in comp]);p=u[sorted(comp)];span=np.linalg.norm(p[:,None]-p,axis=2).max();labels=sorted({owner[tuple(x)]for x in ed});row={'vertices':len(comp),'edges':len(ed),'labels':labels,'spanMm':float(span),'centre':p.mean(0).tolist(),'touchesBadEdge':any(tuple(x)in badcoords for x in p)}
 try:
  loops=cycles(ed);row['loops']=[u[x[::-1]].tolist()for x in loops];row['loopLabels']=[sorted({owner[(a,b)]for a,b in zip(x,np.roll(x,-1))})for x in loops]
 except Exception as ex:row['error']=str(ex)
 rows.append(row)
(W/'small-boundary-components.json').write_text(json.dumps(rows,indent=2)+'\n');(W/'native-scan.json').write_text(json.dumps({'scope':'All 766 named arterial meshes, exact per-label boundary cancellation; candidate-edge incidence checked separately.','reviewedMeshes':len(names),'largeComponentsExcluded':skipped,'perLabel':stats},indent=2)+'\n');(W/'source-assets.json').write_text(json.dumps(scene.source_hashes,indent=2)+'\n')
print('mixed bounded',[(i,r['labels'],round(r['spanMm'],5),r['touchesBadEdge'])for i,r in enumerate(rows)if len(r['labels'])>1 and r['spanMm']<=1],flush=True)
