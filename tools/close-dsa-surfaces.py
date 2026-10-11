"""Close the projection proxies, preserving existing surface coordinates."""
import json
from collections import defaultdict, deque
import sys
from pathlib import Path
import numpy as np
import trimesh
import networkx as nx

root = Path(sys.argv[1])
result = {'schema': 1, 'entries': {}}
for file in sorted(root.glob('*.vertices')):
    key = file.name.removesuffix('.vertices')
    vertices = np.fromfile(file, '<f4').reshape(-1, 3)
    faces = np.fromfile(root / (key + '.indices'), '<u4').reshape(-1, 3)
    mesh = trimesh.Trimesh(vertices=vertices, faces=faces, process=False)
    mesh.merge_vertices(digits_vertex=8)
    mesh.update_faces(mesh.nondegenerate_faces())
    mesh.update_faces(mesh.unique_faces())
    mesh.remove_unreferenced_vertices()
    # Remove duplicate/sliver sheets at non-manifold edges before capping.
    removed = 0
    for _ in range(8):
        counts = np.bincount(mesh.edges_unique_inverse)
        bad = np.flatnonzero(counts > 2)
        if not len(bad):
            break
        remove = set()
        for edge in bad:
            adjacent = np.flatnonzero(mesh.edges_unique_inverse == edge) // 3
            # Retain the two largest surface triangles at the seam.
            adjacent = adjacent[np.argsort(mesh.area_faces[adjacent])[::-1]]
            remove.update(adjacent[2:].tolist())
        keep = np.ones(len(mesh.faces), dtype=bool)
        keep[list(remove)] = False
        removed += len(remove)
        mesh.update_faces(keep)
    mesh.fix_normals(multibody=True)
    for _ in range(12):
        signs = np.where(mesh.edges[:, 0] < mesh.edges[:, 1], 1, -1)
        winding = np.bincount(mesh.edges_unique_inverse, weights=signs)
        counts = np.bincount(mesh.edges_unique_inverse)
        bad = np.flatnonzero((counts == 2) & (winding != 0))
        if not len(bad):
            break
        remove = set()
        for edge in bad:
            adjacent = np.flatnonzero(mesh.edges_unique_inverse == edge) // 3
            remove.add(adjacent[np.argmin(mesh.area_faces[adjacent])])
        keep = np.ones(len(mesh.faces), dtype=bool)
        keep[list(remove)] = False
        mesh.update_faces(keep)
        removed += len(remove)
        mesh.fix_normals(multibody=True)
    if not mesh.is_watertight:
        counts = np.bincount(mesh.edges_unique_inverse)
        edges = mesh.edges[counts[mesh.edges_unique_inverse] == 1]
        graph = nx.DiGraph()
        graph.add_edges_from(edges.tolist())
        cap_vertices, cap_faces = [], []
        for component in nx.weakly_connected_components(graph):
            sub = graph.subgraph(component).copy()
            if not nx.is_eulerian(sub):
                raise RuntimeError(f'{key}: unbalanced boundary {[(n,sub.in_degree(n),sub.out_degree(n)) for n in sub if sub.in_degree(n)!=sub.out_degree(n)][:8]}, winding={mesh.is_winding_consistent}, counts={np.unique(counts,return_counts=True)}')
            # Split a boundary touching itself into simple loops. Each receives
            # its own centre, avoiding non-manifold fans at shared vertices.
            trail, locations = [], {}
            for u, v in nx.eulerian_circuit(sub):
                if not trail:
                    trail = [u]
                    locations = {u: 0}
                trail.append(v)
                if v in locations:
                    start = locations[v]
                    loop = trail[start:-1]
                    if len(loop) >= 3:
                        centre = len(mesh.vertices) + len(cap_vertices)
                        cap_vertices.append(mesh.vertices[loop].mean(axis=0))
                        for j, a in enumerate(loop):
                            cap_faces.append([centre, loop[(j+1) % len(loop)], a])
                    trail = trail[:start+1]
                    locations = {p: j for j, p in enumerate(trail)}
                else:
                    locations[v] = len(trail)-1
        mesh.vertices = np.vstack([mesh.vertices, cap_vertices])
        mesh.faces = np.vstack([mesh.faces, cap_faces])
        mesh.fix_normals(multibody=True)
    # Do not silently ship an invalid signed-depth surface.
    if not mesh.is_watertight or not mesh.is_winding_consistent:
        raise RuntimeError(f'{key}: projection proxy is not closed and oriented, edge counts {np.unique(np.bincount(mesh.edges_unique_inverse), return_counts=True)}')
    lookup = {tuple(p): i for i, p in enumerate(vertices)}
    extras, remap = [], []
    for p in mesh.vertices:
        existing = lookup.get(tuple(p))
        if existing is None:
            existing = len(vertices) + len(extras)
            extras.append(p.tolist())
        remap.append(existing)
    closed = np.asarray(remap, dtype=np.uint32)[mesh.faces]
    # Store a delta from the original index buffer, avoiding a second model set.
    canonical, weld = {}, []
    for p in vertices:
        coordinate = tuple(np.round(p.astype(float), 8))
        if coordinate not in canonical:
            canonical[coordinate] = len(canonical)
        weld.append(canonical[coordinate])
    weld.extend(range(len(canonical), len(canonical)+len(extras)))
    weld = np.asarray(weld)
    source = weld[faces]
    face_map = defaultdict(deque)
    for i, face in enumerate(source):
        face_map[tuple(sorted(face))].append(i)
    matched, caps = {}, []
    for face in closed:
        indices = weld[face]
        candidates = face_map.get(tuple(sorted(indices)))
        if not candidates:
            caps.extend(face.tolist())
            continue
        i = candidates.popleft()
        old = source[i].tolist()
        new = indices.tolist()
        matched[i] = new not in [old, old[1:]+old[:1], old[2:]+old[:2]]
    reverse = sum(matched.values()) > len(matched)/2
    result['entries'][key] = {'vertexCount': len(vertices), 'extra': extras,
        'reverse': reverse, 'flips': [i for i, flip in matched.items() if flip != reverse],
        'removed': sorted(set(range(len(faces))) - set(matched)), 'caps': caps,
        'faces': len(mesh.faces), 'removedSeamFaces': removed, 'volumeMm3': float(mesh.volume)}
    if len(result['entries']) % 100 == 0:
        print('Closed DSA surfaces:', len(result['entries']), flush=True)
(root / 'surfaces.json').write_text(json.dumps(result))
