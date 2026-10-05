"""Small shared-coordinate inferior adjustment of the intracavernous ICA region."""
import json,shutil
import numpy as np
from refine_cavernous import read_glb,write_glb,accessor,smoothstep
from reference import APP,ROOT

def lower_course(p):
    x,y,z=p.T;lat=np.abs(x-.65)
    weight=(smoothstep((z-57)/5)*(1-smoothstep((z-66)/6))*smoothstep((y+56)/5)*(1-smoothstep((y+43)/5))*smoothstep((lat-3)/4)*(1-smoothstep((lat-23)/5)))
    out=p.copy();out[:,2]-=.9*weight;return out

def run():
    baseline=ROOT/'baseline-v0.9.12';report={'release':'0.9.13','maximum_requested_inferior_adjustment_mm':.9,'files':{}}
    for name in ['circulation-refined.glb','anastomoses-refined.glb']:
        source=baseline/name;target=APP/'.authoring'/name
        if not source.exists():shutil.copy2(target,source)
        doc,data=read_glb(source);changed=[];min_det=1.;maximum_error=0.
        for node in doc['nodes']:
            if 'mesh' not in node:continue
            prim=doc['meshes'][node['mesh']]['primitives'][0]
            pos=accessor(doc,data,prim['attributes']['POSITION']);old=pos.astype(float);new=lower_course(old)
            delta=np.linalg.norm(new-old,axis=1);mask=delta>1e-6
            if not mask.any():continue
            jac=np.empty((len(old),3,3));h=.001
            for k in range(3):
                step=np.zeros(3);step[k]=h;jac[:,:,k]=(lower_course(old+step)-lower_course(old-step))/(2*h)
            det=np.linalg.det(jac);assert det.min()>.7;min_det=min(min_det,float(det.min()))
            normal=accessor(doc,data,prim['attributes']['NORMAL']);nn=np.linalg.solve(jac.transpose(0,2,1),normal.copy()[:,:,None])[:,:,0]
            nn/=np.linalg.norm(nn,axis=1)[:,None];normal[mask]=nn[mask]
            faces=accessor(doc,data,prim['indices']).reshape(-1,3)
            old_fn=np.cross(old[faces[:,1]]-old[faces[:,0]],old[faces[:,2]]-old[faces[:,0]])
            new_fn=np.cross(new[faces[:,1]]-new[faces[:,0]],new[faces[:,2]]-new[faces[:,0]])
            edge2=np.sum((old[faces]-old[faces[:,[1,2,0]]])**2,axis=2).max(1)
            stable=np.linalg.norm(old_fn,axis=1)>np.maximum(2e-6,edge2*.002)
            assert np.all(np.einsum('ij,ij->i',old_fn,new_fn)[stable]>0),node['name']
            pos[:]=new;assert np.array_equal(pos[~mask],old[~mask].astype(np.float32))
            doc['accessors'][prim['attributes']['POSITION']].update(min=pos.min(0).tolist(),max=pos.max(0).tolist())
            changed.append({'name':node['name'],'vertices_moved':int(mask.sum()),'maximum_displacement_mm':float(delta.max())})
        write_glb(target,doc,data)
        report['files'][name]={'changed_meshes':changed,'minimum_coordinate_field_jacobian_determinant':min_det,'unchanged_vertices_bit_identical':True}
    (APP/'docs/validation/cavernous-ica-lowering-v0.9.13.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2))
if __name__=='__main__':run()
