"""Strict topology/self-contact checks of the single exterior wall, plus regional contacts."""
from common import *
from scipy.spatial import cKDTree
from scipy.sparse import coo_matrix
from scipy.sparse.csgraph import connected_components
x=np.load(OUT/'network.npz');v=x['v'];f=x['f'];t=v[f].astype(float)
e=np.concatenate([f[:,[0,1]],f[:,[1,2]],f[:,[2,0]]]);sorted_e=np.sort(e,axis=1);ue,inv,count=np.unique(sorted_e,axis=0,return_inverse=True,return_counts=True);sign=np.where(e[:,0]<e[:,1],1,-1);direction=np.bincount(inv,weights=sign);g=coo_matrix((np.ones(len(e)),(e[:,0],e[:,1])),shape=(len(v),len(v))).tocsr();components=connected_components(g,directed=False)[0]
area=np.linalg.norm(np.cross(t[:,1]-t[:,0],t[:,2]-t[:,0]),axis=1);topology=dict(boundaryEdges=int(np.sum(count==1)),nonManifoldEdges=int(np.sum(count>2)),inconsistentlyOrientedEdges=int(np.sum(direction!=0)),connectedComponents=components,degenerateTriangles=int(np.sum(area<1e-10)),duplicateTriangles=int(len(f)-len(np.unique(np.sort(f,axis=1),axis=0))),vertices=len(v),triangles=len(f),signedVolumeMm3=float(np.einsum('ij,ij->i',t[:,0],np.cross(t[:,1],t[:,2])).sum()/6))
print('Topology',topology,flush=True)
# Exact broad-phase boxes, followed by VTK triangle intersection.
lo=t.min(1);hi=t.max(1);pairs=[]
cent=t.mean(1);radius=np.linalg.norm(t-cent[:,None],axis=2).max(1);tree=cKDTree(cent)
for start in range(0,len(f),96):
 aa=np.arange(start,min(start+96,len(f)));near=tree.query_ball_point(cent[aa],radius[aa]+radius.max());bb=np.concatenate(near);aa=np.repeat(aa,[len(k) for k in near]);keep=aa<bb;aa=aa[keep];bb=bb[keep]
 keep=np.all(lo[aa]<=hi[bb]+1e-8,axis=1)&np.all(lo[bb]<=hi[aa]+1e-8,axis=1)&(np.linalg.norm(cent[aa]-cent[bb],axis=1)<=radius[aa]+radius[bb]);aa=aa[keep];bb=bb[keep]
 keep=~np.any(f[aa,:,None]==f[bb,None,:],axis=(1,2));aa=aa[keep];bb=bb[keep]
 for a,b in zip(aa,bb):
  if vtk.vtkTriangle.TrianglesIntersect(*t[a],*t[b]):pairs.append((int(a),int(b)))
print('Non-adjacent intersections',len(pairs),flush=True)
names=json.loads((WORK/'connected-nodes.json').read_text());checks=[];unexpected=[]
def collision(a,b):
 c=vtk.vtkCollisionDetectionFilter();c.SetInputData(0,a);c.SetInputData(1,b);tr=vtk.vtkTransform();c.SetTransform(0,tr);c.SetTransform(1,tr);c.SetCellTolerance(0);c.SetCollisionModeToHalfContacts();c.Update()
 if not c.GetNumberOfContacts():return np.empty((0,3))
 return vtk_to_numpy(c.GetContactsOutput().GetPoints().GetData()).copy()
keys=lambda a:np.ascontiguousarray(a.astype('<f4')).view('V12').ravel()
source=np.concatenate([load(n)[0] for n in names]);sourcekeys=keys(source)
for row in META:
 n=row['name']
 if n in names:continue
 a,b=load(n)
 if np.any(a.min(0)>v.max(0)) or np.any(a.max(0)<v.min(0)):continue
 points=collision(poly(v,f),poly(a,b))
 if not len(points):continue
 shared=a[np.isin(keys(a),sourcekeys)] if row['file']=='venous.glb' else np.empty((0,3))
 # Expected original connections are reviewed separately from exterior obstacles.
 d=cKDTree(shared).query(points)[0] if len(shared) else np.full(len(points),np.inf)
 bad=points[d>2.5];r=dict(target=n,asset=row['file'],contactPoints=len(points),originalAttachmentVertices=len(shared),unexpectedContactPoints=len(bad),contactBounds=[points.min(0).tolist(),points.max(0).tolist()]);checks.append(r)
 if len(bad):unexpected.append(r)
 print('Contact',r,flush=True)
report=dict(release='0.9.48',topology=topology,selfIntersectionPairs=pairs,selfIntersectionCount=len(pairs),contacts=checks,unexpectedContacts=unexpected,networkWatertight=not topology['boundaryEdges'] and not topology['nonManifoldEdges'] and not topology['inconsistentlyOrientedEdges'] and components==1,scope='One exterior network wall, assembled across disjoint labelled patches. Original attachments are separately identified within 2.5 mm of exact baseline shared vertices; all other artery, vein, brain and bone contacts are unexpected.')
report['passed']=report['networkWatertight'] and not pairs and not unexpected and not topology['degenerateTriangles'] and not topology['duplicateTriangles'];(OUT/'quality.json').write_text(json.dumps(report,indent=2)+'\n')
if not report['passed']:sys.exit(1)
