"""Check native interfaces without confusing remeshing with vertex order.

Topology-preserving meshes use their original vertex IDs. For remeshed
collectors, native interface coordinates must be present exactly in the new
surface. Missing coordinates are reported as failures, never silently skipped.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parents[1] / 'mma-v0952'))
from common import *

rev = json.loads((OUT / 'revision.json').read_text())
changed = {r['node'] for r in rev['changed']}
names = sorted(FILES)
old, current, owners, remeshed, unresolved = [], [], [], [], []
for j, n in enumerate(names):
    v, f = load(n)
    q, g = load(n, OUT) if n in changed else (v, f)
    if q.shape != v.shape or not np.array_equal(f, g):
        distance, index = cKDTree(q).query(v)
        mapped = q[index]
        mapped[distance > 1e-7] = np.nan
        current.append(mapped.astype('<f4'))
        remeshed.append(n)
    else:
        current.append(q.astype('<f4'))
    old.append(v.astype('<f4'))
    owners.append(np.full(len(v), j, np.int32))
v, q, ids = np.concatenate(old), np.concatenate(current), np.concatenate(owners)
keys = np.ascontiguousarray(v).view('V12').ravel()
order = np.argsort(keys)
same = keys[order[1:]] == keys[order[:-1]]
a, b = order[:-1][same], order[1:][same]
take = ids[a] != ids[b]
a, b = a[take], b[take]
gap = np.linalg.norm(q[a] - q[b], axis=1)
rows = []
for ia, ib in sorted(set(zip(ids[a], ids[b]))):
    take = (ids[a] == ia) & (ids[b] == ib)
    gg = gap[take]
    missing = int(np.isnan(gg).sum())
    finite = gg[np.isfinite(gg)]
    rows.append(dict(a=names[ia], b=names[ib], sharedVertexPairs=int(take.sum()),
                     missingNativeCoordinates=missing,
                     maxMismatchMm=float(finite.max()) if len(finite) else None))
report = dict(method=__doc__, exactSharedInterfaces=rows,
              remeshedLabels=remeshed, missingNativeCoordinatePairs=int(np.isnan(gap).sum()),
              maxMismatchMm=float(np.nanmax(gap)),
              passedSharedCollars=bool(np.isfinite(gap).all() and (gap < 1e-7).all()))
(OUT / 'native-interface-validation.json').write_text(json.dumps(report, indent=2))
print(json.dumps({k: v for k, v in report.items() if k not in ['exactSharedInterfaces', 'method']}, indent=2))
