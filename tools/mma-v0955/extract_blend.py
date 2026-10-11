"""Extract unchanged upstream master meshes with baked source transforms.

Run with Blender in background mode and disabled automatic script execution.
No modifiers, smoothing, fitting, or anatomical deformation is applied.
"""
import bpy
import json
import sys
from pathlib import Path
import numpy as np

work = Path(sys.argv[sys.argv.index('--') + 1]).resolve()
out = work / (sys.argv[sys.argv.index('--output-name') + 1] if '--output-name' in sys.argv else 'upstream-blend')
out.mkdir(exist_ok=True)
labels = []
filenames = [sys.argv[sys.argv.index('--labels') + 1]] if '--labels' in sys.argv else ['bones.tsv', 'brain.tsv']
for filename in filenames:
    for line in (work / 'source' / filename).read_text().splitlines():
        label, name = line.split('\t')
        labels.append((label, name))
if '--blend-path' in sys.argv:
    path = sys.argv[sys.argv.index('--blend-path') + 1]
    with bpy.data.libraries.load(path, link=False) as (available, requested):
        (out / 'available-object-names.json').write_text(json.dumps(available.objects))
        wanted = {label for label, name in labels}
        requested.objects = [n for n in available.objects if n in wanted]
    for obj in requested.objects:
        if obj is not None:
            bpy.context.scene.collection.objects.link(obj)
    bpy.context.view_layer.update()
inventory = []
for obj in bpy.data.objects:
    if obj.type != 'MESH':
        continue
    v = np.empty(len(obj.data.vertices) * 3, dtype=np.float64)
    obj.data.vertices.foreach_get('co', v)
    m = np.asarray(obj.matrix_world, dtype=float)
    w = v.reshape(-1, 3) @ m[:3, :3].T + m[:3, 3]
    inventory.append(dict(name=obj.name, vertices=len(w), matrix=m.tolist(),
                          bounds=[w.min(0).tolist(), w.max(0).tolist()],
                          modifiers=[x.type for x in obj.modifiers]))
(out / 'inventory.json').write_text(json.dumps(dict(
    sceneUnitSystem=bpy.context.scene.unit_settings.system,
    sceneUnitScale=bpy.context.scene.unit_settings.scale_length,
    objects=inventory), indent=2))

records = []
for label, name in labels:
    obj = bpy.data.objects.get(label)
    if obj is None or obj.type not in {'MESH', 'CURVE'}:
        records.append(dict(node=name, sourceLabel=label, found=False))
        continue
    evaluate = obj.type == 'CURVE' or '--evaluate' in sys.argv
    evaluated = obj.evaluated_get(bpy.context.evaluated_depsgraph_get()) if evaluate else None
    mesh = evaluated.to_mesh() if evaluate else obj.data
    mesh.calc_loop_triangles()
    v = np.empty(len(mesh.vertices) * 3, dtype=np.float64)
    mesh.vertices.foreach_get('co', v)
    m = np.asarray(obj.matrix_world, dtype=float)
    v = v.reshape(-1, 3) @ m[:3, :3].T + m[:3, 3]
    f = np.empty(len(mesh.loop_triangles) * 3, dtype=np.int32)
    mesh.loop_triangles.foreach_get('vertices', f)
    f = f.reshape(-1, 3)
    if np.linalg.det(m[:3, :3]) < 0:
        f = f[:, [0, 2, 1]]
    v.astype('<f8').tofile(out / (name + '.positions.f64'))
    f.astype('<u4').tofile(out / (name + '.indices.bin'))
    records.append(dict(node=name, sourceLabel=label, found=True, sourceObjectType=obj.type,
                        vertices=len(v), triangles=len(f), matrix=m.tolist(),
                        bounds=[v.min(0).tolist(), v.max(0).tolist()],
                        evaluated=evaluate, modifiers=[x.type for x in obj.modifiers]))
    if obj.type == 'CURVE':
        paths = []
        for spline in obj.data.splines:
            points = spline.bezier_points if spline.type == 'BEZIER' else spline.points
            paths.append(dict(type=spline.type, cyclic=spline.use_cyclic_u,
                              points=[dict(co=list(p.co), radius=p.radius,
                                           **(dict(handleLeft=list(p.handle_left), handleRight=list(p.handle_right)) if spline.type=='BEZIER' else {})) for p in points]))
        (out / (name + '.source-curves.json')).write_text(json.dumps(dict(
            matrix=m.tolist(), bevelDepth=obj.data.bevel_depth,
            bevelResolution=obj.data.bevel_resolution, resolution=obj.data.resolution_u,
            splines=paths), indent=2))
    if evaluate:
        evaluated.to_mesh_clear()
(out / 'extraction.json').write_text(json.dumps(records, indent=2))
print('Extracted', sum(r['found'] for r in records), 'of', len(records), flush=True)
