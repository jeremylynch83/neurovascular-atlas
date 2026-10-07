"""Apply source-backed corrections to the catalogue and editable source descriptions."""
import json,re
from pathlib import Path
APP=Path(__file__).resolve().parents[2]
PATH=APP/'anatomy/generated/complete_manifest.json'
m=json.loads(PATH.read_text()); assert m['release']=='0.9.28', 'Apply only to the audited v0.9.28 baseline'; rows={s['id']:s for s in m['structures']}; changed={}
def settext(sid,text):
 s=rows[sid]
 if s.get('description')!=text:changed[sid]={'before':s.get('description'),'after':text};s['description']=text
for side in ['right','left']:
 settext(f'artery.anterior.ophthalmic_{side}',f"The ophthalmic artery usually arises from the [paraophthalmic ICA](#structure-artery.anterior.internal_carotid_{side}.segment.paraophthalmic) and enters the orbit through the [optic canal](#structure-landmark.optic-canal.{side}), initially inferior or inferolateral to the optic nerve. It commonly crosses above the nerve to reach the medial orbit; an inferior crossing and other origin or course variants also occur. The atlas shows one selected pattern. Its branches include the [central retinal artery](#structure-artery.anterior.central_retinal_{side}) and posterior ciliary arteries.")
 for k in ['medial','lateral']:
  settext(f'artery.anterior.posterior_ciliary_{k}_{side}',f"The posterior ciliary arteries arise from the [ophthalmic artery](#structure-artery.anterior.ophthalmic_{side}), often through variable common trunks. Their number and origin relative to the [central retinal artery](#structure-artery.anterior.central_retinal_{side}) vary. The atlas depicts a selected {k} trunk arrangement. Short posterior ciliary branches supply the choroid and optic nerve head; long posterior ciliary branches contribute to the anterior uveal circulation.")
 settext(f'vein.internal_cerebral.{side}',"The paired internal cerebral veins form near the foramen of Monro, commonly through the union of the anterior septal and superior thalamostriate veins, with variable choroidal tributaries and venous-angle arrangements. They drain subependymal and choroidal territories and pass posteriorly in the velum interpositum along the roof of the third ventricle. The two internal cerebral veins unite beneath the splenium to contribute to the [great cerebral vein](#structure-vein.galen). The basal veins may join the internal cerebral or great cerebral veins, or follow other recognised drainage variants. The atlas shows a selected bilateral drainage pattern.")
 settext(f'artery.posterior.vertebral_{side}.segment.v1',f"The preforaminal V1 segment extends from the vertebral origin to its first transverse foramen. Entry is most often at C6; C4, C5, C7 and other entry variants occur. An aortic arch origin, especially on the left, is associated with variable entry levels and does not determine a single C4 entry. The atlas does not resolve individual cervical transverse foramina.")
 settext(f'artery.posterior.vertebral_{side}.segment.v4',f"The intradural V4 segment begins where the vertebral artery penetrates the dura near the craniocervical junction and [foramen magnum](#structure-landmark.foramen-magnum.midline). Passage through the posterior atlanto-occipital membrane belongs to the preceding extradural course and is distinct from dural penetration. V4 ascends anteromedially along the medulla and joins its counterpart to form the [basilar artery](#structure-artery.posterior.basilar), usually near the pontomedullary junction. The precise dural entry is not separately segmented in this atlas.")
 asa="The anterior spinal artery is supplied cranially by one or two variable branches of the intradural vertebral arteries. Bilateral branches may unite near the ventral medulla, or one contribution may predominate; PICA dominance does not determine the arrangement. The atlas depicts bilateral contributions to a single anterior spinal axis. Its union is not assigned a cervical vertebral level because those levels are not resolved. The longitudinal artery is reinforced by segmental radiculomedullary contributions and supplies the anterior spinal cord; its calibre and reinforcement pattern vary."
 settext('artery.posterior.anterior_spinal',asa)
 settext(f'artery.posterior.anterior_spinal_root_{side}',f"Selected {side} vertebral contribution to the [anterior spinal artery](#structure-artery.posterior.anterior_spinal). "+asa)
 sid=f'artery.anterior.temporo_occipital_{side}';text=rows[sid]['description'];text=re.sub(r'The temporo \[occipital artery\]\([^)]*\)', 'The temporo-occipital artery',text);settext(sid,text)
 old=f'artery.anterior.internal_carotid_{side}.segment.petrous';new=f'artery.anterior.internal_carotid_{side}.segment.cavernous';sid=f'artery.anterior.vidian_ica_contribution_{side}'
 rows[old]['children'].remove(sid);rows[new]['children'].append(sid);rows[sid]['parent']=new
 for r in m['relationships']:
  if r['from']==old and r['to']==sid and r['type']=='branches_to':r['from']=new
 rows[sid]['vesselCourse']['attachments']['parentId']=new
 for r in rows[sid]['vesselCourse']['attachments']['incoming']:
  if r['from']==old and r['type']=='branches_to':r['from']=new
 settext(sid,rows[sid]['description']+"\n\nThe ICA contribution may arise from the petrous or adjacent lacerum region. In this selected reconstruction its ostium lies on the lower mesh labelled cavernous in the NYU scheme, so the catalogue parent follows that physical attachment. This label assignment does not make cavernous origin universal.")
 for seg in ['cavernous','paraophthalmic']:
  sid=f'artery.anterior.internal_carotid_{side}.segment.{seg}'
  settext(sid,rows[sid].get('description','')+"\n\nv0.9.29: the mesh partition at the proximal dural ring region is aligned to the existing estimated skull base reference. The cavernous label ends at that regional boundary; the continuing clinoid/ring transition belongs to the NYU paraophthalmic label. The ring itself is not segmented, so this is a provisional anatomical boundary, not a patient-specific intradural classification.")
old="The branches supply most of the lateral cerebral hemisphere, and the insular and opercular cortex."
new="The M4 cortical branches supply the cerebral convexity. The MCA as a whole also supplies the insular and opercular cortex through earlier branches, associated with the M2 insular and M3 opercular portions."
for s in rows.values():
 if old in s.get('description',''):settext(s['id'],s['description'].replace(old,new))
# Update editable source descriptions, keeping historical evidence snapshots untouched.
for rel in ['anatomy/source/venous/courses.json']:
 p=APP/rel;data=json.loads(p.read_text())
 for s in data.get('structures',[]):
  if s.get('id') in changed:s['description']=changed[s['id']]['after']
 p.write_text(json.dumps(data,indent=2)+'\n')
m['release']='0.9.29';PATH.write_text(json.dumps(m,indent=2)+'\n')
(ROOT if False else APP/'docs/validation').mkdir(exist_ok=True)
(APP/'docs/validation/anatomical-text-corrections-v0.9.29.json').write_text(json.dumps({'release':'0.9.29','changedDescriptions':changed,'parentCorrections':[f'artery.anterior.vidian_ica_contribution_{s}' for s in ['right','left']]},indent=2)+'\n')
print('Corrected descriptions:',len(changed))
