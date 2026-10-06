"""Regularise local displacement across new discretised contact pairs.

The source skin is retained. A contact neighbourhood receives one common
posterior translation, so the source face pair keeps its original separation.
Every duplicate labelled coordinate is evaluated together. Fixed targets pin
the neighbourhood. This is an authoring refinement, never a viewer operation.
"""
import json
import numpy as np,trimesh
from scipy.spatial import cKDTree
from fit_vessels import APP,read_glb,write_glb,mesh_records
from reconcile_brainstem import WORK,update_normals
from verify_central_rebuild import contact_faces,self_contacts

def new_self_pairs(before,after):
    def pairs(mesh):
        a,b=contact_faces(mesh,mesh);keep=a<b;a,b=a[keep],b[keep]
        p,q=mesh.vertices[mesh.faces[a]],mesh.vertices[mesh.faces[b]]
        adjacent=(np.linalg.norm(p[:,:,None,:]-q[:,None,:,:],axis=3)<2e-5).any(axis=(1,2))
        return set(zip(a[~adjacent].tolist(),b[~adjacent].tolist()))
    before_pairs,after_pairs=pairs(before),pairs(after)
    return sorted(after_pairs-before_pairs) if len(after_pairs)>len(before_pairs) else []

def main():
    doc,data=read_glb(WORK/'brain-trial.glb');rec=mesh_records(doc,data)
    od,ob=read_glb(WORK/'brain-baseline.glb');old=mesh_records(od,ob)
    for k in rec:rec[k]['old']=old[k]['old']
    offsets={};p=[];q=[];cursor=0
    for k,r in rec.items():offsets[k]=cursor;p.append(r['old']);q.append(r['positions'].astype(float));cursor+=len(r['old'])
    p,q=np.concatenate(p),np.concatenate(q);unique,inverse=np.unique(np.round(p,5),axis=0,return_inverse=True)
    sums=np.zeros((len(unique),3));np.add.at(sums,inverse,p);counts=np.bincount(inverse);source=sums/counts[:,None]
    dy=np.bincount(inverse,weights=q[:,1]-p[:,1])/counts
    fixed=np.abs(dy)<1e-10;tree=cKDTree(source)
    changed={k for k in rec if not np.array_equal(rec[k]['positions'],old[k]['positions'])}
    baseline={k:trimesh.Trimesh(r['old'],r['faces'],process=False) for k,r in rec.items()}
    log=[]
    for iteration in range(16):
        meshes={k:trimesh.Trimesh(r['positions'],r['faces'],process=False) for k,r in rec.items()};groups=[]
        for key in changed:
            for a,b in new_self_pairs(baseline[key],meshes[key]):
                ids=np.unique(np.r_[rec[key]['faces'][a],rec[key]['faces'][b]])+offsets[key]
                groups.append((inverse[ids],False,key+' self'))
            for other in rec:
                if other==key or (other in changed and other<key) or any(t in other for t in ['sulc','lat-fis','ventricle','aqueduct']):continue
                ba,bb=contact_faces(baseline[key],baseline[other])
                if len(ba):continue
                a,b=contact_faces(meshes[key],meshes[other])
                for fa,fb in zip(a,b):
                    ids=np.unique(np.r_[rec[key]['faces'][fa]+offsets[key],rec[other]['faces'][fb]+offsets[other]])
                    groups.append((inverse[ids],other not in changed,key+' / '+other))
        if not groups:break
        # Union local collars so overlapping constraints have one displacement.
        parent=np.arange(len(unique));pinned=set()
        def find(i):
            while parent[i]!=i:parent[i]=parent[parent[i]];i=parent[i]
            return i
        for ids,pin,name in groups:
            collar=np.unique(np.concatenate(tree.query_ball_point(source[ids],r=.6+.12*iteration)))
            ids=np.unique(np.r_[ids,collar]);root=find(int(ids[0]))
            for i in ids:parent[find(int(i))]=root
            if pin or fixed[ids].any():pinned.add(int(ids[0]))
        roots=np.array([find(i) for i in range(len(unique))]);pinroots={find(i) for i in pinned}
        members={}
        for i in np.flatnonzero(roots!=np.arange(len(unique))):members.setdefault(int(roots[i]),[]).append(int(i))
        for root,ids in members.items():
            ids=np.r_[root,ids];dy[ids]=0 if root in pinroots else np.mean(dy[ids])
        for key,r in rec.items():
            ids=inverse[offsets[key]:offsets[key]+len(r['old'])];r['positions'][:]=r['old'];r['positions'][:,1]+=dy[ids]
        log.append({'iteration':iteration+1,'newContactPairs':len(groups),'localRigidCollars':len(members),'examples':sorted({name for _,_,name in groups})})
        print(log[-1],flush=True)
    update_normals(doc,data,rec);write_glb(WORK/'brain-trial.glb',doc,data)
    (WORK/'context-regularisation.json').write_text(json.dumps(log,indent=2)+'\n')

if __name__=='__main__':main()
