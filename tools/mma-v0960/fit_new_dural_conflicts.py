"""Constrain newly exposed dural arterial bodies below the cerebral reference.

Keep native end ports fixed and rotate the delivered radial vectors rather
than compressing their profiles. Every float32 trial must clear neural
surfaces and eligible closed parcels, add no folds and add no arterial,
venous or bone contact pairs. Rejected trials are diagnostic only.
"""
from trial_gates import *
import importlib.util
from types import SimpleNamespace
spec=importlib.util.spec_from_file_location('extract',Path(__file__).parents[1]/'brainstem-quality-v0948/extract_curves.py');ex=importlib.util.module_from_spec(spec);spec.loader.exec_module(ex)
names=['Jugular sigmoid branch','Davidoff and Schechter artery left','Occipital tentorial–PCA dural left']
for n in names:
 v,f=meshes[n];q,r,param,tt=ex.extract(SimpleNamespace(v=v,f=f));pin=pins(n);installed=False
 np.savez_compressed(WORK/(n+'.v0960-before-fit-curve.npz'),q=q,r=r,param=param,tt=tt)
 for collar in [2.,3.,4.,6.,8.]:
  anchors=param[pin];enddist=np.minimum(tt-tt[0],tt[-1]-tt)
  weight=smooth(enddist/collar)
  if len(anchors):weight*=smooth(np.min(abs(tt[:,None]-anchors[None,:]),axis=1)/collar)
  weight*=smooth((-q[:,1]-75.)/10.)
  for amount in [.5,1.,1.5,2.,2.5,3.,4.,5.]:
   new=q.copy();new[:,2]-=amount*weight
   if attempt(n,v,f,q,new,param,tt,r,dict(endCollarMm=collar,inferiorShiftMm=amount,rotationPortMm=1.)):installed=True;break
  if installed:break
 print('FINISHED',n,'installed',installed,flush=True)
(OUT/'new-dural-conflict-trials-v0960.json').write_text(json.dumps(dict(method=__doc__,results=history),indent=2))
