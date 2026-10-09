"""Move the acoustic artery along a sampled clear path with rotated tube walls."""
from common import *
from scipy.interpolate import CubicSpline,PchipInterpolator
from scipy.ndimage import gaussian_filter1d
from scipy.spatial.transform import Rotation,Slerp

def acoustic_transport(side):
 name='Labyrinthine '+side;v,f=load(name);ys=np.linspace(-76.09,-72.05,100);centres=[]
 for y in ys:
  p=section(v,f,1,y);centres.append((p.min(0)+p.max(0))/2)
 old=np.array(centres);old=gaussian_filter1d(old,1.5,axis=0);old[:,1]=ys;native=old.copy();fit=ys<-73.8
 for axis in [0,2]:old[:,axis]=np.polyval(np.polyfit(ys[fit]+75,old[fit,axis],2),ys+75)
 old=native+(old-native)*smooth((ys+74.7)/.8)[:,None]
 record=json.loads((WORK/'acoustic-paths.json').read_text())[side];new=np.array(record['points']);new=gaussian_filter1d(new,1.,axis=0);new[0]=old[0];new[-1]=np.array(record['nearestClearEndpoint'])
 arc=np.r_[0,np.cumsum(np.linalg.norm(np.diff(new,axis=0),axis=1))];t=np.linspace(0,1,len(old));cut=-73.3;tc=(cut-ys[0])/(ys[-1]-ys[0]);rEnd=Rotation.from_rotvec([0,np.deg2rad(55)*(1 if side=='right' else -1),0]);end=np.array(record['nearestClearEndpoint']);end[0]=(1 if side=='right' else -1)*31.8;end[2]=57.;distalScale=.65;oi=CubicSpline(ys,old);cutpoint=end+distalScale*rEnd.apply(oi(cut)-old[-1]);nearest=np.argmin(np.linalg.norm(new-cutpoint,axis=1));new=new[:nearest+1];new[-1]=cutpoint;arc=np.r_[0,np.cumsum(np.linalg.norm(np.diff(new,axis=0),axis=1))]
 ci=CubicSpline(arc/arc[-1],new);target=ci(np.minimum(t/tc,1));late=ys>=cut;target[late]=end+distalScale*rEnd.apply(old[late]-old[-1])
 w=smooth(t/.12);target=old+(target-old)*w[:,None]
 np.savetxt(WORK/('transport-'+side+'.csv'),np.c_[ys,old,target],delimiter=',');ta=np.gradient(old,axis=0);tb=np.gradient(target,axis=0);ta/=np.linalg.norm(ta,axis=1)[:,None];tb/=np.linalg.norm(tb,axis=1)[:,None];axis=np.cross(ta,tb);ss=np.linalg.norm(axis,axis=1);angle=np.arctan2(ss,np.einsum('ij,ij->i',ta,tb));axis/=np.maximum(ss[:,None],1e-12);rv=axis*angle[:,None]*smooth(t/.08)[:,None];rv[late]=rEnd.as_rotvec();rot=Rotation.from_rotvec(rv);blend=smooth((ys-(cut-.8))/.8);rot=Rotation.from_quat(np.array([Slerp([0,1],Rotation.concatenate([r,rEnd]))([b]).as_quat()[0] for r,b in zip(rot,blend)]));interp=Slerp(ys,rot);ni=CubicSpline(ys,target)
 def fn(v):
  y=np.clip(v[:,1],ys[0],ys[-1]);local=v-oi(y);scale=1-(1-distalScale)*smooth((y-(cut-.8))/.8);q=ni(y)+scale[:,None]*interp(y).apply(local);late=v[:,1]>=cut;q[late]=end+distalScale*rEnd.apply(v[late]-old[-1]);q[v[:,1]<=ys[0]]=v[v[:,1]<=ys[0]];return q
 return fn
