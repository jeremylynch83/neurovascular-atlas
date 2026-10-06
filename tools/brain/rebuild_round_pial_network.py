"""Joint circular-section posterior-fossa reconstruction from candidate 55.

Every actual shared source label interface is a coupled centreline node. The
optimiser therefore moves a branch and its parent together, rather than averaging
two incompatible surface projections afterwards. Closed boolean sweeps supply
real ostia. Temporary source outlet caps are removed from the final labelled skin.
"""
import json,shutil
import numpy as np,trimesh,vtk,manifold3d as mf
from scipy.spatial import cKDTree
from scipy.sparse import coo_matrix
from scipy.sparse.csgraph import connected_components
from scipy.optimize import minimize
from scipy.ndimage import gaussian_filter1d,median_filter
from fit_vessels import APP,read_glb,mesh_records,resample,smoothstep,accessor
from refine_context_skin import save_replaced
from rebuild_tubular_brainstem_veins import tube
from fit_expanded_pial_vessels import SRC,stations,ExposedSurface
from build_targets import poly
from reconcile_brainstem import sha

W=APP/'.authoring/posterior-round57'

class SurfaceDistance:
    """Local tissue union distance, retaining genuine fissure corridors."""
    def __init__(self,parts):
        self.parts=[];self.rays=ExposedSurface(trimesh.util.concatenate(parts));self.offsets=self.rays.offsets
        for m in parts:
            normals=vtk.vtkPolyDataNormals();normals.SetInputData(poly(m));normals.ConsistencyOn();normals.AutoOrientNormalsOn();normals.SplittingOff();normals.Update()
            f=vtk.vtkImplicitPolyDataDistance();f.SetInput(normals.GetOutput());self.parts.append((m.bounds,f))
    def hit(self,p,axis,sign):return self.rays.hit(p,axis,sign)
    def distance(self,p,r):
        best=1e3;gradient=np.zeros(3)
        for bounds,f in self.parts:
            if np.any(p<bounds[0]-r-.1) or np.any(p>bounds[1]+r+.1):continue
            d=f.EvaluateFunction(p)
            if d<best:
                best=d;g=[0.,0.,0.];f.EvaluateGradient(p,g);gradient=np.array(g)
        return best,gradient
    def escape(self,p,r):
        d,g=self.distance(p,r);need=max(0.,r+.035-d);axis=int(np.argmax(abs(g)));sign=1 if g[axis]>=0 else -1
        return need/max(abs(g[axis]),.5),axis,sign

def radius_profile(record,q,param,tt):
    p=np.column_stack([np.interp(param,tt,q[:,i]) for i in range(3)]);rad=np.linalg.norm(record['old']-p,axis=1);r=[]
    for t in tt:
        ids=np.argsort(abs(param-t))[:max(16,int(len(rad)/len(tt)*1.5))];r.append(np.median(rad[ids]))
    return np.clip(gaussian_filter1d(median_filter(np.array(r),5),2),.10,1.35)

def interfaces(rr,selected):
    names=list(rr);points=np.concatenate([rr[k]['old'] for k in selected]);lo=points.min(0)-1e-4;hi=points.max(0)+1e-4;local=[];pp=[];ll=[]
    for k in names:
        v=rr[k]['old'];mask=np.all((v>=lo)&(v<=hi),axis=1)
        if not mask.any():continue
        ll.append(np.full(mask.sum(),len(local)));pp.append(v[mask]);local.append(k)
    p=np.concatenate(pp);labels=np.concatenate(ll)
    _,idx,inv=np.unique(np.round(p,5),axis=0,return_index=True,return_inverse=True);order=np.argsort(inv);same=inv[order][1:]==inv[order][:-1];a=labels[order][:-1][same];b=labels[order][1:][same];coords=p[order][:-1][same];good=a!=b;groups={}
    for aa,bb,point in zip(a[good],b[good],coords[good]):
        if local[aa] not in selected and local[bb] not in selected:continue
        pair=tuple(sorted((local[aa],local[bb])));groups.setdefault(pair,[]).append(point)
    retained=sorted({k for pair in groups for k in pair if k not in selected})
    return retained,{p:np.array(v) for p,v in groups.items()}

def posterior_source(parent,origin_index,med):
    origin=parent[origin_index];surface=ExposedSurface(med);sign=1 if origin[0]>.65 else -1;z0=min(30.,origin[2]-3.);xlat=.65+sign*max(11.5,abs(origin[0]-.65));rear=surface.hit(np.array([.65+sign*4.,-85.,z0]),1,-1)
    assert rear is not None
    points=[origin,origin+np.array([sign*1.,-2.,-1.5]),np.array([xlat,rear-.25,z0])]
    for z in np.linspace(z0-1,-30,150):
        x=.65+sign*(4+7.5*np.exp(-(z0-z)/4));hit=surface.hit(np.array([x,-85,z]),1,-1)
        if hit is None:hit=rear
        points.append(np.array([x,hit-.25,z]))
    return resample(np.array(points),190)

def cap_retained(rr,retained,names,base,old_psa=None,use_normals=False):
    vv=[];ff=[];tags=[];offset=0
    for k in retained:
        vv.append(rr[k]['old']);ff.append(rr[k]['faces']+offset);tags.extend([names.index(k)]*len(rr[k]['faces']));offset+=len(rr[k]['old'])
    v=np.concatenate(vv);f=np.concatenate(ff);labels=np.array(tags)
    keys=np.column_stack([v,np.concatenate([rr[k]['_normals'] for k in retained])]) if use_normals else v
    _,idx,inv=np.unique(keys,axis=0,return_index=True,return_inverse=True);v=v[idx];f=inv[f]
    directed=np.concatenate([f[:,[0,1]],f[:,[1,2]],f[:,[2,0]]]);edge_tags=np.tile(labels,3);_,index,count=np.unique(np.sort(directed,axis=1),axis=0,return_index=True,return_counts=True);assert count.max()<=2
    edges=directed[index[count==1]];et=edge_tags[index[count==1]];G=coo_matrix((np.ones(len(edges)),(edges[:,0],edges[:,1])),shape=(len(v),len(v))).tocsr();_,cc=connected_components(G,directed=False);cap_ids=[];keep_caps=[];caps=[]
    for c in np.unique(cc[edges.ravel()]):
        mask=cc[edges[:,0]]==c;edge=edges[mask];points=np.unique(edge);centre=v[points].mean(0);ci=len(v);v=np.vstack([v,centre]);tri=np.column_stack([edge[:,1],edge[:,0],np.full(len(edge),ci)]);f=np.vstack([f,tri]);tag=len(names)+len(cap_ids);labels=np.r_[labels,np.full(len(tri),tag)];cap_ids.append(tag);caps.append(centre)
        if old_psa is not None and (old_psa.query(v[points])[0]<2e-5).mean()>.85:keep_caps.append(tag)
    order=np.argsort(labels,kind='stable');f=f[order];labels=labels[order];values,first=np.unique(labels,return_index=True);run=np.r_[first*3,len(f)*3].astype(np.uint32)
    solid=mf.Manifold(mf.Mesh(v.astype(np.float32),f.astype(np.uint32),run_index=run,run_original_id=(base+values).astype(np.uint32)));assert solid.status()==mf.Error.NoError,str(solid.status())
    return solid,cap_ids,keep_caps

def polish_path(k,q,r,anchors,surface,med_surface):
    """Check complete swept segments, not just the original course stations."""
    anchors=sorted(set([0,len(q)-1]+list(anchors)));out=[];rout=[];mapping={}
    def clearance(p,rad):
        field=med_surface if k.startswith('Posterior spinal ') else surface
        amount,axis,sign=field.escape(p,rad+.065)
        preferred=None
        sg=1 if p[0]>.65 else -1
        if k.startswith('Posterior spinal '):preferred=(1,-1)
        elif k.startswith('PICA ') and p[1]<-100:preferred=(1,-1)
        elif k.startswith('SCA ') and p[1]<-100:preferred=(2,1)
        elif k.startswith('AICA ') and abs(p[0]-.65)>20 and p[1]<-85:preferred=(0,sg)
        elif 'inferior_hemispheric' in k or 'inferior_vermian' in k:preferred=(1,-1)
        elif 'posterior_communicating' in k:preferred=(1,1)
        elif 'lateral_mesencephalic' in k:preferred=(0,sg)
        if amount>1e-4 and preferred is not None:
            axis,sign=preferred;amount=0.
            for point in p+field.offsets*(rad+.065):
                hit=field.hit(point,axis,sign)
                if hit is not None:amount=max(amount,sign*(hit-point[axis])+.04)
        v=p.copy();v[axis]+=sign*amount;return v
    for a,b in zip(anchors[:-1],anchors[1:]):
        points=q[a:b+1].copy();radius=r[a:b+1].copy();start,end=points[0].copy(),points[-1].copy()
        for iteration in range(5):
            arc=np.r_[0,np.cumsum(np.linalg.norm(np.diff(points,axis=0),axis=1))];good=np.r_[True,np.diff(arc)>1e-7];arc=arc[good];points=points[good];radius=radius[good]
            if arc[-1]<1e-5:break
            tt=np.linspace(0,arc[-1],max(3,int(arc[-1]/.20)+1));points=np.column_stack([np.interp(tt,arc,points[:,i]) for i in range(3)]);radius=np.interp(tt,arc,radius)
            points=gaussian_filter1d(points,1.2,axis=0);points[0]=start;points[-1]=end
            for i in range(1,len(points)-1):points[i]=clearance(points[i],radius[i])
        mapping[a]=len(out) if not out else len(out)-1
        if out:out.extend(points[1:]);rout.extend(radius[1:])
        else:out.extend(points);rout.extend(radius)
        mapping[b]=len(out)-1
    return np.array(out),np.array(rout),mapping

def solve(curves,radii,links,fixed,surface,kind,obstacle=None,med_surface=None):
    keys=list(curves);offset={};allq=[];allr=[];N=0
    for k in keys:offset[k]=N;allq.extend(curves[k]);allr.extend(radii[k]);N+=len(curves[k])
    q=np.array(allq);r=np.array(allr);uf=np.arange(N)
    def find(a):
        while uf[a]!=a:uf[a]=uf[uf[a]];a=uf[a]
        return a
    for a,i,b,j in links:
        aa,bb=find(offset[a]+i),find(offset[b]+j);uf[bb]=aa
    roots=np.array([find(i) for i in range(N)]);_,inv=np.unique(roots,return_inverse=True);M=inv.max()+1;counts=np.bincount(inv);source=np.zeros((M,3));np.add.at(source,inv,q);source/=counts[:,None];radius=np.zeros(M);np.maximum.at(radius,inv,r);indices={k:inv[offset[k]:offset[k]+len(curves[k])] for k in keys};q=source.copy();fixed_mask=np.zeros(M,bool);fixed_points=q.copy()
    for k,i,p in fixed:node=indices[k][i];fixed_mask[node]=True;fixed_points[node]=p;source[node]=p;q[node]=p
    rows=[];cols=[];vals=[];row=0
    for k in keys:
        ids=indices[k]
        for i in range(1,len(ids)-1):rows.extend([row]*3);cols.extend(ids[i-1:i+2]);vals.extend([1.,-2.,1.]);row+=1
    D=coo_matrix((vals,(rows,cols)),shape=(row,M)).tocsr();K=(D.T@D).tocsr();weight=1.;logs=[];persistent_lo=source-40.;persistent_hi=source+40.
    preferred={};spinal_tail=set()
    for k in keys:
        for station,node in enumerate(indices[k]):
            p=source[node];sign=1 if p[0]>.65 else -1
            if k.startswith('Posterior spinal ') and station>=30:spinal_tail.add(node);preferred[node]=(1,-1)
            elif k.startswith('PICA ') and p[1]<-100:preferred[node]=(1,-1)
            elif k.startswith('AICA ') and abs(p[0]-.65)>20 and p[1]<-85:preferred[node]=(0,sign)
            elif k.startswith('SCA ') and p[1]<-100:preferred[node]=(2,1)
            elif 'inferior_hemispheric' in k or 'inferior_vermian' in k:preferred[node]=(1,-1)
            elif 'posterior_communicating' in k:preferred[node]=(1,1)
            elif 'lateral_mesencephalic' in k:preferred[node]=(0,sign)
    for iteration in range(10):
        lo=persistent_lo.copy();hi=persistent_hi.copy();desired=source.copy();largest=0.
        for i,p in enumerate(q):
            if fixed_mask[i]:continue
            field=med_surface if i in spinal_tail else surface
            amount,axis,sign=field.escape(p,radius[i]+.045)
            if amount>.001 and i in preferred:
                axis,sign=preferred[i];amount=0.
                for point in p+field.offsets*(radius[i]+.045):
                    hit=field.hit(point,axis,sign)
                    if hit is not None:amount=max(amount,sign*(hit-point[axis])+.04)
            largest=max(largest,amount)
            if amount>1e-4:
                limit=p[axis]+sign*amount
                if sign==1:lo[i,axis]=max(lo[i,axis],min(limit,hi[i,axis]))
                else:hi[i,axis]=min(hi[i,axis],max(limit,lo[i,axis]))
            if obstacle is not None and obstacle.EvaluateFunction(p)<radius[i]+.06:
                # The nearest exposed-skin direction defines superficial lift.
                possibilities=[]
                for ax in range(3):
                    for sg in [-1,1]:
                        hit=surface.hit(p,ax,sg)
                        if hit is not None:
                            gap=sg*(p[ax]-hit)-radius[i]
                            if gap>=-.05:possibilities.append((gap,ax,sg))
                _,ax,sg=min(possibilities) if possibilities else (0.,1,1)
                lift=None
                for step in np.arange(.1,8.01,.1):
                    test=p.copy();test[ax]+=sg*step
                    if obstacle.EvaluateFunction(test)>=radius[i]+.06:lift=step;break
                if lift is not None:
                    limit=p[ax]+sg*lift
                    if sg==1:lo[i,ax]=max(lo[i,ax],min(limit,hi[i,ax]))
                    else:hi[i,ax]=min(hi[i,ax],max(limit,lo[i,ax]))
        for k in keys:
            if k.startswith('Posterior spinal '):
                for node in indices[k][30:]:
                    lo[node,0]=hi[node,0]=source[node,0];lo[node,2]=hi[node,2]=source[node,2]
                    p=q[node];need=0.
                    for point in p+med_surface.offsets*(radius[node]+.03):
                        hit=med_surface.hit(point,1,-1)
                        if hit is not None:need=max(need,-(hit-point[1])+.03)
                    hi[node,1]=min(hi[node,1],p[1]-need);lo[node,1]=-np.inf
        lo[fixed_mask]=fixed_points[fixed_mask];hi[fixed_mask]=fixed_points[fixed_mask];persistent_lo=lo.copy();persistent_hi=hi.copy();before=q.copy();success=[]
        for dim in range(3):
            target=desired[:,dim]
            def objective(v):
                d=v-target;delta=v-source[:,dim];kv=K@delta;return .5*np.dot(d,d)+.5*weight*np.dot(delta,kv),d+weight*kv
            result=minimize(objective,np.clip(q[:,dim],lo[:,dim],hi[:,dim]),jac=True,bounds=list(zip(lo[:,dim],hi[:,dim])),method='L-BFGS-B',options={'maxiter':1000,'ftol':1e-11,'gtol':1e-6,'maxls':40});q[:,dim]=result.x;success.append(bool(result.success))
        movement=np.linalg.norm(q-before,axis=1);worst=int(movement.argmax());owners=[(k,int(np.argmin(abs(indices[k]-worst)))) for k in keys if worst in indices[k]]
        row={'iteration':iteration,'sphereCorrectionMm':float(largest),'maximumMovementMm':float(movement.max()),'worstOwners':owners,'before':before[worst].tolist(),'after':q[worst].tolist(),'source':source[worst].tolist(),'success':success};logs.append(row);print(kind,row,flush=True)
        if largest<.005 and np.linalg.norm(q-before,axis=1).max()<.015 and iteration>=3:break
    return {k:q[indices[k]] for k in keys},logs

def main():
    import argparse
    parser=argparse.ArgumentParser();parser.add_argument('--veins-only',action='store_true');args=parser.parse_args()
    W.mkdir(exist_ok=True);shutil.copyfile(APP/'.authoring/posterior-pial56/brain-trial.glb',W/'brain-trial.glb');shutil.copyfile(APP/'.authoring/posterior-pial56/cord-context.json',W/'cord-context.json')
    metadata=json.loads((APP/'deliverables/posterior-fossa-expanded-review/model-review.json').read_text());brain=trimesh.load(W/'brain-trial.glb',process=False);parts=[];stem_keys=set()
    for name in ['pons','medulla-oblongata','midbrain','base-of-peduncle']:
        pair=[f'brain.{name}.{s}' for s in ['left','right']];stem_keys.update(pair);m=trimesh.util.concatenate([brain.geometry[k] for k in pair]);m.merge_vertices(digits_vertex=5)
        midsag=(np.abs(m.vertices[m.faces,0]-.65).max(1)<.08)&(abs(m.face_normals[:,0])>.9);m.update_faces(~midsag);parts.append(m)
    parts += [brain.geometry[k] for k in metadata['groups']['brain'] if k not in stem_keys]+[brain.geometry['brain.upper-cervical-cord']];surface=ExposedSurface(trimesh.util.concatenate(parts));med_surface=ExposedSurface(trimesh.util.concatenate([brain.geometry['brain.medulla-oblongata.'+s] for s in ['left','right']]+[brain.geometry['brain.upper-cervical-cord']]));report={'parentDirectory':str(SRC.relative_to(APP)),'method':'regional exposed-surface sphere envelopes, joint centreline constraints, circular swept walls, labelled boolean ostia','accepted':False,'appliedToApp':False,'kinds':{}}
    profiles={r['id']:r for r in json.loads((APP/'anatomy/source/venous/fitted-paths.json').read_text())};obstacle=None
    if args.veins_only:
        closed=trimesh.load(W/'arteries-collision-solid.glb',force='mesh',process=False);obstacle=vtk.vtkImplicitPolyDataDistance();obstacle.SetInput(poly(closed));report=json.loads((W/'trial.json').read_text())
    for kind in ['arteries','veins']:
        if args.veins_only and kind=='arteries':continue
        d,b=read_glb(SRC/f'{kind}-trial.glb');rr=mesh_records(d,b);names=list(rr)
        for record in rr.values():record['_normals']=accessor(d,b,record['primitive']['attributes']['NORMAL']).copy()
        selected=metadata['groups']['arteries'] if kind=='arteries' else metadata['groups']['veins']
        selected=[k for k in selected if k!='Basilar' and not any(t in k.lower() for t in ['perforator','paramedian']) and not k.startswith('Posterior spinal ')]
        retained,pairs=interfaces(rr,selected);curves={};radii={}
        for k in selected:
            q,r,param,tt=stations(rr[k]);curves[k]=q;radii[k]=radius_profile(rr[k],q,param,tt)
            if kind=='veins' and k in profiles:
                values=np.array(profiles[k]['radii']);radii[k]=np.interp(np.linspace(0,1,len(q)),np.linspace(0,1,len(values)),values)
            print('Source course',kind,k,len(q),flush=True)
        links=[];fixed=[];mobile=[]
        for (a,bb),p in pairs.items():
            centre=p.mean(0)
            if a in curves and bb in curves:
                i=int(np.argmin(np.linalg.norm(curves[a]-centre,axis=1)));j=int(np.argmin(np.linalg.norm(curves[bb]-centre,axis=1)));links.append((a,i,bb,j))
            else:
                k=a if a in curves else bb;other=bb if k==a else a;i=int(np.argmin(np.linalg.norm(curves[k]-centre,axis=1)))
                if kind=='arteries' and any(t in other.lower() for t in ['perforator','paramedian']):
                    curves[k][i]=centre;mobile.append((other,k,i,centre))
                else:fixed.append((k,i,centre))
        spinal=[]
        if kind=='arteries':
            med=trimesh.util.concatenate([brain.geometry['brain.medulla-oblongata.'+s] for s in ['left','right']]+[brain.geometry['brain.upper-cervical-cord']])
            for side in ['left','right']:
                k='PICA '+side;source=curves[k];ends=cKDTree(rr['Vertebral V4 '+side]['old']).query(source[[0,-1]])[0];i=int((.16 if ends[0]<ends[1] else .84)*(len(source)-1));sk='Posterior spinal '+side;curves[sk]=posterior_source(source,i,med);radii[sk]=np.linspace(.235,.175,len(curves[sk]));selected.append(sk);links.append((k,i,sk,0));spinal.append({'side':side,'picaIndex':i,'picaNode':k,'spinalNode':sk,'oldV3OstiumClosed':True,'proximalFractionFromPicaOrigin':.16})
        fitted,logs=solve(curves,radii,links,fixed,surface,kind,obstacle,med_surface)
        anchor_sets={k:set() for k in fitted}
        for a,i,bb,j in links:anchor_sets[a].add(i);anchor_sets[bb].add(j)
        for k,i,p in fixed:anchor_sets[k].add(i)
        for other,k,i,p in mobile:anchor_sets[k].add(i)
        remap={}
        for k in list(fitted):
            fitted[k],radii[k],remap[k]=polish_path(k,fitted[k],radii[k],anchor_sets[k],surface,med_surface)
            print('Dense swept course checked',kind,k,len(fitted[k]),flush=True)
        # Carry penetrating branch collars with the pial parent while retaining
        # their distal parenchymal entry. Shared source material points receive
        # the same local translation before the retained solid is capped.
        for other,k,i,centre in mobile:
            displacement=fitted[k][remap[k][i]]-centre;record=rr[other];distance=np.linalg.norm(record['old']-centre,axis=1);weight=1-smoothstep((distance-2.)/4.);record['old']=record['old']+displacement*weight[:,None]
        base=mf.Manifold.reserve_ids(len(names)+2000);old_spinal=cKDTree(np.concatenate([rr['Posterior spinal '+s]['old'] for s in ['left','right']])) if kind=='arteries' else None
        ret,capids,keepcaps=cap_retained(rr,retained,names,base,old_spinal,use_normals=kind=='veins');solids=[ret]
        for k,q in fitted.items():
            v,f=tube(q,radii[k],sides=40);solid=mf.Manifold(mf.Mesh(v,f,run_index=np.array([0,len(f)*3],np.uint32),run_original_id=np.array([base+names.index(k)],np.uint32)));assert solid.status()==mf.Error.NoError,(k,str(solid.status()));solids.append(solid)
        union=mf.Manifold.batch_boolean(solids,mf.OpType.Add);print('Union',kind,union.status(),union.num_tri(),flush=True);assert union.status()==mf.Error.NoError
        mesh=union.to_mesh();v=np.array(mesh.vert_properties[:,:3]);f=np.array(mesh.tri_verts);labels=np.zeros(len(f),int)
        for i,oid in enumerate(mesh.run_original_id):labels[mesh.run_index[i]//3:mesh.run_index[i+1]//3]=int(oid)-base
        closed=trimesh.Trimesh(v,f,process=False);closed.export(W/f'{kind}-collision-solid.glb')
        if kind=='arteries':obstacle=vtk.vtkImplicitPolyDataDistance();obstacle.SetInput(poly(closed))
        # Two caps seal the abandoned vertebral posterior-spinal ostia.
        for tag in keepcaps:
            mask=labels==tag;centres=v[f[mask]].mean((0,1));parent='Vertebral V3 '+('right' if centres[0]>.65 else 'left');labels[mask]=names.index(parent)
        keep=labels<len(names);f=f[keep];labels=labels[keep];normal=np.zeros_like(v);fn=np.cross(v[f[:,1]]-v[f[:,0]],v[f[:,2]]-v[f[:,0]])
        for i in range(3):np.add.at(normal,f[:,i],fn)
        normal/=np.maximum(np.linalg.norm(normal,axis=1)[:,None],1e-12);replacements={}
        for k in selected+retained:
            ff=f[labels==names.index(k)];assert len(ff),(kind,'Lost label',k);used,inv=np.unique(ff,return_inverse=True);replacements[k]=(v[used],inv.reshape(-1,3),normal[used])
        save_replaced(W/f'{kind}-trial.glb',d,b,replacements)
        paths={k:{'sourcePoints':curves[k].tolist(),'points':fitted[k].tolist(),'radii':radii[k].tolist()} for k in fitted};(W/f'{kind}-round-courses.json').write_text(json.dumps(paths,separators=(',',':'))+'\n')
        report['kinds'][kind]={'reconstructedLabels':selected,'retainedInterfaceLabels':retained,'sharedCentrelineLinks':len(links),'fixedOutletNodes':len(fixed),'optimizer':logs,'booleanStatus':str(union.status()),'closedCollisionSolid':bool(closed.is_watertight),'oldSpinalOstiaSealed':len(keepcaps)}
        if kind=='arteries':
            for row in spinal:row.update(points=fitted[row['spinalNode']].tolist(),radii=radii[row['spinalNode']].tolist(),origin=fitted[row['spinalNode']][0].tolist(),parent=row['picaNode'])
            (W/'posterior-spinal-courses.json').write_text(json.dumps(spinal,indent=2)+'\n')
        (W/'trial.json').write_text(json.dumps(report,indent=2)+'\n')
    report['hashes']={k:sha(W/f'{k}-trial.glb') for k in ['brain','arteries','veins']};(W/'trial.json').write_text(json.dumps(report,indent=2)+'\n')
    manifest=json.loads((APP/'.authoring/posterior-pial56/candidate-manifest.json').read_text());manifest['candidateDirectory']='posterior-round57';(W/'candidate-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')

if __name__=='__main__':main()
