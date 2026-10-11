"""Require simultaneous neural, bone and receiving-wall clearance.

Retain the distal ILT port geometry. Move the MMA attachment and parent
collar coherently. If no full-constraint trial succeeds, restore the prior
candidate rather than retaining a repair that introduces new relationships.
"""
from route_tools import *
baseline=WORK.parent/'work-v0958/candidate';n='Posterior cavernous MMA–posterolateral ILT left';parent='MMA posterior cavernous left';v,f=load(n,baseline);pv,pf=load(parent,baseline);ii,jj=matches(n,parent);parentpin=pins(parent);parentpin[jj]=False;x=np.load(WORK/(n+'.continuation-curve.npz'));q=x['q'];param=x['param'];tt=x['tt'];r=x['r'];anchor=param[ii].mean();distal=tt[-1] if anchor<tt.mean() else tt[0];from_joint=abs(tt-anchor);from_distal=abs(tt-distal)
obstacles=[]
for other in ['bone.sphenoid','bone.frontal','bone.temporal.left','vein.sphenoparietal.left','vein.middle_meningeal.anterior.left','vein.middle_meningeal.posterior.left']:
 obstacles.append((other,*current(other)))
history=[];installed=False
for medial in [.5,.75,1.,1.5,2.,2.5,3.]:
 for inferior in [2.,2.5,3.,3.5,4.,4.5]:
  new=q.copy();new[:,0]+=medial*smooth(from_distal/2.);new[:,2]-=inferior*smooth(from_joint/2.)*smooth(from_distal/1.5);rotation=smooth((np.minimum(from_joint,from_distal)-.7)/1.)
  w,oc,nc=tube(v,q,new,param,tt,rotation);w[ii]=v[ii]+[medial,0.,0.]
  a=assess(n,w,f,initial=v)
  if a['neuralContacts'] or a['newFoldPairs']:
   history.append(dict(medialMm=medial,inferiorMm=inferior,collateral=a,installed=False));continue
  hits=[dict(other=k,triangleContacts=c) for k,bv,bf in obstacles if (c:=contacts(w,f,bv,bf))]
  d,ix=cKDTree(pv[jj]).query(pv);p=pv+(1-smooth(d/4.))[:,None]*(w[ii]-pv[jj])[ix];p[parentpin]=pv[parentpin];p[jj]=w[ii];b=assess(parent,p,pf,initial=pv);parenthits=[dict(other=k,triangleContacts=c) for k,bv,bf in obstacles if (c:=contacts(p,pf,bv,bf))]
  row=dict(medialMm=medial,inferiorMm=inferior,collateral=a,parent=b,obstacleContacts=hits,parentObstacleContacts=parenthits,installed=False);history.append(row);print(row,flush=True)
  if not hits and not parenthits and not b['neuralContacts'] and not b['newFoldPairs']:
   save(n,w,f,'full-constraint-cavernous-reconstruction-with-preserved-ILT-port');save(parent,p,pf,'coherent-cavernous-attachment-collar');np.savez_compressed(WORK/(n+'.v0959-curve.npz'),q=new,r=r,param=param,tt=tt,rotationWeight=rotation);row['installed']=True;installed=True;break
 if installed:break
if not installed:
 old_revision=json.loads((baseline/'revision.json').read_text());old_rows={r['node']:r for r in old_revision['changed']}
 for name,verts,faces in [(n,v,f),(parent,pv,pf)]:
  write(name,verts,faces)
  rev['changed']=[row for row in rev['changed'] if row['node']!=name]
  if name in old_rows:rev['changed'].append(old_rows[name])
 (OUT/'revision.json').write_text(json.dumps(rev,indent=2))
 path=WORK/(n+'.v0959-curve.npz')
 if path.exists():path.unlink()
(OUT/'full-constraint-cavernous-reconstruction.json').write_text(json.dumps(dict(method=__doc__,installed=installed,restoredPreviousCandidate=not installed,history=history),indent=2));print('INSTALLED',installed,flush=True)
