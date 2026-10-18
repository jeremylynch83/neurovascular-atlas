"""Construct a bounded native collar after reopening a closed proximal cap.

Explicit cut planes and parent rims are authoring inputs. Nothing is installed.
"""
import numpy as np
from scipy.spatial.transform import Rotation
from geometry import edge_table,cycles

def clip_keep(v,f,origin,normal):
    import vtk
    from vtk.util.numpy_support import numpy_to_vtk,numpy_to_vtkIdTypeArray,vtk_to_numpy
    data=vtk.vtkPolyData();pts=vtk.vtkPoints();pts.SetData(numpy_to_vtk(np.asarray(v,dtype=float),deep=True));data.SetPoints(pts);cells=vtk.vtkCellArray();cells.SetCells(len(f),numpy_to_vtkIdTypeArray(np.c_[np.full(len(f),3),f].astype(np.int64).ravel(),deep=True));data.SetPolys(cells)
    plane=vtk.vtkPlane();plane.SetOrigin(origin);plane.SetNormal(normal);clip=vtk.vtkClipPolyData();clip.SetInputData(data);clip.SetClipFunction(plane);clip.Update();out=clip.GetOutput()
    p=vtk_to_numpy(out.GetPoints().GetData()).astype('<f4').astype(float);g=vtk_to_numpy(out.GetPolys().GetData()).reshape(-1,4)[:,1:].astype('<u4')
    # Float32 conversion can collapse intersections exactly onto source vertices.
    p,inv=np.unique(p,axis=0,return_inverse=True);g=inv[g];t=p[g]
    good=np.linalg.norm(np.cross(t[:,1]-t[:,0],t[:,2]-t[:,0]),axis=1)>1e-10;g=g[good]
    used=np.unique(g);remap=np.full(len(p),-1);remap[used]=np.arange(len(used))
    return p[used],remap[g].astype('<u4')

def build_collar(v,f,w,g,port_centre,cut_origin,cut_normal,steps=12):
    cut_normal=np.asarray(cut_normal,dtype=float);cut_normal/=np.linalg.norm(cut_normal)
    p,h=clip_keep(v,f,cut_origin,cut_normal);u,e,count,balance,directed,_=edge_table(p,h);loops=cycles(directed[count==1]);src=min(loops,key=lambda x:abs(np.dot(u[x].mean(0)-cut_origin,cut_normal)));a=u[src]
    # Map the welded physical cut rim back to retained raw source indices.
    lookup={tuple(x):i for i,x in enumerate(p)};source=np.array([lookup[tuple(x)]for x in a]);zz,ee,cc,bb,dd,_=edge_table(w,g);rings=cycles(dd[cc==1]);dst0=min(rings,key=lambda x:np.linalg.norm(zz[x].mean(0)-port_centre))[::-1];parent_lookup={tuple(x):i for i,x in enumerate(w)}
    def normal(q):
        x=q-q.mean(0);n=np.cross(x,np.roll(x,-1,axis=0)).sum(0);return n/np.linalg.norm(n)
    c0=a.mean(0);c1=zz[dst0].mean(0);n0=normal(a);n1=normal(zz[dst0]);length=np.linalg.norm(c1-c0);t0=-n0*length;t1=-n1*length;ts=np.linspace(0,1,steps);centres=[];frames=[];previous=n0;rotation=Rotation.identity()
    for t in ts:
        c=(2*t**3-3*t*t+1)*c0+(t**3-2*t*t+t)*t0+(-2*t**3+3*t*t)*c1+(t**3-t*t)*t1;der=(6*t*t-6*t)*c0+(3*t*t-4*t+1)*t0+(-6*t*t+6*t)*c1+(3*t*t-2*t)*t1;n=-der/np.linalg.norm(der);axis=np.cross(previous,n);s=np.linalg.norm(axis);co=np.dot(previous,n)
        if s>1e-12:rotation=Rotation.from_rotvec(axis/s*np.arctan2(s,co))*rotation
        elif co<0:raise ValueError('Collar reverses tangent')
        centres.append(c);frames.append(rotation);previous=n
    ka=np.r_[0,np.cumsum(np.linalg.norm(np.roll(a,-1,axis=0)-a,axis=1))];ka/=ka[-1];best=None
    for shift in range(len(dst0)):
        dst=np.roll(dst0,shift);b=zz[dst];kb=np.r_[0,np.cumsum(np.linalg.norm(np.roll(b,-1,axis=0)-b,axis=1))];kb/=kb[-1];local=frames[-1].inv().apply(b-c1);sample=np.column_stack([np.interp(ka[:-1],kb,np.r_[local[:,k],local[0,k]])for k in range(3)]);error=np.sum((a-c0-sample)**2)
        if best is None or error<best[0]:best=(error,dst,kb)
    _,dst,kb=best;params=kb[:-1];shape=np.column_stack([np.interp(params,ka,np.r_[a[:,k]-c0[k],a[0,k]-c0[k]])for k in range(3)]);target=frames[-1].inv().apply(zz[dst]-c1);rr=[source];pp=[ka[:-1]];vertices=p.copy();faces=h.tolist()
    for i,t in enumerate(ts[1:-1],1):
        ring=centres[i]+frames[i].apply((1-t)*shape+t*target);idx=np.arange(len(vertices),len(vertices)+len(ring));vertices=np.vstack([vertices,ring]);rr.append(idx);pp.append(params)
    endpoint=np.arange(len(vertices),len(vertices)+len(dst));vertices=np.vstack([vertices,zz[dst]]);rr.append(endpoint);pp.append(params)
    for r,s,ra,sa in zip(rr[:-1],rr[1:],pp[:-1],pp[1:]):
        i=j=0
        while i<len(r)or j<len(s):
            an=ra[i+1]if i+1<len(r)else 1.;bn=sa[j+1]if j+1<len(s)else 1.
            if i<len(r)and(j==len(s)or an<=bn):faces.append([int(r[i%len(r)]),int(s[j%len(s)]),int(r[(i+1)%len(r)])]);i+=1
            else:faces.append([int(r[i%len(r)]),int(s[j%len(s)]),int(s[(j+1)%len(s)])]);j+=1
    return vertices.astype('<f4'),np.array(faces,dtype='<u4'),{'cutOrigin':np.asarray(cut_origin).tolist(),'cutNormal':cut_normal.tolist(),'cutRingVertices':len(source),'parentRim':[parent_lookup[tuple(x)]for x in zz[dst]],'candidateRim':endpoint.tolist(),'retainedClippedTriangles':len(h),'collarTriangles':len(faces)-len(h),'centreline':np.asarray(centres).tolist(),'endpointSeparationMm':float(length),'steps':steps}
