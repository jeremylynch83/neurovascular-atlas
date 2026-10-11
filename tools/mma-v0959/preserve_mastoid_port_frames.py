"""Retain original mastoid port frames while rotating remote tube sections."""
from route_tools import *
n='Occipital mastoid–MMA petrosquamosal right';v,f=load(n,WORK.parent/'work-v0958/candidate');x=np.load(WORK/(n+'.continuation-curve.npz'));q=x['q'];tt=x['tt'];r=x['r'];param=x['param'];tv,tf=current('brain.tentorium-cerebelli.right');tri=tv[tf];normal=np.cross(tri[:,1]-tri[:,0],tri[:,2]-tri[:,0]);cp,_=closest(locator(tv,tf[normal[:,2]<-.01]),q);new=q.copy();weight=smooth((tt-tt[0])/3.)*smooth((tt[-1]-tt)/3.);new[:,2]+=weight*(np.minimum(cp[:,2]-r-.15,q[:,2])-q[:,2]);history=[]
for port in [1.5,2.,2.5,3.]:
 rotation_weight=smooth((np.minimum(tt-tt[0],tt[-1]-tt)-port)/2.)
 w,oldcentre,newcentre=tube(v,q,new,param,tt,rotation_weight);a=assess(n,w,f);a.update(originalPortFrameSupportMm=port,maximumRadialProfileErrorMm=float(abs(np.linalg.norm(w-newcentre,axis=1)-np.linalg.norm(v-oldcentre,axis=1)).max()));history.append(a);print(a,flush=True)
 if not a['neuralContacts'] and not a['newFoldPairs']:
  save(n,w,f,'deep-tentorial-reference-with-rigid-profile-and-native-port-frames');np.savez_compressed(WORK/(n+'.v0959-curve.npz'),q=new,r=r,param=param,tt=tt,rotationWeight=rotation_weight);break
(OUT/'mastoid-port-frame-validation.json').write_text(json.dumps(dict(method=__doc__,installed=not a['neuralContacts'] and not a['newFoldPairs'],history=history),indent=2))
