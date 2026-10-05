"""Bind release evidence to the exact losslessly decoded delivered assets."""
import argparse,hashlib,json,numpy as np
from fit_vessels import APP,PUB,read_glb,mesh_records,accessor

def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def main():
 parser=argparse.ArgumentParser();parser.add_argument('--release',default='0.9.17');parser.add_argument('--arteries-authoring',default='.authoring/arteries-fitted.glb');parser.add_argument('--arteries-exported',default='.authoring/arteries-exported.glb');args=parser.parse_args()
 report={'release':args.release,'assets':{},'allDeliveredAccessorsMatchAuthoring':True}
 changes=json.loads((APP/f'docs/validation/vessel-fitting-v{args.release}.json').read_text())
 for asset,file in [('arteries','complete-circulation.glb'),('veins','venous.glb')]:
  ad,ab=read_glb(APP/args.arteries_authoring if asset=='arteries' else APP/f'.authoring/{asset}-fitted.glb');ed,eb=read_glb(APP/args.arteries_exported if asset=='arteries' else APP/f'.authoring/{asset}-exported.glb')
  bd,bb=read_glb(APP/f'.authoring/{asset}-baseline.glb');author=mesh_records(ad,ab);exported=mesh_records(ed,eb);baseline=mesh_records(bd,bb)
  assert set(author)==set(exported)==set(baseline)
  changed=[]
  for node,r in author.items():
   for attribute in ['POSITION','NORMAL']:
    assert np.array_equal(accessor(ad,ab,r['primitive']['attributes'][attribute]),accessor(ed,eb,exported[node]['primitive']['attributes'][attribute])),node
   assert np.array_equal(r['faces'],exported[node]['faces'])
   assert np.array_equal(r['faces'],baseline[node]['faces'])
   if not np.array_equal(r['positions'],baseline[node]['positions']):changed.append(node)
  assert set(changed)=={r['node'] for r in changes['geometry'] if r['asset']==asset}
  if asset=='veins':assert not changed,'Deferred venous corrections must remain unapplied'
  report['assets'][asset]={'file':file,'sha256':sha(PUB/'models'/file),'labels':len(author),'changedLabels':changed,'triangleIndicesRetainedExactly':True}
 assert sha(APP/'.authoring/brain-baseline.glb')==sha(PUB/'models/brain-context.glb')
 report['brainAssetSha256']=sha(PUB/'models/brain-context.glb');report['allBrainGeometryUnchanged']=True
 manifest=json.loads((PUB/'manifest.json').read_text());courses=json.loads((PUB/'vessel-courses.json').read_text())
 assert manifest['release']==args.release
 hashes={file:sha(PUB/file) for file in {c['geometry']['file'] for c in courses['courses']}}
 for c in courses['courses']:
  assert c['geometrySha256']==hashes[c['geometry']['file']]
  assert c['brainAssetSha256']==report['brainAssetSha256']
 report['courseHashesMatchDeliveredAssets']=True
 (APP/f'docs/validation/fitting-export-v{args.release}.json').write_text(json.dumps(report,indent=2)+'\n')
 print(json.dumps(report,indent=2))
if __name__=='__main__':main()
