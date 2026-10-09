"""Move the bilateral inferior labial course posteriorly, fixing both collars."""
from pathlib import Path
import sys, json, hashlib
import numpy as np
from scipy.spatial import cKDTree
import vtk
from vtk.util.numpy_support import numpy_to_vtk, numpy_to_vtkIdTypeArray, vtk_to_numpy

WORK = Path(sys.argv[1]).resolve()
DATA = WORK / 'decoded'
OUT = WORK / 'candidate'
OUT.mkdir(exist_ok=True)
def load(name):
    return (np.fromfile(DATA / (name + '.positions.bin'), '<f4').reshape(-1, 3),
            np.fromfile(DATA / (name + '.indices.bin'), '<u4').reshape(-1, 3))
def poly(v, f):
    p = vtk.vtkPolyData(); points = vtk.vtkPoints()
    points.SetData(numpy_to_vtk(v.astype(float), deep=True)); p.SetPoints(points)
    cells = vtk.vtkCellArray()
    cells.SetCells(len(f), numpy_to_vtkIdTypeArray(np.c_[np.full(len(f), 3), f].astype(np.int64).ravel(), deep=True))
    p.SetPolys(cells); return p
def shift(v):
    result = v.copy()
    t = np.clip((v[:, 1] - 10) / 18, 0, 1)
    result[:, 1] -= 6.5 * t * t * (3 - 2 * t)
    return result
def contacts(a, b):
    c = vtk.vtkCollisionDetectionFilter(); c.SetInputData(0, a); c.SetInputData(1, b)
    identity = vtk.vtkTransform(); c.SetTransform(0, identity); c.SetTransform(1, identity)
    c.SetCollisionModeToHalfContacts(); c.SetCellTolerance(1e-7); c.Update()
    return c.GetNumberOfContacts()
def locator(p):
    l = vtk.vtkStaticCellLocator(); l.SetDataSet(p); l.BuildLocator(); return l
def distances(l, vertices):
    result = []
    for point in vertices:
        q = [0., 0., 0.]; cell = vtk.reference(0); sub = vtk.reference(0); d = vtk.reference(0.)
        l.FindClosestPoint(point, q, cell, sub, d); result.append(float(d) ** .5)
    return np.asarray(result)

metadata = json.loads((DATA / 'meshes.json').read_text())
bones = [r['name'] for r in metadata if r['file'] == 'craniofacial.glb'
         and (r['name'] == 'bone.mandible' or r['name'].startswith(('tooth-3', 'tooth-4', 'mandibular-alveolar')))]
append = vtk.vtkAppendPolyData()
for name in bones: append.AddInputData(poly(*load(name)))
append.Update(); jaw = append.GetOutput(); jaw_locator = locator(jaw)
names = ['Inferior labial', 'Inferior labial left', 'Contralateral inferior labial midline']
checks = []
for name in names:
    v, f = load(name); after = shift(v)
    assert np.array_equal(v[:, [0, 2]], after[:, [0, 2]])
    # This monotone coordinate map cannot introduce self-intersections.
    assert 1 - 6.5 * 1.5 / 18 > 0
    tri = after[f]; areas = np.linalg.norm(np.cross(tri[:, 1]-tri[:, 0], tri[:, 2]-tri[:, 0]), axis=1)
    assert areas.min() > 1e-10
    before_contacts = contacts(poly(v, f), jaw); after_contacts = contacts(poly(after, f), jaw)
    assert after_contacts <= before_contacts, (name, before_contacts, after_contacts)
    distal = (np.abs(v[:, 0]) < 25) & (v[:, 1] > 26)
    before_gap = distances(jaw_locator, v[distal][::8]); after_gap = distances(jaw_locator, after[distal][::8])
    check = dict(node=name, vertices=len(v), triangles=len(f), boneContactsBefore=before_contacts,
                 boneContactsAfter=after_contacts, distalMedianClearanceBefore=float(np.median(before_gap)),
                 distalMedianClearanceAfter=float(np.median(after_gap)), maxPosteriorShift=float((v[:, 1]-after[:, 1]).max()))
    if name != names[-1]:
        parent = 'Facial left' if name.endswith('left') else 'Facial'
        pv, pf = load(parent); shared = cKDTree(pv).query(v)[0] < 1e-5
        assert shared.sum() > 100 and np.array_equal(v[shared], after[shared])
        check['fixedCollarVertices'] = int(shared.sum())
        # All moved surface triangles must remain clear of the facial parent.
        moving = np.any(np.any(after[f] != v[f], axis=2), axis=1)
        check['movedSurfaceParentContacts'] = contacts(poly(after, f[moving]), poly(pv, pf))
        assert check['movedSurfaceParentContacts'] == 0
    n = vtk.vtkPolyDataNormals(); n.SetInputData(poly(after, f)); n.SplittingOff(); n.ConsistencyOn(); n.Update()
    normals = vtk_to_numpy(n.GetOutput().GetPointData().GetNormals())
    assert np.all(np.linalg.norm(normals, axis=1) > .99)
    after.astype('<f4').tofile(OUT / (name+'.positions.bin'))
    f.tofile(OUT / (name+'.indices.bin'))
    normals.astype('<f4').tofile(OUT / (name+'.normals.bin'))
    checks.append(check)
hashes = json.loads((DATA / 'source-assets.json').read_text())
revision = dict(release='0.9.45', baselineAssetHashes=hashes, newLabels=[],
                changed=[dict(node=n, file=next(r['file'] for r in metadata if r['name']==n)) for n in names],
                checks=checks, selfIntersectionProtection='Strictly monotone posterior coordinate deformation; original topology retained.')
(OUT / 'revision.json').write_text(json.dumps(revision, indent=2)+'\n')
print(json.dumps(checks, indent=2))
