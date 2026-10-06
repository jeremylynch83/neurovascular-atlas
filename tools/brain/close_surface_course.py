"""Close residual near-wall gaps with whole-section coordinate shears.

This is a review refinement, not anatomical acceptance. No wall vertices are
individually clamped. The same physical field applies to adjoining labels.
"""
import json,shutil
import numpy as np,trimesh,vtk
from scipy.interpolate import PchipInterpolator
from scipy.ndimage import maximum_filter1d
from fit_vessels import APP,read_glb,mesh_records,curve_from_mesh,smoothstep
from seat_posterior_candidate import locator,front_fn
from refine_context_skin import save_replaced
from reconcile_brainstem import sha

def profile(points,lo,hi,query):
    grid=np.arange(lo,hi+.025,.05);demand=np.full(len(grid),-np.inf)
    for p in points:
        if not lo<=p[2]<=hi:continue
        amount=query(p)
        if amount is not None:
            i=int(np.clip(round((p[2]-lo)/.05),0,len(grid)-1));demand[i]=max(demand[i],amount)
    good=np.isfinite(demand);demand=np.interp(grid,grid[good],demand[good]);demand=maximum_filter1d(demand,3)
    return np.r_[lo-5,grid,hi+5],np.r_[0,demand,0]

def main():
    src=APP/'.authoring/posterior-surface52';out=APP/'.authoring/posterior-contact53';out.mkdir(exist_ok=True)
    for kind in ['brain','arteries','veins']:
        for state in ['source','trial']:shutil.copyfile(src/f'{kind}-{state}.glb',out/f'{kind}-{state}.glb')
    brain=trimesh.load(out/'brain-trial.glb',process=False);stem=trimesh.util.concatenate([m for k,m in brain.geometry.items() if any(t in k for t in ['pons.','midbrain.','medulla-oblongata','base-of-peduncle'])]);loc=locator(stem);front=front_fn(loc);records=[]
    d,b=read_glb(src/'arteries-trial.glb');rr=mesh_records(d,b);r=rr['Basilar'];v=r['old'];points=np.vstack([v,v[r['faces']].mean(1)])
    def anterior(p):
        y=front(p[0],p[2]);return y-p[1]+1e-4 if y is not None else None
    z,delta=profile(points,41.5,79.,anterior);fn=PchipInterpolator(z,delta);c=curve_from_mesh(trimesh.Trimesh(v,r['faces'],process=False),axis=2,n=150);cy=PchipInterpolator(c[:,2],c[:,1]);targets={}
    for k,r in rr.items():
        v=r['old'];zz=np.clip(v[:,2],z[0],z[-1]);w=(1-smoothstep((abs(v[:,0]-.65)-4)/8))*(1-smoothstep((abs(v[:,1]-cy(np.clip(zz,c[0,2],c[-1,2])))-4)/8));q=v.copy();q[:,1]+=fn(zz)*w*(v[:,2]>z[0])*(v[:,2]<z[-1])
        if np.max(abs(q-v))<1e-7:continue
        m=trimesh.Trimesh(q,r['faces'],process=False);targets[k]=(q,r['faces'],m.vertex_normals)
    save_replaced(out/'arteries-trial.glb',d,b,targets);records.append({'node':'Basilar','shiftRangeMm':[float(delta.min()),float(delta.max())]});np.savez_compressed(out/'basilar-contact-profile.npz',z=z,delta=delta)
    del d,b,rr
    d,b=read_glb(src/'veins-trial.glb');rr=mesh_records(d,b);fields=[]
    for sign,side in [(-1,'left'),(1,'right')]:
        key='vein.lateral_mesencephalic.'+side;r=rr[key];v=r['old'];points=np.vstack([v,v[r['faces']].mean(1)])
        def lateral(p):
            t=vtk.reference(0.);q=[0.,0.,0.];pc=[0.,0.,0.];sub=vtk.reference(0);cell=vtk.reference(0)
            if loc.IntersectWithLine([.65+sign*100,p[1],p[2]],[.65,p[1],p[2]],1e-8,t,q,pc,sub,cell):return sign*(q[0]-p[0])+1e-4
        z,delta=profile(points,46.,77.,lateral);c=curve_from_mesh(trimesh.Trimesh(v,r['faces'],process=False),axis=2,n=150);fields.append((sign,z,PchipInterpolator(z,delta),PchipInterpolator(c[:,2],c[:,0]),PchipInterpolator(c[:,2],c[:,1]),c[0,2],c[-1,2]));records.append({'node':key,'shiftRangeMm':[float(delta.min()),float(delta.max())]});np.savez_compressed(out/f'{side}-contact-profile.npz',z=z,delta=delta)
    targets={}
    for k,r in rr.items():
        if k=='vein.basilar_plexus':continue
        v=r['old'];q=v.copy()
        for sign,z,fn,cx,cy,lo,hi in fields:
            zz=np.clip(v[:,2],lo,hi);w=smoothstep(((v[:,0]-.65)*sign-3)/5)*(1-smoothstep((abs(v[:,0]-cx(zz))-2)/4))*(1-smoothstep((abs(v[:,1]-cy(zz))-2)/4));q[:,0]+=sign*fn(np.clip(v[:,2],z[0],z[-1]))*w*(v[:,2]>z[0])*(v[:,2]<z[-1])
        if np.max(abs(q-v))<1e-7:continue
        m=trimesh.Trimesh(q,r['faces'],process=False);targets[k]=(q,r['faces'],m.vertex_normals)
    save_replaced(out/'veins-trial.glb',d,b,targets)
    report=json.loads((src/'trial.json').read_text());report.update({'contactRefinementParent':str(src.relative_to(APP)),'contactRefinement':records,'requestedWallSurfaceSeparationMm':0.,'accepted':False,'hashes':{k:sha(out/f'{k}-trial.glb') for k in ['brain','arteries','veins']}});(out/'trial.json').write_text(json.dumps(report,indent=2)+'\n');shutil.copyfile(src/'solver.json',out/'solver.json');print(records,flush=True)

if __name__=='__main__':main()
