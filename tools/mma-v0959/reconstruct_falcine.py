"""Bounded intrafalcine reconstruction with unchanged native attachment points.

The source falx midplane is x=0.5 mm. Paired routes retain their respective
side of this plane. Failed trials are recorded and never installed.
"""
from route_tools import *
reports=[]
for prefix in ['ACA falcine–MMA falcine','Anterior falcine–MMA paramedian']:
 for side,sign in [('left',-1),('right',1)]:
  n=prefix+' '+side;v,f=current(n);x=np.load(WORK/(n+'.continuation-curve.npz'));q=x['q'];tt=x['tt'];param=x['param'];pin=pins(n);history=[];installed=False
  for collar in [2.,3.,4.,5.,6.,8.]:
   anchors=param[pin];weight=smooth(np.min(abs(tt[:,None]-anchors[None,:]),axis=1)/collar) if len(anchors) else np.ones(len(tt))
   new=q.copy();new[:,0]+=weight*(.5+sign*.43-q[:,0])
   if prefix.startswith('Anterior'):
    # The convexity end is not a native shared port. Keep its distal source
    # connection until that separate endpoint has been reconstructed.
    distal=tt[-1] if param[pin].mean()<tt.mean() else tt[0]
    taper=smooth(abs(tt-distal)/8.)
    new[:,0]=q[:,0]+(new[:,0]-q[:,0])*taper
   delta=np.column_stack([np.interp(param,tt,new[:,k]-q[:,k]) for k in range(3)])
   w=v+delta;w[pin]=v[pin]
   result=assess(n,w,f);result['collarMm']=collar;history.append(result);print(n,result,flush=True)
   if not result['neuralContacts'] and not result['newFoldPairs'] and result['nativePinsExact']:
    save(n,w,f,'paired-falx-midplane-collateral-reconstruction');installed=True;break
  reports.append(dict(node=n,installed=installed,history=history))
(OUT/'falcine-reconstruction.json').write_text(json.dumps(dict(method=__doc__,results=reports),indent=2))
