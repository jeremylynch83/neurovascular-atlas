"""Build a portable comparison to candidate40, including skull-base context."""
import argparse,json,shutil
import numpy as np,trimesh
from fit_vessels import APP
from package_posterior_model_review import subset
from reconcile_brainstem import ANTERIOR,TRANSVERSE,LATERAL,sha

def main():
    p=argparse.ArgumentParser();p.add_argument('--directory',default='.authoring/posterior-forward42');p.add_argument('--output',default='deliverables/posterior-fossa-forward-review');a=p.parse_args();w=APP/a.directory
    out=APP/a.output;out.mkdir(exist_ok=True);models=out/'models';models.mkdir(exist_ok=True)
    manifest=json.loads((APP/'.authoring/brainstem19/manifest-baseline.json').read_text())
    cb={r['id'] for r in manifest['structures'] if r.get('anatomy',{}).get('category')=='cerebellum'}
    bk=cb|{f'brain.{k}.{s}' for k in ['pons','medulla-oblongata','midbrain','base-of-peduncle'] for s in ['left','right']}
    vk=set(ANTERIOR+TRANSVERSE+LATERAL+['vein.anterior_spinal','vein.basilar_plexus','vein.posterior_communicating']+[f'vein.{k}.{s}' for k in ['superior_petrosal_vein','cerebellopontine_fissure'] for s in ['left','right']])
    for kind,keys in [('brain',bk),('veins',vk),('arteries',{'Basilar'})]:
        for source,name in [('source','current'),('trial','trial')]:subset(w/f'{kind}-{source}.glb',models/f'{name}-{kind}.glb',keys)
    bone=trimesh.load(APP/'.authoring/bones-baseline.glb',process=False);parts={}
    for k,m in bone.geometry.items():
        if k not in ['bone.occipital','bone.sphenoid','bone.temporal.right','bone.temporal.left']:continue
        tri=m.vertices[m.faces];keep=np.all(tri.max(1)>[-40,-129,16],axis=1)&np.all(tri.min(1)<[41,-34,94],axis=1)
        parts[k]=trimesh.Trimesh(m.vertices,m.faces[keep],process=False)
    trimesh.Scene(parts).export(str(models/'skull-base.glb'))
    previous=APP/'deliverables/posterior-fossa-model-review'
    shutil.copytree(previous/'js',out/'js',dirs_exist_ok=True)
    for n in ['SOURCE-ATTRIBUTION.txt','Z_Anatomy_Source_Licence.txt','THREE-LICENSE.txt','serve.py','view.sh']:shutil.copyfile(previous/n,out/n)
    shutil.copyfile(APP/'tools/forward-review-viewer.html',out/'index.html')
    shutil.copyfile(w/'forward-validation.json',out/'forward-validation.json');shutil.copyfile(w/'trial.json',out/'trial.json')
    shutil.copyfile(APP/'.authoring/posterior-family40/combined-acceptance.json',out/'parent-acceptance.json')
    metadata={'cerebellarLabels':sorted(cb),'candidateDirectory':a.directory,'productionGeometryChanged':False,'status':'review candidate, full anatomy not accepted','modelHashes':{f.name:sha(f) for f in models.glob('*.glb')}}
    (out/'model-review.json').write_text(json.dumps(metadata,indent=2)+'\n')
    (out/'README.txt').write_text('POSTERIOR FOSSA FORWARD REVIEW\n\nRun python3 serve.py and open http://127.0.0.1:9844/. No internet or npm installation required.\n\nMatched comparison: previous candidate40 versus the revised anterior-shift candidate. The common movement field advances the brainstem, basilar and related vessels, adds gentle pontine convexity, and keeps the basilar plexus and external attachments stationary. Movement is limited near bone. The cerebellum receives only the local transition into this field, not another global size reduction.\n\nGrey skull-base surfaces are cropped for local context and shown as a right sagittal cutaway. The basilar is a filtered trunk; branch ostia remain visible and arterial branches are omitted from the review display. Full arteries are retained in the separate authoring checkpoint.\n\nThis is a candidate, not an app release. Focused incremental validation is in forward-validation.json; it does not clear the pre-existing failures in parent-acceptance.json.\n\nBrain source attribution: BodyParts3D / Database Center for Life Science, CC BY-SA 2.1 Japan; Z-Anatomy, CC BY-SA 4.0. Inherited source notices are included.\n')
    print(out,flush=True)

if __name__=='__main__':main()
