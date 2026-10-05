"""Exercise the publication gate without mutating geometry or metadata."""
import copy,json,hashlib
from publish_central_rebuild import APP,validate,sha

def main():
    report=json.loads((APP/'docs/validation/central-rebuilt-acceptance-v0.9.18.json').read_text())
    raw=sha(APP/'.authoring/central-rebuilt-trial.glb');brain=sha(APP/'public/anatomy/models/brain-context.glb')
    validate(report,raw,brain)
    paths=[APP/p for p in ['anatomy/generated/complete_manifest.json','public/anatomy/vessel-courses.json','package.json','package-lock.json','public/anatomy/models/complete-circulation.glb']]
    before={str(p):sha(p) for p in paths};results=[]
    for case in ['stale-geometry','stale-context','failed-status','missing-family','opened-join','self-intersection','tissue-contact','skull-contact','arterial-crossing','branch-narrowing','primary-narrowing']:
        data=copy.deepcopy(report)
        if case=='stale-geometry':data['authoringSha256']='stale'
        elif case=='stale-context':data['brainAssetSha256']='stale'
        elif case=='failed-status':data['passed']=False
        elif case=='missing-family':data['geometry'].pop()
        elif case=='opened-join':data['maximumSharedLabelBoundaryGapMm']=.1
        elif case=='self-intersection':data['selfIntersectionChecks'][0]['afterNonadjacentTriangleContacts']=1
        elif case in ['tissue-contact','skull-contact']:data['tissueChecks' if case=='tissue-contact' else 'skullChecks']=[{'beforeTriangleContacts':0,'afterTriangleContacts':1}]
        elif case=='arterial-crossing':data['arterialChecks']=[{'beforeOutsideJoinContacts':0,'afterOutsideJoinContacts':1}]
        elif case=='branch-narrowing':data['branchSections'][0]['minimumAreaRatio']=.1
        else:data['primarySections'][0]['minimumAreaRatio']=.1
        try:validate(data,raw,brain)
        except AssertionError as error:results.append({'case':case,'rejected':True,'reason':str(error)})
        else:raise AssertionError('Publication gate accepted '+case)
    assert before=={str(p):sha(p) for p in paths}
    (APP/'docs/validation/central-publication-guards-v0.9.18.json').write_text(json.dumps({'release':'0.9.18','currentAcceptedReportPasses':True,'invalidFixtures':results,'geometryAndMetadataUnchanged':True},indent=2)+'\n')
    print('Eleven invalid publication fixtures rejected; geometry and metadata retained exactly.')
if __name__=='__main__':main()
