"""Replay explicit, validated mixed-label native wall patches. Never installs assets."""
from pathlib import Path
import sys,json,hashlib,numpy as np
A=Path(__file__).resolve().parents[2];sys.path.insert(0,str(A/'tools/repair'))
from cache import Scene
from geometry import patch_mesh
from regional_validation import validate_regional
W=Path(sys.argv[1]).resolve();CACHE=Path(sys.argv[2]).resolve();overrides={}
for p in (W/'decoded').glob('*.positions.bin'):
 n=p.name[:-len('.positions.bin')];q=W/'decoded'/(n+'.indices.bin');overrides[n]={'positions':str(p),'indices':str(q),'positionSha256':hashlib.sha256(p.read_bytes()).hexdigest(),'indicesSha256':hashlib.sha256(q.read_bytes()).hexdigest()}
scene=Scene(A,CACHE,overrides);spec=json.load(open(W/'accepted-patches.json'));proposals=spec['acceptedProposals'];assert len({p['id']for p in proposals})==len(proposals);O=W/'replayed';O.mkdir(exist_ok=True);C={};checks=[]
for n in sorted({p['target']for p in proposals}):
 pp=[p for p in proposals if p['target']==n];p,g,added=patch_mesh(scene,n,pp);C[n]=(p,g);p.tofile(O/(n+'.positions.bin'));g.tofile(O/(n+'.indices.bin'))
 original,indices=scene.mesh(n);assert np.array_equal(p[:len(original)],original);assert np.array_equal(g[:len(indices)],indices)
 exact=all((O/(n+'.'+kind+'.bin')).read_bytes()==(W/'accepted'/(n+'.'+kind+'.bin')).read_bytes()for kind in ['positions','indices']);checks.append({'node':n,'candidateBuffersByteExact':exact});assert exact,n
network=json.load(open(W/'native-scan.json'))['network'];report=validate_regional(scene,C,[{'id':network['id'],'nodes':network['nodes']}]);(O/'validation.json').write_text(json.dumps(report,indent=2)+'\n');(W/'replay-validation.json').write_text(json.dumps({'passed':report['passed'],'checks':checks},indent=2)+'\n');print({'passed':report['passed'],'issues':report['issues'],'trianglePairsChecked':report['trianglePairsChecked'],'nativeNetworks':report['nativeNetworks'],'replayedBuffers':checks});sys.exit(0 if report['passed']else 1)
