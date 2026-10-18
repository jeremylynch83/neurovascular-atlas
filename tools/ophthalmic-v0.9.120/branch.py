"""Native-rim loft with an explicitly authored regional centreline."""
import numpy as np
from scipy.interpolate import CubicSpline
from scipy.spatial.transform import Rotation

def rim_normal(p):
    q=p-p.mean(0);n=np.cross(q,np.roll(q,-1,axis=0)).sum(0);length=np.linalg.norm(n)
    if len(p)<3 or length<1e-10:raise ValueError('Native rim has zero area')
    return n/length

def bridge(a,b,via=(),steps=32):
    """a follows a retained wall's boundary; b opposes the destination wall."""
    a=np.asarray(a,float);b=np.asarray(b,float);c0=a.mean(0);c1=b.mean(0);n0=rim_normal(a);n1=rim_normal(b);knots=np.vstack([c0,*via,c1]);arc=np.r_[0,np.cumsum(np.linalg.norm(np.diff(knots,axis=0),axis=1))];spline=CubicSpline(arc,knots,bc_type=((1,-n0),(1,-n1)));tt=np.linspace(0,arc[-1],steps);centres=spline(tt);frames=[];rotation=Rotation.identity();previous=n0
    for i,t in enumerate(tt):
        remaining=arc[-1]-t
        if 0<remaining<3:centres[i]+=n1*.4*np.sin(np.pi*remaining/3)
        tangent=-spline(t,1);tangent/=np.linalg.norm(tangent);axis=np.cross(previous,tangent);ss=np.linalg.norm(axis);cc=np.dot(previous,tangent)
        if ss>1e-12:rotation=Rotation.from_rotvec(axis/ss*np.arctan2(ss,cc))*rotation
        elif cc<0:raise ValueError('Regional loft reverses its frame')
        frames.append(rotation);previous=tangent
    ka=np.r_[0,np.cumsum(np.linalg.norm(np.roll(a,-1,axis=0)-a,axis=1))];ka/=ka[-1];best=None
    for k in range(len(b)):
        target=np.roll(b,k,axis=0);kb=np.r_[0,np.cumsum(np.linalg.norm(np.roll(target,-1,axis=0)-target,axis=1))];kb/=kb[-1];local=frames[-1].inv().apply(target-c1);sample=np.column_stack([np.interp(ka[:-1],kb,np.r_[local[:,j],local[0,j]])for j in range(3)]);score=float(np.square(a-c0-sample).sum())
        if best is None or score<best[0]:best=(score,target,kb)
    _,target,kb=best;params=kb[:-1];shape=np.column_stack([np.interp(params,ka,np.r_[a[:,j]-c0[j],a[0,j]-c0[j]])for j in range(3)]);last=frames[-1].inv().apply(target-c1);vertices=a.tolist();rings=[np.arange(len(a))];perimeters=[ka[:-1]]
    for i,t in enumerate(tt[1:-1],1):
        def fade(x):
            x=np.clip(x,0,1);return x*x*(3-2*x)
        radial=a[0]-c0;radial-=n0*np.dot(radial,n0);radial/=np.linalg.norm(radial);second=np.cross(n0,radial)
        circle=.60*(np.cos(params*2*np.pi)[:,None]*radial+np.sin(params*2*np.pi)[:,None]*second)
        wa=1-fade(t/2.5);wb=1-fade((arc[-1]-t)/2.5)
        ring=centres[i]+frames[i].apply(wa*shape+wb*last+(1-wa-wb)*circle);idx=np.arange(len(vertices),len(vertices)+len(ring));vertices.extend(ring.tolist());rings.append(idx);perimeters.append(params)
    end=np.arange(len(vertices),len(vertices)+len(target));vertices.extend(target.tolist());rings.append(end);perimeters.append(params);faces=[]
    for r,s,ra,sa in zip(rings[:-1],rings[1:],perimeters[:-1],perimeters[1:]):
        i=j=0
        while i<len(r)or j<len(s):
            an=ra[i+1]if i+1<len(r)else 1.;bn=sa[j+1]if j+1<len(s)else 1.
            if i<len(r)and(j==len(s)or an<=bn):faces.append([int(r[i%len(r)]),int(s[j%len(s)]),int(r[(i+1)%len(r)])]);i+=1
            else:faces.append([int(r[i%len(r)]),int(s[j%len(s)]),int(s[(j+1)%len(s)])]);j+=1
    return np.array(vertices,dtype='<f4'),np.array(faces,dtype='<u4'),{'centreline':centres.tolist(),'via':np.asarray(via).tolist(),'steps':steps,'firstRimVertices':len(a),'lastRimVertices':len(b)}

def combine(parts):
    vv=[];ff=[];offset=0
    for v,f in parts:vv.append(v);ff.append(f+offset);offset+=len(v)
    p=np.vstack(vv);g=np.vstack(ff);u,inv=np.unique(p,axis=0,return_inverse=True);g=inv[g];t=u[g].astype(float)
    good=np.linalg.norm(np.cross(t[:,1]-t[:,0],t[:,2]-t[:,0]),axis=1)>1e-10;g=g[good]
    used=np.unique(g);remap=np.full(len(u),-1);remap[used]=np.arange(len(used))
    return u[used].astype('<f4'),remap[g].astype('<u4')
