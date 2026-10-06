"""Package a standalone, local before/after review of staged anatomy."""
import argparse,json,shutil,zipfile
from pathlib import Path
from fit_vessels import APP,read_glb
from reconcile_brainstem import ANTERIOR,TRANSVERSE,LATERAL,sha
from refine_context_skin import save_replaced

def subset(src,dest,keys):
    d,b=read_glb(src);d['nodes']=[n for n in d['nodes'] if n.get('name') in keys]
    save_replaced(dest,d,b,{})

def main():
    p=argparse.ArgumentParser();p.add_argument('--directory',default='.authoring/posterior-family40');args=p.parse_args()
    w=APP/args.directory;out=APP/'deliverables/posterior-fossa-model-review';out.mkdir(parents=True,exist_ok=True)
    (out/'models').mkdir(exist_ok=True)
    catalogue=json.loads((APP/'.authoring/brainstem19/manifest-baseline.json').read_text())
    cb={r['id'] for r in catalogue['structures'] if r.get('anatomy',{}).get('category')=='cerebellum'}
    brain_keys=cb|{f'brain.{k}.{s}' for k in ['pons','medulla-oblongata','midbrain','base-of-peduncle'] for s in ['left','right']}
    vein_keys=set(ANTERIOR+TRANSVERSE+LATERAL+['vein.anterior_spinal','vein.basilar_plexus']+[f'vein.{k}.{s}' for k in ['superior_petrosal_vein','cerebellopontine_fissure'] for s in ['left','right']])
    subset(APP/'public/anatomy/models/brain-context.glb',out/'models/current-brain.glb',brain_keys)
    subset(w/'brain-trial.glb',out/'models/trial-brain.glb',brain_keys)
    subset(APP/'.authoring/brainstem19/veins-baseline.glb',out/'models/current-veins.glb',vein_keys)
    subset(w/'veins-trial.glb',out/'models/trial-veins.glb',vein_keys)
    subset(APP/'.authoring/brainstem19/arteries-baseline.glb',out/'models/basilar.glb',{'Basilar'})
    for src,dest in [('build/three.module.js','js/three.module.js'),('build/three.core.js','js/three.core.js'),('examples/jsm/loaders/GLTFLoader.js','js/loaders/GLTFLoader.js'),('examples/jsm/controls/OrbitControls.js','js/controls/OrbitControls.js'),('examples/jsm/utils/BufferGeometryUtils.js','js/utils/BufferGeometryUtils.js'),('examples/jsm/utils/SkeletonUtils.js','js/utils/SkeletonUtils.js'),('LICENSE','THREE-LICENSE.txt')]:
        target=out/dest;target.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(APP/'node_modules/three'/src,target)
    shutil.copyfile(APP/'tools/posterior-review-viewer.html',out/'index.html')
    shutil.copyfile(APP/'public/anatomy/licenses/Z_Anatomy_Source_Licence.txt',out/'Z_Anatomy_Source_Licence.txt')
    (out/'SOURCE-ATTRIBUTION.txt').write_text('Brain context attribution:\nBodyParts3D - The Database Center for Life Science - CC-BY-SA 2.1 Japan\nZ-Anatomy - The open source atlas of anatomy - CC-BY-SA 4.0\n\nSource: https://github.com/LluisV/Z-Anatomy/blob/PC-Version/Resources/Models/FBX/NervousSystem100.fbx\n\nThe brain-context GLBs are registered and, in the trial, locally resized derivatives. Their inherited attribution and share-alike terms are retained. The original source licence notice is in Z_Anatomy_Source_Licence.txt. Three.js is supplied under its separate MIT licence in THREE-LICENSE.txt.\n')
    acceptance=json.loads((w/'combined-acceptance.json').read_text())
    model_review={'status':'unaccepted anatomical review trial','productionGeometryChanged':False,'basilarGeometryChanged':False,'cerebellarLabels':sorted(cb),'candidateBrainSha256':sha(w/'brain-trial.glb'),'candidateVeinsSha256':sha(w/'veins-trial.glb'),'acceptancePassed':acceptance['passed'],'anteriorSurface':acceptance['anteriorSurface'],'lateralGaps':acceptance['lateralGaps'],'failures':acceptance['failures'],'modelSubsetHashes':{p.name:sha(p) for p in (out/'models').glob('*.glb')}}
    (out/'model-review.json').write_text(json.dumps(model_review,indent=2)+'\n')
    for name in ['combined-acceptance.json','trial.json']:
        shutil.copyfile(w/name,out/name)
    (out/'serve.py').write_text("from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler\nfrom pathlib import Path\nimport os, webbrowser\nos.chdir(Path(__file__).resolve().parent)\nurl='http://127.0.0.1:9844/'\nprint('Posterior fossa review: '+url,flush=True)\nwebbrowser.open(url)\ntry:\n    ThreadingHTTPServer(('127.0.0.1',9844),SimpleHTTPRequestHandler).serve_forever()\nexcept KeyboardInterrupt:\n    pass\n")
    (out/'view.sh').write_text('#!/usr/bin/env bash\nset -e\ncd -- "$(dirname -- "$0")"\nexec python3 serve.py\n');(out/'view.sh').chmod(0o755)
    (out/'README.txt').write_text('POSTERIOR FOSSA MODEL REVIEW\n\nUnzip this folder. Run ./view.sh (or python3 serve.py). Open http://127.0.0.1:9844/ if the browser does not open automatically. Drag to rotate, scroll to zoom, and use the matched view and visibility controls. No npm installation or internet connection is required.\n\nThe new model is an unaccepted anatomy trial, not a replacement app release. The basilar artery retains its original wall geometry. The brainstem reduction clears the basilar wall in the signed anterior-surface and triangle-contact checks. Cerebellar tissue receives a modest contraction. Anterior and lateral vein fitting remains under review: full failures and hashes are in model-review.json and combined-acceptance.json. Production v0.9.19 geometry is unchanged.\n\nThe filtered GLBs retain original labelled model parts. They omit unrelated anatomy for this comparison. Source model attribution is retained in the main atlas and its provenance records. Three.js is bundled under its MIT licence in THREE-LICENSE.txt.\n')
    archive=out.with_suffix('.zip')
    with zipfile.ZipFile(archive,'w',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
        for p in sorted(out.rglob('*')):
            if p.is_file():z.write(p,p.relative_to(out.parent))
    print(archive,archive.stat().st_size,flush=True)

if __name__=='__main__':main()
