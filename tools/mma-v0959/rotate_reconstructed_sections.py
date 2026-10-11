"""Rotate reconstructed sections into their new tangent without shrinking.

The delivered radial vectors undergo a rigid rotation at each recovered
curve station. Native interface coordinates remain exactly constrained.
This tests radial-profile preservation, not an anatomically measured lumen.
"""
from route_tools import *
reports=[]
names=['Anterior falcine–MMA paramedian left','Anterior falcine–MMA paramedian right','Occipital mastoid–MMA petrosquamosal right','Posterior cavernous MMA–posterolateral ILT left']
for n in names:
 v,f=load(n,WORK.parent/'work-v0958/candidate');current_v,_=current(n);x=np.load(WORK/(n+'.continuation-curve.npz'));q=x['q'];r=x['r'];param=x['param'];tt=x['tt'];new=q.copy();pin=pins(n)
 if n.startswith('Anterior'):
  target,collar=(.45,1.5) if n.endswith(' left') else (.93,2.)
  weight=smooth(np.min(abs(tt[:,None]-param[pin][None,:]),axis=1)/collar)*smooth((tt[-1]-tt)/8.) if param[pin].mean()<tt.mean() else smooth(np.min(abs(tt[:,None]-param[pin][None,:]),axis=1)/collar)*smooth((tt-tt[0])/8.)
  new[:,0]+=weight*(target-q[:,0])
 elif n.startswith('Occipital'):
  tv,tf=current('brain.tentorium-cerebelli.right');tri=tv[tf];normal=np.cross(tri[:,1]-tri[:,0],tri[:,2]-tri[:,0]);cp,_=closest(locator(tv,tf[normal[:,2]<-.01]),q);weight=smooth((tt-tt[0])/3.)*smooth((tt[-1]-tt)/3.);new[:,2]+=weight*(np.minimum(cp[:,2]-r-.15,q[:,2])-q[:,2])
 else:
  new[:,0]+=.5;new[:,2]-=4.*smooth(np.min(abs(tt[:,None]-param[pin][None,:]),axis=1)/2.)
 w,oldcentre,newcentre=tube(v,q,new,param,tt);w[pin]=current_v[pin];a=assess(n,w,f)
 radial_before=np.linalg.norm(v-oldcentre,axis=1);radial_after=np.linalg.norm(w-newcentre,axis=1);free=~pin
 a.update(maximumFreeRadialProfileErrorMm=float(abs(radial_after[free]-radial_before[free]).max()),constrainedNativePinCount=int(pin.sum()),method=__doc__,node=n)
 installed=not a['neuralContacts'] and not a['newFoldPairs'] and a['nativePinsExact'] and a['maximumFreeRadialProfileErrorMm']<1e-8
 a['installed']=installed
 if installed:
  save(n,w,f,'reference-route-with-rigid-transverse-profile-rotation');np.savez_compressed(WORK/(n+'.v0959-curve.npz'),q=new,r=r,param=param,tt=tt)
 else:np.savez_compressed(OUT/(n+'.section-rotation-trial.npz'),v=w,f=f)
 reports.append(a);print(a,flush=True)
(OUT/'reconstructed-radial-profile-validation.json').write_text(json.dumps(dict(method=__doc__,results=reports,passed=all(r['installed'] for r in reports)),indent=2))
