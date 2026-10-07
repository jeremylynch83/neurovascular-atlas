from geometry import *
import hashlib
APP=Path(__file__).resolve().parents[2];path=APP/'anatomy/generated/complete_manifest.json';m=json.loads(path.read_text());rows={r['id']:r for r in m['structures']}
src=json.loads((APP/'anatomy/source/posterior-veins-v0.9.28.json').read_text());src['release']='0.9.29';src['baselineRelease']='0.9.28'
report=[]
for row in src['structures']:
 if row['mode']!='pial' or not any(row['id'].startswith('vein.'+name+'.') for name in ['superior_cerebellar_peduncular','tectal','horizontal_fissure']):continue
 targets=row.get('surfaceTarget') or row['targets'];targets=[targets] if isinstance(targets,str) else targets
 targets=[t for t in targets if t in rows and rows[t].get('asset')];locs=[locator(meshes[rows[t]['asset']['node']].pd) for t in targets]
 if not locs:continue
 segments=[];paths=[];split=False
 for pi,part in enumerate(row['parts']):
  q=np.asarray(part['points']);rad=np.asarray(part['radius']);rad=np.broadcast_to(rad,(len(q),)) if rad.ndim==0 else rad
  d=np.array([min(close(l,p)[1] for l in locs) for p in q]);arc=np.r_[0,np.cumsum(np.linalg.norm(np.diff(q,axis=0),axis=1))]
  # Authoring boundary: last supported surface station before a sustained
  # terminal departure towards the receiver. This is not a clinical threshold.
  supported=np.flatnonzero(d<=rad+1.0);cut=int(supported[-1]) if len(supported) else 0
  qualifies=cut>2 and cut<len(q)-3 and arc[-1]-arc[cut]>3 and part.get('receiver') and d[-1]>rad[-1]+3
  # For horizontal fissure, use both semilunar banks for attachment support.
  if qualifies:
   split=True;ranges=[(0,cut,'pial'),(cut,len(q)-1,'cisternal')]
  else:ranges=[(0,len(q)-1,'pial')]
  canonical=json.dumps(part['points'],separators=(',',':')).encode();paths.append({'source':'anatomy/source/posterior-veins-v0.9.29.json','sourceStructureId':row['id'],'sourcePart':pi,'pointCount':len(q),'pointSha256':hashlib.sha256(canonical).hexdigest(),'lengthMm':float(arc[-1])})
  for a,b,mode in ranges:
   segments.append({'order':len(segments),'mode':mode,'targetStructureIds':rows[row['id']]['vesselCourse']['targetStructureIds'] if mode=='pial' else [],'stationIds':[],'stationRole':'bounded-source-centreline','pathIndex':pi,'pointRange':[a,b],'arcRangeMm':[float(arc[a]),float(arc[b])],'constraints':{'wallClearance':'radius-aware','allowTissueEntry':False,'avoidAtlasCutFaces':True,'preserveJoinedAttachments':True},'reviewStatus':'representative-course-requires-anatomical-review','summary':('Surface or fissural tributary' if mode=='pial' else 'Free cisternal outlet to the selected receiving vein; do not impose pial apposition')})
  if qualifies:report.append({'id':row['id'],'part':pi,'lastSurfacePoint':cut,'surfaceLengthMm':float(arc[cut]),'outletLengthMm':float(arc[-1]-arc[cut]),'boundaryPosition':q[cut].tolist(),'method':'Source centreline terminal departure from named surface, with radius plus 1 mm authoring support envelope; provisional transition requiring anatomical review'})
 if split:
  c=rows[row['id']]['vesselCourse'];c['segments']=segments;c['coursePaths']=paths;c['summary']+=' Surface/fissural tributary and cisternal outlet are recorded as separate bounded segments.'
  row['courseSegments']=segments;row['coursePaths']=paths
(APP/'anatomy/source/posterior-veins-v0.9.29.json').write_text(json.dumps(src,indent=2)+'\n')
path.write_text(json.dumps(m,indent=2)+'\n');(APP/'docs/validation/anatomical-course-partitions-v0.9.29.json').write_text(json.dumps({'release':'0.9.29','partitions':report},indent=2)+'\n');print(json.dumps(report,indent=1))
