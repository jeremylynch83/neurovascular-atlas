"""Reject the reconstruction if any MMA/brain contact or new fold remains."""
from common import *
import hashlib
rev=json.loads((OUT/'revision.json').read_text())
validation=json.loads((OUT/'validation.json').read_text())
self_check=json.loads((OUT/'self-intersections.json').read_text())
brain=[r for r in validation['contacts'] if r['b'].startswith('brain.') and r['candidateMovedFacesInContact']]
folds=[r for r in self_check['results'] if r['newIntersections']]
fingerprint={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(OUT.glob('*.bin'))}
source=rev['baselineAssetHashes'];actual={name:hashlib.sha256((Path('public/anatomy/models')/name).read_bytes()).hexdigest() for name in source}
checks=dict(noRemainingMmaBrainSurfaceContacts=not brain,noNewSelfIntersections=not folds,sharedCollarsExact=validation['passedSharedCollars'],noNewDegenerateFaces=validation['passedNewDegenerateFaces'],acceptedModelAssetsUnchanged=actual==source)
report=dict(status='rejected_trial',proposedRelease=rev['release'],acceptedRelease='0.9.51',passed=all(checks.values()),checks=checks,changedMeshCount=len(rev['changed']),sharedCollarCount=len(validation['collars']),maxSharedCollarMismatchMm=max(r['maxMismatchMm'] for r in validation['collars']),maxGuideShiftMm=max(g['maxGuideShiftMm'] for g in rev['guides']),remainingMmaBrainContactPairCount=len(brain),newSelfIntersectionPairCount=sum(r['newIntersections'] for r in folds),foldedMeshes=folds,remainingMmaBrainContacts=brain,candidateBufferSha256=fingerprint,acceptedAssetSha256=actual,limitations=['Brain-contact counts are triangle contact diagnostics, not an anatomical error score.','Exact source skull/brain surface intersections near the proposed course do not establish that every possible rerouting is impossible.','The ten accepted v0.9.51 vein additions were not changed or retested in this trial.','No paired meningeal veins were added because the prerequisite MMA reconstruction failed.','Hypothetical brain adjustments were diagnostics only and were not exported.'])
(OUT/'acceptance.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({k:v for k,v in report.items() if k not in ['remainingMmaBrainContacts','candidateBufferSha256','acceptedAssetSha256','foldedMeshes']},indent=2))
raise SystemExit(0 if report['passed'] else 2)
