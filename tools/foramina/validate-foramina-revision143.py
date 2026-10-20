"""Optional authoring QA. NumPy, Trimesh, VTK and python-fcl required."""
from pathlib import Path
import json,hashlib,numpy as np,trimesh
from geometry import Glb
from revision143_surface_qa import check
A=Path(__file__).resolve().parents[2];P=A/'anatomy/source/foramina';meta=json.load(open(P/'revision143-qa-reference.json'));masks=np.load(P/'revision143-patch-masks.npz');g=Glb(A/'public/anatomy/models/craniofacial.glb');report={'release':json.load(open(A/'public/anatomy/manifest.json'))['release'],'temporal':{},'boneTopology':{}}
def digest(a,dt):return hashlib.sha256(np.asarray(a,dtype=dt).tobytes()).hexdigest()
p,f,n=g.mesh('bone.ethmoid');ff=np.take_along_axis(f,(f.argmin(1)[:,None]+np.arange(3))%3,axis=1);got={'positions':digest(p,'<f4'),'triangles':digest(ff,'<u4'),'normals':digest(n,'<f4')};assert got==meta['ethmoidOriginal'],'Restored ethmoid differs from original source';report['ethmoidOriginalRestored']=True
for side in ['right','left']:
 p,f,n=g.mesh('bone.temporal.'+side);assert len(f)==meta['temporalFaceCounts'][side],'Regenerate regional masks after remeshing';mask=np.unpackbits(masks[side])[:len(f)].astype(bool);r={'self':check(p,f[mask]),'sourceJoin':check(p,f[mask],f[~mask])};assert r['self']['materialCrossings']==r['sourceJoin']['materialCrossings']==0;report['temporal'][side]=r
for name in ['bone.ethmoid','bone.sphenoid','bone.occipital','bone.temporal.right','bone.temporal.left','bone.maxilla.right','bone.maxilla.left','maxillary-alveolar-process-left','maxillary-alveolar-process-right']:
 p,f,n=g.mesh(name);t=trimesh.Trimesh(p,f,process=False);counts=np.bincount(t.edges_unique_inverse);r={'vertices':len(p),'triangles':len(f),'windingConsistent':bool(t.is_winding_consistent),'nonManifoldEdges':int((counts>2).sum()),'openBoundaryEdges':int((counts==1).sum())};assert r['windingConsistent']and r['nonManifoldEdges']==0,name;report['boneTopology'][name]=r
(A/'docs/foramina-revision143-saved-geometry.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report),flush=True)
