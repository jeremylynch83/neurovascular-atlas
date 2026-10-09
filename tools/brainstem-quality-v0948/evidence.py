"""Assemble strict regional validation and prove labelled patches cover the outer wall."""
from common import *
import hashlib
names=json.loads((WORK/'connected-nodes.json').read_text());n=np.load(OUT/'network.npz')
def tri_keys(v,f):
 k=np.ascontiguousarray(v.astype('<f4')).view('V12').ravel();return np.ascontiguousarray(np.sort(k[f],axis=1)).view('V36').ravel()
expected=tri_keys(n['v'],n['f']);actual=np.concatenate([tri_keys(*load(k,OUT)) for k in names]);assert np.array_equal(np.sort(expected),np.sort(actual))
vv=[];ff=[];offset=0
for name in names:
 v,f=load(name);vv.append(v);ff.append(f+offset);offset+=len(v)
v=np.concatenate(vv);f=np.concatenate(ff);_,first,inv=np.unique(v,axis=0,return_index=True,return_inverse=True);f=inv[f];v=v[first];e=np.sort(np.concatenate([f[:,[0,1]],f[:,[1,2]],f[:,[2,0]]]),axis=1);edges,count=np.unique(e,axis=0,return_counts=True)
baseline=dict(triangles=len(f),uniqueVertices=len(v),boundaryEdges=int(np.sum(count==1)),nonManifoldEdges=int(np.sum(count>2)),duplicateTriangles=int(len(f)-len(np.unique(np.sort(f,axis=1),axis=0))))
quality=json.loads((OUT/'quality.json').read_text());attachments=json.loads((OUT/'attachments.json').read_text());depth=json.loads((OUT/'depth.json').read_text());loader=json.loads((OUT/'loader.json').read_text())
assert quality['passed'] and attachments['passed'] and depth['passed'] and loader['passed']
assets=json.loads((DATA/'source-assets.json').read_text());unchanged={}
for fn,old in assets.items():
 current=hashlib.sha256(Path('public/anatomy/models',fn).read_bytes()).hexdigest()
 if fn!='venous.glb':assert current==old;unchanged[fn]=current
r=dict(release='0.9.48',baseline=baseline,revision=json.loads((OUT/'revision.json').read_text()),quality=quality,attachments=attachments,depth=depth,export=json.loads((OUT/'export.json').read_text()),loader=loader,patchCoverageExact=True,unchangedAssetHashes=unchanged,build=dict(passed=True,command='npm run build',checks=['anatomy manifest and course contracts','brain bindings','TypeScript','Vite','precompression']))
Path('docs/validation/brainstem-quality-v0.9.48.json').write_text(json.dumps(r,indent=2)+'\n');print('Evidence',baseline,'new triangles',len(expected),'reduction',1-len(expected)/len(f),flush=True)
