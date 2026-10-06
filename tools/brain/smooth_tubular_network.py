"""Joint constrained centreline smoothing, retaining circular swept sections."""
import json,shutil
import numpy as np,trimesh,vtk,manifold3d as mf
from scipy.spatial import cKDTree
from scipy.sparse import coo_matrix
from scipy.optimize import minimize
from fit_vessels import APP,read_glb,mesh_records
from build_targets import poly
from seat_posterior_candidate import locator,front_fn
from refine_context_skin import save_replaced
from reconcile_brainstem import sha
from rebuild_tubular_brainstem_veins import KEYS,frames,tube,retained_solid

def main():
    src=APP/'.authoring/posterior-tubular54';out=APP/'.authoring/posterior-tubular55';out.mkdir(exist_ok=True)
    for kind in ['brain','arteries','veins']:
        shutil.copyfile(src/f'{kind}-source.glb',out/f'{kind}-source.glb')
        if kind!='veins':shutil.copyfile(src/f'{kind}-trial.glb',out/f'{kind}-trial.glb')
    rows=json.loads((src/'tubular-courses.json').read_text());keys=list(rows);points=np.concatenate([np.array(rows[k]['points']) for k in keys]);_,first,inv=np.unique(np.round(points,5),axis=0,return_index=True,return_inverse=True);q=points[first].copy();reference=q.copy();N=len(q);indices={};radii=np.zeros(N);fixed=np.zeros(N,bool);fixed_points=q.copy();off=0;edges=[];rrr=[];ccc=[];vvv=[];nr=0
    for k in keys:
        row=rows[k];n=len(row['points']);ids=inv[off:off+n];off+=n;indices[k]=ids;np.maximum.at(radii,ids,np.array(row['radii']))
        for a in row['attachments']:
            end=0 if np.linalg.norm(q[ids[0]]-a)<np.linalg.norm(q[ids[-1]]-a) else -1;fixed[ids[end]]=True;fixed_points[ids[end]]=a
        for i in range(1,n-1):
            rrr.extend([nr]*3);ccc.extend(ids[i-1:i+2]);vvv.extend([1.,-2.,1.]);nr+=1
    D=coo_matrix((vvv,(rrr,ccc)),shape=(nr,N)).tocsr();K=(D.T@D).tocsr();lam=2200.
    brain=trimesh.load(src/'brain-trial.glb',process=False);stem=trimesh.util.concatenate([m for k,m in brain.geometry.items() if any(t in k for t in ['pons.','midbrain.','medulla-oblongata','base-of-peduncle'])]);loc=locator(stem);front=front_fn(loc);arteries=trimesh.load(src/'arteries-trial.glb',process=False);art=trimesh.util.concatenate(list(arteries.geometry.values()));implicit=vtk.vtkImplicitPolyDataDistance();implicit.SetInput(poly(art));basilar_front=front_fn(locator(arteries.geometry['Basilar']));logs=[]
    def sidewall(p,sign):
        t=vtk.reference(0.);v=[0.,0.,0.];pc=[0.,0.,0.];sub=vtk.reference(0);cell=vtk.reference(0)
        return v[0] if loc.IntersectWithLine([.65+sign*100,p[1],p[2]],[.65,p[1],p[2]],1e-8,t,v,pc,sub,cell) else None
    for iteration in range(6):
        lower=np.full((N,3),-np.inf);upper=np.full((N,3),np.inf);desired=reference.copy();fitted=np.zeros(N,bool);component=np.ones(N,int);signs=np.ones(N);free=np.zeros((N,3),bool)
        for k,row in rows.items():
            ids=indices[k];curve=q[ids];radius=np.array(row['radii']);_,n,bi=frames(curve);theta=np.arange(24)*2*np.pi/24;offset=radius[:,None,None]*(n[:,None,:]*np.cos(theta)[None,:,None]+bi[:,None,:]*np.sin(theta)[None,:,None]);side=row['mode']=='side';dim=0 if side else 1;sign=-1 if side and k.endswith('left') else 1;free[ids,:2]=True
            for i,node in enumerate(ids):
                if fixed[node] or (k=='vein.anterior_spinal' and curve[i,2]<18):continue
                if 'superior_petrosal_vein' in k:continue
                if k=='vein.posterior_communicating' and abs(curve[i,0]-.65)>5:continue
                dim=0 if side else 1;sign=-1 if side and k.endswith('left') else 1
                need=[];lateral_need=[];arterial_need=[];side_sign=-1 if k.endswith('left') else 1
                for offv in offset[i]:
                    p=curve[i]+offv;s=sidewall(p,sign) if side else front(p[0],p[2])
                    if s is not None:need.append(sign*(s-offv[dim])+.025)
                    if not side:
                        arterial=basilar_front(p[0],p[2])
                        if arterial is not None:arterial_need.append(arterial-offv[dim]+.12)
                    if row['mode']=='cage':
                        lateral=sidewall(p,side_sign)
                        if lateral is not None:lateral_need.append(side_sign*(lateral-offv[0])+.025)
                if row['mode']=='cage' and lateral_need and abs(curve[i,0]-.65)>7 and not arterial_need:
                    side_delta=max(lateral_need)-side_sign*curve[i,0];front_delta=max(need)-curve[i,1] if need else np.inf
                    if abs(side_delta)<abs(front_delta):need=lateral_need;dim=0;sign=side_sign
                    else:dim=1;sign=1
                elif row['mode']=='cage':dim=1;sign=1
                if arterial_need:need+=arterial_need;dim=1;sign=1
                if not need:continue
                limit=max(need);fitted[node]=True;component[node]=dim;signs[node]=sign
                if sign==1:lower[node,dim]=max(lower[node,dim],limit);desired[node,dim]=max(desired[node,dim],limit)
                else:upper[node,dim]=min(upper[node,dim],-limit);desired[node,dim]=min(desired[node,dim],-limit)
        # Sphere clearance about each centre guarantees clearance of a round
        # transverse section. Use the superficial direction for the bridge.
        bridges=0
        for node in np.flatnonzero(fitted):
            dim=component[node];sign=signs[node];p=q[node].copy();p[dim]=max(p[dim],lower[node,dim]) if sign==1 else min(p[dim],upper[node,dim]);gap=abs(implicit.EvaluateFunction(p))
            if gap>=radii[node]+.075:continue
            lo=0.;hi=None
            for trial in np.arange(.2,5.01,.2):
                test=p.copy();test[dim]+=sign*trial
                if abs(implicit.EvaluateFunction(test))>=radii[node]+.075:hi=trial;lo=max(0.,trial-.2);break
            if hi is None:continue
            for _ in range(18):
                mid=(lo+hi)/2;test=p.copy();test[dim]+=sign*mid
                if abs(implicit.EvaluateFunction(test))>=radii[node]+.075:hi=mid
                else:lo=mid
            limit=p[dim]+sign*hi
            if sign==1:lower[node,dim]=max(lower[node,dim],limit);desired[node,dim]=max(desired[node,dim],limit)
            else:upper[node,dim]=min(upper[node,dim],limit);desired[node,dim]=min(desired[node,dim],limit)
            bridges+=1
        before=q.copy();success=[]
        for dim in range(3):
            lo=lower[:,dim];hi=upper[:,dim];locked=~free[:,dim];lo[locked]=reference[locked,dim];hi[locked]=lo[locked];lo[fixed]=fixed_points[fixed,dim];hi[fixed]=lo[fixed];bounds=list(zip(lo,hi));target=desired[:,dim]
            def objective(v):
                d=v-target;kv=K@v;return .5*np.dot(d,d)+.5*lam*np.dot(v,kv),d+lam*kv
            start=np.clip(q[:,dim],lo,hi);result=minimize(objective,start,jac=True,bounds=bounds,method='L-BFGS-B',options={'maxiter':2200,'ftol':1e-11,'gtol':1e-6,'maxls':50});q[:,dim]=result.x;success.append(bool(result.success))
        logs.append({'iteration':iteration,'maximumMovementMm':float(np.linalg.norm(q-before,axis=1).max()),'arteryBridgeNodes':bridges,'optimizerSuccess':success});print(logs[-1],flush=True)
    d,b=read_glb(src/'veins-source.glb');records=mesh_records(d,b);names=list(records);base=mf.Manifold.reserve_ids(len(names));retained,caps=retained_solid(records,names,base);solids=[retained];curvature=[]
    for k,row in rows.items():
        curve=q[indices[k]];radius=np.array(row['radii']);row['points']=curve.tolist();v,f=tube(curve,radius);s=mf.Manifold(mf.Mesh(v,f,run_index=np.array([0,len(f)*3],np.uint32),run_original_id=np.array([base+names.index(k)],np.uint32)))
        if s.status()!=mf.Error.NoError:raise RuntimeError(k+' '+str(s.status()))
        solids.append(s);t=np.gradient(curve,axis=0);cur=np.linalg.norm(np.cross(t,np.gradient(t,axis=0)),axis=1)/np.maximum(np.linalg.norm(t,axis=1)**3,1e-10);curvature.append({'node':k,'maximumRadiusCurvature':float(np.max(cur*radius)),'p95RadiusCurvature':float(np.quantile(cur*radius,.95))})
    union=mf.Manifold.batch_boolean(solids,mf.OpType.Add);print('Smoothed network union',union.status(),union.num_tri(),flush=True);m=union.to_mesh();v=np.array(m.vert_properties[:,:3]);f=np.array(m.tri_verts);labels=np.zeros(len(f),int)
    for i,oid in enumerate(m.run_original_id):labels[m.run_index[i]//3:m.run_index[i+1]//3]=int(oid)-base
    normal=np.zeros_like(v);fn=np.cross(v[f[:,1]]-v[f[:,0]],v[f[:,2]]-v[f[:,0]])
    for i in range(3):np.add.at(normal,f[:,i],fn)
    normal/=np.maximum(np.linalg.norm(normal,axis=1)[:,None],1e-12);replacements={}
    for i,k in enumerate(names):
        ff=f[labels==i]
        if not len(ff):raise RuntimeError('Lost label '+k)
        used,inv=np.unique(ff,return_inverse=True);replacements[k]=(v[used],inv.reshape(-1,3),normal[used])
    save_replaced(out/'veins-trial.glb',d,b,replacements);(out/'tubular-courses.json').write_text(json.dumps(rows,separators=(',',':'))+'\n');np.savez_compressed(out/'tubular-network.npz',positions=v,faces=f,labels=labels)
    report=json.loads((src/'trial.json').read_text());report.update({'parentDirectory':str(src.relative_to(APP)),'jointCentrelineSmoothing':logs,'smoothingWeight':lam,'curveCurvature':curvature,'accepted':False,'hashes':{k:sha(out/f'{k}-trial.glb') for k in ['brain','arteries','veins']}});(out/'trial.json').write_text(json.dumps(report,indent=2)+'\n');print(out,flush=True)

if __name__=='__main__':main()
