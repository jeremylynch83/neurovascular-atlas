"""Fit surface veins with a shared section-preserving, bounded AP shear.

Unlike vertex projection, this cannot flatten a circular section onto the
tissue. Source facets are split at every affine field boundary first.
"""
import argparse,json,shutil
import numpy as np,trimesh,vtk
from vtk.util.numpy_support import vtk_to_numpy
from scipy.interpolate import RegularGridInterpolator
from scipy.spatial import cKDTree
from scipy.sparse import coo_matrix,hstack,vstack,eye
from scipy.optimize import linprog
from fit_vessels import APP,read_glb,mesh_records,smoothstep
from fit_brainstem_shear import ShearGrid
from reconcile_anterior_brainstem import split_mesh,InterfaceMap
from refine_context_skin import save_replaced
from seat_posterior_candidate import locator,front_fn
from reconcile_brainstem import ANTERIOR,TRANSVERSE,LATERAL,sha

def main():
    p=argparse.ArgumentParser();p.add_argument('--output',default='.authoring/posterior-shear51');p.add_argument('--cached-source',action='store_true');a=p.parse_args();out=APP/a.output;out.mkdir(exist_ok=True)
    for k in ['brain','arteries']:
        for s in ['source','trial']:shutil.copyfile(APP/'.authoring/posterior-seated50'/f'{k}-{s}.glb',out/f'{k}-{s}.glb')
    brain=trimesh.load(out/'brain-trial.glb',process=False);stem=trimesh.util.concatenate([m for k,m in brain.geometry.items() if any(t in k for t in ['pons.','midbrain.','medulla-oblongata','base-of-peduncle'])]);front=front_fn(locator(stem))
    d,b=read_glb(out/'veins-source.glb' if a.cached_source else APP/'.authoring/posterior-family40/veins-trial.glb');rr=mesh_records(d,b);keys=set(ANTERIOR+TRANSVERSE+LATERAL+['vein.anterior_spinal']+[f'vein.{k}.{s}' for k in ['superior_petrosal_vein','cerebellopontine_fissure'] for s in ['left','right']])
    outer=cKDTree(np.concatenate([r['old'] for k,r in rr.items() if k not in keys]));shared=np.concatenate([r['old'][outer.query(r['old'])[0]<2e-5] for k,r in rr.items() if k in keys]);tree=cKDTree(shared);g=ShearGrid();g.x=np.arange(-34.,36.);g.z=np.arange(-5.,96.);g.shape=(len(g.x),len(g.z));N=np.prod(g.shape);frozen=np.zeros(g.shape,bool);frozen[[0,-1],:]=True;frozen[:,[0,-1]]=True;ids,_=g.rows(shared);frozen.ravel()[ids.ravel()]=True
    # Freeze whole cells crossed by actual shared outlet edges.
    for k in keys:
        r=rr[k];v=r['old'];s=outer.query(v)[0]<2e-5;edges=np.vstack([r['faces'][:,[0,1]],r['faces'][:,[1,2]],r['faces'][:,[2,0]]])
        for edge in edges[s[edges].all(1)]:
            q=v[edge][:,[0,2]];lo=np.maximum(np.floor(q.min(0)-[g.x[0],g.z[0]]).astype(int),0);hi=np.minimum(np.floor(q.max(0)-[g.x[0],g.z[0]]).astype(int)+1,np.array(g.shape)-1);frozen[lo[0]:hi[0]+1,lo[1]:hi[1]+1]=True
    # Collector nodes may move with the local family. Bone proximity limits
    # their displacement in physical 3D space instead of freezing unrelated
    # vessel courses which happen to share the same X/Z grid coordinates.
    frozen[:]=False;frozen[[0,-1],:]=True;frozen[:,[0,-1]]=True
    shared_xz=cKDTree(shared[:,[0,2]])
    sources={};row=[];col=[];data=[];rhs=[];constraints=0
    constrained=set(ANTERIOR+TRANSVERSE+['vein.anterior_spinal'])
    for k in sorted(keys):
        r=rr[k]
        if a.cached_source:v,f=r['old'],r['faces']
        else:
            tmp=trimesh.Trimesh(r['old'][:,[1,0,2]],r['faces'],process=False);v,f=split_mesh(tmp,InterfaceMap.__new__(InterfaceMap));v=v[:,[1,0,2]]
        m=trimesh.Trimesh(v,f,process=False);sources[k]=(v,f,m.vertex_normals)
        if k in constrained:
            points=np.vstack([v,m.triangles.mean(1)]);ids,w=g.rows(points);free=np.ones(len(points),bool)
            if k in TRANSVERSE:free&=abs(points[:,0]-.65)<10
            for i in np.flatnonzero(free):
                q=points[i];y=front(q[0],q[2])
                if y is None:continue
                row.extend([constraints]*3);col.extend(ids[i]);data.extend(-w[i]);rhs.append(q[1]-y);constraints+=1
        print('Affine source refined',k,len(v),flush=True)
    edges=[]
    for i in range(g.shape[0]):
        for j in range(g.shape[1]):
            q=i*g.shape[1]+j
            if i+1<g.shape[0]:edges.append([q,q+g.shape[1]])
            if j+1<g.shape[1]:edges.append([q,q+1])
    edges=np.array(edges);K=len(edges);E=coo_matrix((np.tile([1.,-1.],K),(np.repeat(np.arange(K),2),edges.ravel())),shape=(K,N)).tocsr();A=coo_matrix((data,(row,col)),shape=(constraints,N)).tocsr();Z=lambda a,c:coo_matrix((a,c));I=eye(N)
    xx,zz=np.meshgrid(g.x,g.z,indexing='ij');desired=2*(1-smoothstep((abs(xx-.65)-18)/10))*smoothstep((zz-18)/10)*(1-smoothstep((zz-74)/13));desired[frozen]=0
    matrices=[hstack([A,Z(constraints,N+K)]),hstack([I,-I,Z(N,K)]),hstack([-I,-I,Z(N,K)]),hstack([E,Z(K,N),Z(K,K)]),hstack([-E,Z(K,N),Z(K,K)]),hstack([E,Z(K,N),-eye(K)]),hstack([-E,Z(K,N),-eye(K)])]
    limits=np.r_[rhs,desired.ravel(),-desired.ravel(),np.full(2*K,3.),np.zeros(2*K)]
    result=linprog(np.r_[np.full(N,.2),np.full(N,.05),np.full(K,.02)],A_ub=vstack(matrices).tocsr(),b_ub=limits,bounds=[(0,0) if fix else (0,30) for fix in frozen.ravel()]+[(0,None)]*(N+K),method='highs',options={'time_limit':55})
    report={'solverSuccess':bool(result.success),'message':result.message,'wallConstraints':constraints,'maximumFieldEdgeSlope':3.,'coordinateJacobianDeterminant':1.,'fixedGridBoundaryOnly':True,'coordinateJacobianAppliesToUncappedShearOnly':True,'accepted':False,'appliedToApp':False};(out/'solver.json').write_text(json.dumps(report,indent=2)+'\n');print(report,flush=True)
    if not result.success:raise SystemExit(1)
    g.delta=result.x[:N].reshape(g.shape);targets={}
    bones=trimesh.load(APP/'.authoring/bones-baseline.glb',process=False);bone=trimesh.util.concatenate([m for k,m in bones.geometry.items() if k in ['bone.occipital','bone.sphenoid','bone.temporal.right','bone.temporal.left']])
    from build_targets import poly
    implicit=vtk.vtkImplicitPolyDataDistance();implicit.SetInput(poly(bone));sample=vtk.vtkSampleFunction();sample.SetImplicitFunction(implicit);sample.SetModelBounds(-35,36,-135,-40,-5,96);sample.SetSampleDimensions(72,96,102);sample.ComputeNormalsOff();sample.Update();volume=abs(vtk_to_numpy(sample.GetOutput().GetPointData().GetScalars()).reshape(102,96,72).transpose(2,1,0));D=RegularGridInterpolator((np.arange(-35.,37.),np.arange(-135.,-39.),np.arange(-5.,97.)),volume,bounds_error=False,fill_value=0)
    # Include adjoining labels in the same physical coordinate map, retaining
    # material continuity while keeping the clival plexus stationary.
    for k,r in rr.items():
        if k=='vein.basilar_plexus':continue
        v,f,n=sources[k] if k in sources else (r['old'],r['faces'],None)
        q=g.apply(v);shift=q[:,1]-v[:,1];support=smoothstep((v[:,1]+135)/20)*(1-smoothstep((v[:,1]+51)/11));shift*=support;limit=.9*np.maximum(D(v)-.05,0);q[:,1]=v[:,1]+np.clip(shift,-limit,limit)
        if np.max(abs(q-v))<1e-7 and k not in sources:continue
        m=trimesh.Trimesh(q,f,process=False);targets[k]=(q,f,m.vertex_normals)
    save_replaced(out/'veins-source.glb',d,b,sources);save_replaced(out/'veins-trial.glb',d,b,targets);np.savez_compressed(out/'surface-shear.npz',x=g.x,z=g.z,delta=g.delta,frozen=frozen)
    report.update({'baseAnteriorShiftMm':2.,'requestedWallSurfaceSeparationMm':0.,'collectorNodesMoveWithinBoneLimits':True,'basilarPlexusFixed':True,'hashes':{k:sha(out/f'{k}-trial.glb') for k in ['brain','arteries','veins']}});(out/'trial.json').write_text(json.dumps(report,indent=2)+'\n')

if __name__=='__main__':main()
