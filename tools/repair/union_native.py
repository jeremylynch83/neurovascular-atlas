"""Exterior union of two native wall labels, retaining remote open ports."""
import numpy as np
from geometry import edge_table,cycles

def closed_input(v,f):
    u,inv=np.unique(np.asarray(v,dtype=float),axis=0,return_inverse=True);g=inv[f];_,_,c,b,d,_=edge_table(u,g)
    if np.any(c>2)or np.any((c==2)&(b!=0)):raise ValueError('Non-manifold union input')
    loops=cycles(d[c==1]);vertices=u.tolist();faces=g.tolist()
    for loop in loops:
        centre=len(vertices);vertices.append(u[loop].mean(0).tolist())
        for a,b in zip(loop,np.roll(loop,-1)):faces.append([centre,int(b),int(a)])
    p=np.array(vertices);h=np.array(faces,dtype=np.uint64);t=p[h];volume=np.einsum('ij,ij->i',t[:,0],np.cross(t[:,1],t[:,2])).sum()/6
    if volume<=0:raise ValueError('Non-positive union input volume')
    return p,h,len(g)

def exterior_union(parts,junction_centre,local_cap_radius=1.):
    import manifold3d as m
    names=list(parts);inputs=[closed_input(*parts[n])for n in names];first=m.Manifold.reserve_ids(len(names));solids=[]
    for i,(v,f,_)in enumerate(inputs):
        solid=m.Manifold(m.Mesh64(vert_properties=np.ascontiguousarray(v,np.float64),tri_verts=np.ascontiguousarray(f,np.uint64),run_index=np.array([0,3*len(f)],np.uint64),run_original_id=np.array([first+i],np.uint32),face_id=np.arange(len(f),dtype=np.uint64)))
        if solid.status()!=m.Error.NoError:raise ValueError('Invalid closed union input '+str(solid.status()))
        solids.append(solid)
    union=solids[0]+solids[1]
    if union.status()!=m.Error.NoError:raise ValueError('Union failed '+str(union.status()))
    mesh=union.to_mesh64();v=np.asarray(mesh.vert_properties)[:,:3];f=np.asarray(mesh.tri_verts);runs=np.asarray(mesh.run_index)//3;origins=np.asarray(mesh.run_original_id);face_ids=np.asarray(mesh.face_id);result={};reports=[]
    for i,n in enumerate(names):
        selected=np.zeros(len(f),bool);retained_caps=0
        for k,origin in enumerate(origins):
            if origin!=first+i:continue
            sl=slice(runs[k],runs[k+1]);native=face_ids[sl]<inputs[i][2];local=np.linalg.norm(v[f[sl]].mean(1)-junction_centre,axis=1)<local_cap_radius;selected[sl]=native|local;retained_caps+=int(np.sum(~native&local))
        g=f[selected];used=np.unique(g);lookup=np.full(len(v),-1);lookup[used]=np.arange(len(used));p=v[used].astype('<f4');g=lookup[g].astype('<u4');t=p[g].astype(float);good=np.linalg.norm(np.cross(t[:,1]-t[:,0],t[:,2]-t[:,0]),axis=1)>1e-10;g=g[good]
        result[n]=(p,g);reports.append({'node':n,'retainedExteriorJunctionCapTriangles':retained_caps,'discardedFloat32Degenerates':int(sum(~good)),'vertices':len(p),'triangles':len(g)})
    return result,reports
