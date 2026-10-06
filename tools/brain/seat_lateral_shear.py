"""Move whole lateral wall sections to the stem and preserve labelled joins."""
import argparse,json,shutil
import numpy as np,trimesh,vtk
from scipy.interpolate import PchipInterpolator
from scipy.ndimage import gaussian_filter1d
from fit_vessels import APP,read_glb,mesh_records,curve_from_mesh,smoothstep
from seat_posterior_candidate import locator
from refine_context_skin import save_replaced
from reconcile_brainstem import sha

def reconcile(path,source):
    d,b=read_glb(path);rr=mesh_records(d,b);sd,sb=read_glb(source);sr=mesh_records(sd,sb);names=list(rr)
    pp=np.concatenate([sr[k]['old'] for k in names]);qq=np.concatenate([rr[k]['old'] for k in names]);_,rep,inv=np.unique(np.round(pp,5),axis=0,return_index=True,return_inverse=True);counts=np.bincount(inv);total=np.zeros((len(rep),3));np.add.at(total,inv,qq);total/=counts[:,None];qq[counts[inv]>1]=total[inv[counts[inv]>1]];offset=0;targets={}
    for k in names:
        r=rr[k];n=len(r['old']);q=qq[offset:offset+n];offset+=n
        if np.max(abs(q-r['old']))<1e-7:continue
        m=trimesh.Trimesh(q,r['faces'],process=False);targets[k]=(q,r['faces'],m.vertex_normals)
    save_replaced(path,d,b,targets)

def main():
    p=argparse.ArgumentParser();p.add_argument('--input',default='.authoring/posterior-shear51');p.add_argument('--output',default='.authoring/posterior-surface52');a=p.parse_args();src=APP/a.input;out=APP/a.output;out.mkdir(exist_ok=True)
    for k in ['brain','veins','arteries']:
        for s in ['source','trial']:shutil.copyfile(src/f'{k}-{s}.glb',out/f'{k}-{s}.glb')
    brain=trimesh.load(out/'brain-trial.glb',process=False);stem=trimesh.util.concatenate([m for k,m in brain.geometry.items() if any(t in k for t in ['pons.','midbrain.','medulla-oblongata','base-of-peduncle'])]);l=locator(stem)
    d,b=read_glb(out/'veins-trial.glb');rr=mesh_records(d,b);profiles=[]
    for sign,side in [(-1,'left'),(1,'right')]:
        r=rr['vein.lateral_mesencephalic.'+side];v=r['old'];c=curve_from_mesh(trimesh.Trimesh(v,r['faces'],process=False),axis=2,n=140);keep=np.r_[True,np.diff(c[:,2])>1e-5];c=c[keep];delta=[]
        for cp in c:
            local=v[abs(v[:,2]-cp[2])<.5];demand=[]
            if len(local) and 44<cp[2]<79:
                for wall in local:
                    t=vtk.reference(0.);q=[0.,0.,0.];pc=[0.,0.,0.];sub=vtk.reference(0);cell=vtk.reference(0)
                    if l.IntersectWithLine([.65+sign*100,wall[1],wall[2]],[.65,wall[1],wall[2]],1e-8,t,q,pc,sub,cell):demand.append(sign*(q[0]-wall[0])+.10)
            delta.append(np.clip(max(demand),-2.5,2.5) if demand else 0)
        delta=gaussian_filter1d(np.array(delta),2);profiles.append((sign,PchipInterpolator(c[:,2],c[:,0]),PchipInterpolator(c[:,2],c[:,1]),PchipInterpolator(c[:,2],delta),c[0,2],c[-1,2]))
    targets={}
    for k,r in rr.items():
        if k=='vein.basilar_plexus':continue
        v=r['old'];q=v.copy()
        for sign,cx,cy,amount,lo,hi in profiles:
            z=np.clip(v[:,2],lo,hi);side=smoothstep(((v[:,0]-.65)*sign-3)/5);w=side*smoothstep((v[:,2]-44)/5)*(1-smoothstep((v[:,2]-74)/6));w*=(1-smoothstep((abs(v[:,1]-cy(z))-2)/4))*(1-smoothstep((abs(v[:,0]-cx(z))-2)/4));q[:,0]+=sign*amount(z)*w
        if np.max(abs(q-v))<1e-7:continue
        m=trimesh.Trimesh(q,r['faces'],process=False);targets[k]=(q,r['faces'],m.vertex_normals)
    save_replaced(out/'veins-trial.glb',d,b,targets);reconcile(out/'arteries-trial.glb',out/'arteries-source.glb')
    report=json.loads((src/'trial.json').read_text());report.update({'lateralSectionsSeated':True,'comparisonParent':'.authoring/posterior-family40','accepted':False,'hashes':{k:sha(out/f'{k}-trial.glb') for k in ['brain','veins','arteries']}});(out/'trial.json').write_text(json.dumps(report,indent=2)+'\n');shutil.copyfile(src/'solver.json',out/'solver.json');print(out,flush=True)

if __name__=='__main__':main()
