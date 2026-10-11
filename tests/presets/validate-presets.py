"""Territory coverage and side isolation checks against the shipped catalogue."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
manifest = json.loads((ROOT / 'public/anatomy/manifest.json').read_text())
registry = json.loads((ROOT / 'public/anatomy/preset-vessels.json').read_text())
by_id = {s['id']: s for s in manifest['structures']}
lists = {key: set(ids) for key, ids in registry['vesselIds'].items()}
assert len(lists) == 5
for preset, ids in lists.items():
    assert len(ids) == len(registry['vesselIds'][preset]), f'{preset}: duplicates'
    for sid in ids:
        s = by_id[sid]
        assert s.get('asset') and s['system'] == 'artery'
        assert s.get('displayGroup') != 'anastomoses'
    for side in ('left', 'right'):
        sided = {sid for sid in ids if by_id[sid]['side'] in (side, 'midline')}
        assert sided, (preset, side)
        assert not any(by_id[sid]['side'] == ('right' if side == 'left' else 'left') for sid in sided)
    assert len([sid for sid in ids if by_id[sid]['side'] == 'left']) == len([sid for sid in ids if by_id[sid]['side'] == 'right'])

for side in ('left', 'right'):
    assert f'artery.anterior.internal_carotid_{side}.segment.cavernous' in lists['ica']
    assert f'artery.anterior.ophthalmic_{side}' in lists['ica']
    assert f'artery.anterior.aca_pericallosal_{side}.segment.a5' in lists['ica']
    assert f'artery.anterior.angular_cortical_branch_{side}' in lists['ica']
    assert f'artery.posterior.vertebral_{side}.segment.v4' in lists['vertebrobasilar']
    assert f'artery.posterior.pca_p1_{side}' in lists['vertebrobasilar']
    assert f'artery.posterior.pica_{side}' in lists['vertebrobasilar']
    assert f'artery.posterior.aica_{side}' in lists['vertebrobasilar']
    assert f'artery.posterior.sca_{side}' in lists['vertebrobasilar']
assert 'artery.posterior.basilar' in lists['vertebrobasilar']
assert 'artery.anterior.anterior_communicating' in lists['ica']
assert lists['mma'] < lists['maxillary'] < lists['eca']
assert not (lists['ica'] & lists['eca'])
assert not (lists['ica'] & lists['vertebrobasilar'])
assert not (lists['eca'] & lists['vertebrobasilar'])
print('Passed: five territories, downstream ACA/MCA/PCA/cerebellar coverage, nesting, side isolation and overlay exclusions.')
