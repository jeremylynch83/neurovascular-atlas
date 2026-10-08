from model import *
import hashlib,shutil
r=APP;m=json.load(open(r/'anatomy/generated/complete_manifest.json'));changed=set(a['node'] for a in json.load(open(OUT/'revision.json'))['changed']);hashes={'models/'+p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in (r/'public/anatomy/models').glob('*.glb')};v=json.load(open(OUT/'validation.json'));cal={a['side']:a for a in v['checks']['calibreAndGenu']['sides']};extra={a['side']:a for a in v['checks']['fullSurfaceConstraints']['sides']};bound={a['side']:a for a in json.load(open(OUT/'boundaries.json'))}
m['assetRevisions']={file:sha[:20] for file,sha in hashes.items()};m['assetByteSizes']={file:(r/'public/anatomy'/file).stat().st_size for file in hashes};m['release']='0.9.32';m['icaCavernousRefinement']={'version':'0.9.32','baseline':'0.9.31','method':'Joint ICA loop and independent bone-fitted cavernous chamber; fixed ophthalmic arteries; remeshed parent with native ostial collars','reviewStatus':'requires-anatomical-review','evidence':'docs/ICA_CS_v0.9.32.md','validation': 'anatomy/source/ica-cs-v0932/validation.json'}
for s in m['structures']:
 if 'vesselCourse' not in s:continue
 c=s['vesselCourse'];c['geometrySha256']=hashes[s['asset']['file']];node=s['asset']['node']
 if node not in changed:continue
 c['reviewStatus']='requires-anatomical-review';c['candidateReviewStatus']='ICA / cavernous local geometry checks complete; independent anatomical review pending';s['provenance']['reviewStatus']='unreviewed';s['notes']=s.get('notes','').split(' Geometry update v0.9.32:')[0]+' Geometry update v0.9.32: local ICA/CS reconstruction with exact ophthalmic meshes and native ostial collars; compact independent bone-fitted sinus and shared tributary joins. See docs/ICA_CS_v0.9.32.md.'
 if node.startswith(('ICA cavernous ','ICA paraophthalmic ')) and s['side'] in cal:
  c['radiusPolicy']='preserve-source-profile-with-measured-wall-deformation';c.setdefault('fitting',{})['calibreCheck']={k:cal[s['side']][k] for k in ['method','calibreScope','ratioP05MedianP95','p95AbsoluteFractionalRadiusChange']}
 if node.startswith(('ICA cavernous ','ICA paraophthalmic ','ICA petrous ')):
  s['spatialBoundary']=bound[s['side']];s['spatialBoundary']['nativeGenuToOstiumArcMm']=extra[s['side']]['nativeGenuToOstiumArcMm'];s['spatialBoundary']['revisedGenuToOstiumArcMm']=extra[s['side']]['revisedGenuToOstiumArcMm']
  if 'segmentRange' in s:s['segmentRange']['status']='Legacy authoring stations retained for traceability; final spatial boundary follows documented bone-fitted envelope/estimated petrolingual entry; absolute whole-ICA arc not remeasured'
  s['anatomicalReview']={'status':'provisional-boundary','issueIds':['G04'],'summary':'Updated cavernous loop and anterior genu fit independent sinus and fixed ophthalmic origin. Entry and dural exit are estimates. Native lower petrous canal contacts remain outside the corrected cavernous scope; no segmented dural rings.'}
# Reassign only a source branch that is physically on the retained lower ICA region.
byNode={s.get('asset',{}).get('node'):s for s in m['structures']};byid={s['id']:s for s in m['structures']}
for a in json.load(open(OUT/'catalogue-joins.json')):
 if not a.get('boundaryReassignment'):continue
 child=byNode[a['b']];old=child['parent'];new=byNode[a['boundaryReassignment']]['id'];child['parent']=new
 for rel in m['relationships']:
  if rel['from']==old and rel['to']==child['id'] and rel['type']=='branches_to':rel['from']=new
for s in m['structures']:s['children']=[x['id'] for x in m['structures'] if x.get('parent')==s['id']]
for s in m['structures']:
 if not s.get('vesselCourse'):continue
 a=s['vesselCourse']['attachments'];a['parentId']=s['parent'];a['incoming']=[x for x in m['relationships'] if x['to']==s['id']];a['outgoing']=[x for x in m['relationships'] if x['from']==s['id']]
(r/'anatomy/generated/complete_manifest.json').write_text(json.dumps(m,indent=2)+'\n');c=json.load(open(r/'public/anatomy/vessel-courses.json'));c['courses']=[s['vesselCourse'] for s in m['structures'] if s.get('vesselCourse')];c['release']='0.9.32';(r/'public/anatomy/vessel-courses.json').write_text(json.dumps(c,indent=2)+'\n');dest=r/'anatomy/source/ica-cs-v0932';dest.mkdir(exist_ok=True)
for p in OUT.glob('*.json'):shutil.copy2(p,dest/p.name)
for p in ['centreline-right.npz','centreline-left.npz']:
 if (ROOT/p).resolve()!=(r/'tools/ica-cs-v0932'/p).resolve():shutil.copy2(ROOT/p,r/'tools/ica-cs-v0932'/p)
