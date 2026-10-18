"""Ensure simplification did not introduce new physical defect locations."""
from pathlib import Path
import json,sys
import numpy as np

r=Path(sys.argv[1]);j=json.loads((r/'trial-0.01.json').read_text());results=[]
def defects(p,f):
    unique,inverse=np.unique(p,axis=0,return_inverse=True);w=inverse[f]
    t=p[f].astype(float);area=np.linalg.norm(np.cross(t[:,1]-t[:,0],t[:,2]-t[:,0]),axis=1)
    pos=w[area>0]
    edges=np.sort(np.concatenate([pos[:,[0,1]],pos[:,[1,2]],pos[:,[2,0]]]),axis=1)
    e,c=np.unique(edges,axis=0,return_counts=True)
    bad={tuple(sorted((tuple(unique[a]),tuple(unique[b]))))for a,b in e[c>2]}
    zero={tuple(sorted(map(tuple,v)))for v in t[area==0]}
    return bad,zero
for m in j['meshes']:
    if not m['changed']:continue
    name=m['name']
    p=np.fromfile(r/'baseline'/(name+'.positions.bin'),'<f4').reshape(-1,3)
    f=np.fromfile(r/'baseline'/(name+'.indices.bin'),'<u4').reshape(-1,3)
    q=np.fromfile(r/'0.01'/(name+'.positions.bin'),'<f4').reshape(-1,3)
    g=np.fromfile(r/'0.01'/(name+'.indices.bin'),'<u4').reshape(-1,3)
    before,zbefore=defects(p,f);after,zafter=defects(q,g)
    results.append({'name':name,'newNonManifoldEdgeLocations':len(after-before),'newZeroAreaFaceLocations':len(zafter-zbefore)})
failed=[m for m in results if m['newNonManifoldEdgeLocations']or m['newZeroAreaFaceLocations']]
report={'passed':not failed,'meshes':results,'failed':failed}
(r/'defect-identity.json').write_text(json.dumps(report,indent=2)+'\n')
assert not failed,failed
print(json.dumps({'passed':True,'checkedMeshes':len(results)}))
