"""Apply the checked tubular repair to source meshes and their flow proxies."""
from tubular156 import *
from scipy.interpolate import RBFInterpolator
surface=json.load(open(B/'public/anatomy/dsa-surfaces.json'))
currentSurface=json.load(open(A/'public/anatomy/dsa-surfaces.json'))
def inverse147(q,sid):
 p=np.asarray(q,float).copy()
 for _ in range(200):
  e=q-v147.warp(p,sid)
  if abs(e).max(initial=0)<2e-7:break
  p+=e*.4
 assert abs(q-v147.warp(p,sid)).max(initial=0)<2e-5,(sid,'inverse147')
 return p
fallback=set()
files=['models/complete-circulation.glb','models/complete-anastomoses.glb'];data={};glbs={};original={}
for file in files:
 old=Glb(B/'public/anatomy'/file);g=Glb(A/'public/anatomy'/file);glbs[file]=g
 for sid,row in rows.items():
  if row.get('asset',{}).get('file')!=file:continue
  name=row['asset']['node'];p,f,n=old.mesh(name);cp,cf,cn=g.mesh(name);
  if not np.array_equal(f,cf):
   p=inverse147(cp,sid);f=cf;fallback.add(sid);print('Latest topology retained',sid,flush=True)
  q=transform(p,sid);data[sid]=[p,f,q];original[sid]=cp
# Shared source interfaces must stay coincident even on independent anastomoses.
# Parent arterial walls are authoritative; carry connector cuffs with them.
main=[sid for sid in data if rows[sid]['asset']['file']==files[0]]
pts=np.concatenate([data[sid][0]for sid in main]);targets=np.concatenate([data[sid][2]for sid in main]);tree=cKDTree(pts);portReport=[];corrections={}
for sid,(p,f,q)in data.items():
 if rows[sid]['asset']['file']!=files[1]:continue
 dist,ix=tree.query(p);sel=dist<2e-5
 if not sel.any():continue
 delta=targets[ix[sel]]-q[sel];err=np.linalg.norm(delta,axis=1)
 if err.max()<2e-5:continue
 controls=p[sel];uq,idx=np.unique(np.round(controls,5),axis=0,return_index=True);controls=controls[idx];delta=delta[idx]
 # Compact inverse-distance propagation, exact at coincident cuff vertices.
 def shift(points,controls=controls,delta=delta):
  d,j=cKDTree(controls).query(points);w=smooth((3-d)/3);return w[:,None]*delta[j]
 corrections[sid]=shift;q+=shift(p);data[sid][2]=q
 portReport.append({'id':sid,'sharedVertices':int(sel.sum()),'maximumCuffCorrectionMm':float(err.max())})
changed=[];flowIds=[]
for sid,(p,f,q)in data.items():
 row=rows[sid];move=np.linalg.norm(q-original[sid],axis=1)
 if move.max()<2e-5:continue
 file=row['asset']['file'];glbs[file].replace(row['asset']['node'],q,f)
 def mapped(points):
  a=np.asarray(points,float);b=transform(a,sid)
  if sid in corrections:b+=corrections[sid](a)
  return b
 if sid in currentSurface['entries']and surface['entries'][sid].get('extra'):
  currentSurface['entries'][sid]['extra']=mapped(inverse147(currentSurface['entries'][sid]['extra'],sid)if sid in fallback else surface['entries'][sid]['extra']).tolist()
 if sid in flow['entries']and len(flow['entries'][sid].get('points',[]))>=2:
  row['flowCourseGuide']={'geometrySha256':hashlib.sha256(np.asarray(q,'<f4').tobytes()+np.asarray(f,'<u4').tobytes()).hexdigest(),'points':mapped(inverse147(currentFlow['entries'][sid]['points'],sid)if sid in fallback else flow['entries'][sid]['points']).tolist()};flowIds.append(sid)
 if row.get('vesselCourse'):
  c=row['vesselCourse'];c['reviewStatus']='requires-anatomical-target'if c.get('missingTargets')else'requires-anatomical-review'
  c.setdefault('fitting',{})['revision156']={'method':'Native pre-fitting cross-sections recovered, with a broad smooth shared ICA displacement and centreline transport of ophthalmic radial offsets. Original faces and junction cuffs retained.','maximumDisplacementFrom155Mm':float(move.max()),'source':'Reference146 with numerical inversion of the recorded revision146 deformation.'}
 changed.append({'id':sid,'file':file,'maximumDisplacementMm':float(move.max())});print(sid,float(move.max()),flush=True)
for file,g in glbs.items():
 if not g.changed:continue
 h=g.save();currentSurface['sourceHashes'][file]=h;currentSurface['assetRevisions'][file]=h[:20]
 for row in rows.values():
  if row.get('asset',{}).get('file')==file and row.get('vesselCourse'):row['vesselCourse']['geometrySha256']=h
M['release']='0.9.156'
(A/'anatomy/generated/complete_manifest.json').write_text(json.dumps(M,indent=2)+'\n')
v=json.load(open(A/'public/anatomy/vessel-courses.json'));v['courses']=[row['vesselCourse']for row in M['structures']if row.get('vesselCourse')];v['release']='0.9.156';(A/'public/anatomy/vessel-courses.json').write_text(json.dumps(v,indent=2)+'\n')
(A/'public/anatomy/dsa-surfaces.json').write_text(json.dumps(currentSurface))
(A/'anatomy/source/foramina/revision156-arteries.json').write_text(json.dumps({'changed':changed,'connectorCuffs':portReport},indent=2)+'\n')
(A/'anatomy/source/foramina/revision156-flow-changes.json').write_text(json.dumps(flowIds,indent=2)+'\n')
pkg=json.load(open(A/'package.json'));pkg['version']='0.9.156';(A/'package.json').write_text(json.dumps(pkg,indent=2)+'\n')
print('Saved',len(changed),'nodes and',len(flowIds),'guides',flush=True)
