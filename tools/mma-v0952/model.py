"""Fit bilateral MMA guides to inner cranial surfaces with shared branch transport."""
from vein_geometry import *
from scipy.spatial.transform import Rotation
vtk.vtkLogger.SetStderrVerbosity(vtk.vtkLogger.VERBOSITY_OFF)
models={};fields=[];guides=[]

def inner_table(side):
    vv=[];ff=[]
    for name in ['bone.sphenoid','bone.temporal.'+side,'bone.parietal.'+side,'bone.frontal']:
        v,f=load(name);tri=v[f];normal=np.cross(tri[:,1]-tri[:,0],tri[:,2]-tri[:,0])
        centre=tri.mean(1);keep=np.einsum('ij,ij->i',normal,centre-[0,-60,95])<0
        ff.append(f[keep]+sum(len(x) for x in vv));vv.append(v)
    v=np.concatenate(vv);f=np.concatenate(ff);normal=np.cross(v[f[:,1]]-v[f[:,0]],v[f[:,2]]-v[f[:,0]])
    normal/=np.maximum(np.linalg.norm(normal,axis=1)[:,None],1e-12)
    return locator(v,f),normal

for side,sign in [('right',1),('left',-1)]:
    suffix=' left' if side=='left' else '';rows=[];radii=[]
    for name in ['Middle meningeal'+suffix,'MMA frontal'+suffix]:
        x=np.load(WORK/(name+'.curve.npz'));q=x['q'];r=x['r']
        if q[0,2]>q[-1,2]:q=q[::-1];r=r[::-1]
        if rows:
            take=q[:,2]>rows[-1][-1,2]+.4;q=q[take];r=r[take]
        rows.append(q);radii.append(r)
    raw=np.concatenate(rows);q=resample(raw,.20);r=np.concatenate(radii)[cKDTree(raw).query(q)[1]]
    loc,ns=inner_table(side);cp=[];nn=[];cid=vtk.reference(0);sub=vtk.reference(0);d2=vtk.reference(0.);point=[0.,0.,0.]
    for p in q:
        loc.FindClosestPoint(p,point,cid,sub,d2);cp.append(point.copy());nn.append(ns[int(cid)])
    cp=np.array(cp);nn=gaussian_filter1d(np.array(nn),6,axis=0);nn/=np.maximum(np.linalg.norm(nn,axis=1)[:,None],1e-9)
    # Keep the extracranial origin and lower canal approach fixed.
    delta=cp+nn*(r+.35)[:,None]-q
    delta=gaussian_filter1d(delta,7,axis=0)*smooth((q[:,2]-44)/10)[:,None]
    target=q+delta
    ta=np.gradient(q,axis=0);tb=np.gradient(target,axis=0)
    ta/=np.linalg.norm(ta,axis=1)[:,None];tb/=np.linalg.norm(tb,axis=1)[:,None]
    axis=np.cross(ta,tb);length=np.linalg.norm(axis,axis=1);angle=np.arctan2(length,np.einsum('ij,ij->i',ta,tb))
    rv=axis/np.maximum(length[:,None],1e-12)*angle[:,None]
    tree=cKDTree(q)
    def transform(v,q=q,target=target,tree=tree,rv=rv):
        _,k=tree.query(v)
        a=np.clip(k-1,0,len(q)-2);b=np.clip(k,0,len(q)-2)
        def project(j):
            segment=q[j+1]-q[j]
            t=np.clip(np.einsum('ij,ij->i',v-q[j],segment)/np.maximum(np.einsum('ij,ij->i',segment,segment),1e-12),0,1)
            cp=q[j]+segment*t[:,None]
            return t,cp,np.linalg.norm(v-cp,axis=1)
        t0,p0,d0=project(a);t1,p1,d1=project(b);take=d1<d0
        j=np.where(take,b,a);t=np.where(take,t1,t0);cp=np.where(take[:,None],p1,p0);d=np.minimum(d0,d1)
        weight=smooth((12-d)/10)
        local=v-cp
        rvec=rv[j]*(1-t[:,None])+rv[j+1]*t[:,None]
        centre=target[j]*(1-t[:,None])+target[j+1]*t[:,None]
        moved=centre+Rotation.from_rotvec(rvec).apply(local)
        return v+(moved-v)*weight[:,None]
    fields.append(transform)
    guides.append(dict(side=side,oldPoints=q.tolist(),points=target.tolist(),radiusMm=r.tolist(),innerTablePoints=cp.tolist(),innerTableNormals=nn.tolist(),maxGuideShiftMm=float(np.linalg.norm(delta,axis=1).max()),maxTangentRotationDeg=float(np.rad2deg(angle).max())))

def deform(v):
    q=v.copy()
    for fn in fields:q=fn(q)
    return q

selected={n for n,file in FILES.items() if file in ['complete-circulation.glb','complete-anastomoses.glb'] and ('mma' in n.lower() or 'middle meningeal' in n.lower())}
vascular={n for n,file in FILES.items() if file in ['complete-circulation.glb','complete-anastomoses.glb']}
for _ in range(3):
    moving=[]
    for n in selected:
        v,f=load(n);q=deform(v);take=np.linalg.norm(q-v,axis=1)>1e-6
        if take.any():models[n]=(q,f);moving.append(v[take])
    shared=cKDTree(np.concatenate(moving));extra=[]
    for n in vascular-selected:
        v,f=load(n)
        if np.any(shared.query(v)[0]<1e-5):extra.append(n)
    if not extra:break
    selected.update(extra)
revision=dict(release='0.9.52',baseline='0.9.51',baselineAssetHashes=json.loads((DATA/'source-assets.json').read_text()),changed=[],newLabels=[],method='Inner cranial surface fitting and common rigid-section transport field across native shared arterial branch coordinates',guides=guides)
for name,(v,f) in sorted(models.items()):
    old,_=load(name);write(name,v,f)
    revision['changed'].append(dict(node=name,file=FILES[name],vertices=len(v),triangles=len(f),maxShiftMm=float(np.linalg.norm(v-old,axis=1).max()),topologyExact=True))
    print(name,round(revision['changed'][-1]['maxShiftMm'],3),flush=True)
(OUT/'revision.json').write_text(json.dumps(revision,indent=2)+'\n')
(WORK/'mma-guides.json').write_text(json.dumps(guides,indent=2)+'\n')
print('Guide shifts/rotations',[(g['side'],g['maxGuideShiftMm'],g['maxTangentRotationDeg']) for g in guides],flush=True)
