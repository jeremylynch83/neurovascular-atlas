"""Seat the anterior and lateral vessel walls on the advanced stem candidate.

Pontine fullness consumes most of the old basilar gap; the basilar then seats
through a common AP field with all its labelled branches. Vein course sections
retain their wall offsets and coincident labelled joins are reconciled.
"""
import argparse,json,shutil
import numpy as np,trimesh,vtk
from scipy.interpolate import PchipInterpolator
from scipy.ndimage import gaussian_filter1d,maximum_filter1d
from scipy.spatial import cKDTree
from fit_vessels import APP,read_glb,mesh_records,curve_from_mesh,smoothstep
from build_targets import poly
from reconcile_brainstem import ANTERIOR,TRANSVERSE,LATERAL,sha
from refine_context_skin import save_replaced

def locator(mesh):
    l=vtk.vtkStaticCellLocator();l.SetDataSet(poly(mesh));l.BuildLocator();return l

def front_fn(l):
    cache={}
    def front(x,z):
        key=(round(float(x),5),round(float(z),5))
        if key not in cache:
            t=vtk.reference(0.);q=[0.,0.,0.];pc=[0.,0.,0.];sub=vtk.reference(0);cell=vtk.reference(0)
            cache[key]=q[1] if l.IntersectWithLine([x,5,z],[x,-145,z],1e-8,t,q,pc,sub,cell) else None
        return cache[key]
    return front

def main():
    p=argparse.ArgumentParser();p.add_argument('--input',default='.authoring/posterior-forward43');p.add_argument('--output',default='.authoring/posterior-seated44');p.add_argument('--veins-only',action='store_true');a=p.parse_args();src=APP/a.input;out=APP/a.output;out.mkdir(exist_ok=True)
    brain=trimesh.load(src/'brain-trial.glb',process=False);stem_keys={k for k in brain.geometry if any(t in k for t in ['pons.','midbrain.','medulla-oblongata','base-of-peduncle'])};stem=trimesh.util.concatenate([brain.geometry[k] for k in stem_keys]);l=locator(stem);front=front_fn(l)
    ad,ab=read_glb(src/'arteries-trial.glb');ar=mesh_records(ad,ab);ba=ar['Basilar']['old'];grid=np.arange(41.5,80.51,.25)
    bins=np.clip(np.floor((ba[:,2]-grid[0])/.25).astype(int),0,len(grid)-1);rear=np.full(len(grid),np.inf);np.minimum.at(rear,bins,ba[:,1]);good=np.isfinite(rear);rear=np.interp(grid,grid[good],rear[good]);rear=gaussian_filter1d(rear,1)
    f=[];b=[]
    for z in grid:
        pts=vtk.vtkPoints();ids=vtk.vtkIdList();l.IntersectWithLine([.65,-145,z],[.65,-30,z],1e-8,pts,ids);ys=[pts.GetPoint(j)[1] for j in range(pts.GetNumberOfPoints())]
        f.append(max(ys) if ys else -70);b.append(min(ys) if ys else -84)
    f=gaussian_filter1d(np.array(f),2);b=gaussian_filter1d(np.array(b),2)
    fuller=np.clip(.75*(rear-f-.06),0,4.5)*smoothstep((grid-43)/4)*(1-smoothstep((grid-73)/6));fuller=gaussian_filter1d(fuller,2)
    if a.veins_only:fuller[:]=0
    F=PchipInterpolator(grid,f);B=PchipInterpolator(grid,b);D=PchipInterpolator(grid,fuller)
    bd,bb=read_glb(src/'brain-trial.glb');br=mesh_records(bd,bb)
    manifest=json.loads((APP/'.authoring/brainstem19/manifest-baseline.json').read_text());selected={r['id'] for r in manifest['structures'] if r.get('anatomy',{}).get('category') in ['brainstem','cerebellum']}|{'brain.fourth-ventricle','brain.aqueduct-of-midbrain'}
    targets={}
    for k,r in br.items():
        if k not in selected:continue
        v=r['old'];z=np.clip(v[:,2],grid[0],grid[-1]);dep=smoothstep((v[:,1]-B(z))/np.maximum(F(z)-B(z),5.));w=1-smoothstep((abs(v[:,0]-.65)-13)/13)
        q=v.copy();q[:,1]+=D(z)*dep*w*(v[:,2]>=grid[0])*(v[:,2]<=grid[-1]);m=trimesh.Trimesh(q,r['faces'],process=False);targets[k]=(q,r['faces'],m.vertex_normals)
    save_replaced(out/'brain-trial.glb',bd,bb,targets)
    del bd,bb,br,brain,stem
    brain=trimesh.load(out/'brain-trial.glb',process=False);stem=trimesh.util.concatenate([brain.geometry[k] for k in stem_keys]);l=locator(stem);front=front_fn(l)
    # Minimum AP shear needed for every exported basilar wall point to stay
    # outside the new anterior surface, including its naturally open ostia.
    demand=np.full(len(grid),-np.inf)
    for v,j in zip(ba,bins):
        y=front(v[0],v[2])
        if y is not None:demand[j]=max(demand[j],y+.06-v[1])
    good=np.isfinite(demand);demand=np.interp(grid,grid[good],demand[good]);demand=maximum_filter1d(demand,3);s=gaussian_filter1d(demand,1);demand=np.maximum(s,demand)
    extgrid=np.r_[grid[0]-5,grid,grid[-1]+5];extdelta=np.r_[0,demand,0];A=PchipInterpolator(extgrid,extdelta)
    curve=curve_from_mesh(trimesh.Trimesh(ba,ar['Basilar']['faces'],process=False),axis=2,n=160);CY=PchipInterpolator(curve[:,2],curve[:,1]);targets={}
    for k,r in ar.items():
        v=r['old'];z=np.clip(v[:,2],extgrid[0],extgrid[-1]);y=CY(np.clip(z,curve[0,2],curve[-1,2]));w=(1-smoothstep((abs(v[:,0]-.65)-4)/8))*(1-smoothstep((abs(v[:,1]-y)-4)/8));q=v.copy();q[:,1]+=A(z)*w*(v[:,2]>extgrid[0])*(v[:,2]<extgrid[-1])
        if np.max(abs(q-v))<1e-7:continue
        m=trimesh.Trimesh(q,r['faces'],process=False);targets[k]=(q,r['faces'],m.vertex_normals)
    if a.veins_only:shutil.copyfile(src/'arteries-trial.glb',out/'arteries-trial.glb')
    else:save_replaced(out/'arteries-trial.glb',ad,ab,targets)
    del ad,ab,ar
    vd,vb=read_glb(src/'veins-trial.glb');vr=mesh_records(vd,vb)
    keys=set(ANTERIOR+TRANSVERSE+LATERAL+['vein.anterior_spinal']+[f'vein.cerebellopontine_fissure.{s}' for s in ['left','right']]);fixed=[]
    outer=cKDTree(np.concatenate([r['old'] for k,r in vr.items() if k not in keys]))
    for k in keys:fixed.extend(vr[k]['old'][outer.query(vr[k]['old'])[0]<2e-5])
    frozen=cKDTree(np.array(fixed));targets={};fit_rows=[]
    for k in sorted(keys):
        r=vr[k];v=r['old'];axis=0 if k in TRANSVERSE or 'pontomedullary.' in k else 2;old=trimesh.Trimesh(v,r['faces'],process=False);c=curve_from_mesh(old,axis=axis,n=150);tt=c[:,axis];keep=np.r_[True,np.diff(tt)>1e-5];c=c[keep];tt=tt[keep];displacements=[]
        for j,cp in enumerate(c):
            width=max(.5,(tt[-1]-tt[0])/100);local=v[abs(v[:,axis]-cp[axis])<width]
            if not len(local):local=v[np.argsort(abs(v[:,axis]-cp[axis]))[:12]]
            if k in ANTERIOR or k=='vein.anterior_spinal':
                values=[]
                for wall in local:
                    y=front(wall[0],wall[2])
                    if y is not None:values.append(y+.06-wall[1])
                delta=np.array([0,max(values),0]) if values else np.zeros(3)
            else:
                hit=[0.,0.,0.];cell,sub,d=vtk.reference(0),vtk.reference(0),vtk.reference(0.);l.FindClosestPoint(cp,hit,cell,sub,d);hit=np.array(hit);normal=cp-hit
                if np.linalg.norm(normal)<1e-6:normal=np.array([np.sign(cp[0]-.65),0,0])
                normal/=max(np.linalg.norm(normal),1e-8);radius=max(.2,-np.quantile((local-cp)@normal,.02));delta=hit+normal*(radius+.06)-cp
            # Surface courses leave the stem at their collecting outlets.
            # Do not drag those free collector sections back onto the tissue.
            active=smoothstep((cp[2]-18)/8)*(1-smoothstep((cp[2]-74)/7))
            if k in LATERAL or 'cerebellopontine_fissure.' in k:active*=smoothstep((cp[2]-40)/6)
            displacements.append(np.clip(delta,-5,5)*active)
        displacements=np.array(displacements);displacements=gaussian_filter1d(displacements,.6,axis=0);fn=PchipInterpolator(tt,displacements,axis=0);station=np.clip(v[:,axis],tt[0],tt[-1]);delta=fn(station)
        # Fixed dural collector attachments retain their exact material points.
        pin=smoothstep(frozen.query(v)[0]/2.);q=v+delta*pin[:,None];q[frozen.query(v)[0]<2e-5]=v[frozen.query(v)[0]<2e-5]
        targets[k]=(q,r['faces'],None);fit_rows.append({'node':k,'maximumAdditionalCourseDisplacementMm':float(np.linalg.norm(q-v,axis=1).max())});print('Surface seated',k,flush=True)
    # Reconcile every coincident skin junction, including refined edge points.
    names=sorted(targets);pp=np.concatenate([vr[k]['old'] for k in names]);qq=np.concatenate([targets[k][0] for k in names]);_,rep,inv=np.unique(np.round(pp,5),axis=0,return_index=True,return_inverse=True);counts=np.bincount(inv);common=np.zeros((len(rep),3));np.add.at(common,inv,qq);common/=counts[:,None];qq=common[inv];offset=0
    for k in names:
        n=len(vr[k]['old']);q=qq[offset:offset+n];offset+=n;m=trimesh.Trimesh(q,vr[k]['faces'],process=False);targets[k]=(q,vr[k]['faces'],m.vertex_normals)
    save_replaced(out/'veins-trial.glb',vd,vb,targets)
    # Incremental source remains candidate40 for the complete requested edit.
    for kind in ['brain','veins','arteries']:shutil.copyfile(APP/'.authoring/posterior-family40'/f'{kind}-trial.glb',out/f'{kind}-source.glb')
    report={'parentForwardDirectory':a.input,'comparisonParent':'.authoring/posterior-family40','requestedWallSurfaceSeparationMm':.06,'pontineFrontRestorationMaximumMm':float(fuller.max()),'veinSurfaceFits':fit_rows,'basilarPlexusFixed':True,'accepted':False,'appliedToApp':False,'hashes':{k:sha(out/f'{k}-trial.glb') for k in ['brain','veins','arteries']}}
    (out/'trial.json').write_text(json.dumps(report,indent=2)+'\n');print('Staged wall-contact candidate',out,flush=True)

if __name__=='__main__':main()
