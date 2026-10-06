"""Stage a connected skin fit, pinning exact outlet vertices rather than voxels.

All selected labels share one displacement unknown at each coincident skin
vertex. This avoids fixing a whole 2 mm cell around an unrelated collector.
The result is a trial until independent wall and shape checks accept it.
"""
import json
import numpy as np
import trimesh
import vtk
from scipy.sparse import coo_matrix, eye, vstack
from scipy.sparse.linalg import lsqr
from scipy.optimize import lsq_linear
from scipy.spatial import cKDTree
from scipy.interpolate import PchipInterpolator
from scipy.ndimage import gaussian_filter1d
from fit_vessels import APP, read_glb, mesh_records, ray_tree, hits, curve_from_mesh
from reconcile_brainstem import ANTERIOR, TRANSVERSE, sha
from fit_brainstem_shear import SELECTED
from refine_context_skin import subdivide, save_replaced
from build_targets import poly

WORK = APP / '.authoring/brainstem21-skin'
KEYS = SELECTED | {'vein.posterior_communicating'} | {
    f'vein.{name}.{side}' for name in ['basal', 'lateral_mesencephalic']
    for side in ['left', 'right']}
PRIMARY = set(ANTERIOR + TRANSVERSE + ['vein.posterior_communicating', 'vein.anterior_spinal'])

def main():
    WORK.mkdir(parents=True, exist_ok=True)
    path = APP / '.authoring/brainstem19/veins-baseline.glb'
    doc, data = read_glb(path)
    records = mesh_records(doc, data)
    if (WORK/'veins-source.glb').exists():
        rd, rb = read_glb(WORK/'veins-source.glb')
        rr = mesh_records(rd,rb)
        refined = {k:(rr[k]['old'],rr[k]['faces']) for k in KEYS}
    else:
        refined = subdivide(records, KEYS, .65)
    source = {k: (p, f, trimesh.Trimesh(p, f, process=False).vertex_normals)
              for k, (p, f) in refined.items()}
    save_replaced(WORK / 'veins-source.glb', doc, data, source)
    names = sorted(KEYS)
    vertices = np.concatenate([refined[k][0] for k in names])
    _, original, inverse = np.unique(np.round(vertices, 5), axis=0,
                                    return_index=True, return_inverse=True)
    points = vertices[original]
    offsets = np.r_[0, np.cumsum([len(refined[k][0]) for k in names])]
    faces = np.concatenate([inverse[offsets[i]:offsets[i+1]][refined[k][1]]
                            for i, k in enumerate(names)])
    edges, edge_counts = np.unique(np.sort(np.concatenate([faces[:,[0,1]], faces[:,[1,2]],
                                             faces[:,[2,0]]]), axis=1), axis=0, return_counts=True)
    outside = np.concatenate([r['old'] for k, r in records.items() if k not in KEYS])
    fixed = cKDTree(outside).query(points)[0] < 2e-5
    # Refined vertices on a selected-to-retained boundary also stay fixed.
    # Coincidence with original retained vertices alone would miss these.
    fixed[np.unique(edges[edge_counts == 1])] = True
    # The caudal spinal end has no modelled cord; retain its original position.
    fixed |= points[:,2] < 0
    brain_path = WORK/'brain-trial.glb' if (WORK/'brain-trial.glb').exists() else APP/'public/anatomy/models/brain-context.glb'
    brain = trimesh.load(brain_path, process=False)
    def locator(mesh):
        loc=vtk.vtkStaticCellLocator();loc.SetDataSet(poly(mesh));loc.BuildLocator();return loc
    stem = locator(trimesh.util.concatenate([m for k, m in brain.geometry.items()
                  if any(t in k for t in ['pons.', 'medulla-oblongata', 'midbrain.', 'base-of-peduncle'])]))
    bones = trimesh.load(APP / '.authoring/bones-baseline.glb', process=False)
    bone = locator(trimesh.util.concatenate(list(bones.geometry.values())))
    def first(loc,a,b):
        t=vtk.reference(0.);q=[0.,0.,0.];pc=[0.,0.,0.];sub=vtk.reference(0);cell=vtk.reference(0)
        return q[1] if loc.IntersectWithLine(a,b,1e-8,t,q,pc,sub,cell) else None
    cache = {}
    def bounds(x, z):
        key = (round(float(x), 5), round(float(z), 5))
        if key not in cache:
            front = first(stem, [x, 5, z], [x, -145, z])
            bony = first(bone, [x, front + .1 if front is not None else -115, z], [x, 25, z])
            cache[key] = (front, bony)
        return cache[key]
    n = len(points)
    lower = np.full(n, -25.)
    upper = np.full(n, 30.)
    desired_sum = np.zeros(n); desired_count = np.zeros(n)
    primary_nodes = np.zeros(n, bool)
    for i, key in enumerate(names):
        ids = inverse[offsets[i]:offsets[i+1]]
        if key not in PRIMARY:
            continue
        primary_nodes[ids] = True
        axis = 0 if key in TRANSVERSE or key == 'vein.posterior_communicating' else 2
        old = trimesh.Trimesh(records[key]['old'], records[key]['faces'], process=False)
        course = curve_from_mesh(old, axis=axis, n=120)
        delta = []
        for p in course:
            front, _ = bounds(p[0], p[2])
            delta.append(0 if front is None else front + 1.3 - p[1])
        delta = gaussian_filter1d(np.array(delta), 1.5)
        function = PchipInterpolator(course[:,axis], delta)
        q = points[ids]
        wish = function(np.clip(q[:,axis], course[0,axis], course[-1,axis]))
        np.add.at(desired_sum, ids, wish)
        np.add.at(desired_count, ids, 1)
        for idx in np.unique(ids):
            p = points[idx]; front, bony = bounds(p[0], p[2])
            if front is not None and not fixed[idx]:
                lower[idx] = max(lower[idx], front + .3 - p[1])
            if bony is not None:
                upper[idx] = min(upper[idx], bony - .3 - p[1])
        print('Target', key, flush=True)
    infeasible = lower > upper
    report = {'brainSha256': sha(brain_path),
              'sourceSha256': sha(WORK/'veins-source.glb'), 'nodes': n,
              'exactFixedVertices': int(fixed.sum()),
              'incompatibleWallBounds': int(infeasible.sum())}
    if infeasible.any():
        report['incompatiblePoints'] = points[infeasible].tolist()
        (WORK/'solver.json').write_text(json.dumps(report, indent=2)+'\n')
        raise ValueError('No anterior corridor at constrained wall vertices')
    # Smooth on the connected material skin. Primary desired displacements
    # translate sections; collector displacements are interpolated to fixed ends.
    length = np.maximum(np.linalg.norm(points[edges[:,0]]-points[edges[:,1]], axis=1), .1)
    weight = 2 / length
    e = coo_matrix((np.column_stack([weight, -weight]).ravel(),
                   (np.repeat(np.arange(len(edges)), 2), edges.ravel())),
                  shape=(len(edges), n)).tocsr()
    target_weight = np.where(desired_count > 0, 1., .02)
    desired = desired_sum / np.maximum(desired_count, 1)
    a = vstack([e, eye(n).multiply(target_weight)]).tocsr()
    b = np.r_[np.zeros(len(edges)), desired * target_weight]
    unknown = ~fixed
    result = lsq_linear(a[:,unknown], b, bounds=(lower[unknown], upper[unknown]),
                        method='trf', lsmr_tol=1e-5, tol=1e-5, max_iter=50)
    delta = np.zeros(n); delta[unknown] = result.x
    q = points.copy(); q[:,1] += delta
    replacements = {}; changes = []
    for i, key in enumerate(names):
        ids = inverse[offsets[i]:offsets[i+1]]; p, f = refined[key]
        target = q[ids]; m = trimesh.Trimesh(target, f, process=False)
        replacements[key] = (target, f, m.vertex_normals)
        changes.append({'node':key,'maximumDisplacementMm':float(abs(delta[ids]).max())})
    save_replaced(WORK/'veins-trial.glb', doc, data, replacements)
    np.savez_compressed(WORK/'skin-map.npz', source=points, target=q, fixed=fixed,
                        inverse=inverse, offsets=offsets, names=names, lower=lower, upper=upper)
    report.update(success=bool(result.success), message=result.message,
                  maximumDisplacementMm=float(abs(delta).max()),
                  changes=changes, appliedToApp=False)
    (WORK/'solver.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2),flush=True)

if __name__ == '__main__':
    main()
