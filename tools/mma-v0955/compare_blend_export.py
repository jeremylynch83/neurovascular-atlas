"""Compare the upstream Blender master with the verified original FBX.

Uses only the source axis conversion and unit conversion, never a fitted map.
"""
import json
import sys
from pathlib import Path
import numpy as np
from scipy.spatial import cKDTree
import hashlib

work = Path(sys.argv[1]).resolve()
records = json.loads((work / 'upstream-blend/extraction.json').read_text())
rows = []
for record in records:
    if not record['found']:
        raise ValueError('Missing source label: ' + record['sourceLabel'])
    name = record['node']
    b = np.fromfile(work / 'upstream-blend' / (name + '.positions.f64'), '<f8').reshape(-1, 3)
    # Blender native axes: +X left, +Y posterior, +Z superior, metres.
    # FBX extraction axes: +X left, +Y superior, +Z anterior, millimetres.
    b = b[:, [0, 2, 1]] * [1000, 1000, -1000] - [0, 1620, 0]
    a = np.fromfile(work / 'source' / (name + '.positions.f64'), '<f8').reshape(-1, 3)
    distance = np.concatenate([cKDTree(a).query(b)[0], cKDTree(b).query(a)[0]])
    f = np.fromfile(work / 'source' / (name + '.indices.bin'), '<u4').reshape(-1, 3)
    g = np.fromfile(work / 'upstream-blend' / (name + '.indices.bin'), '<u4').reshape(-1, 3)
    rows.append(dict(node=name, sourceLabel=record['sourceLabel'],
                     fbxVertices=len(a), blendVertices=len(b),
                     fbxTriangles=len(f), blendTriangles=len(g),
                     medianSymmetricVertexDistanceMm=float(np.median(distance)),
                     maximumSymmetricVertexDistanceMm=float(distance.max()),
                     modifiers=record['modifiers']))
archive = Path(sys.argv[2]).resolve()
sha = hashlib.sha256(archive.read_bytes()).hexdigest()
report = dict(method='Baked original object transforms. Source-only axis and metre-to-millimetre conversion. No fitting, smoothing, scaling correction, or deformation.',
              upstreamRepository='https://github.com/Z-Anatomy/Models-of-human-anatomy',
              upstreamArchiveCommit='bb293be456f6d2245191f37752d14ec76894740d',
              archiveSha256=sha, records=rows,
              selectedMeshes=len(rows),
              maximumSymmetricVertexDistanceMm=max(r['maximumSymmetricVertexDistanceMm'] for r in rows),
              vertexCountsMatch=all(r['fbxVertices']==r['blendVertices'] for r in rows),
              triangleCountsMatch=all(r['fbxTriangles']==r['blendTriangles'] for r in rows),
              noSourceModifiers=all(not r['modifiers'] for r in rows))
(work / 'upstream-export-comparison.json').write_text(json.dumps(report, indent=2))
print(json.dumps({k:v for k,v in report.items() if k!='records'}, indent=2))
