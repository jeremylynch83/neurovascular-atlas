"""Seat canonical round veins using a smooth, coupled anterior envelope."""
import json,shutil
import numpy as np,trimesh,vtk,manifold3d as mf
from scipy.ndimage import gaussian_filter1d
from scipy.sparse import coo_matrix
from scipy.optimize import minimize
from fit_vessels import APP,read_glb,mesh_records,accessor,smoothstep
from rebuild_round_pial_network import interfaces,cap_retained
from refine_round_surface_network import Clearance,fit_interval
from rebuild_tubular_brainstem_veins import tube
from refine_context_skin import save_replaced
from build_targets import poly
from reconcile_brainstem import sha

BASE=APP/'.authoring/posterior-round58'
SRC=APP/'.authoring/posterior-tubular55'
W=APP/'.authoring/posterior-round60'

def dense(q,r,anchors,smooth=False):
    ids=sorted(set([0,len(q)-1]+list(anchors)));out=[];rout=[];mapping={}
    for a,b in zip(ids[:-1],ids[1:]):
        p=q[a:b+1];rr=r[a:b+1];arc=np.r_[0,np.cumsum(np.linalg.norm(np.diff(p,axis=0),axis=1))];good=np.r_[True,np.diff(arc)>1e-8];arc=arc[good];p=p[good];rr=rr[good];tt=np.linspace(0,arc[-1],max(3,int(np.ceil(arc[-1]/.20))+1));p=np.column_stack([np.interp(tt,arc,p[:,i]) for i in range(3)]);rr=np.interp(tt,arc,rr)
        if smooth:
            ends=p[[0,-1]].copy();p=gaussian_filter1d(p,6.,axis=0);p+=(ends[0]-p[0])*(1-smoothstep(tt/2.))[:,None];p+=(ends[1]-p[-1])*(1-smoothstep((tt[-1]-tt)/2.))[:,None]
        mapping[a]=len(out)-1 if out else 0;out.extend(p[1:] if out else p);rout.extend(rr[1:] if rout else rr);mapping[b]=len(out)-1
    return np.array(out),np.array(rout),mapping

def main():
    W.mkdir(exist_ok=True)
    for file in ['brain-trial.glb','cord-context.json','arteries-trial.glb','arteries-collision-solid.glb','arteries-round-courses.json','posterior-spinal-courses.json']:shutil.copyfile(BASE/file,W/file)
    meta=json.loads((APP/'deliverables/posterior-fossa-expanded-review/model-review.json').read_text());brain=trimesh.load(W/'brain-trial.glb',process=False);target=trimesh.util.concatenate([brain.geometry[k] for k in meta['groups']['brain']]+[brain.geometry['brain.upper-cervical-cord']]);field=Clearance(target);arterial=trimesh.load(W/'arteries-collision-solid.glb',force='mesh',process=False);obstacle=vtk.vtkImplicitPolyDataDistance();obstacle.SetInput(poly(arterial))
    d,b=read_glb(SRC/'veins-trial.glb');rr=mesh_records(d,b);names=list(rr)
    for rec in rr.values():rec['_normals']=accessor(d,b,rec['primitive']['attributes']['NORMAL']).copy()
    canonical=json.loads((SRC/'tubular-courses.json').read_text());previous=json.loads((BASE/'veins-round-courses.json').read_text());selected=list(previous);curves={k:np.array((canonical[k] if k in canonical else previous[k])['points']) for k in selected};radii={k:np.array((canonical[k] if k in canonical else previous[k])['radii']) for k in selected};original={k:q.copy() for k,q in curves.items()};retained,pairs=interfaces(rr,selected);links=[];mobile=[];anchors={k:set() for k in selected}
    for (a,bb),points in pairs.items():
        centre=points.mean(0)
        if a in curves and bb in curves:
            i=int(np.linalg.norm(curves[a]-centre,axis=1).argmin());j=int(np.linalg.norm(curves[bb]-centre,axis=1).argmin());links.append((a,i,bb,j));curves[a][i]=centre;curves[bb][j]=centre;anchors[a].add(i);anchors[bb].add(j)
        else:
            k=a if a in curves else bb;other=bb if k==a else a;i=int(np.linalg.norm(curves[k]-centre,axis=1).argmin());curves[k][i]=centre;mobile.append((other,k,i,centre));anchors[k].add(i)
    maps={}
    for k in selected:curves[k],radii[k],maps[k]=dense(curves[k],radii[k],anchors[k],smooth=k in canonical)
    links=[(a,maps[a][i],bb,maps[bb][j]) for a,i,bb,j in links];mobile=[(other,k,maps[k][i],p) for other,k,i,p in mobile]
    offset={};N=0
    for k,q in curves.items():offset[k]=N;N+=len(q)
    parent=np.arange(N)
    def find(i):
        while parent[i]!=i:parent[i]=parent[parent[i]];i=parent[i]
        return i
    for a,i,bb,j in links:parent[find(offset[bb]+j)]=find(offset[a]+i)
    roots=np.array([find(i) for i in range(N)]);_,inv=np.unique(roots,return_inverse=True);M=inv.max()+1;ids={k:inv[offset[k]:offset[k]+len(q)] for k,q in curves.items()};source=np.zeros((M,3));count=np.zeros(M);rad=np.zeros(M);active=np.zeros(M,bool)
    for k,q in curves.items():
        weight=100. if k in canonical else 1.;np.add.at(source,ids[k],q*weight);np.add.at(count,ids[k],weight);np.maximum.at(rad,ids[k],radii[k]);active[ids[k]]|=k in canonical
    source/=count[:,None]
    for i in np.flatnonzero(~active):
        source[i]=field.point(source[i],rad[i]+.035,obstacle,outward_reference=field.direction(source[i]))
    lower=source[:,1].copy();target_y=lower.copy();rows=[];cols=[];vals=[];row=0
    for k in canonical:
        if k not in ids:continue
        ii=ids[k]
        for j in range(1,len(ii)-1):rows.extend([row]*3);cols.extend(ii[j-1:j+2]);vals.extend([1.,-2.,1.]);row+=1
    D=coo_matrix((vals,(rows,cols)),shape=(row,M)).tocsr();K=(D.T@D).tocsr()
    # The envelope supplies absolute seating positions, including arterial
    # bridges. Smooth the constrained position, rather than projecting a
    # smoothed path back into a sequence of angular jumps.
    for i in np.flatnonzero(active):
        p=source[i].copy();p[1]=-200.;p=field.point(p,rad[i],obstacle,preferred=(1,1))
        if p[1]<-190.:p=field.point(source[i],rad[i],obstacle,preferred=(1,1))
        lower[i]=p[1];target_y[i]=lower[i]
    print('Anterior seating bounds',int(active.sum()),float(lower[active].min()),float(lower[active].max()),flush=True)
    lo=lower.copy();hi=np.full(M,np.inf);lo[~active]=hi[~active]=source[~active,1];weight=2000.
    def objective(y):
        delta=y-target_y;ky=K@y;return .5*np.dot(delta,delta)+.5*weight*np.dot(y,ky),delta+weight*ky
    y=np.maximum(source[:,1],lower)
    for iteration in range(16):
        result=minimize(objective,y,jac=True,bounds=list(zip(lo,hi)),method='L-BFGS-B',options={'maxiter':6000,'ftol':1e-12,'gtol':1e-6,'maxls':50});assert result.success,str(result.message);y=result.x.copy();correction=0.
        for i in np.flatnonzero(active):
            p=source[i].copy();p[1]=y[i];checked=field.point(p,rad[i]+.035,obstacle,preferred=(1,1));extra=max(0.,checked[1]-y[i]);correction=max(correction,extra)
            if extra>1e-5:lo[i]=max(lo[i],checked[1])
        print('Smooth arterial clearance iteration',iteration,'correction',correction,flush=True)
        if correction<.002:break
    assert correction<.002,('Unresolved arterial envelope',correction)
    fitted_nodes=source.copy();fitted_nodes[:,1]=y;fitted={k:fitted_nodes[ids[k]].copy() for k in selected};rout={k:radii[k].copy() for k in selected}
    newanchors={k:{0,len(curves[k])-1} for k in selected}
    for a,i,bb,j in links:newanchors[a].add(i);newanchors[bb].add(j)
    for _,k,i,_ in mobile:newanchors[k].add(i)
    for k in selected:
        if k in canonical:continue
        baseline=curves[k];delta=np.zeros_like(baseline);weights=np.zeros(len(baseline))
        for i in newanchors[k]:
            move=fitted[k][i]-baseline[i]
            if np.linalg.norm(move)<1e-8:continue
            distance=np.linalg.norm(baseline-baseline[i],axis=1);ww=1-smoothstep(distance/8.);delta+=move*ww[:,None];weights+=ww
        changed=baseline+delta/np.maximum(weights[:,None],1.);changed[list(newanchors[k])]=fitted[k][list(newanchors[k])];out=[];rs=[];mapping={}
        aa=sorted(newanchors[k])
        for a,bb in zip(aa[:-1],aa[1:]):
            qq,radial=fit_interval(changed[a:bb+1],radii[k][a:bb+1],changed[a],changed[bb],field,obstacle);mapping[a]=len(out)-1 if out else 0;out.extend(qq[1:] if out else qq);rs.extend(radial[1:] if rs else radial);mapping[bb]=len(out)-1
        fitted[k]=np.array(out);rout[k]=np.array(rs);newanchors[k]=set(mapping.values())
    for other,k,i,old in mobile:
        p=fitted_nodes[ids[k][i]];move=p-old;rec=rr[other];distance=np.linalg.norm(rec['old']-old,axis=1);rec['old']+=move*(1-smoothstep((distance-2.)/6.))[:,None]
    base=mf.Manifold.reserve_ids(len(names)+2000);ret,caps,_=cap_retained(rr,retained,names,base,use_normals=True);solids=[ret]
    for k,q in fitted.items():
        v,f=tube(q,rout[k],sides=40);solid=mf.Manifold(mf.Mesh(v,f,run_index=np.array([0,len(f)*3],np.uint32),run_original_id=np.array([base+names.index(k)],np.uint32)));assert solid.status()==mf.Error.NoError,(k,solid.status());solids.append(solid);print('Smooth vein',k,len(q),'maxstep',np.linalg.norm(np.diff(q,axis=0),axis=1).max(),flush=True)
    union=mf.Manifold.batch_boolean(solids,mf.OpType.Add);assert union.status()==mf.Error.NoError,str(union.status());mesh=union.to_mesh();v=np.array(mesh.vert_properties[:,:3]);f=np.array(mesh.tri_verts);labels=np.zeros(len(f),int)
    for i,oid in enumerate(mesh.run_original_id):labels[mesh.run_index[i]//3:mesh.run_index[i+1]//3]=int(oid)-base
    closed=trimesh.Trimesh(v,f,process=False);closed.export(W/'veins-collision-solid.glb');f=f[labels<len(names)];labels=labels[labels<len(names)];normal=np.zeros_like(v);fn=np.cross(v[f[:,1]]-v[f[:,0]],v[f[:,2]]-v[f[:,0]])
    for i in range(3):np.add.at(normal,f[:,i],fn)
    normal/=np.maximum(np.linalg.norm(normal,axis=1)[:,None],1e-12);replacements={}
    for k in selected+retained:
        ff=f[labels==names.index(k)];assert len(ff),(k,'missing skin');used,ii=np.unique(ff,return_inverse=True);replacements[k]=(v[used],ii.reshape(-1,3),normal[used])
    save_replaced(W/'veins-trial.glb',d,b,replacements);paths={k:{'points':fitted[k].tolist(),'radii':rout[k].tolist(),'sourcePoints':original[k].tolist(),'anchorIndices':sorted(newanchors[k])} for k in selected};(W/'veins-round-courses.json').write_text(json.dumps(paths,separators=(',',':'))+'\n');report={'candidate':60,'accepted':False,'appliedToApp':False,'method':'canonical centreline sections, a coupled smooth anterior envelope with arterial bridges, and circular swept walls','optimizer':{'success':bool(result.success),'iterations':int(result.nit),'nodes':int(M),'curvatureWeight':weight},'hashes':{kind:sha(W/f'{kind}-trial.glb') for kind in ['brain','arteries','veins']},'closedCollisionSolid':bool(closed.is_watertight),'reconstructedLabels':selected};(W/'trial.json').write_text(json.dumps(report,indent=2)+'\n');manifest=json.loads((BASE/'candidate-manifest.json').read_text());manifest['candidateDirectory']='posterior-round60';manifest['candidateHashes']=report['hashes'];(W/'candidate-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')

if __name__=='__main__':main()
