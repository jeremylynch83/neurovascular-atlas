"""Assess actual saved candidate buffers without waiving unresolved anatomy."""
import json,sys,hashlib
from pathlib import Path
work=Path(sys.argv[1]).resolve();out=work/'candidate';root=work.parent
read=lambda name:json.loads((out/name).read_text())
sha=lambda path:hashlib.sha256(path.read_bytes()).hexdigest()
rev=read('revision.json');mma=read('full-mma-brain-check.json');fold=read('arterial-self-intersections.json');interfaces=read('field-interface-check.json');paired=read('paired-channel-validation.json');channels=read('paired-channel-candidates.json')
categories={s['asset']['node']:s['anatomy']['category'] for s in json.loads((root/'public/anatomy/brain-landmarks.json').read_text())['surfaces']}
neural=[r for r in mma['contacts'] if categories.get(r['brain'])!='dural_reflections'];dural=[r for r in mma['contacts'] if categories.get(r['brain'])=='dural_reflections']
core={g['node'] for g in json.loads((work/'tree-guides.json').read_text())}
paired_bad=[dict(channel=r['node'],**c) for r in paired['checks'] for c in r['contacts'] if not c['intendedReceiver'] and not c['other'].startswith('bone.')]
paired_pairs=sorted({tuple(sorted((x['channel'],x['other']))) for x in paired_bad})
public={name:sha(root/'public/anatomy/models'/name) for name in rev['baselineAssetHashes']}
reference=[r['node'] for r in rev['changed'] if r['node'].startswith(('brain.','bone.'))]
checks=dict(publicAssetsUnchanged=public==rev['baselineAssetHashes'],brainAndSkullUnchanged=not reference,
            allPrimaryMmaBranchesClearOfBrain=not any(r['artery'] in core for r in neural),
            sharedNativeInterfacesExact=interfaces['maxMismatchMm']==0,
            noNewPerLabelArterialFolds=fold['passed'],allMmaBranchesClearOfBrain=not neural,
            pairedChannelsClosedAndManifold=all(r['boundaryEdges']==0 and r['nonManifoldEdges']==0 and r['components']==1 for r in channels['channels']),
            pairedNoSelfFolds=all(r['selfIntersectionPairs']==0 for r in paired['checks']),
            pairedNoUnintendedNeighbours=not paired_bad,
            receiverExteriorInstalled=False,boneCanalGeometryReviewed=False,
            arterialCalibreAndInterbranchRelationshipsReviewed=False,independentAnatomicalReviewCompleted=False)
report=dict(candidate='0.9.56 skull-directed review candidate',status='UNRELEASED',acceptedApp='0.9.51',passed=all(checks.values()),checks=checks,
            primaryMmaBranches=len(core),primaryMmaNeuralContactPairs=sum(r['artery'] in core for r in neural),
            mmaNeuralContactPairs=len(neural),mmaDuralContactPairs=len(dural),previousCheckpointMmaNeuralPairs=80,recoveredAppMmaNeuralPairs=91,
            checkedArterialLabels=len(fold['results']),newPerLabelArterialFolds=sum(r['newIntersections'] for r in fold['results']),
            nativeInterfaceMismatchMm=interfaces['maxMismatchMm'],pairedUnintendedDirectedPairs=len(paired_bad),pairedUnintendedUniquePairs=len(paired_pairs),
            mmaNeuralContacts=neural,mmaDuralContacts=dural,pairedUnintendedContacts=paired_bad,
            candidateBufferSha256={p.name:sha(p) for p in sorted(out.glob('*.bin'))},acceptedAssetSha256=public,
            limitations=['Outer-table ray probes use nominal centreline radii and do not certify full mesh cover or a segmented bone canal.',
                         'Per-label fold checks do not certify all cross-label arterial relationships or preserved lumen calibre.',
                         'Two extracranial courses were restored with exact shared collars; their incremental self-intersection checks passed.',
                         'The viewer compiled and embedded geometry was checked. Browser execution was blocked by the environment, so its runtime remains unverified.',
                         'The independent collateral-control experiment exceeded its movement target and retained neural violations; it was not applied.',
                         'No brain, skull, public GLB, catalogue or accepted app release was changed.'])
(out/'acceptance.json').write_text(json.dumps(report,indent=2))
summary={k:v for k,v in report.items() if k not in ['candidateBufferSha256','acceptedAssetSha256','mmaNeuralContacts','mmaDuralContacts','pairedUnintendedContacts','limitations']}
print(json.dumps(summary,indent=2))
assert checks['publicAssetsUnchanged'] and checks['brainAndSkullUnchanged']
assert checks['sharedNativeInterfacesExact'] and checks['noNewPerLabelArterialFolds']
