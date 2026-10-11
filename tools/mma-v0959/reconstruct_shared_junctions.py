"""Move anatomically misplaced dural junctions together with their parents.

Every native shared coordinate receives the same displacement on both
labels. Other native junctions are locked. Trials require zero collateral
neural surface contacts, no additional parent contacts, and no new folds.
"""
from route_tools import *
def matches(n,other):
 a,_=load(n);b,_=load(other);lookup={bytes(k):i for i,k in enumerate(np.ascontiguousarray(a.astype('<f4')).view('V12').ravel())}
 jj=[];ii=[]
 for j,k in enumerate(np.ascontiguousarray(b.astype('<f4')).view('V12').ravel()):
  if bytes(k) in lookup:jj.append(j);ii.append(lookup[bytes(k)])
 return np.array(ii,int),np.array(jj,int)
reports=[]
for side,sign in [('left',-1),('right',1)]:
 n='ACA falcine–MMA falcine '+side;parent='ACA falcine branch '+side
 v,f=current(n);pv,pf=current(parent);x=np.load(WORK/(n+'.continuation-curve.npz'));q=x['q'];tt=x['tt'];param=x['param'];ii,jj=matches(n,parent)
 pin=pins(n);otherpin=pin.copy();otherpin[ii]=False;parentpin=pins(parent);parentpin[jj]=False
 target=.5+sign*.43;new=q.copy();new[:,0]=target
 # Preserve the MMA end, which already lies within the paired falx routes.
 for axis in range(3):
  if axis==0:continue
  new[:,axis]=q[:,axis]
 delta=np.column_stack([np.interp(param,tt,new[:,k]-q[:,k]) for k in range(3)]);w=v+delta;w[otherpin]=v[otherpin];w[ii,0]=target
 parent_baseline={r['brain']:r['triangleContacts'] for r in neural(pv,pf)};history=[];installed=False
 for support in [3.,4.,6.,8.,12.]:
  shift=w[ii]-pv[jj];d,ix=cKDTree(pv[jj]).query(pv);p=pv+(1-smooth(d/support))[:,None]*shift[ix];p[parentpin]=pv[parentpin];p[jj]=w[ii]
  a=assess(n,w,f);b=assess(parent,p,pf);extra=[r for r in b['neuralContacts'] if r['triangleContacts']>parent_baseline.get(r['brain'],0)]
  exact=np.array_equal(w[ii].astype('<f4'),p[jj].astype('<f4'))
  row=dict(parentSupportMm=support,collateral=a,parent=b,additionalParentContacts=extra,sharedJunctionExact=bool(exact));history.append(row);print(n,row,flush=True)
  if not a['neuralContacts'] and not a['newFoldPairs'] and not b['newFoldPairs'] and not extra and exact:
   save(n,w,f,'paired-falx-shared-ACA-junction-reconstruction');save(parent,p,pf,'coherent-dural-attachment-collar');installed=True;break
 reports.append(dict(node=n,parent=parent,installed=installed,history=history))
# Left cavernous connection: the native parent attachment itself contacts
# parahippocampal cortex. Fit the junction medially together with its collar.
n='Posterior cavernous MMA–posterolateral ILT left';parent='MMA posterior cavernous left'
v,f=current(n);pv,pf=current(parent);ii,jj=matches(n,parent);otherpin=pins(n);otherpin[ii]=False;parentpin=pins(parent);parentpin[jj]=False
x=np.load(WORK/(n+'.continuation-curve.npz'));param=x['param'];tt=x['tt'];q=x['q'];base={r['brain']:r['triangleContacts'] for r in neural(pv,pf)};history=[];installed=False
for amount in [.5,.75,1.,1.25,1.5,2.,2.5,3.]:
 # Intracavernous end bends medially. The distal posterior ILT endpoint is
 # retained because its own parent relation has not yet been reconstructed.
 anchor=param[ii].mean();distal=tt[-1] if anchor<tt.mean() else tt[0]
 weight=smooth(abs(tt-distal)/3.);weight=np.interp(param,tt,weight)
 w=v+weight[:,None]*np.array([amount,0.,0.]);w[ii]=v[ii]+[amount,0.,0.];w[otherpin]=v[otherpin]
 for support in [2.5,4.,6.,8.]:
  d,ix=cKDTree(pv[jj]).query(pv);p=pv+(1-smooth(d/support))[:,None]*(w[ii]-pv[jj])[ix];p[parentpin]=pv[parentpin];p[jj]=w[ii]
  a=assess(n,w,f);b=assess(parent,p,pf);extra=[r for r in b['neuralContacts'] if r['triangleContacts']>base.get(r['brain'],0)]
  exact=np.array_equal(w[ii].astype('<f4'),p[jj].astype('<f4'));row=dict(junctionMedialShiftMm=amount,parentSupportMm=support,collateral=a,parent=b,additionalParentContacts=extra,sharedJunctionExact=bool(exact));history.append(row);print(n,row,flush=True)
  if not a['neuralContacts'] and not a['newFoldPairs'] and not b['newFoldPairs'] and not extra and exact:
   save(n,w,f,'shared-cavernous-wall-attachment-reconstruction');save(parent,p,pf,'coherent-cavernous-attachment-collar');installed=True;break
 if installed:break
reports.append(dict(node=n,parent=parent,installed=installed,history=history))
(OUT/'shared-junction-reconstruction.json').write_text(json.dumps(dict(method=__doc__,results=reports),indent=2))
