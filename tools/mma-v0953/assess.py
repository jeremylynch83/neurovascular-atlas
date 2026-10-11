"""Fail-closed release gate and exact, reviewable candidate fingerprint."""
from common import *
import hashlib
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
r=json.loads((OUT/'revision.json').read_text());v=json.loads((OUT/'validation.json').read_text());s=json.loads((OUT/'self-intersections.json').read_text());topology=json.loads((OUT/'new-vein-topology.json').read_text())
folds=[x for x in s['results'] if x['newIntersections']]
brain=[x for x in v['contacts'] if (x['a'].lower().startswith(('mma','middle meningeal','vein.middle_meningeal')) and x['b'].startswith('brain.')) and x['candidateMovedFacesInContact']]
collars=[x for x in v['collars'] if x['maxMismatchMm']>=1e-4];deg=[x for x in v['meshChecks'] if x['newDegenerateFaces']]
intentional={('vein.middle_meningeal.'+side,'vein.'+receiver+'.'+side) for side in ['right','left'] for receiver in ['pterygoid_plexus','sphenoparietal']}
veincontacts=[x for x in v['contacts'] if x['a'].startswith('vein.middle_meningeal.') and x['candidateMovedFacesInContact'] and not x['b'].startswith('bone.') and (x['a'],x['b']) not in intentional]
assetdir=WORK.parent/'public/anatomy/models';baseline=r['baselineAssetHashes'];actual={n:sha(assetdir/n) for n in baseline};unchanged=all(actual[n]==h for n,h in baseline.items())
passed=not folds and not brain and not collars and not deg and not veincontacts and all(x['components']==1 and x['boundaryEdges']==0 and x['nonManifoldEdges']==0 for x in topology)
report=dict(candidate='0.9.53',baseline='0.9.51',passed=passed,status='ACCEPTED' if passed else 'REJECTED; not an installable release',acceptedAssetsUnchanged=unchanged,baselineAssetSha256=baseline,actualAcceptedAssetSha256=actual,candidateBufferSha256={p.name:sha(p) for p in sorted(OUT.glob('*.bin'))},meshCount=len(r['changed']),checkedSelfIntersectionRows=len(s['results']),foldFailures=folds,remainingMmaBrainPairs=brain,nativeCollarFailures=collars,newDegenerateFaceFailures=deg,newVeinTopology=topology,newVeinNonReceiverContacts=veincontacts,foldFreeFrontalNodes=[x['node'] for x in s['results'] if x['node'].startswith('MMA frontal') and x['candidate']==0],scope=['Exact triangle diagnostics, not independent anatomical certification.','Bone-canals remain unsegmented; bone contacts do not certify canal containment.','Brain, native collar and vascular failures block export.','Accepted application build passed separately; that does not validate the trial geometry.'])
(OUT/'acceptance.json').write_text(json.dumps(report,indent=2)+'\n')
assert unchanged,'Accepted assets were altered during a rejected trial'
print(json.dumps({k:report[k] for k in ['status','acceptedAssetsUnchanged','meshCount','foldFreeFrontalNodes']}));sys.exit(0 if passed else 2)
