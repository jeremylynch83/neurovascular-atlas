"""Rebuild round vein walls from candidate courses, with superficial crossings.

Authoring only. Round sweeps are unioned into a shared labelled surface and
joined to capped retained outlets. Tissue fitting acts on the centreline, never
by clamping individual wall vertices. Pattern and calibre come from this atlas.
"""
import json,shutil
import numpy as np,trimesh,vtk,manifold3d as mf
from scipy.spatial import cKDTree
from scipy.sparse import coo_matrix
from scipy.sparse.csgraph import connected_components
from scipy.ndimage import gaussian_filter1d,maximum_filter1d
from fit_vessels import APP,read_glb,mesh_records,curve_from_mesh,resample,smoothstep
from seat_posterior_candidate import locator,front_fn
from build_targets import poly
from refine_context_skin import save_replaced
from reconcile_brainstem import ANTERIOR,TRANSVERSE,LATERAL,sha

KEYS=set(ANTERIOR+TRANSVERSE+LATERAL+['vein.anterior_spinal','vein.posterior_communicating']+[f'vein.{k}.{s}' for k in ['superior_petrosal_vein','cerebellopontine_fissure'] for s in ['left','right']])

def frames(q):
    t=np.gradient(q,axis=0);t/=np.maximum(np.linalg.norm(t,axis=1)[:,None],1e-10);n=[];v=np.array([1.,0,0]);v-=t[0]*np.dot(v,t[0])
    if np.linalg.norm(v)<.1:v=np.array([0.,1,0]);v-=t[0]*np.dot(v,t[0])
    v/=np.linalg.norm(v)
    for a in t:
        v-=a*np.dot(v,a);v/=np.linalg.norm(v);n.append(v.copy())
    n=np.array(n);return t,n,np.cross(t,n)

def tube(q,r,sides=32):
    _,n,b=frames(q);theta=np.arange(sides)*2*np.pi/sides
    rings=q[:,None,:]+r[:,None,None]*(n[:,None,:]*np.cos(theta)[None,:,None]+b[:,None,:]*np.sin(theta)[None,:,None]);v=rings.reshape(-1,3);f=[]
    for i in range(len(q)-1):
        for j in range(sides):
            a=i*sides+j;b=i*sides+(j+1)%sides;f.extend([[a,b,a+sides],[b,b+sides,a+sides]])
    last=len(v);v=np.vstack([v,q[0],q[-1]])
    for j in range(sides):f.extend([[last,(j+1)%sides,j],[last+1,(len(q)-1)*sides+j,(len(q)-1)*sides+(j+1)%sides]])
    return v.astype(np.float32),np.array(f,np.uint32)

def retained_solid(rr,ids,base):
    vv=[];ff=[];ll=[];offset=0
    for k,r in rr.items():
        if k in KEYS:continue
        vv.append(r['old']);ff.append(r['faces']+offset);ll.extend([ids.index(k)]*len(r['faces']));offset+=len(r['old'])
    v=np.concatenate(vv);f=np.concatenate(ff);lab=np.array(ll);_,idx,inv=np.unique(np.round(v,5),axis=0,return_index=True,return_inverse=True);v=v[idx];f=inv[f]
    directed=np.concatenate([f[:,[0,1]],f[:,[1,2]],f[:,[2,0]]]);face_labels=np.tile(lab,3);edges=np.sort(directed,axis=1);_,index,count=np.unique(edges,axis=0,return_index=True,return_counts=True);boundary=directed[index[count==1]];tags=face_labels[index[count==1]]
    graph=coo_matrix((np.ones(len(boundary)),(boundary[:,0],boundary[:,1])),shape=(len(v),len(v))).tocsr();_,components=connected_components(graph,directed=False);caps=[]
    for c in np.unique(components[boundary.ravel()]):
        mask=components[boundary[:,0]]==c;edge=boundary[mask];points=np.unique(edge);centre=v[points].mean(0);ci=len(v);v=np.vstack([v,centre]);f=np.vstack([f,np.column_stack([edge[:,1],edge[:,0],np.full(len(edge),ci)])]);lab=np.r_[lab,tags[mask]];caps.append({'centre':centre,'radius':np.linalg.norm(v[points]-centre,axis=1).mean()})
    order=np.argsort(lab,kind='stable');f=f[order];lab=lab[order];labels,first=np.unique(lab,return_index=True);run=np.r_[first*3,len(f)*3].astype(np.uint32)
    solid=mf.Manifold(mf.Mesh(v.astype(np.float32),f.astype(np.uint32),run_index=run,run_original_id=(base+labels).astype(np.uint32)))
    if solid.status()!=mf.Error.NoError:raise RuntimeError('Retained outlet caps: '+str(solid.status()))
    return solid,caps

def majorant(values,sigma=2.):
    # A smooth upper envelope rounds local bridges while staying outside walls.
    q=gaussian_filter1d(values,sigma)
    return q+maximum_filter1d(np.maximum(values-q,0),size=max(3,int(sigma*4)//2*2+1))

def main():
    src=APP/'.authoring/posterior-surface52';out=APP/'.authoring/posterior-tubular54';out.mkdir(exist_ok=True)
    for kind in ['brain','arteries']:
        shutil.copyfile(src/f'{kind}-trial.glb',out/f'{kind}-trial.glb');shutil.copyfile(src/f'{kind}-trial.glb',out/f'{kind}-source.glb')
    shutil.copyfile(src/'veins-trial.glb',out/'veins-source.glb')
    d,b=read_glb(src/'veins-trial.glb');rr=mesh_records(d,b);ids=list(rr);base=mf.Manifold.reserve_ids(len(ids));retained,caps=retained_solid(rr,ids,base);print('Retained closed outlets',len(caps),flush=True)
    paths=json.loads((APP/'anatomy/source/venous/fitted-paths.json').read_text());profiles={r['id']:r for r in paths if r['id'] in KEYS}
    brain=trimesh.load(src/'brain-trial.glb',process=False);stem=trimesh.util.concatenate([m for k,m in brain.geometry.items() if any(t in k for t in ['pons.','midbrain.','medulla-oblongata','base-of-peduncle'])]);loc=locator(stem);front=front_fn(loc)
    arteries=trimesh.load(src/'arteries-trial.glb',process=False);art=trimesh.util.concatenate(list(arteries.geometry.values()));implicit=vtk.vtkImplicitPolyDataDistance();implicit.SetInput(poly(art));courses={};data={}
    def sidewall(p,sign):
        t=vtk.reference(0.);q=[0.,0.,0.];pc=[0.,0.,0.];sub=vtk.reference(0);cell=vtk.reference(0)
        return q[0] if loc.IntersectWithLine([.65+sign*100,p[1],p[2]],[.65,p[1],p[2]],1e-8,t,q,pc,sub,cell) else None
    for k in sorted(KEYS):
        r=rr[k];axis=0 if k in TRANSVERSE or k=='vein.posterior_communicating' or 'superior_petrosal_vein' in k else 2
        mesh=trimesh.Trimesh(r['old'],r['faces'],process=False);length=np.linalg.norm(mesh.bounds[1]-mesh.bounds[0]);q=curve_from_mesh(mesh,axis=axis,n=max(80,int(length/.3)));q=gaussian_filter1d(q,1.,axis=0);q=resample(q,len(q));radius=np.interp(np.linspace(0,1,len(q)),np.linspace(0,1,len(profiles[k]['radii'])),profiles[k]['radii'])
        # Continue genuine external attachments into their retained cap centres.
        attachments=[]
        for end in [0,-1]:
            near=min(caps,key=lambda c:np.linalg.norm(c['centre']-q[end]));distance=np.linalg.norm(near['centre']-q[end])
            if distance<3:
                shift=near['centre']-q[end];count=min(12,len(q)//5)
                for i in range(count):j=i if end==0 else -1-i;q[j]+=shift*(1-i/count)**2
                attachments.append((end,near))
        if profiles[k]['points'][0][axis]>profiles[k]['points'][-1][axis]:radius=radius[::-1].copy()
        original=q.copy();sign=-1 if k.endswith('left') else 1;mode='cage' if k in TRANSVERSE else 'side' if any(t in k for t in ['lateral_mesencephalic','cerebellopontine_fissure','superior_petrosal_vein']) else 'front';component=0 if mode=='side' else 1;normal_sign=sign if mode=='side' else 1
        bridge=np.zeros(len(q));fitted=np.zeros(len(q),bool)
        for iteration in range(3):
            _,n,bi=frames(q);theta=np.arange(24)*2*np.pi/24;offset=radius[:,None,None]*(n[:,None,:]*np.cos(theta)[None,:,None]+bi[:,None,:]*np.sin(theta)[None,:,None]);desired=normal_sign*q[:,component]
            for i in range(len(q)):
                # Keep the spinal end and collector outlet collars in place.
                if 'superior_petrosal_vein' in k:continue
                if k=='vein.posterior_communicating' and abs(q[i,0]-.65)>5:continue
                if k=='vein.anterior_spinal' and q[i,2]<18:continue
                if any(np.linalg.norm(q[i]-a['centre'])<2.5 for _,a in attachments):continue
                wall=q[i]+offset[i];need=[]
                for p,off in zip(wall,offset[i]):
                    surface=sidewall(p,sign) if mode=='side' else front(p[0],p[2])
                    if surface is not None:need.append(normal_sign*(surface-off[component])+.015)
                if need:desired[i]=max(need);fitted[i]=True
            if mode=='cage':
                # Only seed round centreline geometry here. The common solver
                # chooses the nearer anterior or lateral surface envelope.
                break
            desired=majorant(desired,2.0);q[:,component]=normal_sign*desired
            # Superficial bridging uses artery-wall distance, including radius.
            for i in range(len(q)):
                if not fitted[i] or any(np.linalg.norm(q[i]-a['centre'])<2.5 for _,a in attachments):continue
                gap=abs(implicit.EvaluateFunction(q[i]));lift=0.
                if gap<radius[i]+.04:
                    lower=0.;upper=12.
                    p=q[i].copy();p[component]+=normal_sign*upper
                    if abs(implicit.EvaluateFunction(p))<radius[i]+.04:continue
                    for _ in range(16):
                        mid=(lower+upper)/2;p=q[i].copy();p[component]+=normal_sign*mid
                        if abs(implicit.EvaluateFunction(p))>=radius[i]+.04:upper=mid
                        else:lower=mid
                    lift=upper
                bridge[i]=max(bridge[i],lift)
            q[:,component]+=normal_sign*majorant(bridge,3.0)
            bridge[:]=0
        for end,a in attachments:
            delta=a['centre']-q[end];count=min(10,len(q)//6)
            for i in range(count):j=i if end==0 else -1-i;q[j]+=delta*(1-i/count)**2
        courses[k]=q;data[k]={'points':q.tolist(),'radii':radius.tolist(),'sourcePoints':original.tolist(),'surfaceFitted':fitted.tolist(),'mode':mode,'attachments':[a['centre'].tolist() for _,a in attachments]};print('Round centreline fitted',k,len(q),flush=True)
    # Rejoin longitudinal segments and their true atlas branches, retaining the
    # existing network pattern rather than copying the illustrative reference.
    def join(a,b):
        qa,qb=courses[a],courses[b];pairs=[(i,j,np.linalg.norm(qa[i]-qb[j])) for i in [0,-1] for j in [0,-1]];i,j,_=min(pairs,key=lambda x:x[2]);point=(qa[i]+qb[j])/2;point[1]=max(qa[i,1],qb[j,1])
        for q,end in [(qa,i),(qb,j)]:
            delta=point-q[end]
            for n in range(12):idx=n if end==0 else -1-n;q[idx]+=delta*(1-n/12)**2
    for a,bk in [('vein.anterior_medullary','vein.anterior_pontine'),('vein.anterior_pontine','vein.anterior_pontomesencephalic'),('vein.anterior_spinal','vein.anterior_medullary')]:join(a,bk)
    def attach(branch,parent,end=None):
        q=courses[branch];p=courses[parent];distance,index=cKDTree(p).query(q[[0,-1]])
        e=int(distance.argmin()) if end is None else end;idx=0 if e==0 else -1;target=p[index[e]];delta=target-q[idx]
        for n in range(min(16,len(q)//4)):j=n if idx==0 else -1-n;q[j]+=delta*(1-n/min(16,len(q)//4))**2
    attach('vein.anterior_pontomesencephalic','vein.posterior_communicating')
    for side in ['left','right']:
        attach('vein.transverse_pontine.'+side,'vein.anterior_pontine');attach('vein.pontomedullary.'+side,'vein.anterior_medullary');join('vein.cerebellopontine_fissure.'+side,'vein.superior_petrosal_vein.'+side);attach('vein.lateral_mesencephalic.'+side,'vein.superior_petrosal_vein.'+side);attach('vein.transverse_pontine.'+side,'vein.superior_petrosal_vein.'+side,0 if side=='left' else 1);attach('vein.pontomedullary.'+side,'vein.cerebellopontine_fissure.'+side,0 if side=='left' else 1)
    solids=[retained];round_stats=[]
    for k,q in courses.items():
        radius=np.array(data[k]['radii']);v,f=tube(q,radius);solid=mf.Manifold(mf.Mesh(v,f,run_index=np.array([0,len(f)*3],np.uint32),run_original_id=np.array([base+ids.index(k)],np.uint32)))
        if solid.status()!=mf.Error.NoError:raise RuntimeError(k+': '+str(solid.status()))
        solids.append(solid);data[k]['points']=q.tolist();round_stats.append({'node':k,'radiusRangeMm':[float(radius.min()),float(radius.max())],'sweepSections':len(q),'sides':32})
    union=mf.Manifold.batch_boolean(solids,mf.OpType.Add);print('Network union',union.status(),union.num_tri(),flush=True)
    if union.status()!=mf.Error.NoError:raise RuntimeError(str(union.status()))
    m=union.to_mesh();v=np.array(m.vert_properties[:,:3]);f=np.array(m.tri_verts);labels=np.zeros(len(f),int)
    for i,oid in enumerate(m.run_original_id):labels[m.run_index[i]//3:m.run_index[i+1]//3]=int(oid)-base
    normal=np.zeros_like(v);fn=np.cross(v[f[:,1]]-v[f[:,0]],v[f[:,2]]-v[f[:,0]])
    for i in range(3):np.add.at(normal,f[:,i],fn)
    normal/=np.maximum(np.linalg.norm(normal,axis=1)[:,None],1e-12);replacements={}
    for i,k in enumerate(ids):
        faces=f[labels==i]
        if not len(faces):raise RuntimeError('Lost label '+k)
        used,inv=np.unique(faces,return_inverse=True);replacements[k]=(v[used],inv.reshape(-1,3),normal[used])
    save_replaced(out/'veins-trial.glb',d,b,replacements)
    (out/'tubular-courses.json').write_text(json.dumps(data,separators=(',',':'))+'\n')
    np.savez_compressed(out/'tubular-network.npz',positions=v,faces=f,labels=labels)
    report={'parentDirectory':str(src.relative_to(APP)),'method':'round circular swept sections, artery-wall bridges, boolean shared labelled network','rebuiltVeins':round_stats,'basilarRetained':True,'brainRetained':True,'retainedOutletCaps':len(caps),'networkBooleanStatus':str(union.status()),'accepted':False,'appliedToApp':False,'hashes':{k:sha(out/f'{k}-trial.glb') for k in ['brain','arteries','veins']}}
    (out/'trial.json').write_text(json.dumps(report,indent=2)+'\n');print(out,flush=True)

if __name__=='__main__':main()
