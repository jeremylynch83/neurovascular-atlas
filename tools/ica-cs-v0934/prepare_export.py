from model import *
import hashlib
names=json.load(open(OUT/'repair.json'))['changed']
base=ROOT/'baseline';base.mkdir(exist_ok=True);import shutil
shutil.copy2(APP/'public/anatomy/models/venous.glb',base/'venous.glb')
(OUT/'revision.json').write_text(json.dumps({'changed':[{'node':n,'file':'venous.glb'} for n in names],'newLabels':[],'baselineAssetHashes':{'venous.glb':hashlib.sha256((base/'venous.glb').read_bytes()).hexdigest()}},indent=2))
p=APP/'package.json';d=json.load(open(p));d['version']='0.9.34';p.write_text(json.dumps(d,indent=2)+'\n')
p=APP/'package-lock.json';d=json.load(open(p));d['version']='0.9.34';d['packages']['']['version']='0.9.34';p.write_text(json.dumps(d,indent=2)+'\n')
