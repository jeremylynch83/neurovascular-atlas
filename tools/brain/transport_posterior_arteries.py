"""Carry existing posterior arterial skin with the local tissue coordinate map.

This preserves existing regional relationships; it is not a new arterial course
fit. Source faces are refined before the non-affine map. The established central
fit and every coordinate outside the posterior fossa support remain untouched.
"""
import json
import numpy as np,trimesh
from scipy.spatial import cKDTree
from fit_vessels import APP,read_glb,mesh_records
from reconcile_brainstem import WORK,ContextMap,selected_context
from refine_context_skin import subdivide,save_replaced

def main():
    d,b=read_glb(WORK/'arteries-baseline.glb');records=mesh_records(d,b)
    brain=trimesh.load(WORK/'brain-baseline.glb',process=False);bones=trimesh.load(APP/'.authoring/bones-baseline.glb',process=False)
    mapping=ContextMap(brain,bones,selected_context(json.loads((WORK/'manifest-baseline.json').read_text())))
    selected=set()
    for k,r in records.items():
        if k.startswith(('ICA ','MCA ','Central')):continue
        if np.max(np.linalg.norm(mapping.apply(r['old'])-r['old'],axis=1))>1e-5:selected.add(k)
    assert not any(k.startswith('ICA ') or k.startswith('Central') or k.startswith('MCA ') for k in selected),'Established anterior geometry would move'
    outside=np.concatenate([r['old'] for k,r in records.items() if k not in selected]);tree=cKDTree(outside)
    selected_points=np.concatenate([records[k]['old'] for k in selected]);shared=selected_points[tree.query(selected_points)[0]<2e-5];fixed=cKDTree(shared) if len(shared) else None
    refined=subdivide(records,selected,.8);source={};replacements={};changes=[]
    for k,(p,f) in refined.items():
        q=mapping.apply(p)
        if fixed:
            delta=p[:,1]-q[:,1];delta=np.minimum(delta,.3*fixed.query(p)[0]);q[:,1]=p[:,1]-delta
        a=trimesh.Trimesh(p,f,process=False);a2=trimesh.Trimesh(q,f,process=False)
        source[k]=(p,f,a.vertex_normals);replacements[k]=(q,f,a2.vertex_normals)
        changes.append({'node':k,'role':'coordinate-transport-retaining-source-relationship','maximumDisplacementMm':float(np.linalg.norm(q-p,axis=1).max()),'sourceVertices':len(records[k]['old']),'refinedVertices':len(p)})
    save_replaced(WORK/'arteries-source-refined.glb',d,b,source);save_replaced(WORK/'arteries-trial.glb',d,b,replacements)
    (WORK/'artery-changes.json').write_text(json.dumps(changes,indent=2)+'\n');print('Staged transported arteries',len(changes),flush=True)

if __name__=='__main__':main()
