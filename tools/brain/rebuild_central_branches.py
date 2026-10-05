"""Review-only cortical branch reconstruction with independent supported courses.

The primary-cleared checkpoint is an input, never a production asset. Branches
are rebuilt from the baseline wall in moving transverse frames. All original
label boundary coordinates are bound to the primary checkpoint and all other
labels are copied exactly. Triangle contact checks remain the acceptance gate.
"""
import argparse, heapq, json, itertools, hashlib
from pathlib import Path
import numpy as np, trimesh, vtk
from scipy.spatial import cKDTree
from scipy.interpolate import PchipInterpolator,RBFInterpolator
from scipy.spatial.transform import Rotation
from scipy.ndimage import gaussian_filter1d
from fit_vessels import APP, read_glb, write_glb, accessor, mesh_records, curve_from_mesh, smoothstep
from build_targets import poly
from verify_fitting import collisions

def implicit(mesh):
    f=vtk.vtkImplicitPolyDataDistance();f.SetInput(poly(mesh));return f

def regularise_terminal(record):
    """Replace the folded right terminal field with ordered whole sections.

    Terminal target X/Y depend only on the original Z station. Its superior
    map has a derivative of at least 0.5; the transition blend still requires
    the complete exported-skin checks. The connected
    branch joins are inferior to this edit and retain their exact checkpoint
    positions. Actual wall contacts are checked after reconstruction.
    """
    old=record['old'];current=record['positions'].astype(float);z=old[:,2]
    stations=np.linspace(144,155,180);delta=[]
    for station in stations:
        distance=np.abs(z-station);ids=np.argsort(distance)[:45]
        weights=np.exp(-distance[ids]**2/.18**2)
        delta.append(np.average((current-old)[ids,:2],axis=0,weights=weights))
    delta=gaussian_filter1d(np.array(delta),2.,axis=0)
    target=old.copy()
    for k in [0,1]:target[:,k]+=PchipInterpolator(stations,delta[:,k])(np.clip(z,stations[0],stations[-1]))
    target[:,2]-=2.5*smoothstep((z-145)/7.5)
    weight=smoothstep((z-146)/2.5)
    record['positions'][:]=current+(target-current)*weight[:,None]

def frames(curve):
    tangent=np.gradient(curve,axis=0);tangent/=np.linalg.norm(tangent,axis=1)[:,None]
    # Rotation-minimising frames avoid a normal flip when a branch turns
    # superiorly. A fixed-reference cross product becomes singular there.
    normal=np.zeros_like(tangent);normal[0]=np.cross(tangent[0],[0,0,1]);normal[0]/=np.linalg.norm(normal[0])
    for i in range(1,len(curve)):
        axis=np.cross(tangent[i-1],tangent[i]);s=np.linalg.norm(axis);c=np.clip(np.dot(tangent[i-1],tangent[i]),-1,1)
        normal[i]=Rotation.from_rotvec(axis/s*np.arctan2(s,c)).apply(normal[i-1]) if s>1e-10 else normal[i-1]
        normal[i]-=tangent[i]*np.dot(normal[i],tangent[i]);normal[i]/=np.linalg.norm(normal[i])
    binormal=np.cross(tangent,normal)
    return np.stack([tangent,normal,binormal],axis=2)

def transport(wall,source,target):
    # Source Y stations preserve cross-sections and avoid branch/root ambiguity.
    t=np.linspace(0,1,len(source));order=np.argsort(source[:,1]);ys=source[order,1]
    keep=np.r_[True,np.diff(ys)>1e-5]
    def linear(x,xp,fp):
        y=np.interp(x,xp,fp)
        left=x<xp[0];right=x>xp[-1]
        y[left]=fp[0]+(x[left]-xp[0])*(fp[1]-fp[0])/(xp[1]-xp[0])
        y[right]=fp[-1]+(x[right]-xp[-1])*(fp[-1]-fp[-2])/(xp[-1]-xp[-2])
        return y
    # An exact piecewise linear inverse retains a positive longitudinal
    # Jacobian even on nearly lateral segments. Linear endpoint continuation
    # preserves the skin cap; clamping would flatten those wall sections.
    param=linear(wall[:,1],ys[keep],t[order][keep])
    def sample(q):return np.column_stack([linear(param,t,q[:,k]) for k in range(3)])
    sf,df=frames(source),frames(target)
    # Refine the source correspondence along its local tangent, rather than
    # treating a world-Y plane as a transverse vessel section.
    speed=np.linalg.norm(np.gradient(source,t,axis=0),axis=1)
    for _ in range(4):
        s=sample(source);tangent=np.column_stack([np.interp(param,t,sf[:,k,0]) for k in range(3)]);tangent/=np.linalg.norm(tangent,axis=1)[:,None]
        param+=np.sum((wall-s)*tangent,axis=1)/np.interp(param,t,speed)
    def sample_frame(f):
        tangent=np.column_stack([np.interp(param,t,f[:,k,0]) for k in range(3)]);tangent/=np.linalg.norm(tangent,axis=1)[:,None]
        normal=np.column_stack([np.interp(param,t,f[:,k,1]) for k in range(3)]);normal-=tangent*np.sum(normal*tangent,axis=1)[:,None];normal/=np.linalg.norm(normal,axis=1)[:,None]
        return np.stack([tangent,normal,np.cross(tangent,normal)],axis=2)
    s,d=sample(source),sample(target);a,b=sample_frame(sf),sample_frame(df)
    local=np.einsum('nji,nj->ni',a,wall-s)
    return d+np.einsum('nij,nj->ni',b,local),param

def plan(root,wish,functions,nearby,sign,step=.7,clearance=.65,primary=None,join_root=None):
    # Finite regional search. Keep the path intracranial by remaining in the
    # connected free component of the root, with bone shell clearance.
    lo=np.array([min(root[0],wish[0])-7,min(root[1],wish[1])-5,root[2]-1])
    hi=np.array([max(root[0],wish[0])+7,root[1]+2,160.])
    axes=[np.arange(a,b+step,step) for a,b in zip(lo,hi)]
    grid=np.stack(np.meshgrid(*axes,indexing='ij'),axis=-1);flat=grid.reshape(-1,3)
    ds=np.full(len(flat),np.inf)
    for f in functions:ds=np.minimum(ds,np.array([f.EvaluateFunction(p) for p in flat]))
    tissue=np.array([min(f.EvaluateFunction(p) for f in nearby) for p in flat])
    valid=(ds>=clearance)&(np.abs(flat[:,0])>12)
    if primary is not None:
        main_distance=np.array([primary.EvaluateFunction(p) for p in flat])
        join_root=root if join_root is None else join_root
        valid&=(np.linalg.norm(flat-join_root,axis=1)<1.1)|(main_distance>=.5)
    shape=grid.shape[:3];ids=np.flatnonzero(valid)
    assert len(ids),'No clearance grid'
    start=int(ids[np.argmin(np.linalg.norm(flat[ids]-root,axis=1))])
    # Prefer a supported distal outlet near the requested branch endpoint.
    goals=ids[(tissue[ids]<2.2)&(flat[ids,1]<root[1]-5)&(ds[ids]>=max(clearance,1.15))]
    goal=int(goals[np.argmin(np.linalg.norm(flat[goals]-wish,axis=1))])
    neighbours=[np.array(q) for q in itertools.product([-1,0,1],repeat=3) if q!=(0,0,0) and q[1]<=0]
    dist={start:0.};parent={};queue=[(np.linalg.norm(flat[start]-flat[goal]),start)]
    while queue:
        _,i=heapq.heappop(queue)
        if i==goal:break
        coord=np.array(np.unravel_index(i,shape))
        for off in neighbours:
            q=coord+off
            if np.any(q<0) or np.any(q>=shape):continue
            j=int(np.ravel_multi_index(q,shape))
            if not valid[j]:continue
            length=np.linalg.norm(off)*step
            cost=dist[i]+length*(1+.12*max(0,tissue[j]-1.2)+.08/(ds[j]-.3))
            if cost<dist.get(j,np.inf):
                dist[j]=cost;parent[j]=i
                heapq.heappush(queue,(cost+np.linalg.norm(flat[j]-flat[goal]),j))
    if goal not in dist:
        # A branch must progress posteriorly. Choose the nearest supported
        # reachable outlet rather than accepting a loop back round the bank.
        reachable=[i for i in goals if i in dist]
        assert reachable,'No posteriorly progressing intracranial branch corridor'
        goal=min(reachable,key=lambda i:np.linalg.norm(flat[i]-wish)+.12*dist[i])
    path=[goal]
    while path[-1]!=start:path.append(parent[path[-1]])
    q=np.vstack([root,flat[path[::-1]]])
    # Remove duplicate and string-pull only through tested free space.
    q=q[np.r_[True,np.linalg.norm(np.diff(q,axis=0),axis=1)>1e-4]]
    def free(a,b):
        points=a+np.linspace(0,1,max(3,int(np.linalg.norm(a-b)/.2)))[:,None]*(b-a)
        return all(all(f.EvaluateFunction(p)>=clearance-.08 for f in functions) and (primary is None or np.linalg.norm(p-join_root)<1.1 or primary.EvaluateFunction(p)>=.45) for p in points)
    result=[q[0]];i=0
    while i<len(q)-1:
        j=len(q)-1
        while j>i+1 and not free(q[i],q[j]):j-=1
        result.append(q[j]);i=j
    route=np.array(result)
    arc=np.r_[0,np.cumsum(np.linalg.norm(np.diff(route,axis=0),axis=1))]
    target=np.column_stack([np.interp(np.linspace(0,arc[-1],160),arc,route[:,k]) for k in range(3)])
    target=gaussian_filter1d(target,5.,axis=0);target[0]=root
    # Lateral segments need a positive longitudinal Jacobian too. A small
    # posterior drift removes constant-Y intervals without returning anteriorly.
    target[:,1]-=np.linspace(0,.35,len(target))
    return target,{'gridStepMm':step,'requiredCentreClearanceMm':clearance,'requestedEndpoint':wish.tolist(),'chosenEndpoint':target[-1].tolist(),'route':route.tolist()}

def main():
    p=argparse.ArgumentParser();p.add_argument('--primary-checkpoint',required=True);p.add_argument('--experimental',action='store_true');p.add_argument('--clearance',type=float,default=.8);p.add_argument('--refine-right-ramus',action='store_true');p.add_argument('--right-prefix-mm',type=float,default=2.0);args=p.parse_args()
    if not args.experimental:p.error('This tool creates review-only geometry; --experimental is required')
    doc,data=read_glb(APP/'.authoring/arteries-baseline.glb');records=mesh_records(doc,data)
    cd,cb=read_glb(Path(args.primary_checkpoint));current=mesh_records(cd,cb)
    brain=trimesh.load(APP/'public/anatomy/models/brain-context.glb',process=False)
    bones=trimesh.load(APP/'.authoring/bones-baseline.glb',process=False)
    report={'status':'review-only','appliedToApp':False,'baseline':'0.9.15','release':'0.9.18','branches':[]}
    if args.refine_right_ramus:
        prior_doc,prior_data=read_glb(APP/'.authoring/central-rebuilt-trial.glb');prior=mesh_records(prior_doc,prior_data)
        for key,r in records.items():r['positions'][:]=prior[key]['positions']
        prior_report=json.loads((APP/'docs/validation/central-rebuilt-trial-v0.9.18.json').read_text())
        report['branches']=[b for b in prior_report['branches'] if b['node']!='Central distal ramus right']
    for side,sign in [('left',-1),('right',1)]:
        if args.refine_right_ramus and side=='left':continue
        for key in ['Central '+side,'MCA superior division '+side]:records[key]['positions'][:]=current[key]['positions']
        if side=='right':regularise_terminal(records['Central '+side])
        primary=records['Central '+side]
        # The branching outlets need more room than the main wall alone. Move
        # this short join-bearing interval medially by 1.2 mm and posteriorly
        # by 0.6 mm, with smooth
        # stationary end collars. Both bank walls are subsequently rechecked.
        z=primary['old'][:,2];weight=smoothstep((z-137)/3)*(1-smoothstep((z-147)/3))
        primary['positions'][:,0]-=sign*1.2*weight
        primary['positions'][:,1]-=.6*weight
        tissues=[m for k,m in brain.geometry.items() if not any(x in k for x in ['sulc','lat-fis','falx','tentorium','ventricle','aqueduct']) and k.endswith(side) and m.bounds[1,2]>130]
        tissue_functions=[implicit(m) for m in tissues]
        bone_targets=[m for m in bones.geometry.values() if m.bounds[1,2]>130]
        functions=tissue_functions+[implicit(m) for m in bone_targets]
        for label in ['Central cortical branch '+side,'Central distal ramus '+side]:
            if args.refine_right_ramus and 'cortical branch' in label:continue
            r=records[label];old=r['old'];tree=cKDTree(primary['old']);dist,idx=tree.query(old);shared=dist<1e-5
            root=old[shared].mean(0);newroot=primary['positions'][idx[shared]].mean(0)
            src=curve_from_mesh(trimesh.Trimesh(old,r['faces'],process=False),axis=1,n=158)[::-1]
            # The actual distal pole, rather than an interior cutter station,
            # defines the cap correspondence and its clearance requirement.
            tangent=src[-1]-src[-3]
            tip=src[-1]+tangent*((old[:,1].min()-.05-src[-1,1])/tangent[1])
            src=np.vstack([root,src,tip])
            wish=src[-1]+(newroot-root)
            support=np.linalg.norm(primary['old']-root,axis=1)<6.
            points,unique=np.unique(primary['old'][support],axis=0,return_index=True)
            delta=(primary['positions'].astype(float)-primary['old'])[support][unique]
            mapping=RBFInterpolator(points,delta,kernel='thin_plate_spline',degree=1,neighbors=min(48,len(points)),smoothing=1e-8)
            print('Plan',label,'root',np.round(newroot,2),'wish',np.round(wish,2),flush=True)
            main_surface=implicit(trimesh.Trimesh(primary['positions'],primary['faces'],process=False))
            join_index=0
            if 'ramus' in label:
                arc=np.r_[0,np.cumsum(np.linalg.norm(np.diff(src,axis=0),axis=1))]
                prefix_length=args.right_prefix_mm if side=='right' else 2.5
                join_index=int(np.searchsorted(arc,prefix_length))
                prefix=src[:join_index+1]+mapping(src[:join_index+1]);prefix[0]=newroot
                start=prefix[-1]
            else:start=newroot
            dst,evidence=plan(start,wish,functions,tissue_functions,sign,clearance=args.clearance,primary=main_surface,join_root=newroot)
            if join_index:
                arc=np.r_[0,np.cumsum(np.linalg.norm(np.diff(dst,axis=0),axis=1))]
                rest=np.column_stack([np.interp(np.linspace(0,arc[-1],len(src)-join_index),arc,dst[:,k]) for k in range(3)])
                dst=np.vstack([prefix[:-1],rest]);evidence['sourceBoundPrefixLengthMm']=prefix_length
            candidate,param=transport(old,src,dst)
            if 'cortical branch' in label:
                # The hemispherical terminal cap is transported rigidly. It
                # must not be decomposed into biased near-pole cutter centres.
                sf,df=frames(src),frames(dst);rotation=df[-8]@sf[-8].T
                cap=dst[-1]+(old-src[-1])@rotation.T
                length=old[:,1]-old[:,1].min();weight=1-smoothstep((length-.6)/1.4)
                candidate+=weight[:,None]*(cap-candidate)
            # Bind the entire original join collar, not a centreline proxy.
            anchors=old[shared];distance=cKDTree(anchors).query(old)[0]
            collar=distance<5.
            bound=old[collar]+mapping(old[collar]);blend=1-smoothstep((distance[collar]-.3)/1.5)
            candidate[collar]+=blend[:,None]*(bound-candidate[collar])
            candidate[shared]=primary['positions'][idx[shared]]
            r['positions'][:]=candidate
            m=trimesh.Trimesh(r['positions'],r['faces'],process=False)
            checks=[]
            for kind,scene in [('brain',brain),('bone',bones)]:
                for k,target in scene.geometry.items():
                    if kind=='brain' and any(x in k for x in ['sulc','lat-fis','falx','tentorium','ventricle','aqueduct']):continue
                    counts=collisions(m,target)
                    if counts:checks.append({'target':k,'triangleContacts':counts})
            evidence.update(node=label,source=src.tolist(),target=dst.tolist(),contacts=checks,maximumDisplacementMm=float(np.linalg.norm(candidate-old,axis=1).max()))
            report['branches'].append(evidence);print('Contacts',label,checks,flush=True)
    # Normals are accumulated across exact original shared coordinates.
    old=np.concatenate([r['old'] for r in records.values()]);_,inverse=np.unique(np.round(old,5),axis=0,return_inverse=True)
    normals=np.zeros((inverse.max()+1,3));offset=0
    for r in records.values():
        v=r['positions'];f=r['faces'];ids=inverse[offset:offset+len(v)];offset+=len(v)
        fn=np.cross(v[f[:,1]]-v[f[:,0]],v[f[:,2]]-v[f[:,0]])
        for i in range(3):np.add.at(normals,ids[f[:,i]],fn)
    normals/=np.maximum(np.linalg.norm(normals,axis=1)[:,None],1e-12)
    offset=0
    for r in records.values():
        v=r['positions'];ids=inverse[offset:offset+len(v)];offset+=len(v)
        if np.array_equal(v,r['old']):continue
        a=r['primitive']['attributes'];accessor(doc,data,a['NORMAL'])[:]=normals[ids]
        doc['accessors'][a['POSITION']].update(min=v.min(0).tolist(),max=v.max(0).tolist())
    out=APP/'.authoring/central-rebuilt-trial.glb';write_glb(out,doc,data)
    report['authoringSha256']=hashlib.sha256(out.read_bytes()).hexdigest()
    report['passedBranchContactChecks']=all(not b['contacts'] for b in report['branches'])
    (APP/'docs/validation/central-rebuilt-trial-v0.9.18.json').write_text(json.dumps(report,indent=2)+'\n')
    print('Branch contacts passed:',report['passedBranchContactChecks'],flush=True)

if __name__=='__main__':main()
