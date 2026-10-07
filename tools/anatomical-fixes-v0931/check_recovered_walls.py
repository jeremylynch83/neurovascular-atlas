"""Reject newly introduced non-adjacent self-intersections after wall recovery."""
import sys, json
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'anatomical-fixes-v0929'))
from geometry import *
OUT = ROOT.parent / 'corrections-work'; C = OUT / 'candidate-final'
revision = json.loads((C/'revision.json').read_text())

def self_pairs(v, f):
    pd = poly(v, f)
    col = vtk.vtkCollisionDetectionFilter()
    col.SetInputData(0, pd); col.SetInputData(1, pd)
    transform = vtk.vtkTransform()
    col.SetTransform(0, transform); col.SetTransform(1, transform)
    col.SetCollisionModeToAllContacts(); col.Update()
    if not col.GetNumberOfContacts(): return set()
    left = vtk_to_numpy(col.GetContactCells(0))
    right = vtk_to_numpy(col.GetContactCells(1))
    # Labels may contain duplicate vertices at seams. Adjacency is geometric.
    _, ids = np.unique(v.astype('<f4'), axis=0, return_inverse=True)
    faces = ids[f]
    nonadjacent = ~np.any(faces[left,:,None] == faces[right,None,:], axis=(1,2))
    pairs = np.sort(np.column_stack([left[nonadjacent],right[nonadjacent]]), axis=1)
    return set(map(tuple, np.unique(pairs, axis=0)))

checks = []
for name in sorted(revision['roundWallRecovery']['roundNodes']):
    m = meshes[name]; v = np.fromfile(C/(name+'.positions.bin'),'<f4').reshape(-1,3)
    before_v = np.fromfile(OUT/'candidate'/(name+'.positions.bin'),'<f4').reshape(-1,3)
    before = self_pairs(before_v, m.f); after = self_pairs(v, m.f)
    introduced = sorted(after-before)
    entry = {'node': name, 'placementStageNonAdjacentContactPairs':len(before),
             'candidateNonAdjacentContactPairs':len(after),
             'newNonAdjacentContactPairs':len(introduced),
             'examples':[[int(a),int(b)] for a,b in introduced[:20]], 'passed':not introduced}
    checks.append(entry); print('SELF',entry,flush=True)
report = {'release':'0.9.31','passed':all(r['passed'] for r in checks),'checks':checks,
          'method':'VTK all-contact triangle collision, excluding faces sharing any identical-coordinate vertex. Only the five round-wall recovered meshes are tested here; the preceding placement field is separately checked. Existing folds at ostia are retained; their repair is outside this crossing correction.'}
(C/'recovered-walls.json').write_text(json.dumps(report,indent=2)+'\n')
print('PASSED',report['passed'],flush=True)
