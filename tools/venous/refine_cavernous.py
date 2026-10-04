"""Local v0.9.6 to v0.9.8 authoring pass in atlas RAS millimetres.

Run from the app root after decode_glb.mjs has decoded the two v0.9.6
assets into .authoring/circulation-raw.glb and .authoring/venous-original.glb.
This is a teaching reconstruction, not patient segmentation. The same smooth
coordinate field is applied to all local arterial branches and anastomoses.
Regional venous replacement preserves the delivered surface outside the box.
"""
import json, struct
from pathlib import Path
import numpy as np
import vtk
import manifold3d as mf
from scipy.spatial import cKDTree
from vtk.util.numpy_support import numpy_to_vtk, vtk_to_numpy
from reference import APP, ROOT, poly, records, arrays


def read_glb(path):
    data = path.read_bytes(); size = struct.unpack_from('<I', data, 12)[0]
    return json.loads(data[20:20+size]), bytearray(data[28+size:])


def write_glb(path, doc, data):
    j = json.dumps(doc, separators=(',', ':')).encode(); j += b' '*(-len(j) % 4)
    data = bytes(data); data += b'\0'*(-len(data) % 4)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('wb') as out:
        out.write(struct.pack('<4sII', b'glTF', 2, 28+len(j)+len(data)))
        out.write(struct.pack('<II', len(j), 0x4e4f534a)); out.write(j)
        out.write(struct.pack('<II', len(data), 0x004e4942))
        for start in range(0, len(data), 4*1024*1024): out.write(data[start:start+4*1024*1024])
    assert path.stat().st_size == 28+len(j)+len(data)


def accessor(doc, data, index):
    a = doc['accessors'][index]; view = doc['bufferViews'][a['bufferView']]
    n = {'SCALAR':1, 'VEC3':3, 'VEC4':4}[a['type']]
    dtype = {5126:'<f4',5125:'<u4',5123:'<u2',5121:'u1'}[a['componentType']]
    stride = view.get('byteStride', np.dtype(dtype).itemsize*n)
    return np.ndarray((a['count'], n), dtype=dtype, buffer=data,
                      offset=view.get('byteOffset',0)+a.get('byteOffset',0),
                      strides=(stride,np.dtype(dtype).itemsize))


def smoothstep(x):
    x = np.clip(x, 0, 1); return x*x*(3-2*x)


def move_artery(p):
    """Medialise the lower siphon, taper to zero at petrous and upper exits."""
    x,y,z = p.T; lateral = np.abs(x-.65)
    w = (smoothstep((z-47)/11)*(1-smoothstep((z-65)/11))
         *smoothstep((y+60)/9)*(1-smoothstep((y+37)/9))
         *smoothstep(lateral/10)*(1-smoothstep((lateral-22)/8)))
    out = p.copy(); out[:,0] -= np.sign(x-.65)*3*w; out[:,2] += 1.4*w
    return out


def refine_arteries(source, destination):
    doc,data = read_glb(source); changed = []; artery_parts = {}
    for node in doc['nodes']:
        if 'mesh' not in node: continue
        assert not any(k in node for k in ['matrix','translation','rotation','scale'])
        for prim in doc['meshes'][node['mesh']]['primitives']:
            pos = accessor(doc,data,prim['attributes']['POSITION']); old = pos.copy().astype(float)
            new = move_artery(old); delta = np.linalg.norm(new-old,axis=1)
            faces = accessor(doc,data,prim['indices']).reshape(-1,3).astype(np.uint32)
            if delta.max() > 1e-6:
                # Inverse-transpose Jacobian preserves shared normals and label seams.
                jac = np.empty((len(old),3,3)); h = .001
                for k in range(3):
                    step = np.zeros(3); step[k] = h
                    jac[:,:,k] = (move_artery(old+step)-move_artery(old-step))/(2*h)
                assert np.linalg.det(jac).min() > .4
                normal = accessor(doc,data,prim['attributes']['NORMAL'])
                nn = np.linalg.solve(jac.transpose(0,2,1), normal.copy()[:,:,None])[:,:,0]
                nn /= np.linalg.norm(nn,axis=1)[:,None]; normal[:] = nn
                old_fn = np.cross(old[faces[:,1]]-old[faces[:,0]],old[faces[:,2]]-old[faces[:,0]])
                new_fn = np.cross(new[faces[:,1]]-new[faces[:,0]],new[faces[:,2]]-new[faces[:,0]])
                # Existing arterial assets contain a few nearly collinear
                # triangles. Their unstable normals cannot diagnose a fold.
                edge2 = np.sum((old[faces]-old[faces[:,[1,2,0]]])**2,axis=2).max(1)
                stable = np.linalg.norm(old_fn,axis=1)>np.maximum(2e-6,edge2*.002)
                assert np.all(np.einsum('ij,ij->i',old_fn,new_fn)[stable]>0), node['name']
                pos[:] = new
                a = doc['accessors'][prim['attributes']['POSITION']]
                a.update(min=pos.min(0).tolist(),max=pos.max(0).tolist())
                changed.append({'name':node['name'],'maximum_displacement_mm':float(delta.max()),
                                'vertices_moved':int((delta>1e-6).sum())})
            if 'ICA cavernous' in node['name']: artery_parts[node['name']] = (pos.copy(),faces)
    write_glb(destination,doc,data)
    return changed, artery_parts


def whole_veins(source):
    doc,data = read_glb(source); pp=[]; ff=[]; ll=[]; ids=[]; offset=0
    for node in doc['nodes']:
        if 'mesh' not in node: continue
        prim=doc['meshes'][node['mesh']]['primitives'][0]
        p=accessor(doc,data,prim['attributes']['POSITION']).copy()
        f=accessor(doc,data,prim['indices']).reshape(-1,3).astype(np.uint32)
        ids.append(node['name']); pp.append(p);ff.append(f+offset);ll.extend([len(ids)-1]*len(f));offset+=len(p)
    pp=np.concatenate(pp);ff=np.concatenate(ff);p,inv=np.unique(pp,axis=0,return_inverse=True)
    return p,inv[ff].astype(np.uint32),np.array(ll,np.uint32),ids


def sdf_sample(pd, lo, hi, shape):
    sdf=vtk.vtkImplicitPolyDataDistance();sdf.SetInput(pd)
    sample=vtk.vtkSampleFunction();sample.SetImplicitFunction(sdf)
    sample.SetModelBounds(*np.column_stack([lo,hi]).ravel());sample.SetSampleDimensions(*shape)
    sample.ComputeNormalsOff();sample.Update()
    return vtk_to_numpy(sample.GetOutput().GetPointData().GetScalars()).reshape(tuple(shape[::-1])).copy(),sdf


def closed_artery(p,f):
    """Cap every oriented boundary cycle for an exclusion mask, not display.

    Label boundaries can touch at a vertex; vtkFillHoles cannot consistently
    separate those loops. Split the oriented boundary into simple cycles and
    cap each cycle with a consistently oriented fan before checking the closed skin.
    """
    p,inv=np.unique(p,axis=0,return_inverse=True);f=inv[f].astype(np.uint32)
    edges=np.concatenate([f[:,[0,1]],f[:,[1,2]],f[:,[2,0]]])
    _,index,count=np.unique(np.sort(edges,axis=1),axis=0,return_inverse=True,return_counts=True)
    assert count.max()==2,'Non-manifold arterial label before capping'
    boundary=edges[count[index]==1]
    outgoing={}
    for i,(a,b) in enumerate(boundary):outgoing.setdefault(int(a),[]).append(i)
    used=set();cycles=[]
    for seed,(a,b) in enumerate(boundary):
        if seed in used:continue
        start=current=int(a);walk=[current]
        while True:
            candidates=[i for i in outgoing.get(current,[]) if i not in used]
            assert candidates,'Arterial boundary must form oriented closed cycles'
            i=candidates[0];used.add(i);current=int(boundary[i,1]);walk.append(current)
            if current==start:break
        stack=[];where={}
        for vertex in walk:
            if vertex in where:
                k=where[vertex];cycle=stack[k:];assert len(cycle)>=3
                cycles.append(cycle)
                for old in stack[k+1:]:del where[old]
                stack=stack[:k+1]
            else:where[vertex]=len(stack);stack.append(vertex)
    assert len(used)==len(boundary)
    positions=[p];faces=[f]
    for j,cycle in enumerate(cycles):
        ci=len(p)+j;positions.append(p[cycle].mean(0)[None,:])
        faces.append(np.array([[cycle[(k+1)%len(cycle)],cycle[k],ci] for k in range(len(cycle))],np.uint32))
    cp=np.concatenate(positions).astype(np.float32);cf=np.concatenate(faces)
    volume=np.einsum('ij,ij->i',cp[cf[:,0]],np.cross(cp[cf[:,1]],cp[cf[:,2]])).sum()/6
    if volume<0:cf=cf[:,[0,2,1]].copy()
    assert abs(volume)>1
    normals=vtk.vtkPolyDataNormals();normals.SetInputData(poly(cp,cf))
    normals.SplittingOff();normals.ConsistencyOn();normals.AutoOrientNormalsOn();normals.Update()
    check=vtk.vtkFeatureEdges();check.SetInputConnection(normals.GetOutputPort())
    check.BoundaryEdgesOn();check.NonManifoldEdgesOn();check.FeatureEdgesOff();check.ManifoldEdgesOff();check.Update()
    assert check.GetOutput().GetNumberOfCells()==0,'Carotid exclusion mask must be closed'
    return normals.GetOutput()


def export_veins(p,f,labels,ids,dest):
    normals=np.zeros_like(p);fn=np.cross(p[f[:,1]]-p[f[:,0]],p[f[:,2]]-p[f[:,0]])
    for k in range(3):np.add.at(normals,f[:,k],fn)
    normals/=np.maximum(np.linalg.norm(normals,axis=1)[:,None],1e-12)
    np.savez_compressed(ROOT/'venous-mesh.npz',positions=p,faces=f,labels=labels,normals=normals)
    doc={'asset':{'version':'2.0','generator':'Neurovascular Atlas local cavernous authoring v0.9.8'},
         'scene':0,'scenes':[{'nodes':list(range(len(ids)))}],'nodes':[],
         'meshes':[],'accessors':[],'bufferViews':[],'buffers':[]};data=bytearray()
    def acc(a,typ,component,target,bounds=False):
        a=np.ascontiguousarray(a);raw=a.tobytes();bv=len(doc['bufferViews'])
        doc['bufferViews'].append({'buffer':0,'byteOffset':len(data),'byteLength':len(raw),'target':target})
        data.extend(raw);data.extend(b'\0'*(-len(data)%4))
        entry={'bufferView':bv,'componentType':component,'count':len(a),'type':typ}
        if bounds:entry.update(min=a.min(0).tolist(),max=a.max(0).tolist())
        doc['accessors'].append(entry);return len(doc['accessors'])-1
    stats=[]
    for i,sid in enumerate(ids):
        faces=f[labels==i];assert len(faces),sid
        used,inv=np.unique(faces,return_inverse=True)
        a=acc(p[used],'VEC3',5126,34962,True);n=acc(normals[used],'VEC3',5126,34962)
        ix=acc(inv.ravel().astype(np.uint32),'SCALAR',5125,34963)
        doc['nodes'].append({'name':sid,'mesh':i})
        doc['meshes'].append({'name':sid,'primitives':[{'attributes':{'POSITION':a,'NORMAL':n},'indices':ix}]})
        stats.append({'id':sid,'vertices':len(used),'triangles':len(faces)})
    doc['buffers']=[{'byteLength':len(data)}];write_glb(dest,doc,data)
    return stats


def refine_veins(arteries):
    p,f,labels,ids=whole_veins(APP/'.authoring/venous-original.glb')
    original=mf.Manifold(mf.Mesh(p,f,face_id=labels));assert original.status()==mf.Error.NoError
    primary={ids.index(s) for s in ['vein.cavernous.right','vein.cavernous.left',
                                  'vein.anterior_intercavernous','vein.posterior_intercavernous']}
    print('Original common venous skin',len(p),len(f),flush=True)
    # Closed regional replacement with a 2 mm overlap collar. Original mesh is
    # untouched beyond the collar; all tributaries are retained in the new field.
    cache=ROOT/'regional-replacement-v097-closed-carotid-all-veins.npz'
    if cache.exists():
        saved=np.load(cache);np_,nf,nl=saved['p'],saved['f'],saved['labels']
        lo,hi,innerlo,innerhi=[saved[k] for k in ['lo','hi','innerlo','innerhi']];step=.30
    else:
        step=.30;lo=np.array([-26.7,-59.1,43.2]);shape=np.array([184,111,133]);hi=lo+(shape-1)*step
        z,y,x=np.meshgrid(lo[2]+np.arange(shape[2])*step,lo[1]+np.arange(shape[1])*step,
                          lo[0]+np.arange(shape[0])*step,indexing='ij')
        points=np.column_stack([x.ravel(),y.ravel(),z.ravel()])
        # Only faces near the sample box can contribute its zero isosurface.
        # Retain a 7 mm margin, much greater than voxel size or fairing motion;
        # the sign close to each existing vessel wall uses its original normals.
        triangles=p[f]
        local_faces=f[np.all(triangles.max(1)>lo-7,axis=1)&np.all(triangles.min(1)<hi+7,axis=1)]
        base_cache=ROOT/'regional-original-field-v097.npz'
        if base_cache.exists():
            base=np.load(base_cache);old=base['old'];owners=base['owners']
        else:
            old,sdf=sdf_sample(poly(p,local_faces),lo,hi,shape);print('Sampled old regional skin',flush=True)
            tree=cKDTree(p[f].mean(1));_,nearest=tree.query(points,workers=-1)
            owners=labels[nearest].reshape(old.shape)
            np.savez_compressed(base_cache,old=old,owners=owners)
        innerlo=lo+2.1;innerhi=hi-2.1
        inside=((x>innerlo[0])&(x<innerhi[0])&(y>innerlo[1])&(y<innerhi[1])&(z>innerlo[2])&(z<innerhi[2]))
        field=np.where(inside&np.isin(owners,list(primary)),50.,old)
        new_owner=owners.copy()
        def softmin(a,b,k=1.2):
            h=np.maximum(k-np.abs(a-b),0)/k;return np.minimum(a,b)-h*h*k*.25
        def ellipsoid(center,radii):
            return (np.sqrt(((x-center[0])/radii[0])**2+((y-center[1])/radii[1])**2+
                            ((z-center[2])/radii[2])**2)-1)*min(radii)
        for side,sign in [('right',1),('left',-1)]:
            def c(cx,cy,cz):return [cx if sign==1 else 1.3-cx,cy,cz]
            body=softmin(ellipsoid(c(14.8,-50,57),(4.1,4.7,9)),
                         ellipsoid(c(12.9,-43.5,66),(5.2,9,7.3)))
            body=softmin(body,ellipsoid(c(12.4,-35.5,71.5),(3.8,4,4.5)))
            # Small anterolateral entry recess under the lesser wing. Keeping
            # this recess connected avoids isolating the original dural wing
            # channel when the medial parasellar body is refitted to bone.
            body=softmin(body,ellipsoid(c(17.3,-39.0,69.2),(3.0,3.6,2.8)),.8)
            mask=body<field;new_owner[mask]=ids.index('vein.cavernous.'+side);field=np.minimum(field,body)
        # Low, smooth dural cross-connections surrounding the inferred sellar space.
        for name,q,rr in [
            ('anterior_intercavernous',[[12.4,-35.5,72.4],[6,-35.5,72.5],[.65,-35.5,72.5],[-4.7,-35.5,72.5],[-11.1,-35.5,72.4]],(1.25,1.25,.72)),
            ('posterior_intercavernous',[[13,-46.5,66.5],[8,-49,67],[5,-52.4,66.4],[.65,-52.6,66.3],[-3.7,-52.4,66.4],[-6.7,-49,67],[-11.7,-46.5,66.5]],(1.1,1.1,.72))]:
            q=np.array(q);a=np.r_[0,np.cumsum(np.linalg.norm(np.diff(q,axis=0),axis=1))]
            dense=np.column_stack([np.interp(np.arange(0,a[-1]+.001,.18),a,q[:,k]) for k in range(3)])
            bridge=np.full_like(field,50.)
            for c in dense:bridge=np.minimum(bridge,ellipsoid(c,rr))
            mask=bridge<field;new_owner[mask]=ids.index('vein.'+name);field=np.minimum(field,bridge)
        # Exclude only the inferred pituitary/sellar soft-tissue space. No gland,
        # cranial nerves or invented septal compartments are added to the catalogue.
        sellar=ellipsoid([.65,-43,68.2],[7.2,6,5.7]);field=np.maximum(field,-sellar)
        # Clear both corrected ICA surfaces and the retained skull base before meshing.
        for name,(ap,af) in arteries.items():
            lower=ap.min(0)-.8;upper=ap.max(0)+.8
            local=(x>=lower[0])&(x<=upper[0])&(y>=lower[1])&(y<=upper[1])&(z>=lower[2])&(z<=upper[2])
            mask=local&(field<.8)
            signed=vtk.vtkImplicitPolyDataDistance();signed.SetInput(closed_artery(ap,af))
            cut=np.array([signed.EvaluateFunction(point) for point in points[mask.ravel()]])
            field[mask]=np.maximum(field[mask],.35-cut)
        append=vtk.vtkAppendPolyData()
        for rec in records:
            if rec['name'] in ['bone.sphenoid','bone.temporal.right','bone.temporal.left']:
                append.AddInputData(poly(*arrays(rec)))
        append.Update();signed=vtk.vtkImplicitPolyDataDistance();signed.SetInput(append.GetOutput())
        # Apply bone exclusion in replacement interior, retain the original collar.
        # Keep pre-existing emissary/other channels intact even where the skull
        # model does not resolve their foramina. The new envelope alone receives
        # this bone exclusion; it must not sever unrelated retained tributaries.
        mask=inside&np.isin(new_owner,list(primary))&(field<.8)
        bone=np.array([signed.EvaluateFunction(point) for point in points[mask.ravel()]])
        field[mask]=np.maximum(field[mask],.25-bone)
        field[[0,-1],:,:]=50;field[:,[0,-1],:]=50;field[:,:,[0,-1]]=50
        print('Built broad parasellar envelopes and clearances',flush=True)
        im=vtk.vtkImageData();im.SetDimensions(*shape);im.SetOrigin(*lo);im.SetSpacing(step,step,step)
        im.GetPointData().SetScalars(numpy_to_vtk(field.ravel(),deep=True))
        cont=vtk.vtkFlyingEdges3D();cont.SetInputData(im);cont.SetValue(0,0);cont.ComputeNormalsOff();cont.Update()
        smooth=vtk.vtkWindowedSincPolyDataFilter();smooth.SetInputConnection(cont.GetOutputPort())
        smooth.SetNumberOfIterations(12);smooth.SetPassBand(.12);smooth.NormalizeCoordinatesOn();smooth.Update()
        dec=vtk.vtkDecimatePro();dec.SetInputConnection(smooth.GetOutputPort());dec.SetTargetReduction(.65)
        dec.PreserveTopologyOn();dec.SplittingOff();dec.BoundaryVertexDeletionOff();dec.Update()
        pd=dec.GetOutput();np_=vtk_to_numpy(pd.GetPoints().GetData()).astype(np.float32)
        nf=vtk_to_numpy(pd.GetPolys().GetData()).reshape(-1,4)[:,1:].astype(np.uint32)
        cent=np_[nf].mean(1);grid=np.rint((cent-lo)/step).astype(int);grid=np.clip(grid,0,shape-1)
        nl=new_owner[grid[:,2],grid[:,1],grid[:,0]]
        np.savez_compressed(cache,p=np_,f=nf,labels=nl,lo=lo,hi=hi,innerlo=innerlo,innerhi=innerhi)
    replacement=mf.Manifold(mf.Mesh(np_.astype(np.float32),nf,face_id=nl));assert replacement.status()==mf.Error.NoError
    # FlyingEdges winds negative-inside distance fields inward. A negative
    # volume would make the Boolean union subtract the intended lumen instead.
    if replacement.volume()<0:
        nf=nf[:,[0,2,1]].copy()
        replacement=mf.Manifold(mf.Mesh(np_.astype(np.float32),nf,face_id=nl))
    assert replacement.volume()>0
    box=mf.Manifold.cube((innerhi-innerlo).tolist()).translate(innerlo.tolist())
    bm=box.to_mesh()
    box=mf.Manifold(mf.Mesh(np.array(bm.vert_properties,dtype=np.float32,copy=True,order='C'),np.array(bm.tri_verts,dtype=np.uint32,copy=True,order='C'),
                           face_id=np.full(len(bm.tri_verts),104,np.uint32)))
    final=(original-box)+replacement
    assert final.status()==mf.Error.NoError
    components=sorted(final.decompose(),key=lambda m:m.volume(),reverse=True)
    removed=[m.volume() for m in components[1:]]
    print('Components',len(components),'largest volumes',[m.volume() for m in components[:8]],flush=True)
    for index,component in enumerate(components[1:4],1):
        mesh=component.to_mesh();vertices=np.asarray(mesh.vert_properties)
        print('Fragment',index,'bounds',vertices.min(0).tolist(),vertices.max(0).tolist(),
              'labels',[(ids[int(i)] if i<len(ids) else 'cut') for i in np.unique(mesh.face_id)],flush=True)
    # Exclusion masks can leave small disconnected scraps of the newly drawn
    # envelope above the carotid/under the clinoid. Remove only local primary
    # scraps. A detached named tributary must fail rather than disappear.
    for component in components[1:]:
        cm=component.to_mesh();cp=np.asarray(cm.vert_properties)
        assert np.all((cp>=lo-.01)&(cp<=hi+.01))
        assert abs(component.volume())<.05 or set(cm.face_id).issubset(primary),set(cm.face_id)
    assert not removed or (max(map(abs,removed))<6 and sum(map(abs,removed))<15),removed[:10]
    final=components[0]
    out=final.to_mesh();p2=np.asarray(out.vert_properties)[:,:3].copy();f2=np.asarray(out.tri_verts).copy()
    l2=np.asarray(out.face_id).copy()
    # Small closure faces can remain where a thin original tributary crosses
    # the voxelised collar. Inspect and label these from the retained skin.
    cut=l2==104
    if cut.any():
        q=p2[f2[cut]].mean(1)
        distances,nearest=cKDTree(p[f].mean(1)).query(q)
        check=vtk.vtkImplicitPolyDataDistance();check.SetInput(poly(p,f))
        gaps=np.abs(np.array([check.EvaluateFunction(point) for point in q]))
        print('Collar closure',int(cut.sum()),'maximum original-skin gap',float(gaps.max()),flush=True)
        for j in np.argsort(gaps)[-8:]:
            print('Closure gap',float(gaps[j]),q[j].tolist(),ids[int(labels[nearest[j]])],flush=True)
        assert gaps.max()<.65,'Regional collar closure departs from retained skin'
        l2[cut]=labels[nearest]
    assert set(l2)==set(range(104)),set(l2)
    stats=export_veins(p2,f2,l2,ids,ROOT/'venous-raw.glb')
    print('Exported local replacement',len(p2),len(f2),flush=True)
    exterior=(p[:,0]<lo[0]+.3)|(p[:,0]>hi[0]-.3)|(p[:,1]<lo[1]+.3)|(p[:,1]>hi[1]-.3)|(p[:,2]<lo[2]+.3)|(p[:,2]>hi[2]-.3)
    distances=cKDTree(p2).query(p[exterior])[0]
    assert distances.max()<1e-5
    return dict(vertices=len(p2),triangles=len(f2),parts=stats,
                connected_components=1,exterior_vertices_preserved=int(exterior.sum()),
                maximum_exterior_vertex_difference_mm=float(distances.max()),
                replacement_bounds_mm=[lo.tolist(),hi.tolist()],authoring_grid_mm=step,
                collar_closure_faces=int(cut.sum()),
                maximum_collar_closure_distance_from_original_skin_mm=float(gaps.max()) if cut.any() else 0.,
                isolated_regional_envelope_scraps_removed=len(removed),removed_volume_mm3=sum(map(abs,removed)))


if __name__=='__main__':
    changed,arteries=refine_arteries(APP/'.authoring/circulation-raw.glb',APP/'.authoring/circulation-refined.glb')
    # Optional anastomotic geometry receives exactly the same coordinate field.
    anast=APP/'.authoring/anastomoses-raw.glb'
    changed_anast=[]
    if anast.exists():changed_anast,_=refine_arteries(anast,APP/'.authoring/anastomoses-refined.glb')
    report=refine_veins(arteries)
    report.update(release='0.9.8',arterial_parts_changed=changed,anastomotic_parts_changed=changed_anast,
                  method='Local continuous arterial deformation and regional venous replacement; teaching reconstruction, not patient imaging')
    (ROOT/'cavernous-local-build.json').write_text(json.dumps(report,indent=2)+'\n')
