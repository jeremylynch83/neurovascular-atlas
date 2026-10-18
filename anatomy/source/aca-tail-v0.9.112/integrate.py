from region import *
import hashlib,shutil
def read(n):return json.load(open(W/n))
def write(p,d):p.write_text(json.dumps(d,indent=2)+'\n')
gate=read('native-validation.json');assert gate['passed'] and read('export-validation.json')['passed'] and read('projection-refresh.json')['passed']
ch=gate['changes'][0];n=ch['node'];old=hashlib.sha256((W/'old-complete-circulation.glb').read_bytes()).hexdigest();new=hashlib.sha256((W/'complete-circulation.glb').read_bytes()).hexdigest()
depth=next(x for x in gate['depth']['changes'][0]['targets']if x['target']=='brain.corpus-callosum')
review={'release':'0.9.112','report':'docs/validation/aca-tail-v0.9.112.json','changedMeshes':[n],'changedVertices':ch['changedVertices'],'changedFaces':ch['changedFaces'],'maximumDisplacementMm':ch['maximumDisplacementMm'],'fixedNativeInterfaces':len(ch['attachments']),'fixedSharedCoordinates':sum(a['sharedCoordinates']for a in ch['attachments']),'allSourceFaceIndicesExact':True,'newNonNeuralCrossings':0,'newSampledTissueEntry':0,'maximumExtraDepthMm':0,'corpusCallosumDepth':depth,'distalWallClearance':{'sourceYMaximumMm':-95.1,'trianglesChecked':1209,'continuousSeparationCertified':True},'inheritedSelfContactPairs':1,'inheritedSelfContactRigidTranslationExact':True,'anatomicalAcceptance':False,'scope':read('spec.json')['scope']}
for rel in ['anatomy/generated/complete_manifest.json','public/anatomy/vessel-courses.json']:
 d=json.loads((A/rel).read_text().replace(old,new).replace(old[:20],new[:20]));d['release']='0.9.112'
 if 'structures'in d:
  for s in d['structures']:
   if s.get('asset',{}).get('node')!=n:continue
   p=np.fromfile(W/'candidate'/(n+'.positions.bin'),'<f4').reshape(-1,3);f=np.fromfile(W/'candidate'/(n+'.indices.bin'),'<u4').reshape(-1,3)
   s['anatomy'].update(bounds=[p.min(0).tolist(),p.max(0).tolist()],centroid=p.astype(float).mean(0).tolist(),positionSha256=hashlib.sha256(p.tobytes()).hexdigest(),indicesSha256=hashlib.sha256(f.tobytes()).hexdigest())
   s['notes']+=' v0.9.112: bounded distal left A5 shaft fit, up to 0.707107 mm outward/superior. All five native interfaces, prior fit and terminal tip fixed. Corpus-callosum overlap reduced; 1,209 distal wall triangles continuously separated. Residual attachment overlap and one rigidly retained native self-contact pair remain open.'
  d['assetByteSizes']['models/complete-circulation.glb']=(W/'complete-circulation.glb').stat().st_size;d['acaTailBatch20']=review;d['candidateStatus']='v0.9.112: bounded distal left A5 fit reduces corpus-callosum overlap and certifies a distal wall section clear. All native interfaces, previous repairs and terminal tip retained. Residual ACA/cortical registration and native self-contact remain open.'
 write(A/rel,d)
shutil.copy2(W/'complete-circulation.glb',A/'public/anatomy/models/complete-circulation.glb');d=read('updated-dsa-surfaces.json');d['sourceHashes']['models/complete-circulation.glb']=new;d['assetRevisions']['models/complete-circulation.glb']=new[:20];write(A/'public/anatomy/dsa-surfaces.json',d)
for rel in ['package.json','package-lock.json']:
 d=json.load(open(A/rel));d['version']='0.9.112'
 if 'packages'in d:d['packages']['']['version']='0.9.112'
 write(A/rel,d)
p=A/'ANATOMICAL_ISSUES.json';d=json.load(open(p));d['reviewVersion']='0.9.112';d['acaTailBatch20']=review;d['reviewFindings']['G05']['leftA5DistalFitBatch20']=review;d['reviewFindings']['G05']['status']='bilateral-distal-A5-local-improvements-regional-registration-open'
if n not in d['geometryChangesSinceCheckpoint']:d['geometryChangesSinceCheckpoint'].append(n)
assert sum(len(s['failedNativeInterfaces'])for s in d['segments'])==1;write(p,d)
p=A/'README.md';s=p.read_text();head,rest=s.split('The models use',1);head=head.replace('v0.9.111','v0.9.112');parts=head.split('\n\n');parts[2]='v0.9.112 fits a bounded distal left A5 shaft region outward/superior by up to 0.707107 mm. It reduces sampled corpus-callosum depth from 0.255 to 0.195 mm and certifies 1,209 distal wall triangles clear. All five native interfaces, earlier repairs and the terminal tip remain exact. Residual attachment overlap, one retained native self-contact pair and wider anatomical findings remain open.';p.write_text('\n\n'.join(parts)+'The models use'+rest+'\nACA distal fit batch 20: see docs/ACA_TAIL_BATCH20_v0.9.112.md.\n')
p=A/'CHANGELOG.md';p.write_text('# v0.9.112\n\n- Fit 463 existing distal left A5 vertices outward/superior within a bounded shaft region, preserving all 8,424 source faces and five native interfaces.\n- Reduce sampled corpus-callosum overlap; continuously certify separation for the 1,209-triangle distal wall section. Residual attachment/transition overlap remains.\n- Keep the terminal tip, all previous repairs and all other meshes exact. One existing self-contact pair remains rigidly translated and unresolved.\n- Refresh only the selected DSA recipe/course; preserve wider anatomical issues as open.\n\n'+p.read_text())
p=A/'ANATOMICAL_ISSUES.md';p.write_text(p.read_text().replace('corrections through v0.9.111.','corrections through v0.9.112.')+'\n## Distal left A5 shaft fit batch 20, v0.9.112\n\nA bounded 0.707107 mm outward/superior fit moves 463 existing vertices and affects 998 source triangles. All 8,424 face indices, five native interfaces (524 shared coordinates), previous fit regions, terminal tip and all other meshes remain exact. Sampled corpus-callosum depth falls from 0.255 to 0.195 mm; continuous separation is certified for 1,209 distal wall triangles with source Y <= -95.1 mm. The transition/attachment overlap and one rigidly retained native self-contact pair remain unresolved. Wider G05/G06 and other regional findings remain open. See [batch 20](docs/ACA_TAIL_BATCH20_v0.9.112.md).\n')
for name in ['ANATOMICAL_ISSUES.json','ANATOMICAL_ISSUES.md']:
 for sub in ['public','public/anatomy']:shutil.copy2(A/name,A/sub/name)
write(W/'batch-review.json',review);print(review)
