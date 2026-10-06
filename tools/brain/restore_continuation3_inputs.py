"""Restore unchanged large inputs omitted from the continuation overlay."""
import json,shutil
from fit_vessels import APP
from reconcile_brainstem import sha
w=APP/'.authoring/posterior-family40';source=APP/'.authoring/brainstem19/arteries-baseline.glb'
expected=json.loads((w/'arteries-fit.json').read_text())['sourceSha256']
assert sha(source)==expected,'Original arterial baseline does not match the final candidate'
for name in ['arteries-source.glb','arteries-trial.glb']:
    dest=w/name
    if not dest.exists() or sha(dest)!=expected:shutil.copyfile(source,dest)
brain=w/'brain-trial.glb';target=APP/'.authoring/posterior-context39/brain-trial.glb'
if not target.exists() or sha(target)!=sha(brain):shutil.copyfile(brain,target)
print('Continuation 3 retained inputs restored with matching hashes.')
