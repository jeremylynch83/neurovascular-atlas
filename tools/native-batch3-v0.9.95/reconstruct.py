"""Replay the explicit batch-three authoring inputs, without installing assets.

Requires NumPy, SciPy, VTK and manifold3d 3.5.4. Outputs need regional validation.
"""
import sys,json,hashlib
from pathlib import Path
import numpy as np
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'repair'))
from cache import Scene
from geometry import snap_seam
from collar import build_collar
from union_native import exterior_union
W,A,C=map(Path,sys.argv[1:4]);B=W/'decoded';O=W/'replayed';O.mkdir(exist_ok=True)
def load(n):return np.fromfile(B/(n+'.positions.bin'),'<f4').reshape(-1,3),np.fromfile(B/(n+'.indices.bin'),'<u4').reshape(-1,3)
overrides={}
for p in B.glob('*.positions.bin'):
 n=p.name[:-len('.positions.bin')];q=B/(n+'.indices.bin');overrides[n]={'positions':str(p.resolve()),'indices':str(q.resolve()),'positionSha256':hashlib.sha256(p.read_bytes()).hexdigest(),'indicesSha256':hashlib.sha256(q.read_bytes()).hexdigest()}
scene=Scene(A,C,overrides);v,f=load('ILT anterior branch left');w,g=load('Inferolateral trunk left');compound=(np.vstack([v,w]),np.vstack([f,g+len(v)]))
class Reference:
 def mesh(self,n):return compound if n=='__ILT_root_compound__'else scene.mesh(n)
 def nearby(self,lo,hi):return scene.nearby(lo,hi)
p,g,detail=snap_seam(Reference(),{'target':'ILT posterior branch left','parent':'__ILT_root_compound__'},{'maxSnapMm':1.,'snapSupportMm':1.})
parts={'ILT posterior branch left':(p,g)};spec=json.load(open(W/'occipital/screened.json'));origin=np.array(spec['cutOrigin']);normal=np.array(spec['cutNormal']);centre=origin-normal*2
v,f=load('Occipital mastoid left');w,g=load('Occipital left');p,h,collar=build_collar(v,f,w,g,centre,origin,normal,steps=12)
union,reports=exterior_union({'Occipital left':(w,g),'Occipital mastoid left':(p,h)},centre,local_cap_radius=1.);parts.update(union)
for n,(v,f)in parts.items():v.astype('<f4').tofile(O/(n+'.positions.bin'));f.astype('<u4').tofile(O/(n+'.indices.bin'))
(O/'reconstruction.json').write_text(json.dumps({'ilt':detail,'occipital':collar,'union':reports},indent=2)+'\n');print('Staged',list(parts))
