"""Prepare exact delivered additions for an independent composite contact check.

First decode public/anatomy/models with tools/decode-posterior-baseline.mjs
into WORK/decoded. This leaves every original decoded buffer available.
"""
import sys,json,shutil
from pathlib import Path
work=Path(sys.argv[1]);data=work/'decoded';out=work/'candidate';out.mkdir(exist_ok=True)
root=Path(__file__).resolve().parents[2]
new=json.loads((root/'anatomy/source/audit-finish-v0950/revision.json').read_text())['newLabels']
meta=json.loads((data/'meshes.json').read_text())
(data/'meshes.json').write_text(json.dumps([r for r in meta if r['name'] not in new],indent=2)+'\n')
rev=dict(release='0.9.51',baseline='accepted v0.9.50 geometry',newLabels=new,changed=[dict(node=n,file='venous.glb',topology='delivered closed reference surface') for n in new])
(out/'revision.json').write_text(json.dumps(rev,indent=2)+'\n')
for n in new:
    for extension in ['positions.bin','indices.bin']:
        shutil.copyfile(data/(n+'.'+extension),out/(n+'.'+extension))
print('Prepared',len(new),'delivered venous additions')
