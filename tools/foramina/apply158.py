"""One-shot source repair from revision157. Preview and validate first."""
from vertebral158 import *
surface=json.load(open(A/'public/anatomy/dsa-surfaces.json'));glbs={'models/complete-circulation.glb':G};changes=[];guides=[];quality=[];writers={sid:(lambda p,sid=sid:warp(p,sid))for sid in targets}
# Carry independent connection cuffs only where they share corrected vertices.
file='models/complete-anastomoses.glb';anc=Glb(A/'public/anatomy'/file);glbs[file]=anc;pts=np.concatenate([data[sid][0]for sid in targets]);dst=np.concatenate(list(targets.values()));tree=cKDTree(pts)
for sid,row in rows.items():
 if row.get('asset',{}).get('file')!=file:continue
 p,f,n=anc.mesh(row['asset']['node']);d,ix=tree.query(p,distance_upper_bound=2e-5);sel=d<2e-5
 if not sel.any():continue
 delta=dst[ix[sel]]-p[sel]
 if np.linalg.norm(delta,axis=1).max()<2e-5:continue
 writers[sid]=make_field(p[sel],delta);data[sid]=(p,f,n)
for sid,move in writers.items():
 p,f,n=data[sid];q=targets[sid]if sid in fairing else move(p);displacement=np.linalg.norm(q-p,axis=1)
 if displacement.max()<2e-5:continue
 row=rows[sid];file=row['asset']['file'];glbs[file].replace(row['asset']['node'],q,f)
 if sid in surface['entries']and surface['entries'][sid].get('extra'):surface['entries'][sid]['extra']=move(surface['entries'][sid]['extra']).tolist()
 if sid in flow['entries']and len(flow['entries'][sid].get('points',[]))>=2:
  row['flowCourseGuide']={'geometrySha256':'pending','points':move(flow['entries'][sid]['points']).tolist()};guides.append(sid)
 sample=p[np.linspace(0,len(p)-1,min(512,len(p))).astype(int)];eps=1e-4;J=np.stack([(move(sample+np.eye(3)[k]*eps)-move(sample-np.eye(3)[k]*eps))/(2*eps)for k in range(3)],axis=2);sv=np.linalg.svd(J,compute_uv=False);det=np.linalg.det(J)
 assert det.min()>.01,(sid,'non-positive deformation',det.min())
 check={'method':'Sampled finite-difference deformation-Jacobian singular-value bounds from revision157 to158; includes axial stretch and is not a direct lumen radius measurement.','ratioP05MedianP95':np.percentile(sv.ravel(),[5,50,95]).tolist(),'p95AbsoluteFractionalRadiusChange':float(np.percentile(abs(sv-1),95))}
 quality.append({'id':sid,'minimumSampledJacobianDeterminant':float(det.min()),**check})
 if row.get('vesselCourse'):
  c=row['vesselCourse'];c['radiusPolicy']='preserve-source-profile-with-measured-wall-deformation';c['reviewStatus']='requires-anatomical-target'if c.get('missingTargets')else'requires-anatomical-review';c.setdefault('fitting',{})['calibreCheck']=check;c['fitting']['revision158']={'method':'Measured native wall cross-sections fitted to a monotone V4 course; local transition fairing, with connected branch cuffs carried and source topology retained.','maximumDisplacementMm':float(displacement.max())}
 if sid in fairing:row['vesselCourse']['fitting']['revision158']['surfaceFairing']=fairing[sid]
 changes.append({'id':sid,'file':file,'node':row['asset']['node'],'maximumDisplacementMm':float(displacement.max())});print('Prepared',sid,float(displacement.max()),flush=True)
# Assertions above all precede writing any production GLB.
for file,g in glbs.items():
 if not g.changed:continue
 h=g.save();surface['sourceHashes'][file]=h;surface['assetRevisions'][file]=h[:20];decoded=Glb(A/'public/anatomy'/file)
 for sid,row in rows.items():
  if row.get('asset',{}).get('file')!=file:continue
  if row.get('vesselCourse'):row['vesselCourse']['geometrySha256']=h
  if sid in guides:
   p,f,_=decoded.mesh(row['asset']['node']);row['flowCourseGuide']['geometrySha256']=hashlib.sha256(np.asarray(p,'<f4').tobytes()+np.asarray(f,'<u4').tobytes()).hexdigest()
M['release']='0.9.158';(A/'anatomy/generated/complete_manifest.json').write_text(json.dumps(M,indent=2)+'\n');(A/'public/anatomy/dsa-surfaces.json').write_text(json.dumps(surface));v=json.load(open(A/'public/anatomy/vessel-courses.json'));v['courses']=[r['vesselCourse']for r in M['structures']if r.get('vesselCourse')];v['release']='0.9.158';(A/'public/anatomy/vessel-courses.json').write_text(json.dumps(v,indent=2)+'\n');(A/'anatomy/source/foramina/revision158-arteries.json').write_text(json.dumps(changes,indent=2)+'\n');(A/'anatomy/source/foramina/revision158-flow-changes.json').write_text(json.dumps(guides,indent=2)+'\n');(A/'docs/revision158-deformation-bounds.json').write_text(json.dumps(quality,indent=2)+'\n');print('Saved',len(changes),'nodes;',len(guides),'flow guides',flush=True)
