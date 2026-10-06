"""Integrate exact checked posterior-fossa geometry as an anatomical review build."""
import json,hashlib,shutil
import numpy as np,trimesh,vtk
from scipy.spatial import cKDTree
from fit_vessels import APP
from build_targets import poly

VERSION='0.9.20'
W=APP/'.authoring/posterior-round61'
PUB=APP/'public/anatomy'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()

def main():
    surface=json.loads((W/'surface-validation.json').read_text());cross=json.loads((W/'crossing-roundness-validation.json').read_text());joins=json.loads((W/'integration-validation.json').read_text())
    assert surface.get('passed') and cross.get('passed') and joins.get('passed'),'Posterior surface, crossings and physical joins must pass first'
    rawhash={k:sha(W/f'{k}-trial.glb') for k in ['brain','arteries','veins']};assert surface['hashes']==rawhash;assert cross['hashes']=={k:rawhash[k] for k in ['veins','arteries']}
    baseline=json.loads((APP/'anatomy/generated/complete_manifest.json').read_text());assert baseline['release']=='0.9.19','Restore the original v0.9.19 baseline before running this one-shot integration';manifest=json.loads((W/'candidate-manifest.json').read_text())
    oldbrain=trimesh.load(PUB/'models/brain-context.glb',process=False);brain=trimesh.load(W/'brain-trial.glb',process=False)
    shutil.copyfile(W/'brain-trial.glb',PUB/'models/brain-context.glb')
    shutil.copyfile(W/'arteries-delivered.glb',PUB/'models/complete-circulation.glb');shutil.copyfile(W/'veins-delivered.glb',PUB/'models/venous.glb')
    mapping={'models/brain-trial.glb':'models/brain-context.glb','models/arteries-trial.glb':'models/complete-circulation.glb','models/veins-trial.glb':'models/venous.glb'}
    hashes={file:sha(PUB/file) for file in set(mapping.values())};bh=hashes['models/brain-context.glb'];cache={};trees={}
    def rebind(a):
        key=a['structureId'];m=brain.geometry[key];query=np.array(a['position'],float)
        if key in oldbrain.geometry and len(m.vertices)==len(oldbrain.geometry[key].vertices):
            if key not in trees:trees[key]=cKDTree(oldbrain.geometry[key].vertices)
            i=trees[key].query(query)[1];query+=m.vertices[i]-oldbrain.geometry[key].vertices[i]
        if key not in cache:
            loc=vtk.vtkStaticCellLocator();loc.SetDataSet(poly(m));loc.BuildLocator();cache[key]=loc
        closest=[0.,0.,0.];cell,sub,d=vtk.reference(0),vtk.reference(0),vtk.reference(0.);cache[key].FindClosestPoint(query,closest,cell,sub,d);t=int(cell)
        weights=trimesh.triangles.points_to_barycentric(m.vertices[m.faces[[t]]],np.array([closest]))[0];weights=np.clip(weights,0,1);weights/=weights.sum();a.update(triangleIndex=t,barycentric=weights.tolist(),position=(weights@m.vertices[m.faces[t]]).tolist(),assetSha256=bh)
    for row in manifest['structures']:
        asset=row.get('asset')
        if asset and asset['file'] in mapping:asset['file']=mapping[asset['file']]
        if row.get('surfaceAnchor'):rebind(row['surfaceAnchor']);row['landmark']['point']=row['surfaceAnchor']['position']
        for a in row.get('secondarySurfaceAnchors',[]):rebind(a)
        c=row.get('vesselCourse')
        if c and asset:
            c['geometry']=asset.copy();c['geometrySha256']=(hashes[asset['file']] if asset['file'] in hashes else sha(PUB/asset['file']));c['brainAssetSha256']=bh
            if c['reviewStatus'] not in ['requires-anatomical-review','requires-anatomical-target','protected-baseline']:c['reviewStatus']='requires-anatomical-review'
            c['candidateReviewStatus']='local surface and joins checked; wider anatomical relations require review'
        if row['id']=='brain.upper-cervical-cord':row['provenance']={'sourceType':'teaching-reconstruction','reviewStatus':'unreviewed','confidence':'Illustrative continuation fitted to the caudal medullary surface','sourceRefs':[]}
        if row['id']=='vein.basilar_plexus':
            row.pop('asset',None);row.pop('vesselCourse',None);row['geometryStatus']='planned';row['notes']='Clival/basilar plexus geometry omitted at author request.'
        if asset and asset['node'] in brain.geometry and row.get('anatomy'):
            m=brain.geometry[asset['node']];row['anatomy'].update(bounds=m.bounds.tolist(),centroid=m.vertices.mean(0).tolist())
    byid={r['id']:r for r in manifest['structures']}
    for row in manifest['structures']:
        guide=row.get('vesselGuide')
        if guide and guide.get('anchorIds'):
            row['landmark']['course']=[byid[k]['surfaceAnchor']['position'] for k in guide['anchorIds']];row['landmark']['point']=row['landmark']['course'][0]
    for side in ['left','right']:
        id='artery.posterior.posterior_spinal_'+side;parent='artery.posterior.pica_'+side
        for row in manifest['structures']:
            if id in row.get('children',[]) and row['id']!=parent:row['children'].remove(id)
        if id not in byid[parent]['children']:byid[parent]['children'].append(id)
        byid[id]['parent']=parent;byid[id]['vesselCourse']['attachments']['parentId']=parent
        c=byid[id]['vesselCourse'];c['segments']=[{'order':i,'mode':mode,'targetStructureIds':c['targetStructureIds'],'stationIds':c['stationIds'],'stationRole':'whole-course-reference','constraints':{'wallClearance':'radius-aware','allowTissueEntry':False,'avoidAtlasCutFaces':True,'preserveJoinedAttachments':True},'reviewStatus':'requires-individual-segment-boundaries'} for i,mode in enumerate(['cisternal','pial'])]
        for r in manifest['relationships']:
            if r['to']==id and r['type']=='branches_to':r['from']=parent
        for row in manifest['structures']:
            c=row.get('vesselCourse')
            if c:
                c['attachments']['incoming']=[r for r in manifest['relationships'] if r['to']==row['id']]
                c['attachments']['outgoing']=[r for r in manifest['relationships'] if r['from']==row['id']]
    manifest.update(release=VERSION,releaseChannel='anatomical-review',vesselCourseState='posterior-fossa-fitted; wider-contacts-awaiting-review')
    manifest['brainRegistration']['registeredAssetSha256']=bh
    manifest['brainRegistration'].setdefault('regionalAdjustments',[]).append({'release':VERSION,'method':'Recovered posterior-fossa candidate 59, with illustrative cervical continuation; tissue geometry retained through candidates 60 and 61','brainSha256':bh})
    manifest['candidateStatus']={'number':61,'appliedToApp':True,'accepted':False,'posteriorSurfaceChecksPassed':True,'physicalJoinChecksPassed':True,'veinCrossingChecksPassed':True,'widerAnatomicalReviewComplete':False}
    manifest.pop('candidateAssets',None);manifest.pop('candidateDirectory',None);manifest.pop('candidateHashes',None)
    for file,h in hashes.items():manifest['assetRevisions'][file]=h[:20]
    (APP/'anatomy/generated/complete_manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
    landmarks=json.loads((PUB/'brain-landmarks.json').read_text());landmarks['registration']=manifest['brainRegistration'];landmarks['anchors']=[r for r in manifest['structures'] if r.get('landmark') and r['system']=='brain'];(PUB/'brain-landmarks.json').write_text(json.dumps(landmarks,indent=2)+'\n')
    courses=json.loads((PUB/'vessel-courses.json').read_text());courses.update(release=VERSION,brainRegistration=manifest['brainRegistration'],courses=[r['vesselCourse'] for r in manifest['structures'] if r.get('vesselCourse')]);(PUB/'vessel-courses.json').write_text(json.dumps(courses,indent=2)+'\n')
    for file in ['package.json','package-lock.json']:
        p=APP/file;data=json.loads(p.read_text());data['version']=VERSION
        if file=='package-lock.json':data['packages']['']['version']=VERSION
        p.write_text(json.dumps(data,indent=2)+'\n')
    dest=APP/'docs/validation';dest.mkdir(exist_ok=True)
    for name in ['surface-validation','crossing-roundness-validation','integration-validation','join-repairs']:
        shutil.copyfile(W/f'{name}.json',dest/f'posterior-{name}-v{VERSION}.json')
    shutil.copyfile(APP/'.authoring/posterior-round59/integration-validation.json',dest/f'posterior-wider-context-review-v{VERSION}.json')
    report={'release':VERSION,'channel':'anatomical-review','appliedToApp':True,'anatomicallyComplete':False,'sourceCandidate':61,'sourceHashes':rawhash,'deliveredHashes':hashes,'checksPassed':['posterior-fossa surface walls','containment in closed posterior tissue','sampled vein minor diameter','vein-artery crossings','physical source joins','bilateral proximal PICA-to-PSA joins'],'remaining':['Upper cerebral/pontomesencephalic collecting routes need full parenchymal reconciliation.','Some posterior arterial and cerebellar venous routes still contact cerebral atlas parts outside the posterior-fossa audit.','Open atlas surfaces permit triangle checks, not proof of solid containment.'],'plexusGeometryRendered':False}
    (dest/f'posterior-review-v{VERSION}.json').write_text(json.dumps(report,indent=2)+'\n')
    print('Integrated anatomical review',VERSION,flush=True)

if __name__=='__main__':main()
