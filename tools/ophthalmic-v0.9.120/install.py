from pathlib import Path
import json,hashlib,shutil
R=Path('/workspace/scratch/3da1329b983b');W=R/'ophthalmic-work';A=W/'inr-anatomy-atlas-v0.9.120';B=R/'vessel-work/inr-anatomy-atlas-v0.9.119'
def read(p):return json.loads(p.read_text())
def write(p,v):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(v,indent=2,ensure_ascii=False)+'\n')
m=read(B/'anatomy/generated/complete_manifest.json');changed=read(W/'export/changes.json');names={r['node']for r in changed};hashes={f:hashlib.sha256((A/'public/anatomy'/f).read_bytes()).hexdigest()for f in m['assetRevisions']}
m['release']='0.9.120';m['assetRevisions']={f:h[:20]for f,h in hashes.items()};m['assetByteSizes']={f:(A/'public/anatomy'/f).stat().st_size for f in hashes}
for side in ['right','left']:
 rel={'from':'vein.inferior_ophthalmic.'+side,'to':'vein.superior_ophthalmic.'+side,'type':'drains_to'}
 assert rel not in m['relationships'];m['relationships'].append(rel)
for s in m['structures']:
 if s.get('vesselCourse'):s['vesselCourse']['geometrySha256']=hashes[s['asset']['file']]
 if s['id']not in names:continue
 n=s['id'];side=s['side'];v=__import__('numpy').fromfile(W/'export'/(n+'.positions.bin'),'<f4').reshape(-1,3);rec=next(r for r in changed if r['node']==n)
 s['anatomy'].update(bounds=[v.min(0).astype(float).tolist(),v.max(0).astype(float).tolist()],centroid=v.mean(0,dtype=float).tolist(),positionSha256=rec['positionSha256'],indicesSha256=rec['indicesSha256'])
 s['notes']+=' v0.9.120: a selected posterior IOV-to-SOV drainage pattern is reconstructed in the posterior orbit. Original pterygoid and cavernous junction coordinates are retained. New branch calibre is illustrative. Globe, optic nerve and extraocular muscle relationships remain unverified.'
 s['provenance']['reviewStatus']='awaiting-anatomical-review'
 if 'ref.orbital2003'not in s['provenance']['sourceRefs']:s['provenance']['sourceRefs'].append('ref.orbital2003')
 if 'inferior_ophthalmic'in n:
  s['description']=f'The inferior ophthalmic vein drains posteriorly into the [superior ophthalmic vein](#structure-vein.superior_ophthalmic.{side}), which continues to the [cavernous sinus](#structure-vein.cavernous.{side}). A communicating limb is retained towards the [pterygoid venous plexus](#structure-vein.pterygoid_plexus.{side}) through the inferior orbital fissure. This is a selected teaching pattern; orbital venous anatomy is variable.'
  summary='Posterior orbital limb joins SOV, with onward drainage to the cavernous sinus through the existing SOV course. Retain the inferior orbital fissure communication and exact pterygoid junction. New mid-branch radius 0.60 mm; native collar transitions retained.'
 else:
  s['description']+=f' A posterior orbital tributary from the [inferior ophthalmic vein](#structure-vein.inferior_ophthalmic.{side}) is represented in this reference pattern.'
  summary='Retain the existing SOV course and cavernous sinus collar. A bounded side-wall opening receives the new posterior IOV limb in the posterior orbit.'
 c=s['vesselCourse'];c['reviewStatus']='requires-anatomical-review';c['summary']=summary;c['candidateReviewStatus']='v0.9.120 local mesh and clearance checks passed; clinical anatomical review remains required.'
 c['attachments']['incoming']=[r for r in m['relationships']if r['to']==n];c['attachments']['outgoing']=[r for r in m['relationships']if r['from']==n];c['attachments']['status']='new-IOV-SOV-and-retained-pterygoid-rims-verified-as-exact-shared-boundaries'
oldregistry=m['currentDeferredReviewRegistry'];registry=read(A/oldregistry);registry['reviewRelease']='0.9.120';registry['orbitalRepairSourceChange']={'previousRegistry':oldregistry,'changedNodes':sorted(names),'scope':'Four orbital vein labels only. Prior venous and brain spatial exclusions remain stale and require review; their required source hashes are deliberately retained.'}
m['currentDeferredReviewRegistry']='anatomy/source/ophthalmic-v0.9.120/deferred-repairs.json';write(A/m['currentDeferredReviewRegistry'],registry)
m['orbitalVenousRepair']={'release':'0.9.120','baseline':'0.9.119','changedNodes':sorted(names),'report':'docs/validation/ophthalmic-v0.9.120.json','pattern':'IOV to SOV in posterior orbit, plus retained pterygoid communication','anatomicalAcceptance':'requires clinical review; missing orbital soft tissue references'}
write(A/'anatomy/generated/complete_manifest.json',m);write(A/'public/anatomy/manifest.json',m)
c=read(B/'public/anatomy/vessel-courses.json');c['release']='0.9.120';c['courses']=[s['vesselCourse']for s in m['structures']if s.get('vesselCourse')];write(A/'public/anatomy/vessel-courses.json',c)
d=read(W/'export/dsa-surfaces.json');d['sourceHashes']={f:hashes[f]for f in d['sourceHashes']};d['assetRevisions']=m['assetRevisions'];write(A/'public/anatomy/dsa-surfaces.json',d)
for file in ['package.json','package-lock.json']:
 d=read(A/file);d['version']='0.9.120'
 if file=='package-lock.json':d['packages']['']['version']='0.9.120'
 write(A/file,d)
p=A/'README.md';s=p.read_text().replace('# Neurovascular Atlas v0.9.119','# Neurovascular Atlas v0.9.120',1).replace('inr-anatomy-atlas-v0.9.119.zip','inr-anatomy-atlas-v0.9.120.zip').replace('verifies v0.9.119','verifies v0.9.120');s=s.replace('\n\n','\n\nAdds bilateral posterior inferior ophthalmic vein connections to the superior ophthalmic veins, preserving pterygoid and cavernous junctions. Conservatively softens the left IOV kink. See docs/OPHTHALMIC_v0.9.120.md. This remains a reference teaching reconstruction requiring clinical review.\n\n',1);p.write_text(s)
p=A/'CHANGELOG.md';p.write_text('# v0.9.120\n\nAdd bilateral posterior IOV-to-SOV branches with true shared wall boundaries. Preserve native pterygoid and SOV-to-cavernous collars. Soften the left IOV dip by at most 0.8 mm, maintaining clearance from infraorbital vessels. Refresh the four DSA projection recipes and anatomy metadata. Other 1,246 mesh geometries remain exact. Retain earlier brain and venous deferred review requirements.\n\n'+p.read_text())
S=A/'anatomy/source/ophthalmic-v0.9.120';S.mkdir(exist_ok=True)
for n in names:
 for suffix in ['positions.bin','indices.bin','normal-snorm16.bin']:shutil.copy2(W/'export'/(n+'.'+suffix),S/(n+'.'+suffix))
for file in ['authoring.json','geometry-check.json','selfcheck.json']:shutil.copy2(W/'candidate'/file,S/file)
for file in ['changes.json','projection-check.json','model-patch.json']:shutil.copy2(W/'export'/file,S/file)
for file in ['probe.py','repair.py','branch.py','check.py','selfcheck.py','finalise.py','projections.py','normal-inputs.mjs','install.py']:shutil.copy2(W/file,A/'tools/ophthalmic-v0.9.120'/file)
print(json.dumps({'release':m['release'],'changedNodes':sorted(names),'venousSha256':hashes['models/venous.glb']}))
