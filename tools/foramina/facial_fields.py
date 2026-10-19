"""Reference-guided v0.9.139 facial and mandibular arterial adjustments."""
import numpy as np
from scipy.interpolate import PchipInterpolator

def ramp(v,a,b):
 t=np.clip((np.asarray(v)-a)/(b-a),0,1);return t*t*(3-2*t)
def band(v,a,b,c,d):return ramp(v,a,b)*(1-ramp(v,c,d))
def warp(points):
 q=np.array(points,float).reshape(-1,3).copy()
 if not len(q):return q
 x,y,z=q.T.copy();drop=PchipInterpolator([-100,-15,-8,-3,1,5,10,14,18,100],[0,0,.8,3,3,2.8,3,.5,0,0])(np.clip(y,-100,100));q[:,2]-=drop*band(z,-35,-29,-15,-9)*band(abs(x),0,2,39,45)
 # The mylohyoid artery remains extrabony on the medial mandibular side.
 x,y,z=q.T.copy();q[:,0]-=1.6*np.tanh(x/2)*band(abs(x),10,14,21,24)*band(y,-23,-17,-5,0)*band(z,-24,-20,-10,-4)
 # Supraorbital passage: retain the ophthalmic origin and scalp endpoints.
 x,y,z=q.T.copy();w=band(abs(x),21,26,35,42)*band(y,0,12,30,46)*band(z,70,76,84,100);q[:,1]-=3*w;q[:,2]+=3.2*w
 # Supratrochlear passage, with a gentle fit around the medial frontal rim.
 x,y,z=q.T.copy();w=band(abs(x),5,9,16,22)*band(y,15,28,34,55)*band(z,60,65,74,92);q[:,1]-=3*w;q[:,2]+=2.5*w
 return q
