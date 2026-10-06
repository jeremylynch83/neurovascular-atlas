"""Standard-library checks for persisted brain geometry/semantic bindings."""
import json,hashlib,struct,math,subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
def validate_brain(manifest):
 errors=[];reg=manifest.get('brainRegistration')
 if not reg:return errors
 rows={s['id']:s for s in manifest['structures']};path=ROOT/'public/anatomy/models/brain-context.glb';data=path.read_bytes();sha=hashlib.sha256(data).hexdigest()
 if sha!=reg['registeredAssetSha256']:errors.append('Brain registration asset hash mismatch')
 ln=struct.unpack_from('<I',data,12)[0];doc=json.loads(data[20:20+ln]);binary=memoryview(data)[28+ln:];nodes={n['name']:n for n in doc['nodes'] if 'mesh' in n}
 if any(v.get('extensions',{}).get('EXT_meshopt_compression') for v in doc['bufferViews']):
  binary=memoryview(subprocess.check_output(['node',str(ROOT/'tools/decode-meshopt-views.mjs'),str(path)],cwd=ROOT))
 def accessor(index):
  a=doc['accessors'][index];bv=doc['bufferViews'][a['bufferView']];code={5123:'H',5125:'I',5126:'f'}[a['componentType']];width={'VEC3':3,'SCALAR':1}[a['type']];fmt='<'+code*width;size=struct.calcsize(fmt);stride=bv.get('byteStride',size);start=bv.get('byteOffset',0)+a.get('byteOffset',0)
  return [struct.unpack_from(fmt,binary,start+i*stride) for i in range(a['count'])]
 cache={}
 for s in rows.values():
  a=s.get('surfaceAnchor')
  if not a:continue
  try:
   target=rows[a['structureId']];assert target['system']=='brain' and target.get('asset')
   assert a['assetSha256']==sha and a['registrationId']==reg['id']
   assert s['landmark']['kind']=='brain-surface'
   weights=a['barycentric'];assert len(weights)==3 and all(math.isfinite(x) and -1e-6<=x<=1+1e-6 for x in weights) and abs(sum(weights)-1)<1e-6
   node=target['asset']['node']
   if node not in cache:
    primitive=doc['meshes'][nodes[node]['mesh']]['primitives'][0];cache[node]=(accessor(primitive['attributes']['POSITION']),accessor(primitive['indices']))
   vertices,indices=cache[node];triangle=a['triangleIndex'];assert isinstance(triangle,int) and 0<=3*triangle<len(indices)-2
   p=[sum(weights[j]*vertices[indices[3*triangle+j][0]][k] for j in range(3)) for k in range(3)]
   assert max(abs(x-y) for x,y in zip(p,a['position']))<1e-4
   assert max(abs(x-y) for x,y in zip(p,s['landmark']['point']))<1e-4
  except (AssertionError,KeyError,ValueError,IndexError) as e:errors.append(f'{s["id"]}: invalid or stale brain anchor {e}')
 for s in rows.values():
  g=s.get('vesselGuide')
  if not g:continue
  if any(id not in rows or rows[id]['system'] not in ['vein','artery'] for id in g['vesselIds']):errors.append(f'{s["id"]}: unknown guide vessel')
  if any(id not in rows or not rows[id].get('asset') for id in g['surfaceStructureIds']):errors.append(f'{s["id"]}: unknown guide surface')
  if any(id not in rows or not rows[id].get('surfaceAnchor') for id in g.get('anchorIds',[])):errors.append(f'{s["id"]}: unknown course anchor')
  keys=g.get('anchorIds',[])
  if keys:
   points=s['landmark']['course']
   if len(points)!=len(keys) or any(max(abs(x-y) for x,y in zip(point,rows[key]['surfaceAnchor']['position']))>1e-4 for point,key in zip(points,keys)):
    errors.append(f'{s["id"]}: course differs from its bound stations')
 # Secondary witnesses carry the same stale-asset and triangle checks.
 for s in rows.values():
  for a in s.get('secondarySurfaceAnchors',[]):
   try:
    target=rows[a['structureId']];node=target['asset']['node']
    assert a['assetSha256']==sha and a['registrationId']==reg['id']
    if node not in cache:
     primitive=doc['meshes'][nodes[node]['mesh']]['primitives'][0];cache[node]=(accessor(primitive['attributes']['POSITION']),accessor(primitive['indices']))
    vertices,indices=cache[node];weights=a['barycentric'];triangle=a['triangleIndex']
    assert isinstance(triangle,int) and 0<=3*triangle<len(indices)-2
    assert len(weights)==3 and all(math.isfinite(x) and -1e-6<=x<=1+1e-6 for x in weights) and abs(sum(weights)-1)<1e-6
    p=[sum(weights[j]*vertices[indices[3*triangle+j][0]][k] for j in range(3)) for k in range(3)]
    assert max(abs(x-y) for x,y in zip(p,a['position']))<1e-4
   except (AssertionError,KeyError,ValueError,IndexError) as e:errors.append(f'{s["id"]}: invalid secondary surface anchor {e}')
 return errors
if __name__=='__main__':
 manifest=json.loads((ROOT/'public/anatomy/manifest.json').read_text());errors=validate_brain(manifest)
 if errors:raise SystemExit('\n'.join(errors))
 print('Brain surface bindings and guide references validated.')
