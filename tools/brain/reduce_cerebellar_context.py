"""Stage a cerebellar size reduction with a shared posterior stem transition."""
import argparse,json,shutil
import numpy as np,trimesh
from fit_vessels import APP,read_glb,mesh_records,smoothstep
from refine_context_skin import save_replaced
from reconcile_brainstem import sha

def main():
    p=argparse.ArgumentParser();p.add_argument('--brain-directory',default='.authoring/posterior-anchor26');p.add_argument('--output-directory',default='.authoring/posterior-context27');p.add_argument('--fraction',type=float,default=.08);a=p.parse_args()
    assert 0<a.fraction<.15
    src=APP/a.brain_directory;work=APP/a.output_directory;work.mkdir(parents=True,exist_ok=True)
    d,b=read_glb(src/'brain-trial.glb');records=mesh_records(d,b)
    manifest=json.loads((APP/'.authoring/brainstem19/manifest-baseline.json').read_text())
    selected={r['id'] for r in manifest['structures'] if r.get('anatomy',{}).get('category') in ['cerebellum','brainstem']}|{'brain.fourth-ventricle','brain.aqueduct-of-midbrain'}
    centre=np.array([.65,-110.,54.]);target={};changes=[]
    for k,r in records.items():
        if k not in selected:continue
        v,f=r['old'],r['faces']
        w=(1-smoothstep((v[:,1]+88)/18))*(1-smoothstep((v[:,2]-80)/12))
        q=v+a.fraction*w[:,None]*(centre-v)
        if np.linalg.norm(q-v,axis=1).max()<1e-5:continue
        aa=trimesh.Trimesh(v,f,process=False);bb=trimesh.Trimesh(q,f,process=False)
        target[k]=(q,f,bb.vertex_normals)
        changes.append({'node':k,'maximumDisplacementMm':float(np.linalg.norm(q-v,axis=1).max()),'closedSource':bool(aa.is_watertight),'closedCandidate':bool(bb.is_watertight),'volumeChangeFraction':float(abs(bb.volume)/abs(aa.volume)-1) if aa.is_watertight else None})
    save_replaced(work/'brain-trial.glb',d,b,target)
    shutil.copyfile(src/'brain-source.glb',work/'brain-source.glb')
    shutil.copyfile(src/'volume-map.npz',work/'volume-map.npz')
    report=json.loads((src/'registration.json').read_text());report['parentBrainSha256']=report['brainSha256'];report['brainSha256']=sha(work/'brain-trial.glb')
    report['cerebellarReduction']={'fraction':a.fraction,'centreMm':centre.tolist(),'method':'common contraction with anterior and superior transitions, on labelled posterior-fossa tissue','changes':changes}
    report['volumeMapDescribesOnlyParentAPReduction']=True
    report['appliedToApp']=False
    (work/'registration.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report['cerebellarReduction'],indent=2),flush=True)

if __name__=='__main__':main()
