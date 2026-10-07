import json,hashlib
from pathlib import Path
APP=Path(__file__).resolve().parents[2];ROOT=APP.parent/'fixes-work';p=APP/'anatomy/generated/complete_manifest.json';m=json.loads(p.read_text());rows={s['id']:s for s in m['structures']};by_node={s['asset']['node']:s for s in m['structures'] if s.get('asset')}
rev=json.loads((ROOT/'candidate/revision.json').read_text());quality=json.loads((ROOT/'candidate/validation.json').read_text());clear=json.loads((ROOT/'candidate/clearance.json').read_text())
hashes={'models/'+p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in (APP/'public/anatomy/models').glob('*.glb')}
calibres={r['node']:r for r in quality['calibreChanges']}
for s in rows.values():
 if s.get('vesselCourse'):
  c=s['vesselCourse'];c['geometrySha256']=hashes[s['asset']['file']]
  if s['asset']['node'] in calibres:
   c['radiusPolicy']='preserve-source-profile-with-measured-wall-deformation'
   c['fitting']={'release':'0.9.29','baseline':'0.9.28','status':'local-overpass-mesh-gates-passed-anatomical-review-pending','calibreCheck':calibres[s['asset']['node']],'maximumDisplacementMm':next(r['maximumDisplacementMm'] for r in rev['changed'] if r['node']==s['asset']['node'])}
   c['candidateReviewStatus']='Local connected overpass validated; no whole-model anatomical approval'
   s['provenance']['sourceRefs']=list(dict.fromkeys(s['provenance']['sourceRefs']+['ref.audit2026.R01','ref.audit2026.R14']))
def review(sid,issue,status,text):
 s=rows[sid];r=s.setdefault('anatomicalReview',{'status':status,'issueIds':[],'summary':''})
 r['issueIds'].append(issue);r['summary']+=((' ' if r['summary'] else '')+text)
 if status=='correction-required':r['status']=status;s['provenance']['reviewStatus']='revision-required'
for sid in ['vein.straight','vein.galen','brain.falx-cerebri','brain.tentorium-cerebelli.right','brain.tentorium-cerebelli.left']:
 review(sid,'G01','correction-required','The straight sinus and registered falcotentorial junction remain misaligned. The connected Galenic, sinus and dural region needs joint anatomical refitting.')
for r in clear['resolvedAuditContacts']:
 if r['candidateHalfContacts']:
  for node in [r['one'],r['two']]:
   sid=by_node[node]['id']
   if 'G02' not in rows[sid].get('anatomicalReview',{}).get('issueIds',[]):review(sid,'G02','correction-required','An audited posterior artery–vein intersection involving this structure remains. Five of the twelve audited pairs have been cleared; seven remain open.')
measure=json.loads((APP.parent/'audit-work/measurements.json').read_text())
for r in measure['selectedBoneContacts']:
 if not r['contacts']:continue
 sid=by_node[r['one']]['id'];review(sid,'G03','correction-required','This vessel contacts the coarse skull mesh in a canal region. A continuous canal lumen is not resolved, so vessel trajectory error cannot be distinguished reliably from missing bony canal detail.')
for side in ['right','left']:
 for seg in ['cavernous','paraophthalmic']:
  review(f'artery.anterior.internal_carotid_{side}.segment.{seg}','G04','provisional-boundary','The NYU mesh boundary now follows the existing estimated proximal dural-ring reference, preserving the arterial surface. No dural-ring surface is segmented; independent soft-tissue calibration remains open.')
 for seg in ['a2','a3','a4']:
  review(f'artery.anterior.aca_pericallosal_{side}.segment.{seg}','G05','correction-required','The pericallosal route remains offset from the registered callosal reference. A connected fitting trial introduced new cingulate and venous contacts and was withheld.')
 for s in [f'vein.superior_cerebellar_peduncular.{side}',f'vein.tectal.{side}',f'vein.horizontal_fissure.{side}']:
  rows[s]['provenance']['sourceRefs']=list(dict.fromkeys(rows[s]['provenance']['sourceRefs']+['ref.audit2026.R01']))
# One review entry per issue in each structure.
for s in rows.values():
 if s.get('anatomicalReview'):s['anatomicalReview']['issueIds']=list(dict.fromkeys(s['anatomicalReview']['issueIds']))
m['vesselCourseState']='partially-fitted-awaiting-review';m['vesselCourseSchemaVersion']='1.1'
m['candidateStatus']['widerAnatomicalReviewComplete']=False
m['anatomicalAuditCorrections']={'release':'0.9.29','baseline':'0.9.28','date':'2026-10-07','descriptionCorrections':67,'parentCorrections':2,'boundedMixedCourses':6,'resolvedAuditedCrossingPairs':5,'remainingAuditedCrossingPairs':7,'unchangedBrainAndSkull':True,'wholeModelAnatomicallyApproved':False,'report':'docs/ANATOMICAL_CORRECTIONS_v0.9.29.md'}
p.write_text(json.dumps(m,indent=2)+'\n')
v=APP/'public/anatomy/vessel-courses.json';data=json.loads(v.read_text());data['release']='0.9.29';data['schemaVersion']='1.1';data['state']=m['vesselCourseState'];data['segmentBoundaryPolicy']='Whole-course references retained where unspecified; bounded mixed courses use distinct target subsets and complete adjacent source-point ranges';data['courses']=[s['vesselCourse'] for s in m['structures'] if s.get('vesselCourse')];v.write_text(json.dumps(data,indent=2)+'\n')
for src,name in [('revision.json','anatomical-mesh-authoring'),('validation.json','anatomical-mesh-quality'),('clearance.json','anatomical-clearance'),('export.json','anatomical-export')]:
 (APP/f'docs/validation/{name}-v0.9.29.json').write_bytes((ROOT/'candidate'/src).read_bytes())
# Actual authoring evidence and audit references remain reproducible.
register=json.loads((APP.parent/'audit-work/issue-register.json').read_text());register['release']='0.9.29';register['baselineRelease']='0.9.28';register['auditDate']='2026-10-07'
for r in register['issues']:
 k=r['id'];r['status']='Implemented' if k.startswith('T') or k.startswith('M') else 'Partially implemented' if k=='G02' else 'Provisional boundary corrected; calibration open' if k=='G04' else 'Open'
 r['closureEvidence']= 'docs/validation/anatomical-text-corrections-v0.9.29.json' if k.startswith('T') or k=='M01' else 'docs/validation/anatomical-course-partitions-v0.9.29.json' if k=='M02' else 'docs/validation/anatomical-clearance-v0.9.29.json' if k=='G02' else 'docs/validation/anatomical-mesh-authoring-v0.9.29.json' if k=='G04' else 'Retained baseline geometry; regional anatomical references remain unresolved'
(APP/'docs/validation/anatomical-correction-register-v0.9.29.json').write_text(json.dumps(register,indent=2)+'\n')
print('Updated catalogue, hashes, course export and correction register')
