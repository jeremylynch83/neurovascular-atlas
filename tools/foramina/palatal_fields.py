"""Local v0.9.138 nasal/palatal arterial fit in RAS millimetres.

Apply identically to connected display parts, closing surfaces and flow guides.
"""
import numpy as np
from scipy.interpolate import PchipInterpolator

def ramp(v,a,b):
 t=np.clip((np.asarray(v)-a)/(b-a),0,1);return t*t*(3-2*t)
def band(v,a,b,c,d):return ramp(v,a,b)*(1-ramp(v,c,d))
def warp(points):
 q=np.array(points,float).reshape(-1,3).copy()
 if not len(q):return q
 x,y,z=q.T.copy();ax=abs(x)
 # Descending shaft: retain the maxillary mouths, fit the palatine junction.
 dx=PchipInterpolator([0,12,16,20,25,30,36,40,43,100],[0,0,1,1.8,0,-2.1,-1.8,0,0,0])(np.clip(z,0,100))
 q[:,0]+=np.tanh(x/2)*dx*band(y,-27,-23,-18,-15)*band(ax,8,14,26,34)
 x,y,z=q.T.copy();q[:,1]+=3.8*band(z,25,30,35,40)*band(y,-28,-23,-20,-10)*band(abs(x),10,14,25,31)
 x,y,z=q.T.copy();q[:,1]+=2.5*band(abs(x),12,16,23,27)*band(y,-32,-28,-24,-18)*band(z,37,40,43,46)
 # Bring the hard-palate arteries closer to its inferior surface.
 x,y,z=q.T.copy();lift=PchipInterpolator([-100,-19,-16,-13,-7,5,9,13,16,100],[0,0,1.4,3.3,5.1,5,4,1.5,0,0])(np.clip(y,-100,100))
 q[:,2]+=lift*ramp(x,-1,3)*(1-ramp(z,18,29))*band(abs(x),0,.8,22,28)
 # Septal mucosal sheet alongside the asymmetric delivered vomer.
 x,y,z=q.T.copy();target=PchipInterpolator([-40,-20,-16,-13,-10,-8,-6,-3,0,4,11,20,40],[-40,-20,-16,-11,-3,-.6,-.2,.3,2.4,6.5,11,20,40])(np.clip(x,-40,40))
 q[:,0]+=(target-x)*band(y,-12,-8,11,18)*band(z,23,27,44,50)
 # Lateral nasal branches pass medial to the lateral nasal wall.
 x,y,z=q.T.copy();q[:,0]-=2.2*np.tanh(x/2)*band(abs(x),8,13,18,24)*band(y,-21,-14,17,24)*band(z,23,28,43,49)
 x,y,z=q.T.copy();target=PchipInterpolator([-40,-30,-20,-14,-10,-7,-4,0,5.5,8,12,16,22,30,40],[-40,-30,-20,-6,-4,-3.4,-2,0,5.5,6.3,6.7,9,20,30,40])(np.clip(x,-40,40))
 q[:,0]+=(target-x)*band(y,-11,-5,20,25)*band(z,23,28,37,41)
 # Turn medially at the sphenopalatine entry before travelling anteriorly.
 x,y,z=q.T.copy();q[:,1]-=2.2*band(abs(x),8,12,18,23)*band(y,-21,-16,-10,-5)*band(z,35,40,46,51)
 x,y,z=q.T.copy();q[:,2]-=1.7*band(y,-3,0,6,10)*band(abs(x),0,.5,6,10)*ramp(z,39,43)
 x,y,z=q.T.copy();q[:,0]-=.6*band(x,-1.5,0,1.5,3)*band(y,-4,-2,1,4)*band(z,38,40,43,46)
 return incisive_warp(q)

def concha_warp(points,side):
 q=np.array(points,float).copy();x,y,z=q.T.copy()
 if side=='right':q[:,0]+=2.2*(1-ramp(x,6,13))*band(y,-18,-10,16,22)*band(z,20,25,39,44)
 else:q[:,0]-=2.2*ramp(x,-12,-6)*band(y,-18,-10,16,22)*band(z,20,25,39,44)
 return q

def incisive_warp(points):
 q=np.array(points,float).copy();x,y,z=q.T.copy();q[:,1]-=3.5*band(abs(x),0,.5,4,7)*band(y,9,16,22,30)*band(z,14,18,23,27)
 return q
