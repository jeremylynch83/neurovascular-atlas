"""Publish only a hash-bound, accepted complete central arterial family.

Staged export and every retained label are checked before any app mutation.
The remaining four production assets and all deferred geometry remain exact.
"""
import hashlib,json,shutil
import numpy as np
from fit_vessels import APP,read_glb,mesh_records,accessor

def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()

def validate(report,authoring_hash,brain_hash):
    assert report['passed'] and not report['failures'],'Failed central connected-family acceptance'
    assert report['authoringSha256']==authoring_hash,'Stale central authoring validation'
    assert report['brainAssetSha256']==brain_hash,'Stale central brain context validation'
    expected={f'{label} {side}' for label in ['Central','Central cortical branch','Central distal ramus','MCA superior division'] for side in ['left','right']}
    assert {r['node'] for r in report['geometry']}==expected,'Incomplete central connected family'
    assert report['maximumSharedLabelBoundaryGapMm']<2e-4,'Opened shared junction'
    assert {r['node'] for r in report['selfIntersectionChecks']}==expected,'Missing skin self-intersection check'
    assert all(r['afterNonadjacentTriangleContacts']<=r['beforeNonadjacentTriangleContacts'] for r in report['selfIntersectionChecks']),'New skin self-intersection'
    for key in ['tissueChecks','skullChecks']:
        assert all(r['afterTriangleContacts']<=r['beforeTriangleContacts'] for r in report[key]),'New '+key
    assert all(r['afterOutsideJoinContacts']<=r['beforeOutsideJoinContacts'] for r in report['arterialChecks']),'New arterial crossing'
    assert len(report['branchSections'])==4 and all(r['minimumAreaRatio']>.55 for r in report['branchSections']),'Missing or failed branch skin-envelope check'
    assert len(report['primarySections'])==2 and all(r['minimumAreaRatio']>.5 for r in report['primarySections']),'Missing or failed primary skin-envelope check'

def main():
    raw=APP/'.authoring/central-rebuilt-trial.glb';compressed=APP/'.authoring/central-rebuilt-export.glb';decoded=APP/'.authoring/central-rebuilt-export-decoded.glb'
    audit=json.loads((APP/'docs/validation/central-rebuilt-acceptance-v0.9.18.json').read_text())
    validate(audit,sha(raw),sha(APP/'public/anatomy/models/brain-context.glb'))
    a,ab=read_glb(raw);e,eb=read_glb(decoded);b,bb=read_glb(APP/'.authoring/arteries-baseline.glb');ar,er,br=[mesh_records(d,c) for d,c in [(a,ab),(e,eb),(b,bb)]]
    assert set(ar)==set(er)==set(br),'Export label inventory differs'
    changed={r['node']:r for r in audit['geometry']}
    for key in ar:
        for attribute in ['POSITION','NORMAL']:
            value=accessor(a,ab,ar[key]['primitive']['attributes'][attribute]);export=accessor(e,eb,er[key]['primitive']['attributes'][attribute])
            assert np.array_equal(value,export),'Staged export changed '+key+' '+attribute
            if key not in changed:assert np.array_equal(value,accessor(b,bb,br[key]['primitive']['attributes'][attribute])),'Changed retained label '+key
        assert np.array_equal(ar[key]['faces'],er[key]['faces']) and np.array_equal(ar[key]['faces'],br[key]['faces']),'Export changed triangle topology'
    assert sha(APP/'.authoring/brain-baseline.glb')==audit['brainAssetSha256'],'Changed brain context'
    retained={'models/venous.glb':'0699bebd7a38b934753f889b03e750d7e42be30559efe7f34a58d2f094c2f92b',
        'models/complete-anastomoses.glb':'4f2e45a13d20646b95cf320e663772019067dd1313607a2db9eb04a88a2da66d',
        'models/craniofacial.glb':'8339b8ca742b1126807740c73905366ce12b446f5d994df44d218a0ebee1f91a',
        'models/brain-context.glb':'0c2c84e340cf270e2488bde6553e685a6c0ef320c33b3459fe2ead962e4fad06'}
    for file,expected in retained.items():assert sha(APP/'public/anatomy'/file)==expected,'Changed deferred or retained asset '+file
    p=APP/'anatomy/generated/complete_manifest.json';m=json.loads(p.read_text())
    branches=json.loads((APP/'docs/validation/central-rebuilt-trial-v0.9.18.json').read_text())
    assert branches['authoringSha256']==audit['authoringSha256'],'Stale branch reconstruction provenance'
    export_hash=sha(compressed);hashes={'models/complete-circulation.glb':export_hash}
    primary_ids=set();branch_sources=[]
    for s in m['structures']:
        course=s.get('vesselCourse')
        if not course:continue
        file=course['geometry']['file']
        if file not in hashes:hashes[file]=sha(APP/'public/anatomy'/file)
        course['geometrySha256']=hashes[file];course['brainAssetSha256']=audit['brainAssetSha256']
        key=s['asset']['node']
        if key not in changed:continue
        role='parent-transition' if key.startswith('MCA') else ('primary' if key in ['Central left','Central right'] else 'attached-cortical-branch')
        course['fitting']={'release':'0.9.18','baseline':'0.9.15','status':'fitted-awaiting-anatomical-review','role':role,'maximumDisplacementMm':changed[key]['maximumDisplacementMm'],'acceptanceEvidence':'docs/validation/central-rebuilt-acceptance-v0.9.18.json'}
        course['summary']=course['summary'].replace(' Central arterial family fitting remains blocked by unresolved adjoining branch courses and clearance; original geometry retained.','')
        suffix=' Regional skin fitted to the registered atlas in v0.9.18; anatomical review remains pending.'
        if suffix not in course['summary']:course['summary']+=suffix
        if role=='primary':primary_ids.add(s['id'])
        if role=='attached-cortical-branch':
            side=s['side'];targets=[f'brain.{label}.{side}' for label in ['central-sulcus','postcentral-gyrus','superior-parietal-lobule']]
            course['targetStructureIds']=targets;course['stationIds']=[];course['stationOrder']='not-applicable'
            course['segments']=[{'order':0,'mode':'pial','targetStructureIds':targets,'stationIds':[],'stationRole':'reconstructed-regional-course','constraints':{'wallClearance':'radius-aware','allowTissueEntry':False,'avoidAtlasCutFaces':True,'preserveJoinedAttachments':True},'reviewStatus':'requires-anatomical-review'}]
            branch=next(r for r in branches['branches'] if r['node']==key)
            branch_sources.append({'vesselId':s['id'],'geometry':course['geometry'],'geometrySha256':export_hash,'brainAssetSha256':audit['brainAssetSha256'],'source':branch['source'],'target':branch['target'],'rule':'independent-cortical-course-with-shared-source-bound-collar','reviewStatus':'requires-anatomical-review'})
    for r in m['relationships']:
        if r['type']=='course_landmark' and r['from'] in primary_ids:r['note']='Central sulcal guide used for the v0.9.18 fitted atlas skin; anatomical review pending.'
    m['release']='0.9.18';m['vesselCourseState']='partially-fitted-awaiting-review';m['assetRevisions']['models/complete-circulation.glb']=export_hash[:20]
    # Every expensive or fallible precondition is above this point.
    shutil.copyfile(compressed,APP/'public/anatomy/models/complete-circulation.glb')
    p.write_text(json.dumps(m,indent=2)+'\n')
    export=json.loads((APP/'public/anatomy/vessel-courses.json').read_text());export['release']='0.9.18';export['state']=m['vesselCourseState'];export['brainRegistration']=m['brainRegistration'];export['courses']=[s['vesselCourse'] for s in m['structures'] if s.get('vesselCourse')]
    (APP/'public/anatomy/vessel-courses.json').write_text(json.dumps(export,indent=2)+'\n')
    (APP/'anatomy/source/brain/central-courses-v0.9.18.json').write_text(json.dumps({'release':'0.9.18','courses':branch_sources,'limitations':audit['limitations']},indent=2)+'\n')
    for file in ['package.json','package-lock.json']:
        path=APP/file;data=json.loads(path.read_text());data['version']='0.9.18'
        if file=='package-lock.json':data['packages']['']['version']='0.9.18'
        path.write_text(json.dumps(data,indent=2)+'\n')
    report={'release':'0.9.18','baseline':'0.9.15','geometry':[{**r,'asset':'arteries'} for r in audit['geometry']],'brainAdjustments':[],'deferredGroups':['dural','brainstem'],'method':'Independent cortical branch courses, rotation-minimising wall transport, source-bound joins and ramus prefixes, rigid cap transport, ordered right terminal sections and local join adjustments of 1.2 mm medially and 0.6 mm posteriorly.'}
    report.update(status='applied-atlas-fit-awaiting-anatomical-review',appliedToApp=True)
    (APP/'docs/validation/vessel-fitting-v0.9.18.json').write_text(json.dumps(report,indent=2)+'\n')
    print('Published eight validated central-family labels; deferred venous and brain geometry retained.')

if __name__=='__main__':main()
