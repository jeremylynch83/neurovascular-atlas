"""Check failure paths that must prevent fitting with stale or invalid anatomy."""
from copy import deepcopy
import json
from pathlib import Path
from validate_courses import validate_courses
from validate_brain import validate_brain

APP=Path(__file__).resolve().parents[2]
manifest=json.loads((APP/'public/anatomy/manifest.json').read_text())
assert not validate_courses(manifest)
assert not validate_brain(manifest)
for change in ['stale-brain','unknown-station','tissue-entry','wrong-side','missing-vessel']:
    test=deepcopy(manifest)
    vessel=next(s for s in test['structures'] if s['id']=='artery.anterior.central_right')
    c=vessel['vesselCourse']
    if change=='stale-brain':c['brainAssetSha256']='stale'
    if change=='unknown-station':c['stationIds']=['brain.missing']
    if change=='tissue-entry':c['segments'][0]['constraints']['allowTissueEntry']=True
    if change=='wrong-side':c['side']='left'
    if change=='missing-vessel':del vessel['vesselCourse']
    assert validate_courses(test), change
test=deepcopy(manifest)
station=next(s for s in test['structures'] if s.get('secondarySurfaceAnchors'))
station['secondarySurfaceAnchors'][0]['assetSha256']='stale'
assert validate_brain(test)
print('Stale geometry, missing targets, unintended tissue-entry, side and secondary-binding failures rejected.')
