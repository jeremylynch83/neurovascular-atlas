"""Refine reference collars while retaining rigid transverse section profiles."""
from route_tools import *
reports=[]
n='Anterior falcine–MMA paramedian left';v,f=load(n,WORK.parent/'work-v0958/candidate');initial,_=current(n);x=np.load(WORK/(n+'.continuation-curve.npz'));q=x['q'];tt=x['tt'];param=x['param'];r=x['r'];pin=pins(n);history=[];installed=False
for target in [.45,.5,.55,.6]:
 for collar in [2.,2.5,3.,4.,5.]:
  new=q.copy();weight=smooth(np.min(abs(tt[:,None]-param[pin][None,:]),axis=1)/collar)*smooth((tt[-1]-tt)/8.);new[:,0]+=weight*(target-q[:,0]);w,oldcentre,newcentre=tube(v,q,new,param,tt);w[pin]=initial[pin];a=assess(n,w,f);a.update(targetX=target,collarMm=collar);history.append(a);print(n,a,flush=True)
  if not a['neuralContacts'] and not a['newFoldPairs'] and a['nativePinsExact']:
   save(n,w,f,'reference-route-with-rigid-transverse-profile-rotation');np.savez_compressed(WORK/(n+'.v0959-curve.npz'),q=new,r=r,param=param,tt=tt);installed=True;break
 if installed:break
reports.append(dict(node=n,installed=installed,history=history))
n='Occipital mastoid–MMA petrosquamosal right';v,f=load(n,WORK.parent/'work-v0958/candidate');initial,_=current(n);x=np.load(WORK/(n+'.continuation-curve.npz'));q=x['q'];tt=x['tt'];param=x['param'];r=x['r'];tv,tf=current('brain.tentorium-cerebelli.right');tri=tv[tf];norm=np.cross(tri[:,1]-tri[:,0],tri[:,2]-tri[:,0]);cp,_=closest(locator(tv,tf[norm[:,2]<-.01]),q);history=[];installed=False
for collar in [2.,2.5,3.,3.5,4.]:
 for margin in [.15,.3,.45,.6]:
  new=q.copy();weight=smooth((tt-tt[0])/collar)*smooth((tt[-1]-tt)/collar);new[:,2]+=weight*(np.minimum(cp[:,2]-r-margin,q[:,2])-q[:,2]);w,oldcentre,newcentre=tube(v,q,new,param,tt);a=assess(n,w,f);a.update(collarMm=collar,marginMm=margin);history.append(a);print(n,a,flush=True)
  if not a['neuralContacts'] and not a['newFoldPairs']:
   save(n,w,f,'reference-route-with-rigid-transverse-profile-rotation');np.savez_compressed(WORK/(n+'.v0959-curve.npz'),q=new,r=r,param=param,tt=tt);installed=True;break
 if installed:break
reports.append(dict(node=n,installed=installed,history=history))
(OUT/'rotated-collar-refinement.json').write_text(json.dumps(dict(method=__doc__,results=reports),indent=2))
