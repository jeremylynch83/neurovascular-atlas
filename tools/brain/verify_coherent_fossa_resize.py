"""Compare the size experiment with exact material-matched brain surfaces."""
import argparse, json, numpy as np, trimesh
from fit_vessels import APP
from reconcile_brainstem import sha
from verify_fitting import collisions
W=APP/'.authoring/coherent-fossa22'
parser=argparse.ArgumentParser();parser.add_argument('--directory');args=parser.parse_args()
if args.directory:W=APP/args.directory
source=trimesh.load(W/'brain-source.glb',process=False);new=trimesh.load(W/'brain-trial.glb',process=False)
registration=json.loads((W/'registration.json').read_text())
assert registration['brainSha256']==sha(W/'brain-trial.glb')
targets={'bone':trimesh.load(APP/'.authoring/bones-baseline.glb',process=False),'vein':trimesh.load(APP/'.authoring/brainstem19/veins-baseline.glb',process=False)}
report={'candidateSha256':sha(W/'brain-trial.glb'),'sourceSha256':sha(W/'brain-source.glb'),'contacts':[],'geometry':[],'failures':[],'appliedToApp':False,'retainedArteryCheckCompleted':False}
for k in new.geometry:
    a,b=source.geometry[k],new.geometry[k]
    if np.array_equal(a.vertices,b.vertices):continue
    ratio=b.area_faces/np.maximum(a.area_faces,1e-20)
    report['geometry'].append({'node':k,'minimumTriangleAreaRatio':float(ratio.min())})
    if ratio[a.area_faces>1e-8].min()<.1:report['failures'].append([k,'collapsed-facet'])
    if any(t in k for t in ['sulc','lat-fis','ventricle','aqueduct']):continue
    for domain,scene in targets.items():
        for target,m in scene.geometry.items():
            counts=[collisions(m,c) for c in [a,b]]
            if any(counts):report['contacts'].append([k,domain,target,*counts])
            if counts[1]>counts[0]:report['failures'].append([k,domain,target,*counts])
    for target,m in new.geometry.items():
        if not any(t in target for t in ['falx-cerebri','tentorium-cerebelli']):continue
        counts=[collisions(c,m) for c in [a,b]]
        if any(counts):report['contacts'].append([k,'dura',target,*counts])
        if counts[1]>counts[0]:report['failures'].append([k,'dura',target,*counts])
    print('Checked fixed obstacles',k,flush=True)
    (W/'context-progress.json').write_text(json.dumps(report,indent=2)+'\n')
report['passed']=not report['failures']
(W/'context-acceptance.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({'passed':report['passed'],'failures':report['failures']},indent=2),flush=True)
