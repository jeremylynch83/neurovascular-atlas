"""Remove only selected exact-zero-area faces, stage buffers and verify topology."""
from pathlib import Path
import sys,json,hashlib,numpy as np
from fractions import Fraction
from collections import Counter
A=Path(__file__).resolve().parents[2];sys.path.insert(0,str(A/'tools/repair'))
from cache import Scene
from geometry import edge_table
W=Path(sys.argv[1]).resolve();D=W/'decoded';overrides={}
for p in D.glob('*.positions.bin'):
 n=p.name[:-len('.positions.bin')];q=D/(n+'.indices.bin');overrides[n]={'positions':str(p),'indices':str(q),'positionSha256':hashlib.sha256(p.read_bytes()).hexdigest(),'indicesSha256':hashlib.sha256(q.read_bytes()).hexdigest()}
scene=Scene(A,Path(sys.argv[2]).resolve(),overrides);spec=json.load(open(W/'selection.json'));O=W/'replayed';O.mkdir(exist_ok=True);rows=[];removed_counts=Counter();removed_balances=Counter()
def exact_zero(t):
 a,b,c=[[Fraction(float(x))for x in p]for p in t];u=[y-x for x,y in zip(a,b)];v=[z-x for x,z in zip(a,c)];return u[1]*v[2]==u[2]*v[1]and u[2]*v[0]==u[0]*v[2]and u[0]*v[1]==u[1]*v[0]
def topology(v,f):
 u,e,c,b,_,_=edge_table(v,f);return {tuple(map(tuple,u[x]))for x in e[c==1]},{tuple(map(tuple,u[x]))for x in e[(c>2)|((c==2)&(b!=0))]}
for r in spec['selected']:
 n=r['node'];v,f=scene.mesh(n);ids=r['faceIds'];assert len(set(ids))==len(ids);proof=[]
 for i in ids:
  t=v[f[i]];assert exact_zero(t),(n,i,'positive-area-face-removal');proof.append({'sourceFace':i,'positions':t.tolist(),'exactZeroArea':True})
  q=list(map(tuple,t))
  for x,y in zip(q,q[1:]+q[:1]):
   edge=tuple(sorted([x,y]));removed_counts[edge]+=1;removed_balances[edge]+=1 if x<y else -1
 keep=np.ones(len(f),bool);keep[ids]=False;g=np.asarray(f[keep],dtype='<u4');v.tofile(O/(n+'.positions.bin'));g.tofile(O/(n+'.indices.bin'));boundary,bad=topology(v,f);postboundary,postbad=topology(v,g);assert postboundary<=boundary and postbad<=bad
 exact=None
 if (W/'accepted'/(n+'.indices.bin')).exists():
  exact=all((O/(n+'.'+kind+'.bin')).read_bytes()==(W/'accepted'/(n+'.'+kind+'.bin')).read_bytes()for kind in ['positions','indices']);assert exact
 rows.append({'node':n,'sourceVertices':len(v),'sourceTriangles':len(f),'triangles':len(g),'removedExactZeroAreaFaces':len(ids),'retainedSourceFaceIds':np.flatnonzero(keep).tolist(),'positionsByteExact':True,'allRetainedIndicesExact':True,'boundaryBefore':len(boundary),'boundaryAfter':len(postboundary),'badBefore':len(bad),'badAfter':len(postbad),'newBoundaryEdges':0,'newBadEdges':0,'replayedBuffersByteExact':exact,'proof':proof})
# Independently recount every affected edge in all 766 arterial source meshes.
expected={tuple(tuple(p)for p in r['edge']):r for r in spec['edges']};coords=np.asarray(sorted({p for edge in expected for p in edge}),dtype='<f4');dt=np.dtype([('x','<f4'),('y','<f4'),('z','<f4')]);match=coords.view(dt).reshape(-1);counts=Counter();balances=Counter();reviewed=0
for n in sorted(scene.rows):
 if scene.systems[n]!='artery':continue
 reviewed+=1;v,f=scene.mesh(n);mask=np.isin(np.asarray(v).view(dt).reshape(-1),match)
 if not mask.any():continue
 for a,b in [(0,1),(1,2),(2,0)]:
  ids=f[mask[f[:,a]]&mask[f[:,b]]]
  for i,j in ids[:,[a,b]]:
   x,y=tuple(v[i]),tuple(v[j]);edge=tuple(sorted([x,y]))
   if edge in expected:counts[edge]+=1;balances[edge]+=1 if x<y else -1
for edge,r in expected.items():
 assert(counts[edge],balances[edge])==(r['beforeCount'],r['beforeBalance']);after=counts[edge]-removed_counts[edge];balance=balances[edge]-removed_balances[edge];assert(after,balance)==(r['afterCount'],r['afterBalance']);assert not(after==1 and counts[edge]!=1);was_bad=counts[edge]>2 or(counts[edge]==2 and balances[edge]!=0);is_bad=after>2 or(after==2 and balance!=0);assert was_bad or not is_bad
report={'passed':True,'release':'0.9.104','reviewedArterialMeshes':reviewed,'globalEdgesChecked':len(expected),'globalBadEdgesBefore':spec['globalBadEdgesBefore'],'globalBadEdgesAfter':spec['globalBadEdgesAfter'],'globalBoundaryEdgesBefore':spec['globalBoundaryEdgesBefore'],'globalBoundaryEdgesAfter':spec['globalBoundaryEdgesAfter'],'changes':rows,'removedExactZeroAreaFaces':sum(r['removedExactZeroAreaFaces']for r in rows),'positiveAreaFacesRemoved':0,'verticesMoved':0,'newFaces':0,'newBoundaryEdges':0,'newBadEdges':0,'scope':'Exact-zero-area deletion only. All positive-area source faces, all vertex/normal data and exact source attachments are retained. No new crossings or tissue entry can be introduced without new/moved surface area.'};(W/'cleanup-validation.json').write_text(json.dumps(report,indent=2)+'\n');print({k:v for k,v in report.items()if k not in ['changes','scope']})
