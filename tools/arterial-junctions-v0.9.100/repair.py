"""Replay explicit, validated mixed-label native wall patches. Never installs assets."""
from pathlib import Path
import sys,json,hashlib,numpy as np
A=Path(__file__).resolve().parents[2];sys.path.insert(0,str(A/'tools/repair'))
from cache import Scene
from geometry import patch_mesh,edge_table
from regional_validation import validate_regional
from global_edges import source_incidence,assess
W=Path(sys.argv[1]).resolve();CACHE=Path(sys.argv[2]).resolve();overrides={}
for p in (W/'decoded').glob('*.positions.bin'):
 n=p.name[:-len('.positions.bin')];q=W/'decoded'/(n+'.indices.bin');overrides[n]={'positions':str(p),'indices':str(q),'positionSha256':hashlib.sha256(p.read_bytes()).hexdigest(),'indicesSha256':hashlib.sha256(q.read_bytes()).hexdigest()}
scene=Scene(A,CACHE,overrides);spec=json.load(open(W/'accepted-patches.json'));proposals=spec['acceptedProposals'];assert len({p['id']for p in proposals})==len(proposals);boundaries={}
for proposal in proposals:
 coords=list(map(tuple,proposal['boundaryCoordinates']));wanted={(b,a)for a,b in zip(coords,coords[1:]+coords[:1])};owners=[]
 for n in proposal['boundaryLabels']:
  if n not in boundaries:
   v,f=scene.mesh(n);u,e,c,b,d,_=edge_table(v,f);boundaries[n]={(tuple(u[a]),tuple(u[b]))for a,b in d[c==1]}
  if boundaries[n]&wanted:owners.append(n)
 assert len(owners)>=2 and proposal['target']in owners,('not-a-mixed-label-native-wall-gap',proposal['id'])
O=W/'replayed';O.mkdir(exist_ok=True);C={};checks=[]
for n in sorted({p['target']for p in proposals}):
 pp=[p for p in proposals if p['target']==n];p,g,added=patch_mesh(scene,n,pp);C[n]=(p,g);p.tofile(O/(n+'.positions.bin'));g.tofile(O/(n+'.indices.bin'))
 original,indices=scene.mesh(n);assert np.array_equal(p[:len(original)],original);assert np.array_equal(g[:len(indices)],indices)
 exact=all((O/(n+'.'+kind+'.bin')).read_bytes()==(W/'accepted'/(n+'.'+kind+'.bin')).read_bytes()for kind in ['positions','indices']);checks.append({'node':n,'candidateBuffersByteExact':exact});assert exact,n
network=json.load(open(W/'native-scan.json'))['network'];report=validate_regional(scene,C,[{'id':network['id'],'nodes':network['nodes']}])
c,b,m=source_incidence(scene,proposals);certificate=assess(proposals,c,b,m);(W/'replay-global-edge-validation.json').write_text(json.dumps(certificate,indent=2)+'\n');assert certificate['passed'],certificate['issues']
(O/'validation.json').write_text(json.dumps(report,indent=2)+'\n');(W/'replay-validation.json').write_text(json.dumps({'passed':report['passed'],'checks':checks},indent=2)+'\n');print({'passed':report['passed'],'issues':report['issues'],'trianglePairsChecked':report['trianglePairsChecked'],'nativeNetworks':report['nativeNetworks'],'replayedBuffers':checks});sys.exit(0 if report['passed']else 1)
