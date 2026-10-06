"""Build-time standard-library checks for vessel course authoring contracts."""
import hashlib, json
from pathlib import Path

APP = Path(__file__).resolve().parents[2]
MODES = {'dural-attachment','dural-free-edge','bony-groove','cisternal','pial','opercular','insular','sulcal','surface-vein','bridging','deep-venous','subependymal','penetrating','choroidal'}

def validate_courses(manifest):
    if not manifest.get('vesselCourseSchemaVersion'): return []
    rows = {s['id']:s for s in manifest['structures']}
    reg = manifest['brainRegistration']
    errors, hashes = [], {}
    for s in rows.values():
        if s['system'] not in ['artery','vein'] or not s.get('asset'): continue
        try:
            c = s['vesselCourse']
            assert c['vesselId']==s['id'] and c['side']==s['side'] and c['geometry']==s['asset']
            assert c['registrationId']==reg['id'] and c['brainAssetSha256']==reg['registeredAssetSha256']
            file=s['asset']['file']
            if file not in hashes:hashes[file]=hashlib.sha256((APP/'public/anatomy'/file).read_bytes()).hexdigest()
            assert c['geometrySha256']==hashes[file]
            assert all(k in rows and rows[k]['system']=='brain' and rows[k].get('asset') for k in c['targetStructureIds'])
            assert all(k in rows and rows[k].get('surfaceAnchor') for k in c['stationIds'])
            assert c['radiusPolicy']=='preserve-delivered-profile'
            assert c['scope'] in ['intracranial','intracranial-and-upper-cervical','protected-baseline','potential-anastomosis']
            assert c['reviewStatus'] in ['requires-anatomical-review','requires-anatomical-target','protected-baseline']
            assert bool(c['segments'])==(c['scope'] in ['intracranial','intracranial-and-upper-cervical'])
            assert not c['missingTargets'] or c['reviewStatus']=='requires-anatomical-target'
            for i,segment in enumerate(c['segments']):
                assert segment['order']==i and segment['mode'] in MODES
                assert segment['constraints']['allowTissueEntry']==(segment['mode']=='penetrating')
                assert segment['constraints']['avoidAtlasCutFaces'] and segment['constraints']['preserveJoinedAttachments']
                assert segment['constraints']['wallClearance']=='radius-aware'
                assert segment['stationIds']==c['stationIds'] and segment['targetStructureIds']==c['targetStructureIds']
            a=c['attachments']
            assert a['parentId']==s['parent']
            for r in a['incoming']+a['outgoing']:
                assert r in manifest['relationships'] and r['from'] in rows and r['to'] in rows
        except (AssertionError,KeyError,ValueError,TypeError) as e: errors.append(f'{s["id"]}: invalid vessel course specification {e}')
    export=APP/'public/anatomy/vessel-courses.json'
    if not export.is_file():
        errors.append('Missing vessel course export')
    else:
        data=json.loads(export.read_text())
        embedded={s['id']:s['vesselCourse'] for s in rows.values() if s.get('vesselCourse')}
        exported={c['vesselId']:c for c in data['courses']}
        if embedded!=exported:errors.append('Vessel course export differs from catalogue')
        if data['brainRegistration']!=reg:errors.append('Vessel course export has stale brain registration')
    return errors
