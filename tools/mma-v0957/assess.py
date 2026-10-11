"""Consolidate actual candidate checks without waiving unresolved anatomy."""
import json,sys,hashlib,numpy as np
from scipy.sparse import coo_matrix
from scipy.sparse.csgraph import connected_components
from pathlib import Path
work=Path(sys.argv[1]).resolve();out=work/'candidate';root=work.parent
read=lambda name:json.loads((out/name).read_text())
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
rev=read('revision.json');mma=read('full-mma-brain-check.json');fold=read('arterial-self-intersections.json');interfaces=read('field-interface-check.json');paired=read('paired-channel-validation.json');channels=read('paired-channel-candidates.json')
neural=[r for r in mma['contacts']if not r['brain'].startswith(('brain.falx','brain.tentorium'))];dural=[r for r in mma['contacts']if r not in neural]
core={g['node']for g in json.loads((work/'tree-guides.json').read_text())}
topology=[]
for row in channels['channels']:
 n=row['node'];v=np.fromfile(out/(n+'.positions.bin'),'<f4').reshape(-1,3);f=np.fromfile(out/(n+'.indices.bin'),'<u4').reshape(-1,3)
 edges=np.sort(np.vstack([f[:,[0,1]],f[:,[1,2]],f[:,[2,0]]]),axis=1);_,counts=np.unique(edges,axis=0,return_counts=True)
 graph=coo_matrix((np.ones(len(edges)),(edges[:,0],edges[:,1])),shape=(len(v),len(v))).tocsr();components=connected_components(graph,directed=False,return_labels=False)
 row.update(boundaryEdges=int((counts==1).sum()),nonManifoldEdges=int((counts>2).sum()),components=int(components))
 topology.append(dict(node=n,boundaryEdges=row['boundaryEdges'],nonManifoldEdges=row['nonManifoldEdges'],components=int(components)))
paired_bad=[dict(channel=r['node'],**c)for r in paired['checks']for c in r['contacts']if not c['intendedReceiver']and not c['boneCanalUnsegmented']]
paired_neural=[r for r in paired_bad if r['other'].startswith('brain.')]
paired_pairs=sorted({tuple(sorted((r['channel'],r['other'])))for r in paired_bad})
public={n:sha(root/'public/anatomy/models'/n)for n in rev['baselineAssetHashes']}
checks=dict(publicAssetsUnchanged=public==rev['baselineAssetHashes'],brainAndSkullUnchanged=not any(r['node'].startswith(('brain.','bone.'))for r in rev['changed']),allPrimaryMmaBranchesClearOfBrain=not any(r['artery']in core for r in neural),sharedNativeInterfacesExact=interfaces['maxMismatchMm']==0,noNewPerLabelArterialFolds=fold['passed'],allMmaBranchesClearOfBrain=not neural,pairedChannelsClosedAndManifold=all(r['boundaryEdges']==0 and r['nonManifoldEdges']==0 and r['components']==1 for r in channels['channels']),pairedNoSelfFolds=all(r['selfIntersectionPairs']==0 for r in paired['checks']),pairedClearOfBrain=not paired_neural,pairedNoUnintendedNeighbours=not paired_bad,receiverExteriorInstalled=False,boneCanalGeometryReviewed=False,arterialCalibreAndInterbranchRelationshipsReviewed=False,independentAnatomicalReviewCompleted=False)
report=dict(candidate='0.9.57 regional correction candidate',status='UNRELEASED',acceptedApp='0.9.51',passed=all(checks.values()),checks=checks,primaryMmaBranches=len(core),primaryMmaNeuralContactPairs=sum(r['artery']in core for r in neural),mmaNeuralContactPairs=len(neural),mmaDuralContactPairs=len(dural),previousCheckpointMmaNeuralPairs=21,recoveredAppMmaNeuralPairs=91,checkedArterialLabels=len(fold['results']),newPerLabelArterialFolds=sum(r['newIntersections']for r in fold['results']),nativeInterfaceMismatchMm=interfaces['maxMismatchMm'],pairedNeuralContactPairs=len(paired_neural),pairedUnintendedDirectedPairs=len(paired_bad),pairedUnintendedUniquePairs=len(paired_pairs),pairedTopology=topology,mmaNeuralContacts=neural,mmaDuralContacts=dural,pairedUnintendedContacts=paired_bad,candidateBufferSha256={p.name:sha(p)for p in sorted(out.glob('*.bin'))},acceptedAssetSha256=public,changes=['Both orbital branches corrected below the temporal poles; a gentle native-origin transition removes the left fold.','Posterior vein receiver stems rebuilt between their unchanged endpoints, removing both superior-temporal contacts.','Larger collateral experiments failed and were restored byte-for-byte to v0.9.56.','The combined receiver exterior has exact native openings and no new folds, but its orbital-cortex contacts prevent installation.'],limitations=['Nineteen MMA neural contact pairs and two mutual vein overlaps remain.','Bone canals/grooves, calibre and cross-label arterial relationships remain unreviewed.','Independent anatomical review is outstanding.','The viewer compiles and its embedded buffers are checked; browser execution remains unverified.','The public app remains v0.9.51; failed candidate geometry is not exported.'])
report['receiverExteriorTrial']=dict(seams=read('receiver-seam-validation.json'),neighbours=read('receiver-neighbour-validation.json'),installed=False)
report['receiverLocalClearanceTrial']=read('receiver-local-clearance-trial.json')
(out/'paired-channel-candidates.json').write_text(json.dumps(channels,indent=2))
(out/'acceptance.json').write_text(json.dumps(report,indent=2))
print(json.dumps({k:report[k]for k in ['candidate','passed','checks','mmaNeuralContactPairs','pairedNeuralContactPairs','pairedUnintendedUniquePairs','newPerLabelArterialFolds','nativeInterfaceMismatchMm']},indent=2))
assert checks['publicAssetsUnchanged']and checks['brainAndSkullUnchanged']and checks['sharedNativeInterfacesExact']and checks['noNewPerLabelArterialFolds']
