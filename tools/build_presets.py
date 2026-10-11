"""Resolve named arterial territories to explicit, reviewable mesh lists.

Follows anatomical parent/segment ownership and branches_to, never potential
anastomoses, communicating relationships, or spatial proximity.
"""
import collections
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
manifest = json.loads((ROOT / 'public/anatomy/manifest.json').read_text())
by_id = {s['id']: s for s in manifest['structures']}
seeds = {
    'ica': ['artery.anterior.internal_carotid_left', 'artery.anterior.internal_carotid_right',
            'artery.anterior.anterior_communicating'],
    'eca': ['artery.carotid.external.right.left', 'artery.carotid.external.right'],
    'vertebrobasilar': ['artery.posterior.vertebral_left', 'artery.posterior.vertebral_right',
                       'artery.posterior.basilar', 'artery.posterior.anterior_spinal'],
    'mma': ['artery.eca.maxillary.mma.right.left', 'artery.eca.maxillary.mma.right'],
    'maxillary': ['artery.eca.maxillary.right.left', 'artery.eca.maxillary.right'],
}

def eligible(s):
    return s['system'] == 'artery' and s.get('displayGroup') != 'anastomoses'

edges = collections.defaultdict(set)
for s in by_id.values():
    if eligible(s):
        for parent in (s.get('parent'), s.get('segmentOf')):
            if parent in by_id and eligible(by_id[parent]):
                edges[parent].add(s['id'])
for r in manifest['relationships']:
    if r['type'] in ('branches_to', 'has_segment') and eligible(by_id[r['from']]) and eligible(by_id[r['to']]):
        edges[r['from']].add(r['to'])

resolved = {}
for key, roots in seeds.items():
    assert all(root in by_id for root in roots)
    seen = set()
    queue = list(roots)
    while queue:
        sid = queue.pop()
        if sid in seen:
            continue
        seen.add(sid)
        queue.extend(edges[sid])
    resolved[key] = sorted(sid for sid in seen if by_id[sid].get('asset'))
    assert resolved[key], key
    print(key, len(resolved[key]), collections.Counter(by_id[sid]['side'] for sid in resolved[key]))

output = ROOT / 'src/presetVessels.json'
output.write_text(json.dumps(resolved, indent=2) + '\n')
(ROOT / 'public/anatomy/preset-vessels.json').write_text(json.dumps({
    'schemaVersion': 1, 'geometryCheckpoint': '0.9.67-batch2-continuation',
    'rootIds': seeds, 'vesselIds': resolved,
    'sidePolicy': 'Requested side plus shared midline vessels; both includes all sides.',
    'excluded': ['veins', 'potential anastomosis overlays', 'course landmarks'],
}, indent=2) + '\n')
