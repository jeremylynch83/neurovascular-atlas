"""Reuse exact source facet subdivision when updating only map constraints."""
import json,numpy as np,trimesh
from fit_vessels import read_glb,mesh_records
from reconcile_local_volume import WORK,VolumeMap,STEM,close_roundoff_holes
from reconcile_brainstem import sha
from refine_context_skin import save_replaced
brain=trimesh.load(WORK/'brain-baseline.glb',process=False);mapping=VolumeMap(brain)
doc,data=read_glb(WORK/'brain-baseline.glb');records=mesh_records(doc,data);source={};target={};changes=[]
for k in sorted(STEM):
 r=records[k];p,f=r['old'],r['faces'];holes=[]
 if brain.geometry[k].is_watertight:f,holes=close_roundoff_holes(p,f)
 q=mapping.apply(p);a,b=[trimesh.Trimesh(v,f,process=False) for v in [p,q]]
 source[k]=(p,f,a.vertex_normals);target[k]=(q,f,b.vertex_normals)
 changes.append({'node':k,'maximumDisplacementMm':float(mapping.amount(p).max()),'refinedVertices':len(p),'refinedTriangles':len(f),'closedSource':bool(a.is_watertight),'closedCandidate':bool(b.is_watertight),'roundoffHoleDiametersMm':holes,'volumeChangeFraction':float(abs(b.volume)/abs(a.volume)-1) if a.is_watertight else None})
 print(k,changes[-1],flush=True)
save_replaced(WORK/'brain-source-refined.glb',doc,data,source);save_replaced(WORK/'brain-trial.glb',doc,data,target)
np.savez_compressed(WORK/'volume-map.npz',origin=mapping.origin,delta=mapping.delta,mask=mapping.mask)
(WORK/'brain-changes.json').write_text(json.dumps(changes,indent=2)+'\n');(WORK/'map.json').write_text(json.dumps({'method':'fixed-interface tetrahedral map, exact source facet subdivision','minimumYDerivative':mapping.minimumYDerivative,'brainSha256':sha(WORK/'brain-trial.glb'),'protectedAnteriorArteriesAndCavernousVeins':True,'changes':changes},indent=2)+'\n')
