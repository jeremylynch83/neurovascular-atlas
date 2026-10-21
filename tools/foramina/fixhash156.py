from pathlib import Path
import sys,json,hashlib,numpy as np
A=Path(__file__).resolve().parents[2];sys.path.insert(0,str(A/'tools/foramina'));from geometry import Glb
m=json.load(open(A/'anatomy/generated/complete_manifest.json'));changed=set(json.load(open(A/'anatomy/source/foramina/revision156-flow-changes.json')))
for file in ['models/complete-circulation.glb','models/complete-anastomoses.glb']:
 g=Glb(A/'public/anatomy'/file)
 for row in m['structures']:
  if row['id']in changed and row['asset']['file']==file:
   p,f,n=g.mesh(row['asset']['node']);row['flowCourseGuide']['geometrySha256']=hashlib.sha256(np.asarray(p,'<f4').tobytes()+np.asarray(f,'<u4').tobytes()).hexdigest()
(A/'anatomy/generated/complete_manifest.json').write_text(json.dumps(m,indent=2)+'\n');print('Geometry-bound guide hashes refreshed from encoded source')
