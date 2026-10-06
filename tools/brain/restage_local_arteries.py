"""Reuse material facets for mapped posterior and adjoining arterial labels."""
import json,numpy as np,trimesh
from fit_vessels import APP,read_glb,mesh_records
from transport_local_volume import load_map
from reconcile_local_volume import WORK,split_mesh
from refine_context_skin import save_replaced
mapping=load_map();bd,bb=read_glb(APP/'.authoring/brainstem19/arteries-baseline.glb');baseline=mesh_records(bd,bb);sd,sb=read_glb(WORK/'arteries-source-refined.glb');old=mesh_records(sd,sb);already={r['node'] for r in json.loads((WORK/'artery-changes.json').read_text())};source={};target={};changes=[]
for k,r in baseline.items():
 allowed=k.startswith(('Basilar','PCA ','SCA ','AICA ','PICA ','Pontine ','Anterior spinal','Posterior spinal','Vertebral V3','Vertebral V4','VA medullary','Medial posterior choroidal','Thalamoperforator','Peduncular perforator','PCom perforator','Posterior communicating','Anterior choroidal','AChA optic tract','AChA peduncular','AChA capsular','Tuberothalamic','Anterior thalamoperforating'))
 if k.startswith(('ICA ','MCA ','Central')):assert mapping.amount(r['old']).max()<1e-7
 if not allowed or mapping.amount(r['old']).max()<1e-5:continue
 if k in already:p,f=old[k]['old'],old[k]['faces']
 else:p,f=split_mesh(trimesh.Trimesh(r['old'],r['faces'],process=False))
 q=mapping.apply(p);a,b=[trimesh.Trimesh(v,f,process=False) for v in [p,q]];source[k]=(p,f,a.vertex_normals);target[k]=(q,f,b.vertex_normals);changes.append({'node':k,'role':'parent-transition' if k.startswith('Vertebral V3') else 'retained-posterior-relationship-transport','maximumDisplacementMm':float(mapping.amount(p).max()),'sourceTriangles':len(r['faces']),'refinedTriangles':len(f)})
save_replaced(WORK/'arteries-source-refined.glb',bd,bb,source);save_replaced(WORK/'arteries-trial.glb',bd,bb,target);(WORK/'artery-changes.json').write_text(json.dumps(changes,indent=2)+'\n');print('Staged',len(changes),flush=True)
