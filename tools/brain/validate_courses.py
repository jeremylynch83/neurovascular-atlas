"""Build-time standard-library checks for vessel course authoring contracts."""
import hashlib, json
from pathlib import Path

APP = Path(__file__).resolve().parents[2]
MODES = {'dural-attachment','dural-free-edge','bony-groove','cisternal','pial','opercular','insular','sulcal','surface-vein','bridging','deep-venous','subependymal','penetrating','choroidal'}

def validate_segments(c, rows, source_cache=None):
    """Bound segments may use distinct targets, with complete source-path coverage."""
    source_cache = {} if source_cache is None else source_cache
    targets, stations = set(), set()
    by_path = {}
    for i, segment in enumerate(c['segments']):
        assert segment['order'] == i and segment['mode'] in MODES
        assert segment['constraints']['allowTissueEntry'] == (segment['mode'] == 'penetrating')
        assert segment['constraints']['avoidAtlasCutFaces'] and segment['constraints']['preserveJoinedAttachments']
        assert segment['constraints']['wallClearance'] == 'radius-aware'
        assert set(segment['targetStructureIds']) <= set(c['targetStructureIds'])
        assert set(segment['stationIds']) <= set(c['stationIds'])
        assert segment['stationIds'] == [s for s in c['stationIds'] if s in segment['stationIds']]
        targets.update(segment['targetStructureIds']); stations.update(segment['stationIds'])
        if 'coursePaths' in c:
            pi = segment['pathIndex']; assert isinstance(pi, int) and 0 <= pi < len(c['coursePaths'])
            path = c['coursePaths'][pi]; source = path['source']
            assert source.startswith('anatomy/source/') and '..' not in Path(source).parts
            if source not in source_cache:
                data = json.loads((APP/source).read_text())
                source_cache[source] = {s['id']:s for s in data['structures']}
            points = source_cache[source][path['sourceStructureId']]['parts'][path['sourcePart']]['points']
            assert path['sourceStructureId'] == c['vesselId'] and path['pointCount'] == len(points)
            assert path['pointSha256'] == hashlib.sha256(json.dumps(points,separators=(',',':')).encode()).hexdigest()
            a,b = segment['pointRange']; assert isinstance(a,int) and isinstance(b,int) and 0 <= a < b < len(points)
            import math
            arc = [0.0]
            for x,y in zip(points,points[1:]): arc.append(arc[-1]+math.dist(x,y))
            assert abs(path['lengthMm']-arc[-1]) < 1e-6
            assert all(abs(x-y)<1e-6 for x,y in zip(segment['arcRangeMm'],[arc[a],arc[b]])) and len(segment['arcRangeMm']) == 2
            by_path.setdefault(pi,[]).append((a,b))
    if c['segments']:
        assert targets == set(c['targetStructureIds']) and stations == set(c['stationIds'])
    if 'coursePaths' in c:
        assert set(by_path) == set(range(len(c['coursePaths'])))
        for pi,ranges in by_path.items():
            assert ranges[0][0] == 0 and ranges[-1][1] == c['coursePaths'][pi]['pointCount']-1
            assert all(one[1] == two[0] for one,two in zip(ranges,ranges[1:]))

def validate_courses(manifest):
    if not manifest.get('vesselCourseSchemaVersion'): return []
    rows = {s['id']:s for s in manifest['structures']}
    reg = manifest['brainRegistration']
    errors, hashes, source_cache = [], {}, {}
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
            assert c['radiusPolicy'] in ['preserve-delivered-profile','preserve-source-profile-with-measured-wall-deformation']
            if c['radiusPolicy']=='preserve-source-profile-with-measured-wall-deformation':
                check=c['fitting']['calibreCheck']
                assert check['method'] and len(check['ratioP05MedianP95'])==3 and check['p95AbsoluteFractionalRadiusChange']>=0
                assert c['reviewStatus']=='requires-anatomical-review'
            assert c['scope'] in ['intracranial','intracranial-and-upper-cervical','protected-baseline','potential-anastomosis']
            assert c['reviewStatus'] in ['requires-anatomical-review','requires-anatomical-target','protected-baseline']
            assert bool(c['segments'])==(c['scope'] in ['intracranial','intracranial-and-upper-cervical'])
            assert not c['missingTargets'] or c['reviewStatus']=='requires-anatomical-target'
            validate_segments(c, rows, source_cache)
            a=c['attachments']
            assert a['parentId']==s['parent']
            for r in a['incoming']+a['outgoing']:
                assert r in manifest['relationships'] and r['from'] in rows and r['to'] in rows
        except (AssertionError,KeyError,ValueError,TypeError,IndexError,OSError) as e: errors.append(f'{s["id"]}: invalid vessel course specification {e}')
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
