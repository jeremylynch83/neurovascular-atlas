"""Extract exact decoded GLB label buffers for compact offline provenance."""
import argparse,copy
from pathlib import Path
from fit_vessels import read_glb,write_glb,accessor

def main():
 p=argparse.ArgumentParser();p.add_argument('source');p.add_argument('target');p.add_argument('--node',action='append',required=True);args=p.parse_args()
 source,raw=read_glb(Path(args.source));data=bytearray();doc={'asset':copy.deepcopy(source['asset']),'scene':0,'scenes':[{'nodes':[]}],'nodes':[],'meshes':[],'materials':copy.deepcopy(source.get('materials',[])),'accessors':[],'bufferViews':[],'buffers':[{}]}
 found=set()
 def extract(i,target):
  values=accessor(source,raw,i).copy();index=len(doc['accessors']);a=copy.deepcopy(source['accessors'][i]);a.pop('byteOffset',None);a['bufferView']=len(doc['bufferViews'])
  data.extend(b'\0'*(-len(data)%4));doc['bufferViews'].append({'buffer':0,'byteOffset':len(data),'byteLength':values.nbytes,'target':target});data.extend(values.tobytes());doc['accessors'].append(a);return index
 for node in source['nodes']:
  if node.get('name') not in args.node:continue
  assert 'mesh' in node and not any(k in node for k in ['matrix','translation','rotation','scale'])
  n=copy.deepcopy(node);n['mesh']=len(doc['meshes']);mesh=copy.deepcopy(source['meshes'][node['mesh']])
  for primitive in mesh['primitives']:
   assert not primitive.get('extensions'),'Decode compressed source first'
   primitive['attributes']={k:extract(i,34962) for k,i in primitive['attributes'].items()};primitive['indices']=extract(primitive['indices'],34963)
  doc['scenes'][0]['nodes'].append(len(doc['nodes']));doc['nodes'].append(n);doc['meshes'].append(mesh);found.add(n['name'])
 assert found==set(args.node),'Missing named source mesh'
 doc['buffers'][0]['byteLength']=len(data);write_glb(Path(args.target),doc,data)
 print(f'Extracted {len(found)} exact label buffers.',flush=True)
if __name__=='__main__':main()
