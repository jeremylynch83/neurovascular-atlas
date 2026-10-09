"""Connected component and oriented closed-surface volume checks."""
from common import *
from scipy.sparse import coo_matrix
from scipy.sparse.csgraph import connected_components
rev=json.loads((OUT/'revision.json').read_text());stats=[]
for node in rev['newLabels']:
 v,f=load(node,OUT);a=np.concatenate([f[:,0],f[:,1],f[:,2]]);b=np.concatenate([f[:,1],f[:,2],f[:,0]]);g=coo_matrix((np.ones(len(a)),(a,b)),shape=(len(v),len(v))).tocsr();cc,_=connected_components(g,directed=False);volume=np.sum(np.einsum('ij,ij->i',v[f[:,0]],np.cross(v[f[:,1]],v[f[:,2]])))/6;stats.append(dict(node=node,connectedComponents=int(cc),signedVolumeMm3=float(volume)))
passed=all(s['connectedComponents']==1 and s['signedVolumeMm3']>0 for s in stats);(OUT/'new-surface-components.json').write_text(json.dumps(dict(release='0.9.51',passed=passed,results=stats),indent=2)+'\n');assert passed;print('All new surfaces connected with positive oriented volume')
