from geometry import *
from extract_curves import extract
from scipy.spatial import cKDTree
from collections import Counter
import itertools,hashlib
OUT=ROOT/'candidate';revision=json.loads((OUT/'revision.json').read_text());changed={r['node'] for r in revision['changed']};new={}
for n in changed:new[n]=(np.fromfile(OUT/(n+'.positions.bin'),'<f4').reshape(-1,3),np.fromfile(OUT/(n+'.indices.bin'),'<u4').reshape(-1,3))
def field(v):
 d=np.linalg.norm((v-np.array([7,-54.5,79]))/[7,7,7],axis=1);return (1-smooth((d-.35)/.65))[:,None]*np.array([-.5,-1.5,-1.9])
report={'release':'0.9.29','checks':{'meshQuality':{'passed':True,'labels':[]},'physicalJunctions':{'passed':True,'assets':[]}},'calibreChanges':[]}
for n in changed:
 m=meshes[n];v,f=new[n];tri=v[f].astype(float);cross=np.cross(tri[:,1]-tri[:,0],tri[:,2]-tri[:,0]);area=np.linalg.norm(cross,axis=1)
 finite=np.isfinite(v).all();zero=int((area<1e-10).sum());baseline=m.v[m.f];cross0=np.cross(baseline[:,1]-baseline[:,0],baseline[:,2]-baseline[:,0]);oldzero=int((np.linalg.norm(cross0,axis=1)<1e-10).sum())
 passed=finite and (zero<=oldzero);r={'node':n,'finite':bool(finite),'degenerateTriangles':zero,'baselineDegenerateTriangles':oldzero}
 if n.startswith('vein.'):
  h=1e-4;grad=np.column_stack([(field(m.v+np.eye(3)[j]*h)[:,0]-field(m.v-np.eye(3)[j]*h)[:,0])/(-.5*2*h) for j in range(3)])
  det=1+grad@np.array([-.5,-1.5,-1.9]);r['minimumJacobianDeterminant']=float(det.min());passed=passed and det.min()>.15
  # Pointwise triangle orientation is compared to the mapped original normals;
  # field Jacobian positivity also excludes a fold in the surrounding map.
  f0=cross0/np.maximum(np.linalg.norm(cross0,axis=1)[:,None],1e-20);f1=cross/np.maximum(area[:,None],1e-20)
  r['minimumNormalDot']=float(np.min(np.einsum('ij,ij->i',f0,f1)));passed=passed and r['minimumNormalDot']>0
 r['passed']=bool(passed);report['checks']['meshQuality']['labels'].append(r);report['checks']['meshQuality']['passed'] &= bool(passed)
 print(n,'quality',r,flush=True)
 if n.startswith('vein.'):
  q,rad,param,tt=extract(m);p=np.column_stack([np.interp(param,tt,q[:,j]) for j in range(3)]);qn=q+field(q);pn=p+field(p);tangent=np.gradient(qn,tt,axis=0);tangent/=np.maximum(np.linalg.norm(tangent,axis=1)[:,None],1e-9);tan=np.column_stack([np.interp(param,tt,tangent[:,j]) for j in range(3)]);tan/=np.maximum(np.linalg.norm(tan,axis=1)[:,None],1e-9)
  dr=v-pn;rr=np.sqrt(np.maximum(0,(dr*dr).sum(1)-(dr*tan).sum(1)**2));old=m.v-p;oldt=np.gradient(q,tt,axis=0);oldt/=np.linalg.norm(oldt,axis=1)[:,None];ot=np.column_stack([np.interp(param,tt,oldt[:,j]) for j in range(3)]);ot/=np.maximum(np.linalg.norm(ot,axis=1)[:,None],1e-9);ro=np.sqrt(np.maximum(0,(old*old).sum(1)-(old*ot).sum(1)**2));mask=(ro>.1)&(param>tt[0]+1)&(param<tt[-1]-1);ratio=rr[mask]/ro[mask];z={'node':n,'method':'Original geodesic-section coordinates and transported centreline tangent; cap-adjacent points excluded','ratioP05MedianP95':np.percentile(ratio,[5,50,95]).tolist(),'p95AbsoluteFractionalRadiusChange':float(np.percentile(abs(ratio-1),95))};report['calibreChanges'].append(z);print('Calibre',z,flush=True)
# Shared boundary vertices must remain present on both labels, including every
# existing receiving collar. Repartitioned ICA retains the exact union skin.
def joins(file,after):
 names=[n for n,m in meshes.items() if m.file==file];vv=[];labels=[]
 for i,n in enumerate(names):
  v=new[n][0] if after and n in new else meshes[n].v.astype('<f4');v=np.unique(v.astype('<f4'),axis=0);vv.append(v);labels.extend([i]*len(v))
 v=np.vstack(vv);labels=np.array(labels);_,inv,cnt=np.unique(v,axis=0,return_inverse=True,return_counts=True);keep=cnt[inv]>1;order=np.argsort(inv[keep]);ids=inv[keep][order];la=labels[keep][order];starts=np.r_[0,np.flatnonzero(np.diff(ids))+1,len(ids)];pairs=Counter()
 for a,b in zip(starts[:-1],starts[1:]):
  for x,y in itertools.combinations(np.unique(la[a:b]),2):pairs[(names[x],names[y])]+=1
 return pairs
for file in set(meshes[n].file for n in changed):
 before=joins(file,False);after=joins(file,True);lost=[{'one':a,'two':b,'before':cnt,'after':after[(a,b)]} for (a,b),cnt in before.items() if cnt>=2 and after[(a,b)]<2]
 report['checks']['physicalJunctions']['assets'].append({'file':file,'originalDirectJunctionPairs':sum(c>=2 for c in before.values()),'lostPairs':lost,'passed':not lost});report['checks']['physicalJunctions']['passed'] &= not lost;print('Junctions',file,'lost',lost,flush=True)
 # Identity of the labelled union geometry for the ICA partitioning.
 if file=='complete-circulation.glb':
  def trianglehash(after):
   triangles=[]
   for n,m in meshes.items():
    if m.file!=file:continue
    v,f=new[n] if after and n in new else (m.v.astype('<f4'),m.f);triangles.append(v[f].reshape(-1,9).astype('<f4'))
   t=np.vstack(triangles);return hashlib.sha256(np.sort(t.view('V36').ravel()).tobytes()).hexdigest()
  same=trianglehash(False)==trianglehash(True);report['icaUnionGeometryUnchanged']=same;report['checks']['meshQuality']['passed'] &= same
clear=json.loads((OUT/'clearance.json').read_text());report['clearance']={'newContacts':clear['newContacts'],'passed':not clear['newContacts']};report['passed']=all(x['passed'] for x in report['checks'].values()) and report['clearance']['passed'];(OUT/'validation.json').write_text(json.dumps(report,indent=2)+'\n');print('Final passed',report['passed'],flush=True)
