from region import *
import shutil,hashlib,zipfile
def read(n):return json.load(open(W/n))
def write(p,d):p.write_text(json.dumps(d,indent=2)+'\n')
r=read('reconstruction-validation.json');c=read('crossing-validation.json');d=read('depth-validation.json');full=read('full-clearance-validation.json');native=read('native-validation.json');ex=read('export-validation.json');pr=read('projection-refresh.json');fl=read('flow-refresh.json');ret=read('integration-retention.json')
assert r['passed'] and all(x['replayedBuffersByteExact']for x in r['changes']) and d['passed'] and full['passed'] and native['passed'] and ex['passed'] and pr['passed'] and fl['passed'] and c['passedNoNewNonNeuralCrossings']
assert len(c['inheritedSourceCrossings'])==2 and native['geometry']['inheritedSelfContactRigidTranslationExact']
assert all(x['before']==x['after']for x in ret['selectedLabelTopology'])
assert 'Ran 22 tests'in(W/'repair-test.log').read_text() and (W/'repair-test.log').read_text().rstrip().endswith('OK')
assert 'Ran 3 tests'in(W/'clearance-test.log').read_text() and (W/'clearance-test.log').read_text().rstrip().endswith('OK')
assert 'built in'in(W/'build.log').read_text();dt=(W/'dsa-test.log').read_text();assert 'Invalid: []'in dt and '828 meshes, 8971510 triangles'in dt and 'Validated 579 selectable arterial courses, 2353 closed sections'in dt
scan=read('final-scan/degenerate-scan.json');assert sum(len(x['zeroAreaFaceIds'])for x in scan['rows'])==7
for n in ['ANATOMICAL_ISSUES.json','ANATOMICAL_ISSUES.md']:
 for sub in ['public','public/anatomy']:assert(A/n).read_bytes()==(A/sub/n).read_bytes()
issues=json.load(open(A/'ANATOMICAL_ISSUES.json'));assert issues['reviewVersion']=='0.9.112' and sum(len(x['failedNativeInterfaces'])for x in issues['segments'])==1
assert(A/'public/anatomy/models/complete-circulation.glb').read_bytes()==(W/'complete-circulation.glb').read_bytes()
selected={x['id']for x in pr['changes']};shape=[]
with zipfile.ZipFile(R/'inr-anatomy-atlas-v0.9.111.zip')as z:
 for name in ['dsa-surfaces.json','dsa-flow.json']:
  old=json.loads(z.read('inr-anatomy-atlas-v0.9.111/public/anatomy/'+name));now=json.load(open(A/'public/anatomy'/name))
  assert old['entries'].keys()==now['entries'].keys() and all(v==now['entries'][k]for k,v in old['entries'].items()if k not in selected)
  if name=='dsa-flow.json':
   for k in ['generatorHash','graphHash','graphSource','veinSites']:assert old[k]==now[k],k
  else:
   for row in pr['changes']:
    n=row['node'];v=np.fromfile(W/'decoded'/(n+'.positions.bin'),'<f4').reshape(-1,3);p=np.fromfile(W/'candidate'/(n+'.positions.bin'),'<f4').reshape(-1,3);f=np.fromfile(W/'decoded'/(n+'.indices.bin'),'<u4').reshape(-1,3)
    def areas(q):
     t=q[f].astype(float);return np.linalg.norm(np.cross(t[:,1]-t[:,0],t[:,2]-t[:,0]),axis=1)/2
    ratio=areas(p)/areas(v);volume=old['entries'][row['id']]['volumeMm3'];shape.append({'node':n,'sourceAreaRatioMin':float(ratio.min()),'sourceAreaRatioMax':float(ratio.max()),'proxyVolumeBeforeMm3':volume,'proxyVolumeAfterMm3':row['volumeMm3'],'proxyVolumeRelativeChangePercent':100*(row['volumeMm3']/volume-1)})
write(W/'shape-measures.json',shape)
native['reconstruction']=r;native['changes']=r['changes'];write(W/'native-validation.json',native)
E=A/'anatomy/source/aca-tail-v0.9.112';E.mkdir(parents=True,exist_ok=True)
for n in ['decoded','accepted','candidate','replayed']:shutil.copytree(W/n,E/n,dirs_exist_ok=True)
for p in W.glob('*.json'):shutil.copy2(p,E/p.name)
for p in W.glob('*.log'):shutil.copy2(p,E/p.name)
for n in ['accept.py','integrate.py','finalize.py','retention.py','package.py']:shutil.copy2(W/n,E/n)
shutil.copy2(W/'native-validation.json',E/'replay-validation.json');shutil.copy2(W/'final-scan/degenerate-scan.json',E/'remaining-zero-area.json')
T=E/'screened-trials';T.mkdir(exist_ok=True)
for p in W.glob('*trial.py'):shutil.copy2(p,T/p.name)
for p in W.glob('*trial.json'):shutil.copy2(p,T/p.name)
shutil.copy2(W/'region.py',T/'region.py');shutil.copytree(W/'rejected-whole-tail',T/'rejected-whole-tail',dirs_exist_ok=True)
write(T/'dispositions.json',{'installedSpec':'../spec.json','initialMedialAndLateralTailMoves':'Excluded: extra corpus-callosum depth, new entry, vessel crossings or reversed faces.','upwardWholeTailMoves':'Excluded: contacts with the open left posteroventral cingulate surface. Closed-target sample checks alone were insufficient.','narrowAnteriorRampWidth0_5':'Excluded: twelve faces oppose their original normals.','posteriorSupportMinus96_9':'Excluded: fifteen new contacts with the open posteroventral cingulate surface.','accepted':'Bounded source Y -96.3 to -94.3 mm; full translation from -95.7 to -95.1 mm. Five native interfaces, prior fit and terminal tip fixed. No new crossings or sampled depth regressions.','sourceSelfContact':'Source faces 1156 and 1222 already cross. All their vertices and stored normals undergo the same exact rigid translation. One unique pair remains unresolved.','clearanceScope':'Only the distal 1,209-triangle section at source Y <= -95.1 mm is continuously certified outside the corpus callosum. Whole-label clearance is not claimed.'})
write(E/'checksums.json',{p.relative_to(E).as_posix():hashlib.sha256(p.read_bytes()).hexdigest()for sub in ['decoded','accepted','candidate','replayed']for p in(E/sub).rglob('*')if p.is_file()})
depth=next(x for x in d['changes'][0]['targets']if x['target']=='brain.corpus-callosum');proof=full['targets'][0]['proof'];sh=shape[0]
report={'release':'0.9.112','baseline':'0.9.111','batch':20,'anatomicalAcceptance':False,'scope':read('spec.json')['scope'],'changes':r['changes'],'addedOrRemovedVertices':0,'addedOrRemovedTriangles':0,'newNonNeuralCrossings':0,'inheritedSelfContactPairs':1,'inheritedSelfContactRigidTranslationExact':True,'depthValidation':d,'distalWallClearance':full,'wholeLabelClearance':False,'shapeMeasures':shape,'exportValidation':ex,'projectionValidation':pr,'flowValidation':fl,'retention':ret,'priorFitRetention':read('prior-fit-retention.json'),'unselectedMeshesByteExact':1249,'finalUnselectedRecipesExact':827,'finalUnselectedCoursesExact':596,'remainingZeroAreaFaces':7,'originalUnresolvedILTInterfaceRetained':True,'verification':{'fullBuild':'passed','repairTests':22,'clearanceTests':3,'dsa':'passed','closedOrientedProxies':828,'proxyTriangles':8971510,'selectableArterialCourses':579,'closedSections':2353,'fullAtlasRenderPerformed':False},'evidence':'anatomy/source/aca-tail-v0.9.112','limitations':['Residual left A5 attachment/transition overlap remains. The complete ACA/cortical registration is unresolved.','One source self-contact pair is rigidly preserved, not repaired.','Certificate margins are mathematical lower bounds, not physiological clearances.','Native seam retention does not certify receiving-lumen continuity.','Other regional findings, ILT interface, seven zero-area arterial faces and PICA/native-wall findings remain open.','No independent anatomical imaging or target segmentation was introduced.']}
write(A/'docs/validation/aca-tail-v0.9.112.json',report)
doc=f'''# Distal left A5 shaft fit batch 20, v0.9.112

This bounded fit reduces left A5/corpus-callosum overlap. It moves 463 existing vertices outward by 0.5 mm and superiorly by 0.5 mm at most, a maximum displacement of 0.707107 mm. All 4,473 vertices and 8,424 original face indices remain. The fit affects 998 physical faces. All five native interfaces and 524 shared coordinates remain fixed: left A4 (64), falcine branch (101), inferior internal parietal (142), long callosal (71) and precuneal (146). All 524 boundary edges/vertices remain fixed, with zero bad edges and unchanged weld partitions and connectivity.

The maximum sampled corpus-callosum depth over the changed region falls from {depth['maximumDepthBeforeMm']:.9f} to {depth['maximumDepthAfterMm']:.9f} mm. Inside samples fall from 1,317 to 584. These are repeated face samples, not independent anatomical defect counts. Residual transition/attachment overlap remains. This is a partial correction, not whole-label clearance or anatomical acceptance.

## Defined correction and retained geometry

The quintic compact bump has source-Y support [-96.3, -94.3] mm and plateau [-95.7, -95.1] mm. The posterior transition width is 0.6 mm; the anterior width is 0.8 mm. Y stays fixed. Each analytical constant-Y section translates rigidly and the analytical Jacobian determinant is one. Every source face retains positive orientation relative to its original normal.

All 4,010 vertices outside the support retain positions and stored normals exactly. This includes the earlier mid-shaft fit and terminal tip. Both A4s, right A5 (including batch 19 clearance), branch roots and all 1,249 other named meshes remain exact. Changed coordinates are checked against all 766 arterial meshes; no coordinate weld is added. All 21 runtime source files, 1,250 meshes, 1,666 catalogue structures, relationships and asset bindings are retained.

## Tissue and crossing gates

The paired depth gate checks 6,986 matching changed-face corner, edge-midpoint and centroid samples against all nearby brain/bone targets. It finds no new sampled tissue entry, no extra depth and no signed-distance/enclosed-volume disagreement above 0.0001 mm. Open target surfaces require conservative enclosing-ball separation, including the left posteroventral cingulate surface. Its open topology does not support an absolute-inside claim.

The complete changed-face crossing check tests 19,786 triangle pairs and finds zero new non-neural crossings. The remaining 42 closed-target contact triangle pairs are the known residual corpus-callosum overlap and are covered by the paired depth gate.

One native self-contact pair, source faces 1156 and 1222, already exists. Both triangles lie entirely on the rigid plateau. Their positions undergo the same exact [-0.5, 0, +0.5] mm translation and their stored normals remain exact. The two directional records describe one unique pair. This native tessellation issue remains unresolved and is not counted as a new contact or a repaired defect.

## Continuous distal-section clearance

All 1,209 wall triangles whose original vertices have Y <= -95.1 mm are continuously certified outside the complete closed corpus-callosum surface. The section includes the posterior transition and fixed tip. Whole-label clearance is not claimed. In 8,463 matched section samples, inside samples fall from 231 to zero and sampled depth from 0.110128246 mm to zero. Original face-centroid signs agree with enclosed-volume parity.

The enclosing signed-distance ball proof evaluates {proof['evaluatedBalls']:,} balls and certifies {proof['certifiedLeafTriangles']:,} leaf triangles, with maximum subdivision depth {proof['maximumSubdivisionDepth']}. Every leaf must have signed distance at its centre minus enclosing radius, including the numerical buffer, greater than 0.00001 mm. No unresolved leaf is permitted. Certified leaf area {proof['certifiedAreaMm2']:.12f} mm² covers the original section area {proof['sourceTriangleAreaMm2']:.12f} mm² within the recorded tolerance. The minimum certified margin is {proof['minimumCertifiedClearanceMarginMm']:.12f} mm. This is a conservative lower bound, not a measured anatomical clearance.

## Export, shape and application checks

Fixed and plateau normals retain source SNORM16 integers. Flank normals use the inverse transpose of the analytical shear followed by one SNORM16 encoding. Independent replay reproduces accepted positions, normals and indices byte for byte. GLTFLoader verifies all 599 circulation meshes, including 598 unchanged meshes, all accepted buffers and every original source face index. Four other GLBs remain byte-exact.

Physical face-area ratios range from {sh['sourceAreaRatioMin']:.6f} to {sh['sourceAreaRatioMax']:.6f}. The DSA proxy volume changes from {sh['proxyVolumeBeforeMm3']:.9f} to {sh['proxyVolumeAfterMm3']:.9f} mm³ ({sh['proxyVolumeRelativeChangePercent']:.9f}%). The discretised mesh measurement is distinct from the exact analytical unit-determinant mapping.

Only the selected position-only DSA recipe and course are refreshed. Source index lineage, sanitised flips/removals, cap positions/connectivity and native rims remain exact. The proxy remains closed, oriented and positive-volume. All 827 other recipes and 596 other courses remain exact after the final build. Selectability, directed connections, graph, vein sites, generator and unrelated edge distances remain exact.

The full build, 22 repair tests, three clearance tests and DSA checks pass: 828 closed/oriented proxies, 8,971,510 triangles, 579 selectable arterial courses and 2,353 closed sections. Issue-register copies agree. No full-atlas render was performed.

## Excluded trials and remaining work

Whole-tail medial/lateral/upward alternatives introduce vessel contacts, extra tissue depth, new entry or open cortical contacts. A narrower anterior transition reverses twelve faces. An earlier posterior support still introduces fifteen open cortical contacts. These are excluded. Keeping the terminal tip fixed removes those contacts while preserving the overlap reduction.

Residual left A5 attachment/transition overlap, one retained native self-contact pair, wider ACA/callosal/cortical registration, receiving lumens, Galenic/petrosal/dural/canal findings, seven zero-area arterial triangles, PICA/ACom/native-wall issues and the separate ILT interface remain open. No independent imaging or segmentation was added.

Evidence: anatomy/source/aca-tail-v0.9.112. Replay tools: tools/aca-tail-v0.9.112. Report: docs/validation/aca-tail-v0.9.112.json.
'''
(A/'docs/ACA_TAIL_BATCH20_v0.9.112.md').write_text(doc)
for rel in ['docs/validation/aca-tail-v0.9.112.json','docs/ACA_TAIL_BATCH20_v0.9.112.md']:
 dest=A/'public'/rel;dest.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(A/rel,dest)
(A/'tools/aca-tail-v0.9.112/README.md').write_text('''# Bounded distal left A5 fit, v0.9.112

Copy anatomy/source/aca-tail-v0.9.112 to WORK before replay. Use absolute WORK and CACHE paths. The historical source GLB is recoverable from v0.9.111.

- reconstruct.py WORK CACHE replays spec.json from immutable decoded baseline buffers, checking fixed native interfaces/boundaries, normals, source face orientation, weld partitions and every arterial mesh. Accepted buffers must match byte for byte.
- validate_crossings.py WORK CACHE checks every changed face against the entire scene, including self/adjacent faces. Zero new non-neural crossings are allowed. One unique source self-contact pair (1156,1222) remains; acceptance also proves exact rigid translation and unchanged stored normals for all its vertices.
- validate_depth.py WORK CACHE checks matched samples against closed tissue volumes, with no new entry or depth increase over 0.001 mm. Open surfaces require enclosing-ball separation. Residual embedding is explicitly retained.
- validate_full_clearance.py WORK CACHE certifies only the distal 1,209-triangle section at source Y <= -95.1 mm outside the corpus callosum. Despite its inherited filename, it does not certify the whole A5 label. Area coverage and centroid parity are checked. Unresolved leaves fail.
- test_clearance.py checks separated, crossing and touching analytic cases.
- decode-normals.mjs SOURCE_GLB WORK/decoded extracts raw SNORM16 normals.
- export.mjs WORK SOURCE_GLB OUTPUT_GLB requires passing native-validation.json. verify-export.mjs WORK checks exact accepted buffers, all face indices, retained corner normals, 598 other circulation meshes and four other GLBs.
- projections.py WORK CACHE preserves source index lineage, caps and native rims while updating the selected proxy positions.
- Refresh only the ID in selected-course-ids.json. verify-flow.mjs WORK preserves all unselected courses and graph semantics; it requires old-dsa-flow.json.

See docs/ACA_TAIL_BATCH20_v0.9.112.md for scope, excluded trials and unresolved findings. No full-atlas render is required for this bounded correction.
''')
print({'release':'0.9.112','checks':'passed','shape':shape,'evidenceFiles':sum(p.is_file()for p in E.rglob('*'))})
