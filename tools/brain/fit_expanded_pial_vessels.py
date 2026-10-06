"""Surface-course correction of candidate 55, preserving whole vessel sections.

Uses geodesic station contours of the delivered labelled wall, not a world-axis
section that would collapse arterial loops. Sections move in transported frames.
The six exposed-surface rays provide conservative sphere clearance. Intentional
penetrating branches receive parent-collar transport only. Production is untouched.
"""
import argparse,copy,json,shutil
import numpy as np,trimesh,vtk
from scipy.sparse import coo_matrix
from scipy.sparse.csgraph import dijkstra,connected_components
from scipy.spatial import cKDTree
from scipy.interpolate import PchipInterpolator
from scipy.ndimage import gaussian_filter1d,maximum_filter1d
from vtk.util.numpy_support import numpy_to_vtk,vtk_to_numpy
from fit_vessels import APP,read_glb,mesh_records,smoothstep
from build_targets import poly
from refine_context_skin import save_replaced
from seat_posterior_candidate import locator
from rebuild_tubular_brainstem_veins import frames,tube
from reconcile_brainstem import sha

SRC=APP/'.authoring/posterior-tubular55'
OUT=APP/'.authoring/posterior-pial56'

class ExposedSurface:
    def __init__(self,mesh):
        self.loc=locator(mesh);self.bounds=mesh.bounds;self.cache={}
        offsets=np.array([[x,y,z] for x in [-1,0,1] for y in [-1,0,1] for z in [-1,0,1] if x or y or z],float)
        self.offsets=offsets/np.linalg.norm(offsets,axis=1)[:,None]
    def hit(self,p,axis,sign):
        key=(axis,sign,*np.round(np.delete(p,axis),4))
        if key not in self.cache:
            start=p.copy();end=p.copy();start[axis]=self.bounds[1,axis]+30 if sign==1 else self.bounds[0,axis]-30
            end[axis]=self.bounds[0,axis]-1 if sign==1 else self.bounds[1,axis]+1
            t=vtk.reference(0.);q=[0.,0.,0.];pc=[0.,0.,0.];sub=vtk.reference(0);cell=vtk.reference(0)
            self.cache[key]=q[axis] if self.loc.IntersectWithLine(start,end,1e-8,t,q,pc,sub,cell) else None
        return self.cache[key]
    def escape(self,p,r,preferred=None):
        choices=[]
        for axis in range(3):
            for sign in [-1,1]:
                amount=0.
                for point in p+self.offsets*r:
                    hit=self.hit(point,axis,sign)
                    if hit is not None:amount=max(amount,sign*(hit-point[axis])+.045)
                penalty=0. if preferred is None else .15*(axis!=preferred[0] or sign!=preferred[1])
                choices.append((amount+penalty,amount,axis,sign))
        _,amount,axis,sign=min(choices)
        return amount,axis,sign

def stations(record):
    mesh=trimesh.Trimesh(record['old'],record['faces'],process=False)
    v=mesh.vertices;_,idx,inv=np.unique(np.round(v,5),axis=0,return_index=True,return_inverse=True)
    v=v[idx];f=inv[mesh.faces];m=trimesh.Trimesh(v,f,process=False)
    edges=m.edges_unique;weights=np.linalg.norm(v[edges[:,0]]-v[edges[:,1]],axis=1)
    graph=coo_matrix((np.r_[weights,weights],(np.r_[edges[:,0],edges[:,1]],np.r_[edges[:,1],edges[:,0]])),shape=(len(v),len(v))).tocsr()
    _,components=connected_components(graph,directed=False);largest=np.argmax(np.bincount(components));start=int(np.flatnonzero(components==largest)[0])
    d=dijkstra(graph,indices=start);valid=np.isfinite(d);a=int(np.argmax(np.where(valid,d,-1)));da=dijkstra(graph,indices=a);b=int(np.argmax(np.where(np.isfinite(da),da,-1)));db=dijkstra(graph,indices=b)
    scalar=np.zeros(len(v));scalar[valid]=(da[valid]-db[valid]+da[b])/2
    if not valid.all():
        nearest=cKDTree(v[valid]).query(v[~valid])[1];scalar[~valid]=scalar[valid][nearest]
    count=max(45,min(250,int(da[b]/.4)));tt=np.linspace(.12,max(.13,da[b]-.12),count)
    data=poly(trimesh.Trimesh(v,f[np.all(valid[f],axis=1)],process=False));sc=numpy_to_vtk(scalar);sc.SetName('arc');data.GetPointData().SetScalars(sc);contour=vtk.vtkContourFilter();contour.SetInputData(data);q=[]
    for station in tt:
        contour.SetValue(0,float(station));contour.Update();points=contour.GetOutput().GetPoints();assert points is not None
        points=vtk_to_numpy(points.GetData());q.append(points.mean(0))
    q=gaussian_filter1d(np.array(q),.7,axis=0)
    param=scalar[inv];sample=np.column_stack([np.interp(param,tt,q[:,i]) for i in range(3)])
    rad=np.linalg.norm(record['old']-sample,axis=1);bins=np.clip(np.searchsorted(tt,param),0,len(tt)-1);r=np.zeros(len(tt));np.maximum.at(r,bins,rad)
    r=maximum_filter1d(np.maximum(r,.12),5);r=np.maximum(r,gaussian_filter1d(r,1))
    return q,r,param,tt

def sample(q,tt,param):return np.column_stack([np.interp(param,tt,q[:,i]) for i in range(3)])

def transport(v,q,target,tt,param):
    old=frames(q);new=frames(target)
    def basis(f):
        t=sample(f[0],tt,param);t/=np.maximum(np.linalg.norm(t,axis=1)[:,None],1e-10)
        n=sample(f[1],tt,param);n-=t*np.sum(n*t,axis=1)[:,None];n/=np.maximum(np.linalg.norm(n,axis=1)[:,None],1e-10)
        return np.stack([t,n,np.cross(t,n)],axis=2)
    sf,tf=basis(old),basis(new);local=np.einsum('nji,nj->ni',sf,v-sample(q,tt,param))
    return sample(target,tt,param)+np.einsum('nij,nj->ni',tf,local)

def fit_course(q,r,surface,iterations=8):
    target=q.copy();delta=np.zeros_like(q);directions=None
    for iteration in range(iterations):
        push=np.zeros_like(q);directions=[]
        for i,p in enumerate(target):
            amount,axis,sign=surface.escape(p,float(r[i]));push[i,axis]=sign*amount;directions.append((axis,sign))
        if np.linalg.norm(push,axis=1).max()<.005:break
        # Smooth the displacement, retaining the source loop and overall route.
        desired=delta+push;delta=gaussian_filter1d(desired,2.,axis=0)
        target=q+delta
        # A final conservative envelope adds no deformation of section walls.
        for i,p in enumerate(target):
            amount,axis,sign=surface.escape(p,float(r[i]),directions[i]);target[i,axis]+=sign*amount
        delta=target-q
    return target

def cord_mesh(brain):
    med=trimesh.util.concatenate([brain.geometry['brain.medulla-oblongata.'+s] for s in ['left','right']])
    contour=vtk.vtkCutter();plane=vtk.vtkPlane();plane.SetOrigin(0,0,13);plane.SetNormal(0,0,1);contour.SetCutFunction(plane);contour.SetInputData(poly(med));contour.Update()
    p=vtk_to_numpy(contour.GetOutput().GetPoints().GetData());centre=p.mean(0);xr=(p[:,0].max()-p[:,0].min())/2;yr=(p[:,1].max()-p[:,1].min())/2
    z=np.linspace(12.8,-34,96);theta=np.arange(64)*2*np.pi/64;blend=smoothstep((12.8-z)/15);xrad=xr*(1-blend)+6.2*blend;yrad=yr*(1-blend)+5.5*blend
    rings=np.stack([centre[0]+xrad[:,None]*np.cos(theta),centre[1]+yrad[:,None]*np.sin(theta),np.broadcast_to(z[:,None],(len(z),64))],axis=2);v=rings.reshape(-1,3);f=[]
    for i in range(len(z)-1):
        for j in range(64):a=i*64+j;b=i*64+(j+1)%64;f.extend([[a,a+64,b],[b,a+64,b+64]])
    last=len(v);v=np.vstack([v,[centre[0],centre[1],z[0]],[centre[0],centre[1],z[-1]]])
    for j in range(64):f.extend([[last,j,(j+1)%64],[last+1,(len(z)-1)*64+(j+1)%64,(len(z)-1)*64+j]])
    m=trimesh.Trimesh(v,np.array(f),process=False);m.fix_normals();assert m.is_watertight
    return m,{'centre':centre.tolist(),'rostralRadii':[float(xr),float(yr)],'caudalRadii':[6.2,5.5],'zRange':[12.8,-34.],'provenance':'Illustrative upper-cervical continuation of the registered caudal medullary contour; not an imported cord segmentation.'}

def reconcile(records,changes):
    """Transport retained proximal collars and make every source seam identical."""
    # Parent-collar displacement is seeded by transformed shared material points.
    moving=[k for k in changes if np.linalg.norm(changes[k]-records[k]['old'],axis=1).max()>1e-5]
    if not moving:return
    points=np.concatenate([records[k]['old'] for k in moving]);targets=np.concatenate([changes[k] for k in moving]);tree=cKDTree(points)
    for k,r in records.items():
        if k in changes:continue
        d,idx=tree.query(r['old']);shared=d<2e-5
        if not shared.any():continue
        seed=r['old'][shared];disp=targets[idx[shared]]-seed;near=cKDTree(seed);dd,j=near.query(r['old']);changes[k]=r['old']+disp[j]*(1-smoothstep(dd/4))[:,None]
    keys=list(changes);p=np.concatenate([records[k]['old'] for k in keys]);q=np.concatenate([changes[k] for k in keys]);_,idx,inv=np.unique(np.round(p,5),axis=0,return_index=True,return_inverse=True);count=np.bincount(inv);mean=np.zeros((len(idx),3));np.add.at(mean,inv,q);mean/=count[:,None];q=mean[inv];off=0
    for k in keys:n=len(records[k]['old']);changes[k]=q[off:off+n];off+=n

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--kind',choices=['arteries','veins','all'],default='all');args=parser.parse_args();OUT.mkdir(exist_ok=True)
    manifest=json.loads((APP/'public/anatomy/manifest.json').read_text());cb={r['id'] for r in manifest['structures'] if r.get('anatomy',{}).get('category')=='cerebellum'};keys=cb|{f'brain.{k}.{s}' for k in ['pons','midbrain','medulla-oblongata','base-of-peduncle'] for s in ['left','right']}
    brain=trimesh.load(SRC/'brain-trial.glb',process=False);cord,cord_info=cord_mesh(brain)
    d,b=read_glb(SRC/'brain-trial.glb');template=next(n for n in d['nodes'] if n.get('name')=='brain.medulla-oblongata.right');node=copy.deepcopy(template);node['name']='brain.upper-cervical-cord';node['mesh']=len(d['meshes']);d['meshes'].append(copy.deepcopy(d['meshes'][template['mesh']]));d['nodes'].append(node);d['meshes'][node['mesh']]['name']=node['name']
    save_replaced(OUT/'brain-trial.glb',d,b,{'brain.upper-cervical-cord':(cord.vertices,cord.faces,cord.vertex_normals)})
    (OUT/'cord-context.json').write_text(json.dumps(cord_info,indent=2)+'\n')
    tissue=trimesh.util.concatenate([brain.geometry[k] for k in keys]+[cord]);surface=ExposedSurface(tissue)
    metadata=json.loads((APP/'deliverables/posterior-fossa-expanded-review/model-review.json').read_text());baseline=json.loads((OUT/'baseline-contacts.json').read_text());contacts={(r['kind'],r['node']):r['triangleContacts'] for r in baseline};report={'parentDirectory':str(SRC.relative_to(APP)),'method':'geodesic wall stations, whole-section frame transport and reconciled shared skin seams','cordContext':cord_info,'accepted':False,'appliedToApp':False,'rows':[]}
    for kind in ['arteries','veins']:
        if args.kind not in [kind,'all']:continue
        d,b=read_glb(SRC/f'{kind}-trial.glb');rr=mesh_records(d,b);changes={};curves={}
        selected=metadata['groups']['arteries'] if kind=='arteries' else metadata['groups']['veins']+metadata['groups']['deep-veins']
        for k in selected:
            if kind=='arteries' and (any(s in k.lower() for s in ['perforator','paramedian']) or k=='Basilar' or k.startswith('Posterior spinal ')):continue
            if contacts.get((kind,k),0)==0:continue
            print('Fitting',kind,k,flush=True);q,r,param,tt=stations(rr[k]);target=fit_course(q,r,surface)
            changes[k]=transport(rr[k]['old'],q,target,tt,param);curves[k]={'sourcePoints':q.tolist(),'points':target.tolist(),'radii':r.tolist(),'stations':tt.tolist()}
            row={'kind':kind,'node':k,'maximumCourseMovementMm':float(np.linalg.norm(target-q,axis=1).max()),'baselineTriangleContacts':contacts[(kind,k)]};report['rows'].append(row);print(row,flush=True)
        reconcile(rr,changes)
        replacements={}
        for k,q in changes.items():
            m=trimesh.Trimesh(q,rr[k]['faces'],process=False);replacements[k]=(q,rr[k]['faces'],m.vertex_normals)
        save_replaced(OUT/f'{kind}-trial.glb',d,b,replacements)
        (OUT/f'{kind}-pial-courses.json').write_text(json.dumps(curves,separators=(',',':'))+'\n')
        (OUT/f'{kind}-changed-labels.json').write_text(json.dumps(list(changes),indent=2)+'\n')
        (OUT/f'{kind}-fitting.json').write_text(json.dumps(report,indent=2)+'\n')
    report['hashes']={k:sha(OUT/f'{k}-trial.glb') for k in ['brain','arteries','veins'] if (OUT/f'{k}-trial.glb').exists()};(OUT/'trial.json').write_text(json.dumps(report,indent=2)+'\n')

if __name__=='__main__':main()
