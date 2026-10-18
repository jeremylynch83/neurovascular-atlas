"""Select a conservative subset of exact-zero-area deletions; never edit a model."""
from pathlib import Path
import sys,json,hashlib,numpy as np
A=Path(__file__).resolve().parents[2];sys.path.insert(0,str(A/'tools/repair'))
from cache import Scene
from geometry import edge_table
W=Path(sys.argv[1]).resolve();overrides={}
for p in (W/'decoded').glob('*.positions.bin'):
 n=p.name[:-len('.positions.bin')];q=p.with_name(n+'.indices.bin')
 overrides[n]={'positions':str(p),'indices':str(q),'positionSha256':hashlib.sha256(p.read_bytes()).hexdigest(),'indicesSha256':hashlib.sha256(q.read_bytes()).hexdigest()}
scene=Scene(A,Path(sys.argv[2]).resolve(),overrides)
from collections import Counter,defaultdict
scan=json.load(open(W/'degenerate-scan.json'));constraints={};effects=defaultdict(list);faces={};wanted=set()
def edges(tri):
 q=list(map(tuple,tri));c=Counter();b=Counter()
 for x,y in zip(q,q[1:]+q[:1]):
  e=tuple(sorted([x,y]));c[e]+=1;b[e]+=1 if x<y else -1
 return c,b
for row in scan['rows']:
 n=row['node'];v,f=scene.mesh(n);u,e,c,b,_,_=edge_table(v,f);source={tuple(map(tuple,u[x])):(int(cc),int(bb))for x,cc,bb in zip(e,c,b)}
 for i in row['zeroAreaFaceIds']:
  ident=(n,i);faces[ident]=True;dc,db=edges(v[f[i]])
  for edge in dc:
   wanted.add(edge);key=(n,edge);constraints[key]=source[edge];effects[key].append((ident,dc[edge],db[edge]));effects[('global',edge)].append((ident,dc[edge],db[edge]))
coords=np.asarray(sorted({p for edge in wanted for p in edge}),dtype='<f4');dt=np.dtype([('x','<f4'),('y','<f4'),('z','<f4')]);match=coords.view(dt).reshape(-1);counts=Counter();balances=Counter()
for n in scene.rows:
 if scene.systems[n]!='artery':continue
 v,f=scene.mesh(n);mask=np.isin(np.asarray(v).view(dt).reshape(-1),match)
 if not mask.any():continue
 for a,b in [(0,1),(1,2),(2,0)]:
  for i,j in f[mask[f[:,a]]&mask[f[:,b]]][:,[a,b]]:
   x,y=tuple(v[i]),tuple(v[j]);edge=tuple(sorted([x,y]))
   if edge in wanted:counts[edge]+=1;balances[edge]+=1 if x<y else -1
for edge in wanted:constraints[('global',edge)]=(counts[edge],balances[edge])
selected=set(faces);passes=[];guarded={}
while True:
 remove=set();violations=[]
 for key,(c,b)in constraints.items():
  active=[x for x in effects[key]if x[0]in selected];pc=c-sum(x[1]for x in active);pb=b-sum(x[2]for x in active);prebad=c>2 or(c==2 and b!=0);postbad=pc>2 or(pc==2 and pb!=0)
  if(pc==1 and c!=1)or(postbad and not prebad):
   why='new-boundary-edge'if pc==1 and c!=1 else 'new-bad-edge';violations.append({'scope':key[0],'reason':why,'faces':[list(x[0])for x in active]})
   for x in active:remove.add(x[0]);guarded.setdefault(x[0],[]).append({'scope':key[0],'reason':why})
 if not remove:break
 passes.append({'facesGuarded':len(remove),'violatingConstraints':len(violations)});selected-=remove
assert selected
rows=[]
for n in sorted({n for n,i in selected}):
 ids=sorted(i for node,i in selected if node==n);rows.append({'node':n,'faceIds':ids})
edgeRows=[];bad0=bad1=bnd0=bnd1=0
for edge in sorted(wanted):
 c,b=constraints[('global',edge)];active=[x for x in effects[('global',edge)]if x[0]in selected];pc=c-sum(x[1]for x in active);pb=b-sum(x[2]for x in active);bad0+=c>2 or(c==2 and b!=0);bad1+=pc>2 or(pc==2 and pb!=0);bnd0+=c==1;bnd1+=pc==1;edgeRows.append({'edge':[list(map(float,p))for p in edge],'beforeCount':c,'beforeBalance':b,'afterCount':pc,'afterBalance':pb})
report={'release':'0.9.104','selected':rows,'sourceZeroAreaFaces':len(faces),'removedZeroAreaFaces':len(selected),'remainingZeroAreaFaces':len(faces)-len(selected),'globalAffectedEdges':len(wanted),'globalBadEdgesBefore':int(bad0),'globalBadEdgesAfter':int(bad1),'globalBoundaryEdgesBefore':int(bnd0),'globalBoundaryEdgesAfter':int(bnd1),'newBoundaryEdges':0,'newBadEdges':0,'selectionMethod':'Conservative monotone guard propagation from local and global edge constraints; not an optimiser.','guardPasses':passes,'guardedFaces':[{'node':n,'face':i,'reasons':r}for(n,i),r in sorted(guarded.items())],'edges':edgeRows};(W/'selection.json').write_text(json.dumps(report,indent=2)+'\n');print('SELECTED',len(selected),'of',len(faces),'faces',len(rows),'meshes','GLOBAL BAD',bad0,'->',bad1,'BOUNDARY',bnd0,'->',bnd1,'passes',passes,flush=True)
