"""Offline, shared-skin fitting of the delivered v0.9.15 vascular meshes.

Decoded delivered GLBs are authoritative. Curves guide a compact, incremental
coordinate deformation; they never replace the labelled vascular skin. Identical
coordinates at label boundaries receive identical displacements. Fixed boundary
collars isolate each batch from protected anatomy. No fitting runs in the app.
"""
import json, struct, hashlib, argparse
from pathlib import Path
import numpy as np
import trimesh, vtk
from scipy.spatial import cKDTree
from scipy.interpolate import PchipInterpolator
from scipy.ndimage import gaussian_filter1d,maximum_filter1d
from build_targets import poly
from vtk.util.numpy_support import vtk_to_numpy

APP=Path(__file__).resolve().parents[2]
PUB=APP/'public/anatomy'

def read_glb(path):
    raw=path.read_bytes();size=struct.unpack_from('<I',raw,12)[0]
    return json.loads(raw[20:20+size]),bytearray(raw[28+size:])

def accessor(doc,data,i):
    a=doc['accessors'][i];v=doc['bufferViews'][a['bufferView']]
    n={'SCALAR':1,'VEC2':2,'VEC3':3,'VEC4':4}[a['type']]
    dtype={5126:'<f4',5125:'<u4',5123:'<u2',5121:'u1'}[a['componentType']]
    return np.ndarray((a['count'],n),dtype=dtype,buffer=data,
        offset=v.get('byteOffset',0)+a.get('byteOffset',0),
        strides=(v.get('byteStride',np.dtype(dtype).itemsize*n),np.dtype(dtype).itemsize))

def write_glb(path,doc,data):
    j=json.dumps(doc,separators=(',',':')).encode();j+=b' '*(-len(j)%4)
    b=bytes(data);b+=b'\0'*(-len(b)%4)
    payload=struct.pack('<4sIIII',b'glTF',2,28+len(j)+len(b),len(j),0x4e4f534a)+j+struct.pack('<II',len(b),0x004e4942)+b
    # Large authoring buffers may receive a short write. Stream bounded chunks
    # and check the resulting GLB rather than accepting a truncated asset.
    with path.open('wb') as stream:
        view=memoryview(payload);offset=0
        while offset<len(view):
            written=stream.write(view[offset:offset+8*1024*1024])
            if not written:raise OSError('Incomplete GLB write: '+str(path))
            offset+=written
    assert path.stat().st_size==len(payload),'Truncated GLB: '+str(path)

def smoothstep(x):
    x=np.clip(x,0,1);return x*x*(3-2*x)

def resample(q,n=80):
    arc=np.r_[0,np.cumsum(np.linalg.norm(np.diff(q,axis=0),axis=1))]
    unique=np.r_[True,np.diff(arc)>1e-6];arc,q=arc[unique],q[unique]
    return np.column_stack([PchipInterpolator(arc,q[:,k])(np.linspace(0,arc[-1],n)) for k in range(3)])

def ray_tree(mesh):
    tree=vtk.vtkOBBTree();tree.SetDataSet(poly(mesh));tree.BuildLocator();return tree

def hits(tree,a,b):
    p=vtk.vtkPoints();tree.IntersectWithLine(a,b,p,None)
    return np.array([p.GetPoint(i) for i in range(p.GetNumberOfPoints())]).reshape(-1,3)

def front(tree,x,z):
    q=hits(tree,[x,5,z],[x,-140,z])
    if not len(q):raise ValueError(f'Missing exposed front surface at {x}, {z}')
    return q[np.argmax(q[:,1])]

def curve_from_mesh(mesh,axis=2,n=80):
    """Dense cross-section centres of the actual exported labelled tube."""
    lo,hi=mesh.bounds[:,axis];t=np.linspace(lo+.5,hi-.5,n);points=[]
    data=poly(mesh)
    for station in t:
        plane=vtk.vtkPlane();o=np.zeros(3);o[axis]=station;normal=np.zeros(3);normal[axis]=1
        plane.SetOrigin(*o);plane.SetNormal(*normal)
        cut=vtk.vtkCutter();cut.SetInputData(data);cut.SetCutFunction(plane);cut.Update()
        p=cut.GetOutput().GetPoints()
        if p is not None:
            v=vtk_to_numpy(p.GetData());points.append(v.mean(0))
    assert len(points)>n*.8,'Incomplete labelled tube sections'
    q=np.array(points);q=gaussian_filter1d(q,.8,axis=0)
    return resample(q,n)

class Batch:
    def __init__(self,name,curves,inner=3,outer=20):
        self.name=name;self.curves=curves;self.inner=inner;self.outer=outer
    def apply(self,points,fixed,steps=100):
        src=np.concatenate([c['source'] for c in self.curves]);dst=np.concatenate([c['target'] for c in self.curves])
        if np.linalg.norm(dst-src,axis=1).max()<3:steps=24
        p=points.copy();pin=cKDTree(fixed) if len(fixed) else None
        # Protect collars in their ORIGINAL coordinates. Multiplication is
        # fixed per vertex, giving precisely stationary shared boundary points.
        if pin:
            distance=pin.query(p)[0];lock=smoothstep(distance/8.)
        else:lock=np.ones(len(p))
        moved=np.zeros(len(p),bool)
        for i in range(steps):
            guide=src+(dst-src)*(i/steps);delta=(dst-src)/steps
            tree=cKDTree(guide);distance,index=tree.query(p,k=min(5,len(src)))
            weights=1/(distance*distance+1.5)**2
            v=(weights[:,:,None]*delta[index]).sum(1)/weights.sum(1)[:,None]
            taper=1-smoothstep((distance[:,0]-self.inner)/(self.outer-self.inner))
            d=v*(taper*lock)[:,None];p+=d;moved|=np.linalg.norm(d,axis=1)>1e-9
        p[~moved]=points[~moved]
        return p

class ShearBatch:
    """Triangular coordinate maps preserve transverse profiles and orientation.

    Dural fitting changes Z as a function of Y. Cortical fitting changes X/Y
    as a function of Z. In each inner edit region the Jacobian determinant is
    one. Outer labelled junctions have stationary, shared boundary collars.
    """
    def __init__(self,name,curve,mode):self.name=name;self.curves=[curve];self.mode=mode
    def apply(self,p,fixed,steps=100):
        c=self.curves[0];source=c['source'];delta=c['target']-source
        axis=1 if self.mode=='dural' else 2
        order=np.argsort(source[:,axis]);s=source[order];d=delta[order]
        keep=np.r_[True,np.diff(s[:,axis])>1e-5];s,d=s[keep],d[keep]
        t=np.clip(p[:,axis],s[0,axis],s[-1,axis])
        shift=np.column_stack([PchipInterpolator(s[:,axis],d[:,k])(t) for k in range(3)])
        if self.mode=='dural':
            # Zero before the anterior junction, and outside a generous vertical
            # support. At the sinus, this is a pure superior/inferior shear.
            centre=PchipInterpolator(s[:,axis],s[:,2])(t)
            dz=shift[:,2]*(1-smoothstep((p[:,1]-s[-1,1])/28))
            lower=np.minimum(45,centre+dz-12)
            z=p[:,2];mapped=z.copy()
            # A monotone, piecewise linear vertical map is invertible even when
            # the dural seam is much lower than the old estimated sinus.
            a,b,c,e=lower,centre-4,centre+4,centre+35
            B,C=centre+dz-4,centre+dz+4
            zone=(z>a)&(z<b);mapped[zone]=a[zone]+(z[zone]-a[zone])*(B[zone]-a[zone])/(b[zone]-a[zone])
            zone=(z>=b)&(z<=c);mapped[zone]=z[zone]+dz[zone]
            zone=(z>c)&(z<e);mapped[zone]=C[zone]+(z[zone]-c[zone])*(e[zone]-C[zone])/(e[zone]-c[zone])
            w=1-smoothstep((np.abs(p[:,0]-.65)-6)/28)
            shift[:]=0;shift[:,2]=mapped-z
        else:
            w=np.ones(len(p));shift[:,2]=0
        if len(fixed):w*=smoothstep(cKDTree(fixed).query(p)[0]/8)
        return p+shift*w[:,None]

class StemBatch:
    """Smooth anterior/lateral cage map, evaluated once in baseline coordinates."""
    def __init__(self,name,curves):self.name=name;self.curves=curves
    def apply(self,p,fixed,steps=100):
        source=np.concatenate([c['source'] for c in self.curves]);target=np.concatenate([c['target'] for c in self.curves])
        # Route-dependent transverse displacements; Z is retained. Large changes
        # therefore do not fold the tubes back in their longitudinal direction.
        delta=target-source;delta[:,2]=0
        tree=cKDTree(source[:,[0,2]])
        dist,idx=tree.query(p[:,[0,2]],k=6)
        w=1/(dist*dist+.4)**2;shift=(w[:,:,None]*delta[idx]).sum(1)/w.sum(1)[:,None]
        nearest=source[idx[:,0]];support=1-smoothstep((np.linalg.norm(p-nearest,axis=1)-4)/28)
        if len(fixed):support*=smoothstep(cKDTree(fixed).query(p)[0]/10)
        return p+shift*support[:,None]

def mesh_records(doc,data):
    out={}
    for node in doc['nodes']:
        if 'mesh' not in node:continue
        assert not any(k in node for k in ['matrix','translation','rotation','scale']), 'Only world-space baseline supported'
        prim=doc['meshes'][node['mesh']]['primitives'][0]
        p=accessor(doc,data,prim['attributes']['POSITION'])
        f=accessor(doc,data,prim['indices']).reshape(-1,3)
        out[node['name']]={'primitive':prim,'positions':p,'faces':f,'old':p.astype(float).copy()}
    return out

def neighbours(records,selected):
    """Select joined labels from actual coincident boundary coordinates."""
    source=np.concatenate([r['old'] for k,r in records.items() if k in selected])
    tree=cKDTree(source);added=set()
    for k,r in records.items():
        if k not in selected and tree.query(r['old'])[0].min()<1e-5:added.add(k)
    return selected|added

def deform(records,batch,selected,whole=False,excluded=()):
    selected=(set(records) if whole else neighbours(records,set(selected)))-set(excluded)
    p=np.concatenate([r['positions'].astype(float) for k,r in records.items() if k in selected])
    # Pin every coordinate shared with labels outside this batch. Common-skin
    # junctions inside the region remain free to move together.
    untouched=[r['positions'].astype(float) for k,r in records.items() if k not in selected]
    fixed=p[cKDTree(np.concatenate(untouched)).query(p)[0]<1e-5] if untouched else np.empty((0,3))
    new=batch.apply(p,fixed);offset=0;report=[]
    for k,r in records.items():
        if k not in selected:continue
        count=len(r['positions']);q=new[offset:offset+count];offset+=count
        delta=np.linalg.norm(q-r['positions'],axis=1)
        r['positions'][:]=q
        if delta.max()>1e-5:report.append({'node':k,'maximumDisplacementMm':float(delta.max()),'movedVertices':int((delta>1e-5).sum())})
    return {'name':batch.name,'selectedNodes':sorted(selected),'fixedBoundaryCoordinates':len(fixed),'changedNodes':report}

def refine_envelope(records,keys,tree,direction,rows=None):
    """Translate whole local cross-sections beyond the exposed tissue envelope.

    The target is computed from EVERY actual vessel-wall vertex, including its
    radius. Anterior, lateral and cortical envelopes avoid atlas cut faces.
    A conservative smooth maximum propagates wall clearance to the centreline.
    """
    curves=[]
    for key in keys:
        r=records[key];m=trimesh.Trimesh(r['positions'],r['faces'],process=False)
        axis=0 if any(k in key for k in ['transverse_pontine','pontomedullary']) else 2
        src=curve_from_mesh(m,axis=axis,n=120)
        sign=-1 if key.endswith(('left','_left')) else 1
        displacement=np.zeros((len(src),3));wall=r['positions'].astype(float)
        parameter=src[:,axis]
        for p in wall:
            if direction=='cortical' and p[2]<120:continue
            if direction=='cage':
                candidates=[]
                for component,sgn,a,b in [(1,1,[p[0],5,p[2]],[p[0],-140,p[2]]),(0,sign,[sign*115,p[1],p[2]],[.65,p[1],p[2]])]:
                    hit=hits(tree,a,b)
                    if not len(hit):continue
                    surface=hit[np.argmax(sgn*hit[:,component])];gap=sgn*(surface[component]-p[component])+.55
                    if gap>0:candidates.append((gap,component,sgn))
                if not candidates:continue
                gap,component,sgn=min(candidates)
                if gap>8:continue
            elif direction=='anterior':a=[p[0],5,p[2]];b=[p[0],-140,p[2]];component=1;sgn=1
            else:a=[sign*115,p[1],p[2]];b=[.65,p[1],p[2]];component=0;sgn=sign
            if direction!='cage':
                hit=hits(tree,a,b)
                if not len(hit):continue
                surface=hit[np.argmax(sgn*hit[:,component])]
            # A distant posterior bridging outlet must not be projected to an
            # unrelated anterior face of a different anatomical level.
                gap=sgn*(surface[component]-p[component])+.45
            if gap<=0 or gap>8:continue
            index=int(np.argmin(np.abs(parameter-p[axis])))
            displacement[index,component]=max(displacement[index,component],gap)
        displacement=maximum_filter1d(displacement,size=7,axis=0,mode='nearest')
        displacement=gaussian_filter1d(displacement,1.,axis=0,mode='nearest')
        displacement[:,0]*=sign
        dst=src+displacement
        curves.append({'id':key,'source':src,'target':dst,'rule':'exported-wall-envelope-clearance'})
    return deform(records,Batch(direction+'-wall-envelope',curves,inner=3,outer=12),keys)

def refine_cortical(records,side,brain,allow_z=False):
    key='Central '+side;r=records[key];src=curve_from_mesh(trimesh.Trimesh(r['positions'],r['faces'],process=False),n=120)
    bones=trimesh.load(APP/'.authoring/bones-baseline.glb',process=False)
    surfaces=[brain.geometry['brain.'+k+'.'+side] for k in ['precentral-gyrus','postcentral-gyrus']]+[bones.geometry['bone.parietal.'+side]]
    locators=[]
    for m in surfaces:
        f=vtk.vtkImplicitPolyDataDistance();f.SetInput(poly(m));locators.append(f)
    displacement=np.zeros_like(src);deficit=np.zeros(len(src))
    for p in r['positions'].astype(float):
        if p[2]<115:continue
        for f in locators:
            d=f.EvaluateFunction(p)
            if d>=.35:continue
            gradient=np.zeros(3);f.EvaluateGradient(p,gradient)
            if not allow_z:gradient[2]=0
            norm=np.linalg.norm(gradient)
            if norm<1e-8:continue
            gap=.35-d;i=int(np.argmin(abs(src[:,2]-p[2])))
            if gap>deficit[i]:displacement[i]=gradient*gap/norm;deficit[i]=gap
    # Expand each correction across nearby full cross-sections. Early passes
    # retain Z; terminal refinement may follow the full local normal where
    # the banks converge. The authoritative common skin remains intact.
    for i in range(len(src)):
        near=np.arange(max(0,i-3),min(len(src),i+4));j=near[np.argmax(deficit[near])]
        if deficit[j]>deficit[i]:displacement[i]=displacement[j]
    displacement=gaussian_filter1d(displacement,1,axis=0)
    curve={'id':key,'source':src,'target':src+displacement,'rule':'signed-local-corridor-wall-clearance'}
    return deform(records,Batch('central-corridor-wall-clearance-'+side,[curve],inner=3,outer=12),[key])

def fit_terminal_corridor(records,side,brain,rows):
    key='Central '+side;r=records[key];m=trimesh.Trimesh(r['positions'],r['faces'],process=False)
    phase=trimesh.Trimesh(m.vertices,m.faces[np.all(m.vertices[m.faces,2]>=150,axis=1)],process=False)
    surfaces=[brain.geometry['brain.'+k+'.'+side] for k in ['precentral-gyrus','postcentral-gyrus']]
    # Only constrain a terminal span that still intersects a bank. Do not move
    # the opposite already-clear artery merely to impose symmetry.
    from verify_fitting import collisions
    if not sum(collisions(phase,t) for t in surfaces):return None
    src=curve_from_mesh(m,n=120);dst=src.copy()
    guide=np.array(rows['brain.landmark.central-sulcus.'+side]['landmark']['course'])
    fs=[]
    for t in surfaces:
        f=vtk.vtkImplicitPolyDataDistance();f.SetInput(poly(t));fs.append(f)
    offsets=np.array([[x,y,0] for x in np.linspace(-8,8,65) for y in np.linspace(-8,8,65)])
    offsets=offsets[np.argsort(np.linalg.norm(offsets,axis=1))]
    for i,q in enumerate(src):
        if q[2]<150:continue
        desired=np.array([guide[-1,0],guide[-1,1],q[2]]) if q[2]>=152.8 else np.array([PchipInterpolator(guide[:,2],guide[:,k])(min(q[2],guide[-1,2])) for k in range(3)])
        desired[2]=q[2]
        for offset in offsets:
            candidate=desired+offset
            if min(f.EvaluateFunction(candidate) for f in fs)>=1.25:
                w=smoothstep((q[2]-150)/2.8);dst[i]=q+(candidate-q)*w;break
        else:raise ValueError(f'Unsupported terminal corridor: {side}, {q}')
    curve={'id':key,'source':src,'target':dst,'rule':'terminal-sulcal-corridor'}
    return deform(records,ShearBatch('terminal-sulcal-corridor-'+side,curve,'cortical'),[key])

def refine_triangle_contacts(records,side,brain):
    key='Central '+side;r=records[key]
    m=trimesh.Trimesh(r['positions'],r['faces'],process=False)
    mask=np.all(m.vertices[m.faces,2]>=120,axis=1)
    phase=trimesh.Trimesh(m.vertices,m.faces[mask],process=False)
    target=trimesh.util.concatenate([brain.geometry['brain.'+k+'.'+side] for k in ['precentral-gyrus','postcentral-gyrus']])
    test=vtk.vtkCollisionDetectionFilter();test.SetInputData(0,poly(phase));test.SetInputData(1,poly(target));test.SetTransform(0,vtk.vtkTransform());test.SetTransform(1,vtk.vtkTransform());test.SetCollisionModeToAllContacts();test.Update()
    if not test.GetNumberOfContacts():return None
    cells0=vtk_to_numpy(test.GetContactCells(0));cells1=vtk_to_numpy(test.GetContactCells(1))
    src=[];dst=[]
    for a,b in zip(cells0,cells1):
        wall=phase.vertices[phase.faces[a]];tri=target.vertices[target.faces[b]]
        normal=np.cross(tri[1]-tri[0],tri[2]-tri[0]);normal/=max(np.linalg.norm(normal),1e-12)
        depth=float(((wall-tri[0])@normal).min());delta=normal*min(1.,max(.12,.22-depth))
        point=wall.mean(0);src.append(point);dst.append(point+delta)
    curve={'id':key,'source':np.array(src),'target':np.array(dst),'rule':'actual-triangle-contact-clearance'}
    result=deform(records,Batch('actual-triangle-contact-clearance-'+side,[curve],inner=2,outer=6),[key]);result['inputContacts']=int(test.GetNumberOfContacts());return result

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--prepare-only',action='store_true');parser.add_argument('--refine-only',action='store_true');parser.add_argument('--terminal-only',action='store_true');parser.add_argument('--contact-only',action='store_true');parser.add_argument('--include-left-central-experiment',action='store_true');parser.add_argument('--include-right-central-experiment',action='store_true');parser.add_argument('--include-dural-experiment',action='store_true');parser.add_argument('--include-brainstem-experiment',action='store_true');args=parser.parse_args()
    if (args.refine_only or args.terminal_only or args.contact_only) and not (args.include_left_central_experiment or args.include_right_central_experiment):parser.error('Resume modes require an explicit central experiment flag.')
    active_sides=(['left'] if args.include_left_central_experiment else [])+(['right'] if args.include_right_central_experiment else [])
    manifest=json.loads((APP/'anatomy/generated/complete_manifest.json').read_text());rows={s['id']:s for s in manifest['structures']}
    brain=trimesh.load(PUB/'models/brain-context.glb',process=False)
    docs={};records={}
    for name in ['veins','arteries']:
        doc,data=read_glb(APP/f'.authoring/{name}-baseline.glb');docs[name]=(doc,data);records[name]=mesh_records(doc,data)
    if args.refine_only or args.terminal_only or args.contact_only:
        for name in records:
            doc_,data_=read_glb(APP/f'.authoring/{name}-fitted.glb');current=mesh_records(doc_,data_)
            for key,r in records[name].items():r['positions'][:]=current[key]['positions']
    def mesh(kind,key):
        r=records[kind][key];return trimesh.Trimesh(r['old'],r['faces'],process=False)
    # Full falcotentorial attachment, anterior to posterior. Preserve original
    # sinus profile; place its centre 1.3 mm superior to the dural seam.
    source=curve_from_mesh(mesh('veins','vein.straight'),axis=1)[::-1]
    seam=np.array(rows['brain.landmark.falcotentorial']['landmark']['course'])[::-1]
    target=source.copy()
    target[:,2]=PchipInterpolator(seam[:,1],seam[:,2],extrapolate=True)(np.clip(source[:,1],seam[0,1],seam[-1,1]))+1.3
    # The source guide includes tentorial attachment anterior to the venous
    # junction. It is not the required start of the straight sinus. Keep the
    # existing AP junction position and fit its Z to the appropriate seam.
    posterior=source[:,1]<seam[0,1]
    target[posterior,2]=np.interp(source[posterior,1],[source[:,1].min(),seam[0,1]],[66.0,seam[0,2]+1.3])
    target[:,2]=source[:,2]+(target[:,2]-source[:,2])*smoothstep((source[:,1]+139)/9)
    dural=[{'id':'vein.straight','source':source,'target':target,'rule':'dural-attachment','surfaceIds':['brain.falx-cerebri','brain.tentorium-cerebelli.left','brain.tentorium-cerebelli.right']}]
    # Inspect radiating vein routes on exposed surfaces. Never attract the
    # longitudinal channel to the atlas halves' artificial midline cut faces.
    kinds=['medulla-oblongata','pons','midbrain','base-of-peduncle']
    stemmesh=trimesh.util.concatenate([brain.geometry[f'brain.{k}.{s}'] for k in kinds for s in ['left','right']])
    stem=ray_tree(stemmesh)
    paths={q['id']:q for q in json.loads((APP/'anatomy/source/venous/fitted-paths.json').read_text())}
    stemcurves=[]
    for key in ['vein.anterior_medullary','vein.anterior_pontine','vein.anterior_pontomesencephalic']:
        src=curve_from_mesh(mesh('veins',key))
        rad=float(np.median(paths[key]['radii']));dst=np.array([front(stem,q[0],q[2]) for q in src]);dst[:,1]+=rad+.2
        dst=gaussian_filter1d(dst,1.3,axis=0)
        stemcurves.append({'id':key,'source':src,'target':dst,'rule':'surface-vein','surfaceIds':[f'brain.{k}.{s}' for k in kinds for s in ['left','right']]})
    # Transverse channels follow the exposed anterolateral surface. The lateral
    # ends retain their existing free bridging spans to the petrosal collectors.
    for name,z in [('transverse_pontine',57.),('pontomedullary',45.)]:
        for side in ['left','right']:
            key=f'vein.{name}.{side}';src=resample(np.array(paths[key]['points']))
            dst=src.copy();sign=1 if side=='right' else -1
            for i,q in enumerate(src):
                frac=np.clip(abs(q[0]-.65)/22,0,1);angle=frac*np.pi/2
                zz=q[2]
                origin=np.array([.65,-69 if name=='transverse_pontine' else -72,zz])
                direction=np.array([sign*np.sin(angle),np.cos(angle),0])
                intersection=hits(stem,origin+direction*80,origin)
                if len(intersection):
                    surface=intersection[np.argmax(np.linalg.norm(intersection-origin,axis=1))]
                    desired=surface+direction*.95
                    desired=desired*(1-smoothstep((frac-.72)/.28))+q*smoothstep((frac-.72)/.28)
                    dst[i]=desired
            dst=gaussian_filter1d(dst,1.5,axis=0)
            stemcurves.append({'id':key,'source':src,'target':dst,'rule':'surface-vein-with-bridging-outlet','surfaceIds':['brain.pons.left','brain.pons.right','brain.medulla-oblongata.left','brain.medulla-oblongata.right']})
    # Lateral mesencephalic channels: retain the basal and petrosal outlet
    # collars, fit the intervening exposed lateral midbrain/upper pontine course.
    for side in ['left','right']:
        key='vein.lateral_mesencephalic.'+side;src=resample(np.array(paths[key]['points']));dst=src.copy();sign=1 if side=='right' else -1
        for i,q in enumerate(src):
            z=np.clip(q[2],59.5,83.5);origin=np.array([.65,-68,z]);direction=np.array([sign,0,0])
            intersection=hits(stem,origin+direction*70,origin)
            if len(intersection):
                desired=intersection[np.argmax(np.linalg.norm(intersection-origin,axis=1))]+direction*1.05
                weight=smoothstep((q[2]-59)/7)*(1-smoothstep((q[2]-81)/7));dst[i]=q*(1-weight)+desired*weight
        dst=gaussian_filter1d(dst,1.5,axis=0)
        stemcurves.append({'id':key,'source':src,'target':dst,'rule':'surface-vein-with-bridging-outlets','surfaceIds':['brain.midbrain.'+side,'brain.pons.'+side]})
    cortical=[]
    for side in ['left','right']:
        src=curve_from_mesh(mesh('arteries','Central '+side));guide=np.array(rows['brain.landmark.central-sulcus.'+side]['landmark']['course'])
        # Ordered, shape-preserving interpolation along the reviewed lateral
        # sulcal lip, keeping the proximal opercular attachment as a fixed collar.
        z=src[:,2];tip=guide[-1,2]-.5;zz=np.minimum(z,tip)
        dst=np.column_stack([PchipInterpolator(guide[:,2],guide[:,k])(zz) for k in range(3)])
        sign=1 if side=='right' else -1
        bone_scene=trimesh.load(APP/'.authoring/bones-baseline.glb',process=False)
        surfaces=[brain.geometry['brain.'+k+'.'+side] for k in ['precentral-gyrus','postcentral-gyrus']]+[bone_scene.geometry['bone.parietal.'+side]]
        locators=[]
        for m in surfaces:
            f=vtk.vtkImplicitPolyDataDistance();f.SetInput(poly(m));locators.append(f)
        # The sulcal reference lies between the banks. Projecting beyond the
        # outer envelope would leave that corridor and can enter the skull.
        offsets=np.array([[x,y,0] for x in np.linspace(-8,8,41) for y in np.linspace(-8,8,41)])
        offsets=offsets[np.argsort(np.linalg.norm(offsets,axis=1))]
        for i,q in enumerate(dst):
            for offset in offsets:
                candidate=q+offset
                if min(f.EvaluateFunction(candidate) for f in locators)>=1.1:
                    dst[i]=candidate;break
            else:raise ValueError(f'No supported central sulcal corridor at {side}, {q}')
        dst=gaussian_filter1d(dst,1.1,axis=0)
        weight=smoothstep((z-z.min())/8);dst=src+(dst-src)*weight[:,None]
        cortical.append({'id':'artery.anterior.central_'+side,'source':src,'target':dst,'rule':'opercular-to-sulcal','surfaceIds':['brain.central-sulcus.'+side,'brain.precentral-gyrus.'+side,'brain.postcentral-gyrus.'+side]})
    brain_adjustments=manifest.get('brainAdjustmentPolicy',{}).get('appliedAdjustments',[])
    specs={'baseline':'0.9.15','release':'0.9.17','brainAssetSha256':manifest['brainRegistration']['registeredAssetSha256'],'brainAdjustments':brain_adjustments,
        'leftCentralExperimentApplied':args.include_left_central_experiment,'rightCentralExperimentApplied':args.include_right_central_experiment,'duralExperimentApplied':args.include_dural_experiment,'brainstemExperimentApplied':args.include_brainstem_experiment,'method':'Monotone dural map, cortical shear and incremental compact brainstem deformation of decoded delivered common skin, with shared attachment collars and actual-wall clearance refinement.',
        'curves':[{**c,'applied':(c['rule']=='opercular-to-sulcal' and ((c['id'].endswith('left') and args.include_left_central_experiment) or (c['id'].endswith('right') and args.include_right_central_experiment))) or (c['rule']=='dural-attachment' and args.include_dural_experiment) or (c['rule'].startswith('surface-vein') and args.include_brainstem_experiment),'source':c['source'].tolist(),'target':c['target'].tolist()} for c in dural+stemcurves+cortical]}
    sourcepath=APP/'anatomy/source/brain/vessel-fitting-v0.9.17.json';sourcepath.write_text(json.dumps(specs,indent=2)+'\n')
    if args.prepare_only:return
    changes=json.loads((APP/'docs/validation/vessel-fitting-v0.9.17.json').read_text())['batches'] if args.refine_only or args.terminal_only or args.contact_only else []
    dural_map=ShearBatch('straight-sinus-and-shared-attachments',dural[0],'dural')
    if args.include_dural_experiment and not (args.refine_only or args.terminal_only or args.contact_only):
        changes.append(deform(records['veins'],dural_map,
        ['vein.straight','vein.galen','vein.inferior_sagittal','vein.confluence'],whole=True,excluded=[] if args.include_brainstem_experiment else [c['id'] for c in stemcurves]))
    if args.include_brainstem_experiment and not (args.refine_only or args.terminal_only or args.contact_only):
        # Use separate compact fields for the anterior cage and lateral channels.
        anterior=[c for c in stemcurves if 'lateral_mesencephalic' not in c['id']]
        lateral=[c for c in stemcurves if 'lateral_mesencephalic' in c['id']]
        for c in stemcurves:
            if args.include_dural_experiment:c['source']=dural_map.apply(c['source'],np.empty((0,3)))
        changes.append(deform(records['veins'],Batch('brainstem-veins-and-shared-attachments',stemcurves,inner=3,outer=25),[c['id'] for c in stemcurves]))
        # Re-evaluate the actual deformed wall, not the original authoring curve.
        # Radius clearance on an oblique medullary surface requires more than a
        # radius measured along the anterior axis. Refine these three channels
        # using their exported cross-section centres, with shared adjoining collars.
        for iteration in range(3):
            correction=[]
            for key in ['vein.anterior_medullary','vein.pontomedullary.left','vein.pontomedullary.right']:
                r=records['veins'][key];src=curve_from_mesh(trimesh.Trimesh(r['positions'],r['faces'],process=False),axis=2 if key=='vein.anterior_medullary' else 0)
                dst=src.copy()
                for i,q in enumerate(src):
                    intersections=hits(stem,[q[0],5,q[2]],[q[0],-140,q[2]])
                    if not len(intersections):continue
                    anterior_point=intersections[np.argmax(intersections[:,1])]
                    samples=[]
                    for dx,dz in [(0,.3),(0,-.3),(.3,0),(-.3,0)]:
                        h=hits(stem,[q[0]+dx,5,q[2]+dz],[q[0]+dx,-140,q[2]+dz])
                        samples.append(float(h[:,1].max()) if len(h) else anterior_point[1])
                    slope=np.hypot((samples[0]-samples[1])/.6,(samples[2]-samples[3])/.6)
                    clearance=min(2.8,.72*np.sqrt(1+slope*slope)+.6)
                    dst[i,1]=max(q[1],anterior_point[1]+clearance)
                dst[:,1]=gaussian_filter1d(dst[:,1],1,axis=0)
                dst[:,1]=np.maximum(dst[:,1],src[:,1])
                correction.append({'id':key,'source':src,'target':dst,'rule':'radius-aware-wall-refinement'})
            changes.append(deform(records['veins'],Batch('medullary-wall-clearance-'+str(iteration+1),correction,inner=3,outer=16),[c['id'] for c in correction]))
    for c in ([] if args.refine_only or args.terminal_only or args.contact_only else [c for c in cortical if (c['id'].endswith('left') and args.include_left_central_experiment) or (c['id'].endswith('right') and args.include_right_central_experiment)]):
        changes.append(deform(records['arteries'],ShearBatch(c['id'],c,'cortical'),[rows[c['id']]['asset']['node']]))
    anterior_keys=[c['id'] for c in stemcurves if 'lateral_mesencephalic' not in c['id']]
    lateral_keys=[c['id'] for c in stemcurves if 'lateral_mesencephalic' in c['id']]
    for iteration in range(16 if args.terminal_only or args.contact_only else (8 if args.refine_only else 0),16):
        if args.include_brainstem_experiment:
            changes.append(refine_envelope(records['veins'],[k for k in anterior_keys if not any(t in k for t in ['transverse_pontine','pontomedullary'])],stem,'anterior'))
            changes.append(refine_envelope(records['veins'],[k for k in anterior_keys if any(t in k for t in ['transverse_pontine','pontomedullary'])],stem,'cage'))
            changes.append(refine_envelope(records['veins'],lateral_keys,stem,'lateral'))
        for side in active_sides:
            banks=ray_tree(trimesh.util.concatenate([brain.geometry['brain.'+k+'.'+side] for k in ['precentral-gyrus','postcentral-gyrus']]))
            changes.append(refine_cortical(records['arteries'],side,brain,allow_z=iteration>=8))
    for side in active_sides:
        result=None if args.contact_only else fit_terminal_corridor(records['arteries'],side,brain,rows)
        if result:changes.append(result)
    for iteration in range(12):
        contact_changes=[]
        for side in active_sides:
            result=refine_triangle_contacts(records['arteries'],side,brain)
            if result:contact_changes.append(result)
        if contact_changes:print('Triangle contact refinement',iteration+1,[(c['name'],c['inputContacts']) for c in contact_changes],flush=True)
        changes.extend(contact_changes)
        if not contact_changes:break
    geometry=[]
    for name,(doc,data) in docs.items():
        if all(np.array_equal(r['positions'],r['old']) for r in records[name].values()):
            write_glb(APP/f'.authoring/{name}-fitted.glb',doc,data);continue
        # Accumulate normals over the complete common skin, across label seams.
        # Protected label buffers are not rewritten.
        all_old=np.concatenate([r['old'] for r in records[name].values()])
        _,inverse=np.unique(np.round(all_old,5),axis=0,return_inverse=True)
        shared_normals=np.zeros((inverse.max()+1,3));offset=0
        for r in records[name].values():
            p=r['positions'].astype(float);f=r['faces'];ids=inverse[offset:offset+len(p)];offset+=len(p)
            fn=np.cross(p[f[:,1]]-p[f[:,0]],p[f[:,2]]-p[f[:,0]])
            for k in range(3):np.add.at(shared_normals,ids[f[:,k]],fn)
        shared_normals/=np.maximum(np.linalg.norm(shared_normals,axis=1)[:,None],1e-12)
        offset=0
        for key,r in records[name].items():
            p=r['positions'].astype(float);old=r['old'];f=r['faces'];delta=np.linalg.norm(p-old,axis=1)
            normal_ids=inverse[offset:offset+len(p)];offset+=len(p)
            if delta.max()<1e-6:continue
            oldfn=np.cross(old[f[:,1]]-old[f[:,0]],old[f[:,2]]-old[f[:,0]])
            fn=np.cross(p[f[:,1]]-p[f[:,0]],p[f[:,2]]-p[f[:,0]])
            area0=np.linalg.norm(oldfn,axis=1);area=np.linalg.norm(fn,axis=1)
            assert np.isfinite(p).all() and np.all(area[area0>1e-8]>1e-9),key
            # Recompute shared normals after deformation, rather than retaining
            # stale vertex normals or transforming labels independently.
            normals=shared_normals[normal_ids]
            accessor(doc,data,r['primitive']['attributes']['NORMAL'])[:]=normals
            doc['accessors'][r['primitive']['attributes']['POSITION']].update(min=p.min(0).tolist(),max=p.max(0).tolist())
            geometry.append({'asset':name,'node':key,'maximumDisplacementMm':float(delta.max()),'movedVertices':int((delta>1e-5).sum()),
                'triangleCountRetained':len(f),'vertexCountRetained':len(p),'minimumTriangleAreaRatio':float(np.min(area[area0>1e-8]/area0[area0>1e-8])),
                'medianTriangleAreaRatio':float(np.median(area[area0>1e-8]/area0[area0>1e-8])),'unchangedVerticesBitIdentical':bool(np.array_equal(p[delta<1e-6],old[delta<1e-6]))})
        write_glb(APP/f'.authoring/{name}-fitted.glb',doc,data)
    report={'release':'0.9.17','baseline':'0.9.15','leftCentralExperimentApplied':args.include_left_central_experiment,'rightCentralExperimentApplied':args.include_right_central_experiment,'duralExperimentApplied':args.include_dural_experiment,'brainstemExperimentApplied':args.include_brainstem_experiment,'brainAdjustments':brain_adjustments,'batches':changes,'geometry':geometry,
        'limitations':['Atlas teaching reconstruction; anatomical review remains required.',
            'Common-skin junction topology is retained; this is not a separately segmented lumen.',
            'Unedited posterior arterial courses and remaining brain/vessel relationships need subsequent regional fitting.']}
    (APP/'docs/validation/vessel-fitting-v0.9.17.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({'batches':len(changes),'changedNodes':len(geometry),'maximumDisplacementMm':max(r['maximumDisplacementMm'] for r in geometry)},indent=2))

if __name__=='__main__':main()
