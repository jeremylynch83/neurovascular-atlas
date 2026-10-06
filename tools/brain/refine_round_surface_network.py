"""Refine candidate 57 with exact tissue-distance constraints on round sweeps."""
import json,shutil
import numpy as np,trimesh,vtk,manifold3d as mf
from scipy.spatial import cKDTree
from scipy.ndimage import gaussian_filter1d
from scipy.sparse import coo_matrix
from scipy.sparse.csgraph import connected_components
from fit_vessels import APP,read_glb,mesh_records,accessor,resample,smoothstep
from rebuild_round_pial_network import interfaces,cap_retained
from rebuild_tubular_brainstem_veins import tube
from refine_context_skin import save_replaced
from build_targets import poly
from reconcile_brainstem import sha
from fit_expanded_pial_vessels import ExposedSurface

SRC=APP/'.authoring/posterior-round57'
W=APP/'.authoring/posterior-round58'
DENSE_ONLY=False
RESTORED=set()

def retain_collision_topology(source,rr,retained,names,base):
    """Keep native Boolean vertex identities at coincident tangent seams."""
    skin=trimesh.load(source,force='mesh',process=False);sv=np.asarray(skin.vertices);sf=np.asarray(skin.faces);allv=[sv]+[rr[k]['_original'] for k in names];lengths=np.cumsum([0]+[len(v) for v in allv]);_,inv=np.unique(np.concatenate(allv),axis=0,return_inverse=True);skin_ids=inv[:len(sv)];keys=[np.sort(skin_ids[sf],axis=1)];tags=[]
    for j,k in enumerate(names):
        ids=inv[lengths[j+1]:lengths[j+2]];keys.append(np.sort(ids[rr[k]['faces']],axis=1));tags.extend([j]*len(rr[k]['faces']))
    lengths_f=np.cumsum([0]+[len(k) for k in keys]);_,face_inv=np.unique(np.concatenate(keys),axis=0,return_inverse=True);lab=np.full(face_inv.max()+1,len(names),int);lab[face_inv[lengths_f[1]:]]=np.array(tags);labels=lab[face_inv[:len(sf)]];keep=np.isin(labels,[names.index(k) for k in retained]+[len(names)]);f=sf[keep].copy();labels=labels[keep];v=sv.copy()
    delta=np.zeros((inv.max()+1,3));magnitude=np.zeros(len(delta))
    for j,k in enumerate(names):
        if k not in retained:continue
        ids=inv[lengths[j+1]:lengths[j+2]];d=rr[k]['old']-rr[k]['_original'];mag=np.linalg.norm(d,axis=1);changed=mag>magnitude[ids]+1e-8;delta[ids[changed]]=d[changed];magnitude[ids[changed]]=mag[changed]
    v+=delta[skin_ids]
    directed=np.concatenate([f[:,[0,1]],f[:,[1,2]],f[:,[2,0]]]);_,index,count=np.unique(np.sort(directed,axis=1),axis=0,return_index=True,return_counts=True);assert count.max()<=2;edges=directed[index[count==1]];G=coo_matrix((np.ones(len(edges)),(edges[:,0],edges[:,1])),shape=(len(v),len(v))).tocsr();_,cc=connected_components(G,directed=False);caps=[len(names)]
    for component in np.unique(cc[edges.ravel()]):
        edge=edges[cc[edges[:,0]]==component];points=np.unique(edge);ci=len(v);v=np.vstack([v,v[points].mean(0)]);tri=np.column_stack([edge[:,1],edge[:,0],np.full(len(edge),ci)]);f=np.vstack([f,tri]);tag=len(names)+len(caps);caps.append(tag);labels=np.r_[labels,np.full(len(tri),tag)]
    order=np.argsort(labels,kind='stable');f=f[order];labels=labels[order];values,first=np.unique(labels,return_index=True);run=np.r_[first*3,len(f)*3].astype(np.uint32);solid=mf.Manifold(mf.Mesh(v.astype(np.float32),f.astype(np.uint32),run_index=run,run_original_id=(base+values).astype(np.uint32)));assert solid.status()==mf.Error.NoError,str(solid.status());return solid,caps,[]

class Clearance:
    def __init__(self,mesh):
        self.mesh=mesh;self.field=vtk.vtkImplicitPolyDataDistance();self.field.SetInput(poly(mesh));self.rays=ExposedSurface(mesh)
    def arterial_envelope(self,mesh):
        self.rays=ExposedSurface(trimesh.util.concatenate([self.mesh,mesh]))
    def direction(self,p):
        cp=[0.,0.,0.];self.field.EvaluateFunctionAndGetClosestPoint(p,cp);g=p-np.array(cp)
        return g/max(np.linalg.norm(g),1e-10)
    def point(self,p,r,obstacle=None,preferred=None,lift_direction=None,outward_reference=None):
        p=p.copy()
        reference=outward_reference
        if preferred is not None:
            axis,sign=preferred;amount=0.
            for point in p+self.rays.offsets*(r+.08):
                hit=self.rays.hit(point,axis,sign)
                if hit is not None:amount=max(amount,sign*(hit-point[axis])+.06)
            p[axis]+=sign*amount
        for _ in range(30):
            cp=[0.,0.,0.];d=self.field.EvaluateFunctionAndGetClosestPoint(p,cp)
            if reference is not None:d=abs(d)*(1 if np.dot(p-np.array(cp),reference)>=0 else -1)
            if (abs(d) if preferred is not None else d)>=r+.075:break
            if reference is not None:g=reference
            else:
                g=[0.,0.,0.];self.field.EvaluateGradient(p,g);g=np.array(g);g/=max(np.linalg.norm(g),1e-10)
            if preferred is not None:
                axis,sign=preferred;p[axis]+=sign*.08
            else:p+=g*min(1.5,r+.08-d)
        if obstacle is not None:
            if preferred is not None:
                axis,sign=preferred;outward=np.zeros(3);outward[axis]=sign
            else:outward=reference if reference is not None else self.direction(p)
            for _ in range(50):
                d=obstacle.EvaluateFunction(p)
                if d>=r+.065:break
                g=outward
                if preferred is None:
                    ag=[0.,0.,0.];obstacle.EvaluateGradient(p,ag);ag=np.array(ag);ag/=max(np.linalg.norm(ag),1e-10);dot=np.dot(ag,outward)
                    if dot>-.5:
                        g=ag-outward*min(dot,0.);g/=max(np.linalg.norm(g),1e-10)
                # Lift the vein away from tissue, over the crossing artery.
                p+=g*min(.20,max(.06,r+.075-d))
                if reference is not None:
                    cp=[0.,0.,0.];bd=self.field.EvaluateFunctionAndGetClosestPoint(p,cp);bd=abs(bd)*(1 if np.dot(p-np.array(cp),reference)>=0 else -1)
                    if bd<r+.075:p+=reference*(r+.08-bd)
            if obstacle.EvaluateFunction(p)<r+.065:
                directions=[outward]+[np.eye(3)[axis]*sign for axis in range(3) for sign in [-1,1]]
                escaped=None
                for distance in np.arange(.1,6.01,.1):
                    for direction in directions:
                        if np.dot(direction,outward)<-.05:continue
                        candidate=p+direction*distance;cp=[0.,0.,0.];bd=self.field.EvaluateFunctionAndGetClosestPoint(candidate,cp);bd=abs(bd)*(1 if np.dot(candidate-np.array(cp),outward)>=0 else -1)
                        if bd>=r+.075 and obstacle.EvaluateFunction(candidate)>=r+.075:escaped=candidate;break
                    if escaped is not None:break
                if escaped is not None:p=escaped
        return p

def vein_lift(k,p):
    if 'inferior_hemispheric' in k or 'inferior_vermian' in k:return (1,-1)
    if 'lateral_mesencephalic' in k:return (0,1 if k.endswith('right') else -1)
    if 'superior_petrosal_vein' in k:return (1,1)
    if 'anterior_' in k or 'posterior_communicating' in k or 'pontomedullary' in k or 'transverse_pontine' in k:return (1,1)
    return (2,1)

def fit_interval(q,r,start,end,field,obstacle,preferred=None,lift_direction=None):
    q=q.copy();q[0]=start;q[-1]=end
    normals=np.array([field.direction(p) for p in q]) if obstacle is not None else None
    for iteration in range(16):
        arc=np.r_[0,np.cumsum(np.linalg.norm(np.diff(q,axis=0),axis=1))];good=np.r_[True,np.diff(arc)>1e-8];q=q[good];r=r[good];arc=arc[good]
        if normals is not None:normals=normals[good]
        if arc[-1]<1e-6:return np.array([start,end]),np.array([r[0],r[-1]])
        tt=np.linspace(0,arc[-1],max(3,int(np.ceil(arc[-1]/.12))+1));q=np.column_stack([np.interp(tt,arc,q[:,j]) for j in range(3)]);r=np.interp(tt,arc,r)
        if normals is not None:
            normals=np.column_stack([np.interp(tt,arc,normals[:,j]) for j in range(3)]);normals=gaussian_filter1d(normals,2.,axis=0);normals/=np.maximum(np.linalg.norm(normals,axis=1)[:,None],1e-10)
        if not DENSE_ONLY:q=gaussian_filter1d(q,2.,axis=0)
        q[0]=start;q[-1]=end
        before=q.copy()
        for i in range(1,len(q)-1):q[i]=field.point(q[i],r[i],obstacle,preferred,lift_direction,normals[i] if normals is not None else None)
        step=np.linalg.norm(np.diff(q,axis=0),axis=1).max()
        if iteration>=5 and step<.20 and np.linalg.norm(q-before,axis=1).max()<.002:break
    return q,r

def main():
    global DENSE_ONLY,RESTORED
    import argparse
    parser=argparse.ArgumentParser();parser.add_argument('--veins-only',action='store_true');parser.add_argument('--arteries-only',action='store_true');parser.add_argument('--polish-veins',action='store_true');parser.add_argument('--restore-collector-curves',action='store_true');args=parser.parse_args()
    if args.restore_collector_curves:
        args.polish_veins=True;RESTORED={'vein.posterior_communicating'}|{f'vein.{k}.{s}' for k in ['superior_petrosal_vein','lateral_mesencephalic'] for s in ['left','right']}
    if args.polish_veins:args.veins_only=True;DENSE_ONLY=True
    W.mkdir(exist_ok=True)
    for file in ['brain-trial.glb','cord-context.json']:shutil.copyfile(SRC/file,W/file)
    meta=json.loads((APP/'deliverables/posterior-fossa-expanded-review/model-review.json').read_text());brain=trimesh.load(W/'brain-trial.glb',process=False);target=trimesh.util.concatenate([brain.geometry[k] for k in meta['groups']['brain']]+[brain.geometry['brain.upper-cervical-cord']]);field=Clearance(target);obstacle=None;report={'candidate':58,'parentDirectory':str(SRC.relative_to(APP)),'accepted':False,'appliedToApp':False,'method':'dense circular sweeps with exact signed tissue-distance clearance and shared branch anchors','kinds':{}}
    if args.veins_only:
        closed=trimesh.load(W/'arteries-collision-solid.glb',force='mesh',process=False);obstacle=vtk.vtkImplicitPolyDataDistance();obstacle.SetInput(poly(closed));report=json.loads((W/'trial.json').read_text())
        if RESTORED:field.arterial_envelope(closed)
    if args.arteries_only:report=json.loads((W/'trial.json').read_text())
    for kind in ['veins'] if args.veins_only else ['arteries'] if args.arteries_only else ['arteries','veins']:
        model_source=W if args.polish_veins else SRC
        d,b=read_glb(model_source/f'{kind}-trial.glb');rr=mesh_records(d,b);names=list(rr)
        for rec in rr.values():rec['_normals']=accessor(d,b,rec['primitive']['attributes']['NORMAL']).copy();rec['_original']=rec['old'].copy()
        saved=json.loads((model_source/f'{kind}-round-courses.json').read_text());selected=list(saved)
        if RESTORED:
            canonical=json.loads((APP/'.authoring/posterior-tubular55/tubular-courses.json').read_text())
            for k in RESTORED:saved[k]=canonical[k].copy()
        curves={k:np.array(v['points']) for k,v in saved.items()};radii={k:np.array(v['radii']) for k,v in saved.items()};retained,pairs=interfaces(rr,selected);links=[];mobile=[]
        for (a,bb),points in pairs.items():
            centre=points.mean(0)
            if a in curves and bb in curves:
                if kind=='arteries' and (a.startswith('Posterior spinal ') or bb.startswith('Posterior spinal ')):continue
                distance,j=cKDTree(curves[bb]).query(curves[a]);i=int(distance.argmin());j=int(j[i])
                if distance[i]<1e-4:links.append((a,i,bb,j))
                else:links.append((a,int(np.linalg.norm(curves[a]-centre,axis=1).argmin()),bb,int(np.linalg.norm(curves[bb]-centre,axis=1).argmin())))
            else:
                k=a if a in curves else bb;other=bb if k==a else a;i=int(np.linalg.norm(curves[k]-centre,axis=1).argmin());mobile.append((other,k,i,curves[k][i].copy()))
        spinal=[]
        if kind=='arteries':
            for side in ['left','right']:
                k='PICA '+side;va='Vertebral V4 '+side;q=curves[k];distance,j=cKDTree(curves[va]).query(q);root=int(distance.argmin());arc=np.r_[0,np.cumsum(np.linalg.norm(np.diff(q,axis=0),axis=1))];direction=1 if root<len(q)/2 else -1;i=int(np.abs(arc-(arc[root]+direction*4.)).argmin());origin=q[i].copy();sg=1 if side=='right' else -1
                # A single smooth lateral-to-dorsal transition, followed by a
                # monotonic caudal course on the dorsal medulla and cord.
                z0=min(32.,origin[2]-1.5);xlat=origin[0];ps=[origin,np.array([xlat,origin[1]-3.,origin[2]-.6]),np.array([.65+sg*4.,-94.,z0])]
                for z in np.linspace(z0-1,-30,190):
                    x=.65+sg*4.;ps.append(np.array([x,-92.,z]))
                sk='Posterior spinal '+side;curves[sk]=resample(np.array(ps),500);radii[sk]=np.linspace(.235,.175,500);links.append((k,i,sk,0));spinal.append({'side':side,'picaNode':k,'spinalNode':sk,'oldV3OstiumClosed':True,'distanceFromPicaVertebralJoinMm':float(abs(arc[i]-arc[root])),'oldPicaIndex':i})
        anchors={k:{0,len(q)-1} for k,q in curves.items()}
        for a,i,bb,j in links:anchors[a].add(i);anchors[bb].add(j)
        for _,k,i,_ in mobile:anchors[k].add(i)
        # Union the branch anchor graph; every member receives one position.
        groups={};parent={}
        def find(v):
            parent.setdefault(v,v)
            if parent[v]!=v:parent[v]=find(parent[v])
            return parent[v]
        for a,i,bb,j in links:parent[find((bb,j))]=find((a,i))
        for k,ids in anchors.items():
            for i in ids:groups.setdefault(find((k,i)),[]).append((k,i))
        for members in groups.values():
            p=np.mean([curves[k][i] for k,i in members],axis=0);r=max(radii[k][i] for k,i in members);special=next((k for k,i in members if k.startswith('PCA short circumflex ')),None);preferred=(0,1 if special.endswith('right') else -1) if special else (1,1) if any(k in RESTORED for k,i in members) else None;lift_direction=vein_lift(members[0][0],p) if kind=='veins' else None;reference=field.direction(p) if kind=='veins' else None;p=field.point(p,r,obstacle,preferred,lift_direction,reference)
            for k,i in members:curves[k][i]=p
        fitted={};newr={};remap={}
        for k,q in curves.items():
            ids=sorted(anchors[k]);out=[];rout=[];mapping={}
            for a,bb in zip(ids[:-1],ids[1:]):
                preferred=(0,1 if k.endswith('right') else -1) if k.startswith('PCA short circumflex ') else (1,1) if k in RESTORED else None
                lift_direction=vein_lift(k,q[a]) if kind=='veins' else None
                qq,rad=fit_interval(q[a:bb+1],radii[k][a:bb+1],q[a],q[bb],field,obstacle,preferred,lift_direction);mapping[a]=len(out)-1 if out else 0
                out.extend(qq[1:] if out else qq);rout.extend(rad[1:] if rout else rad);mapping[bb]=len(out)-1
            fitted[k]=np.array(out);newr[k]=np.array(rout);remap[k]=mapping
            print('Refined',kind,k,'nodes',len(out),'maxstep',np.linalg.norm(np.diff(fitted[k],axis=0),axis=1).max(),flush=True)
        # Retain the rest of the atlas and move only adjoining source collars.
        for other,k,i,old in mobile:
            delta=fitted[k][remap[k][i]]-old;rec=rr[other];distance=np.linalg.norm(rec['old']-old,axis=1);weight=1-smoothstep((distance-2.)/6.);rec['old']+=delta*weight[:,None]
        pending={k:{'points':fitted[k].tolist(),'radii':newr[k].tolist(),'sourcePoints':saved[k]['sourcePoints'],'anchorIndices':sorted(remap[k].values())} for k in fitted};(W/f'{kind}-pending-courses.json').write_text(json.dumps(pending,separators=(',',':'))+'\n')
        base=mf.Manifold.reserve_ids(len(names)+2000)
        if args.polish_veins:ret,caps,keepcaps=retain_collision_topology(model_source/'veins-collision-solid.glb',rr,retained,names,base)
        else:ret,caps,keepcaps=cap_retained(rr,retained,names,base,use_normals=True)
        solids=[ret]
        for k,q in fitted.items():
            v,f=tube(q,newr[k],sides=40);solid=mf.Manifold(mf.Mesh(v,f,run_index=np.array([0,len(f)*3],np.uint32),run_original_id=np.array([base+names.index(k)],np.uint32)));assert solid.status()==mf.Error.NoError,(k,solid.status());solids.append(solid)
        union=mf.Manifold.batch_boolean(solids,mf.OpType.Add);assert union.status()==mf.Error.NoError,str(union.status());mesh=union.to_mesh();v=np.array(mesh.vert_properties[:,:3]);f=np.array(mesh.tri_verts);labels=np.zeros(len(f),int)
        for i,oid in enumerate(mesh.run_original_id):labels[mesh.run_index[i]//3:mesh.run_index[i+1]//3]=int(oid)-base
        closed=trimesh.Trimesh(v,f,process=False);closed.export(W/f'{kind}-collision-solid.glb')
        if kind=='arteries':obstacle=vtk.vtkImplicitPolyDataDistance();obstacle.SetInput(poly(closed))
        f=f[labels<len(names)];labels=labels[labels<len(names)];normal=np.zeros_like(v);fn=np.cross(v[f[:,1]]-v[f[:,0]],v[f[:,2]]-v[f[:,0]])
        for i in range(3):np.add.at(normal,f[:,i],fn)
        normal/=np.maximum(np.linalg.norm(normal,axis=1)[:,None],1e-12);replacements={}
        for k in selected+retained:
            ff=f[labels==names.index(k)];assert len(ff),(kind,k);used,inv=np.unique(ff,return_inverse=True);replacements[k]=(v[used],inv.reshape(-1,3),normal[used])
        save_replaced(W/f'{kind}-trial.glb',d,b,replacements)
        paths={k:{'points':fitted[k].tolist(),'radii':newr[k].tolist(),'sourcePoints':saved[k]['sourcePoints'],'anchorIndices':sorted(remap[k].values())} for k in fitted};(W/f'{kind}-round-courses.json').write_text(json.dumps(paths,separators=(',',':'))+'\n')
        if kind=='arteries':
            for row in spinal:
                row.update(picaIndex=remap[row['picaNode']][row['oldPicaIndex']],points=fitted[row['spinalNode']].tolist(),radii=newr[row['spinalNode']].tolist(),origin=fitted[row['spinalNode']][0].tolist(),parent=row['picaNode'])
            (W/'posterior-spinal-courses.json').write_text(json.dumps(spinal,indent=2)+'\n')
        report['kinds'][kind]={'reconstructedLabels':selected,'retainedInterfaceLabels':retained,'sharedCentrelineLinks':len(links),'booleanStatus':str(union.status()),'closedCollisionSolid':bool(closed.is_watertight)};(W/'trial.json').write_text(json.dumps(report,indent=2)+'\n')
    report['hashes']={k:sha(W/f'{k}-trial.glb') for k in ['brain','arteries','veins']};(W/'trial.json').write_text(json.dumps(report,indent=2)+'\n');manifest=json.loads((SRC/'candidate-manifest.json').read_text());manifest['candidateDirectory']='posterior-round58';manifest['candidateHashes']=report['hashes'];(W/'candidate-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')

if __name__=='__main__':main()
