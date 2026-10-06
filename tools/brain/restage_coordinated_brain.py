"""Reuse the same tetrahedral material facets with revised fixed boundaries."""
import json,numpy as np,trimesh
from fit_vessels import read_glb,mesh_records
from reconcile_local_volume import WORK,VolumeMap,close_roundoff_holes,split_mesh
from reconcile_brainstem import sha
from refine_context_skin import save_replaced
brain=trimesh.load(WORK/'brain-baseline.glb',process=False);mapping=VolumeMap(brain)
doc,data=read_glb(WORK/'brain-baseline.glb');baseline=mesh_records(doc,data);sd,sb=read_glb(WORK/'brain-source-refined.glb');records=mesh_records(sd,sb);source={};target={};changes=[]
for k in sorted(mapping.selected):
 r=records[k];p,f=r['old'],r['faces'];maximum=float(mapping.amount(p).max())
 if maximum<1e-5:continue
 if np.array_equal(f,baseline[k]['faces']) and np.array_equal(p,baseline[k]['old']):
  p,f=split_mesh(trimesh.Trimesh(p,f,process=False))
 holes=[]
 if brain.geometry[k].is_watertight:f,holes=close_roundoff_holes(p,f)
 q=mapping.apply(p);a,b=[trimesh.Trimesh(v,f,process=False) for v in [p,q]];source[k]=(p,f,a.vertex_normals);target[k]=(q,f,b.vertex_normals)
 changes.append({'node':k,'maximumDisplacementMm':maximum,'refinedVertices':len(p),'refinedTriangles':len(f),'closedSource':bool(a.is_watertight),'closedCandidate':bool(b.is_watertight),'roundoffHoleDiametersMm':holes,'volumeChangeFraction':float(abs(b.volume)/abs(a.volume)-1) if a.is_watertight else None})
save_replaced(WORK/'brain-source-refined.glb',doc,data,source);save_replaced(WORK/'brain-trial.glb',doc,data,target);np.savez_compressed(WORK/'volume-map.npz',origin=mapping.origin,delta=mapping.delta,mask=mapping.mask)
(WORK/'brain-changes.json').write_text(json.dumps(changes,indent=2)+'\n');(WORK/'map.json').write_text(json.dumps({'method':'coordinated fixed-interface tetrahedral map','minimumYDerivative':mapping.minimumYDerivative,'brainSha256':sha(WORK/'brain-trial.glb'),'changes':changes},indent=2)+'\n')
print([(r['node'],r['volumeChangeFraction']) for r in changes if r['closedSource']],flush=True)
