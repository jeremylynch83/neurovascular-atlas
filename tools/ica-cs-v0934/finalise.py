from model import *
import hashlib,shutil
m=json.load(open(APP/'anatomy/generated/complete_manifest.json'));m['release']='0.9.34'
m['icaCavernousRefinement']={'version':'0.9.34','baseline':'0.9.33','method':'Repair perforated venous surface; restore compact chamber, retain primary ICA channel, fair connected network and graft native remote collars','reviewStatus':'requires-anatomical-review','evidence':'docs/ICA_CS_v0.9.34.md','validation':'anatomy/source/ica-cs-v0934/validation.json'}
hashes={'models/'+p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in (APP/'public/anatomy/models').glob('*.glb')}
m['assetRevisions']={k:v[:20] for k,v in hashes.items()};m['assetByteSizes']={k:(APP/'public/anatomy'/k).stat().st_size for k in hashes}
changed=set(json.load(open(OUT/'repair.json'))['changed'])
for s in m['structures']:
 if s.get('vesselCourse'):s['vesselCourse']['geometrySha256']=hashes[s['asset']['file']]
 if s.get('asset',{}).get('node') in changed:
  s['notes']=s.get('notes','')+' Geometry update v0.9.34: repaired continuous venous wall and native tributary collars. Broad small-branch clearance cuts removed.'
(APP/'anatomy/generated/complete_manifest.json').write_text(json.dumps(m,indent=2)+'\n')
c=json.load(open(APP/'public/anatomy/vessel-courses.json'));c['release']='0.9.34';c['courses']=[s['vesselCourse'] for s in m['structures'] if s.get('vesselCourse')];(APP/'public/anatomy/vessel-courses.json').write_text(json.dumps(c,indent=2)+'\n')
dest=APP/'anatomy/source/ica-cs-v0934';dest.mkdir(exist_ok=True)
for p in OUT.glob('*.json'):shutil.copy2(p,dest/p.name)
(APP/'README.txt').write_text('Neurovascular Atlas v0.9.34\n\nCavernous sinus surface repair. See docs/ICA_CS_v0.9.34.md. Use the included installer as before.\n')
