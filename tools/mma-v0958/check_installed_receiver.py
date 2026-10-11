"""Independent checks on the actual partitioned receiver buffers.

Reassemble by coordinate welding, verify one owner per exterior triangle,
and compare the boundary with the native collector. Test current scene
surfaces, including bone, without assuming old trial reports still apply.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parents[1] / 'mma-v0952'))
from common import *
from fold_engine import intersections
from scipy.sparse import coo_matrix
from scipy.sparse.csgraph import connected_components
vtk.vtkLogger.SetStderrVerbosity(vtk.vtkLogger.VERBOSITY_OFF)
rev = json.loads((OUT / 'revision.json').read_text())
changed = {r['node'] for r in rev['changed']}
reports = []
def boundary(v, f):
    edges = np.sort(np.vstack([f[:, [0, 1]], f[:, [1, 2]], f[:, [2, 0]]]), axis=1)
    edges, count = np.unique(edges, axis=0, return_counts=True)
    keys = {tuple(sorted((v[a].tobytes(), v[b].tobytes()))) for a, b in edges[count == 1]}
    return keys, int((count > 2).sum()), edges
for side in ['right', 'left']:
    receiver = 'vein.sphenoparietal.' + side
    labels = [receiver, 'vein.middle_meningeal.anterior.' + side, 'vein.middle_meningeal.posterior.' + side]
    vv, ff, offset = [], [], 0
    for n in labels:
        v, f = load(n, OUT)
        vv.append(v.astype('<f4')); ff.append(f + offset); offset += len(v)
    raw, faces = np.vstack(vv), np.vstack(ff)
    v, inv = np.unique(raw, axis=0, return_inverse=True); f = inv[faces]
    sourcev, sourcef = load(receiver); sourcev, si = np.unique(sourcev.astype('<f4'), axis=0, return_inverse=True); sourcef = si[sourcef]
    keys, nonmanifold, edges = boundary(v, f)
    sourcekeys, _, _ = boundary(sourcev, sourcef)
    canonical = np.sort(f, axis=1)
    duplicates = len(f) - len(np.unique(canonical, axis=0))
    graph = coo_matrix((np.ones(len(edges)), (edges[:, 0], edges[:, 1])), shape=(len(v), len(v))).tocsr()
    components = connected_components(graph, directed=False, return_labels=False)
    tri = v[f].astype(float)
    area = np.linalg.norm(np.cross(tri[:, 1] - tri[:, 0], tri[:, 2] - tri[:, 0]), axis=1) / 2
    folds = intersections(v.astype(float), f)
    contacts_found = []
    lo, hi = v.min(0)-.2, v.max(0)+.2
    for n in FILES:
        if n in labels: continue
        neural = n.startswith('brain.') and not n.startswith(('brain.falx', 'brain.tentorium'))
        arterial = FILES[n] in ['complete-circulation.glb', 'complete-anastomoses.glb']
        bone = n.startswith('bone.')
        if not (neural or arterial or bone): continue
        w, g = load(n, OUT) if n in changed else load(n)
        if np.any(w.max(0)<lo) or np.any(w.min(0)>hi): continue
        t = w[g]; take = np.all(t.max(1)>=lo, axis=1) & np.all(t.min(1)<=hi, axis=1)
        if not take.any(): continue
        count = contacts(v.astype(float), f, w, g[take])
        if count:
            contacts_found.append(dict(other=n, triangleContacts=count, domain='neural' if neural else 'arterial' if arterial else 'bone'))
    report = dict(side=side, labels=labels, vertices=len(v), triangles=len(f),
                  nativeBoundaryExact=keys==sourcekeys, boundaryEdges=len(keys),
                  nonManifoldEdges=nonmanifold, duplicateExteriorTriangles=duplicates,
                  connectedComponents=int(components), selfIntersectionPairs=len(folds),
                  degenerateTriangles=int((area<1e-10).sum()), contacts=contacts_found)
    report['passedGeometry'] = keys==sourcekeys and not nonmanifold and not duplicates and components==1 and not folds and not (area<1e-10).any()
    report['clearOfNeuralAndArterialSurfaces'] = not any(c['domain']!='bone' for c in contacts_found)
    report['boneRelationsReviewed'] = not any(c['domain']=='bone' for c in contacts_found)
    reports.append(report); print(json.dumps(report), flush=True)
(OUT/'installed-receiver-validation.json').write_text(json.dumps(dict(method=__doc__, results=reports),indent=2))
