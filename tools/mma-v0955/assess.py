"""Assess the source-verified checkpoint. Never accepts anatomy by build alone."""
import sys
import json
import hashlib
from pathlib import Path

work = Path(sys.argv[1]).resolve(); out = work / 'candidate'
read = lambda filename: json.loads((out / filename).read_text())
sha = lambda path: hashlib.sha256(path.read_bytes()).hexdigest()
revision = read('revision.json')
restoration = read('reference-restoration.json')
interfaces = read('field-interface-check.json')
arterial = read('arterial-self-intersections.json')
mma = read('full-mma-brain-check.json')
paired = read('paired-channel-validation.json')
channels = read('paired-channel-candidates.json')
receivers = read('receiver-neighbour-validation.json')
source = json.loads((work / 'source-reference-comparison.json').read_text())
master = json.loads((work / 'upstream-export-comparison.json').read_text())
categories = {s['asset']['node']:s['anatomy']['category'] for s in json.loads(
    (work.parent / 'public/anatomy/brain-landmarks.json').read_text())['surfaces']}
brain_changes = [r for r in revision['changed'] if r['node'].startswith('brain.')]
restored_exact = all(sha(out / (r['node']+'.'+suffix)) == digest
                     for r in restoration['records'] for suffix, digest in r['baselineHashes'].items())
public_hashes = {n:sha(work.parent / 'public/anatomy/models' / n)
                 for n in revision['baselineAssetHashes']}
assets_unchanged = public_hashes == revision['baselineAssetHashes']
neural = [r for r in mma['contacts'] if categories.get(r['brain']) != 'dural_reflections']
dural = [r for r in mma['contacts'] if categories.get(r['brain']) == 'dural_reflections']
paired_bad = [dict(channel=r['node'], **c) for r in paired['checks'] for c in r['contacts']
              if not c['intendedReceiver'] and not c['other'].startswith('bone.')]
paired_bone = [dict(channel=r['node'], **c) for r in paired['checks'] for c in r['contacts']
               if c['other'].startswith('bone.')]
source_bones = [r for r in master['records'] if r['node'].startswith('bone.')]
source_cortex = [r for r in master['records'] if categories.get(r['node']) == 'cerebral_cortex']
checks = dict(acceptedAssetsUnchanged=assets_unchanged,
              restoredReferenceExact=restored_exact and not brain_changes,
              nativeInterfacesPreserved=interfaces['passedSharedCollars'],
              noNewChangedArterialFolds=arterial['passed'],
              pairedNoSelfIntersections=all(not r['selfIntersectionPairs'] for r in paired['checks']),
              pairedOutwardNondegenerate=all(r['signedVolumeMm3']>0 and not r['degenerateTriangles'] for r in paired['checks']),
              pairedClosedManifold=all(r['boundaryEdges']==0 and r['nonManifoldEdges']==0 and r['components']==1 for r in channels['channels']),
              mmaNoNeuralContacts=not neural,
              mmaDuralCoursesReviewed=False,
              pairedNoUnintendedNeuralOrVascularContacts=not paired_bad,
              pairedBoneRelationsReviewed=False,
              supplementalReceiverNoNewNeighbourContacts=all(r['noNewNeuralOrVascularContacts'] for r in receivers),
              coherentSourceReferenceReviewed=False,
              receiverExteriorsInstalledInLabelledBuffers=False,
              independentAnatomicalReviewCompleted=False)
report = dict(candidate='0.9.55 source-verified checkpoint', acceptedRelease='0.9.51',
              status='UNRELEASED CHECKPOINT', passed=all(checks.values()), checks=checks,
              restoredExactMeshes=restoration['restoredMeshes'], changedBrainLabels=len(brain_changes),
              maxNativeInterfaceMismatchMm=interfaces['maxMismatchMm'],
              checkedChangedArterialLabels=len(arterial['results']),
              newChangedArterialFoldPairs=sum(r['newIntersections'] for r in arterial['results']),
              mmaNeuralContactPairs=len(neural), mmaDuralContactPairs=len(dural),
              pairedUnintendedNeuralOrVascularContactPairs=len(paired_bad),
              pairedUnreviewedBoneContactPairs=len(paired_bone),
              originalSourceNearGuideSkullNeuralContactPairs=source['sourcePairCount'],
              retainedAtlasNearGuideSkullNeuralContactPairs=source['atlasPairCount'],
              upstreamSkullMaximumVertexDifferenceMm=max(r['maximumSymmetricVertexDistanceMm'] for r in source_bones),
              upstreamCortexMaximumVertexDifferenceMm=max(r['maximumSymmetricVertexDistanceMm'] for r in source_cortex),
              mmaNeuralContacts=neural, mmaDuralContacts=dural,
              pairedUnintendedContacts=paired_bad,
              acceptedAssetSha256=public_hashes,
              candidateBufferSha256={p.name:sha(p) for p in sorted(out.glob('*.bin'))},
              supplementalReceiverSha256={p.name:sha(p) for p in sorted(out.glob('receiver-seam-completed-*.npz'))},
              scope=['The rejected cortical deformation was removed. Exact accepted buffers were restored; no new anatomical registration is claimed.',
                     'The original shared source itself contains skull/neural intersections near the full trial MMA guides. A joint similarity transform cannot remove intrinsic source intersections.',
                     'The upstream master skull and cortex match the original export to sub-micrometre vertex distances. This is an export comparison, not independent anatomical validation.',
                     'Four new veins and two supplemental receiver exteriors remain experiments. Their neighbour checks were rerun against the undeformed reference and fail.',
                     'No artery, brain, vein, skull, manifest or app release was exported. A successful build of unchanged assets would not grant anatomy acceptance.'])
assert assets_unchanged, 'Public assets unexpectedly changed'
(out / 'acceptance.json').write_text(json.dumps(report, indent=2))
print(json.dumps({k:v for k,v in report.items() if k not in ['candidateBufferSha256','acceptedAssetSha256','mmaNeuralContacts','mmaDuralContacts','pairedUnintendedContacts']}, indent=2))
raise SystemExit(0 if report['passed'] else 2)
