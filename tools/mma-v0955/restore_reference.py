"""Remove the rejected cortical deformation from an isolated candidate.

Restore the exact accepted buffers for the cerebral reference and its vascular
assignment, then invalidate every inherited candidate acceptance report.
"""
import json
import sys
import shutil
import hashlib
from pathlib import Path

work = Path(sys.argv[1]).resolve()
candidate = work / 'candidate'
baseline = work / 'decoded'
revision = json.loads((candidate / 'revision.json').read_text())
restored = []
kept = []
for row in revision['changed']:
    if row.get('field') != 'cortical-reference':
        kept.append(row)
        continue
    name = row['node']
    hashes = {}
    for suffix in ['positions.bin', 'indices.bin', 'normals.bin']:
        src = baseline / (name + '.' + suffix)
        dst = candidate / src.name
        if src.exists():
            shutil.copyfile(src, dst)
            assert src.read_bytes() == dst.read_bytes()
            hashes[suffix] = hashlib.sha256(dst.read_bytes()).hexdigest()
        elif dst.exists():
            dst.unlink()
    restored.append(dict(node=name, file=row['file'], baselineHashes=hashes))
revision.update(release='0.9.55', changed=kept,
                status='unreleased-reference-correction-blocked',
                method='Retained MMA course and paired-vein experiments. Removed rejected cortical deformation and restored the exact accepted cerebral and vascular buffers. Original source reference verified independently. No app assets exported.')
(candidate / 'revision.json').write_text(json.dumps(revision, indent=2))
inherited = candidate / 'superseded-v0954-reports'
inherited.mkdir(exist_ok=True)
reports = ['acceptance.json', 'self-intersections.json', 'brain-self-intersections.json',
           'arterial-self-intersections.json', 'venous-self-intersections.json',
           'mma-contacts.json', 'paired-veins-validation.json', 'receiver-neighbour-validation.json',
           'field-validation.json', 'smooth-field-validation.json']
for filename in reports:
    path = candidate / filename
    if path.exists():
        shutil.move(path, inherited / filename)
report = dict(status='restored-exact-baseline', restoredMeshes=len(restored),
              records=restored, publicAssetsChanged=False,
              sourceReferenceCorrectionAccepted=False,
              inheritedAcceptanceInvalidated=True)
(candidate / 'reference-restoration.json').write_text(json.dumps(report, indent=2))
print('Restored exact baseline buffers for', len(restored), 'meshes')
