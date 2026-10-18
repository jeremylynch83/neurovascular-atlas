from parent_adjust import *
from loft import directed
from affected_checks import local_contacts,affected_intersections
q=original[directed(original,faces,target)];x=q-q.mean(0);axis=-np.cross(x,np.roll(x,-1,axis=0)).sum(0);axis/=np.linalg.norm(axis);p=adjust(axis*.15,2.);b,bf=mesh('bone.sphenoid');sd=vtk.vtkImplicitPolyDataDistance();sd.SetInput(poly(b,bf));moved=np.flatnonzero(np.any(p!=original,1));previous=np.array([sd.EvaluateFunction(x)for x in original]);protected=np.unique(np.r_[rr[0],rr[1],rr[2]])
for step in range(3):
 for i in moved:
  if i in protected:continue
  value=sd.EvaluateFunction(p[i]);margin=min(.002,float(np.linalg.norm(p[i]-original[i]))*.05)
  if previous[i]<0 and value<previous[i]+margin:
   grad=[0.,0.,0.];sd.EvaluateGradient(p[i],grad);p[i]+=np.array(grad)*(previous[i]+margin-value)/np.linalg.norm(grad)
 p=p.astype('<f4').astype(float)
selected=np.flatnonzero(np.any(np.isin(faces,moved),1));active=set(map(int,moved))-set(map(int,protected));bary=np.array([[1,0,0],[0,1,0],[0,0,1],[1/3,1/3,1/3],[.5,.5,0],[0,.5,.5],[.5,0,.5]])
for iteration in range(12):
 constraints=[]
 for face in faces[selected]:
  for alpha in bary:
   source=alpha@original[face];current=alpha@p[face];oldvalue=sd.EvaluateFunction(source);value=sd.EvaluateFunction(current);goal=min(oldvalue,0.);deficit=goal-value
   if deficit>2e-6:constraints.append((deficit,face.copy(),alpha.copy()))
 if not constraints:break
 for _,face,alpha in sorted(constraints,key=lambda x:-x[0]):
  current=alpha@p[face];goal=min(sd.EvaluateFunction(alpha@original[face]),0.);deficit=goal-sd.EvaluateFunction(current)
  if deficit<=1e-6:continue
  weights=alpha*np.array([int(i)in active for i in face]);denom=np.dot(weights,weights)
  if denom<1e-12:continue
  grad=[0.,0.,0.];sd.EvaluateGradient(current,grad);direction=np.array(grad)/np.linalg.norm(grad)
  for i,weight in zip(face,weights):p[i]+=weight/denom*(deficit+3e-6)*direction
 p=p.astype('<f4').astype(float)
a=original[faces[selected]];c=p[faces[selected]]
def samples(t):return np.vstack([t.reshape(-1,3),t.mean(1),(t[:,0]+t[:,1])/2,(t[:,1]+t[:,2])/2,(t[:,2]+t[:,0])/2])
before=np.array([sd.EvaluateFunction(x)for x in samples(a)]);after=np.array([sd.EvaluateFunction(x)for x in samples(c)]);increase=float(np.max(np.maximum(-after,0)-np.maximum(-before,0)));newinside=int(np.sum((before>=0)&(after< -1e-5)));folds=intersections(p,faces)-intersections(original,faces);aa=original[faces];cc=p[faces];n0=np.cross(aa[:,1]-aa[:,0],aa[:,2]-aa[:,0]);n1=np.cross(cc[:,1]-cc[:,0],cc[:,2]-cc[:,0]);rev=int(np.sum((np.einsum('ij,ij->i',n0,n1)<=0)&(np.linalg.norm(n0,axis=1)>1e-10)));row={'support':2.,'axialDisplacementMm':.15,'maxTotalDisplacementMm':float(np.linalg.norm(p-original,axis=1).max()),'newSelfIntersections':len(folds),'reversedFaces':rev,'minimumPortBoneClearanceMm':min(sd.EvaluateFunction(x)for x in p[target]),'newBoneInsideSamples':newinside,'maxBonePenetrationIncreaseMm':increase,'boneContactsBefore':local_contacts(original,faces,b,bf),'boneContactsAfter':local_contacts(p,faces,b,bf),'maxLocalSampledDepthBeforeMm':float(np.maximum(-before,0).max()),'maxLocalSampledDepthAfterMm':float(np.maximum(-after,0).max())};print(row,flush=True)
assert not folds and not rev and not newinside and increase<1e-5,row
np.savez(D.parent/'fitted-parent.npz',v=p,f=faces);(D.parent/'fitted-parent.json').write_text(json.dumps(row,indent=2)+'\n')
