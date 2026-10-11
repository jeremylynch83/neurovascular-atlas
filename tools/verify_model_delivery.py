"""Verify a delivered checkpoint without VTK or the original atlas workspace.

Usage: python verify_package.py /path/to/unpacked/checkpoint
Requires Python 3 and NumPy. No network access is used.
"""
import sys,json,struct,hashlib
from pathlib import Path
import numpy as np

def verify(root):
 root=Path(root);exports=json.loads((root/'docs/checkpoint-export-v0.9.67.json').read_text());mf=json.loads((root/'public/anatomy/manifest.json').read_text());geometry={};hashes={};count=0
 for asset in exports['assets']:
  raw=(root/'public/anatomy/models'/asset['file']).read_bytes();assert hashlib.sha256(raw).hexdigest()==asset['sha256'],asset['file'];hashes[asset['file']]=asset['sha256'];magic,version,size=struct.unpack_from('<III',raw);assert (magic,version,size)==(0x46546c67,2,len(raw));jl=struct.unpack_from('<I',raw,12)[0];doc=json.loads(raw[20:20+jl]);start=28+jl
  def array(i):
   a=doc['accessors'][i];view=doc['bufferViews'][a['bufferView']];offset=start+view.get('byteOffset',0)+a.get('byteOffset',0);width=3 if a['type']=='VEC3' else 1;dtype='<f4' if a['componentType']==5126 else '<u4';x=np.frombuffer(raw,dtype=dtype,count=a['count']*width,offset=offset);return x.reshape(-1,width) if width>1 else x
  for mesh,expected in zip(doc['meshes'],asset['meshes']):
   assert mesh['name']==expected['node'];p=mesh['primitives'][0];v=array(p['attributes']['POSITION']);f=array(p['indices']).reshape(-1,3);assert len(v)==expected['vertices'] and len(f)==expected['triangles'];assert np.isfinite(v).all() and f.max()<len(v);assert hashlib.sha256(v.tobytes()).hexdigest()==expected['positionSha256'];assert hashlib.sha256(f.tobytes()).hexdigest()==expected['indicesSha256'];geometry[mesh['name']]=(v.copy(),f.copy());count+=2
 by={s['id']:s for s in mf['structures']};anchors=0
 def walk(x):
  nonlocal anchors
  if isinstance(x,dict):
   if {'structureId','triangleIndex','barycentric','position'}.issubset(x):
    n=by[x['structureId']]['asset']['node'];v,f=geometry[n];w=np.array(x['barycentric']);assert abs(w.sum()-1)<1e-6 and w.min()>-1e-6 and w.max()<1+1e-6;point=(v[f[x['triangleIndex']]].astype(float)*w[:,None]).sum(0);assert np.linalg.norm(point-x['position'])<1e-5;assert x['assetSha256']==hashes['brain-context.glb'];anchors+=1
   for value in x.values():walk(value)
  elif isinstance(x,list):
   for value in x:walk(value)
 for name in ['manifest.json','brain-landmarks.json','vessel-courses.json']:walk(json.loads((root/'public/anatomy'/name).read_text()))
 for course in json.loads((root/'public/anatomy/vessel-courses.json').read_text())['courses']:
  assert course['geometrySha256']==hashes[Path(course['geometry']['file']).name];assert course['brainAssetSha256']==hashes['brain-context.glb']
 report={'passed':True,'meshes':len(geometry),'exactBufferComparisons':count,'verifiedSurfaceAnchors':anchors,'assets':len(hashes),'scope':'File identity, finite coordinates, index bounds, exact exported buffers and updated surface/course bindings. Does not repeat anatomical collision or fold tests.'};print(json.dumps(report));return report
if __name__=='__main__':verify(sys.argv[1])
