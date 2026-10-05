"""Authoring only: register the named source surfaces and derive semantic anchors.
Normal npm builds consume the committed GLB and manifest, without Python geometry dependencies.
"""
from pathlib import Path
import json,re,hashlib
import numpy as np
import trimesh,vtk
from vtk.util.numpy_support import numpy_to_vtk,numpy_to_vtkIdTypeArray
APP=Path(__file__).resolve().parents[2];SRC=APP/'anatomy/source/brain';PUB=APP/'public/anatomy'
def dump(p,v):p.write_text(json.dumps(v,indent=2,ensure_ascii=False)+'\n')
def slug(s):return re.sub('[^a-z0-9]+','-',s.lower()).strip('-')
def sid(n):return 'brain.'+slug(n[:-2] if n.endswith(('.l','.r')) else n)+('.left' if n.endswith('.l') else '.right' if n.endswith('.r') else '')
source=json.loads((SRC/'source-manifest.json').read_text());reg=json.loads((SRC/'registration.json').read_text());T=np.array(reg['matrix']);scene=trimesh.load(SRC/'source-orientation.glb',force='scene');out=trimesh.Scene();rows=[];relations=[];byid={};meshes={};locators={}
ref='source.z-anatomy-brain';registration_id='z-anatomy-skull-v0.9.14'
def add(id,name,parent,side='midline',**kw):
 row=dict(id=id,name=name,parent=parent,children=[],system='brain',side=side,kind='group',aliases=[],geometryStatus='planned',provenance=dict(sourceType='atlas-derived',confidence='Skull-registered atlas context; not patient-specific',reviewStatus='unreviewed',sourceRefs=[ref]))
 row.update(kw);rows.append(row);byid[id]=row;return row
def group(id,name,parent,side='midline',**kw):return add('brain'+('.'+id if id else ''),name,'brain'+('.'+parent if parent else '') if parent is not None else None,side,**kw)
group('','Brain and dura',None,aliases=['brain','encephalon','orientation'])
for id,name in [('cerebrum','Cerebral hemispheres'),('brainstem','Brainstem'),('cerebellum','Cerebellum'),('deep','Deep structures'),('ventricles','Ventricles'),('dura','Falx and tentorium'),('landmarks','Vessel course landmarks')]:group(id,name,'')
for side in ['left','right']:
 group('cerebrum.'+side,'Cerebral hemisphere, '+side,'cerebrum',side)
 group('cerebellum.'+side,'Cerebellar hemisphere, '+side,'cerebellum',side)
group('cerebellum.vermis','Cerebellar vermis','cerebellum',aliases=['vermis'])
for id,name in [('midbrain','Midbrain'),('pons','Pons'),('medulla','Medulla oblongata')]:group('brainstem.'+id,name,'brainstem')
colours={'cerebral_cortex':'#c8b9a5','cerebellum':'#92abc7','brainstem':'#d4a778','dural_reflections':'#aaa0c2','ventricles':'#60b8bd','deep_landmarks':'#c49aa9'}
for record in source['records']:
 n=record['name'];cat=record['category'];side='left' if n.endswith('.l') else 'right' if n.endswith('.r') else 'midline';base=n[:-2] if side!='midline' else n;name=base.replace('*','').replace('  ',' ')
 name=name.replace('Lat_Fis-ant-Vertical','Lateral fissure, anterior ascending ramus').replace('Lat_Fis-ant-Horizont','Lateral fissure, anterior horizontal ramus').replace('Lat_Fis-post','Lateral fissure, posterior ramus')
 if base=='Base of peduncle':name='Cerebral peduncle (crus cerebri)'
 if side!='midline':name+=', '+side
 if cat=='cerebral_cortex':
  lobe=next((a[:-2] for a in record['source_ancestors'] if a.endswith('lobe.g') or a=='Insula.g'),'Cortical regions');pid='brain.cerebrum.'+side+'.'+slug(lobe)
  if pid not in byid:add(pid,lobe+', '+side,'brain.cerebrum.'+side,side)
 elif cat=='cerebellum':pid='brain.cerebellum.'+(side if side!='midline' else 'vermis')
 elif cat=='brainstem':pid='brain.brainstem.'+('pons' if base=='Pons' else 'medulla' if base=='Medulla oblongata' else 'midbrain')
 else:pid='brain.'+{'dural_reflections':'dura','ventricles':'ventricles','deep_landmarks':'deep'}[cat]
 id=sid(n);m=scene.geometry[n].copy();m.apply_transform(T);m.vertices=np.asarray(m.vertices,dtype=np.float32).astype(float);meshes[n]=m
 # Export smooth normals, preserving all original triangles and labelled boundaries.
 _=m.vertex_normals;out.add_geometry(m,node_name=id,geom_name=id)
 aliases=[n,base];aliases += {'Central sulcus':['Rolandic sulcus','sulcus of Rolando','central fissure'],'Lat_Fis-post':['Sylvian fissure','lateral sulcus','posterior Sylvian fissure'],'Parieto-occipital sulcus':['parietooccipital sulcus'],'Circular sulcus of insula':['peri-insular sulcus'],'Optic chiasm':['chiasma opticum'],'Globus pallidus':['pallidum'],'Base of peduncle':['crus cerebri','basis pedunculi'],'Aqueduct of midbrain':['Cerebral aqueduct','Aqueduct of Sylvius'],'Tonsil of cerebellum':['cerebellar tonsil'],'Falx cerebri':['falx'],'Tentorium cerebelli':['tentorium'],'Pons':['pons'],'Medulla oblongata':['medulla'],'Superior cerebellar peduncle':['brachium conjunctivum','SCP'],'Hippocampus':['hippocampal formation']}.get(base,[])
 desc={'dural_reflections':'Dural reflection retained with the brain in the source atlas. Its surface provides regional context for adjacent venous sinuses; sinus lumina are separate structures.','ventricles':'Atlas surface representing the ventricular space. Use as an orientation boundary, not as a vascular lumen.','cerebellum':'Named cerebellar surface from the source atlas. Lobular contours are simplified and provide regional orientation for venous courses.','brainstem':'Named brainstem surface from the source atlas. Its exposed contour provides orientation for surface veins.','deep_landmarks':'Named deep anatomical structure retained in the shared brain registration.','cerebral_cortex':'Labelled cortical parcel from the source atlas; parcel boundaries and sulcal surfaces are atlas approximations.'}[cat]
 role='sulcal-reference' if 'sulcus' in base.lower() or base.startswith('Lat_Fis') else 'csf-boundary' if cat=='ventricles' else 'dural-surface' if cat=='dural_reflections' else 'parenchymal-surface'
 if role=='sulcal-reference':desc='Named sulcal reference surface from the atlas, showing the position of the groove or fissure. It is a course landmark rather than a solid tissue boundary.'
 add(id,name,pid,side,kind='structure',aliases=list(dict.fromkeys(aliases)),geometryStatus='web-optimised',asset={'file':'models/brain-context.glb','node':id},color=colours[cat],description=desc,anatomy={'category':cat,'sourceLabel':n,'registrationId':registration_id,'bounds':m.bounds.tolist(),'centroid':m.centroid.tolist(),'surfaceRole':role})
 pd=vtk.vtkPolyData();pts=vtk.vtkPoints();pts.SetData(numpy_to_vtk(np.array(m.vertices),deep=True));pd.SetPoints(pts);cells=vtk.vtkCellArray();cells.SetCells(len(m.faces),numpy_to_vtkIdTypeArray(np.c_[np.full(len(m.faces),3),m.faces].astype(np.int64).ravel(),deep=True));pd.SetPolys(cells);loc=vtk.vtkStaticCellLocator();loc.SetDataSet(pd);loc.BuildLocator();locators[n]=loc
(PUB/'models/brain-context.glb').write_bytes(out.export(file_type='glb'))
asset_hash=hashlib.sha256((PUB/'models/brain-context.glb').read_bytes()).hexdigest()
# All guide seeds use the documented source-orientation coordinates (LAS axes reordered:
# source +X left, +Y superior, +Z anterior, mm). Projection is to an explicitly named mesh.
anchors=[]
def anchor(key,label,part,seed,side='midline',vessels=(),aliases=(),description=''):
 query=np.array(seed)@T[:3,:3].T+T[:3,3];closest=[0.,0.,0.];cell=vtk.reference(0);sub=vtk.reference(0);dist=vtk.reference(0.);locators[part].FindClosestPoint(query,closest,cell,sub,dist)
 mesh=meshes[part];triangle=int(cell);bary=trimesh.triangles.points_to_barycentric(mesh.vertices[mesh.faces[[triangle]]],np.array([closest]))[0];point=bary@mesh.vertices[mesh.faces[triangle]]
 id='brain.landmark.'+key;bind={'structureId':sid(part),'triangleIndex':triangle,'barycentric':bary.tolist(),'position':point.tolist(),'assetSha256':asset_hash,'registrationId':registration_id}
 row=add(id,label,'brain.landmarks',side,kind='structure',aliases=list(aliases),geometryStatus='placeholder',description=description or 'Regional course guide on the labelled atlas surface. This marker is not a segmented vessel or a verified venous attachment.',landmark={'status':'regional','point':point.tolist(),'course':[],'connects':part,'contents':', '.join(vessels),'kind':'brain-surface'},surfaceAnchor=bind,vesselGuide={'role':'course-guide','vesselNames':list(vessels),'surfaceStructureIds':[sid(part)]})
 relations.append({'from':id,'to':sid(part),'type':'located_on'});anchors.append(row);return id
for side,s,code in [('left',1,'l'),('right',-1,'r')]:
 def a(key,label,part,p,v=(),aliases=()):return anchor(key+'.'+side,label+', '+side,part+'.'+code,[p[0]*s,p[1],p[2]],side,v,aliases)
 a('lateral-midbrain','Lateral midbrain surface','Midbrain',[17,-10,-10],['Lateral mesencephalic vein','Basal vein of Rosenthal'],['lateral mesencephalic region'])
 a('cerebral-peduncle','Cerebral peduncle, lateral surface','Base of peduncle',[15,-12,2],['Peduncular vein','Basal vein of Rosenthal'])
 a('tectum-superior','Superior tectal surface','Superior colliculus',[5,-5,-20],['Tectal veins','Posterior mesencephalic vein'],['quadrigeminal plate superior'])
 a('tectum-inferior','Inferior tectal surface','Inferior colliculus',[5,-13,-21],['Tectal veins','Precentral cerebellar vein'],['quadrigeminal plate inferior'])
 a('lateral-pons','Lateral pontine surface','Pons',[20,-31,-5],['Lateral pontine vein','Superior petrosal vein'],['cerebellopontine region'])
 a('pontomesencephalic','Pontomesencephalic junction region','Pons',[4,-18,1],['Anterior pontomesencephalic vein','Pontomesencephalic sulcus vein'])
 a('pontomedullary','Pontomedullary junction region','Pons',[7,-43,-7],['Vein of the pontomedullary sulcus'])
 a('lateral-medulla','Lateral medullary surface','Medulla oblongata',[11,-53,-14],['Lateral medullary vein'])
 a('superior-peduncle','Superior cerebellar peduncle surface','Superior cerebellar peduncle',[8,-22,-23],['Brachial tributary of the precentral cerebellar vein','Vein of the superior cerebellar peduncle'])
 a('flocculus','Floccular surface','Flocculus',[21,-35,-20],['Vein of the cerebellopontine fissure'])
 a('tonsil-medial','Medial tonsillar surface','Tonsil of cerebellum',[4,-50,-39],['Medial tonsillar vein','Vein of the lateral recess of the fourth ventricle'])
 a('tonsil-posterior','Posterior tonsillar surface','Tonsil of cerebellum',[13,-48,-56],['Retrotonsillar veins','Inferior vermian vein'])
 a('cerebellar-tentorial','Tentorial cerebellar surface','Superior semilunar lobule',[28,-13,-59],['Superior hemispheric veins'],['superior cerebellar surface'])
 a('cerebellar-suboccipital','Suboccipital cerebellar surface','Inferior semilunar lobule',[28,-43,-74],['Inferior hemispheric veins'],['inferior cerebellar surface'])
 a('cerebellar-petrosal','Petrosal cerebellar surface','Wing of central lobule',[16,-23,-13],['Anterior cerebellar veins','Superior petrosal vein'],['anterior cerebellar surface'])
 a('tentorial-notch','Tentorial free-edge region','Tentorium cerebelli',[18,-10,-18],['Basal vein of Rosenthal','Tentorial veins'],['tentorial incisura'])
 a('tentorial-lateral','Lateral tentorial surface','Tentorium cerebelli',[46,-23,-50],['Tentorial veins','Transverse sinus'])
 a('thalamic-superior','Superior thalamic surface','Thalamus',[10,15,-10],['Internal cerebral vein','Superior thalamic veins'])
 a('thalamic-posterior','Posterior thalamic surface','Thalamus',[12,8,-25],['Posterior thalamic veins','Basal vein of Rosenthal'],['pulvinar region'])
 a('ventricular-body','Lateral ventricular body boundary','Lateral ventricle',[9,25,-10],['Thalamostriate vein','Septal veins','Internal cerebral vein'])
 a('ventricular-atrium','Ventricular atrial boundary','Lateral ventricle',[25,14,-53],['Atrial veins','Medial atrial vein'],['trigone of lateral ventricle'])
 a('ventricular-temporal-horn','Temporal horn boundary','Lateral ventricle',[31,-13,0],['Inferior ventricular vein'])
 a('hippocampal','Hippocampal surface','Hippocampus',[25,-13,-10],['Hippocampal veins','Basal vein of Rosenthal'])
 a('caudate-head','Caudate head, ventricular surface','Caudate nucleus',[8,12,29],['Anterior caudate vein','Thalamostriate vein'])
 a('caudate-body','Caudate body, ventricular surface','Caudate nucleus',[16,24,-10],['Longitudinal caudate veins','Thalamostriate vein'])
 a('fornix','Forniceal body surface','Fornix',[3,17,0],['Internal cerebral vein','Septal veins'])
 a('choroid-plexus','Choroid plexus surface','Choroid plexus',[7,16,-3],['Superior choroidal vein','Internal cerebral vein'])
anchor('septum-pellucidum','Septal surface region','Septum pellucidum',[1,19,16],vessels=['Anterior septal vein','Posterior septal vein'],aliases=['septal veins landmark'])
anchor('hypothalamic','Inferior hypothalamic surface','Hypothalamus',[0,-14,12],vessels=['Hypothalamic veins','Basal vein of Rosenthal'])
# Midline seeds choose outer contours, avoiding the artificial cut faces of paired brainstem meshes.
anchor('anterior-pons','Anterior pontine surface','Pons.l',[1,-30,9],vessels=['Median anterior pontine vein'],aliases=['ventral pons'])
anchor('anterior-medulla','Anterior medullary surface','Medulla oblongata.l',[1,-56,-7],vessels=['Median anterior medullary vein'],aliases=['ventral medulla'])
anchor('precentral-cerebellar','Precentral cerebellar region','Lingula of cerebellum',[0,-23,-25],vessels=['Precentral cerebellar vein'])
anchor('superior-vermis','Superior vermian surface','Culmen',[0,-8,-36],vessels=['Superior vermian vein','Culmen veins'])
anchor('inferior-vermis','Inferior vermian surface','Pyramis of vermis',[0,-43,-61],vessels=['Inferior vermian vein'])
anchor('uvula','Vermian uvula surface','Uvula of vermis',[0,-49,-45],vessels=['Inferior vermian vein','Uvular veins'])
anchor('fourth-ventricle-roof','Fourth ventricular roof boundary','Fourth ventricle',[0,-34,-34],vessels=['Veins of the roof of the fourth ventricle'])
anchor('fourth-ventricle-floor','Fourth ventricular floor boundary','Fourth ventricle',[0,-34,-18],vessels=['Median posterior brainstem veins'])
anchor('callosal-splenium','Splenial surface region','Corpus callosum',[0,21,-46],vessels=['Posterior pericallosal vein','Vein of Galen'],aliases=['splenium'])
anchor('callosal-genu','Callosal genu region','Corpus callosum',[0,19,39],vessels=['Anterior pericallosal vein'],aliases=['genu'])
anchor('third-ventricle-roof','Third ventricular roof boundary','Third ventricle',[0,12,-5],vessels=['Internal cerebral veins'])
anchor('falx-inferior','Inferior falcine edge region','Falx cerebri',[0,29,0],vessels=['Inferior sagittal sinus'])
anchor('falcotentorial','Falcotentorial junction region','Falx cerebri',[0,-4,-61],vessels=['Straight sinus','Vein of Galen'])
# Sparse, explicitly regional stations; no claim that a line between them follows a sulcus.
courses=[('ventral-brainstem','Ventral brainstem course guides',['brain.landmark.pontomesencephalic.left','brain.landmark.anterior-pons','brain.landmark.anterior-medulla'],['Anterior pontomesencephalic vein','Median anterior pontine vein','Median anterior medullary vein']),('vermian','Vermian course guides',['brain.landmark.superior-vermis','brain.landmark.inferior-vermis','brain.landmark.uvula'],['Superior vermian vein','Inferior vermian vein'])]
for id,label,keys,vessels in courses:
 points=[byid[k]['landmark']['point'] for k in keys]
 add('brain.landmark.'+id,label,'brain.landmarks',kind='structure',geometryStatus='placeholder',description='Dashed lines join regional guide stations for orientation. They are not fitted vessel centrelines.',landmark={'status':'regional','point':points[0],'course':points,'connects':', '.join(keys),'contents':', '.join(vessels),'kind':'brain-course'},vesselGuide={'role':'course-guide','vesselNames':vessels,'anchorIds':keys,'surfaceStructureIds':[byid[k]['surfaceAnchor']['structureId'] for k in keys]})
manifest=json.loads((APP/'anatomy/generated/complete_manifest.json').read_text());manifest['structures']=[s for s in manifest['structures'] if s['system']!='brain'];manifest['relationships']=[r for r in manifest['relationships'] if not r['from'].startswith('brain') and not r['to'].startswith('brain')];manifest['sources']=[s for s in manifest['sources'] if s['id']!=ref];manifest['roots']=[r for r in manifest['roots'] if r!='brain']
# Resolve only existing vessel IDs; absent future veins remain named guide targets.
normalise=lambda s:re.sub(r'[^a-z0-9]','',s.lower().replace('left','').replace('right',''))
for row in rows:
 if row['parent']:byid[row['parent']]['children'].append(row['id'])
 guide=row.get('vesselGuide')
 if not guide:continue
 guide['vesselIds']=[]
 for vessel in manifest['structures']:
  if vessel['system'] not in ['vein','artery'] or vessel['kind']!='structure':continue
  if row['side']!='midline' and vessel['side'] not in [row['side'],'midline']:continue
  if any(normalise(n)==normalise(v) for n in guide['vesselNames'] for v in [vessel['name']]+vessel.get('aliases',[])):
   guide['vesselIds'].append(vessel['id']);relations.append({'from':vessel['id'],'to':row['id'],'type':'course_landmark','note':'Regional guide only; existing vessel geometry has not been refitted.'})
manifest['structures']+=rows;manifest['relationships']+=relations;manifest['roots'].append('brain');manifest['sources'].append({'id':ref,'title':'Z-Anatomy brain and dural orientation surfaces','role':f'{len(meshes)} named atlas meshes; skull-based similarity registration. Regional surface landmarks for vessel authoring.','licence':'CC BY-SA 4.0; inherited BodyParts3D attribution retained','notes':source['source_url']+'; full credit and source licence in public/anatomy/licenses/Z_Anatomy_Source_Licence.txt'})
manifest['brainRegistration']={'id':registration_id,'coordinateSystem':'RAS','units':'mm','matrixFromSourceOrientation':T.tolist(),'sourceAssetSha256':hashlib.sha256((SRC/'source-orientation.glb').read_bytes()).hexdigest(),'registeredAssetSha256':asset_hash,'method':reg['method'],'status':'atlas-registered','limitations':'Regional teaching context. Temporal skull residuals are greater than vault residuals. Source cerebellar lobules are simplified; no separate middle/inferior cerebellar peduncle meshes. Existing vessels have not been refitted to the new brain surfaces.'}
dump(APP/'anatomy/generated/complete_manifest.json',manifest)
dump(PUB/'brain-landmarks.json',{'schemaVersion':'1.0','registration':manifest['brainRegistration'],'anchors':[r for r in rows if r.get('landmark')],'surfaces':[{'id':r['id'],'name':r['name'],'asset':r['asset'],'anatomy':r['anatomy']} for r in rows if r.get('asset')]})
dump(SRC/'label-map.json',[{'id':r['id'],'name':r['name'],'sourceLabel':r['anatomy']['sourceLabel'],'parent':r['parent']} for r in rows if r.get('asset')])
print(json.dumps({'surfaces':len(meshes),'surfaceAnchors':len(anchors),'courseGuides':len(courses),'triangles':sum(len(m.faces) for m in meshes.values()),'sha256':asset_hash}))
