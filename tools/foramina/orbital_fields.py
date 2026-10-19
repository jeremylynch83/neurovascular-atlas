import numpy as np
from scipy.interpolate import PchipInterpolator
AE={'x':[0,5.5,6.5,8.5,10.5,12.5,14.5,17,21],'dy':[0,0,3,7,6,3,1,0,0],'dz':[0,0,-2,-6,-5,-3,-1,0,0]}
PE={'x':[0,7.5,8,10,12,14,18,26],'dy':[0,0,.3,1,.5,0,0,0],'dz':[0,0,-1,-3.5,-2.5,-1,0,0]}
SOF={'z':[0,44,46,50,56,62,66,67.5,72,150],'dx':[0,0,.4,1.5,1,0,0,0,0,0],'dy':[0,0,2,6,7,4,1,0,0,0]}
def warp(points,sid):
 p=np.array(points,float).reshape(-1,3);q=p.copy()
 if not len(p):return q
 if 'anterior_ethmoidal_'in sid or 'posterior_ethmoidal_'in sid:
  r=AE if 'anterior_ethmoidal_'in sid else PE;x=np.clip(abs(p[:,0]),r['x'][0],r['x'][-1]);q[:,1]+=PchipInterpolator(r['x'],r['dy'])(x);q[:,2]+=PchipInterpolator(r['x'],r['dz'])(x)
 elif 'deep_recurrent_ophthalmic' in sid:
  guard=16.1 if sid.endswith('right')else 15.15
  x=np.clip(abs(p[:,0]),0,50);q[:,1]+=PchipInterpolator([0,guard,guard+.5,18.4,20,21.2,50],[0,0,1.5,4,1.5,0,0])(x)
 elif 'artery_of_superior_orbital_fissure' in sid:
  z=np.clip(p[:,2],SOF['z'][0],SOF['z'][-1]);g=np.clip((p[:,1]+29)/3,0,1);g=g*g*(3-2*g);root=np.clip((p[:,2]-44.7)/1.5,0,1);g*=root*root*(3-2*root);q[:,0]+=np.sign(p[:,0])*PchipInterpolator(SOF['z'],SOF['dx'])(z)*g;q[:,1]+=PchipInterpolator(SOF['z'],SOF['dy'])(z)*g
 return q
