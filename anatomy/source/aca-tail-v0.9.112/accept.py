from region import *
import shutil
def read(n):return json.load(open(W/n))
r=read('reconstruction-validation.json');c=read('crossing-validation.json');d=read('depth-validation.json');full=read('full-clearance-validation.json')
assert r['passed'] and c['passedNoNewNonNeuralCrossings'] and d['passed'] and full['passed']
assert {(x['face'],x['otherFace'])for x in c['inheritedSourceCrossings']}=={(1156,1222),(1222,1156)}
n='ACA A5 left';v,f=scene.mesh(n);p=np.fromfile(W/'replayed'/(n+'.positions.bin'),'<f4').reshape(-1,3)
ids=np.unique(f[[1156,1222]])
assert np.all(v[ids,1]>=-95.7) and np.all(v[ids,1]<=-95.1)
assert np.array_equal(p[ids].astype(float)-v[ids].astype(float),np.tile([-.5,0,.5],(len(ids),1)))
na=np.fromfile(W/'decoded'/(n+'.normal-snorm16.bin'),'<i2').reshape(-1,4);nb=np.fromfile(W/'replayed'/(n+'.normal-snorm16.bin'),'<i2').reshape(-1,4)
assert np.array_equal(na[ids],nb[ids])
fixed=(v[:,1]>=-94.3)|(v[:,1]<=-96.3)
assert np.array_equal(v[fixed],p[fixed]) and np.array_equal(na[fixed],nb[fixed])
prior={'node':n,'fixedSourceYRanges':[{'minimum':-94.3},{'maximum':-96.3}],'fixedVertices':int(fixed.sum()),'positionsAndStoredNormalsExact':True,'previousMidShaftFitAndTerminalTipRetained':True}
native={'release':'0.9.112','passed':True,'changes':r['changes'],'reconstruction':r,'geometry':{'trianglePairsChecked':c['trianglePairsChecked'],'newNonNeuralCrossings':0,'inheritedSelfContactPairs':1,'inheritedSelfContactRigidTranslationExact':True,'closedCorticalContactTrianglePairs':len(c['closedTargetContactsForPairedDepthGate'])},'depth':d,'distalWallClearance':full,'priorFitRetention':prior,'anatomicalAcceptance':False}
for name,data in [('native-validation.json',native),('accepted-patches.json',{'release':'0.9.112','changes':r['changes']}),('prior-fit-retention.json',prior)]:
 (W/name).write_text(json.dumps(data,indent=2)+'\n')
for name in ['accepted','candidate']:shutil.copytree(W/'replayed',W/name,dirs_exist_ok=True)
print(native['geometry'],prior)
