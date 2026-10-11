"""Fit residual bodies to modelled dural references, retaining native ends.

These are teaching reconstructions. Surface clearance is distinct from
volumetric containment, anatomical acceptance, and calibre validation.
"""
from route_tools import *
from scipy.ndimage import gaussian_filter1d
reports=[]
for side in ['left','right']:
 n='Occipital mastoid–MMA petrosquamosal '+side;v,f=current(n);x=np.load(WORK/(n+'.continuation-curve.npz'));q=x['q'];param=x['param'];tt=x['tt'];r=x['r'];tv,tf=current('brain.tentorium-cerebelli.'+side);tri=tv[tf];normal=np.cross(tri[:,1]-tri[:,0],tri[:,2]-tri[:,0]);cp,_=closest(locator(tv,tf[normal[:,2]<-.01]),q);history=[];installed=False
 for collar in [2.,3.,4.,5.,6.]:
  weight=smooth((tt-tt[0])/collar)*smooth((tt[-1]-tt)/collar);new=q.copy();new[:,2]+=weight*(np.minimum(cp[:,2]-r-.15,q[:,2])-q[:,2]);delta=np.column_stack([np.interp(param,tt,new[:,k]-q[:,k]) for k in range(3)]);w=v+delta;w[pins(n)]=v[pins(n)];result=assess(n,w,f);result['endCollarMm']=collar;history.append(result);print(n,result,flush=True)
  if not result['neuralContacts'] and not result['newFoldPairs'] and result['nativePinsExact']:
   save(n,w,f,'deep-tentorial-reference-mastoid-collateral');installed=True;break
 reports.append(dict(node=n,installed=installed,history=history))
n='Anterior falcine–MMA paramedian left';v,f=current(n);x=np.load(WORK/(n+'.continuation-curve.npz'));q=x['q'];tt=x['tt'];param=x['param'];r=x['r'];pin=pins(n);bv,bf=current('bone.frontal');bl=locator(bv,bf)
history=[];installed=False
for support in [10.,12.,15.,18.,20.]:
 new=q.copy();weight=smooth(np.min(abs(tt[:,None]-param[pin][None,:]),axis=1)/2.)*smooth((tt[-1]-tt)/8.);new[:,0]+=weight*(.07-q[:,0])
 roof=[]
 for p in new:
  a=p.copy();b=p.copy();a[2]=140.;b[2]=190.;t=vtk.reference(0.);hit=[0.,0.,0.];pc=[0.,0.,0.];sub=vtk.reference(0);cid=vtk.reference(0)
  found=bl.IntersectWithLine(a,b,1e-7,t,hit,pc,sub,cid);roof.append(hit[2] if found else p[2])
 blend=smooth((tt-(tt[-1]-support))/5.)*smooth((tt[-1]-tt)/4.)
 new[:,2]+=blend*(np.maximum(np.array(roof)-r-.20,q[:,2])-q[:,2])
 delta=np.column_stack([np.interp(param,tt,new[:,k]-q[:,k]) for k in range(3)]);w=v+delta;w[pin]=v[pin];result=assess(n,w,f);result['convexityTransitionSupportMm']=support;history.append(result);print(n,result,flush=True)
 if not result['neuralContacts'] and not result['newFoldPairs'] and result['nativePinsExact']:
  save(n,w,f,'falx-to-inner-frontal-reference-collateral');installed=True;break
reports.append(dict(node=n,installed=installed,history=history))
# Combine a coherent medial shift at the left cavernous junction with a
# downward body correction. The parent collar remains in the same frame.
n='Posterior cavernous MMA–posterolateral ILT left';parent='MMA posterior cavernous left';v,f=current(n);pv,pf=current(parent);ii,jj=matches(n,parent);parentpin=pins(parent);parentpin[jj]=False;x=np.load(WORK/(n+'.continuation-curve.npz'));param=x['param'];tt=x['tt'];history=[];installed=False
for medial in [.5,.75,1.,1.5,2.]:
 for inferior in [1.,1.5,2.,2.5,3.,4.]:
  distance=np.min(abs(param[:,None]-param[ii][None,:]),axis=1);w=v+np.array([medial,0.,0.]);w[:,2]-=inferior*smooth(distance/2.);w[ii]=v[ii]+[medial,0.,0.]
  d,ix=cKDTree(pv[jj]).query(pv);p=pv+(1-smooth(d/4.))[:,None]*(w[ii]-pv[jj])[ix];p[parentpin]=pv[parentpin];p[jj]=w[ii]
  a=assess(n,w,f);b=assess(parent,p,pf);row=dict(medialMm=medial,inferiorMm=inferior,collateral=a,parent=b);history.append(row);print(n,row,flush=True)
  if not a['neuralContacts'] and not a['newFoldPairs'] and not b['neuralContacts'] and not b['newFoldPairs']:
   save(n,w,f,'deep-cavernous-body-and-shared-junction-reconstruction');save(parent,p,pf,'coherent-cavernous-attachment-collar');installed=True;break
 if installed:break
reports.append(dict(node=n,parent=parent,installed=installed,history=history))
(OUT/'reference-body-reconstruction.json').write_text(json.dumps(dict(method=__doc__,results=reports),indent=2))
