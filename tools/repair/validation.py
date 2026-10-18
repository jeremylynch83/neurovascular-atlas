"""Incremental checks for append-only patches and bounded seam alignment."""
import numpy as np
from geometry import edge_table,triangle_crosses

def affected(v,f,p,g):
    if len(p)<len(v)or len(g)<len(f)or not np.array_equal(g[:len(f)],f):raise ValueError('Unsupported topology change: use regional reconstruction')
    moved=np.flatnonzero(np.any(v!=p[:len(v)],axis=1))
    ids=np.r_[np.flatnonzero(np.any(np.isin(f,moved),axis=1)),np.arange(len(f),len(g))].astype(int)
    return ids,moved

def ray_inside(scene,name,point):
    v,f=scene.mesh(name);bounds=scene.rows[name]['bounds'];extent=np.linalg.norm(np.array(bounds[1])-bounds[0]);results=[]
    for direction in [[1,.371,.173],[.217,1,.419],[.137,.293,1]]:
        d=np.array(direction,dtype=float);d/=np.linalg.norm(d);end=point+d*(extent+np.linalg.norm(point-np.mean(bounds,axis=0))+1)*4
        ids=scene.bvh(name).query(np.minimum(point,end)-1e-9,np.maximum(point,end)+1e-9)
        t=np.asarray(v[f[ids]],dtype=float);e1=t[:,1]-t[:,0];e2=t[:,2]-t[:,0];h=np.cross(d,e2);det=np.einsum('ij,ij->i',e1,h);ok=np.abs(det)>1e-12
        safe=np.where(ok,det,1);s=point-t[:,0];u=np.einsum('ij,ij->i',s,h)/safe;q=np.cross(s,e1);bary=q@d/safe;dist=np.einsum('ij,ij->i',e2,q)/safe
        hit=ok&(u>=-1e-10)&(bary>=-1e-10)&(u+bary<=1+1e-10)&(dist>1e-7)
        if np.any(hit&((u<1e-9)|(bary<1e-9)|(u+bary>1-1e-9))):continue
        depths=np.sort(dist[hit]);n=int(len(depths)) if not len(depths)else 1+int(np.sum(np.diff(depths)>1e-7))
        results.append(bool(n%2))
    if not results or len(set(results))>1:return None
    return results[0]

def validate(scene,candidates,networks,limits):
    ids={};changes=[];problems=[]
    for name,(p,g) in candidates.items():
        v,f=scene.mesh(name)
        if not np.isfinite(p).all()or not len(g)or g.min()<0 or g.max()>=len(p):raise ValueError('Invalid candidate arrays')
        selected,moved=affected(v,f,p,g);ids[name]=selected
        t=np.asarray(p[g[selected]],dtype=float);cross=np.cross(t[:,1]-t[:,0],t[:,2]-t[:,0]);area=np.linalg.norm(cross,axis=1)/2
        if np.any(area<limits['minTriangleAreaMm2']):problems.append({'node':name,'reason':'degenerate-triangle'})
        existing=selected[selected<len(f)]
        if len(existing):
            old=np.asarray(v[f[existing]],dtype=float);new=np.asarray(p[g[existing]],dtype=float)
            if np.any(np.einsum('ij,ij->i',np.cross(old[:,1]-old[:,0],old[:,2]-old[:,0]),np.cross(new[:,1]-new[:,0],new[:,2]-new[:,0]))<=0):problems.append({'node':name,'reason':'reversed-face'})
        changes.append({'node':name,'sourceVertices':len(v),'sourceTriangles':len(f),'addedVertices':len(p)-len(v),'addedTriangles':len(g)-len(f),'movedVertices':len(moved),'affectedTriangles':len(selected),'maximumDisplacementMm':float(np.linalg.norm(p[:len(v)]-v,axis=1).max())})
    pair_checks=0;crossings=[];containment=[]
    for name,(p,g) in candidates.items():
        for i in ids[name]:
            a=np.asarray(p[g[i]],dtype=float);lo=a.min(0)-1e-7;hi=a.max(0)+1e-7
            for other in sorted(set(scene.nearby(lo,hi))|set(candidates)):
                w,h=candidates.get(other,scene.mesh(other));near=scene.bvh(other).query(lo,hi)
                if other in candidates:near=np.unique(np.r_[near,ids[other]])
                for j in near:
                    if other==name and i==j:continue
                    b=np.asarray(w[h[j]],dtype=float)
                    if np.any(b.max(0)<lo)or np.any(b.min(0)>hi):continue
                    pair_checks+=1
                    if triangle_crosses(a,b):crossings.append({'node':name,'face':int(i),'other':other,'otherFace':int(j)})
        ts=np.asarray(p[g[ids[name]]],dtype=float)
        samples=np.unique(np.vstack([ts.reshape(-1,3),ts.mean(1),((ts+np.roll(ts,-1,axis=1))/2).reshape(-1,3)]),axis=0)
        if not len(samples):continue
        for other in scene.nearby(samples.min(0),samples.max(0)):
            system=scene.systems[other]
            if system not in ['bone','brain']or any(x in other for x in ['.falx-','.tentorium-','.petroclinoid-']):continue
            if hasattr(scene,'volume_topology'):topology=scene.volume_topology(other)
            else:
                _,_,c,b,_,_=edge_table(*scene.mesh(other));topology={'closedOrientedManifold':bool(np.all(c==2)and np.all(b==0))}
            if not topology['closedOrientedManifold']:
                # Do not treat ray parity on an open source mesh as proof of
                # containment. An unchanged source anchor and an empty ball
                # containing the entire changed face prove local separation.
                safe=True;minimum_margin=float('inf');v,f=scene.mesh(name);w,h=scene.mesh(other)
                for i in ids[name]:
                    tri=np.asarray(p[g[i]],dtype=float);anchor=np.asarray(v[f[i,0]]if i<len(f)else tri[0],dtype=float)
                    radius=float(np.linalg.norm(tri-anchor,axis=1).max());distance=scene.bvh(other).nearest(anchor,w,h);minimum_margin=min(minimum_margin,distance-radius)
                    if distance<=radius+1e-6:safe=False
                containment.append({'node':name,'target':other,'targetTopology':topology,'method':'source-anchor-empty-ball','minimumClearanceMarginMm':minimum_margin,'passed':safe,'absoluteVolumeMembershipCertified':False})
                if not safe:problems.append({'node':name,'other':other,'reason':'open-target-near-edit-requires-regional-review'})
                continue
            outcomes=[ray_inside(scene,other,x) for x in samples]
            inside=sum(x is True for x in outcomes);uncertain=sum(x is None for x in outcomes)
            containment.append({'node':name,'target':other,'targetTopology':topology,'method':'three-ray-parity','insideSamples':inside,'ambiguousSamples':uncertain,'samples':len(samples)})
            if inside or uncertain:problems.append({'node':name,'other':other,'reason':'tissue-or-bone-entry-requires-regional-review','insideSamples':inside,'ambiguousSamples':uncertain})
    for network in networks:
        before=[];after=[];offset=0;new_offset=0
        for name in network['nodes']:
            v,f=scene.mesh(name);p,g=candidates.get(name,(v,f));before.append((v,f+offset));after.append((p,g+new_offset));offset+=len(v);new_offset+=len(p)
        def stats(data):
            _,_,count,balance,_,_=edge_table(np.vstack([v for v,_ in data]),np.vstack([f for _,f in data]))
            return {'boundaryEdges':int(sum(count==1)),'nonManifoldEdges':int(sum(count>2)),'misorientedEdges':int(sum((count==2)&(balance!=0)))}
        old,new=stats(before),stats(after)
        if new['nonManifoldEdges']>old['nonManifoldEdges']or new['misorientedEdges']>old['misorientedEdges']or new['boundaryEdges']>=old['boundaryEdges']:problems.append({'network':network['id'],'reason':'native-boundary-regression-or-no-closure','before':old,'after':new})
        for row in changes:
            if row['node']==network['target']:row.setdefault('networks',[]).append({'id':network['id'],'before':old,'after':new})
    if crossings:problems.append({'reason':'changed-face-crossing','count':len(crossings)})
    return {'passed':not problems,'changes':changes,'trianglePairsChecked':pair_checks,'crossings':crossings,'containment':containment,'problems':problems,'scope':'All affected faces against the entire scene, including adjacent faces and coplanar overlap. Unchanged remote defects are retained. Tissue/bone ray samples are a local regression gate, not anatomical approval.'}
