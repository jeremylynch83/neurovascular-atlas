from common import *
from scipy.sparse import coo_matrix
from scipy.sparse.csgraph import connected_components
rows=[]
for side in ['right','left']:
 n='vein.middle_meningeal.'+side;v,f=load(n,OUT);_,inv=np.unique(v,axis=0,return_inverse=True);f=inv[f];e,count=np.unique(np.sort(np.concatenate([f[:,[0,1]],f[:,[1,2]],f[:,[2,0]]]),axis=1),axis=0,return_counts=True);g=coo_matrix((np.ones(len(e)),(e[:,0],e[:,1])),shape=(inv.max()+1,inv.max()+1)).tocsr();nc,cc=connected_components(g,directed=False);row=dict(node=n,components=nc,componentVertices=np.bincount(cc).tolist(),boundaryEdges=int(np.sum(count==1)),nonManifoldEdges=int(np.sum(count>2)),vertices=len(v),triangles=len(f));rows.append(row);print(row)
(OUT/'new-vein-topology.json').write_text(json.dumps(rows,indent=2)+'\n')
