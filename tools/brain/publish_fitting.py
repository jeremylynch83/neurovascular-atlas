"""Refresh catalogue bindings after lossless authoring export."""
import json,hashlib
from pathlib import Path
APP=Path(__file__).resolve().parents[2]
def main():
 p=APP/'anatomy/generated/complete_manifest.json';m=json.loads(p.read_text());report=json.loads((APP/'docs/validation/vessel-fitting-v0.9.17.json').read_text())
 assert not report['geometry'],'No geometry fits are accepted in the v0.9.17 checkpoint'
 geometry=json.loads((APP/'docs/validation/fitting-geometry-v0.9.17.json').read_text());context=json.loads((APP/'docs/validation/fitting-context-v0.9.17.json').read_text())
 for kind in ['veins','arteries']:
  sha=hashlib.sha256((APP/f'.authoring/{kind}-fitted.glb').read_bytes()).hexdigest()
  assert geometry.get('authoringGeometryHashes',{}).get(kind)==sha and context.get('authoringGeometryHashes',{}).get(kind)==sha,'Missing or stale geometry validation'
 assert all(r['after']['triangleContactsWithBanks']==0 for r in geometry['relationships'] if r.get('status')=='fitted' and 'triangleContactsWithBanks' in r['after'])
 surroundings=json.loads((APP/'docs/validation/fitting-surrounding-tissue-v0.9.17.json').read_text())
 assert surroundings['authoringGeometrySha256']==geometry['authoringGeometryHashes']['arteries'],'Stale surrounding tissue audit'
 assert all(c['afterTriangleContacts']<=c['beforeTriangleContacts'] for r in surroundings['checks'] for c in r.get('contacts',[])),'New tissue contacts in edited family'
 assert all(r['noIncreasedContacts'] for r in context['skullChecks']) and context['unchangedBrainSurfaces']==188
 changed={r['node']:r for r in report['geometry']};hashes={}
 primary=set()
 blocked={'artery.anterior.central_left','artery.anterior.central_right','vein.straight','vein.galen','vein.inferior_sagittal','vein.confluence','vein.anterior_pontomesencephalic','vein.anterior_pontine','vein.anterior_medullary'}|{f'vein.{k}.{side}' for k in ['lateral_mesencephalic','transverse_pontine','pontomedullary'] for side in ['left','right']}
 for s in m['structures']:
  if not s.get('vesselCourse'):continue
  c=s['vesselCourse'];f=c['geometry']['file']
  c['brainAssetSha256']=m['brainRegistration']['registeredAssetSha256']
  if f not in hashes:hashes[f]=hashlib.sha256((APP/'public/anatomy'/f).read_bytes()).hexdigest()
  c['geometrySha256']=hashes[f]
  if s['asset']['node'] in changed:
   r=changed[s['asset']['node']]
   c['fitting']={'release':'0.9.17','baseline':'0.9.15','role':'primary' if s['id'] in primary else 'shared-attachment-or-regional-transition','maximumDisplacementMm':r['maximumDisplacementMm'],'status':'fitted-awaiting-anatomical-review'}
  if s['id'] in blocked:
   if s['id'] in {'artery.anterior.central_left','artery.anterior.central_right'}:
    for previous in [' Fitting remains blocked by unresolved adjoining cortical branch courses; original geometry retained.',' Fitting remains blocked by the unresolved terminal sulcal join; original geometry retained.']:
     c['summary']=c['summary'].replace(previous,'')
   c['summary']=c['summary'].replace(' Geometry fitted to registered atlas targets in v0.9.17; anatomical review pending.','')
   c['fitting']={'release':'0.9.17','baseline':'0.9.15','role':'deferred-primary','maximumDisplacementMm':0,'status':'blocked-target-reconciliation'}
   suffix=' Surface fitting remains blocked by unresolved brainstem, clival and cerebellar context relationships.' if s['id'] not in {'vein.straight','vein.galen','vein.inferior_sagittal','vein.confluence'} else ' Dural fitting remains blocked by unresolved neighbouring tissue and shared junction relationships.'
   if s['id']=='artery.anterior.central_right':suffix=' Central arterial family fitting remains blocked by unresolved adjoining branch courses and clearance; original geometry retained.'
   if s['id']=='artery.anterior.central_left':suffix=' Central arterial family fitting remains blocked by unresolved adjoining branch courses and clearance; original geometry retained.'
   if suffix not in c['summary']:c['summary']+=suffix
  if s['id'] in primary:
   suffix=' Geometry fitted to registered atlas targets in v0.9.17; anatomical review pending.'
   if suffix not in c['summary']:c['summary']+=suffix
 for r in m['relationships']:
  if r['type']=='course_landmark' and r['from'] in blocked:r['note']='Registered guide evaluated in a rejected v0.9.17 trial; production geometry retained.'
 m['release']='0.9.17';p.write_text(json.dumps(m,indent=2)+'\n')
 export=json.loads((APP/'public/anatomy/vessel-courses.json').read_text());export['brainRegistration']=m['brainRegistration'];export['courses']=[s['vesselCourse'] for s in m['structures'] if s.get('vesselCourse')]
 (APP/'public/anatomy/vessel-courses.json').write_text(json.dumps(export,indent=2)+'\n')
 for file in ['package.json','package-lock.json']:
  path=APP/file;data=json.loads(path.read_text());data['version']='0.9.17'
  if file=='package-lock.json':data['packages']['']['version']='0.9.17'
  path.write_text(json.dumps(data,indent=2)+'\n')
 print('Refreshed vascular geometry versions and catalogue course bindings.')
if __name__=='__main__':main()
