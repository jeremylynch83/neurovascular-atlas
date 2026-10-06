"""Whole-wall containment audit, complementing surface-intersection tests."""
import argparse,json
import numpy as np,trimesh
from fit_vessels import APP
from verify_fitting import inside,collisions
from reconcile_brainstem import sha,ANTERIOR
parser=argparse.ArgumentParser();parser.add_argument('--brain',default='public/anatomy/models/brain-context.glb');parser.add_argument('--veins',default='.authoring/brainstem19/veins-baseline.glb');parser.add_argument('--output',default='docs/validation/closed-brainstem-containment-v0.9.19.json');args=parser.parse_args()
brain_path=APP/args.brain;vein_path=APP/args.veins
brain=trimesh.load(brain_path,process=False);veins=trimesh.load(vein_path,process=False)
report={'brainSha256':sha(brain_path),'veinsSha256':sha(vein_path),'checks':[],'failures':[],'limitations':['Containment is evaluated only on closed tissue surfaces. Open pons and midbrain surfaces require an exposed-surface or cisternal-corridor check.','The app geometry is unchanged by this audit.']}
for k in ANTERIOR+['vein.anterior_spinal']:
    for target,m in brain.geometry.items():
        if not any(t in target for t in ['medulla-oblongata','pons.','midbrain.','base-of-peduncle']):continue
        closed=m.is_watertight
        contained=int(inside(veins.geometry[k].vertices,m).sum()) if closed else None
        row={'vein':k,'target':target,'closedTissue':closed,'wallVertices':len(veins.geometry[k].vertices),'containedWallVertices':contained,'triangleContacts':collisions(veins.geometry[k],m)}
        report['checks'].append(row)
        if contained:report['failures'].append({'vein':k,'target':target,'containedWallVertices':contained})
report['closedTissueContainmentPassed']=not report['failures']
p=APP/args.output;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report['failures'],indent=2),flush=True)
