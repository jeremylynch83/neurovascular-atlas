from round_geometry import *
from scipy.sparse.csgraph import dijkstra
from scipy.sparse.linalg import spsolve
from scipy.sparse import diags
PARENT='ACA A5 right';v,f=mesh(PARENT);rr=rims(v,f);target=rr[2];e=np.unique(np.sort(np.vstack([f[:,[0,1]],f[:,[1,2]],f[:,[2,0]]]),1),axis=0);length=np.linalg.norm(v[e[:,0]]-v[e[:,1]],axis=1);G=coo_matrix((np.r_[length,length],(np.r_[e[:,0],e[:,1]],np.r_[e[:,1],e[:,0]])),shape=(len(v),len(v))).tocsr();dist=dijkstra(G,indices=target,min_only=True)
def shifted(delta,support):
 fixed=np.unique(np.r_[np.flatnonzero(dist>support),*[r for i,r in enumerate(rr)if i!=2]]);boundary=np.unique(np.r_[target,fixed]);free=np.setdiff1d(np.arange(len(v)),boundary);weights=1/np.maximum(length,1e-4);A=coo_matrix((np.r_[weights,weights],(np.r_[e[:,0],e[:,1]],np.r_[e[:,1],e[:,0]])),shape=G.shape).tocsr();L=diags(np.asarray(A.sum(1)).ravel())-A;u=np.zeros(len(v));u[target]=1;u[free]=spsolve(L[free][:,free],-L[free][:,boundary]@u[boundary]);p=(v+u[:,None]*np.array(delta)).astype('<f4').astype(float);return p,u
if __name__=='__main__':
 history=[];accepted=[];tissue=mesh('brain.cingulate-gyrus-and-sulcus-posterior-dorsal-part.right');sd=vtk.vtkImplicitPolyDataDistance();sd.SetInput(poly(*tissue))
 for support in [1.5,2.5,4.]:
  for dz in [-.5,-.75,-1.,-1.25]:
   p,u=shifted((0,0,dz),support);a=v[f];b=p[f];n0=np.cross(a[:,1]-a[:,0],a[:,2]-a[:,0]);n1=np.cross(b[:,1]-b[:,0],b[:,2]-b[:,0]);reversed=int(np.sum(np.einsum('ij,ij->i',n0,n1)<=0));folds=len(intersections(p,f));r={'supportMm':support,'deltaZMm':dz,'folds':folds,'reversed':reversed,'portBrainSignedDistanceRange':[min(sd.EvaluateFunction(x)for x in p[target]),max(sd.EvaluateFunction(x)for x in p[target])],'movedVertices':int(np.sum(np.linalg.norm(p-v,axis=1)>0))};history.append(r);print(json.dumps(r),flush=True)
   if not folds and not reversed and r['portBrainSignedDistanceRange'][0]>.1:
    np.savez(D.parent/('port-'+str(support)+'-'+str(abs(dz))+'.npz'),v=p,f=f);accepted.append(r)
 (D.parent/'port-shorten-trials.json').write_text(json.dumps({'candidates':accepted,'trials':history},indent=2)+'\n')
