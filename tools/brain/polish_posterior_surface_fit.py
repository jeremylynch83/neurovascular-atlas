"""Final smooth basilar seating and explicit anterior venous wall exclusion.

The original smooth basilar trunk is sheared with a bounded slope. Surface
veins and their adjoining material points receive the same local correction.
"""
import argparse,json,shutil
import numpy as np,trimesh
from scipy.interpolate import PchipInterpolator
from scipy.ndimage import gaussian_filter1d,maximum_filter1d
from scipy.spatial import cKDTree
from fit_vessels import APP,read_glb,mesh_records,smoothstep,curve_from_mesh
from seat_posterior_candidate import locator,front_fn
from refine_context_skin import save_replaced
from reconcile_brainstem import sha,ANTERIOR,TRANSVERSE

def main():
    p=argparse.ArgumentParser();p.add_argument('--input',default='.authoring/posterior-seated49');p.add_argument('--output',default='.authoring/posterior-seated50');a=p.parse_args();src=APP/a.input;out=APP/a.output;out.mkdir(exist_ok=True)
    # Restore the same modest cerebellar contraction used in candidate40.
    d,b=read_glb(src/'brain-trial.glb');rr=mesh_records(d,b);manifest=json.loads((APP/'.authoring/brainstem19/manifest-baseline.json').read_text());keys={r['id'] for r in manifest['structures'] if r.get('anatomy',{}).get('category') in ['brainstem','cerebellum']}|{'brain.fourth-ventricle','brain.aqueduct-of-midbrain'};targets={}
    for k,r in rr.items():
        if k not in keys:continue
        v=r['old'];w=(1-smoothstep((v[:,1]+88)/18))*(1-smoothstep((v[:,2]-80)/12));q=v+.04*w[:,None]*(np.array([.65,-110.,54.])-v);m=trimesh.Trimesh(q,r['faces'],process=False);targets[k]=(q,r['faces'],m.vertex_normals)
    save_replaced(out/'brain-trial.glb',d,b,targets);del d,b,rr
    brain=trimesh.load(out/'brain-trial.glb',process=False);stem=trimesh.util.concatenate([m for k,m in brain.geometry.items() if any(t in k for t in ['pons.','midbrain.','medulla-oblongata','base-of-peduncle'])]);l=locator(stem);front=front_fn(l)
    d,b=read_glb(src/'arteries-trial.glb');rr=mesh_records(d,b);r=rr['Basilar'];v=r['old'];grid=np.arange(41.,81.01,.25);bins=np.clip(np.floor((v[:,2]-grid[0])/.25).astype(int),0,len(grid)-1);demand=np.full(len(grid),-np.inf)
    for wall,j in zip(v,bins):
        y=front(wall[0],wall[2])
        if y is not None:demand[j]=max(demand[j],y+.10-wall[1])
    good=np.isfinite(demand);demand=np.interp(grid,grid[good],demand[good]);demand=maximum_filter1d(demand,3)
    # A conservative Lipschitz envelope avoids local kinks and skin collapse.
    delta=np.max(demand[None,:]-.35*abs(grid[:,None]-grid[None,:]),axis=1);delta=gaussian_filter1d(delta,1.5);delta=np.maximum(delta,demand)
    zz=np.r_[grid[0]-10,grid,grid[-1]+10];fn=PchipInterpolator(zz,np.r_[0,delta,0]);c=curve_from_mesh(trimesh.Trimesh(v,r['faces'],process=False),axis=2,n=120);cy=PchipInterpolator(c[:,2],c[:,1]);targets={}
    posterior=lambda k:k=='Basilar' or any(k.startswith(t) for t in ['Vertebral V4','PCA ','SCA ','AICA ','PICA ','Pontine ','Anterior spinal','Posterior spinal','VA medullary','Thalamoperforator','Thalamogeniculate','Peduncular perforator','Medial posterior choroidal','Lateral posterior choroidal','Labyrinthine','Common cochlear','Anterior vestibular'])
    for k,r in rr.items():
        if not posterior(k):continue
        v=r['old'];z=np.clip(v[:,2],zz[0],zz[-1]);w=(1-smoothstep((abs(v[:,0]-.65)-4)/8))*(1-smoothstep((abs(v[:,1]-cy(np.clip(z,c[0,2],c[-1,2])))-4)/8));q=v.copy();q[:,1]+=fn(z)*w*(v[:,2]>zz[0])*(v[:,2]<zz[-1]);m=trimesh.Trimesh(q,r['faces'],process=False);targets[k]=(q,r['faces'],m.vertex_normals)
    save_replaced(out/'arteries-trial.glb',d,b,targets);del d,b,rr
    d,b=read_glb(src/'veins-trial.glb');rr=mesh_records(d,b);keys=set(ANTERIOR+TRANSVERSE+['vein.anterior_spinal']);targets={}
    # Correct residual anterior wall penetration, including labelled joins.
    seed=[]
    for k in keys:
        for v in rr[k]['old']:
            y=front(v[0],v[2])
            if y is not None and v[1]<y+.10:seed.append(v)
    near=cKDTree(np.array(seed)) if seed else None
    for k,r in rr.items():
        if k=='vein.basilar_plexus':continue
        v=r['old'];q=v.copy();mask=np.ones(len(v),bool) if k in keys else near.query(v)[0]<1. if near else np.zeros(len(v),bool)
        for i in np.flatnonzero(mask):
            y=front(v[i,0],v[i,2])
            if y is not None:q[i,1]=max(v[i,1],y+.10)
        if np.max(abs(q-v))<1e-7:continue
        m=trimesh.Trimesh(q,r['faces'],process=False);targets[k]=(q,r['faces'],m.vertex_normals)
    save_replaced(out/'veins-trial.glb',d,b,targets)
    for kind in ['brain','veins','arteries']:shutil.copyfile(APP/'.authoring/posterior-family40'/f'{kind}-trial.glb',out/f'{kind}-source.glb')
    report={'parentDirectory':a.input,'comparisonParent':'.authoring/posterior-family40','requestedBaseAnteriorShiftMm':2.,'requestedWallSurfaceSeparationMm':.10,'basilarPlexusFixed':True,'accepted':False,'appliedToApp':False,'basilarShearRangeMm':[float(delta.min()),float(delta.max())],'hashes':{k:sha(out/f'{k}-trial.glb') for k in ['brain','veins','arteries']}}
    (out/'trial.json').write_text(json.dumps(report,indent=2)+'\n');print('Polished candidate',out,report['basilarShearRangeMm'],flush=True)

if __name__=='__main__':main()
