from pathlib import Path
import hashlib,json,shutil
ROOT=Path(__file__).resolve().parent;APP=ROOT.parents[1];OUT=ROOT/'candidate';dest=APP/'anatomy/source/ica-cs-v0933';dest.mkdir(exist_ok=True)
revision=json.load(open(OUT/'revision.json'));changed={a['node'] for a in revision['changed']};m=json.load(open(APP/'anatomy/generated/complete_manifest.json'));m['release']='0.9.33';m['icaCavernousRefinement']={'version':'0.9.33','baseline':'0.9.32','method':'Reduce independent posterior sinus roof space with bone and artery clearance constraints; fair joined artery/vein meshes while preserving ostia and all labelled connections','reviewStatus':'requires-anatomical-review','evidence':'docs/ICA_CS_v0.9.33.md','validation':'anatomy/source/ica-cs-v0933/validation.json'}
hashes={'models/'+p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in (APP/'public/anatomy/models').glob('*.glb')}
for s in m['structures']:
 c=s.get('vesselCourse')
 if c:c['geometrySha256']=hashes[s['asset']['file']]
 if s.get('asset',{}).get('node') in changed:
  s['notes']=s.get('notes','')+' Geometry update v0.9.33: reduced posterior sinus roof and constrained smoothing of connected local vessel surfaces; native topology and fixed ophthalmic attachments retained.'
  if c:c['candidateReviewStatus']='Local v0.9.33 numerical checks passed; anatomical review pending';c['reviewStatus']='requires-anatomical-review'
(APP/'anatomy/generated/complete_manifest.json').write_text(json.dumps(m,indent=2)+'\n')
c=json.load(open(APP/'public/anatomy/vessel-courses.json'));c['release']='0.9.33';c['courses']=[s['vesselCourse'] for s in m['structures'] if s.get('vesselCourse')];(APP/'public/anatomy/vessel-courses.json').write_text(json.dumps(c,indent=2)+'\n')
for p in OUT.glob('*.json'):shutil.copy2(p,dest/p.name)
(APP/'README.txt').write_text('Neurovascular Atlas v0.9.33\n\nUse the included installer as before.\n\nSee docs/ICA_CS_v0.9.33.md for posterior sinus reduction, constrained smoothing and validation limits. Comparison renders are in review-renders.\n')
