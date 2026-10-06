"""Z-ordered lateral midbrain venous skin transport with fixed outlet collars."""
import json
import numpy as np,trimesh
from scipy.interpolate import PchipInterpolator
from scipy.ndimage import gaussian_filter1d
from scipy.spatial import cKDTree
from fit_vessels import read_glb,mesh_records,write_glb,curve_from_mesh,ray_tree,hits,smoothstep
from reconcile_brainstem import WORK,LATERAL,update_normals
from refine_context_skin import subdivide,save_replaced

def main():
    d,b=read_glb(WORK/'veins-trial.glb');records=mesh_records(d,b)
    refined=subdivide(records,set(LATERAL),.6)
    replacements={k:(p,f,trimesh.Trimesh(p,f,process=False).vertex_normals) for k,(p,f) in refined.items()}
    save_replaced(WORK/'veins-lateral-source.glb',d,b,replacements)
    d,b=read_glb(WORK/'veins-lateral-source.glb');records=mesh_records(d,b)
    brain=trimesh.load(WORK/'brain-trial.glb',process=False)
    stem=ray_tree(trimesh.util.concatenate([m for k,m in brain.geometry.items() if any(t in k for t in ['midbrain.','pons.','base-of-peduncle'])]))
    reports=[]
    for key in LATERAL:
        r=records[key];p=r['old'];sign=1 if key.endswith('right') else -1
        other=np.concatenate([a['old'] for k,a in records.items() if k!=key]);distance=cKDTree(other).query(p)[0];shared=p[distance<2e-5]
        lower=shared[shared[:,2]<73,2].max();upper=shared[shared[:,2]>73,2].min()
        src=curve_from_mesh(trimesh.Trimesh(p,r['faces'],process=False),n=160);target=src.copy()
        for i,q in enumerate(src):
            y=-73.;origin=np.array([.65,y,q[2]]);h=hits(stem,[sign*100,y,q[2]],origin)
            if len(h):
                target[i]=h[np.argmax(sign*h[:,0])];target[i,0]+=sign*1.15
        delta=gaussian_filter1d(target-src,3,axis=0);delta[:,2]=0
        z=np.clip(p[:,2],src[0,2],src[-1,2]);shift=np.column_stack([PchipInterpolator(src[:,2],delta[:,k])(z) for k in range(3)])
        w=smoothstep((p[:,2]-lower-.3)/5)*(1-smoothstep((p[:,2]-upper+5.3)/5))
        r['positions'][:]=p+shift*w[:,None]
        r['positions'][distance<2e-5]=p[distance<2e-5]
        reports.append({'node':key,'lowerFixedCollarUpperZ':float(lower),'upperFixedCollarLowerZ':float(upper),'source':src.tolist(),'target':target.tolist(),'maximumDisplacementMm':float(np.linalg.norm(shift*w[:,None],axis=1).max())})
    update_normals(d,b,records);write_glb(WORK/'veins-trial.glb',d,b)
    (WORK/'lateral-fit.json').write_text(json.dumps(reports,indent=2)+'\n')
    print(json.dumps([{k:r[k] for k in ['node','lowerFixedCollarUpperZ','upperFixedCollarLowerZ','maximumDisplacementMm']} for r in reports]),flush=True)

if __name__=='__main__':main()
