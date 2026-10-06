"""Refresh candidate metadata and prepare the lossless geometry checkpoint."""
import json,shutil,hashlib,zipfile
from pathlib import Path
import numpy as np,trimesh
from fit_vessels import APP
from reconcile_brainstem import sha

W=APP/'.authoring/posterior-round59'
OUT=APP/'deliverables/posterior-fossa-pial-review'

def main():
    surface=json.loads((W/'surface-validation.json').read_text());cross=json.loads((W/'crossing-roundness-validation.json').read_text());assert surface['passed'] and cross['passed'];hashes={k:sha(W/f'{k}-trial.glb') for k in ['brain','arteries','veins']};assert surface['hashes']==hashes;assert cross['hashes']=={k:hashes[k] for k in ['veins','arteries']}
    manifest=json.loads((W/'candidate-manifest.json').read_text());assets={};nodes={};scenes={}
    for kind in ['brain','arteries','veins']:
        path=W/f'{kind}-trial.glb';scene=trimesh.load(path,process=False);scenes[kind]=scene;assets[kind]={'file':f'models/{kind}-trial.glb','sha256':hashes[kind],'byteSize':path.stat().st_size,'nodeCount':len(scene.geometry)}
        for key,m in scene.geometry.items():nodes[key]=(kind,m)
    for r in manifest['structures']:
        node=r.get('asset',{}).get('node')
        if node not in nodes:continue
        kind,m=nodes[node];r['asset']['file']=assets[kind]['file'];a=r.get('anatomy')
        if a is not None:a['bounds']=m.bounds.tolist();a['centroid']=m.vertices.mean(0).tolist()
        course=r.get('vesselCourse')
        if course:
            course['geometry']={'file':assets[kind]['file'],'node':node};course['geometrySha256']=hashes[kind];course['brainAssetSha256']=hashes['brain'];course['candidateReviewStatus']='surface-placement-checked; anatomical-review-pending'
        if r['id']=='brain.upper-cervical-cord':
            r['name']='Upper cervical cord (illustrative)';r['anatomy']['sourceLabel']='Illustrative upper cervical continuation';r['anatomy']['surfaceRole']='illustrative-parenchymal-context';r['notes']='Illustrative continuation fitted to the supplied caudal medullary cut.';r['provenance']={'sourceType':'illustrative-continuation','reviewStatus':'anatomical-review-pending'}
        if r['id'] in ['artery.posterior.posterior_spinal_left','artery.posterior.posterior_spinal_right']:
            side=r['side'];r['parent']='artery.posterior.pica_'+side;course['attachments']['parentId']=r['parent'];course['attachments']['status']='physical-PICA-junction-checked';course['reviewStatus']='candidate-surface-checked; anatomical-review-pending'
    index={r['id']:r for r in manifest['structures']};cord=index['brain.upper-cervical-cord'];parent=index.get(cord['parent'])
    if parent and cord['id'] not in parent.setdefault('children',[]):parent['children'].append(cord['id'])
    manifest['candidateAssets']=assets;manifest['candidateHashes']=hashes;manifest['candidateStatus']={'number':59,'accepted':False,'appliedToApp':False,'surfaceChecksPassed':True,'venousCrossingChecksPassed':True,'sampledVeinFlatteningChecksPassed':True,'openTissuePartsUseTriangleChecks':True};(W/'candidate-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
    # Validate every displayed subset against the exact source positions/faces.
    metadata=json.loads((OUT/'model-review.json').read_text());rows=[]
    for group,keys in metadata['groups'].items():
        kind='brain' if group=='brain' else 'arteries' if group=='arteries' else 'veins';subset=trimesh.load(OUT/'models'/f'{group}.glb',process=False)
        for k in keys:
            a=scenes[kind].geometry[k];b=subset.geometry[k];assert np.array_equal(a.vertices,b.vertices) and np.array_equal(a.faces,b.faces),(group,k)
        rows.append({'group':group,'exactSourceLabels':len(keys),'passed':True})
    validation={'candidate':59,'passed':True,'subsetChecks':rows,'sourceHashes':hashes,'tissueSurfaceContactCount':surface['surfaceContactCount'],'wallVerticesInsideClosedTissue':surface['surfaceContainedWallVertices'],'posteriorSpinal':surface['posteriorSpinal'],'veinArteryCrossings':sum(r['triangleContactsWithArteries'] for r in cross['rows']),'veinWallVerticesInsideArteries':sum(r['wallVerticesInsideArteries'] for r in cross['rows']),'veinFlatteningChecksPassed':cross['sectionFlatteningChecksPassed'],'minimumSampledDiameterRatio':min(r['minimumDiameterToIntendedRatio'] for r in cross['rows'] if r['minimumDiameterToIntendedRatio'] is not None),'strictIsolatedAspectChecksPassed':cross['strictIsolatedAspectChecksPassed'],'reviewAccepted':False,'appliedToApp':False};(OUT/'geometry-validation.json').write_text(json.dumps(validation,indent=2)+'\n')
    for name in ['surface-validation.json','crossing-roundness-validation.json','posterior-spinal-courses.json','cord-context.json']:shutil.copyfile(W/name,OUT/name)
    (OUT/'README.txt').write_text('POSTERIOR FOSSA SURFACE VESSEL REVIEW: CANDIDATE 59\n\nRun python3 serve.py or ./view.sh, then open http://127.0.0.1:9864/. Drag to rotate; scroll to zoom. Choose arterial, venous, combined, Galenic or PICA/PSA views. Adjust tissue opacity or highlight a named vessel. The viewer works without internet or additional packages.\n\nBoth posterior spinal arteries arise from the proximal PICAs, curve onto the dorsal medulla and continue on the posterior upper-cervical surface. The previous vertebral V3 origins are closed. Surface arterial and venous courses were corrected against the supplied tissue skins. Veins retain circular swept sections and are lifted over arterial crossings. Intentional perforator and paramedian entry is retained. Clival/basilar plexus is omitted.\n\nOpaque surface views and transparent overview views are included in views/. The cord is an illustrative continuation fitted to the caudal medullary cut. The existing brainstem and cerebellar geometry is retained.\n\nThe Galenic views show posterior-fossa tributaries together with basal veins, internal cerebral veins and Galen. The internal cerebral veins also drain into Galen. Petrosal and sinus outlets are shown separately.\n\nValidation uses actual exported walls, triangle contacts and containment in closed tissue parts. Open atlas parts permit triangle-contact checks only. Sampled free vein segments preserve their intended minor diameter; bent sections may widen. Raw aspect ratios, diameter measurements and the separate strict aspect check are retained in the reports. This remains an anatomical review candidate.\n\nThe models are exact labelled subsets of the full checkpoint. Source attribution and licences accompany the files.\n')
    archive=APP/'deliverables/posterior-fossa-pial-checkpoint.zip'
    with zipfile.ZipFile(archive,'w',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
        root='posterior-fossa-pial-checkpoint/'
        for name in ['brain-trial.glb','arteries-trial.glb','veins-trial.glb','arteries-collision-solid.glb','veins-collision-solid.glb']:
            z.write(W/name,root+'models/'+name)
        for name in ['candidate-manifest.json','trial.json','surface-validation.json','crossing-roundness-validation.json','arteries-round-courses.json','veins-round-courses.json','posterior-spinal-courses.json','cord-context.json']:z.write(W/name,root+name)
        for p in sorted((APP/'tools/brain').glob('*.py')):z.write(p,root+'tools/brain/'+p.name)
        for name in ['brain-trial.glb','arteries-trial.glb','veins-trial.glb','tubular-courses.json']:z.write(APP/'.authoring/posterior-tubular55'/name,root+'inputs/source55/'+name)
        z.write(APP/'.authoring/posterior-round58/veins-round-courses.json',root+'inputs/seed58-veins.json')
        z.write(APP/'anatomy/source/venous/fitted-paths.json',root+'anatomy/source/venous/fitted-paths.json')
        z.write(APP/'deliverables/posterior-fossa-expanded-review/model-review.json',root+'deliverables/posterior-fossa-expanded-review/model-review.json')
        for name in ['THREE-LICENSE.txt','Z_Anatomy_Source_Licence.txt','SOURCE-ATTRIBUTION.txt']:z.write(OUT/name,root+name)
        z.writestr(root+'restore_authoring_inputs.py',"from pathlib import Path\nimport shutil\nr=Path(__file__).resolve().parent\ns=r/'.authoring/posterior-tubular55'\ns.mkdir(parents=True,exist_ok=True)\nfor p in (r/'inputs/source55').iterdir():shutil.copyfile(p,s/p.name)\nb=r/'.authoring/posterior-round58'\nb.mkdir(parents=True,exist_ok=True)\nfor n in ['brain-trial.glb','arteries-trial.glb','arteries-collision-solid.glb']:shutil.copyfile(r/'models'/n,b/n)\nfor n in ['cord-context.json','arteries-round-courses.json','posterior-spinal-courses.json','candidate-manifest.json']:shutil.copyfile(r/n,b/n)\nshutil.copyfile(r/'inputs/seed58-veins.json',b/'veins-round-courses.json')\nprint('Inputs restored. The final full GLBs are in models/.')\n")
        z.writestr(root+'README.txt','CANDIDATE 59: FULL GEOMETRY CHECKPOINT\n\nThe full brain, artery and vein assets are in models/. Their exact hashes and updated catalogue references are in candidate-manifest.json. The portable posterior-fossa viewer is a separate download.\n\nThe source55 input meshes, current fitted course records, native closed collision solids and authoring scripts are retained. Run python3 restore_authoring_inputs.py before using the authoring scripts. The vein reconstruction is tools/brain/smooth_canonical_surface_veins.py; it requires numpy, scipy, trimesh, vtk and manifold3d. The supplied full geometry is the exact reviewed candidate regardless of authoring environment.\n\nBoth PSAs are joined to proximal PICAs and follow the dorsal medulla and illustrative upper cervical cord. Existing tissue shape is retained. The clival plexus is hidden in the review viewer. Intentional arterial perforators enter tissue. See surface-validation.json and crossing-roundness-validation.json for scope, actual exported-wall checks, minor-diameter measurements and raw aspect ratios. Anatomical acceptance remains pending.\n')
    with zipfile.ZipFile(archive) as z:assert z.testzip() is None
    assert archive.stat().st_size<500*1024**2
    print('Checkpoint',archive,archive.stat().st_size,'Validation',validation,flush=True)

if __name__=='__main__':main()
