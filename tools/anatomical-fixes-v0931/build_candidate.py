"""Compose only accepted local corrections from the unchanged release baseline."""
import sys,hashlib
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'anatomical-fixes-v0929'))
from geometry import *
OUT=ROOT.parent/'corrections-work';C=OUT/'candidate';C.mkdir(exist_ok=True)
if '--recorded' in sys.argv:
 fields=json.loads((Path(__file__).resolve().parents[2]/'docs/validation/anatomical-mesh-authoring-v0.9.31.json').read_text())['fields']
 upper=fields['upper'];lower=fields['lower'];ring=fields['ring']
else:
 upper=json.loads((OUT/'upper-context/revision.json').read_text());lower=json.loads((OUT/'common-refined/revision.json').read_text())
 ring=json.loads((OUT/'local-crossing-search.json').read_text())['ring']['best']
assert not upper['newContacts'] and not lower['newContacts'] and not ring['newContacts']
lower_names=set(lower['baseline']['changed']);lower_names={n for n in lower_names if meshes[n].file=='venous.glb'}
def bump(v,c,e,d,p):
 r=np.linalg.norm((v-np.array(c))/e,axis=1);w=1-smooth((r-p)/(1-p));return w[:,None]*np.array(d)
def transform(v,file,name):
 v=v.copy()
 if file in ['venous.glb','brain-context.glb']:
  for j in range(upper['steps']):
   c=np.array(upper['centre'])+np.array(upper['delta'])*j/upper['steps'];v+=bump(v,c,upper['extent'],np.array(upper['delta'])/upper['steps'],upper['plateau'])
 if file=='brain-context.glb' or name in lower_names:
  r=lower['baseline'];v+=bump(v,r['centre'],r['extent'],r['delta'],r['plateau'])
 for r in lower['refinements']:
  if file=='venous.glb' or (file=='brain-context.glb' and r['mode']=='common'):v+=bump(v,r['centre'],r['extent'],r['delta'],r['plateau'])
 if file=='venous.glb':v+=bump(v,ring['centre'],ring['extent'],ring['delta'],.6)
 return v
changed=[]
for n,m in meshes.items():
 m.new=transform(m.v,m.file,n)
 if np.max(abs(m.new-m.v))<1e-7:continue
 changed.append({'node':n,'file':m.file,'maximumDisplacementMm':float(np.linalg.norm(m.new-m.v,axis=1).max()),'topology':'retained'})
 m.new.astype('<f4').tofile(C/(n+'.positions.bin'));m.f.astype('<u4').tofile(C/(n+'.indices.bin'))
# Area-weighted normals on the joined asset, split only after common seam normals.
changed_names={r['node'] for r in changed}
for file in set(r['file'] for r in changed):
 names=[n for n,m in meshes.items() if m.file==file];vv=[];ff=[];offset=0
 for n in names:
  m=meshes[n];v=m.new.astype('<f4');vv.append(v);ff.append(m.f+offset);offset+=len(v)
 v=np.vstack(vv);f=np.vstack(ff);_,first,inv=np.unique(v,axis=0,return_index=True,return_inverse=True);uv=v[first].astype(float);uf=inv[f];tri=uv[uf];fn=np.cross(tri[:,1]-tri[:,0],tri[:,2]-tri[:,0]);normal=np.zeros_like(uv)
 for j in range(3):np.add.at(normal,uf[:,j],fn)
 normal/=np.maximum(np.linalg.norm(normal,axis=1)[:,None],1e-20);normal=normal[inv];offset=0
 for n in names:
  m=meshes[n]
  if n in changed_names:normal[offset:offset+len(m.new)].astype('<f4').tofile(C/(n+'.normals.bin'))
  offset+=len(m.new)
report={'release':'0.9.31','baselineRelease':'0.9.30','newLabels':[],'baselineAssetHashes':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in (ROOT/'baseline').glob('*.glb')},'changed':changed,'fields':{'upper':upper,'lower':lower,'ring':ring},'unchangedArterialGeometry':True}
(C/'revision.json').write_text(json.dumps(report,indent=2)+'\n');print('Candidate',len(changed),'labels',flush=True)
