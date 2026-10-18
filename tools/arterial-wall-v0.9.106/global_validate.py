"""Independently count changed coordinate edges against all 766 arterial source meshes."""
from common import *
from fractions import Fraction as Q
from collections import Counter,defaultdict
spec=json.load(open(W/'spec.json'));replay=json.load(open(W/'replay-reconstruction.json'));delta=Counter();db=Counter();candidates={}
def add(t,sign):
 t=list(map(tuple,t))
 for x,y in zip(t,t[1:]+t[:1]):
  e=tuple(sorted([x,y]));delta[e]+=sign;db[e]+=sign*(1 if x<y else -1)
def positive(t):
 a,b,c=[[Q(float(x))for x in p]for p in t];u=[y-x for x,y in zip(a,b)];v=[z-x for x,z in zip(a,c)]
 return any(x!=0 for x in [u[1]*v[2]-u[2]*v[1],u[2]*v[0]-u[0]*v[2],u[0]*v[1]-u[1]*v[0]])
for r in replay['changes']:
 n=r['node'];v,f=scene.mesh(n);p=np.fromfile(W/'replayed'/(n+'.positions.bin'),'<f4').reshape(-1,3);g=np.fromfile(W/'replayed'/(n+'.indices.bin'),'<u4').reshape(-1,3);candidates[n]=(p,g)
 for i in r['removedFaces']:add(v[f[i]],-1)
 for t in r['newTriangles']:add(p[t],1)
keys=set(delta);coords=np.asarray(sorted({p for e in keys for p in e}),dtype='<f4');dt=np.dtype([('x','<f4'),('y','<f4'),('z','<f4')]);match=coords.view(dt).reshape(-1)
def collect(use_candidates):
 counts=Counter();balances=Counter();inc=defaultdict(list);reviewed=0
 for n in sorted(scene.rows):
  if scene.systems[n]!='artery':continue
  reviewed+=1;v,f=candidates[n]if use_candidates and n in candidates else scene.mesh(n);mask=np.isin(np.asarray(v).view(dt).reshape(-1),match)
  if not mask.any():continue
  for a,b in [(0,1),(1,2),(2,0)]:
   for fid in np.flatnonzero(mask[f[:,a]]&mask[f[:,b]]):
    i,j=f[fid,[a,b]];x,y=tuple(v[i]),tuple(v[j]);e=tuple(sorted([x,y]))
    if e in keys:
     direction=1 if x<y else -1;counts[e]+=1;balances[e]+=direction;inc[e].append({'node':n,'face':int(fid),'direction':direction,'positiveArea':positive(v[f[fid]])})
 assert reviewed==766;return counts,balances,inc
before,bal0,inc0=collect(False);after,bal1,inc1=collect(True);rows=[];bad0=set();bad1=set();bnd0=set();bnd1=set()
for e in sorted(keys):
 c,b=before[e],bal0[e];pc,pb=after[e],bal1[e];assert(pc,pb)==(c+delta[e],b+db[e])
 if c>2 or(c==2 and b!=0):bad0.add(e)
 if pc>2 or(pc==2 and pb!=0):bad1.add(e)
 if c==1:bnd0.add(e)
 if pc==1:bnd1.add(e)
 rows.append({'edge':[list(map(float,p))for p in e],'sourceCount':c,'sourceBalance':b,'candidateCount':pc,'candidateBalance':pb})
assert bad1<=bad0 and bnd1<=bnd0
zero={r['node']:set(r['zeroFaces'])for r in spec['changes']};ports=[];patch_boundary=[]
for r in spec['changes']:
 for patch in r.get('patches',[]):
  q=list(map(tuple,patch['boundaryCoordinates']));owners=set()
  for x,y in zip(q,q[1:]+q[:1]):
   e=tuple(sorted([x,y]));direction=1 if x<y else -1
   source=[v for v in inc0[e]if v['face']not in zero.get(v['node'],set())]
   assert len(source)==1 and source[0]['positiveArea']and source[0]['direction']==-direction
   owners.add(source[0]['node']);assert after[e]==2 and bal1[e]==0 and all(i['positiveArea']for i in inc1[e])
   patch_boundary.append({'edge':[list(map(float,p))for p in e],'sourceWall':source[0],'oppositePairedCandidateIncidences':inc1[e]})
  assert owners==set(patch['boundaryLabels'])and r['node']in owners and len(owners)>=2
for r in replay['changes']:
 for x,y in r['newPerLabelBoundaryEdges']:
  e=tuple(sorted([tuple(x),tuple(y)]));w=inc1[e];assert len(w)==2 and len({i['node']for i in w})==2 and sum(i['direction']for i in w)==0 and all(i['positiveArea']for i in w)
  ports.append({'edge':[x,y],'oppositePairedCandidateIncidences':w})
# Both lacrimal subdivision edges must pair with the named native neighbour.
subdivision=[]
for r in spec['changes']:
 if 'split'not in r:continue
 v,f=scene.mesh(r['node']);q=r['split']
 for a,b in [(q['start'],q['middle']),(q['middle'],q['end'])]:
  e=tuple(sorted(map(tuple,v[[a,b]])));w=inc1[e];assert after[e]==2 and bal1[e]==0 and {i['node']for i in w}=={'Lacrimal right','Lateral superior palpebral right'}and all(i['positiveArea']for i in w)
  subdivision.append({'edge':[list(map(float,p))for p in e],'oppositePairedCandidateIncidences':w})
report={'passed':True,'reviewedArterialMeshes':766,'sourceAndCandidateIndependentlyRecounted':True,'affectedEdges':len(keys),'badEdgesBefore':len(bad0),'badEdgesAfter':len(bad1),'boundaryEdgesBefore':len(bnd0),'boundaryEdgesAfter':len(bnd1),'newBadEdges':0,'newGlobalBoundaryEdges':0,'pairedPatchBoundaryEdges':len(patch_boundary),'newPerLabelEdgesOppositePaired':len(ports),'pairedLacrimalSubdivisionEdges':len(subdivision),'patchBoundary':patch_boundary,'newPerLabelPortProofs':ports,'lacrimalSubdivision':subdivision,'edges':rows}
(W/'global-edge-validation.json').write_text(json.dumps(report,indent=2)+'\n');print({k:v for k,v in report.items()if k not in ['patchBoundary','newPerLabelPortProofs','lacrimalSubdivision','edges']})
