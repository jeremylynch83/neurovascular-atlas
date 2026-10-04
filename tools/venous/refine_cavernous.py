"""Local cavernous v0.9.12 authoring pass in atlas RAS millimetres.

Run from the app root with the original venous skin, retained v0.9.7 corrected
arteries and bone reference extraction available in .authoring. This release
retains the corrected arteries. The historical arterial deformation functions
remain for verification. Regional venous replacement preserves the delivered
surface outside the box. This is a teaching reconstruction, not segmentation.
"""
import json, struct, io, os
from pathlib import Path
import numpy as np
import vtk
import manifold3d as mf
from scipy.spatial import cKDTree
from scipy.interpolate import CubicSpline
from vtk.util.numpy_support import numpy_to_vtk, vtk_to_numpy
from reference import APP, ROOT, poly, records, arrays


def atomic_npz(path,**arrays):
    buffer=io.BytesIO();np.savez_compressed(buffer,**arrays)
    data=buffer.getvalue();temp=path.with_suffix('.tmp')
    with temp.open('wb') as out:
        for start in range(0,len(data),1048576):out.write(data[start:start+1048576])
        out.flush();os.fsync(out.fileno())
    temp.replace(path)
    with np.load(path) as check:
        for key in check.files:assert check[key].shape==arrays[key].shape


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


def retained_ica_courses():
    """Actual contiguous ICA skin through both cavernous label exits."""
    doc,data=read_glb(APP/'.authoring/circulation-refined.glb');result={}
    for side in ['right','left']:
        pp=[];ff=[];offset=0
        for node in doc['nodes']:
            if node['name'] not in [f'ICA {label} {side}' for label in ['petrous','cavernous','paraophthalmic']]:continue
            q=doc['meshes'][node['mesh']]['primitives'][0]
            p=accessor(doc,data,q['attributes']['POSITION']).copy()
            f=accessor(doc,data,q['indices']).reshape(-1,3).copy()
            pp.append(p);ff.append(f+offset);offset+=len(p)
        p=np.concatenate(pp);f=np.concatenate(ff);p,inv=np.unique(p,axis=0,return_inverse=True)
        result[side]=(p,inv[f].astype(np.uint32))
    return result


def export_veins(p,f,labels,ids,dest):
    normals=np.zeros_like(p);fn=np.cross(p[f[:,1]]-p[f[:,0]],p[f[:,2]]-p[f[:,0]])
    for k in range(3):np.add.at(normals,f[:,k],fn)
    normals/=np.maximum(np.linalg.norm(normals,axis=1)[:,None],1e-12)
    atomic_npz(ROOT/'venous-mesh.npz',positions=p,faces=f,labels=labels,normals=normals)
    doc={'asset':{'version':'2.0','generator':'Neurovascular Atlas local cavernous authoring v0.9.12'},
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
    cache=ROOT/'regional-replacement-v0912-ica-bone-g.npz'
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
            atomic_npz(base_cache,old=old,owners=owners)
        innerlo=lo+2.1;innerhi=hi-2.1
        inside=((x>innerlo[0])&(x<innerhi[0])&(y>innerlo[1])&(y<innerhi[1])&(z>innerlo[2])&(z<innerhi[2]))
        junction_ids={ids.index('vein.'+name+'.'+side)
                      for name in ['sphenoparietal','superficial_middle_cerebral','superior_ophthalmic','ovale_emissary','superior_petrosal','inferior_petrosal']
                      for side in ['right','left']}
        replace=inside&np.isin(owners,list(primary|junction_ids))
        field=np.where(replace,50.,old)
        new_owner=owners.copy()
        def softmin(a,b,k=1.2):
            h=np.maximum(k-np.abs(a-b),0)/k;return np.minimum(a,b)-h*h*k*.25
        def ellipsoid(center,radii):
            return (np.sqrt(((x-center[0])/radii[0])**2+((y-center[1])/radii[1])**2+
                            ((z-center[2])/radii[2])**2)-1)*min(radii)
        def softmax(a,b,k=.8):return -softmin(-a,-b,k)
        append=vtk.vtkAppendPolyData()
        for rec in records:
            if rec['name'] in ['bone.sphenoid','bone.temporal.right','bone.temporal.left']:
                append.AddInputData(poly(*arrays(rec)))
        append.Update();bone_sdf=vtk.vtkImplicitPolyDataDistance();bone_sdf.SetInput(append.GetOutput())
        rebuilt_entry=np.zeros_like(field,dtype=bool)
        junction_paths=[]
        artery_fields={}
        # Fit the receiving envelope to the actual retained cavernous ICA skin.
        # Cache its closed-mask distance on this authoring grid for iterations.
        for name,(ap,af) in arteries.items():
            side=name.split()[-1]
            acache=ROOT/('artery-distance-v097-enclosed-'+side+'.npz')
            if acache.exists():cut=np.load(acache)['distance']
            else:
                closed=closed_artery(ap,af)
                # Closest-normal signed distances can misclassify exterior
                # points beside a nonplanar temporary cap. Obtain occupancy
                # independently with ray-based enclosed-point classification.
                old_cache=ROOT/('artery-distance-v097-'+side+'.npz')
                if old_cache.exists():cut=np.load(old_cache)['distance']
                else:cut,_=sdf_sample(closed,lo,hi,shape)
                cloud=vtk.vtkPolyData();cloud_points=vtk.vtkPoints()
                cloud_points.SetData(numpy_to_vtk(points,deep=True));cloud.SetPoints(cloud_points)
                enclosed=vtk.vtkSelectEnclosedPoints();enclosed.SetInputData(cloud)
                enclosed.SetSurfaceData(closed);enclosed.SetTolerance(1e-6)
                enclosed.CheckSurfaceOn();enclosed.Update()
                membership=vtk_to_numpy(enclosed.GetOutput().GetPointData().GetArray('SelectedPoints')).reshape(cut.shape).astype(bool)
                cut=np.where(membership,-np.abs(cut),np.abs(cut))
                atomic_npz(acache,distance=cut)
                print('Cached robust ICA occupancy',side,flush=True)
            artery_fields[side]=cut
        bone_locator=vtk.vtkStaticCellLocator();bone_locator.SetDataSet(append.GetOutput());bone_locator.BuildLocator()
        apposition_seeds=[]
        def capsule(a,b,radius):
            a=np.array(a);b=np.array(b);v=b-a;vv=np.dot(v,v)
            low=np.maximum(np.floor((np.minimum(a,b)-radius-.7-lo)/step).astype(int),0)
            high=np.minimum(np.ceil((np.maximum(a,b)+radius+.7-lo)/step).astype(int)+1,shape)
            sl=np.s_[low[2]:high[2],low[1]:high[1],low[0]:high[0]]
            dx=x[sl]-a[0];dy=y[sl]-a[1];dz=z[sl]-a[2]
            t=np.clip((dx*v[0]+dy*v[1]+dz*v[2])/max(vv,1e-9),0,1)
            distance=np.sqrt((dx-t*v[0])**2+(dy-t*v[1])**2+(dz-t*v[2])**2)-radius
            return sl,distance

        def branch_field(q,width,depth):
            q=np.array(q,dtype=float)
            # Move newly drawn centres away from the resolved bony surface.
            # The first port is measured on the retained vein and kept fixed.
            for j in range(1,len(q)):
                for _ in range(4):
                    gap=bone_sdf.EvaluateFunction(q[j]);target=depth+.3
                    if gap>=target:break
                    grad=np.empty(3)
                    for axis in range(3):
                        delta=np.zeros(3);delta[axis]=.03
                        grad[axis]=(bone_sdf.EvaluateFunction(q[j]+delta)-bone_sdf.EvaluateFunction(q[j]-delta))/.06
                    grad/=max(np.linalg.norm(grad),1e-9)
                    q[j]+=grad*min(target-gap,1.5)
            arc=np.r_[0,np.cumsum(np.linalg.norm(np.diff(q,axis=0),axis=1))]
            curve=CubicSpline(arc,q,axis=0);stations=np.arange(0,arc[-1]+.001,.15)
            centres=curve(stations);tangents=curve(stations,1)
            branch=np.full_like(field,50.)
            for point,tangent,station in zip(centres,tangents,stations):
                tangent/=np.linalg.norm(tangent)
                normal=np.array([0,.85,.5]);normal-=tangent*np.dot(normal,tangent)
                normal/=max(np.linalg.norm(normal),1e-9);wide=np.cross(tangent,normal)
                taper=1-.15*smoothstep(station/arc[-1]);radii=np.array([.65,width*taper,depth*taper])
                radius=max(radii)+.7
                low=np.maximum(np.floor((point-radius-lo)/step).astype(int),0)
                high=np.minimum(np.ceil((point+radius-lo)/step).astype(int)+1,shape)
                sl=np.s_[low[2]:high[2],low[1]:high[1],low[0]:high[0]]
                dx=x[sl]-point[0];dy=y[sl]-point[1];dz=z[sl]-point[2]
                def project(v):return dx*v[0]+dy*v[1]+dz*v[2]
                distance=(np.sqrt((project(tangent)/radii[0])**2+
                                  (project(wide)/radii[1])**2+(project(normal)/radii[2])**2)-1)*min(radii)
                branch[sl]=np.minimum(branch[sl],distance)
            return branch,centres
        for side,sign in [('right',1),('left',-1)]:
            def c(cx,cy,cz):return [cx if sign==1 else 1.3-cx,cy,cz]
            # Thin curved lens, with a tapered oval perimeter and a gently
            # indented roof. No planar side, anterior or posterior walls.
            lateral=x if sign==1 else 1.3-x
            centre_x=14.4-.26*(z-60)+.022*(y+44)**2
            centre_z=61.8+.5*(y+45.8)
            body=(np.sqrt(((lateral-centre_x)/1.45)**2+
                          ((y+45.8)/9.0)**2+((z-centre_z)/9.5)**2)-1)*1.45
            roof=68.0+.035*(y+44)**2-.28*(lateral-centre_x)**2
            body=softmax(body,z-roof,1.4)
            # A slim periarterial receiving space continues around the entire
            # labelled cavernous course, including its superior bend and exit.
            body=softmin(body,artery_fields[side]-.85,.55)
            # Fit the sphenoidal medial wall to nearby facing carotid-sulcus
            # bone. The later bone cut sets a small numerical surface clearance.
            ap,af=arteries['ICA cavernous '+side]
            sampled=np.unique(np.round(ap[(ap[:,2]>54)&(ap[:,2]<73)]/.65).astype(int),axis=0)*.65
            medial=np.full_like(field,50.)
            for point in sampled:
                q=[0.,0.,0.];cell=vtk.reference(0);sub=vtk.reference(0);dist2=vtk.reference(0.)
                bone_locator.FindClosestPoint(point,q,cell,sub,dist2);q=np.array(q)
                vector=point-q;gap=np.linalg.norm(vector)
                if not (.45<gap<3.5 and sign*vector[0]>.6*gap):continue
                sl,distance=capsule(q,point,.65)
                medial[sl]=softmin(medial[sl],distance,.35)
                apposition_seeds.append({'side':side,'bone_point':q.tolist(),'arterial_neighbourhood':point.tolist(),'gap_mm':float(gap)})
            # Sample the facing sulcus as well as projecting from the artery;
            # this fills gaps where one arterial point has several nearby bone
            # patches and a nearest-point-only projection misses part of the wall.
            bp,bf=arrays(next(r for r in records if r['name']=='bone.sphenoid'))
            bc=bp[bf].mean(1);bn=np.cross(bp[bf[:,1]]-bp[bf[:,0]],bp[bf[:,2]]-bp[bf[:,0]])
            bn/=np.maximum(np.linalg.norm(bn,axis=1)[:,None],1e-12)
            lat=bc[:,0] if sign==1 else 1.3-bc[:,0]
            candidates=(lat>5)&(lat<14)&(bc[:,1]>-54)&(bc[:,1]<-36)&(bc[:,2]>55)&(bc[:,2]<70)&(sign*bn[:,0]>.35)
            aloc=vtk.vtkStaticCellLocator();aloc.SetDataSet(poly(ap,af));aloc.BuildLocator()
            seen=set()
            for q,normal in zip(bc[candidates],bn[candidates]):
                key=tuple(np.rint(q/.4).astype(int))
                if key in seen:continue
                seen.add(key)
                point=[0.,0.,0.];cell=vtk.reference(0);sub=vtk.reference(0);dist2=vtk.reference(0.)
                aloc.FindClosestPoint(q,point,cell,sub,dist2);point=np.array(point)
                vector=point-q;gap=np.linalg.norm(vector)
                if not (.45<gap<3.5 and sign*vector[0]>.6*gap and np.dot(vector,normal)>.45*gap):continue
                sl,distance=capsule(q,point,.7)
                medial[sl]=softmin(medial[sl],distance,.35)
                apposition_seeds.append({'side':side,'bone_point':q.tolist(),'arterial_neighbourhood':point.tolist(),'gap_mm':float(gap),'method':'facing sulcus patch'})
            body=softmin(body,medial,.55)
            mask=body<field;new_owner[mask]=ids.index('vein.cavernous.'+side)
            field=softmin(field,body,.85)
            # Rebuild the terminal receiving channels with tangent-continuous
            # curves and smoothly blended mouths. No flat joining plates.
            dz=-.05 if side=='left' else 0
            for name,q,width,depth in [
                ('sphenoparietal',[[25.5,-30.96,74.77],[23,-33.1,72.8],[20,-35.5,70.6],[17.2,-37.9,68.5],[14.2,-40.2,67.5]],1.45,.7),
                ('superficial_middle_cerebral',[[25.5,-31.2,60.2],[23,-32.8,61.3],[20,-35.7,62.9],[16.9,-39.7,65.1],[14.7,-42.5,65.8]],1.3,1.2),
                ('superior_ophthalmic',[[20.9,-27.8,69.2],[20.5,-31,67.6],[18.5,-35.2,67],[16,-37.8,66.5],[14.5,-40.2,66.2]],1.0,.9),
                ('ovale_emissary',[[26.5,-43.5,45.0],[24.3,-45.8,49.4],[21.5,-46.6,53],[18.5,-47.2,55.4],[16.4,-47.8,58.2]],.9,.8),
                ('superior_petrosal',[[22.6,-57.5,56.7],[21.8,-56.8,56.3],[19,-54.7,56.8],[17,-53.2,58.4],[15.8,-51.6,60]],1.05,.8),
                ('inferior_petrosal',[[13.3,-58,51.5],[13.3,-56.6,52.2],[13.8,-54.7,53.8],[14.6,-53.6,56],[15.1,-52.2,58.2]],1.05,.9)]:
                if side=='left' and name=='superficial_middle_cerebral':
                    q=[[25.5,-31.4,60.7],[23,-33.1,61.9],[20,-35.9,63.5],[16.9,-39.7,65.1],[14.7,-42.5,65.8]]
                q=[c(cx,cy,cz+dz) for cx,cy,cz in q]
                branch,centres=branch_field(q,width,depth)
                mask=branch<field;new_owner[mask]=ids.index('vein.'+name+'.'+side)
                rebuilt_entry|=mask;field=softmin(field,branch,.95)
                junction_paths.append({'id':'vein.'+name+'.'+side,'points':centres.tolist(),
                                       'width_radius_mm':width,'depth_radius_mm':depth})
            # Short posterior communication to the retained clival plexus.
            q=([c(11,-53.5,54.8),c(12.8,-54.5,56),c(14.4,-54.7,57.8),c(15.9,-53.7,59.7),c(15.6,-51.7,60.8)]
               if side=='right' else
               [c(11,-53.0,57.3),c(12.8,-54.5,57.2),c(14.4,-54.7,58.3),c(15.9,-53.7,59.7),c(15.6,-51.7,60.8)])
            neck,centres=branch_field(q,.75,.65)
            mask=neck<field;new_owner[mask]=ids.index('vein.cavernous.'+side)
            field=softmin(field,neck,.8)
            junction_paths.append({'id':'vein.cavernous.'+side,'role':'basilar receiving neck','points':centres.tolist(),'width_radius_mm':.75,'depth_radius_mm':.65})
        # Thin curved sellar cross-connections, with centres fitted clear of bone.
        for name,q,width,depth in [
            ('anterior_intercavernous',[[14.4,-41,67.2],[14.7,-39,68.6],[13,-37.8,70.3],[7,-37.5,70.6],[.65,-37.5,70.7],[-5.7,-37.5,70.6],[-11.7,-37.8,70.3],[-13.4,-39,68.6],[-13.1,-41,67.2]],.8,.6),
            ('posterior_intercavernous',[[14.8,-49,64.8],[9,-51.8,65.8],[5,-52.7,66.2],[.65,-52.9,66.2],[-3.7,-52.7,66.2],[-7.7,-51.8,65.8],[-13.5,-49,64.8]],.9,.65)]:
            bridge,centres=branch_field(q,width,depth)
            mask=bridge<field;new_owner[mask]=ids.index('vein.'+name)
            field=softmin(field,bridge,.8)
            junction_paths.append({'id':'vein.'+name,'points':centres.tolist(),'width_radius_mm':width,'depth_radius_mm':depth})
        # Exclude only the inferred pituitary/sellar soft-tissue space. No gland,
        # cranial nerves or invented septal compartments are added to the catalogue.
        sellar=ellipsoid([.65,-43,68.2],[5.9,5.6,5.6]);field=np.maximum(field,-sellar)
        # The artery stays excluded from venous volume while its outer
        # receiving envelope surrounds it. No arterial geometry is changed.
        for side,cut in artery_fields.items():
            mask=inside&(np.isin(new_owner,list(primary))|rebuilt_entry)
            field[mask]=np.maximum(field[mask],(.22-cut)[mask])
        # Clear the actual continuing ICA too. A cavernous-label-only closed
        # mask ends at the label port and can leave a venous disk over the next
        # arterial segment, although it clears the labelled cavernous skin.
        continued_mask=inside&(np.isin(new_owner,list(primary))|rebuilt_entry)&(field<.8)
        continued_points=points[continued_mask.ravel()]
        cloud=vtk.vtkPolyData();cloud_points=vtk.vtkPoints()
        cloud_points.SetData(numpy_to_vtk(continued_points,deep=True));cloud.SetPoints(cloud_points)
        for side,(ap,af) in retained_ica_courses().items():
            closed=closed_artery(ap,af);sdf=vtk.vtkImplicitPolyDataDistance();sdf.SetInput(closed)
            distances=np.abs(np.array([sdf.EvaluateFunction(point) for point in continued_points]))
            enclosed=vtk.vtkSelectEnclosedPoints();enclosed.SetInputData(cloud);enclosed.SetSurfaceData(closed)
            enclosed.SetTolerance(1e-6);enclosed.CheckSurfaceOn();enclosed.Update()
            membership=vtk_to_numpy(enclosed.GetOutput().GetPointData().GetArray('SelectedPoints')).astype(bool)
            cut=np.where(membership,-distances,distances)
            field[continued_mask]=np.maximum(field[continued_mask],.22-cut)
        print('Cleared continuing ICA exits',len(continued_points),'grid samples',flush=True)
        signed=bone_sdf
        # Apply bone exclusion in replacement interior, retain the original collar.
        # Keep pre-existing emissary/other channels intact even where the skull
        # model does not resolve their foramina. The new envelope alone receives
        # this bone exclusion; it must not sever unrelated retained tributaries.
        mask=inside&(np.isin(new_owner,list(primary))|rebuilt_entry)&(field<.8)
        bone=np.array([signed.EvaluateFunction(point) for point in points[mask.ravel()]])
        field[mask]=np.maximum(field[mask],.18-bone)
        field[[0,-1],:,:]=50;field[:,[0,-1],:]=50;field[:,:,[0,-1]]=50
        (ROOT/'medial-bone-apposition-v0.9.12.json').write_text(json.dumps(apposition_seeds,indent=2)+'\n')
        print('Built ICA-conforming envelope and medial bone apposition',len(apposition_seeds),'seeds',flush=True)
        (ROOT/'cavernous-junction-paths-v0.9.12.json').write_text(json.dumps(junction_paths,indent=2)+'\n')
        im=vtk.vtkImageData();im.SetDimensions(*shape);im.SetOrigin(*lo);im.SetSpacing(step,step,step)
        im.GetPointData().SetScalars(numpy_to_vtk(field.ravel(),deep=True))
        cont=vtk.vtkFlyingEdges3D();cont.SetInputData(im);cont.SetValue(0,0);cont.ComputeNormalsOff();cont.Update()
        smooth=vtk.vtkWindowedSincPolyDataFilter();smooth.SetInputConnection(cont.GetOutputPort())
        smooth.SetNumberOfIterations(12);smooth.SetPassBand(.12);smooth.NormalizeCoordinatesOn();smooth.Update()
        dec=vtk.vtkDecimatePro();dec.SetInputConnection(smooth.GetOutputPort());dec.SetTargetReduction(.55)
        dec.PreserveTopologyOn();dec.SplittingOff();dec.BoundaryVertexDeletionOff();dec.Update()
        pd=dec.GetOutput();np_=vtk_to_numpy(pd.GetPoints().GetData()).astype(np.float32)
        nf=vtk_to_numpy(pd.GetPolys().GetData()).reshape(-1,4)[:,1:].astype(np.uint32)
        cent=np_[nf].mean(1);grid=np.rint((cent-lo)/step).astype(int);grid=np.clip(grid,0,shape-1)
        nl=new_owner[grid[:,2],grid[:,1],grid[:,0]]
        atomic_npz(cache,p=np_,f=nf,labels=nl,lo=lo,hi=hi,innerlo=innerlo,innerhi=innerhi)
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
    # Allow only bounded fragments of the newly drawn envelope; none may
    # contain a retained tributary.
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
    # The completed v0.9.7 arterial correction is retained in this release.
    doc,data=read_glb(APP/'.authoring/circulation-refined.glb');arteries={}
    for node in doc['nodes']:
        if 'ICA cavernous' not in node['name']:continue
        prim=doc['meshes'][node['mesh']]['primitives'][0]
        arteries[node['name']]=(accessor(doc,data,prim['attributes']['POSITION']).copy(),
                              accessor(doc,data,prim['indices']).reshape(-1,3).copy())
    report=refine_veins(arteries)
    report.update(release='0.9.12',arterial_parts_changed=[],anastomotic_parts_changed=[],
                  method='Slim ICA-conforming cavernous envelope with carotid-sulcus bone apposition and retained direct tributary attachments; ICA and skull retained')
    (ROOT/'cavernous-local-build.json').write_text(json.dumps(report,indent=2)+'\n')
