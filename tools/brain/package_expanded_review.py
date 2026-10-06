"""Exact labelled subsets of candidate 55 for wider vascular inspection."""
import json, shutil, hashlib,argparse
from pathlib import Path
import numpy as np
from fit_vessels import APP, read_glb, accessor
from package_posterior_model_review import subset

OUT = APP / 'deliverables/posterior-fossa-expanded-review'
SOURCE = APP / '.authoring/posterior-tubular55'

def main():
    global OUT,SOURCE
    parser=argparse.ArgumentParser();parser.add_argument('--source',default='.authoring/posterior-tubular55');parser.add_argument('--output',default='deliverables/posterior-fossa-expanded-review');parser.add_argument('--candidate',type=int,default=55);args=parser.parse_args();OUT=APP/args.output;SOURCE=APP/args.source
    (OUT/'models').mkdir(parents=True, exist_ok=True)
    manifest = json.loads(((SOURCE/'candidate-manifest.json') if (SOURCE/'candidate-manifest.json').exists() else (APP/'public/anatomy/manifest.json')).read_text())
    cb = {r['id'] for r in manifest['structures'] if r.get('anatomy',{}).get('category') == 'cerebellum'}
    brain = cb | {f'brain.{k}.{s}' for k in ['pons','medulla-oblongata','midbrain','base-of-peduncle'] for s in ['left','right']}
    if (SOURCE/'cord-context.json').exists():brain.add('brain.upper-cervical-cord')
    posterior = {'vein.'+k for k in ['precentral_cerebellar','superior_vermian','posterior_communicating','anterior_pontomesencephalic','anterior_pontine','anterior_medullary','anterior_spinal']}
    posterior |= {f'vein.{k}.{s}' for k in ['superior_petrosal_vein','lateral_mesencephalic','cerebellopontine_fissure','inferior_vermian','inferior_hemispheric','transverse_pontine','pontomedullary'] for s in ['left','right']}
    deep = {'vein.galen'} | {f'vein.{k}.{s}' for k in ['basal','internal_cerebral'] for s in ['left','right']}
    outlets = {'vein.straight','vein.confluence'} | {f'vein.{k}.{s}' for k in ['superior_petrosal','transverse','sigmoid'] for s in ['left','right']}
    d,b = read_glb(SOURCE/'arteries-trial.glb')
    prefixes = ('SCA ','AICA ','PICA ','Pontine ','VA medullary ','Peduncular ','Labyrinthine ','Common cochlear ','Anterior vestibular ','Anterior spinal','Posterior spinal ','PCA P1 ','PCA P2-P3 ','PCA short circumflex ','PCA long circumflex ','PCA collicular ','Vertebral V4 ')
    arteries = {n['name'] for n in d['nodes'] if n.get('name','') == 'Basilar' or n.get('name','').startswith(prefixes)}
    groups = {'brain':('brain-trial.glb',brain),'arteries':('arteries-trial.glb',arteries),'veins':('veins-trial.glb',posterior),'deep-veins':('veins-trial.glb',deep),'outlets':('veins-trial.glb',outlets)}
    result = {'candidate':args.candidate,'status':'Anatomical review candidate; existing placement and joins remain under review.','productionGeometryChanged':False,'cerebellarLabels':sorted(cb),'groups':{},'bounds':{},'hashes':{}}
    all_names = set()
    for group,(source,keys) in groups.items():
        src=SOURCE/source; dest=OUT/'models'/f'{group}.glb'
        doc,data=read_glb(src); available={n.get('name') for n in doc['nodes']}
        assert not (keys-available), (group, sorted(keys-available))
        subset(src,dest,keys)
        doc,data=read_glb(dest); lows=[]; highs=[]
        for node in doc['nodes']:
            prim=doc['meshes'][node['mesh']]['primitives'][0]
            points=accessor(doc,data,prim['attributes']['POSITION'])
            lows.append(points.min(axis=0));highs.append(points.max(axis=0))
        result['bounds'][group]=[np.min(lows,axis=0).tolist(),np.max(highs,axis=0).tolist()]
        result['groups'][group]=sorted(keys);all_names|=keys
        result['hashes'][group]=hashlib.sha256(dest.read_bytes()).hexdigest()
        print(group,len(keys),dest.stat().st_size,result['bounds'][group],flush=True)
    assert 'vein.basilar_plexus' not in all_names
    nodes={r['id']:r.get('asset',{}).get('node') for r in manifest['structures']}
    result['relationships']=[r for r in manifest['relationships'] if nodes.get(r.get('from')) in all_names and nodes.get(r.get('to')) in all_names and r.get('type') in ['drains_to','communicates_with','branches_from','branches_to']]
    if (SOURCE/'posterior-spinal-courses.json').exists():result['posteriorSpinal']=json.loads((SOURCE/'posterior-spinal-courses.json').read_text())
    (OUT/'model-review.json').write_text(json.dumps(result,indent=2)+'\n')
    base=APP/'deliverables/posterior-fossa-tubular-review'
    shutil.copytree(base/'js',OUT/'js',dirs_exist_ok=True)
    for name in ['THREE-LICENSE.txt','Z_Anatomy_Source_Licence.txt','SOURCE-ATTRIBUTION.txt']:
        shutil.copyfile(base/name,OUT/name)
    (OUT/'index.html').write_text((APP/'tools/expanded-review-viewer.html').read_text().replace('Candidate 55',f'Candidate {args.candidate}'))
    (OUT/'serve.py').write_text("from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler\nfrom pathlib import Path\nimport os, webbrowser\nos.chdir(Path(__file__).resolve().parent)\nurl='http://127.0.0.1:9864/'\nprint(url,flush=True)\nwebbrowser.open(url)\nThreadingHTTPServer(('127.0.0.1',9864),SimpleHTTPRequestHandler).serve_forever()\n")
    (OUT/'view.sh').write_text('#!/usr/bin/env bash\nset -e\ncd -- "$(dirname -- "$0")"\nexec python3 serve.py\n'); (OUT/'view.sh').chmod(0o755)
    (OUT/'README.txt').write_text('EXPANDED POSTERIOR FOSSA VASCULAR REVIEW\n\nRun python3 serve.py, or ./view.sh, then open http://127.0.0.1:9864/. No installation or internet is required. Drag to rotate; scroll to zoom. Choose combined, venous, arterial or deep-vein views and adjust tissue opacity. Select a named vessel to highlight it.\n\nThese are exact labelled subsets of candidate 55. No further geometry editing was performed. Clival/basilar plexus is omitted. Arteries include vertebral V4, basilar, proximal PCA/circumflex branches, SCA/AICA/PICA and their cerebellar and brainstem branches, labyrinthine and spinal branches. Veins include posterior-fossa veins, bilateral basal and internal cerebral veins, Galen, straight sinus and petrosal/transverse/sigmoid outlets.\n\nThe deep cerebral veins and posterior-fossa Galenic tributaries meet at Galen; these renders do not imply that all posterior-fossa venous drainage enters the internal cerebral veins. Existing geometry may have remaining placement and join issues. Production geometry was not changed.\n\nModels retain the supplied labels and coordinates. Sources and licences are in the accompanying attribution files. model-review.json records the selected structures, catalogue relationships, bounds and hashes. Individual renders are in views/.\n')

if __name__=='__main__':main()
