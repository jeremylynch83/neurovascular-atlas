#!/usr/bin/env python3
"""Editable venous teaching reconstruction, v0.9.0. Not part of app build.

RAS millimetres in the existing atlas frame. Sparse manually authored courses
follow Lynch pp62-76/Figs2.16-2.19. Bone fitting is a separate authoring pass.
No source PDF, patient images or third-party image pixels are redistributed.
"""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'anatomy/source/venous'
OUT.mkdir(parents=True,exist_ok=True)
rows=[]; relations=[]
colours={'dural':'#6f95e8','superficial':'#74bde8','deep':'#939de8','posterior':'#76c7d3','extracranial':'#598fcd','skullbase':'#839acb'}
def ref(key,side=None): return 'vein.'+key+('.'+side if side else '')
def add(key,name,group,points,radius,description='',side=None,parent=None,fit=None,aliases=(),page=64,shape='round'):
 sid=ref(key,side)
 rows.append(dict(id=sid,name=name+(' '+side if side else ''),group=group,parent=parent or 'vein.'+group,side=side or 'midline',points=points,radius=radius,description=description,fit=fit,aliases=list(aliases),page=page,shape=shape,color=colours[group]))
 return sid
def rel(a,b,kind='drains_to'): relations.append({'from':a,'to':b,'type':kind})
def link(key,text,side=None):return f'[{text}](#structure-{ref(key,side)})'
def attach(key,t=1,side=None):return {'structure':ref(key,side),'fraction':t}

tor=[.65,-144.5,67]
add('confluence','Confluence of sinuses','dural',[[.65,-142,68],tor,[.65,-147,66]],3.5,
 'The confluence joins the '+link('superior_sagittal','superior sagittal')+', '+link('straight','straight')+', and '+link('occipital_sinus','occipital sinuses')+' and drains into the transverse sinuses.',aliases=['Torcula','Torcular Herophili'],fit='dural',page=64)
add('superior_sagittal','Superior sagittal sinus','dural',[[.65,8,80],[.65,17,109],[.65,-2,142],[.65,-35,160],[.65,-77,167],[.65,-117,150],[.65,-143,119],[.65,-151,90],attach('confluence',.5)], [1.2,3.4],
 'The superior sagittal sinus extends from the foramen caecum to the '+link('confluence','confluence of sinuses')+'. It is located within the superior attachment of the falx to the calvarium. It receives the superficial cerebral veins from the medial and lateral cerebral hemispheres, the largest of which is the vein of Trolard.',parent=ref('confluence'),aliases=['SSS'],fit='dural',shape='sinus')
add('straight','Straight sinus','dural',[[.65,-103,101],[.65,-114,93],[.65,-129,80],attach('confluence',.5)], [2.4,3.1],
 'The straight sinus is an unpaired structure located at the junction between the falx and tentorium in the midline, and it follows a straight course posteriorly. It receives blood from the '+link('inferior_sagittal','inferior sagittal sinus')+', '+link('galen','vein of Galen')+', posterior cerebral veins, superior cerebellar veins, and falx cerebri, and drains into the '+link('confluence','confluence of sinuses')+'.',parent=ref('confluence'),shape='sinus')
add('inferior_sagittal','Inferior sagittal sinus','dural',[[.65,-14,124],[.65,-35,133],[.65,-64,135],[.65,-86,124],attach('straight',0)], [0.65,1.45],
 'This lies in the inferior edge of the falx parallel to the '+link('superior_sagittal','superior sagittal sinus')+'. It receives blood from the anterior corpus callosum, cingulate gyrus, medial cerebral hemispheres, and the falx. It joins the '+link('galen','vein of Galen')+' to form the '+link('straight','straight sinus')+'.',parent=ref('straight'),aliases=['ISS'])
add('occipital_sinus','Occipital sinus','dural',[[.65,-104,35],[.65,-122,40],[.65,-138,52],attach('confluence',.65)], [1,1.6],
 'The occipital sinus usually drains superiorly to the '+link('confluence','confluence')+' but may drain inferiorly to the sigmoid or '+link('marginal','marginal sinuses')+'. It is often hypoplastic or absent in adults.',parent=ref('confluence'),page=67)
add('marginal','Marginal sinus','dural',[[.65,-104,35],[12,-99,34],[18,-88,32],[13,-73,34],[.65,-68,35],[-11.7,-73,34],[-16.7,-88,32],[-10.7,-99,34],[.65,-104,35]],1.05,
 'The marginal sinus encircles the foramen magnum and is connected to a network of adjacent venous structures including the '+link('basilar_plexus','clival plexus')+' anteriorly, the vertebral venous plexus inferiorly, and sigmoid sinuses laterally.',page=67)
add('galen','Vein of Galen','deep',[[.65,-92,96],[.65,-96,97],[.65,-100,100],attach('straight',0)], [2.5,2.8],
 'This short subarachnoid vessel is formed by the midline convergence of the internal cerebral veins, below the splenium, beneath which it curves. It ends at the tentorial hiatus apex, where it joins the '+link('inferior_sagittal','inferior sagittal sinus')+' to become the '+link('straight','straight sinus')+'. The vessel also receives blood from the posterior pericallosal veins, the internal occipital veins, and veins of the posterior fossa.',aliases=['Great cerebral vein','Great vein of Galen'],page=72)

for side,sign in [('right',1),('left',-1)]:
 def p(x,y,z):return [x if sign==1 else 1.30-x,y,z if sign==1 else z-.05]
 def pts(*values):return [p(*v) for v in values]
 def a(key,t=1):return attach(key,t,side)
 def L(key,text):return link(key,text,side)
 # Outflow first, so all dependent endpoint attachments resolve deterministically.
 ijv=add('internal_jugular','Internal jugular vein','extracranial',pts((27,-65,38),(30,-66,26),(31,-61,4),(34,-59,-28),(34,-53,-60),(30,-46,-107)),[4.2 if sign==1 else 3.7,4.8 if sign==1 else 4.2],
  'Together with the vertebral venous plexus, the IJV is the largest drainage pathway for the brain, face, and neck. It is the continuation of the '+L('sigmoid','sigmoid sinus')+' in the jugular foramen, runs vertically in the carotid sheath in the neck, and joins the subclavian vein to form the brachiocephalic vein. Its tributaries include the '+L('inferior_petrosal','inferior petrosal sinus')+', anterior condylar vein, facial vein, lingual vein, pharyngeal vein, superior thyroid vein, and middle thyroid vein.',side=side,aliases=['IJV','Internal jugular'],page=62)
 add('sigmoid','Sigmoid sinus','dural',pts((58,-95,66),(54,-89,61),(46,-92,48),(34,-86,40),(28,-73,37))+[a('internal_jugular',0)],3.5 if sign==1 else 3.0,
  'This is the anteromedial inferior continuation of the '+L('transverse','transverse sinus')+' and ends within the jugular fossa. It receives blood from the pons and medulla. It also connects to the scalp veins through the mastoid and condylar veins.',side=side,page=67)
 add('transverse','Transverse sinus','dural',[attach('confluence',.5)]+pts((20,-143,67),(40,-132,67),(53,-114,67))+[a('sigmoid',0)],3.0 if sign==1 else 2.6,
  'The transverse sinuses arise at the '+link('confluence','confluence of sinuses')+' and sweep around anterolaterally, confined by the tentorium. They receive veins from the temporal and occipital lobes, particularly the '+L('labbe','vein of Labbé')+', cerebellar veins, and the '+L('superior_petrosal','superior petrosal sinus')+'. Hypoplasia of one or the other is common, usually the left.',side=side,parent=ref('sigmoid',side),fit='dural',page=67,shape='sinus')
 add('cavernous','Cavernous sinus','dural',pts((15,-49,56),(14,-47,63),(13,-42,67),(14,-35,69)),[3.6,4.6],
  'The cavernous sinuses are located on each side of the pituitary fossa. They are an important bidirectional confluence of the intracranial and extracranial venous systems. The sinus contains the ICA, its sympathetic plexus, and the abducens nerve (CN VI). Within the lateral wall, from superior to inferior, are CN III, CN IV, CN V1, and CN V2. The cavernous sinuses connect to the ophthalmic veins, '+L('pterygoid_plexus','pterygoid plexus')+', '+L('superior_petrosal','superior petrosal sinus')+', '+L('inferior_petrosal','inferior petrosal sinus')+', '+link('basilar_plexus','basilar plexus')+', and contralateral cavernous sinus through the intercavernous sinuses.',side=side,aliases=['CS'],page=68)
 add('superior_petrosal','Superior petrosal sinus','dural',[a('cavernous',.25)]+pts((24,-60,64),(38,-71,66),(48,-82,67))+[a('sigmoid',0)],1.45,
  'These run in the petrosal ridge to connect the posterior aspect of the '+L('cavernous','cavernous sinus')+' to the junction of the '+L('transverse','transverse')+' and '+L('sigmoid','sigmoid sinuses')+'. They may receive blood from supra- or infratentorial structures.',side=side,parent=ref('cavernous',side),aliases=['SPS'],page=67)
 add('inferior_petrosal','Inferior petrosal sinus','dural',[a('cavernous',.1)]+pts((15,-55,52),(19,-61,45),(24,-65,38))+[a('internal_jugular',.065)],1.4,
  'These sinuses run inferiorly and laterally to connect the posterior aspect of the '+L('cavernous','cavernous sinus')+' to the '+L('internal_jugular','jugular vein')+' in the pars nervosa. They also receive blood from the internal auditory veins and infratentorial structures.',side=side,parent=ref('cavernous',side),aliases=['IPS'],page=67)
 add('sphenoparietal','Sphenoparietal sinus','dural',pts((48,-20,83),(40,-18,79),(29,-22,76),(22,-28,74))+[a('cavernous',.9)],1.25,
  'This runs along the lesser sphenoid wing, receiving adjacent Sylvian, uncal, inferior frontal, meningeal, diploic, and orbital veins before draining into the '+L('cavernous','cavernous sinus')+'. Variants may drain into the transverse sinus, superior petrosal sinus, tentorial sinuses, or pterygoid venous plexus.',side=side,parent=ref('cavernous',side),page=67)
 # Superficial collectors. A balanced, communicating pattern is represented.
 add('superficial_middle_cerebral','Superficial middle cerebral vein','superficial',pts((64,-72,111),(62,-60,107),(57,-41,97),(53,-27,87))+[a('sphenoparietal',.05)],1.3,
  'The superficial middle cerebral (Sylvian) vein arises in the Sylvian fissure and drains the adjacent operculum. It empties anteriorly into the '+L('cavernous','cavernous sinus')+' or '+L('pterygoid_plexus','pterygoid venous plexus')+'.',side=side,aliases=['SMV','SMCV','Superficial Sylvian vein'],page=69)
 add('trolard','Superior anastomotic vein of Trolard','superficial',[a('superficial_middle_cerebral',.12)]+pts((63,-70,124),(55,-77,145),(36,-87,159),(17,-91,161))+[attach('superior_sagittal',.55)], [1.35,1.8],
  'The superior anastomotic vein of Trolard is the largest anastomotic vein connecting the '+L('superficial_middle_cerebral','superficial middle cerebral vein')+' with the '+link('superior_sagittal','superior sagittal sinus')+'. Trolard and Labbé are in haemodynamic balance such that either may be absent.',side=side,parent=ref('superficial_middle_cerebral',side),fit='cortical',aliases=['Trolard'],page=69)
 add('labbe','Posterior anastomotic vein of Labbé','superficial',[a('superficial_middle_cerebral',.15)]+pts((65,-79,98),(62,-94,86),(58,-112,77))+[a('transverse',.76)], [1.4,1.7],
  'The posterior anastomotic vein of Labbé is the largest anastomotic vein connecting the '+L('superficial_middle_cerebral','superficial middle cerebral vein')+' with the '+L('transverse','transverse sinus')+'. Trolard and Labbé are in haemodynamic balance such that either may be absent.',side=side,parent=ref('superficial_middle_cerebral',side),fit='cortical',aliases=['Labbe','Labbé','Inferior anastomotic vein'],page=69)
 for key,label,points,station in [
  ('frontal_cortical','Frontal cortical vein',pts((47,-3,114),(40,-2,130),(26,-13,147),(11,-27,156)),.28),
  ('parietal_cortical','Parietal cortical vein',pts((59,-118,113),(48,-132,129),(30,-137,140),(13,-133,144)),.7)]:
  add(key,label,'superficial',points+[attach('superior_sagittal',station)],[.65,1.2],
   'Cortical veins drain regions of the cerebral cortex into nearby sinuses. The peripheral medial surfaces drain to the '+link('superior_sagittal','superior sagittal sinus')+'. Bridging veins cross the subdural space and may fuse with meningeal veins before entering a major sinus.',side=side,fit='cortical',page=69)
 # Deep venous complex below the callosal arc and above/around the midbrain.
 add('internal_cerebral','Internal cerebral vein','deep',pts((3,-39,105),(3,-54,106),(4,-72,105),(7,-83,101))+[attach('galen',0)], [1.35,1.7],
  'The paired internal cerebral veins form at the foramen of Monro from the junction of the superior choroidal and superior thalamostriate veins and drain the subependymal and choroid venous systems. They extend posteriorly along the roof of the third ventricle and the velum interpositum. Initially running parallel to the midline, they diverge laterally near the pineal recess, tracing the pineal body. They then join with the basal vein and converge under the splenium to form the '+link('galen','vein of Galen')+'.',side=side,parent=ref('galen'),aliases=['ICV'],page=72)
 add('basal','Basal vein of Rosenthal','deep',pts((15,-39,80),(22,-51,78),(27,-69,82),(26,-83,87),(18,-91,92))+[attach('galen',.12)], [1.2,1.65],
  'The basal vein of Rosenthal originates under the anterior perforated substance in the chiasmatic cistern medial to the uncus of the temporal lobe, runs posteriorly, and terminates in either the '+link('galen','vein of Galen')+' or '+L('internal_cerebral','internal cerebral vein')+'. It is formed by the confluence of the '+L('anterior_cerebral','anterior cerebral vein')+' and '+L('deep_middle_cerebral','deep middle cerebral vein')+'. Its second segment encircles the cerebral peduncle, and its third segment is located behind the midbrain. It connects to the superior petrosal sinus via the '+L('lateral_mesencephalic','lateral mesencephalic vein')+'.',side=side,parent=ref('galen'),aliases=['BVR','Basal vein'],page=71)
 add('thalamostriate','Superior thalamostriate vein','deep',pts((14,-79,107),(16,-65,109),(13,-51,108),(8,-42,106))+[a('internal_cerebral',0)], [1,1.2],
  'The thalamostriate vein primarily drains the lateral subependymal, posterior frontal, and anterior parietal veins, as well as the caudate nucleus and internal capsule. It receives minimal drainage from the thalamus itself, but does receive the superior choroidal vein. It runs along the thalamocaudate groove towards the '+L('internal_cerebral','internal cerebral vein')+'.',side=side,parent=ref('internal_cerebral',side),page=71)
 add('anterior_septal','Anterior septal vein','deep',pts((3,-14,106),(4,-22,109),(4,-31,108))+[a('internal_cerebral',0)], [.65,.95],
  'The anterior septal vein starts in the frontal horn of the lateral ventricle, formed from the deep medullary veins of the anterior frontal lobe. It runs posteriorly to join the '+L('thalamostriate','thalamostriate vein')+' at the venous angle near the foramen of Monro. It may instead join the internal cerebral vein more posteriorly.',side=side,parent=ref('internal_cerebral',side),page=70)
 add('superior_choroidal','Superior choroidal vein','deep',pts((8,-83,109),(9,-68,111),(9,-52,110))+[a('thalamostriate',.96)],.65,
  'The superior choroidal vein joins the superior thalamostriate vein near the foramen of Monro to form the '+L('internal_cerebral','internal cerebral vein')+'. The internal cerebral veins drain the subependymal and choroid venous systems.',side=side,parent=ref('internal_cerebral',side),page=72)
 add('anterior_cerebral','Anterior cerebral vein','deep',pts((3,-14,92),(4,-24,84),(8,-33,79))+[a('basal',0)],.8,
  'The anterior cerebral vein receives olfactory, posterior orbitofrontal, and anterior pericallosal veins. It joins the '+L('deep_middle_cerebral','deep middle cerebral vein')+' to form the '+L('basal','basal vein of Rosenthal')+'.',side=side,parent=ref('basal',side),page=71)
 add('deep_middle_cerebral','Deep middle cerebral vein','deep',pts((40,-62,95),(38,-48,88),(29,-41,82))+[a('basal',0)],.95,
  'The deep middle cerebral vein is formed from insular and inferior striate veins. It joins the '+L('anterior_cerebral','anterior cerebral vein')+' to form the '+L('basal','basal vein of Rosenthal')+'.',side=side,parent=ref('basal',side),page=72)
 # Posterior fossa collector and selected major tributaries.
 add('superior_petrosal_vein','Superior petrosal vein','posterior',pts((24,-84,58),(28,-80,61),(32,-74,64))+[a('superior_petrosal',.55)], [1.2,1.65],
  'The superior petrosal vein, or petrosal vein, is the largest vein in the posterior cranial fossa. It drains the anterior cerebellum and brainstem into the '+L('superior_petrosal','superior petrosal sinus')+'. It is usually formed by multiple smaller veins converging into one, but sometimes there are two or three. Major contributors include the vein of the cerebellopontine fissure, and the petrosal, posterior mesencephalic, anterior pontomesencephalic, and tentorial groups.',side=side,aliases=['Petrosal vein','Vein of Dandy'],page=76)
 add('lateral_mesencephalic','Lateral mesencephalic vein','posterior',[a('basal',.65)]+pts((24,-85,77),(23,-86,67))+[a('superior_petrosal_vein',.12)],.85,
  'The lateral mesencephalic veins connect the '+L('basal','basal vein of Rosenthal')+' to lateral brainstem and medullary fissure veins. They act as a crucial collateral drainage route, especially when the basal vein is discontinuous, draining posteriorly to infratentorial veins.',side=side,parent=ref('superior_petrosal_vein',side),page=74)
 add('cerebellopontine_fissure','Vein of the cerebellopontine fissure','posterior',pts((22,-95,44),(29,-94,49),(30,-89,54))+[a('superior_petrosal_vein',0)],1,
  'Anterior hemispheric veins draining the petrosal surface converge near the flocculus to form the vein of the cerebellopontine fissure, which drains into the '+L('superior_petrosal','superior petrosal sinus')+' through the '+L('superior_petrosal_vein','superior petrosal vein')+'.',side=side,parent=ref('superior_petrosal_vein',side),page=76)
 add('inferior_vermian','Inferior vermian vein','posterior',pts((5,-115,43),(7,-126,47),(8,-137,55))+[attach('confluence',.45)], [0.8,1.1],
  'The paired inferior vermian veins lie in the cerebellovermian fissure and drain the inferior vermis and medial suboccipital surface into the '+link('confluence','torcular')+' or transverse sinus, directly or via a tentorial sinus.',side=side,page=76)
 add('inferior_hemispheric','Inferior hemispheric vein','posterior',pts((41,-112,43),(33,-127,43),(19,-134,48))+[a('inferior_vermian',.56)], [.6,.85],
  'Inferior hemispheric veins can run longitudinally or transversely. Longitudinal veins join superior hemispheric veins and drain into a dural or tentorial sinus, while transverse veins are associated with cerebellar fissures and drain into the '+L('inferior_vermian','inferior vermian vein')+'.',side=side,parent=ref('inferior_vermian',side),page=76)
 # Face and neck. The lower neck is deliberately truncated with the arteries.
 add('external_jugular','External jugular vein','extracranial',pts((46,-57,-7),(46,-63,-26),(44,-64,-51),(42,-55,-78),(40,-42,-107)),[2.2,2.7],
  'The EJV drains the deep face, scalp, and posterolateral neck. It originates from the convergence of the retromandibular, posterior auricular, and superficial temporal veins in front of the angle of the mandible. The vein runs caudally on top of the sternocleidomastoid to join the subclavian vein. Like the IJV, it has a valve just prior to its termination.',side=side,aliases=['EJV'],page=62)
 add('retromandibular','Retromandibular vein','extracranial',pts((46,-40,32),(49,-42,18),(48,-46,3))+[a('external_jugular',0)], [1.8,2.2],
  'The maxillary vein converges with the '+L('superficial_temporal','superficial temporal vein')+' to form the retromandibular vein. It contributes to drainage of the deep face and scalp into the '+L('external_jugular','external jugular vein')+'.',side=side,parent=ref('external_jugular',side),page=62)
 add('maxillary','Maxillary vein','extracranial',pts((30,-33,35),(38,-34,32))+[a('retromandibular',0)],1.65,
  'The '+L('pterygoid_plexus','pterygoid plexus')+' becomes the maxillary vein, which later converges with the '+L('superficial_temporal','superficial temporal vein')+' to form the '+L('retromandibular','retromandibular vein')+'.',side=side,parent=ref('retromandibular',side),page=62)
 add('pterygoid_plexus','Pterygoid venous plexus','extracranial',pts((24,-27,43),(28,-34,42),(30,-38,38))+[a('maxillary',0)],1.15,
  'The pterygoid plexus is a large venous network located between the temporalis and lateral pterygoid muscles. It drains into the '+L('maxillary','maxillary vein')+' and connects with the '+L('cavernous','cavernous sinus')+' via emissary veins. The plexus receives numerous tributaries, including the sphenopalatine, middle meningeal, deep temporal, pterygoid, masseteric, buccinator, alveolar, and palatine veins. It also receives blood from the '+L('inferior_ophthalmic','inferior ophthalmic vein')+', '+L('deep_facial','deep facial vein')+', and infraorbital vein.',side=side,parent=ref('maxillary',side),page=62)
 add('superficial_temporal','Superficial temporal vein','extracranial',pts((65,-39,121),(69,-32,103),(65,-27,82),(61,-27,59),(54,-31,43))+[a('retromandibular',0)], [1.1,1.65],
  'The superficial temporal vein drains the scalp and converges with the '+L('maxillary','maxillary vein')+' to form the '+L('retromandibular','retromandibular vein')+'.',side=side,parent=ref('retromandibular',side),page=62)
 add('posterior_auricular','Posterior auricular vein','extracranial',pts((67,-74,70),(67,-73,48),(59,-68,24))+[a('external_jugular',0)], [1,1.5],
  'The posterior auricular vein contributes to drainage of the scalp and posterolateral neck into the '+L('external_jugular','external jugular vein')+'.',side=side,parent=ref('external_jugular',side),page=62)
 add('facial','Facial vein','extracranial',pts((15,25,55),(21,29,41),(28,21,23),(35,3,3),(34,-20,-16),(31,-44,-23))+[a('internal_jugular',.4)], [1.3,2.2],
  'The extracranial drainage of the head and neck mirrors the arteries. The supratrochlear and supraorbital veins drain to the facial vein, which is a tributary of the '+L('internal_jugular','internal jugular vein')+'. The '+L('deep_facial','deep facial vein')+' connects with the pterygoid plexus.',side=side,parent=ref('internal_jugular',side),page=62)
 add('angular','Angular vein','extracranial',pts((10,21,75),(12,26,67))+[a('facial',0)],1.05,'',side=side,parent=ref('facial',side),page=62)
 add('deep_facial','Deep facial vein','extracranial',[a('facial',.24)]+pts((34,9,23),(37,-8,28),(33,-22,35))+[a('pterygoid_plexus',.65)],1,
  'The deep facial vein connects the '+L('facial','facial vein')+' with the '+L('pterygoid_plexus','pterygoid venous plexus')+'.',side=side,parent=ref('facial',side),page=62)
 add('superior_ophthalmic','Superior ophthalmic vein','skullbase',[a('angular',.35)]+pts((15,14,70),(25,2,72),(27,-12,72),(23,-23,70),(20,-33,66))+[a('cavernous',.9)], [1.1,1.65],
  'The ophthalmic veins connect superiorly and anteriorly with the '+L('cavernous','cavernous sinus')+', an important bidirectional confluence of the intracranial and extracranial venous systems.',side=side,aliases=['SOV'],page=68)
 add('inferior_ophthalmic','Inferior ophthalmic vein','skullbase',pts((18,12,48),(28,0,47),(30,-10,45),(26,-22,42))+[a('pterygoid_plexus',0)], [.8,1],
  'The inferior ophthalmic vein contributes to drainage into the '+L('pterygoid_plexus','pterygoid venous plexus')+'. The ophthalmic veins also connect with the '+L('cavernous','cavernous sinus')+'.',side=side,aliases=['IOV'],page=62)
 add('ovale_emissary','Emissary vein of foramen ovale','skullbase',[a('cavernous',.2)]+pts((21,-46,54),(24,-46,51),(24,-46,48),(28,-40,43))+[a('pterygoid_plexus',.55)],.8,
  'Emissary veins are inconstant channels and serve as two-way connections linking extracranial veins, diploic veins, and intracranial meningeal veins and sinuses. Emissary veins passing through the skull foramina include those of the foramen ovale. The '+L('pterygoid_plexus','pterygoid plexus')+' connects with the '+L('cavernous','cavernous sinus')+' via emissary veins.',side=side,page=69)
 add('vertebral','Vertebral vein','extracranial',pts((22,-86,1),(23,-87,-24),(23,-87,-51),(24,-85,-79),(27,-75,-96),(29,-58,-107)), [1.5,2.1],
  'The vertebral artery venous plexus arises at C2 and receives blood from the '+L('suboccipital_plexus','suboccipital plexus')+' and the anterior, lateral, and posterior condylar veins. It continues as a solitary vertebral vein in the vertebral canal surrounding the vertebral artery, leaving at C6 via the foramen transversarium to join the brachiocephalic vein.',side=side,page=63)
 add('suboccipital_plexus','Suboccipital venous plexus','extracranial',pts((24,-110,16),(29,-108,10),(29,-98,5))+[a('vertebral',0)],1.15,
  'The suboccipital venous plexus contributes to the vertebral venous system through the '+L('vertebral','vertebral artery venous plexus')+' and '+L('deep_cervical','deep cervical vein')+'. It also communicates with condylar veins.',side=side,parent=ref('vertebral',side),page=63)
 add('deep_cervical','Deep cervical vein','extracranial',[a('suboccipital_plexus',.25)]+pts((29,-112,-9),(27,-108,-43),(29,-93,-78),(30,-71,-103)),1.5,
  'The deep cervical vein receives tributaries of the '+L('suboccipital_plexus','suboccipital venous plexus')+'. It follows the deep cervical artery to end in the IJV or brachiocephalic vein.',side=side,page=63)
 add('anterior_condylar','Anterior condylar vein','skullbase',pts((11,-75,34),(17,-71,31),(21,-69,29))+[a('internal_jugular',.07)],1,
  'The anterior condylar vein, or vein of the hypoglossal canal, connects the '+link('marginal','marginal sinus')+' and adjacent skull-base venous network to the '+L('internal_jugular','internal jugular vein')+' at the bulb. The anterior condylar confluence is formed by the anterior and lateral condylar veins and tributaries of the clival plexus.',side=side,aliases=['Vein of hypoglossal canal'],page=67)
 add('lateral_condylar','Lateral condylar vein','skullbase',[a('anterior_condylar',.65)]+pts((26,-77,26),(29,-91,19))+[a('suboccipital_plexus',.58)],.9,
  'The lateral condylar vein connects the jugular and anterior condylar region with the '+L('suboccipital_plexus','suboccipital plexus')+' and vertebral venous system.',side=side,parent=ref('anterior_condylar',side),page=67)
 # Relationships describe the represented flow pattern, independently of tree grouping.
 for src,dst in [('sigmoid','internal_jugular'),('transverse','sigmoid'),('superior_petrosal','sigmoid'),('inferior_petrosal','internal_jugular'),('sphenoparietal','cavernous'),('superficial_middle_cerebral','sphenoparietal'),('labbe','transverse'),('thalamostriate','internal_cerebral'),('anterior_septal','internal_cerebral'),('superior_choroidal','thalamostriate'),('anterior_cerebral','basal'),('deep_middle_cerebral','basal'),('superior_petrosal_vein','superior_petrosal'),('cerebellopontine_fissure','superior_petrosal_vein'),('inferior_hemispheric','inferior_vermian'),('retromandibular','external_jugular'),('maxillary','retromandibular'),('pterygoid_plexus','maxillary'),('superficial_temporal','retromandibular'),('posterior_auricular','external_jugular'),('angular','facial'),('facial','internal_jugular'),('superior_ophthalmic','cavernous'),('inferior_ophthalmic','pterygoid_plexus'),('suboccipital_plexus','vertebral')]:rel(ref(src,side),ref(dst,side))
 for src,dst in [('superficial_middle_cerebral','trolard'),('superficial_middle_cerebral','labbe'),('cavernous','superior_petrosal'),('cavernous','inferior_petrosal'),('deep_facial','facial'),('deep_facial','pterygoid_plexus'),('ovale_emissary','cavernous'),('ovale_emissary','pterygoid_plexus'),('superior_ophthalmic','angular'),('lateral_mesencephalic','basal'),('lateral_mesencephalic','superior_petrosal_vein'),('anterior_condylar','internal_jugular'),('lateral_condylar','anterior_condylar'),('lateral_condylar','suboccipital_plexus'),('suboccipital_plexus','deep_cervical')]:rel(ref(src,side),ref(dst,side),'communicates_with')
 for src,dst in [('internal_cerebral','galen'),('basal','galen'),('trolard','superior_sagittal'),('frontal_cortical','superior_sagittal'),('parietal_cortical','superior_sagittal'),('inferior_vermian','confluence')]:rel(ref(src,side),ref(dst))
 rel(ref('confluence'),ref('transverse',side))
 rel(ref('anterior_condylar',side),ref('marginal'),'communicates_with')

# Midline communicating channels and posterior-fossa veins.
add('anterior_intercavernous','Anterior intercavernous sinus','dural',[attach('cavernous',.92,'right'),[6,-32,67],[.65,-31,67],[-5,-32,67],attach('cavernous',.92,'left')],1.1,
 'The cavernous sinuses connect medially to the contralateral side through the intercavernous sinuses.',page=68)
add('posterior_intercavernous','Posterior intercavernous sinus','dural',[attach('cavernous',.3,'right'),[6,-49,64],[.65,-50,64],[-5,-49,64],attach('cavernous',.3,'left')],.95,
 'The cavernous sinuses connect medially to the contralateral side through the intercavernous sinuses.',page=68)
add('basilar_plexus','Basilar venous plexus','skullbase',[[.65,-50,61],[.65,-57,51],[.65,-64,41],attach('marginal',.5)],1,
 'The basilar or clival plexus connects with the cavernous sinuses posteriorly and with the '+link('marginal','marginal sinus')+' and anterior condylar venous network below.',aliases=['Clival plexus','Basilar plexus'],page=67)
add('anterior_communicating','Anterior communicating vein','deep',[attach('anterior_cerebral',.72,'right'),[.65,-31,80],attach('anterior_cerebral',.72,'left')],.65,
 'The anterior cerebral veins are connected by the anterior communicating vein in half the population. This contributes to the anterior venous circle in the suprasellar cistern.',page=72)
add('posterior_communicating','Posterior communicating vein','deep',[attach('basal',.3,'right'),[12,-60,78],[.65,-62,78],[-10.7,-60,78],attach('basal',.3,'left')],.75,
 'The posterior communicating vein is a constant vessel in the interpeduncular fossa. This, in addition to hypothalamic and ventral mesencephalic veins, contributes to the posterior aspect of the venous circle.',page=72)
add('precentral_cerebellar','Precentral cerebellar vein','posterior',[[.65,-100,72],[.65,-97,79],[.65,-95,87],attach('galen',.25)],1.1,
 'The precentral cerebellar vein, an unpaired vein, ascends in the quadrigeminal cistern behind the tectal plate to drain into the '+link('galen','vein of Galen')+'. It can merge with the '+link('superior_vermian','superior vermian vein')+' to form the superior cerebellar vein or drain directly into the vein of Galen independently.',page=74)
add('superior_vermian','Superior vermian vein','posterior',[[.65,-136,77],[.65,-123,84],[.65,-110,86],attach('precentral_cerebellar',.78)],1,
 'The superior vermian veins drain the superior vermis and the medial parts of the superior cerebellar hemispheres. The anterior veins drain into the '+link('galen','vein of Galen')+', and the posterior veins drain into the '+link('confluence','confluence of sinuses')+'.',parent=ref('precentral_cerebellar'),page=76)
add('anterior_pontomesencephalic','Median anterior pontomesencephalic vein','posterior',[[2.8,-66,67],[2.5,-61,71],attach('posterior_communicating',.5)],.75,
 'The midline brainstem veins form a continuous anastomotic venous channel comprising the median anterior pontomesencephalic, median anterior pontine, and median anterior medullary veins. Blood may flow cranially to the posterior communicating vein or peduncular veins, or caudally into the spinal veins.',page=74)
add('anterior_pontine','Median anterior pontine vein','posterior',[[3,-81,45],[3,-76,52],[3,-71,59],attach('anterior_pontomesencephalic',0)],.8,
 'The median anterior pontine vein forms part of the continuous midline anastomotic channel between the '+link('anterior_pontomesencephalic','median anterior pontomesencephalic vein')+' and '+link('anterior_medullary','median anterior medullary vein')+'.',parent=ref('anterior_pontomesencephalic'),page=74)
add('anterior_medullary','Median anterior medullary vein','posterior',[[2.8,-90,27],[3,-87,35],attach('anterior_pontine',0)],.65,
 'The median anterior medullary vein continues inferiorly as the '+link('anterior_spinal','anterior spinal vein')+'. It forms part of the continuous midline venous channel on the anterior brainstem.',parent=ref('anterior_pontine'),page=74)
add('anterior_spinal','Anterior spinal vein','posterior',[[2.8,-89,-24],[2.8,-89,0],attach('anterior_medullary',0)],.65,
 'The anterior spinal vein is the inferior continuation of the '+link('anterior_medullary','median anterior medullary vein')+'. Blood may flow cranially through the brainstem venous channel or caudally into the spinal veins.',parent=ref('anterior_medullary'),page=74)
for side,sg in [('right',1),('left',-1)]:
 def p(x,y,z):return [x if sg==1 else 1.3-x,y,z]
 for key,name,points,src in [
  ('transverse_pontine','Transverse pontine vein',[attach('anterior_pontine',.55),p(11,-72,56),p(19,-77,57),attach('superior_petrosal_vein',0,side)],'anterior_pontine'),
  ('pontomedullary','Vein of the pontomedullary sulcus',[attach('anterior_medullary',.8),p(12,-83,41),p(22,-91,43),attach('cerebellopontine_fissure',0,side)],'anterior_medullary')]:
  add(key,name,'posterior',points,.7,'',side=side,parent=ref('superior_petrosal_vein',side),page=74)
  rel(ref(key,side),ref(src),'communicates_with');rel(ref(key,side),ref('superior_petrosal_vein',side),'communicates_with')
 for key in ['anterior_intercavernous','posterior_intercavernous']:rel(ref(key),ref('cavernous',side),'communicates_with')
 rel(ref('anterior_communicating'),ref('anterior_cerebral',side),'communicates_with')
 rel(ref('posterior_communicating'),ref('basal',side),'communicates_with')
 rel(ref('basilar_plexus'),ref('cavernous',side),'communicates_with')
for src,dst in [('superior_sagittal','confluence'),('straight','confluence'),('occipital_sinus','confluence'),('inferior_sagittal','straight'),('galen','straight'),('precentral_cerebellar','galen'),('superior_vermian','precentral_cerebellar')]:rel(ref(src),ref(dst))
for src,dst in [('occipital_sinus','marginal'),('basilar_plexus','marginal'),('anterior_pontomesencephalic','posterior_communicating'),('anterior_pontine','anterior_pontomesencephalic'),('anterior_medullary','anterior_pontine'),('anterior_spinal','anterior_medullary')]:rel(ref(src),ref(dst),'communicates_with')

# Additional loops remain part of their named plexus, not invented named veins.
for side,sg in [('right',1),('left',-1)]:
 def p(x,y,z):return [x if sg==1 else 1.3-x,y,z]
 lookup={s['id']:s for s in rows}
 lookup[ref('pterygoid_plexus',side)]['additionalPaths']=[
  [attach('pterygoid_plexus',.08,side),p(32,-24,44),p(38,-29,39),attach('pterygoid_plexus',.95,side)],
  [attach('pterygoid_plexus',.3,side),p(24,-36,35),p(28,-39,32),attach('pterygoid_plexus',.96,side)]]
 lookup[ref('suboccipital_plexus',side)]['additionalPaths']=[
  [attach('suboccipital_plexus',.03,side),p(18,-113,12),p(17,-101,6),attach('suboccipital_plexus',.98,side)],
  [attach('suboccipital_plexus',.25,side),p(32,-116,7),p(33,-103,2),attach('suboccipital_plexus',.9,side)]]
lookup={s['id']:s for s in rows}
lookup[ref('basilar_plexus')]['additionalPaths']=[
 [attach('cavernous',.12,'right'),[7,-57,51],[8,-65,40],attach('anterior_condylar',0,'right')],
 [attach('cavernous',.12,'left'),[-5.7,-57,51],[-6.7,-65,40],attach('anterior_condylar',0,'left')],
 [[7,-57,51],[.65,-57,51],[-5.7,-57,51]],[[8,-65,40],[.65,-64,41],[-6.7,-65,40]]]

# Local course amendments after review of the actual registered bone surfaces.
for side,sg in [('right',1),('left',-1)]:
 def p(x,y,z):return [x if sg==1 else 1.3-x,y,z if sg==1 else z-.05]
 lookup[ref('internal_jugular',side)]['points']=[p(27,-65,38),p(31,-69,27),p(38,-69,12),p(41,-67,-10),p(42,-63,-35),p(42,-58,-70),p(34,-46,-107)]
 lookup[ref('internal_jugular',side)]['radius']=[2.4,4.2 if sg==1 else 3.7,4.8 if sg==1 else 4.2]
 lookup[ref('external_jugular',side)]['points']=[p(46,-57,-7),p(52,-63,-26),p(52,-64,-51),p(50,-55,-78),p(45,-42,-107)]
 lookup[ref('facial',side)]['points']=[p(15,25,55),p(23,30,41),p(31,22,22),p(40,9,5),p(43,-9,-12),p(43,-23,-26),p(36,-36,-37),attach('internal_jugular',.55,side)]
 lookup[ref('deep_facial',side)]['points']=[attach('facial',.24,side),p(38,7,20),p(38,0,21),p(38,-9,26),p(35,-20,31),attach('pterygoid_plexus',.65,side)]
 lookup[ref('inferior_petrosal',side)]['points']=[attach('cavernous',.1,side),p(13,-57,57),p(13,-65,51),p(18,-72,44),p(25,-71,35),attach('internal_jugular',.065,side)]
 lookup[ref('superior_ophthalmic',side)]['points']=[attach('angular',.35,side),p(15,14,70),p(25,2,72),p(27,-12,72),p(23,-20,70),p(19.8,-24,70.2),p(22.5,-28,70),p(20,-32,67),attach('cavernous',.9,side)]
 lookup[ref('superior_ophthalmic',side)]['radius']=[1.0,1.1]
 lookup[ref('sphenoparietal',side)]['points']=[p(48,-24,85),p(40,-27,85),p(29,-28,79),p(22,-32,72),attach('cavernous',.9,side)]
 lookup[ref('basal',side)]['points']=[p(20,-43,81),p(25,-53,79),p(27,-69,82),p(26,-83,87),p(18,-91,92),attach('galen',.12)]
 lookup[ref('anterior_cerebral',side)]['points']=[p(3,-14,92),p(7,-23,80),p(11,-34,78),attach('basal',0,side)]
 lookup[ref('posterior_auricular',side)]['points']=[p(70,-74,70),p(69,-73,48),p(60,-68,24),attach('external_jugular',0,side)]
 lookup[ref('pterygoid_plexus',side)]['additionalPaths'][1]=[attach('pterygoid_plexus',.3,side),p(29,-37,34),p(34,-39,33),attach('pterygoid_plexus',.96,side)]
 lookup[ref('superficial_middle_cerebral',side)]['fit']='cortical'
 # The lateral condylar route stays outside the occipital condyle.
 lookup[ref('lateral_condylar',side)]['points']=[attach('anterior_condylar',.82,side),p(29,-73,24),p(32,-87,17),attach('suboccipital_plexus',.58,side)]
lookup[ref('posterior_intercavernous')]['points']=[attach('cavernous',.4,'right'),[6,-43,67],[.65,-43,67],[-5,-43,67],attach('cavernous',.4,'left')]
lookup[ref('superior_vermian')]['points']=[[.65,-133,66],[.65,-123,76],[.65,-110,80],attach('precentral_cerebellar',.78)]
orbital=OUT/'orbital-corridors.json'
if orbital.exists():
 for side,corridor in json.loads(orbital.read_text()).items():
  sg=1 if side=='right' else -1
  def p(x,y,z):return [x if sg==1 else 1.3-x,y,z]
  lookup[ref('superior_ophthalmic',side)]['points']=[attach('angular',.35,side),p(15,14,70),p(25,2,72),p(27,-12,72)]+corridor+[attach('cavernous',.9,side)]
  lookup[ref('superior_ophthalmic',side)]['radius']=.85

document={'release':'0.9.0','coordinates':'RAS mm','groups':{'dural':'Dural venous sinuses','superficial':'Superficial cerebral veins','deep':'Deep cerebral veins','posterior':'Posterior fossa and spinal veins','extracranial':'Extracranial veins','skullbase':'Skull-base venous connections'},'structures':rows,'relationships':relations}
(OUT/'courses.json').write_text(json.dumps(document,ensure_ascii=False,indent=2)+'\n')
print(f'Authored {len(rows)} venous structures and {len(relations)} relationships')
