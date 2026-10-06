"""Offline connected-skin fit against the accepted v0.9.19 context.

Welded material coordinates are the optimisation variables. All retained
attachments are pinned exactly; no production asset is written by this tool.
"""
import argparse, json
import numpy as np, trimesh
from scipy.spatial import cKDTree
from scipy.sparse import coo_matrix
from scipy.optimize import minimize
from fit_vessels import APP, read_glb, mesh_records, neighbours, ray_tree, hits, write_glb
from fit_brainstem_shear import SELECTED
from reconcile_brainstem import ANTERIOR, TRANSVERSE, update_normals, sha

W=APP/'.authoring/connected-anterior20'

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--experimental',action='store_true');args=parser.parse_args()
    assert args.experimental, 'Authoring-only candidate requires --experimental'
    W.mkdir(exist_ok=True)
    source=APP/'.authoring/brainstem19/veins-baseline.glb'
    doc,data=read_glb(source);records=mesh_records(doc,data)
    selected=neighbours(records,SELECTED)
    keys=sorted(selected);lengths=[len(records[k]['old']) for k in keys]
    old=np.concatenate([records[k]['old'] for k in keys])
    _,first,inverse=np.unique(np.round(old,5),axis=0,return_index=True,return_inverse=True)
    p=old[first];N=len(p)
    retained=np.concatenate([r['old'] for k,r in records.items() if k not in selected])
    fixed=cKDTree(retained).query(p)[0]<1e-5
    brain=trimesh.load(APP/'public/anatomy/models/brain-context.glb',process=False)
    stem=ray_tree(trimesh.util.concatenate([m for k,m in brain.geometry.items() if any(s in k for s in ['pons.','medulla-oblongata','midbrain.','base-of-peduncle'])]))
    bones=trimesh.load(APP/'.authoring/bones-baseline.glb',process=False)
    bone=ray_tree(trimesh.util.concatenate(list(bones.geometry.values())))
    cache={}
    def limits(q):
        key=tuple(np.round(q[[0,2]],5))
        if key not in cache:
            h=hits(stem,[q[0],5,q[2]],[q[0],-145,q[2]])
            front=float(h[:,1].max()) if len(h) else None
            h=hits(bone,[q[0],-135,q[2]],[q[0],20,q[2]])
            h=h[h[:,1]>(front+.1 if front is not None else -110)]
            roof=float(h[:,1].min()) if len(h) else None
            cache[key]=(front,roof)
        return cache[key]
    lower=np.full(N,-12.);upper=np.full(N,15.);wish=np.zeros(N);count=np.zeros(N)
    edges=[];weights=[];offset=0
    primary=set(ANTERIOR+TRANSVERSE+['vein.anterior_spinal'])
    for k,n in zip(keys,lengths):
        r=records[k];ids=inverse[offset:offset+n];offset+=n
        e=np.unique(np.sort(np.vstack([r['faces'][:,[0,1]],r['faces'][:,[1,2]],r['faces'][:,[2,0]]]),axis=1),axis=0)
        axis=0 if k in TRANSVERSE or k=='vein.posterior_communicating' else 2
        dp=r['old'][e[:,1]]-r['old'][e[:,0]];length=np.linalg.norm(dp,axis=1)
        # Strong within-section coherence preserves the transverse wall shape.
        weight=2.+35.*np.exp(-(abs(dp[:,axis])/.18)**2)
        edges.extend(ids[e]);weights.extend(weight/np.maximum(length,.08)**2)
        if k in primary:
            l=np.full(n,-12.);u=np.full(n,15.)
            for i,q in enumerate(r['old']):
                if k=='vein.anterior_spinal' and q[2]<15:continue
                front,roof=limits(q)
                if front is not None:l[i]=front+.25-q[1]
                if roof is not None:u[i]=roof-.25-q[1]
            # Include material facet interiors, not only centreline or vertices.
            for face,q in zip(r['faces'],r['old'][r['faces']].mean(1)):
                if k=='vein.anterior_spinal' and q[2]<15:continue
                front,roof=limits(q)
                if front is not None:l[face]=np.maximum(l[face],front+.25-q[1])
                if roof is not None:u[face]=np.minimum(u[face],roof-.25-q[1])
            np.maximum.at(lower,ids,l);np.minimum.at(upper,ids,u)
            target=np.clip(l+.15,-8,12)
            if k=='vein.anterior_spinal':target[r['old'][:,2]<15]=0
            np.add.at(wish,ids,target);np.add.at(count,ids,1)
        print('Constraints',k,flush=True)
    wish=np.divide(wish,count,out=np.zeros(N),where=count>0)
    lower[fixed]=0;upper[fixed]=0;wish[fixed]=0
    invalid=np.flatnonzero(lower>upper)
    if len(invalid):
        (W/'infeasible-bounds.json').write_text(json.dumps([{'point':p[i].tolist(),'lowerMm':float(lower[i]),'upperMm':float(upper[i])} for i in invalid],indent=2))
        raise RuntimeError(f'{len(invalid)} incompatible wall bounds')
    edges=np.array(edges);weights=np.array(weights);row=np.repeat(np.arange(len(edges)),2)
    D=coo_matrix((np.tile([-1.,1.],len(edges)),(row,edges.ravel())),shape=(len(edges),N)).tocsr()
    fidelity=np.where(count>0,1.,.35)
    def objective(v):
        a=v-wish;b=D@v
        return .5*(np.sum(fidelity*a*a)+np.sum(weights*b*b)),fidelity*a+D.T@(weights*b)
    fit=minimize(objective,np.clip(wish,lower,upper),method='L-BFGS-B',jac=True,bounds=list(zip(lower,upper)),options={'maxiter':1800,'ftol':1e-11,'gtol':1e-5,'maxcor':15})
    displacement=fit.x[inverse];offset=0
    for k,n in zip(keys,lengths):
        records[k]['positions'][:,1]=records[k]['old'][:,1]+displacement[offset:offset+n];offset+=n
    changes=update_normals(doc,data,records)
    candidate=W/'veins-trial.glb';write_glb(candidate,doc,data)
    report={'method':'welded material wall coordinates, section-weighted smooth AP offsets','solverSuccess':bool(fit.success),'message':fit.message,'iterations':fit.nit,'sourceSha256':sha(source),'candidateSha256':sha(candidate),'brainSha256':sha(APP/'public/anatomy/models/brain-context.glb'),'selectedLabels':keys,'fixedSharedCoordinates':int(fixed.sum()),'changes':changes,'productionWritten':False}
    (W/'fit.json').write_text(json.dumps(report,indent=2)+'\n')
    np.savez_compressed(W/'fit-material.npz',source=p,offsets=fit.x,fixed=fixed,lower=lower,upper=upper)
    print(json.dumps({'solver':fit.message,'iterations':fit.nit,'changes':changes},indent=2),flush=True)

if __name__=='__main__':main()
