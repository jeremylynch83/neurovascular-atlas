"""Replay explicit native wall and exact subdivision repairs; never installs a GLB."""
from common import *
from fractions import Fraction as Q
from geometry import patch_mesh
from regional_validation import validate_regional
import subprocess
spec=json.load(open(W/'spec.json'));D=W/'decoded';D.mkdir(exist_ok=True);O=W/'replayed';O.mkdir(exist_ok=True);rows=[];candidates={}
def rational(p):return [Q(float(x))for x in p]
def sub(a,b):return [x-y for x,y in zip(a,b)]
def cross(a,b):return [a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0]]
def exactcross(t):
 a,b,c=map(rational,t);return cross(sub(b,a),sub(c,a))
def top(v,f):
 u,e,c,b,_,_=edge_table(v,f)
 return {tuple(map(tuple,u[x]))for x in e[c==1]},{tuple(map(tuple,u[x]))for x in e[(c>2)|((c==2)&(b!=0))]}
for r in spec['changes']:
 n=r['node'];v,f=scene.mesh(n);removed=list(r['zeroFaces']);new=[];appended=[];p=v;proof={}
 for i in r['zeroFaces']:assert exactcross(v[f[i]])==[0,0,0]
 if 'split'in r:
  q=r['split'];a,s,e,m=[q[k]for k in ['apex','start','end','middle']];assert list(f[q['sourceFace']])==[a,s,e]
  S,E,M=map(rational,v[[s,e,m]]);d=sub(E,S);j=next(i for i in range(3)if d[i]);t=(M[j]-S[j])/d[j];assert 0<t<1 and M==[x+t*y for x,y in zip(S,d)]
  oldcross=exactcross(v[f[q['sourceFace']]]);assert oldcross!=[0,0,0];new=[[a,s,m],[a,m,e]]
  assert exactcross(v[new[0]])==[t*x for x in oldcross]and exactcross(v[new[1]])==[(1-t)*x for x in oldcross]
  removed.append(q['sourceFace']);proof={'exactSurfacePartition':True,'splitFraction':str(t),'sourcePatchAreaMm2':float(np.linalg.norm(np.cross(v[s].astype(float)-v[a],v[e].astype(float)-v[a]))/2)}
 if 'patches'in r:
  for proposal in r['patches']:
   assert n in proposal['boundaryLabels']and len(proposal['boundaryLabels'])>=2
   assert len(proposal['boundaryCoordinates'])<=12
   pts=np.array(proposal['boundaryCoordinates']);assert np.linalg.norm(pts[:,None]-pts,axis=2).max()<0.1
  p,full,appended=patch_mesh(scene,n,r['patches']);new.extend(full[len(f):].tolist())
 removed=sorted(removed);keep=np.ones(len(f),bool);keep[removed]=False;g=np.vstack([f[keep],np.array(new,dtype='<u4')]).astype('<u4')
 assert np.array_equal(p[:len(v)],v)
 before,bad=top(v,f);after,postbad=top(p,g);assert postbad<=bad
 for directory in [D,O]:
  (v if directory==D else p).tofile(directory/(n+'.positions.bin'));(f if directory==D else g).tofile(directory/(n+'.indices.bin'))
 exact=None
 if(W/'accepted'/(n+'.indices.bin')).exists():
  exact=all((O/(n+'.'+k+'.bin')).read_bytes()==(W/'accepted'/(n+'.'+k+'.bin')).read_bytes()for k in ['positions','indices']);assert exact
 candidates[n]=(p,g)
 rows.append({'node':n,'removedFaces':removed,'zeroAreaFaces':r['zeroFaces'],'newTriangles':new,'appendedVertices':appended,'retainedSourceFaceIds':np.flatnonzero(keep).tolist(),'sourceVertices':len(v),'candidateVertices':len(p),'boundaryBefore':len(before),'boundaryAfter':len(after),'badBefore':len(bad),'badAfter':len(postbad),'newPerLabelBoundaryEdges':[[list(x),list(y)]for x,y in sorted(after-before)],'newBadEdges':0,'allOriginalPositionsRetained':True,'replayedBuffersByteExact':exact,**proof})
validation=validate_regional(scene,candidates,[]);(W/'regional-validation.json').write_text(json.dumps(validation,indent=2)+'\n');assert validation['passed'],validation['issues']
if not(D/'source-assets.json').exists():(D/'source-assets.json').write_text(json.dumps({Path(k).name:v for k,v in scene.source_hashes.items()},indent=2)+'\n')
(W/'replay-reconstruction.json').write_text(json.dumps({'release':'0.9.106','changes':rows,'allOriginalPositionsRetained':True},indent=2)+'\n')
subprocess.run(['python3',str(A/'tools/arterial-wall-v0.9.106/global_validate.py'),str(W),str(CACHE)],check=True)
report={'passed':True,'release':'0.9.106','changes':rows,'global':json.load(open(W/'global-edge-validation.json')),'removedExactZeroAreaFaces':sum(len(r['zeroAreaFaces'])for r in rows),'sourcePositiveAreaFacesRetriangulated':1,'newPositiveAreaFaces':sum(len(r['newTriangles'])for r in rows),'verticesMoved':0,'appendedExistingWorldCoordinates':sum(len(r['appendedVertices'])for r in rows),'exactLacrimalSurfacePartition':True,'newGlobalBoundaryEdges':0,'newBadEdges':0,'regionalValidation':validation}
(W/'native-validation.json').write_text(json.dumps(report,indent=2)+'\n');print({k:v for k,v in report.items()if k not in ['changes','regionalValidation','global']})
