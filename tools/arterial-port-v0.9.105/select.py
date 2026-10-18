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
from fractions import Fraction as Q
def positive(t):
 a,b,c=[[Q(float(x))for x in p]for p in t];u=[y-x for x,y in zip(a,b)];v=[z-x for x,z in zip(a,c)];return any(x!=0 for x in [u[1]*v[2]-u[2]*v[1],u[2]*v[0]-u[0]*v[2],u[0]*v[1]-u[1]*v[0]])
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
coords=np.asarray(sorted({p for edge in wanted for p in edge}),dtype='<f4');dt=np.dtype([('x','<f4'),('y','<f4'),('z','<f4')]);match=coords.view(dt).reshape(-1);counts=Counter();balances=Counter();incidence=defaultdict(list)
for n in scene.rows:
 if scene.systems[n]!='artery':continue
 v,f=scene.mesh(n);mask=np.isin(np.asarray(v).view(dt).reshape(-1),match)
 if not mask.any():continue
 for a,b in [(0,1),(1,2),(2,0)]:
  for fid in np.flatnonzero(mask[f[:,a]]&mask[f[:,b]]):
   i,j=f[fid,[a,b]]
   x,y=tuple(v[i]),tuple(v[j]);edge=tuple(sorted([x,y]))
   if edge in wanted:
    counts[edge]+=1;balances[edge]+=1 if x<y else -1;incidence[edge].append((n,int(fid),1 if x<y else -1,positive(v[f[fid]])))
for edge in wanted:constraints[('global',edge)]=(counts[edge],balances[edge])
# Exact subset search within components linked by a shared coordinate edge.
adj={ident:set()for ident in faces}
for values in effects.values():
 ids={v[0]for v in values}
 for ident in ids:adj[ident].update(ids-{ident})
components=[];unseen=set(faces)
while unseen:
 seed=min(unseen);todo=[seed];group=set()
 while todo:
  ident=todo.pop()
  if ident in group:continue
  group.add(ident);todo.extend(adj[ident]-group)
 unseen-=group;components.append(sorted(group))
print('GROUP SIZES',sorted(map(len,components),reverse=True),flush=True)
selected=set();search=[]
for group in components:
 assert len(group)<=20,('component needs a different exact solver',len(group))
 gs=set(group);local={k:v for k,v in constraints.items()if any(x[0]in gs for x in effects[k])};best=set();valid=0
 for bits in range(1<<len(group)):
  candidate={ident for j,ident in enumerate(group)if bits&(1<<j)}
  if len(candidate)<len(best):continue
  passed=True
  for key,(c,b)in local.items():
   active=[x for x in effects[key]if x[0]in candidate];pc=c-sum(x[1]for x in active);pb=b-sum(x[2]for x in active)
   prebad=c>2 or(c==2 and b!=0);postbad=pc>2 or(pc==2 and pb!=0)
   if postbad and not prebad:passed=False;break
   if pc==1 and c!=1:
    if key[0]=='global':passed=False;break
    retained=[r for r in incidence[key[1]]if(r[0],r[1])not in candidate]
    if len(retained)!=2 or len({r[0]for r in retained})!=2 or sum(r[2]for r in retained)!=0 or not all(r[3]for r in retained):passed=False;break
  if passed:
   valid+=1
   if len(candidate)>len(best)or(len(candidate)==len(best)and sorted(candidate)<sorted(best)):best=candidate
 selected.update(best);search.append({'faces':[list(x)for x in group],'subsetsEnumerated':1<<len(group),'selected':[list(x)for x in sorted(best)]})
rows=[]
for n in sorted({n for n,i in selected}):rows.append({'node':n,'faceIds':sorted(i for node,i in selected if node==n)})
edgeRows=[];bad0=bad1=bnd0=bnd1=0
for edge in sorted(wanted):
 c,b=constraints[('global',edge)];active=[x for x in effects[('global',edge)]if x[0]in selected];pc=c-sum(x[1]for x in active);pb=b-sum(x[2]for x in active)
 bad0+=c>2 or(c==2 and b!=0);bad1+=pc>2 or(pc==2 and pb!=0);bnd0+=c==1;bnd1+=pc==1
 edgeRows.append({'edge':[list(map(float,p))for p in edge],'beforeCount':c,'beforeBalance':b,'afterCount':pc,'afterBalance':pb})
report={'release':'0.9.105','selected':rows,'sourceZeroAreaFaces':len(faces),'removedZeroAreaFaces':len(selected),'remainingZeroAreaFaces':len(faces)-len(selected),'globalAffectedEdges':len(wanted),'globalBadEdgesBefore':int(bad0),'globalBadEdgesAfter':int(bad1),'globalBoundaryEdgesBefore':int(bnd0),'globalBoundaryEdgesAfter':int(bnd1),'newGlobalBoundaryEdges':0,'newBadEdges':0,'selectionMethod':'Exact component subset enumeration; newly exposed per-label edges must pair with positive-area retained neighbouring artery walls; no new global boundary or bad edge.','componentSearch':search,'retainedFaces':[{'node':n,'face':i}for n,i in sorted(set(faces)-selected)],'edges':edgeRows}
(W/'selection.json').write_text(json.dumps(report,indent=2)+'\n');print('SELECTED',len(selected),'of',len(faces),'faces',len(rows),'meshes','GLOBAL BAD',bad0,'->',bad1,'BOUNDARY',bnd0,'->',bnd1,flush=True)
