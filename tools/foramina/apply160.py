"""One-shot repair from v159. Rebuild proximal walls; carry shared collars."""
from maxillary160 import *
import hashlib
from remesh160 import loops
surface=json.load(open(BASE/'public/anatomy/dsa-surfaces.json'));baseline={sid:{'selectable':r['selectable'],'fullSafe':r.get('safeRanges')==[[0,r['length']]]}for sid,r in flow['entries'].items()};(A/'anatomy/source/foramina/revision160-flow-status-baseline.json').write_text(json.dumps(baseline))
glbs={'models/complete-circulation.glb':G};file='models/complete-anastomoses.glb';anc=Glb(BASE/'public/anatomy'/file);anc.path=A/'public/anatomy'/file;glbs[file]=anc
# Preserve other connector cuffs explicitly, including unchanged attachments.
allIds=list(data);allp=np.concatenate([data[sid][0]for sid in allIds]);allq=np.concatenate([targets.get(sid,data[sid][0])for sid in allIds]);tree=cKDTree(allp)
for sid,row in rows.items():
 if row.get('asset',{}).get('file')!=file:continue
 p,f,n=anc.mesh(row['asset']['node']);d,ix=tree.query(p,distance_upper_bound=2e-5);sel=d<2e-5
 if not sel.any():continue
 delta=allq[ix[sel]]-p[sel]
 if np.linalg.norm(delta,axis=1).max()<2e-5:continue
 writers[sid]=field(p[sel],delta,outer=4);data[sid]=(p,f,n);targets[sid]=writers[sid](p)
changed=[];guides=[];oldSource={sid:data[sid]for sid in meshTargets};oldSurface={sid:json.loads(json.dumps(surface['entries'][sid]))for sid in meshTargets}
for sid,move in writers.items():
 p,f,n=data[sid];q,g=meshTargets.get(sid,(targets[sid],f));row=rows[sid];file=row['asset']['file'];glbs[file].replace(row['asset']['node'],q,g)
 if sid not in meshTargets and sid in surface['entries']and surface['entries'][sid].get('extra'):surface['entries'][sid]['extra']=move(surface['entries'][sid]['extra']).tolist()
 if sid in flow['entries']:
  points=move(flow['entries'][sid]['points'])
  if sid in meshTargets:
   side=row['side'];sign=1 if side=='right'else -1;direction=np.array([-.6*sign,.8,0]);basis=np.array([[.8*sign,.6,0],[0,0,1]]).T;s=np.linspace(-72.89,-47.61,95);points=s[:,None]*direction+profiles[side](np.clip(s,-72.9,-46.5))@basis.T;native=np.array(flow['entries'][sid]['points']);remaining=native[native@direction>=-47.6];points=np.r_[points,remaining]
  row['flowCourseGuide']={'geometrySha256':'pending','points':points.tolist()};guides.append(sid)
 if row.get('vesselCourse'):
  c=row['vesselCourse'];c['reviewStatus']='requires-anatomical-review';c['radiusPolicy']='preserve-source-profile-with-measured-wall-deformation';c.setdefault('fitting',{})['revision160']={'method':'Local proximal IMA wall reconstruction with explicit port loops; ECA and attached branch collars carried. Distal native IMA retained. Teaching reconstruction.'}
 if sid in meshTargets:
  c=row['vesselCourse'];c['radiusPolicy']='reconstruct-local-tubular-wall';rec=c['fitting']['revision160'];r=remeshReports[sid];rec.update(sourceBoundaryLoops=r['boundaryLoops'],outputBoundaryLoops=r['boundaryLoops'],rebuiltSidePorts=r['sidePortsRebuilt'],illustrativeRadiusMm=1.05,measuredPatientProfile=False,retainedDistalCutS=r['retainedDistalCutS'])
 else:
  sample=p[np.linspace(0,len(p)-1,min(256,len(p))).astype(int)];eps=1e-4;J=np.stack([(move(sample+np.eye(3)[k]*eps)-move(sample-np.eye(3)[k]*eps))/(2*eps)for k in range(3)],axis=2);sv=np.linalg.svd(J,compute_uv=False);row['vesselCourse']['fitting']['calibreCheck']={'method':'Sampled first-stage collar-field singular values; includes axial stretch, not a measured lumen profile. Final source fairing and native-collar policy recorded separately.','ratioP05MedianP95':np.percentile(sv.ravel(),[5,50,95]).tolist(),'p95AbsoluteFractionalRadiusChange':float(np.percentile(abs(sv-1),95))}
 changed.append({'id':sid,'file':file,'node':row['asset']['node'],'oldVertices':len(p),'newVertices':len(q),'oldFaces':len(f),'newFaces':len(g),'maximumSharedCuffDisplacementMm':float(np.linalg.norm(targets[sid]-p,axis=1).max())});print('Prepared',sid,len(q),len(g),flush=True)
for file,g in glbs.items():
 if not g.changed:continue
 h=g.save();surface['sourceHashes'][file]=h;surface['assetRevisions'][file]=h[:20];actual=Glb(A/'public/anatomy'/file)
 for sid,row in rows.items():
  if row.get('asset',{}).get('file')!=file:continue
  if row.get('vesselCourse'):row['vesselCourse']['geometrySha256']=h
  if sid in guides:
   p,f,_=actual.mesh(row['asset']['node']);row['flowCourseGuide']['geometrySha256']=hashlib.sha256(np.asarray(p,'<f4').tobytes()+np.asarray(f,'<u4').tobytes()).hexdigest()
  if sid not in meshTargets:continue
  p,f,_=actual.mesh(row['asset']['node']);oldp,oldf,_=oldSource[sid];old=oldSurface[sid];sign=1 if row['side']=='right'else -1;direction=np.array([-.6*sign,.8,0]);cut=-47.6
  # Retain reviewed closing surfaces for all unchanged distal ports.
  combined=np.r_[oldp,np.asarray(old['extra'])];caps=np.array(old['caps']).reshape(-1,3);keep=np.min(combined[caps]@direction,axis=1)>cut;caps=caps[keep];used=np.unique(caps);mapping={};extras=[];tree=cKDTree(p)
  for i in used:
   if i<len(oldp):
    dist,idx=tree.query(oldp[i]);assert dist<2e-5,(sid,dist);mapping[int(i)]=int(idx)
   else:mapping[int(i)]=len(p)+len(extras);extras.append(combined[i])
  newcaps=[[mapping[int(i)]for i in tri]for tri in caps]
  # New proximal ports are simple ellipse boundaries on the rebuilt wall.
  edges={}
  for tri in f:
   for a,b in zip(tri,np.roll(tri,-1)):edges.setdefault(tuple(sorted((int(a),int(b)))),[]).append((int(a),int(b)))
  for loop in loops(p,f):
   if np.mean(p[loop]@direction)>cut:continue
   cap=len(p)+len(extras);extras.append(np.mean(p[loop],axis=0))
   for a,b in zip(loop,np.roll(loop,-1)):
    edge=edges[tuple(sorted((int(a),int(b))))];assert len(edge)==1;a,b=edge[0];newcaps.append([b,a,cap])
  pp=np.r_[p,np.array(extras)];ff=np.r_[f,np.array(newcaps)];volume=float(np.einsum('ij,ij->i',pp[ff[:,0]],np.cross(pp[ff[:,1]],pp[ff[:,2]])).sum()/6);assert volume>0
  surface['entries'][sid]={'vertexCount':len(p),'extra':np.array(extras).tolist(),'reverse':False,'flips':[],'removed':[],'caps':np.array(newcaps).ravel().tolist(),'faces':len(ff),'removedSeamFaces':0,'volumeMm3':volume}
M['release']='0.9.160';(A/'anatomy/generated/complete_manifest.json').write_text(json.dumps(M,indent=2)+'\n');(A/'public/anatomy/dsa-surfaces.json').write_text(json.dumps(surface));v=json.load(open(A/'public/anatomy/vessel-courses.json'));v['release']='0.9.160';v['courses']=[r['vesselCourse']for r in M['structures']if r.get('vesselCourse')];(A/'public/anatomy/vessel-courses.json').write_text(json.dumps(v,indent=2)+'\n');(A/'anatomy/source/foramina/revision160-arteries.json').write_text(json.dumps(changed,indent=2)+'\n');(A/'anatomy/source/foramina/revision160-flow-changes.json').write_text(json.dumps(guides,indent=2));(A/'docs/revision160-wall-reconstruction.json').write_text(json.dumps(remeshReports,indent=2));print('Saved',len(changed),'nodes',flush=True)
