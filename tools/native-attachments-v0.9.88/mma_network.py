from round_geometry import *
from vtk.util.numpy_support import vtk_to_numpy
from scipy.spatial.transform import Rotation
from scipy.sparse import coo_matrix
from scipy.sparse.csgraph import connected_components
def incoming_component(v,f,side):
 u,inv=np.unique(v,axis=0,return_inverse=True);h=inv[f];e=np.vstack([h[:,[0,1]],h[:,[1,2]],h[:,[2,0]]]);G=coo_matrix((np.ones(len(e)*2),(np.r_[e[:,0],e[:,1]],np.r_[e[:,1],e[:,0]])),shape=(len(u),len(u))).tocsr();_,labels=connected_components(G);origin=int(np.argmin(u[:,0])if side=='left'else np.argmax(u[:,0]));keep=labels[origin];mask=np.all(labels[h]==keep,axis=1);f=f[mask];used=np.unique(f);remap=np.full(len(v),-1);remap[used]=np.arange(len(used));return v[used],remap[f].astype(np.uint32)
def clipped(v,f,axis,value,inside):
 pl=vtk.vtkPlane();origin=np.zeros(3);origin[axis]=value;normal=np.zeros(3);normal[axis]=1;pl.SetOrigin(*origin);pl.SetNormal(*normal);c=vtk.vtkClipPolyData();c.SetInputData(poly(v,f));c.SetClipFunction(pl);c.SetInsideOut(inside);c.Update();o=c.GetOutput()
 return vtk_to_numpy(o.GetPoints().GetData()).astype('<f4').astype(float),vtk_to_numpy(o.GetPolys().GetData()).reshape(-1,4)[:,1:].astype(np.uint32)
def make(side,cutx,z,bow):
 parent='MMA paramedian '+side;child='MMA falcine terminal '+side;pv,pf=mesh(parent);cv,cf=mesh(child);v,f=clipped(pv,pf,0,cutx,side=='left');v,f=incoming_component(v,f,side);w,g=clipped(cv,cf,2,z,True)
 rp=rims(v,f);rc=rims(w,g);i=min(range(len(rp)),key=lambda i:abs(v[rp[i],0].mean()-cutx));j=min(range(len(rc)),key=lambda j:abs(w[rc[j],2].mean()-z))
 src=directed(v,f,rp[i]);dst0=directed(w,g,rc[j])[::-1];a=v[src];c0=a.mean(0);u=a-c0
 def normal(q):
  n=np.cross(q,np.roll(q,-1,axis=0)).sum(0);return n/np.linalg.norm(n)
 b0=w[dst0];c1=b0.mean(0);n0=normal(u);n1=normal(b0-c1);axis=np.cross(n0,n1);sin=np.linalg.norm(axis);angle=np.arctan2(sin,np.dot(n0,n1));axis/=max(sin,1e-12);R=Rotation.from_rotvec(axis*angle)
 ka=np.r_[0,np.cumsum(np.linalg.norm(np.roll(a,-1,axis=0)-a,axis=1))];ka/=ka[-1];best=None
 for shift in range(len(dst0)):
  dst=np.roll(dst0,shift);b=w[dst];kb=np.r_[0,np.cumsum(np.linalg.norm(np.roll(b,-1,axis=0)-b,axis=1))];kb/=kb[-1];local=R.inv().apply(b-c1);sample=np.column_stack([np.interp(ka[:-1],kb,np.r_[local[:,k],local[0,k]])for k in range(3)]);err=np.sum((u-sample)**2)
  if best is None or err<best[0]:best=(err,dst,sample,kb)
 dst=best[1];sample=best[2];delta=c1-c0;length=np.linalg.norm(delta);T0=n0*np.sign(np.dot(n0,delta))*length*.4;T1=n1*np.sign(np.dot(n1,delta))*length*.6
 q=v.copy();ff=f.tolist();rings=[src];params=[ka[:-1]];split=None;source_count=len(v)
 for step,t in enumerate(np.linspace(0,1,22)[1:-1],1):
  centre=(2*t**3-3*t*t+1)*c0+(t**3-2*t*t+t)*T0+(-2*t**3+3*t*t)*c1+(t**3-t*t)*T1;centre[2]-=bow*np.sin(np.pi*t)
  radial=Rotation.from_rotvec(axis*angle*t).apply((1-t)*u+t*sample);ring=centre+radial;ix=np.arange(len(q),len(q)+len(ring));q=np.vstack([q,ring]);rings.append(ix);params.append(ka[:-1])
  if step==12:split=(len(q),len(ff),ix.copy())
 endpoint=np.arange(len(q),len(q)+len(dst));q=np.vstack([q,w[dst]]);rings.append(endpoint);params.append(best[3][:-1]);stripgroups=[]
 for k,(r,s,ra,sa)in enumerate(zip(rings[:-1],rings[1:],params[:-1],params[1:])):
  faces=[];ii=jj=0
  while ii<len(r)or jj<len(s):
   an=ra[ii+1]if ii+1<len(r)else 1.;bn=sa[jj+1]if jj+1<len(s)else 1.
   if ii<len(r)and(jj==len(s)or an<=bn):faces.append([int(r[ii%len(r)]),int(s[jj%len(s)]),int(r[(ii+1)%len(r)])]);ii+=1
   else:faces.append([int(r[ii%len(r)]),int(s[jj%len(s)]),int(s[(jj+1)%len(s)])]);jj+=1
  stripgroups.append(np.array(faces,dtype=np.uint32))
 # Partition the common exterior wall at a new exact shared ring.
 cutring=rings[12];parent_faces=np.vstack([f,*stripgroups[:12]]);parent_positions=q[:cutring[-1]+1]
 child_indices=np.unique(np.concatenate([cutring,*[t.ravel()for t in stripgroups[12:]]]));mapping={int(i):len(w)+k for k,i in enumerate(child_indices)};child_positions=np.vstack([w,q[child_indices]]);child_faces=g.tolist()
 # Replace the duplicated final ring indices with the retained child cut rim.
 for i,j in zip(endpoint,dst):mapping[int(i)]=int(j)
 for t in np.vstack(stripgroups[12:]):child_faces.append([mapping[int(i)]for i in t])
 cp=np.asarray(child_positions,dtype='<f4').astype(float);cg=np.array(child_faces,dtype=np.uint32);pp=parent_positions.astype('<f4').astype(float);pg=parent_faces.astype(np.uint32)
 return {parent:(pp,pg),child:(cp,cg)}, {'side':side,'cutX':cutx,'childCutZ':z,'inferiorBowMm':bow,'parentPortCoordsBefore':pv[rims(pv,pf)[-1]].mean(0).tolist(),'sharedParentIndices':cutring.tolist(),'sharedChildIndices':[mapping[int(i)]for i in cutring],'originalParentVertexCount':len(pv),'originalChildVertexCount':len(cv),'newParentVertices':len(pp),'newChildVertices':len(cp)}
BASE={n:mesh(n)for n in ['MMA paramedian left','MMA paramedian right','MMA falcine terminal left','MMA falcine terminal right']};ss=mesh('vein.superior_sagittal');history=[];accepted=[]
for lateral in [2.2,3.]:
 for bow in [.4,.8,1.2]:
  changed={};details=[];screen={'lateralCutOffsetMm':lateral,'inferiorBowMm':bow,'networks':[]};safe=True
  for side in ['left','right']:
   cutx=.635+(-lateral if side=='left'else lateral);parts,d=make(side,cutx,157.5,bow);changed.update(parts);details.append(d);vs=[];fs=[];offset=0
   for n,(p,f)in parts.items():
    folds=intersections(p,f);c=cropped_contacts(p,f,*ss);rr={'node':n,'selfIntersections':len(folds),'sinusContacts':c};screen['networks'].append(rr);print(json.dumps(rr),flush=True)
    if folds or c:safe=False
    vs.append(p);fs.append(f+offset);offset+=len(p)
   combined=intersections(np.vstack(vs),np.vstack(fs));screen.setdefault('combined',[]).append({'side':side,'selfIntersections':len(combined)});print(json.dumps(screen['combined'][-1]),flush=True)
   if combined:safe=False
   if not safe:break
  if safe:
   lo=np.min([p.min(0)for p,f in changed.values()],0);hi=np.max([p.max(0)for p,f in changed.values()],0);contacts_report=[];new=[];increased=[]
   for m in META:
    other=m['name']
    if other in changed:continue
    w,g=mesh(other)
    if np.any(w.max(0)<lo)or np.any(w.min(0)>hi):continue
    for n,(p,f)in changed.items():
     v,h=BASE[n];pre=cropped_contacts(v,h,w,g);post=cropped_contacts(p,f,w,g)
     if pre or post:contacts_report.append({'node':n,'other':other,'before':pre,'after':post})
     if other=='brain.falx-cerebri':continue
     if post and not pre:new.append([n,other])
     if post>pre:increased.append([n,other])
   screen['contacts']=contacts_report;screen['newContactObjects']=new;screen['increasedContactObjects']=increased;safe=not new and not increased;print(json.dumps({'scenePassed':safe,'new':new,'increased':increased}),flush=True)
  screen['passed']=safe;history.append(screen)
  if safe:
   for n,(p,f)in changed.items():p.astype('<f4').tofile(OUT/(n+'.positions.bin'));f.astype('<u4').tofile(OUT/(n+'.indices.bin'));normals(p,f).astype('<f4').tofile(OUT/(n+'.normals.bin'))
   accepted=details;break
 if accepted:break
(D.parent/'mma-network-trials.json').write_text(json.dumps({'accepted':accepted,'trials':history},indent=2)+'\n')
