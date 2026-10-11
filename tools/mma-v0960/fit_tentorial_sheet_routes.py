"""Fit tentorial collateral bodies to the actual sheet, not its height alone.

The previous height-only projection retained points outside the anterior
margin of the tentorial sheet. Use the closest inferior-sheet coordinates
in all three axes, preserving delivered end ports, free radial profiles,
native shared coordinates and the complete obstacle gates.
"""
from trial_gates import *
from scipy.ndimage import gaussian_filter1d
for n in ['MMA–tentorial marginal left','MMA–tentorial marginal right','Occipital mastoid–MMA petrosquamosal left']:
 v,f=meshes[n];a=np.load(WORK/(n+'.continuation-curve.npz'));q=a['q'];tt=a['tt'];param=a['param'];r=a['r'];side='left' if n.endswith('left') else 'right'
 tv,tf=meshes['brain.tentorium-cerebelli.'+side];tri=tv[tf];nn=np.cross(tri[:,1]-tri[:,0],tri[:,2]-tri[:,0]);lc=locator(tv,tf[nn[:,2]<-.01]);cp,_=closest(lc,q);installed=False
 for collar in [2.,3.,4.,5.,6.,8.]:
  for gap in [.15,.4,.8]:
   goal=gaussian_filter1d(cp,1.5,axis=0);goal[:,2]-=r+gap;weight=smooth((tt-tt[0])/collar)*smooth((tt[-1]-tt)/collar);new=q+weight[:,None]*(goal-q)
   if attempt(n,v,f,q,new,param,tt,r,dict(endCollarMm=collar,deepSheetClearanceMm=gap,rotationPortMm=1.,projection='all-three-coordinates')):installed=True;break
  if installed:break
 print('FINISHED',n,'installed',installed,flush=True)
(OUT/'tentorial-sheet-route-trials-v0960.json').write_text(json.dumps(dict(method=__doc__,results=history),indent=2))
