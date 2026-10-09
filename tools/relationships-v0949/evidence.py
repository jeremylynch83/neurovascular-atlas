"""Collect final release evidence after geometry, export, loader and build checks."""
from pathlib import Path
import hashlib
import json
import shutil
import sys

work = Path(sys.argv[1]).resolve()
repo = Path(__file__).resolve().parents[2]
candidate = work / 'candidate'
names = ['revision', 'validation', 'self-intersections', 'metrics', 'quality', 'export', 'loader', 'build']
data = {name: json.loads((candidate / (name + '.json')).read_text()) for name in names}
assert data['revision']['release'] == json.loads((repo / 'package.json').read_text())['version'] == '0.9.49'
for name in ['self-intersections', 'quality', 'loader', 'build']:
    assert data[name]['passed'], name
assert data['validation']['passedNewDegenerateFaces'] and data['validation']['passedSharedCollars']
assert all(r['continuousVolumeAttachment'] for r in data['metrics']['attachments'])
assert not data['quality']['newUnexpectedContactPairs']
assert len(data['quality']['regionalNetworks']) == 4
assert all(r['passed'] and r['exactDisjointPatchCoverage'] for r in data['quality']['regionalNetworks'])
assert all(r['candidate'] == 0 for r in data['self-intersections']['results'])

models = repo / 'public/anatomy/models'
hashes = {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in models.glob('*.glb')}
baseline = data['revision']['baselineAssetHashes']
protected = ['brain-context.glb', 'craniofacial.glb']
assert all(hashes[name] == baseline[name] for name in protected)
for row in data['export']['checks']:
    assert hashes[row['file']] == row['sha256'] and row['exactPositionCodecRoundtrip']
for row in data['loader']['checks']:
    assert hashes[row['file']] == row['sha256']
    assert row['exactLoadedPositionsAndIndices'] and row['unitLoadedNormals']

# Replace intermediate coordinate-field checks with checks of the final rebuilt surfaces.
data['revision']['checks'] = data['validation']['meshChecks']
data['revision']['checksScope'] = 'Final candidate meshes, after acoustic and frontal meningeal reconstruction.'
(candidate / 'revision.json').write_text(json.dumps(data['revision'], indent=2) + '\n')
record = {
    'release': '0.9.49', 'baselineRelease': '0.9.48', 'passed': True,
    'changedLabels': len(data['revision']['changed']),
    'assetSha256': hashes,
    'unchangedAssets': {name: hashes[name] for name in protected},
    'checks': data,
    'limitations': [
        'Watertightness applies to the four rebuilt regional exteriors. Selectable patches have open shared interfaces.',
        'Native parent connections use solid-volume overlap; whole-atlas surface welding is not claimed.',
        'Existing contact pairs remain in the register, including altered contact locations within those pairs.',
        'Small canal lumens and cervical vertebrae are absent. Canal containment remains unverified.',
        'The left hypoglossal collar has a new occipital contact in the unsegmented canal corridor.',
        'Reference anatomy and illustrative calibre; anatomical review is still pending.'
    ]
}
dest = repo / 'docs/validation/relationships-v0.9.49.json'
dest.parent.mkdir(parents=True, exist_ok=True)
dest.write_text(json.dumps(record, indent=2) + '\n')
source = repo / 'anatomy/source/relationships-v0949'
source.mkdir(parents=True, exist_ok=True)
for name in ['acoustic-paths.json', 'temporal-paths.json', 'transport-right.csv', 'transport-left.csv']:
    shutil.copy2(work / name, source / name)
for name in ['revision', 'metrics']:
    shutil.copy2(candidate / (name + '.json'), source / (name + '.json'))
print(json.dumps({'release': record['release'], 'passed': True, 'changedLabels': record['changedLabels'], 'regionalNetworks': 4, 'evidence': str(dest)}, indent=2))
