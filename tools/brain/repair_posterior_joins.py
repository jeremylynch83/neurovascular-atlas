"""Close two missed arterial attachments in the native labelled solid."""
import json,shutil
import numpy as np,trimesh,manifold3d as mf
from scipy.spatial import cKDTree
from fit_vessels import APP,read_glb,mesh_records,accessor,curve_from_mesh,resample
from rebuild_tubular_brainstem_veins import tube
from refine_context_skin import save_replaced
from reconcile_brainstem import sha

def main():
    src=APP/'.authoring/posterior-round60';w=APP/'.authoring/posterior-round61';w.mkdir(exist_ok=True)
    for p in src.iterdir():
        if p.is_file() and p.suffix in ['.glb','.json']:shutil.copyfile(p,w/p.name)
    doc,buf=read_glb(src/'arteries-trial.glb');rr=mesh_records(doc,buf);names=list(rr)
    skin=trimesh.load(src/'arteries-collision-solid.glb',force='mesh',process=False)
    centroids=[];tags=[]
    for j,k in enumerate(names):
        m=rr[k];centroids.append(m['old'][m['faces']].mean(1));tags.extend([j]*len(m['faces']))
    distance,index=cKDTree(np.concatenate(centroids)).query(skin.triangles.mean(1));labels=np.array(tags)[index];labels[distance>3e-5]=len(names)
    order=np.argsort(labels,kind='stable');faces=skin.faces[order];lab=labels[order];values,first=np.unique(lab,return_index=True);base=mf.Manifold.reserve_ids(len(names)+5)
    solid=mf.Manifold(mf.Mesh(skin.vertices.astype(np.float32),faces.astype(np.uint32),run_index=np.r_[first*3,len(faces)*3].astype(np.uint32),run_original_id=(base+values).astype(np.uint32)))
    assert solid.status()==mf.Error.NoError,solid.status()
    courses=json.loads((src/'arteries-round-courses.json').read_text());connectors=[]
    # The junction lies inside the parent and child lumina, so the Boolean
    # union removes terminal caps and leaves a single shared external skin.
    q=np.array(courses['PCA P1 right']['points']);bas=trimesh.Trimesh(rr['Basilar']['old'],rr['Basilar']['faces'],process=False);bc=curve_from_mesh(bas,axis=2,n=160)
    end=q[-1];parent=bc[np.abs(bc[:,2]-76.5).argmin()];d=end-q[-8];d/=np.linalg.norm(d)
    connectors.append(('PCA P1 right','Basilar',resample(np.vstack([end-d*.6,end,parent]),40),.55))
    k='SCA proximal perforator left';m=trimesh.Trimesh(rr[k]['old'],rr[k]['faces'],process=False);pc=curve_from_mesh(m,axis=1,n=50);sq=np.array(courses['SCA left']['points']);dd,j=cKDTree(sq).query(pc);i=dd.argmin();root=pc[i];parent=sq[j[i]];end=pc[max(0,i-7)] if i>len(pc)//2 else pc[min(len(pc)-1,i+7)]
    connectors.append((k,'SCA left',resample(np.vstack([parent,root,end]),40),.135))
    solids=[solid];report=[]
    for child,parent,q,r in connectors:
        v,f=tube(q,np.full(len(q),r),sides=40);part=mf.Manifold(mf.Mesh(v,f,run_index=np.array([0,len(f)*3],np.uint32),run_original_id=np.array([base+names.index(child)],np.uint32)))
        assert part.status()==mf.Error.NoError,(child,part.status());solids.append(part);report.append({'child':child,'parent':parent,'connectorRadiusMm':r,'points':q.tolist()})
    union=mf.Manifold.batch_boolean(solids,mf.OpType.Add);assert union.status()==mf.Error.NoError,union.status();mesh=union.to_mesh();v=np.array(mesh.vert_properties[:,:3]);f=np.array(mesh.tri_verts);labels=np.zeros(len(f),int)
    for i,oid in enumerate(mesh.run_original_id):labels[mesh.run_index[i]//3:mesh.run_index[i+1]//3]=int(oid)-base
    trimesh.Trimesh(v,f,process=False).export(w/'arteries-collision-solid.glb')
    keep=labels<len(names);f,labels=f[keep],labels[keep];normal=np.zeros_like(v);fn=np.cross(v[f[:,1]]-v[f[:,0]],v[f[:,2]]-v[f[:,0]])
    for i in range(3):np.add.at(normal,f[:,i],fn)
    normal/=np.maximum(np.linalg.norm(normal,axis=1)[:,None],1e-12);replace={}
    for j in np.unique(labels):
        ff=f[labels==j];used,inv=np.unique(ff,return_inverse=True);replace[names[j]]=(v[used],inv.reshape(-1,3),normal[used])
    save_replaced(w/'arteries-trial.glb',doc,buf,replace)
    out={'repairs':report,'closedSolid':union.status()==mf.Error.NoError,'arteriesSha256':sha(w/'arteries-trial.glb')};(w/'join-repairs.json').write_text(json.dumps(out,indent=2)+'\n');print('Repaired joins',[(r['child'],r['parent']) for r in report],flush=True)

if __name__=='__main__':main()
