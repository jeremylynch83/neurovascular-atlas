"""Small, bounded native wall repairs. No anatomical target is inferred."""
from collections import defaultdict
import numpy as np

def edge_table(v,f):
    u,inv=np.unique(np.asarray(v,dtype=float),axis=0,return_inverse=True);g=inv[f]
    directed=np.vstack([g[:,[0,1]],g[:,[1,2]],g[:,[2,0]]]);physical=np.sort(directed,axis=1)
    edges,first,which,count=np.unique(physical,axis=0,return_index=True,return_inverse=True,return_counts=True)
    balance=np.bincount(which,weights=np.where(directed[:,0]<directed[:,1],1,-1),minlength=len(edges))
    return u,edges,count,balance,directed[first],first

def cycles(edges):
    unused=set(map(tuple,edges));loops=[]
    while unused:
        a,b=min(unused);unused.remove((a,b));trail=[a,b]
        while True:
            if trail[-1] in trail[:-1]:
                j=trail[:-1].index(trail[-1]);loops.append(trail[j:-1]);trail=trail[:j+1]
            options=sorted(e for e in unused if e[0]==trail[-1])
            if not options:break
            a,b=options[0];unused.remove((a,b));trail.append(b)
        if len(trail)!=1:raise ValueError('Open or inconsistently directed boundary')
    return loops

def area2(a,b,c):
    ab,ac=b-a,c-a;return ab[0]*ac[1]-ab[1]*ac[0]

def triangulate(points):
    _,_,basis=np.linalg.svd(points-points.mean(0),full_matrices=False);xy=(points-points.mean(0))@basis[:2].T
    sign=np.sign(sum(area2(np.zeros(2),a,b) for a,b in zip(xy,np.roll(xy,-1,axis=0))))
    if not sign:raise ValueError('Degenerate polygon')
    rest=list(range(len(points)));out=[]
    while len(rest)>3:
        ears=[]
        for j,b in enumerate(rest):
            a,c=rest[j-1],rest[(j+1)%len(rest)]
            if sign*area2(xy[a],xy[b],xy[c])<=1e-12:continue
            if any(min(sign*area2(xy[a],xy[b],xy[k]),sign*area2(xy[b],xy[c],xy[k]),sign*area2(xy[c],xy[a],xy[k]))>=-1e-12 for k in rest if k not in [a,b,c]):continue
            ears.append((np.linalg.norm(points[a]-points[c]),j,[a,b,c]))
        if not ears:raise ValueError('Non-simple projected polygon')
        _,j,t=min(ears);out.append(t);rest.pop(j)
    out.append(rest);return np.array(out,dtype=np.uint32)

def scan_network(scene,network,limits):
    names=network['nodes'];target=network['target']
    if target not in names or len(set(names))!=len(names):raise ValueError('Invalid network selection')
    data=[scene.mesh(n) for n in names];offsets=np.r_[0,np.cumsum([len(v) for v,_ in data])]
    v=np.vstack([v for v,_ in data]);f=np.vstack([f+offsets[i] for i,(_,f) in enumerate(data)])
    u,e,count,balance,direction,first=edge_table(v,f)
    if np.any(count>2)or np.any((count==2)&(balance!=0)):raise ValueError('Network has non-manifold or inconsistent source edges')
    faceowners=np.concatenate([np.full(len(f),i) for i,(_,f) in enumerate(data)])
    edgeowners=np.tile(faceowners,3)[first]
    b=direction[count==1];owners=edgeowners[count==1];ownerbyedge={tuple(x):int(o) for x,o in zip(b,owners)}
    adjacency=defaultdict(set)
    for a,c in b:adjacency[int(a)].add(int(c));adjacency[int(c)].add(int(a))
    components=[];pending=set(adjacency)
    while pending:
        todo=[min(pending)];component=set()
        while todo:
            i=todo.pop()
            if i in component:continue
            component.add(i);pending.discard(i);todo.extend(adjacency[i]-component)
        components.append(component)
    result=[]
    for component in components:
        bd=[tuple(x) for x in b if int(x[0])in component]
        points=u[sorted(component)];span=float(np.linalg.norm(points[:,None]-points,axis=2).max()) if len(component)<=limits['maxComponentVertices'] else None
        base={'network':network['id'],'target':target,'componentVertices':len(component),'componentEdges':len(bd),'centre':points.mean(0).tolist(),'spanMm':span}
        if len(component)>limits['maxComponentVertices']:
            result.append({**base,'eligible':False,'reason':'regional-boundary-or-native-port'});continue
        if span>limits['maxComponentSpanMm']:
            result.append({**base,'eligible':False,'reason':'span-limit'});continue
        try:loops=cycles(bd)
        except ValueError as ex:result.append({**base,'eligible':False,'reason':str(ex)});continue
        for loop in loops:
            ownerids={ownerbyedge[(a,c)] for a,c in zip(loop,np.roll(loop,-1))}
            row={**base,'boundaryCoordinates':u[loop[::-1]].tolist(),'boundaryLabels':[names[i] for i in sorted(ownerids)]}
            if names.index(target)not in ownerids or len(ownerids)<2:
                result.append({**row,'eligible':False,'reason':'single-label-port-not-a-junction-gap'});continue
            polygon=u[loop[::-1]]
            try:
                if np.linalg.norm(polygon[:,None]-polygon,axis=2).max()>limits['maxSpanMm']:raise ValueError('loop-span-limit')
                triangles=triangulate(polygon);t=polygon[triangles]
                area=np.linalg.norm(np.cross(t[:,1]-t[:,0],t[:,2]-t[:,0]),axis=1)/2
                _,_,basis=np.linalg.svd(polygon-polygon.mean(0),full_matrices=False);warp=float(np.abs((polygon-polygon.mean(0))@basis[-1]).max())
                if area.min()<limits['minTriangleAreaMm2']:raise ValueError('degenerate-patch')
                if area.sum()>limits['maxPatchAreaMm2']:raise ValueError('area-limit')
                if warp>limits['maxWarpMm']:raise ValueError('planarity-limit')
                result.append({**row,'eligible':True,'reason':'small-mixed-label-wall-gap','triangles':triangles.tolist(),'areaMm2':float(area.sum()),'warpMm':warp})
            except ValueError as ex:result.append({**row,'eligible':False,'reason':str(ex)})
    return result

def patch_mesh(scene,target,proposals):
    v,f=scene.mesh(target);points=v.tolist();lookup={tuple(p):i for i,p in enumerate(points)};added=[];sources=[]
    for r in proposals:
        ids=[]
        for p in r['boundaryCoordinates']:
            key=tuple(p)
            if key not in lookup:
                lookup[key]=len(points);points.append(p)
                owners=[n for n in r['boundaryLabels']if n!=target and np.any(np.all(scene.mesh(n)[0]==p,axis=1))]
                if not owners:raise ValueError('Patch introduces a coordinate absent from declared neighbours')
                sources.append({'index':lookup[key],'coordinate':p,'normalSource':owners[0]})
            ids.append(lookup[key])
        added.extend(np.array(ids)[r['triangles']].tolist())
    return np.array(points,dtype='<f4'),np.vstack([f,added]).astype('<u4'),sources

def snap_seam(scene,spec,limits):
    """Align two explicitly paired complete rims with bounded harmonic fitting.

    Remote boundaries and every vertex shared with any other label stay fixed.
    Cases beyond the displacement bound are escalated to regional review.
    """
    from scipy.sparse import coo_matrix,diags
    from scipy.sparse.csgraph import dijkstra
    from scipy.sparse.linalg import spsolve
    child,parent=spec['target'],spec['parent'];v,f=scene.mesh(child);w,g=scene.mesh(parent)
    def rims(v,f):
        u,_,count,_,direction,_=edge_table(v,f);return u,cycles(direction[count==1])
    u,cr=rims(v,f);z,pr=rims(w,g);best=None
    for c in cr:
        for p in pr:
            if len(c)!=len(p):continue
            for seq in [p,p[::-1]]:
                for k in range(len(seq)):
                    dst=z[np.roll(seq,k)];src=u[c];dist=np.linalg.norm(src-dst,axis=1)
                    score=float(dist.max())
                    if best is None or score<best[0]:best=(score,src,dst)
    if best is None or best[0]>limits['maxSnapMm']:raise ValueError('registration-or-rim-reconstruction-required')
    _,src,dst=best
    if np.array_equal(src,dst):raise ValueError('seam-already-exact')
    u,inv=np.unique(v,axis=0,return_inverse=True);uf=inv[f];lookup={tuple(x):i for i,x in enumerate(u)};rim=np.array([lookup[tuple(x)]for x in src]);known=np.zeros_like(u,dtype=float);known[rim]=dst-src
    edges=np.unique(np.sort(np.vstack([uf[:,[0,1]],uf[:,[1,2]],uf[:,[2,0]]]),axis=1),axis=0);length=np.linalg.norm(u[edges[:,0]]-u[edges[:,1]],axis=1)
    graph=coo_matrix((np.r_[length,length],(np.r_[edges[:,0],edges[:,1]],np.r_[edges[:,1],edges[:,0]])),shape=(len(u),len(u))).tocsr();distance=dijkstra(graph,indices=rim,min_only=True)
    _,be,count,_,_,_=edge_table(u,uf);locked=set(np.unique(be[count==1]))-set(rim)
    # Protect every other label's exact existing attachment, including internal
    # shared coordinates and split-normal source vertices.
    lo=u.min(0);hi=u.max(0);positions={tuple(x):i for i,x in enumerate(u)}
    for n in scene.nearby(lo,hi):
        if n in [child,parent]:continue
        q,_=scene.mesh(n)
        for x in q[np.all(q>=lo,axis=1)&np.all(q<=hi,axis=1)]:
            i=positions.get(tuple(x))
            if i is not None:locked.add(i)
    if any(i in locked and np.any(known[i])for i in rim):raise ValueError('would-move-another-native-attachment')
    boundary=np.unique(np.r_[rim,list(locked),np.flatnonzero(distance>=limits['snapSupportMm'])]).astype(int)
    weights=1/np.maximum(length,1e-8);adj=coo_matrix((np.r_[weights,weights],(np.r_[edges[:,0],edges[:,1]],np.r_[edges[:,1],edges[:,0]])),shape=(len(u),len(u))).tocsr();lap=diags(np.asarray(adj.sum(1)).ravel())-adj
    free=np.setdiff1d(np.arange(len(u)),boundary)
    if len(free):known[free]=spsolve(lap[free][:,free],-lap[free][:,boundary]@known[boundary])
    out=(u+known).astype('<f4');out[rim]=dst;out=out[inv]
    if np.linalg.norm(out-v,axis=1).max()>limits['maxSnapMm']+1e-6:raise ValueError('displacement-limit')
    return out,np.array(f,dtype='<u4'),{'parent':parent,'sourceRimCoordinates':src.tolist(),'parentRimCoordinates':dst.tolist(),'maximumDisplacementMm':float(np.linalg.norm(out-v,axis=1).max()),'protectedOtherCoordinates':len(locked)}

def triangle_crosses_exact(a,b):
    """Exact binary-coordinate predicate for potentially intersecting triangles.

    Fraction(float) represents the supplied binary values exactly. It does
    not round a small separation to coplanarity or inflate a vertex into an
    interval. Shared vertices/edges alone are allowed; positive overlap is not.
    """
    from fractions import Fraction
    a=[[Fraction(float(x))for x in p]for p in a]
    b=[[Fraction(float(x))for x in p]for p in b]
    def sub(x,y):return [p-q for p,q in zip(x,y)]
    def cross(x,y):return [x[1]*y[2]-x[2]*y[1],x[2]*y[0]-x[0]*y[2],x[0]*y[1]-x[1]*y[0]]
    def dot(x,y):return sum(p*q for p,q in zip(x,y))
    na=cross(sub(a[1],a[0]),sub(a[2],a[0]));nb=cross(sub(b[1],b[0]),sub(b[2],b[0]))
    if not any(na)or not any(nb):return False
    da=[dot(sub(x,a[0]),na)for x in b];db=[dot(sub(x,b[0]),nb)for x in a]
    for distances in [da,db]:
        if (all(x>=0 for x in distances)or all(x<=0 for x in distances))and sum(x==0 for x in distances)<2:return False
    line=cross(na,nb)
    if not any(line):
        if any(da):return False
        axis=max(range(3),key=lambda k:abs(na[k]));aa=[[x for k,x in enumerate(p)if k!=axis]for p in a];bb=[[x for k,x in enumerate(p)if k!=axis]for p in b]
        def orient(p,q,r):return (q[0]-p[0])*(r[1]-p[1])-(q[1]-p[1])*(r[0]-p[0])
        sign=1 if orient(*bb)>0 else -1;polygon=aa
        for x,y in zip(bb,bb[1:]+bb[:1]):
            source=polygon;polygon=[]
            if not source:return False
            for p,q in zip(source,source[1:]+source[:1]):
                dp=sign*orient(x,y,p);dq=sign*orient(x,y,q)
                if dp>=0:polygon.append(p)
                if (dp>=0)!=(dq>=0):polygon.append([p[k]+(q[k]-p[k])*dp/(dp-dq)for k in range(2)])
        return len(polygon)>=3 and abs(sum(p[0]*q[1]-p[1]*q[0]for p,q in zip(polygon,polygon[1:]+polygon[:1])))>0
    axis=max(range(3),key=lambda k:abs(line[k]))
    def cut(triangle,distances):
        points=[p[axis]for p,d in zip(triangle,distances)if d==0]
        for i,j in [(0,1),(1,2),(2,0)]:
            if distances[i]*distances[j]<0:points.append(triangle[i][axis]+(triangle[j][axis]-triangle[i][axis])*distances[i]/(distances[i]-distances[j]))
        return points
    p,q=cut(a,db),cut(b,da)
    if not p or not q:return False
    low=max(min(p),min(q));high=min(max(p),max(q))
    if high<=low:return False
    shared=[p for p in a if p in b]
    if len(shared)>=2:
        interval=[p[axis]for p in shared]
        if low>=min(interval)and high<=max(interval):return False
    return True

def triangle_crosses(a,b,tol=1e-7):
    """Interior crossing or positive coplanar overlap, allowing shared edges.

    Tests adjacent triangles too: a common vertex does not excuse an overlap.
    Tangent point/edge contact is not classified as penetration. ``tol`` is
    an uncertainty threshold for the floating-point filters, not permission
    to thicken planes or discard small genuine intersections. Potential
    positive intersections are decided using exact binary coordinates.
    """
    a=np.asarray(a,dtype=float);b=np.asarray(b,dtype=float)
    if np.any(a.max(0)<b.min(0))or np.any(b.max(0)<a.min(0)):return False
    na=np.cross(a[1]-a[0],a[2]-a[0]);nb=np.cross(b[1]-b[0],b[2]-b[0]);la=np.linalg.norm(na);lb=np.linalg.norm(nb)
    if la==0 or lb==0:return False
    na/=la;nb/=lb
    da=(b-a[0])@na;db=(a-b[0])@nb
    if np.linalg.norm(np.cross(na,nb))<1e-6:return triangle_crosses_exact(a,b)
    if np.all(da>tol)or np.all(da< -tol)or np.all(db>tol)or np.all(db< -tol):return False
    shared=[x for x in a if np.any(np.all(x==b,axis=1))]
    # Distinct planes meet along the shared edge only. A single shared
    # point also cannot hide an overlap if the remaining vertices of either
    # triangle lie strictly on the same side of the other triangle's plane.
    if len(shared)>=2:return False
    if len(shared)==1:
        common=shared[0]
        for points,distances in [(b,da),(a,db)]:
            other=distances[np.any(points!=common,axis=1)]
            if np.all(other>tol)or np.all(other< -tol):return False
    if np.any(np.abs(da)<=tol)or np.any(np.abs(db)<=tol):return triangle_crosses_exact(a,b)
    line=np.cross(na,nb)
    line/=np.linalg.norm(line)
    def cut(t,d):
        pts=[x for x,z in zip(t,d)if z==0]
        for i,j in [(0,1),(1,2),(2,0)]:
            if d[i]*d[j]<0:pts.append(t[i]+(t[j]-t[i])*d[i]/(d[i]-d[j]))
        return np.array(pts)@line if pts else np.array([])
    p,q=cut(a,db),cut(b,da)
    if not len(p)or not len(q):return False
    low=max(p.min(),q.min());high=min(p.max(),q.max())
    if high<low-tol:return False
    return triangle_crosses_exact(a,b)
