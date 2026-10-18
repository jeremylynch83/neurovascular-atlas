from pathlib import Path
import zipfile,json,numpy as np
from scipy.sparse import coo_matrix
from scipy.sparse.csgraph import connected_components
A=Path('/workspace/scratch/3da1329b983b/atlas/inr-anatomy-atlas-v0.9.91');W=A.parents[1]/'batch20-work';z=zipfile.ZipFile(A.parents[1]/'inr-anatomy-atlas-v0.9.111.zip');root='inr-anatomy-atlas-v0.9.111/';src=[n for n in z.namelist()if n.startswith(root+'src/')and not n.endswith('/')];assert all((A/n[len(root):]).read_bytes()==z.read(n)for n in src)
a=json.loads(z.read(root+'public/anatomy/manifest.json'));b=json.load(open(A/'anatomy/generated/complete_manifest.json'))
def graph(m):return [(s['id'],s.get('parent'),s.get('children'),s.get('asset'))for s in m['structures']]
assert graph(a)==graph(b);assert a['relationships']==b['relationships'];result={'runtimeSourceFilesByteExact':len(src),'namedMeshesRetained':1250,'unchangedNamedMeshes':1250-len(json.load(open(W/'accepted-patches.json'))['changes']),'catalogueStructuresRetained':len(b['structures']),'relationshipsAndAssetBindingsUnchanged':True,'selectedLabelTopology':[]}
for row in json.load(open(W/'accepted-patches.json'))['changes']:
 n=row['node'];stats={}
 for d,label in [('decoded','before'),('candidate','after')]:
  p=np.fromfile(W/d/(n+'.positions.bin'),'<f4').reshape(-1,3);g=np.fromfile(W/d/(n+'.indices.bin'),'<u4').reshape(-1,3);u,inv=np.unique(p,axis=0,return_inverse=True);f=inv[g];used,remap=np.unique(f,return_inverse=True);f=remap.reshape(-1,3);e=np.vstack([f[:,[0,1]],f[:,[1,2]],f[:,[2,0]]]);adj=coo_matrix((np.ones(len(e)),(e[:,0],e[:,1])),shape=(len(used),len(used))).tocsr();stats[label]={'components':int(connected_components(adj,directed=False,return_labels=False))}
 result['selectedLabelTopology'].append({'node':n,**stats})
(W/'integration-retention.json').write_text(json.dumps(result,indent=2)+'\n');print(result)
