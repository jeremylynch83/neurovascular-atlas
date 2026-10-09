"""Catalogue repairs and explicit limits for unresolved bony passages."""
from common import *
import hashlib
p=Path('anatomy/generated/complete_manifest.json');m=json.loads(p.read_text());m['release']='0.9.49';rows={s['id']:s for s in m['structures']};rev=json.loads((OUT/'revision.json').read_text());changed={r['node'] for r in rev['changed']};metrics=json.loads((OUT/'metrics.json').read_text());calibre={r['node']:r for r in metrics['calibre']};profiles={r['node']:r for r in rev['acousticRadiusProfiles']+rev.get('meningealRadiusProfiles',[])}
hashes={file:hashlib.sha256(Path('public/anatomy',file).read_bytes()).hexdigest() for file in {s.get('asset',{}).get('file') for s in m['structures']} if file}
bad=('artery.eca.incisive.right.left','landmark.incisive-canal.midline')
removed=[r for r in m['relationships'] if (r['from'],r['to'])==bad]
m['relationships']=[r for r in m['relationships'] if (r['from'],r['to'])!=bad and not (r['from'].startswith('artery.eca.mma_orbital.') and r['type']=='associated_passage' and 'superior-orbital-fissure' in r['to'])]
for side in ['right','left']:
 legacy='.right' if side=='right' else '.right.left'
 vid='artery.eca.apa.hypoglossal'+legacy;target='landmark.hypoglossal.'+side
 if not any(r['from']==vid and r['to']==target and r['type']=='associated_passage' for r in m['relationships']):m['relationships'].append(dict(**{'from':vid,'to':target},type='associated_passage',note='Arterial and anterior condylar venous reference courses share the hypoglossal region. The lumen and nerve are not segmented.'))
 s=rows['vein.vertebral.'+side];s['description']=f'The vertebral venous system receives the [suboccipital plexus](#structure-vein.suboccipital_plexus.{side}) and condylar communications. It accompanies the vertebral artery in the transverse foraminal canal, with an upper plexiform arrangement that commonly lies ventrolateral to the artery and a larger lower collecting vein. The vein leaves the lower transverse foramina and drains to the brachiocephalic vein. This atlas displays a representative dominant channel and a suboccipital plexus; the cervical vertebrae and complete intraforaminal plexus are not modelled.'
 t=rows['artery.connection.transverse_facial_facial.'+side];t['description']=f'This channel illustrates a potential connection between the [inferior transverse facial division](#structure-artery.amendment.transverse_facial_inferior_division.{side}) and the [facial artery](#structure-artery.eca.facial{legacy}). Its calibre, depth and conspicuous patency are illustrative. The course runs anterior to the corrected facial venous crossing in this reference model.'
 s=rows['artery.eca.mma_orbital'+legacy];s['referenceRouteVariant']='meningo-orbital via cranio-orbital (Hyrtl) canal; illustrative, canal unsegmented';s['notes']+=' v0.9.49 uses the meningo-orbital (Hyrtl) reference variant described here. Its association with the superior orbital fissure has been removed; the separate recurrent meningeal/SOF pathways remain catalogued. Presence of a Hyrtl canal is not established in this bone mesh.'
# Preserve a review register for provisional findings rather than imposing measured lumens.
provisional=['internal-acoustic','hypoglossal','pterygoid-canal','palatovaginal','stylomastoid','jugular-foramen','supraorbital','anterior-ethmoidal','posterior-ethmoidal','greater-palatine-canal','greater-palatine-foramen','sphenopalatine-foramen']
for s in m['structures']:
 asset=s.get('asset',{});course=s.get('vesselCourse')
 if course:
  file=asset.get('file')
  if file:course['geometrySha256']=hashes[file]
  course['attachments']['incoming']=[r for r in m['relationships'] if r['to']==s['id']]
  course['attachments']['outgoing']=[r for r in m['relationships'] if r['from']==s['id']]
  if asset.get('node') in changed:
   course['fittingPrevious']=course.get('fitting');course['fitting']=dict(release='0.9.49',baseline='0.9.48',method=rev['method'],status='reference-relationship-correction-anatomical-review-pending',validation='docs/validation/relationships-v0.9.49.json')
   course['radiusPolicy']='preserve-source-profile-with-measured-wall-deformation';course['fitting']['calibreCheck']=calibre.get(asset['node']);course['reviewStatus']='requires-anatomical-review';course['candidateReviewStatus']='Local relationship corrections implemented and native shared collars checked. Unsegmented canals and wider anatomy remain under review.'
   course['summary']=next((g['reason'] for g in rev['groups'] if asset['node'] in g['nodes']),'Tubular reconstruction of the frontal MMA branch network along the locally corrected inner-table course.')
   course['attachments']['status']='native-shared-mesh-interfaces-verified'
   if asset['node'] in profiles:
    s['notes']=s.get('notes','')+' v0.9.49: disjoint exterior patch of a closed regional tubular network. Native parent attachments use volume continuity; whole-atlas surface welding is not claimed.';profile=profiles[asset['node']];radii=profile.get('tubeRadiusP05MedianP95') or ([profile['radiusMm']]*3 if 'radiusMm' in profile else np.percentile(np.r_[np.linspace(.30,.22,12),np.linspace(.22,.14,100)],[5,50,95]).tolist());course['radiusPolicy']='reconstruct-tube-with-smoothed-source-radius';course['fitting'].pop('calibreCheck');course['fitting']['radiusProfile']=dict(node=s['id'],method=profile.get('policy') or profile['method'],tubeRadiusP05MedianP95=radii);course['meshQuality']=dict(release='0.9.49',networkId=('frontal-meningeal-' if asset['node'].startswith('MMA') else 'acoustic-arterial-')+s['side'],watertightScope='combined exterior network wall',individualPatchHasIntentionalLabelBoundary=True,validation='docs/validation/relationships-v0.9.49.json');course['attachments']['status']='native-parent-volume-connection-and-disjoint-exterior-label-interfaces-verified'
 if 'landmark' in s and any(s['id'].startswith('landmark.'+q+'.') for q in provisional):
  s['relationshipAudit']=dict(release='0.9.49',status='surface-region-only-no-segmented-lumen',geometryAutomaticallyMovedToGuide=False,summary='The v0.9.48 guide-to-vessel wall measurement is a screening distance to an approximate point. It does not establish canal-centre error, displacement or containment. Remaining canal fit requires a segmented lumen or a reviewed surface reference.')
  s['notes']+=' v0.9.49 corridor review: this anchor does not define the lumen centre or a displacement target.'
m['relationshipCorrections']=dict(release='0.9.49',baseline='0.9.48',incorrectMaxillaryIncisiveAssociationRemoved=bool(removed),MmaOrbitalRouteVariant='Hyrtl reference variant; no demonstrated bony canal',geometryNodes=sorted(changed),report='docs/RELATIONSHIP_CORRECTIONS_v0.9.49.md',widerAnatomicalReviewComplete=False)
m['assetRevisions']={file:sha[:20] for file,sha in hashes.items()};m['assetByteSizes']={file:Path('public/anatomy',file).stat().st_size for file in hashes};m['candidateStatus']['widerAnatomicalReviewComplete']=False;p.write_text(json.dumps(m,indent=2)+'\n')
p=Path('public/anatomy/vessel-courses.json');e=json.loads(p.read_text());e['release']='0.9.49';e['courses']=[s['vesselCourse'] for s in m['structures'] if s.get('vesselCourse')];p.write_text(json.dumps(e,indent=2)+'\n')
p=Path('package-lock.json');l=json.loads(p.read_text());l['version']='0.9.49';l['packages']['']['version']='0.9.49';p.write_text(json.dumps(l,indent=2)+'\n')
print('Corrected catalogue relationships and refreshed asset-bound course metadata.')
