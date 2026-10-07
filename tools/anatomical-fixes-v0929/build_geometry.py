"""Connected correction candidates. Identical coordinate fields preserve shared joins."""
from geometry import *
from extract_curves import extract
from scipy.interpolate import RBFInterpolator
import hashlib
OUT=ROOT/'candidate';OUT.mkdir(exist_ok=True)
M=json.loads((ROOT/'baseline/manifest.json').read_text());rows={r['id']:r for r in M['structures']}
def bump(v,centre,extent,delta,plateau=.55):
 d=np.linalg.norm((v-np.asarray(centre))/extent,axis=1);w=1-smooth((d-plateau)/(1-plateau));return w[:,None]*np.asarray(delta)
def venous_field(v):
 return bump(v,[7,-54.5,79],[7,7,7],[-.5,-1.5,-1.9],.35)
changed=[]
for n,m in meshes.items():
 if m.file!='venous.glb':continue
 m.new=m.v+venous_field(m.v)
 if np.max(np.linalg.norm(m.new-m.v,axis=1))>1e-7:changed.append(n)
print('Local venous adjustment',len(changed),flush=True)
# Repartition the unmodified ICA surface at the independent, pre-existing estimated
# proximal dural-ring height. No sinus sleeve, vessel movement or bone carving.
partitions={}
for side in ['right','left']:
 a=meshes[f'ICA cavernous {side}'];b=meshes[f'ICA paraophthalmic {side}']
 ring=rows[f'landmark.ica.dural-rings.{side}']['landmark']['course'][0]
 height=ring[2];take=a.v[a.f].mean(1)[:,2]>height
 fa=a.f[~take];fb=np.vstack([b.f,a.f[take]+len(b.v)]);vb=np.vstack([b.v,a.v])
 def compact(v,f):
  used,inv=np.unique(f,return_inverse=True);return v[used],inv.reshape(-1,3).astype(np.uint32)
 vbnew=np.vstack([b.new,a.new]);a.new,af=compact(a.new,fa);b.new,bf=compact(vbnew,fb)
 partitions[a.name]=af;partitions[b.name]=bf;changed.extend(n for n in [a.name,b.name] if n not in changed)
 partitions[side]={'heightMm':height,'definition':'NYU cavernous to paraophthalmic at estimated proximal dural ring','movedTriangles':int(take.sum()),'uncertainty':'No segmented dural ring; provisional reference boundary'}
# Candidate field for pericallosal A3/A4: supported by a callosal-sulcal reference,
# accepted only after the connected regional family clears neighbours.
if '--aca-trial' in __import__('sys').argv:
 controls=[];deltas=[]
 loc=locator(meshes['brain.corpus-callosum'].pd)
 for side in ['right','left']:
  for seg in ['A2','A3','A4','A5']:
   n=f'ACA {seg} {side}'
   if n not in meshes:continue
   q,rad,_,_=extract(meshes[n])
   for p,r in zip(q[::10],rad[::10]):
    target,dist=close(loc,p);direction=(p-target)/max(dist,1e-9)
    # A2 lower shaft fixed, rising towards the genu. A5 smoothly returns to its
    # retained route at the posterior callosal limit; preserve calibre controls.
    w=1. if seg in ['A3','A4'] else float(smooth((p[2]-97)/14)) if seg=='A2' else float(smooth((p[1]+94)/24))
    controls.append(p);deltas.append(w*((target+direction*(r+2.0))-p))
 controls=np.asarray(controls);deltas=np.asarray(deltas)
 # Average duplicates and nearby opposed labels before interpolation.
 keys=np.round(controls,2);_,ix=np.unique(keys,axis=0,return_index=True);controls=controls[ix];deltas=deltas[ix]
 tree=__import__('scipy.spatial',fromlist=['cKDTree']).cKDTree(controls)
 rb=RBFInterpolator(controls,deltas,kernel='thin_plate_spline',smoothing=1.0,neighbors=20)
 for n,m in meshes.items():
  if m.file!='complete-circulation.glb' or n in partitions:continue
  d=tree.query(m.v)[0];mask=d<19
  if not mask.any():continue
  delta=np.zeros_like(m.v);delta[mask]=rb(m.v[mask])*(1-smooth((d[mask]-4)/15))[:,None]
  m.new=m.v+delta
  if np.max(np.linalg.norm(delta,axis=1))>1e-7:changed.append(n)
 print('ACA trial labels',len(changed),flush=True)
# Recompute normals on the welded complete asset skin, keeping port seams smooth.
for file in {meshes[n].file for n in changed}:
 names=[n for n in meshes if meshes[n].file==file];vv=[];ff=[];offset=0
 for n in names:
  m=meshes[n];v=m.new;f=partitions.get(n,m.f);vv.append(v);ff.append(f+offset);offset+=len(v)
 v=np.vstack(vv);f=np.vstack(ff);_,first,inv=np.unique(v.astype('<f4'),axis=0,return_index=True,return_inverse=True);uv=v[first];uf=inv[f]
 tri=uv[uf];fn=np.cross(tri[:,1]-tri[:,0],tri[:,2]-tri[:,0]);norm=np.zeros_like(uv)
 for j in range(3):np.add.at(norm,uf[:,j],fn)
 norm/=np.maximum(np.linalg.norm(norm,axis=1)[:,None],1e-20);norm=norm[inv];offset=0
 for n in names:
  m=meshes[n];count=len(m.new)
  if n in changed:
   m.new.astype('<f4').tofile(OUT/(n+'.positions.bin'));partitions.get(n,m.f).astype('<u4').tofile(OUT/(n+'.indices.bin'));norm[offset:offset+count].astype('<f4').tofile(OUT/(n+'.normals.bin'))
  offset+=count
revision={'release':'0.9.29','baselineRelease':'0.9.28','newLabels':[],'baselineAssetHashes':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in (ROOT/'baseline').glob('*.glb')},'changed':[{'node':n,'file':meshes[n].file,'maximumDisplacementMm':float(np.linalg.norm(meshes[n].new-meshes[n].v,axis=1).max()) if n not in partitions else 0,'topology':'retained' if n not in partitions else 'repartitioned original triangles'} for n in changed],'icaPartitions':{s:partitions[s] for s in ['right','left']}}
(OUT/'revision.json').write_text(json.dumps(revision,indent=2)+'\n');print('Saved candidate',len(changed),flush=True)
