"""Authoring only: append named targets from the original FBX without changing retained meshes."""
import argparse, hashlib, json, os
from pathlib import Path
import numpy as np
import trimesh, ufbx, vtk
from vtk.util.numpy_support import numpy_to_vtk, numpy_to_vtkIdTypeArray, vtk_to_numpy

APP = Path(__file__).resolve().parents[2]
SRC = APP / 'anatomy/source/brain'
TARGETS = {
    **{name + '.' + side: 'cerebral_cortex' for name in
       ['Central sulcus', 'Parieto-occipital sulcus', 'Lat_Fis-post', 'Circular sulcus of insula']
       for side in ['l', 'r']},
    **{name + '.' + side: 'deep_landmarks' for name in
       ['Putamen', 'Globus pallidus', 'Optic tract', 'Optic chiasm'] for side in ['l', 'r']},
}

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--fbx', type=Path, required=True)
    parser.add_argument('--inventory', type=Path, required=True)
    args = parser.parse_args()
    manifest = json.loads((SRC / 'source-manifest.json').read_text())
    assert hashlib.sha256(args.fbx.read_bytes()).hexdigest() == manifest['source_fbx_sha256']
    inventory = json.loads(args.inventory.read_text())
    existing = trimesh.load(SRC / 'source-orientation.glb', force='scene', process=False)
    original = {k: (v.vertices.copy(), v.faces.copy()) for k, v in existing.geometry.items()}
    fbx = ufbx.load_file(str(args.fbx))
    nodes = fbx.nodes
    held = [fbx, nodes]
    added = []
    for row in inventory:
        name = row['name']
        if name not in TARGETS or name in existing.geometry:
            continue
        node = nodes[row['index']]
        mesh = node.mesh
        vertices, faces, indices = mesh.vertices, mesh.faces, mesh.vertex_indices
        held.extend([node, mesh, vertices, faces, indices])
        matrix = node.geometry_to_world
        transform = np.array([[matrix.c0.x, matrix.c1.x, matrix.c2.x, matrix.c3.x],
                              [matrix.c0.y, matrix.c1.y, matrix.c2.y, matrix.c3.y],
                              [matrix.c0.z, matrix.c1.z, matrix.c2.z, matrix.c3.z],
                              [0, 0, 0, 1]])
        world = (np.array([(v.x, v.y, v.z) for v in vertices]) @ transform[:3, :3].T
                 + transform[:3, 3]) * manifest['unit_conversion_factor_to_mm']
        poly = vtk.vtkPolyData()
        points = vtk.vtkPoints()
        points.SetData(numpy_to_vtk(world, deep=True))
        poly.SetPoints(points)
        packed = []
        for face in faces:
            if face.num_indices >= 3:
                packed.append(face.num_indices)
                packed.extend(indices[k] for k in range(face.index_begin, face.index_begin + face.num_indices))
        cells = vtk.vtkCellArray()
        cells.SetCells(sum(f.num_indices >= 3 for f in faces),
                       numpy_to_vtkIdTypeArray(np.array(packed, dtype=np.int64), deep=True))
        poly.SetPolys(cells)
        triangulate = vtk.vtkTriangleFilter()
        triangulate.SetInputData(poly)
        triangulate.Update()
        triangles = vtk_to_numpy(triangulate.GetOutput().GetPolys().GetData()).reshape(-1, 4)[:, 1:].copy()
        if np.linalg.det(transform[:3, :3]) < 0:
            triangles = triangles[:, ::-1]
        result = trimesh.Trimesh(world, triangles, process=False)
        bounds = result.bounds.tolist()
        result.apply_translation(manifest['translation_after_conversion_mm'])
        existing.add_geometry(result, geom_name=name, node_name=name)
        record = {'name': name, 'category': TARGETS[name], 'fbx_node_index': row['index'],
                  'triangles': len(triangles), 'vertices': len(world),
                  'source_world_bounds_mm': bounds, 'source_geometry_to_world_cm': transform.tolist(),
                  'source_ancestors': row['ancestors'], 'orientation_group': 'Additional vessel targets'}
        manifest['records'].append(record)
        added.append(name)
    assert all(name in existing.geometry for name in TARGETS), 'A requested source target is absent'
    (SRC / 'source-orientation.glb').write_bytes(existing.export(file_type='glb'))
    roundtrip = trimesh.load(SRC / 'source-orientation.glb', force='scene', process=False)
    assert all(np.array_equal(v, roundtrip.geometry[k].vertices) and
               np.array_equal(f, roundtrip.geometry[k].faces) for k, (v, f) in original.items())
    manifest['detailed_mesh_count'] = len(roundtrip.geometry)
    manifest['triangle_count'] = sum(len(m.faces) for m in roundtrip.geometry.values())
    manifest['changes'] += ' v0.9.15: added 16 named sulcal/deep targets; retained source geometry unchanged.'
    (SRC / 'source-manifest.json').write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + '\n')
    print(json.dumps({'added': added, 'surfaces': len(roundtrip.geometry), 'retainedGeometryExact': True}), flush=True)
    # Keep ufbx parent wrappers alive through conversion; avoid native teardown.
    os._exit(0)

if __name__ == '__main__':
    main()
