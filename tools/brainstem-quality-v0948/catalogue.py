"""Refresh venous metadata after the checked tubular rebuild, preserving brain bindings."""
from common import *
import hashlib
rev=json.loads((OUT/'revision.json').read_text());changed={r['node']:r for r in rev['changed']};sha=hashlib.sha256(Path('public/anatomy/models/venous.glb').read_bytes()).hexdigest()
p=Path('anatomy/generated/complete_manifest.json');m=json.loads(p.read_text());m['release']='0.9.48'
for s in m['structures']:
 c=s.get('vesselCourse')
 if c and s.get('asset',{}).get('file')=='models/venous.glb':
  c['geometrySha256']=sha
  if s['id'] in changed:
   if c.get('fitting',{}).get('release')!='0.9.48':c['fittingPrevious']=c.get('fitting')
   c['fitting']=dict(release='0.9.48',baseline='0.9.47',status='unified-tubular-network-mesh-gates-passed-anatomical-review-pending',radiusProfile=next(r for r in rev['radiusProfiles'] if r['node']==s['id']),validation='docs/validation/brainstem-quality-v0.9.48.json')
   c['radiusPolicy']='reconstruct-tube-with-smoothed-source-radius';c['reviewStatus']='requires-anatomical-review';c['candidateReviewStatus']='Rebuilt as a disjoint exterior patch of a single watertight tubular network. Anatomical calibre remains illustrative.'
   c['summary']='Smooth tubular pontine venous network with a single closed exterior wall, no internal label caps and connected existing endpoint attachments. The transverse crossing remains behind the basilar artery.'
   c['meshQuality']=dict(release='0.9.48',networkId='anterior-pontine-four-vein-network',watertightScope='combined exterior network wall',individualPatchHasIntentionalLabelBoundary=True,validation='docs/validation/brainstem-quality-v0.9.48.json')
   c['attachments']['status']='regional-endpoint-volume-connections-verified'
m['candidateStatus']['widerAnatomicalReviewComplete']=False
m['regionalMeshRebuilds']=[r for r in m.get('regionalMeshRebuilds',[]) if r.get('release')!='0.9.48']
m['regionalMeshRebuilds'].append(dict(release='0.9.48',nodes=list(changed),method=rev['method'],evidence='docs/validation/brainstem-quality-v0.9.48.json',wholeAtlasWatertight=False))
p.write_text(json.dumps(m,indent=2)+'\n')
p=Path('public/anatomy/vessel-courses.json');e=json.loads(p.read_text());e['release']='0.9.48';rows={s['id']:s for s in m['structures']}
for c in e['courses']:
 if c['vesselId'] in rows and rows[c['vesselId']].get('vesselCourse'):c.update(rows[c['vesselId']]['vesselCourse'])
p.write_text(json.dumps(e,indent=2)+'\n')
print('Refreshed venous asset hashes and regional network metadata.')
