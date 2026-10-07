"""Refresh every binding affected by the accepted geometry, retaining open findings."""
import sys, json, hashlib, shutil
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'anatomical-fixes-v0929'))
from geometry import *
APP = Path(__file__).resolve().parents[2]
C = APP.parent/'corrections-work/candidate-final'
revision = json.loads((C/'revision.json').read_text())
quality = json.loads((C/'validation.json').read_text())
wall_checks = json.loads((C/'recovered-walls.json').read_text())
assert quality['passed'] and wall_checks['passed']
path = APP/'anatomy/generated/complete_manifest.json'
m = json.loads(path.read_text()); rows = {s['id']:s for s in m['structures']}
changed = {r['node']:r for r in revision['changed']}
hashes = {'models/'+p.name:hashlib.sha256(p.read_bytes()).hexdigest()
          for p in (APP/'public/anatomy/models').glob('*.glb')}
brain_hash = hashes['models/brain-context.glb']
calibre = {r['node']:r for r in quality['calibreChanges']}
for name in changed:
    meshes[name].new = np.fromfile(C/(name+'.positions.bin'),'<f4').reshape(-1,3).astype(float)

def refresh_anchor(a):
    mesh = meshes[rows[a['structureId']]['asset']['node']]
    tri = mesh.new[mesh.f[a['triangleIndex']]]
    a['position'] = (tri*np.array(a['barycentric'])[:,None]).sum(0).tolist()
    a['assetSha256'] = brain_hash

for s in rows.values():
    name = s.get('asset',{}).get('node')
    if s.get('asset',{}).get('file') == 'models/brain-context.glb' and name in changed:
        v = meshes[name].new
        s['anatomy']['bounds'] = [v.min(0).tolist(),v.max(0).tolist()]
        s['anatomy']['centroid'] = v.mean(0).tolist()
        s['anatomy']['regionalAdjustmentRelease'] = '0.9.31'
    if s.get('surfaceAnchor'):
        refresh_anchor(s['surfaceAnchor'])
        s['landmark']['point'] = s['surfaceAnchor']['position']
    for a in s.get('secondarySurfaceAnchors',[]): refresh_anchor(a)
    c = s.get('vesselCourse')
    if c:
        c['brainAssetSha256'] = brain_hash
        c['geometrySha256'] = hashes[s['asset']['file']]
        if name in changed:
            c['summary'] = c.get('summary','').replace('Surface fitting remains blocked by unresolved brainstem, clival and cerebellar context relationships.', 'v0.9.31 applies a local connected crossing correction; wider brainstem, clival and cerebellar relationships remain under anatomical review.')
            c['fitting'] = {'release':'0.9.31','baseline':'0.9.30',
                'status':'crossing-mesh-gates-passed-anatomical-review-pending',
                'maximumDisplacementMm':changed[name]['maximumDisplacementMm'],
                'validation':'docs/validation/anatomical-mesh-quality-v0.9.31.json'}
            if name in calibre:
                c['radiusPolicy'] = 'preserve-source-profile-with-measured-wall-deformation'
                c['reviewStatus'] = 'requires-anatomical-review'
                c['fitting']['calibreCheck'] = calibre[name]
            c['candidateReviewStatus'] = 'Local crossing correction applied; regional anatomy and illustrative calibre require review'
    review = s.get('anatomicalReview')
    if review and 'G02' in review['issueIds']:
        if len(review['issueIds']) == 1:
            review['status'] = 'correction-implemented-awaiting-review'
            review['summary'] = 'All twelve audited posterior artery-vein surface intersections are cleared in v0.9.31. Local tissue and venous shape adjustments pass the recorded geometry gates; anatomical review remains pending.'
            s['provenance']['reviewStatus'] = 'unreviewed'
        else:
            old = 'An audited posterior artery–vein intersection involving this structure remains. Five of the twelve audited pairs have been cleared; seven remain open.'
            review['summary'] = review['summary'].replace(old,'All twelve audited posterior artery-vein surface intersections are cleared in v0.9.31; other recorded findings remain open.')
for s in rows.values():
    ids = s.get('vesselGuide',{}).get('anchorIds',[])
    if ids: s['landmark']['course'] = [rows[key]['surfaceAnchor']['position'] for key in ids]

reg = m['brainRegistration']; reg['registeredAssetSha256'] = brain_hash
reg['method'] = 'Bone-correspondence similarity registration, followed by recorded regional adjustments. See regionalAdjustments and brainAdjustmentPolicy for the subsequent local deformation fields.'
reg['limitations'] = 'Regional teaching context. Brainstem geometry has local crossing-related adjustments, not an independent patient-derived refit. Fine anatomy, illustrative vessel calibres and the open correction-register findings require review.'
reg['regionalAdjustments']=[r for r in reg.get('regionalAdjustments',[]) if r.get('release')!='0.9.31']
reg['regionalAdjustments'].append({'release':'0.9.31',
    'brainSha256':brain_hash,'method':'Common brainstem and venous placement fields, then a 0.6 mm maximum local peduncular recess after vein-wall recovery.',
    'evidence':'docs/validation/anatomical-mesh-authoring-v0.9.31.json'})
m['brainAdjustmentPolicy']['appliedAdjustments']=[r for r in m['brainAdjustmentPolicy'].get('appliedAdjustments',[]) if r.get('release')!='0.9.31']
m['brainAdjustmentPolicy']['appliedAdjustments'].append({
    'release':'0.9.31','status':'crossing-context-adjustment-awaiting-anatomical-review',
    'geometry':[r for r in revision['changed'] if r['file']=='brain-context.glb'],
    'completeVenousRefitApplied':False,
    'evidence':'docs/validation/anatomical-mesh-quality-v0.9.31.json'})
m['release'] = '0.9.31'; m['candidateStatus']['widerAnatomicalReviewComplete'] = False
m['anatomicalAuditCorrections'] = {'release':'0.9.31','baseline':'0.9.30','date':'2026-10-07',
    'retainedDescriptionCorrections':67,'retainedParentCorrections':2,'boundedMixedCourses':6,
    'newlyResolvedAuditedCrossingPairs':7,'resolvedAuditedCrossingPairs':12,
    'remainingAuditedCrossingPairs':0,'unchangedArteriesSkullAndAnastomoses':True,
    'wholeModelAnatomicallyApproved':False,'report':'docs/ANATOMICAL_CORRECTIONS_v0.9.31.md'}
m['assetRevisions'] = {file:sha[:20] for file,sha in hashes.items()}
m['assetByteSizes'] = {file:(APP/'public/anatomy'/file).stat().st_size for file in hashes}
path.write_text(json.dumps(m,indent=2)+'\n')
vpath=APP/'public/anatomy/vessel-courses.json'; export=json.loads(vpath.read_text())
export.update(release=m['release'],brainRegistration=reg,brainAdjustmentPolicy=m['brainAdjustmentPolicy'],
              courses=[s['vesselCourse'] for s in m['structures'] if s.get('vesselCourse')])
vpath.write_text(json.dumps(export,indent=2)+'\n')
lpath=APP/'public/anatomy/brain-landmarks.json'; landmarks=json.loads(lpath.read_text())
landmarks['registration']=reg
landmarks['anchors']=[rows[a['id']] for a in landmarks['anchors']]
landmarks['surfaces']=[{key:rows[s['id']][key] for key in s} for s in landmarks['surfaces']]
lpath.write_text(json.dumps(landmarks,indent=2)+'\n')
validation=APP/'docs/validation'
for source,target in [('revision.json','anatomical-mesh-authoring'),('validation.json','anatomical-mesh-quality'),
                      ('clearance.json','anatomical-clearance'),('export.json','anatomical-export'),
                      ('recovered-walls.json','anatomical-recovered-walls')]:
    shutil.copyfile(C/source,validation/(target+'-v0.9.31.json'))
shutil.copyfile(APP.parent/'corrections-work/candidate/validation.json',validation/'anatomical-placement-stage-v0.9.31.json')
register=json.loads((validation/'anatomical-correction-register-v0.9.29.json').read_text())
register.update(release='0.9.31',baselineRelease='0.9.30')
for issue in register['issues']:
    if issue['id']=='G02':
        issue['status']='Geometry implemented; anatomical review pending'
        issue['closureEvidence']='docs/validation/anatomical-clearance-v0.9.31.json: 12/12 audited pairs clear; original joins retained; no new cross-asset or independent intra-venous contact pairs'
    elif issue['id']=='G01':
        issue['closureEvidence']='Dural-ridge trial introduced new cortical and vascular contacts and was withheld. See anatomical-rejected-trials-v0.9.31.json.'
    elif issue['id']=='G05':
        issue['closureEvidence']='Connected callosal fitting trials introduced new cingulate, septal and venous contacts and were withheld. See anatomical-rejected-trials-v0.9.31.json.'
    elif issue['id']=='G03':
        issue['closureEvidence']='The supplied coarse skull does not resolve continuous canal lumina. Independent canal geometry and joint vessel/skull calibration are required; bone and canal trajectories were retained.'
(validation/'anatomical-correction-register-v0.9.31.json').write_text(json.dumps(register,indent=2)+'\n')
print('Updated geometry hashes, all bound anchors, course exports and correction register')
