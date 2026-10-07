"""Check the exact staged geometry, before production assets can be written."""
import sys,itertools
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'anatomical-fixes-v0929'))
from geometry import *
from extract_curves import extract
from scipy.spatial import cKDTree
from collections import Counter
sys.path.insert(0,str(Path(__file__).resolve().parent))
OUT=ROOT.parent/'corrections-work';C=OUT/'candidate';revision=json.loads((C/'revision.json').read_text());changed={r['node'] for r in revision['changed']};new={n:np.fromfile(C/(n+'.positions.bin'),'<f4').reshape(-1,3) for n in changed};pd={n:poly(v,meshes[n].f) for n,v in new.items()};bounds={n:np.array(p.GetBounds()).reshape(3,2).T for n,p in pd.items()}
def after(n):return pd.get(n,meshes[n].pd)
def transformed(n,v):
 r=revision['fields'];v=v.copy();file=meshes[n].file;u=r['upper'];lower_names=set(r['lower']['baseline']['changed'])
 def bump(v,c,e,d,p):
  radius=np.linalg.norm((v-np.array(c))/e,axis=1);w=1-smooth((radius-p)/(1-p));return w[:,None]*np.array(d)
 if file in ['venous.glb','brain-context.glb']:
  for j in range(u['steps']):v+=bump(v,np.array(u['centre'])+np.array(u['delta'])*j/u['steps'],u['extent'],np.array(u['delta'])/u['steps'],u['plateau'])
 l=r['lower']['baseline']
 if file=='brain-context.glb' or n in lower_names:v+=bump(v,l['centre'],l['extent'],l['delta'],l['plateau'])
 for f in r['lower']['refinements']:
  if file=='venous.glb' or (file=='brain-context.glb' and f['mode']=='common'):v+=bump(v,f['centre'],f['extent'],f['delta'],f['plateau'])
 if file=='venous.glb':v+=bump(v,r['ring']['centre'],r['ring']['extent'],r['ring']['delta'],.6)
 return v
clear={'release':'0.9.31','checkedPairs':0,'newContacts':[],'baselineContacts':[],'resolvedAuditContacts':[]}
audit=json.loads((Path(__file__).resolve().parents[2]/'docs/validation/anatomical-clearance-v0.9.29.json').read_text())
for r in audit['resolvedAuditContacts']:
 hits=contacts(after(r['one']),after(r['two']));entry={'one':r['one'],'two':r['two'],'baselineContacts':r['candidateHalfContacts'],'candidateContacts':hits};clear['resolvedAuditContacts'].append(entry);print('AUDIT',entry,flush=True)
seen=set()
for n,p in pd.items():
 for o,m in meshes.items():
  if m.file==meshes[n].file or m.file=='complete-anastomoses.glb':continue
  key=tuple(sorted([n,o]))
  if key in seen:continue
  seen.add(key);b=bounds.get(o,m.bounds)
  if np.any(bounds[n][1]<b[0]) or np.any(b[1]<bounds[n][0]):continue
  clear['checkedPairs']+=1
  if contacts(p,after(o),True):
   old=contacts(meshes[n].pd,m.pd,True);(clear['baselineContacts'] if old else clear['newContacts']).append({'one':n,'two':o})
 print('CHECKED',n,'new',len(clear['newContacts']),flush=True)
(C/'clearance.json').write_text(json.dumps(clear,indent=2)+'\n')
report={'release':'0.9.31','checks':{'meshQuality':{'passed':True,'labels':[]},'physicalJunctions':{'passed':True,'assets':[]}},'calibreChanges':[]}
for n in sorted(changed):
 m=meshes[n];v=new[n];f=m.f;tri=v[f].astype(float);fn=np.cross(tri[:,1]-tri[:,0],tri[:,2]-tri[:,0]);area=np.linalg.norm(fn,axis=1);old=m.v[f];oldarea=np.linalg.norm(np.cross(old[:,1]-old[:,0],old[:,2]-old[:,0]),axis=1);h=1e-4;grad=np.stack([(transformed(n,m.v+np.eye(3)[j]*h)-transformed(n,m.v-np.eye(3)[j]*h))/(2*h) for j in range(3)],axis=2);det=np.linalg.det(grad);finite=bool(np.isfinite(v).all());zero=int((area<1e-10).sum());oldzero=int((oldarea<1e-10).sum());passed=finite and zero<=oldzero and float(det.min())>0
 q={'node':n,'finite':finite,'baselineDegenerateTriangles':oldzero,'degenerateTriangles':zero,'minimumJacobianDeterminant':float(det.min()),'passed':bool(passed)};report['checks']['meshQuality']['labels'].append(q);report['checks']['meshQuality']['passed'] &= bool(passed);print('QUALITY',q,flush=True)
 if m.file=='venous.glb' and n not in ['vein.marginal','vein.basilar_plexus']:
  q,rad,param,tt=extract(m);p=np.column_stack([np.interp(param,tt,q[:,j]) for j in range(3)]);qn=transformed(n,q);pn=transformed(n,p);tangent=np.gradient(qn,tt,axis=0);tangent/=np.maximum(np.linalg.norm(tangent,axis=1)[:,None],1e-9);tan=np.column_stack([np.interp(param,tt,tangent[:,j]) for j in range(3)]);tan/=np.maximum(np.linalg.norm(tan,axis=1)[:,None],1e-9);dr=v-pn;rr=np.sqrt(np.maximum(0,(dr*dr).sum(1)-(dr*tan).sum(1)**2));oldt=np.gradient(q,tt,axis=0);oldt/=np.maximum(np.linalg.norm(oldt,axis=1)[:,None],1e-9);ot=np.column_stack([np.interp(param,tt,oldt[:,j]) for j in range(3)]);ot/=np.maximum(np.linalg.norm(ot,axis=1)[:,None],1e-9);dr0=m.v-p;ro=np.sqrt(np.maximum(0,(dr0*dr0).sum(1)-(dr0*ot).sum(1)**2));mask=(ro>.1)&(param>tt[0]+1)&(param<tt[-1]-1);ratio=rr[mask]/ro[mask]
  if len(ratio):report['calibreChanges'].append({'node':n,'method':'Transported geodesic section and tangent; cap-adjacent points excluded; illustrative calibre only','ratioP05MedianP95':np.percentile(ratio,[5,50,95]).tolist(),'p95AbsoluteFractionalRadiusChange':float(np.percentile(abs(ratio-1),95))})
def joins(file,after):
 names=[n for n,m in meshes.items() if m.file==file];vv=[];labels=[]
 for i,n in enumerate(names):
  v=new[n] if after and n in new else meshes[n].v.astype('<f4');v=np.unique(v.astype('<f4'),axis=0);vv.append(v);labels.extend([i]*len(v))
 v=np.vstack(vv);labels=np.array(labels);_,inv,cnt=np.unique(v,axis=0,return_inverse=True,return_counts=True);keep=cnt[inv]>1;order=np.argsort(inv[keep]);ids=inv[keep][order];la=labels[keep][order];starts=np.r_[0,np.flatnonzero(np.diff(ids))+1,len(ids)];pairs=Counter()
 for a,b in zip(starts[:-1],starts[1:]):
  for x,y in itertools.combinations(np.unique(la[a:b]),2):pairs[(names[x],names[y])]+=1
 return pairs
for file in set(meshes[n].file for n in changed):
 before=joins(file,False);afterpairs=joins(file,True);lost=[{'one':a,'two':b,'before':cnt,'after':afterpairs[(a,b)]} for (a,b),cnt in before.items() if cnt>=2 and afterpairs[(a,b)]<2];report['checks']['physicalJunctions']['assets'].append({'file':file,'originalDirectJunctionPairs':sum(c>=2 for c in before.values()),'lostPairs':lost,'passed':not lost});report['checks']['physicalJunctions']['passed'] &= not lost;print('JOINS',file,'lost',lost,flush=True)
report['clearance']={'passed':not clear['newContacts'],'newContacts':clear['newContacts']};report['allTwelveAuditedCrossingsClear']=all(r['candidateContacts']==0 for r in clear['resolvedAuditContacts']);report['passed']=all(r['passed'] for r in report['checks'].values()) and report['clearance']['passed'] and report['allTwelveAuditedCrossingsClear'];(C/'validation.json').write_text(json.dumps(report,indent=2)+'\n');print('PASSED',report['passed'],flush=True)
