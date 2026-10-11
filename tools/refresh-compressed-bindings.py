"""Refresh hashes, surface witnesses and metadata after a topology-preserving export."""
import hashlib,json,struct,subprocess,math
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
report=json.loads((ROOT/'docs/compression-validation.json').read_text())
# Previous transport hashes are retained in the manifest before the export.
old=json.loads((ROOT/'anatomy/generated/complete_manifest.json').read_text())
old_hashes={a['name']+'.glb':[a['previousTransportSha256'],a['sourceSha256']] for a in report['assets']}
old_hashes['brain-context.glb'].append(old['brainRegistration']['registeredAssetSha256'])
for s in old['structures']:
 if s.get('vesselCourse') and s.get('asset'):
  old_hashes[Path(s['asset']['file']).name].append(s['vesselCourse']['geometrySha256'])
for name in old_hashes:
 old_hashes[name].append(old['assetRevisions']['models/'+name])
 old_hashes[name]=set(old_hashes[name])
new_hashes={a['name']+'.glb':a['sha256'] for a in report['assets']}
path=ROOT/'public/anatomy/models/brain-context.glb';raw=path.read_bytes();length=struct.unpack_from('<I',raw,12)[0];doc=json.loads(raw[20:20+length])
binary=subprocess.check_output(['node',str(ROOT/'tools/decode-meshopt-views.mjs'),str(path)],cwd=ROOT)
def accessor(id):
 a=doc['accessors'][id];v=doc['bufferViews'][a['bufferView']];width=3 if a['type']=='VEC3' else 1;code={5126:'f',5125:'I',5123:'H'}[a['componentType']];fmt='<'+code*width;stride=v.get('byteStride',struct.calcsize(fmt));start=v.get('byteOffset',0)+a.get('byteOffset',0)
 return [struct.unpack_from(fmt,binary,start+i*stride) for i in range(a['count'])]
nodes={};metadata={}
for n in doc['nodes']:
 if 'mesh' not in n:continue
 p=doc['meshes'][n['mesh']]['primitives'][0];positions=accessor(p['attributes']['POSITION']);indices=accessor(p['indices']);nodes[n['name']]=(positions,indices)
 a=doc['accessors'][p['attributes']['POSITION']];v=doc['bufferViews'][a['bufferView']];start=v['byteOffset'];posbytes=binary[start:start+a['count']*12]
 metadata[n['name']]={'bounds':[a['min'],a['max']],'centroid':[sum(x[k] for x in positions)/len(positions) for k in range(3)],'positionSha256':hashlib.sha256(posbytes).hexdigest()}
rows={s['id']:s for s in old['structures']}
points={};max_shift=0;count=0
def update_anchor(a):
 global max_shift,count
 node=rows[a['structureId']]['asset']['node'];vertices,indices=nodes[node];t=a['triangleIndex'];w=a['barycentric'];p=[sum(w[j]*vertices[indices[t*3+j][0]][k] for j in range(3)) for k in range(3)]
 max_shift=max(max_shift,math.dist(p,a['position']));a['position']=p;count+=1
for s in old['structures']:
 if s.get('surfaceAnchor'):
  a=json.loads(json.dumps(s['surfaceAnchor']));update_anchor(a);points[s['id']]=a['position']
def recurse(x):
 if isinstance(x,list):
  for item in x:recurse(item)
 elif isinstance(x,dict):
  if all(k in x for k in ['triangleIndex','barycentric','structureId','position']):update_anchor(x)
  for item in x.values():recurse(item)
  if x.get('surfaceAnchor') and x.get('landmark'):x['landmark']['point']=x['surfaceAnchor']['position']
  guide=x.get('vesselGuide',{})
  if guide.get('anchorIds') and x.get('landmark'):x['landmark']['course']=[points[k] for k in guide['anchorIds']]
  if x.get('asset',{}).get('file')=='models/brain-context.glb' and x.get('anatomy'):
   x['anatomy'].update(metadata[x['asset']['node']])
for folder in ['anatomy','public/anatomy']:
 for p in (ROOT/folder).rglob('*.json'):
  text=p.read_text()
  # Hashes may be complete SHA256 values or truncated cache revisions.
  for name,previous_values in old_hashes.items():
   for previous in previous_values:
    if len(previous)==64:text=text.replace('"'+previous+'"','"'+new_hashes[name]+'"')
    text=text.replace('"'+previous[:20]+'"','"'+new_hashes[name][:20]+'"')
  value=json.loads(text);recurse(value)
  if isinstance(value,dict) and 'release' in value:value['release']='0.9.71'
  p.write_text(json.dumps(value,indent=2)+'\n')
report['surfaceAnchorsRefreshed']=len(points);report['maximumAnchorShiftMm']=max_shift
(ROOT/'docs/compression-validation.json').write_text(json.dumps(report,indent=2)+'\n')
print('Refreshed',len(points),'primary surface anchors; maximum shift',max_shift,'mm')
