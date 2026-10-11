"""Consolidate the complete checkpoint gate without changing public assets."""
from common import *
import hashlib
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
rev=json.loads((OUT/'revision.json').read_text());interfaces=json.loads((OUT/'field-interface-check.json').read_text());arterial=json.loads((OUT/'arterial-self-intersections.json').read_text());venous=json.loads((OUT/'venous-self-intersections.json').read_text());neural=json.loads((OUT/'brain-self-intersections.json').read_text());paired=json.loads((OUT/'paired-channel-validation.json').read_text());channels=json.loads((OUT/'paired-channel-candidates.json').read_text());mma_brain=json.loads((OUT/'full-mma-brain-check.json').read_text())
# Updated paired meshes are separately audited after the native venous check.
newnames={x['node'] for x in channels['channels']};nativeveins=[x for x in venous['results'] if x['node'] not in newnames]
paired_bad=[dict(channel=row['node'],**c) for row in paired['checks'] for c in row['contacts'] if not c['intendedReceiver'] and not c['boneCanalUnsegmented']]
brainfolds=[x for x in neural['results'] if x['newIntersections']];arterialfolds=[x for x in arterial['results'] if x['newIntersections']]
mma=[x for x in arterial['results'] if x['node'].startswith(('MMA ','Middle meningeal')) or 'MMA' in x['node']]
base=rev['baselineAssetHashes'];actual={n:sha(WORK.parent/'public/anatomy/models'/n) for n in base};unchanged=actual==base
checks=dict(acceptedAssetsUnchanged=unchanged,exactNativeInterfaces=interfaces['passedSharedCollars'],noNewMmaFolds=all(not x['newIntersections'] for x in mma),noNewNativeVenousFolds=all(not x['newIntersections'] for x in nativeveins),pairedClosedManifold=all(x['boundaryEdges']==0 and x['nonManifoldEdges']==0 and x['components']==1 for x in channels['channels']),pairedDistinctMeshes=all(x['distinctMeshes'] for x in paired['pairedMeshesDistinct']),pairedOutwardAndNonDegenerate=all(x['signedVolumeMm3']>0 and not x['degenerateTriangles'] for x in paired['checks']),pairedNoSelfIntersections=all(not x['selfIntersectionPairs'] for x in paired['checks']),pairedNoUnintendedNeuralOrVascularContacts=not paired_bad,noNewFullArterialFolds=not arterialfolds,noNewFullBrainFolds=not brainfolds,noRemainingMmaBrainContacts=mma_brain['passed'],pairedReceiverExteriorMerged=channels['receiverExteriorMerged'],skullAndCanalRelationsAccepted=False,regionalBrainRegistrationReviewed=False)
report=dict(candidate='0.9.54 checkpoint',acceptedRelease='0.9.51',passed=all(checks.values()),status='UNRELEASED CHECKPOINT',checks=checks,checkedMmaLabels=len(mma),newMmaFoldPairs=sum(x['newIntersections'] for x in mma),checkedNativeVenousLabels=len(nativeveins),newNativeVenousFoldPairs=sum(x['newIntersections'] for x in nativeveins),maxNativeInterfaceMismatchMm=interfaces['maxMismatchMm'],pairedChannelCount=len(channels['channels']),pairedUnintendedNeuralOrVascularContactPairs=len(paired_bad),brainCheckedLabels=len(neural['results']),newBrainFoldPairs=sum(x['newIntersections'] for x in brainfolds),brainFoldFailures=brainfolds,arterialCheckedLabels=len(arterial['results']),newNonMmaArterialFoldPairs=sum(x['newIntersections'] for x in arterialfolds),arterialFoldFailures=arterialfolds,remainingMmaBrainContactPairs=len(mma_brain['contacts']),newPairedContacts=paired_bad,acceptedAssetSha256=actual,candidateBufferSha256={p.name:sha(p) for p in sorted(OUT.glob('*.bin'))},scope=['Exact triangle and native-coordinate diagnostics; independent anatomical review is outstanding.','All four channels are independently closed exterior meshes; receiving-wall overlaps are still unmerged.','Bone contacts remain unresolved; mesh intersections cannot establish intradiploic groove or canal containment.','The wider cortical trial is rejected because its full brain and pial artery checks fail.','Positive sampled Jacobians and a successful build of the unchanged accepted app do not validate this geometry.'])
if (OUT/'receiver-seam-validation.json').exists():
    seams=json.loads((OUT/'receiver-seam-validation.json').read_text())
    neighbours=json.loads((OUT/'receiver-neighbour-validation.json').read_text())
    report['supplementalSharedReceiverExterior']=dict(
        topologyAndSourceCollarsPassed=all(r['passed'] for r in seams),
        noNewNeuralOrVascularContacts=all(r['noNewNeuralOrVascularContacts'] for r in neighbours),
        boneRelationsAccepted=all(r['boneRelationsAccepted'] for r in neighbours),
        geometrySha256={p.name:sha(p) for p in sorted(OUT.glob('receiver-seam-completed-*.npz'))},
        installedInActiveBuffers=False,
        scope='Separate completed exterior surfaces, checked against the rejected cortical candidate. Recheck after registration correction and partition into catalogue labels before release.')
    report['scope'][1]='The supplemental paired-vein/receiver exteriors pass seam and neural/vascular neighbour checks. Active labelled buffers remain separate and unexported; bone and reference checks fail.'
assert unchanged,'Accepted app assets changed during a rejected reconstruction'
(OUT/'acceptance.json').write_text(json.dumps(report,indent=2))
print(json.dumps({k:v for k,v in report.items() if k not in ['candidateBufferSha256','acceptedAssetSha256','brainFoldFailures','arterialFoldFailures']},indent=2))
raise SystemExit(0 if report['passed'] else 2)

