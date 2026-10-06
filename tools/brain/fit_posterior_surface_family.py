"""Review-only surface fitting with transported original vessel sections.

Both asset families use the same brainstem target. Shared source boundaries
receive one common displacement. Original wall offsets rotate with the course
in free sections; boundary collars retain the common displacement instead.
"""
import argparse,json,shutil
import numpy as np,trimesh,vtk
from scipy.interpolate import PchipInterpolator
from scipy.ndimage import gaussian_filter1d,maximum_filter1d
from scipy.spatial import cKDTree
from fit_vessels import APP,read_glb,mesh_records,curve_from_mesh,smoothstep,neighbours
from build_targets import poly
from reconcile_brainstem import ANTERIOR,TRANSVERSE,LATERAL,sha
from refine_context_skin import save_replaced,subdivide

def locator(m):
    l=vtk.vtkStaticCellLocator();l.SetDataSet(poly(m));l.BuildLocator();return l

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--brain-directory',default='.authoring/posterior-context27');parser.add_argument('--output-directory',default='.authoring/posterior-family27');parser.add_argument('--retain-arteries',action='store_true');args=parser.parse_args()
    work=APP/args.output_directory;work.mkdir(parents=True,exist_ok=True)
    brain_path=APP/args.brain_directory/'brain-trial.glb';brain=trimesh.load(brain_path,process=False)
    shutil.copyfile(brain_path,work/'brain-trial.glb')
    stem=trimesh.util.concatenate([m for k,m in brain.geometry.items() if any(t in k for t in ['pons.','medulla-oblongata','midbrain.','base-of-peduncle'])]);loc=locator(stem)
    cache={}
    def hit(a,b):
        t=vtk.reference(0.);q=[0.,0.,0.];pc=[0.,0.,0.];sub=vtk.reference(0);cell=vtk.reference(0)
        return np.array(q) if loc.IntersectWithLine(a,b,1e-8,t,q,pc,sub,cell) else None
    def front(x,z):
        key=(round(float(x),4),round(float(z),4))
        if key not in cache:cache[key]=hit([x,5,z],[x,-145,z])
        return cache[key]
    vein_d,vein_b=read_glb(APP/'.authoring/brainstem19/veins-baseline.glb');vr=mesh_records(vein_d,vein_b)
    anterior=np.concatenate([curve_from_mesh(trimesh.Trimesh(vr[k]['old'],vr[k]['faces'],process=False),axis=2,n=90) for k in ANTERIOR+['vein.anterior_spinal']])
    anterior=anterior[np.argsort(anterior[:,2])];_,index=np.unique(np.round(anterior[:,2],5),return_index=True);anterior=anterior[index]
    old_y=PchipInterpolator(anterior[:,2],anterior[:,1],extrapolate=True)
    zz=np.arange(-25.,94.,.25);shift=[]
    for z in zz:
        q=front(3.,z);shift.append(0 if q is None else q[1]+1.6-float(old_y(z)))
    shift=gaussian_filter1d(np.clip(shift,-15,20),3)
    shift*=smoothstep((zz-9)/12)*(1-smoothstep((zz-72)/6))
    shift_fn=PchipInterpolator(zz,shift)
    side_profiles={};source_side={}
    for sign in [-1,1]:
        target=[]
        for z in zz:
            f=front(.65,z);b=hit([.65,-145,z],[.65,5,z])
            y=-78 if f is None or b is None else b[1]+.55*(f[1]-b[1])
            q=hit([sign*100,y,z],[.65,y,z])
            target.append([.65+sign*20,y] if q is None else [q[0]+sign*1.5,y])
        side_profiles[sign]=PchipInterpolator(zz,gaussian_filter1d(np.array(target),2,axis=0),axis=0)
        side='right' if sign==1 else 'left'
        curves=[]
        for key in ['vein.cerebellopontine_fissure.'+side,'vein.lateral_mesencephalic.'+side]:
            m=trimesh.Trimesh(vr[key]['old'],vr[key]['faces'],process=False)
            curves.append(curve_from_mesh(m,axis=2,n=120))
        c=np.concatenate(curves);c=c[np.argsort(c[:,2])];_,ii=np.unique(np.round(c[:,2],5),return_index=True);c=c[ii]
        source_side[sign]=PchipInterpolator(c[:,2],c[:,[0,1]],axis=0,extrapolate=True)
    def common_vein(p):
        q=p.copy();z=np.clip(p[:,2],zz[0],zz[-1]);tx=abs(p[:,0]-.65)
        w=smoothstep((tx-9)/13);active=smoothstep((z-30)/10)*(1-smoothstep((z-80)/9))
        dy=shift_fn(z)
        for sign in [-1,1]:
            mask=(p[:,0]-.65)*sign>=0;target=side_profiles[sign](z[mask]);original=source_side[sign](np.clip(z[mask],44,87));wall=p[mask]
            # Side routes approach the lateral brainstem, including the
            # cerebellopontine transition, then rejoin fixed collectors.
            side_w=w[mask]*active[mask]*(1-smoothstep((wall[:,1]+88)/30))
            dx=target[:,0]-original[:,0]
            q[mask,0]+=dx*side_w
            q[mask,1]+=dy[mask]*(1-side_w)*(1-smoothstep((tx[mask]-16)/10))+side_w*(target[:,1]-original[:,1])
        low=tx<9;q[low,1]=p[low,1]+dy[low]
        return q
    selected=set(ANTERIOR+TRANSVERSE+LATERAL+['vein.anterior_spinal']+[f'vein.{k}.{s}' for k in ['superior_petrosal_vein','cerebellopontine_fissure','basal'] for s in ['left','right']])
    stage('veins',vein_d,vein_b,vr,selected,common_vein,work)
    del vein_d,vein_b,vr
    if args.retain_arteries:
        src=APP/'.authoring/brainstem19/arteries-baseline.glb'
        for name in ['arteries-source.glb','arteries-trial.glb']:shutil.copyfile(src,work/name)
        (work/'arteries-fit.json').write_text(json.dumps({'sourceSha256':sha(src),'trialSha256':sha(src),'selected':[],'changes':[],'appliedToApp':False},indent=2)+'\n')
        (work/'trial.json').write_text(json.dumps({'brainSha256':sha(work/'brain-trial.glb'),'veinsSha256':sha(work/'veins-trial.glb'),'arteriesSha256':sha(src),'arteriesRetainedExactly':True,'accepted':False,'appliedToApp':False},indent=2)+'\n')
        return
    ad,ab=read_glb(APP/'.authoring/brainstem19/arteries-baseline.glb');ar=mesh_records(ad,ab)
    selected=neighbours(ar,{'Basilar'})
    basilar=trimesh.Trimesh(ar['Basilar']['old'],ar['Basilar']['faces'],process=False)
    curve=curve_from_mesh(basilar,axis=2,n=150);centre=PchipInterpolator(curve[:,2],curve[:,1],extrapolate=True)
    p=basilar.vertices;demand=[]
    for v in p:
        q=front(v[0],v[2]);demand.append(-20 if q is None else q[1]+.5-v[1])
    grid=np.arange(35.,85.,.25);amount=np.full(len(grid),-20.)
    ids=np.clip(np.floor((p[:,2]-grid[0])/.25).astype(int),0,len(grid)-1)
    np.maximum.at(amount,ids,np.array(demand))
    amount=maximum_filter1d(amount,9);amount=gaussian_filter1d(amount,2)
    amount=np.maximum(amount,0);amount*=smoothstep((grid-39)/6)*(1-smoothstep((grid-81)/3))
    shift=PchipInterpolator(grid,amount,extrapolate=False)
    def common_artery(p):
        q=p.copy();z=np.clip(p[:,2],grid[0],grid[-1]);axis_y=centre(z)
        w=(1-smoothstep((abs(p[:,0]-.65)-5)/20))*(1-smoothstep((abs(p[:,1]-axis_y)-4)/18))
        q[:,1]+=shift(z)*w;return q
    stage('arteries',ad,ab,ar,selected,common_artery,work)
    report={'method':'surface-directed course transport; original material wall sections rotate with course; common joined collars','brainSha256':sha(work/'brain-trial.glb'),'veinsSha256':sha(work/'veins-trial.glb'),'arteriesSha256':sha(work/'arteries-trial.glb'),'appliedToApp':False,'accepted':False,'requiresIndependentValidation':True}
    (work/'trial.json').write_text(json.dumps(report,indent=2)+'\n')

def stage(kind,d,b,records,selected,field,work):
    outside=np.concatenate([r['old'] for k,r in records.items() if k not in selected]);outer=cKDTree(outside)
    fixed=np.concatenate([r['old'][outer.query(r['old'])[0]<1e-5] for k,r in records.items() if k in selected]);fixed_tree=cKDTree(fixed)
    source=subdivide(records,selected,.6);targets={};before={};rows=[]
    for k,(p,f) in source.items():
        mesh=trimesh.Trimesh(p,f,process=False)
        axis=0 if k in TRANSVERSE else 2
        curve=curve_from_mesh(trimesh.Trimesh(records[k]['old'],records[k]['faces'],process=False),axis=axis,n=120)
        t=curve[:,axis];unique=np.r_[True,np.diff(t)>1e-6];curve=curve[unique];t=t[unique]
        c=PchipInterpolator(t,curve,axis=0);mapped=field(curve)
        pin=smoothstep(fixed_tree.query(curve)[0]/(4 if kind=='arteries' else 7))
        mapped=curve+(mapped-curve)*pin[:,None]
        n=PchipInterpolator(t,mapped,axis=0);station=np.clip(p[:,axis],t[0],t[-1])
        old_t=c.derivative()(station);new_t=n.derivative()(station)
        old_t/=np.maximum(np.linalg.norm(old_t,axis=1)[:,None],1e-9);new_t/=np.maximum(np.linalg.norm(new_t,axis=1)[:,None],1e-9)
        v=np.cross(old_t,new_t);dot=np.sum(old_t*new_t,axis=1);offset=p-c(station)
        rotated=offset+np.cross(v,offset)+np.cross(v,np.cross(v,offset))/np.maximum(1+dot,1e-5)[:,None]
        q=n(station)+rotated
        # Every original shared junction uses the same field. A short collar
        # blends smoothly back into course-frame transport away from joins.
        others=cKDTree(np.concatenate([r['old'] for key,r in records.items() if key!=k]))
        shared=records[k]['old'][others.query(records[k]['old'])[0]<1e-5]
        common=field(p);pin=smoothstep(fixed_tree.query(p)[0]/(4 if kind=='arteries' else 7));common=p+(common-p)*pin[:,None]
        if len(shared):
            w=smoothstep((cKDTree(shared).query(p)[0]-.15)/2.5)
            q=common+(q-common)*w[:,None]
        # Branching arterial courses are not single-valued in Z. Applying
        # a Z-based local frame to those branches can fold their skin. Keep
        # the shared AP transport for this family and validate its sections.
        # Use common material-point transport for the final combined trial.
        # Local course frames are retained above as diagnostic proposals;
        # they must not introduce skin folds at branching sections.
        q=common
        # External outlets remain exactly at their source coordinates.
        is_fixed=fixed_tree.query(p)[0]<1e-5;q[is_fixed]=p[is_fixed]
        target=trimesh.Trimesh(q,f,process=False)
        before[k]=(p,f,mesh.vertex_normals);targets[k]=(q,f,target.vertex_normals)
        rows.append({'node':k,'maximumDisplacementMm':float(np.linalg.norm(q-p,axis=1).max()),'sourceVertices':len(records[k]['old']),'materialVertices':len(p)})
        print('Course fitted',kind,k,rows[-1]['maximumDisplacementMm'],flush=True)
    # Refinement adds points on shared edges between the original junction
    # vertices. Reconcile every such labelled material point too, rather
    # than recognising only the original vertex list as the junction.
    names=sorted(before);pp=np.concatenate([before[k][0] for k in names]);qq=np.concatenate([targets[k][0] for k in names]);tags=np.concatenate([np.full(len(before[k][0]),i) for i,k in enumerate(names)])
    _,representative,inverse=np.unique(np.round(pp,5),axis=0,return_index=True,return_inverse=True)
    low=np.full(len(representative),len(names));high=np.full(len(representative),-1)
    np.minimum.at(low,inverse,tags);np.maximum.at(high,inverse,tags);joined=low!=high
    selected_groups=np.flatnonzero(joined);points=pp[representative[selected_groups]]
    pin=smoothstep(fixed_tree.query(points)[0]/(4 if kind=='arteries' else 7));common=points+(field(points)-points)*pin[:,None]
    values=np.zeros((len(representative),3));values[selected_groups]=common;qq[joined[inverse]]=values[inverse[joined[inverse]]]
    offset=0
    for k in names:
        p,f,n=before[k];q=qq[offset:offset+len(p)];offset+=len(p);mesh=trimesh.Trimesh(q,f,process=False);targets[k]=(q,f,mesh.vertex_normals)
    save_replaced(work/f'{kind}-source.glb',d,b,before);save_replaced(work/f'{kind}-trial.glb',d,b,targets)
    (work/f'{kind}-fit.json').write_text(json.dumps({'sourceSha256':sha(work/f'{kind}-source.glb'),'trialSha256':sha(work/f'{kind}-trial.glb'),'selected':sorted(selected),'changes':rows,'appliedToApp':False},indent=2)+'\n')

if __name__=='__main__':main()
