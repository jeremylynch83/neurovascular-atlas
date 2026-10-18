"""Fill only four small native wall gaps, without moving any source vertex.

Usage: python3 tools/tentorial-attachment-v0.9.92/repair.py WORK
WORK/decoded must contain the v0.9.91 decoded models. No runtime dependency.
"""
import sys, json
from pathlib import Path
from collections import defaultdict
import numpy as np
from scipy.sparse import coo_matrix
from scipy.sparse.csgraph import connected_components

W = Path(sys.argv[1]).resolve()
D = W / 'decoded'
OUT = W / 'candidate'
OUT.mkdir(exist_ok=True)

def mesh(name):
    return (np.fromfile(D / (name + '.positions.bin'), '<f4').reshape(-1, 3).astype(float),
            np.fromfile(D / (name + '.indices.bin'), '<u4').reshape(-1, 3))

def edges(v, f):
    u, inv = np.unique(v, axis=0, return_inverse=True)
    result = defaultdict(list)
    for t in inv[f]:
        for a, b in zip(t, np.roll(t, -1)):
            if a != b:
                result[tuple(sorted([int(a), int(b)]))].append((int(a), int(b)))
    return u, result

def signed_area(a, b, c):
    ab, ac = b-a, c-a
    return ab[0]*ac[1]-ab[1]*ac[0]

def triangulate(points):
    # Ear clipping in the local best-fit plane. The four accepted gaps have
    # simple projected polygons; all output vertices are existing coordinates.
    _, _, basis = np.linalg.svd(points-points.mean(0), full_matrices=False)
    xy = (points-points.mean(0)) @ basis[:2].T
    sign = np.sign(sum(signed_area(np.zeros(2), a, b)
                       for a, b in zip(xy, np.roll(xy, -1, axis=0))))
    assert sign
    remaining = list(range(len(points)))
    triangles = []
    while len(remaining) > 3:
        ears = []
        for j, b in enumerate(remaining):
            a, c = remaining[j-1], remaining[(j+1) % len(remaining)]
            area = sign*signed_area(xy[a], xy[b], xy[c])
            if area <= 1e-12:
                continue
            inside = False
            for k in remaining:
                if k in [a, b, c]:
                    continue
                if min(sign*signed_area(xy[a], xy[b], xy[k]),
                       sign*signed_area(xy[b], xy[c], xy[k]),
                       sign*signed_area(xy[c], xy[a], xy[k])) >= -1e-12:
                    inside = True
            if not inside:
                ears.append((np.linalg.norm(points[a]-points[c]), j, [a,b,c]))
        assert ears, 'Non-simple or degenerate patch polygon'
        _, j, t = min(ears)
        triangles.append(t)
        remaining.pop(j)
    triangles.append(remaining)
    return np.array(triangles)

rows = []
for side in ['left', 'right']:
    names = ['Tentorial marginal '+side, 'Dorsal meningeal '+side,
             'Meningohypophyseal trunk '+side]
    data = [mesh(n) for n in names]
    offsets = np.r_[0, np.cumsum([len(v) for v, _ in data])]
    v = np.vstack([v for v, _ in data])
    f = np.vstack([f+offsets[i] for i, (_, f) in enumerate(data)])
    u, ee = edges(v, f)
    assert all(len(e) <= 2 for e in ee.values())
    assert all(len(e) != 2 or e[0] == e[1][::-1] for e in ee.values())
    boundary = np.array([e[0] for e in ee.values() if len(e) == 1])
    graph = coo_matrix((np.ones(len(boundary)*2),
             (np.r_[boundary[:,0],boundary[:,1]], np.r_[boundary[:,1],boundary[:,0]])),
             shape=(len(u),len(u)))
    _, lab = connected_components(graph)
    # Explicit, bounded candidate selection, not an automatic mesh-hole filler.
    target = np.array([-15.66,-50.65,66.60] if side == 'left' else [15.3,-51.75,65.5])
    selected = []
    for k in np.unique(lab[np.unique(boundary)]):
        bd = boundary[lab[boundary[:,0]] == k]
        ids = np.unique(bd)
        if len(ids) > 6 or np.linalg.norm(u[ids].mean(0)-target) > .5:
            continue
        selected.extend(map(tuple, bd))
    assert len(selected) == (6 if side == 'left' else 9)
    # Split the right figure-of-eight boundary into its two simple cycles.
    unused = set(selected)
    loops = []
    while unused:
        a,b = min(unused)
        unused.remove((a,b))
        trail = [a,b]
        while True:
            if trail[-1] in trail[:-1]:
                j = trail[:-1].index(trail[-1])
                loops.append(trail[j:-1][::-1]) # oppose source half-edges
                trail = trail[:j+1]
            options = sorted(e for e in unused if e[0] == trail[-1])
            if not options:
                break
            a,b = options[0]
            unused.remove((a,b))
            trail.append(b)
        assert len(trail) == 1
    assert sorted(map(len,loops)) == ([6] if side == 'left' else [3,3,3])
    source, original_faces = data[0]
    points = source.tolist()
    lookup = {tuple(p): i for i,p in enumerate(points)}
    added_faces, patches, appended = [], [], []
    for loop in loops:
        polygon = u[loop]
        local = []
        for p in polygon:
            key = tuple(p)
            if key not in lookup:
                lookup[key] = len(points)
                points.append(p.tolist())
                owners = [n for n,(vv,_) in zip(names[1:],data[1:])
                          if np.any(np.all(vv==p,axis=1))]
                assert owners
                appended.append({'index':lookup[key], 'coordinate':p.tolist(), 'normalSource':owners[0]})
            local.append(lookup[key])
        tris = np.array(local)[triangulate(polygon)]
        area = np.linalg.norm(np.cross(np.array(points)[tris[:,1]]-np.array(points)[tris[:,0]],
                                     np.array(points)[tris[:,2]]-np.array(points)[tris[:,0]]),axis=1)/2
        assert min(area)>1e-9
        added_faces.extend(tris.tolist())
        patches.append({'boundaryCoordinates':polygon.tolist(), 'triangles':tris.tolist(),
                        'areaMm2':float(area.sum()),'maximumSpanMm':float(np.linalg.norm(polygon[:,None]-polygon,axis=2).max())})
    p = np.array(points,dtype='<f4')
    g = np.vstack([original_faces,added_faces]).astype('<u4')
    p.tofile(OUT/(names[0]+'.positions.bin'))
    g.tofile(OUT/(names[0]+'.indices.bin'))
    np.array(added_faces,dtype='<u4').tofile(OUT/(names[0]+'.patch-indices.bin'))
    # The combined native surface must gain no nonmanifold or misoriented edge,
    # and every selected boundary edge must now have its opposite partner.
    vv = np.vstack([p, data[1][0], data[2][0]])
    ff = np.vstack([g, data[1][1]+len(p), data[2][1]+len(p)+len(data[1][0])])
    uu, post = edges(vv,ff)
    assert all(len(e)<=2 and (len(e)!=2 or e[0]==e[1][::-1]) for e in post.values())
    canonical = {tuple(x):i for i,x in enumerate(uu)}
    for a,b in selected:
        x,y = canonical[tuple(u[a])],canonical[tuple(u[b])]
        assert len(post[tuple(sorted([x,y]))])==2
    row = {'node':names[0], 'passed':True, 'sourceVerticesUnmoved':len(source),
           'sourceTrianglesRetained':len(original_faces), 'appendedVertices':appended,
           'newTriangles':len(added_faces), 'patches':patches,
           'closedBoundaryEdges':len(selected), 'maximumDisplacementMm':0.,
           'combinedNonManifoldEdges':0,'combinedMisorientedEdges':0}
    rows.append(row)
    print(names[0],len(appended),'added vertices',len(added_faces),'triangles',flush=True)
(W/'patches.json').write_text(json.dumps({'release':'0.9.92','changes':rows},indent=2)+'\n')
