"""Derive version-bound, ordered anatomical guides from the registered atlas surfaces."""
from pathlib import Path
import hashlib, json
import numpy as np
import trimesh, vtk
from vtk.util.numpy_support import numpy_to_vtk, numpy_to_vtkIdTypeArray, vtk_to_numpy

APP = Path(__file__).resolve().parents[2]
PUB = APP / 'public/anatomy'
vtk.vtkLogger.SetStderrVerbosity(vtk.vtkLogger.VERBOSITY_ERROR)

def dump(path, value):
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + '\n')

def poly(mesh):
    data = vtk.vtkPolyData()
    points = vtk.vtkPoints()
    points.SetData(numpy_to_vtk(mesh.vertices, deep=True))
    data.SetPoints(points)
    cells = vtk.vtkCellArray()
    cells.SetCells(len(mesh.faces), numpy_to_vtkIdTypeArray(
        np.c_[np.full(len(mesh.faces), 3), mesh.faces].astype(np.int64).ravel(), deep=True))
    data.SetPolys(cells)
    return data

def cut(data, origin, normal):
    plane = vtk.vtkPlane()
    plane.SetOrigin(*origin)
    plane.SetNormal(*normal)
    cutter = vtk.vtkCutter()
    cutter.SetInputData(data)
    cutter.SetCutFunction(plane)
    cutter.Update()
    return cutter.GetOutput()

def main():
    manifest = json.loads((APP / 'anatomy/generated/complete_manifest.json').read_text())
    scene = trimesh.load(PUB / 'models/brain-context.glb', force='scene', process=False)
    rows = {r['id']: r for r in manifest['structures']}
    # Re-running this authoring step replaces its own stations only.
    owned = [r['id'] for r in manifest['structures'] if r.get('guideAuthoring') == 'targets-v0.9.15']
    manifest['structures'] = [r for r in manifest['structures'] if r['id'] not in owned]
    manifest['relationships'] = [r for r in manifest['relationships'] if r['from'] not in owned and r['to'] not in owned]
    for r in manifest['structures']:
        r['children'] = [k for k in r['children'] if k not in owned]
    rows = {r['id']: r for r in manifest['structures']}
    sha = hashlib.sha256((PUB / 'models/brain-context.glb').read_bytes()).hexdigest()
    registration = manifest['brainRegistration']['id']
    surfaces, locators = {}, {}
    for name, mesh in scene.geometry.items():
        surfaces[name] = poly(mesh)
        loc = vtk.vtkStaticCellLocator()
        loc.SetDataSet(surfaces[name])
        loc.BuildLocator()
        locators[name] = loc

    def binding(target, query):
        closest = [0., 0., 0.]
        cell, sub, distance = vtk.reference(0), vtk.reference(0), vtk.reference(0.)
        locators[target].FindClosestPoint(query, closest, cell, sub, distance)
        mesh = scene.geometry[target]
        tri = int(cell)
        weights = trimesh.triangles.points_to_barycentric(
            mesh.vertices[mesh.faces[[tri]]], np.array([closest]))[0]
        weights = np.clip(weights, 0, 1)
        weights /= weights.sum()
        point = weights @ mesh.vertices[mesh.faces[tri]]
        return {'structureId': target, 'triangleIndex': tri, 'barycentric': weights.tolist(),
                'position': point.tolist(), 'assetSha256': sha, 'registrationId': registration}

    def guide(identifier, name, side, targets, queries, vessel_ids, description, secondary=()):
        old = rows.get(identifier)
        base = dict(old) if old else dict(id=identifier, parent='brain.landmarks', children=[],
            system='brain', side=side, kind='structure', aliases=[], geometryStatus='placeholder',
            provenance=dict(sourceType='atlas-derived', confidence='Skull-registered atlas context; not patient-specific',
                            reviewStatus='unreviewed', sourceRefs=['source.z-anatomy-brain']))
        base.pop('surfaceAnchor', None)
        keys, points = [], []
        for i, query in enumerate(queries):
            bound = binding(targets[0], query)
            key = identifier + '.station-' + str(i + 1).zfill(2)
            station = dict(id=key, name=f'{name}, station {i + 1:02}', parent=identifier, children=[],
                system='brain', side=side, kind='structure', aliases=[], geometryStatus='placeholder',
                provenance=base['provenance'], description='Ordered atlas course station bound to the named surface.',
                surfaceAnchor=bound, guideAuthoring='targets-v0.9.15',
                landmark=dict(kind='brain-surface', status='regional', point=bound['position'], course=[],
                              connects=rows[targets[0]]['name'], contents=''))
            if secondary:
                station['secondarySurfaceAnchors'] = [binding(k, bound['position']) for k in secondary]
            manifest['structures'].append(station)
            rows[key] = station
            manifest['relationships'].append({'from': key, 'to': targets[0], 'type': 'located_on'})
            keys.append(key)
            points.append(bound['position'])
        base.update(name=name, description=description, children=keys,
                    guideAuthoring='targets-v0.9.15' if old is None else 'retained-guide',
                    landmark=dict(kind='brain-course', status='regional', point=points[0], course=points,
                                  connects=', '.join(rows[k]['name'] for k in targets),
                                  contents=', '.join(rows[k]['name'] for k in vessel_ids)),
                    vesselGuide=dict(role='course-guide', vesselNames=[rows[k]['name'] for k in vessel_ids],
                                     vesselIds=vessel_ids, surfaceStructureIds=targets, anchorIds=keys))
        if old:
            manifest['structures'][manifest['structures'].index(old)] = base
        else:
            manifest['structures'].append(base)
            rows['brain.landmarks']['children'].append(identifier)
        rows[identifier] = base
        manifest['relationships'] = [r for r in manifest['relationships']
            if not (r['from'] == identifier and r['type'] == 'located_on')]
        manifest['relationships'].append({'from': identifier, 'to': targets[0], 'type': 'located_on'})
        for vessel in vessel_ids:
            relation = {'from': vessel, 'to': identifier, 'type': 'course_landmark',
                        'note': 'Anatomical target course; existing vessel geometry has not been fitted.'}
            if not any(r['from'] == vessel and r['to'] == identifier and r['type'] == 'course_landmark'
                       for r in manifest['relationships']):
                manifest['relationships'].append(relation)
        return base

    # Medial tentorial crest on the original source midline plane. Keep both
    # leaves and the falx as independent witnesses at every station.
    T = np.array(manifest['brainRegistration']['matrixFromSourceOrientation'])
    midline_origin, midline_normal = T[:3, 3], T[:3, 0] / np.linalg.norm(T[:3, 0])
    leaves = ['brain.tentorium-cerebelli.left', 'brain.tentorium-cerebelli.right']
    medial_vertices = [m.vertices[np.abs((m.vertices - midline_origin) @ midline_normal) < 2.5]
                       for m in [scene.geometry[k] for k in leaves]]
    lower = max(v[:, 1].min() for v in medial_vertices) + .5
    upper = min(v[:, 1].max() for v in medial_vertices) - .5
    assert upper - lower > 35, 'Incomplete medial tentorial course'

    def crest(target, y):
        section = cut(surfaces[target], [0, y, 0], [0, 1, 0])
        points = vtk_to_numpy(section.GetPoints().GetData())
        hits = points[np.abs((points - midline_origin) @ midline_normal) < 2.5]
        assert len(hits), f'Missing medial tentorial section at {y}'
        return hits[np.argmax(hits[:, 2])]

    queries = [np.mean([crest(k, y) for k in leaves], axis=0) for y in np.linspace(upper, lower, 25)]
    seam = guide('brain.landmark.falcotentorial', 'Falcotentorial attachment course', 'midline',
                 ['brain.tentorium-cerebelli.left', 'brain.tentorium-cerebelli.right', 'brain.falx-cerebri'],
                 queries, ['vein.straight', 'vein.galen'],
                 'Ordered medial tentorial attachment guide from anterior to posterior. Each station is referenced to both tentorial leaves and the falx. The straight sinus follows this attachment; Galen approaches its anterior end. This is an atlas target, not a fitted sinus lumen.',
                 secondary=['brain.tentorium-cerebelli.right', 'brain.falx-cerebri'])
    seam['aliases'] = list(dict.fromkeys(seam.get('aliases', []) + ['falcotentorial junction', 'straight sinus guide']))
    distances = []
    for key in seam['vesselGuide']['anchorIds']:
        r = rows[key]
        p = np.array(r['surfaceAnchor']['position'])
        distances.append([float(np.linalg.norm(p - a['position'])) for a in r['secondarySurfaceAnchors']])
    seam['targetValidation'] = {'method': 'Upper contours of both tentorial leaves within 2.5 mm of the registered source midline; paired midpoint bound to the left leaf with independent right-leaf and falx witnesses',
        'stationCount': 25, 'rightTentoriumDistanceMm': np.array(distances)[:, 0].tolist(),
        'falxSurfaceDistanceMm': np.array(distances)[:, 1].tolist(),
        'status': 'atlas-derived-target', 'limitation': 'Finite-thickness atlas sheets; these distances describe surface agreement, not dural wall thickness or a segmented sinus lumen.'}

    # Lateral lip of the named sulcal reference, sampled inferior to superior.
    for side in ['left', 'right']:
        target = 'brain.central-sulcus.' + side
        mesh = scene.geometry[target]
        queries = []
        for z in np.linspace(mesh.bounds[0, 2] + .5, mesh.bounds[1, 2] - .5, 9):
            section = cut(surfaces[target], [0, 0, z], [0, 0, 1])
            points = vtk_to_numpy(section.GetPoints().GetData())
            queries.append(points[np.argmax(np.abs(points[:, 0] - T[0, 3]))])
        guide('brain.landmark.central-sulcus.' + side, 'Central sulcus course, ' + side,
              side, [target], queries, ['artery.anterior.central_' + side],
              'Ordered inferior-to-superior stations along the lateral lip of the central sulcal reference. The artery approaches via the Sylvian and opercular region before following the sulcus. These stations identify the target groove; they are not a completed arterial centreline.')

    # Semantic bindings for the newly imported posterior Sylvian and occipital targets.
    for side in ['left', 'right']:
        for label, target, vessel in [
            ('Posterior Sylvian region', 'brain.lat-fis-post.' + side, 'artery.anterior.mca_superior_division_' + side),
            ('Parieto-occipital sulcus region', 'brain.parieto-occipital-sulcus.' + side, 'artery.posterior.pca_parieto_occipital_' + side)]:
            m = scene.geometry[target]
            axis = 2
            queries = [m.vertices[np.argmin(abs(m.vertices[:, axis] - z))] for z in
                       np.linspace(m.bounds[0, axis] + .5, m.bounds[1, axis] - .5, 5)]
            guide('brain.landmark.' + target[6:], label + ', ' + side, side, [target], queries, [vessel],
                  'Regional ordered stations on the named atlas reference. The individual vascular approach and branches require fitting and review.')

    manifest['brainAdjustmentPolicy'] = {'scope': 'Small local translations, rotations or smooth deformations of brain structures alongside vessel fitting',
        'preserve': ['overall skull registration', 'brain shape and volume', 'neighbouring anatomical continuity', 'sulcal banks and ventricular relationships'],
        'afterAdjustment': ['recompute surface-bound guides', 'update asset revision', 'recheck affected vessels and skull clearance'],
        'bounds': 'Set per region following inspection; no universal displacement tolerance',
        'appliedAdjustments': []}
    dump(APP / 'anatomy/generated/complete_manifest.json', manifest)
    dump(PUB / 'brain-landmarks.json', {'schemaVersion': '1.1', 'registration': manifest['brainRegistration'],
         'anchors': [r for r in manifest['structures'] if r.get('landmark') and r['system'] == 'brain'],
         'surfaces': [{'id': r['id'], 'name': r['name'], 'asset': r['asset'], 'anatomy': r['anatomy']}
                      for r in manifest['structures'] if r.get('anatomy') and r.get('asset')]})
    dump(APP / 'docs/validation/anatomical-targets-v0.9.15.json', {'surfaces': len(scene.geometry),
         'falcotentorial': seam['targetValidation'], 'centralSulci': 'Bilateral original source meshes and nine ordered triangle-bound stations per side',
         'brainAdjustments': [], 'registrationRetained': True})
    print(json.dumps({'surfaces': len(scene.geometry), 'falcotentorialStations': 25,
                      'falcotentorialFalxDistanceRangeMm': [min(d[1] for d in distances), max(d[1] for d in distances)],
                      'guideCount': sum(bool(r.get('vesselGuide')) for r in manifest['structures'])}))

if __name__ == '__main__':
    main()
