"""Fail closed when any required reconstruction gate is absent or fails."""
from common import *
import hashlib
rev=json.loads((OUT/'revision.json').read_text())
field=json.loads((OUT/'field-interface-check.json').read_text())
mma=json.loads((OUT/'self-intersections.json').read_text())
brain=json.loads((OUT/'full-mma-brain-check.json').read_text())
paired=json.loads((OUT/'paired-channel-candidates.json').read_text())
paired_check=json.loads((OUT/'paired-channel-validation.json').read_text())
vein_path=OUT/'venous-self-intersections.json'
veins=json.loads(vein_path.read_text()) if vein_path.exists() else None
source_hashes={name:hashlib.sha256((Path('public/anatomy/models')/name).read_bytes()).hexdigest() for name in rev['baselineAssetHashes']}
paired_bad=[(row['node'],c) for row in paired_check['checks'] for c in row['contacts'] if not c['intendedReceiver'] and not c['boneCanalUnsegmented']]
checks=dict(acceptedAssetsUnchanged=source_hashes==rev['baselineAssetHashes'],exactNativeCoincidentInterfaces=field['passedSharedCollars'],noNewCheckedMmaFolds=mma['passed'],noRemainingCheckedMmaBrainContacts=brain['passed'],pairedClosedManifoldComponents=all(r['boundaryEdges']==0 and r['nonManifoldEdges']==0 and r['components']==1 for r in paired['channels']),pairedOutwardOrientation=all(r['signedVolumeMm3']>0 for r in paired_check['checks']),pairedNoSelfIntersections=all(r['selfIntersectionPairs']==0 for r in paired_check['checks']),pairedNoUnintendedNeuralOrVascularContacts=not paired_bad,pairedReceiverExteriorMerged=paired['receiverExteriorMerged'],noNewCheckedVenousFolds=bool(veins and veins['passed']),fullReferenceSurfaceAndVascularChecksComplete=False,skullAndCanalContainmentCertified=False)
fingerprints={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(OUT.glob('*.bin'))}
report=dict(status='unreleased_reconstruction_checkpoint',passed=all(checks.values()),acceptedRelease='0.9.51',proposedRelease='0.9.52',checks=checks,checkedMmaLabels=len(mma['results']),newCheckedMmaSelfIntersectionPairs=sum(r['newIntersections'] for r in mma['results']),checkedBrainContactLabels=len(brain['checkedLabels']),remainingCheckedMmaBrainContactPairs=len(brain['contacts']),maxNativeCoincidentInterfaceMismatchMm=field['maxMismatchMm'],pairedChannelCount=len(paired['channels']),pairedUnintendedNeuralOrVascularContactPairs=len(paired_bad),candidateBufferSha256=fingerprints,acceptedAssetSha256=source_hashes,limitations=['Exact native-interface equality and sampled positive field Jacobians do not certify the full reconstruction.','The registration field and newly refitted venous drainage stems need further shape and contact validation.','Unsegmented grooves and bone canals prevent a containment claim for the paired channels.','The paired drainage stems overlap the retained lesser-wing channel but do not yet share its exterior surface.','No updated app assets, manifest, release archive or application build were produced because the geometry gate fails.'])
(OUT/'acceptance.json').write_text(json.dumps(report,indent=2))
print(json.dumps({k:v for k,v in report.items() if k not in ['candidateBufferSha256','acceptedAssetSha256']},indent=2))
raise SystemExit(0 if report['passed'] else 2)
