"""Measure the delivered labelled vessel walls against their anatomical targets.

This baseline audit reports sampled unsigned distances, never invented centrelines
or an inside/outside classification from open atlas meshes.
"""
import argparse, csv, hashlib, io, json, zipfile
from collections import Counter
from pathlib import Path
import numpy as np
import trimesh, vtk
from build_targets import poly

APP = Path(__file__).resolve().parents[2]
PUB = APP / 'public/anatomy'

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--baseline', type=Path, required=True)
    args = parser.parse_args()
    manifest = json.loads((APP / 'anatomy/generated/complete_manifest.json').read_text())
    rows = {s['id']: s for s in manifest['structures']}
    brain = trimesh.load(PUB / 'models/brain-context.glb', force='scene', process=False)
    assets = {'models/complete-circulation.glb': '.authoring/arteries-v0.9.14.glb',
              'models/venous.glb': '.authoring/veins-v0.9.14.glb'}
    vascular = {file: trimesh.load(APP / decoded, force='scene', process=False) for file, decoded in assets.items()}
    hashes = {file: hashlib.sha256((PUB / file).read_bytes()).hexdigest() for file in assets}
    retained = {}
    with zipfile.ZipFile(args.baseline) as archive:
        old = json.loads(archive.read('anatomy/generated/complete_manifest.json'))
        for s in old['structures']:
            if s['system'] != 'brain':
                current = {k:v for k,v in rows[s['id']].items() if k != 'vesselCourse'}
                assert s == current, f'Baseline catalogue changed: {s["id"]}'
        for file in ['complete-circulation', 'complete-anastomoses', 'venous', 'craniofacial']:
            path = f'public/anatomy/models/{file}.glb'
            prior = hashlib.sha256(archive.read(path)).hexdigest()
            assert prior == hashlib.sha256((APP / path).read_bytes()).hexdigest(), path
            retained[path] = prior
        old_brain = trimesh.load(io.BytesIO(archive.read('public/anatomy/models/brain-context.glb')),
                                  file_type='glb', force='scene', process=False)
        assert all(np.array_equal(m.vertices, brain.geometry[k].vertices) and
                   np.array_equal(m.faces, brain.geometry[k].faces) for k,m in old_brain.geometry.items())
        old_registration = old['brainRegistration']
        assert old_registration['matrixFromSourceOrientation'] == manifest['brainRegistration']['matrixFromSourceOrientation']
    locations = {}
    meshes = {}
    def vessel_mesh(identifier):
        if identifier not in meshes:
            asset = rows[identifier]['asset']
            scene = vascular[asset['file']]
            transform, geometry = scene.graph[asset['node']]
            m = scene.geometry[geometry].copy()
            m.apply_transform(transform)
            meshes[identifier] = m
        return meshes[identifier]

    def attachment_geometry(identifier):
        r = rows.get(identifier, {})
        if r.get('asset') and r['asset']['file'] in vascular: return [identifier]
        # Match the engine's segment ownership, without using unrelated branches.
        return [s['id'] for s in rows.values() if s.get('segmentOf') == identifier
                and s.get('asset') and s['asset']['file'] in vascular]

    attachment_locators = {}
    attachment_gaps = {}
    def junction_gap(source, target):
        key = (source, target)
        if key not in attachment_gaps:
            ids = attachment_geometry(target)
            if not ids:
                attachment_gaps[key] = {'targetId': target, 'status': 'no-labelled-parent-surface'}
            else:
                if target not in attachment_locators:
                    data = poly(trimesh.util.concatenate([vessel_mesh(k) for k in ids]))
                    loc = vtk.vtkStaticCellLocator(); loc.SetDataSet(data); loc.BuildLocator()
                    attachment_locators[target] = loc
                m = vessel_mesh(source)
                # Include every vertex for the attachment screen; the result
                # remains a minimum vertex-to-triangle distance, not patency.
                d = distances(m.vertices, attachment_locators[target])
                attachment_gaps[key] = {'targetId': target, 'targetGeometryIds': ids,
                    'status': 'surface-proximity-measured', 'minimumVertexToSurfaceGapMm': float(d.min()),
                    'sourceVertexCount': len(m.vertices), 'patencyVerified': False}
        return attachment_gaps[key]
    def locator(ids):
        key = tuple(sorted(ids))
        if key not in locations:
            data = poly(trimesh.util.concatenate([brain.geometry[k] for k in key]))
            loc = vtk.vtkStaticCellLocator()
            loc.SetDataSet(data)
            loc.BuildLocator()
            locations[key] = loc
        return locations[key]
    def distances(points, loc):
        result = []
        q = [0.,0.,0.]
        cell, sub, d = vtk.reference(0), vtk.reference(0), vtk.reference(0.)
        for p in points:
            loc.FindClosestPoint(p, q, cell, sub, d)
            result.append(float(d)**.5)
        return np.array(result)
    def stats(d):
        return {'minimumMm':float(d.min()),'medianMm':float(np.median(d)),
                'p95Mm':float(np.quantile(d,.95)),'maximumMm':float(d.max())}
    def line_distances(points, stations):
        a, b = stations[:-1], stations[1:]
        v = b-a
        t = np.clip(np.sum((points[:,None,:]-a)*v,axis=2)/np.sum(v*v,axis=1),0,1)
        return np.linalg.norm(points[:,None,:]-(a+t[:,:,None]*v),axis=2).min(axis=1)

    audit = []
    initial = {'vein.straight','vein.anterior_pontomesencephalic','vein.anterior_pontine','vein.anterior_medullary',
               'artery.anterior.central_left','artery.anterior.central_right'}
    for s in manifest['structures']:
        if 'vesselCourse' not in s: continue
        c = s['vesselCourse']
        record = {'id':s['id'],'name':s['name'],'side':s['side'],'scope':c['scope'],
                  'status':c['reviewStatus'],'modes':[r['mode'] for r in c['segments']],
                  'targetStructureIds':c['targetStructureIds'],'missingTargets':c['missingTargets'],
                  'attachments':c['attachments'],'fittingPerformed':False}
        if c['scope'] != 'intracranial':
            record['status']='retained-baseline'
            record['evidence']='Catalogue and vascular asset match the delivered v0.9.14 baseline exactly.'
            audit.append(record)
            continue
        asset = s['asset']
        mesh = vessel_mesh(s['id'])
        assert np.isfinite(mesh.vertices).all()
        wall = mesh.vertices[::max(1,len(mesh.vertices)//512)]
        centroids = mesh.triangles_center[::max(1,len(mesh.faces)//512)]
        sample = np.concatenate([wall,centroids])
        record['geometry']={'asset':asset,'assetSha256':hashes[asset['file']],
            'boundsMm':mesh.bounds.tolist(),'vertices':len(mesh.vertices),'triangles':len(mesh.faces),'sampledWallPoints':len(sample)}
        joins = list(dict.fromkeys(([s['parent']] if s.get('parent') else []) +
            [r['to'] for r in c['attachments']['outgoing'] if r['type']=='drains_to'] +
            [r['from'] for r in c['attachments']['incoming'] if r['type']=='branches_to']))
        record['attachmentSurfaceProximity'] = [junction_gap(s['id'], target) for target in joins]
        if c['targetStructureIds']:
            d = distances(sample, locator(c['targetStructureIds']))
            record['targetWallDistance'] = stats(d)
        if s['id']=='vein.straight':
            stations=np.array(rows['brain.landmark.falcotentorial']['landmark']['course'])
            record['attachmentLineWallDistance']=stats(line_distances(sample,stations))
        if s['id'].startswith('artery.anterior.central_') and 'cortical' not in s['id']:
            target='brain.central-sulcus.'+s['side']
            record['centralSulcusWallDistance']=stats(distances(sample,locator([target])))
        if s['id'] in initial:
            record['status']='requires-fitting'
            record['evidence']='Initial correction target from anatomical review; actual delivered wall distances recorded against the registered surface or attachment guide.'
        elif c['missingTargets']:
            record['evidence']='A complete route cannot be specified until the listed target or entry boundaries are reviewed.'
        else:
            record['evidence']='Named anatomical rule and sampled delivered wall distances; individual course and segment boundaries await anatomical review.'
        record['distanceInterpretation']='Unsigned sampled vessel-wall distance to named atlas reference surfaces; no inference of containment, patency or clinical accuracy.'
        audit.append(record)
    report={'release':'0.9.15','baseline':'Delivered v0.9.14, based on v0.9.13',
        'baselineZipSha256':hashlib.sha256(args.baseline.read_bytes()).hexdigest(),
        'retainedAssets':retained,'retainedBrainMeshesExact':len(old_brain.geometry),
        'newBrainTargets':len(brain.geometry)-len(old_brain.geometry),'overallRegistrationRetained':True,
        'brainAdjustmentsApplied':[],'statusCounts':dict(Counter(r['status'] for r in audit)),
        'method':'Actual decoded GLB node geometry with world transforms. Uniformly strided vertices and triangle centroids, up to approximately 1024 wall samples per intracranial label. VTK closest triangle distances to named target surfaces.',
        'limitations':['Sampled unsigned distance is not an exhaustive intersection or containment test.',
            'Attachment screens measure minimum vertex-to-triangle surface gaps, not lumen patency or shared junction topology. Catalogue relationships alone are not physical joins.',
            'Delivered labelled geometry is the authoritative radius/shape baseline; no fabricated centreline or numerical radius profile is substituted.',
            'Individual segment boundaries and tissue entry sites require review before fitting.',
            'Retained-baseline means unchanged, not independently verified anatomical correctness.'],
        'vessels':audit}
    dest=APP/'docs/validation/anatomical-audit-v0.9.15.json'
    dest.write_text(json.dumps(report,indent=2,ensure_ascii=False)+'\n')
    csv_path=APP/'docs/validation/anatomical-audit-v0.9.15.csv'
    with csv_path.open('w',newline='') as f:
        writer=csv.writer(f)
        writer.writerow(['ID','Name','Side','Scope','Status','Modes','Target wall median mm','Target wall p95 mm','Missing targets'])
        for r in audit:
            d=r.get('targetWallDistance',{})
            writer.writerow([r['id'],r['name'],r['side'],r['scope'],r['status'],'; '.join(r['modes']),d.get('medianMm',''),d.get('p95Mm',''),'; '.join(r['missingTargets'])])
    lines=['# Anatomical baseline audit v0.9.15','',
        'Stages 1 and 2 establish anatomical targets and course specifications. Vessel surfaces have not been fitted.', '',
        f"{len(audit)} vascular labels audited; {sum(r['scope']=='intracranial' for r in audit)} intracranial course specifications. The four skull/vascular assets, existing vascular catalogue and original 172 brain meshes are retained exactly.", '',
        '## First fitting targets','',
        '| Vessel | Target | Median wall distance mm | 95th percentile mm |',
        '| --- | --- | ---: | ---: |']
    for r in audit:
        if r['id'] not in initial:continue
        d=r.get('attachmentLineWallDistance',r.get('centralSulcusWallDistance',r.get('targetWallDistance',{})))
        lines.append(f"| {r['name']} | {'Falcotentorial line' if r['id']=='vein.straight' else 'Central sulcus' if 'central_' in r['id'] else 'Brainstem surface'} | {d['medianMm']:.2f} | {d['p95Mm']:.2f} |")
    lines+=['','These are sampled unsigned distances of the displayed vessel wall to the atlas target, not required displacement or a centreline tolerance.','','## Review state','']
    lines += [f'- {k}: {v}' for k,v in report['statusCounts'].items()]
    lines += ['', '## Remaining target gaps','']
    gaps=Counter(k for r in audit for k in r['missingTargets'])
    lines += [f'- {k}: {v} vascular labels.' for k,v in gaps.items()]
    lines += ['', '## Limits of this audit',''] + ['- '+x for x in report['limitations']]
    (APP/'docs/ANATOMICAL_AUDIT_v0.9.15.md').write_text('\n'.join(lines)+'\n')
    print(json.dumps({'vessels':len(audit),'statusCounts':report['statusCounts'],'baselineAssetsExact':True,
                      'brainMeshesExact':len(old_brain.geometry),'newTargets':report['newBrainTargets']}))

if __name__=='__main__':
    main()
