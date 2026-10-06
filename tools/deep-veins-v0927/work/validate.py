from common import *
from scipy.sparse import coo_matrix
from scipy.sparse.csgraph import connected_components
rev=json.loads((OUT/'revision.json').read_text());spec=json.loads((OUT/'courses.json').read_text());new={r['id']:r for r in spec['structures']};changed={r['node'] for r in rev['changed']};arrays={};pds={}
for k in changed:
 v=np.fromfile(OUT/(k+'.positions.bin'),'<f4').reshape(-1,3).astype(float);f=np.fromfile(OUT/(k+'.indices.bin'),'<u4').reshape(-1,3);arrays[k]=(v,f);pds[k]=poly(v,f)
report={'release':'0.9.27','baseline':'0.9.26','newFamilies':22,'newMeshLabels':44,'excluded':'Transmedullary veins','checks':{},'newArteryOrBoneContacts':[],'unexpectedVenousJoins':[],'otherExistingVeinContacts':[],'passed':False,'scope':'Actual triangle skin intersections, labelled shared ostia, finite non-degenerate geometry and catalogue coverage. Intentional intraparenchymal/subependymal/choroidal courses can intersect their target tissue. No clinical accuracy or general solid containment claim.'}
quality=[]
for k,(v,f) in arrays.items():
 t=v[f];area=np.linalg.norm(np.cross(t[:,1]-t[:,0],t[:,2]-t[:,0]),axis=1);n=np.fromfile(OUT/(k+'.normals.bin'),'<f4').reshape(-1,3);quality.append({'node':k,'vertices':len(v),'triangles':len(f),'zeroAreaTriangles':int((area==0).sum()),'passed':bool(np.isfinite(v).all() and (area>0).all() and np.isfinite(n).all() and (np.linalg.norm(n,axis=1)>.99).all())})
report['checks']['meshQuality']={'parts':quality,'passed':all(r['passed'] for r in quality)}
# All external outlets actually share output skin vertices after the labelled union.
joins=[]
for k,row in new.items():
 for receiver in sorted({p['receiver'] for p in row['parts'] if p['receiver']!=k}|{c['to'] for c in row.get('additionalAuthoredConnections',[])}):
  d=cKDTree(arrays[receiver][0]).query(arrays[k][0],distance_upper_bound=.001)[0];matches=int((d<.001).sum());joins.append({'from':k,'to':receiver,'sharedVertices':matches,'passed':matches>=3})
report['checks']['physicalJunctions']={'pairs':joins,'passed':all(r['passed'] for r in joins)}
# Check new skin adjacency against the authored drainage graph. Triple ostia are reported explicitly.
adjacencies=[];allowed={tuple(sorted([r['from'],r['to']])) for r in joins}
for k,row in new.items():
 for conn in row.get('additionalAuthoredConnections',[]):allowed.add(tuple(sorted([k,conn['to']])))
 for b in row.get('commonJunctionNeighbours',[]):allowed.add(tuple(sorted([k,b])))
for a,k in enumerate(sorted(changed)):
 for b in sorted(changed)[a+1:]:
  v=arrays[k][0];w=arrays[b][0]
  if np.any(v.max(0)<w.min(0)-.001) or np.any(w.max(0)<v.min(0)-.001):continue
  shared=cKDTree(w).query(v,distance_upper_bound=.001)[0]<.001
  if shared.sum()<3:continue
  if k not in new and b not in new:continue
  rec={'one':k,'two':b,'sharedVertices':int(shared.sum()),'authoredDirectJoin':tuple(sorted([k,b])) in allowed};adjacencies.append(rec)
  if not rec['authoredDirectJoin']:report['unexpectedVenousJoins'].append(rec)
report['checks']['junctionAdjacency']={'pairs':adjacencies,'passed':not report['unexpectedVenousJoins']}
# Preserve interfaces between retained receiving trunks and untouched venous labels.
collars=[]
for k in sorted(changed-new.keys()):
 tree=cKDTree(meshes[k].v)
 for b,m in meshes.items():
  if m.file!=meshes[k].file or b in changed:continue
  if np.any(meshes[k].bounds[1]<m.bounds[0]-.001) or np.any(m.bounds[1]<meshes[k].bounds[0]-.001):continue
  shared=m.v[tree.query(m.v,distance_upper_bound=.0007)[0]<.0007]
  if len(shared)<3:continue
  loc=locator(pds[k]);gap=max(close(loc,p)[1] for p in shared);collars.append({'one':k,'two':b,'maximumOriginalCollarGapMm':gap,'passed':gap<.025})
report['checks']['retainedCollars']={'pairs':collars,'toleranceMm':.025,'passed':all(r['passed'] for r in collars)}
for i,k in enumerate(sorted(new)):
 for b,m in meshes.items():
  if b in changed:continue
  if m.file==meshes['vein.galen'].file:
   if contacts(pds[k],m.pd,True):report['otherExistingVeinContacts'].append({'newVein':k,'other':b})
   continue
  if m.file not in ['complete-circulation.glb','craniofacial.glb','complete-anastomoses.glb']:continue
  hit=contacts(pds[k],m.pd,True)
  if hit:report['newArteryOrBoneContacts'].append({'newVein':k,'other':b,'asset':m.file})
 if i%8==0:print('Walls',i+1,'/',len(new),'contact pairs',len(report['newArteryOrBoneContacts']),flush=True)
report['checks']['newArteryAndBoneClearance']={'passed':not report['newArteryOrBoneContacts']}
report['checks']['otherExistingVeinClearance']={'passed':not report['otherExistingVeinContacts']}
report['passed']=all(r['passed'] for r in report['checks'].values());(OUT/'validation.json').write_text(json.dumps(report,indent=2)+'\n');print('PASSED',report['passed'],'failed joins',[r for r in joins if not r['passed']],'unexpected',report['unexpectedVenousJoins'],'contacts',report['newArteryOrBoneContacts'],flush=True)
