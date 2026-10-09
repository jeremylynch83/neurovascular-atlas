"""Compact smooth displacement fields fitted to actual petrous/clival surfaces.
All venous labels receive the same coordinate map, retaining shared interfaces.
The outer transverse sinus is checked against the parietal bone as well.
"""
from common import *
from scipy.interpolate import PchipInterpolator
from scipy.ndimage import gaussian_filter1d
vtk.vtkLogger.SetStderrVerbosity(vtk.vtkLogger.VERBOSITY_OFF)
fields=[];screens=[]
bone_names=[n for n in FILES if n.startswith('bone.') and n not in ['bone.mandible','bone.hyoid']]
locators={n:locator(*load(n)) for n in bone_names}
def screen(name,axis,stations,directory=DATA):
 v,f=load(name,directory);rows=[]
 for s in stations:
  p=section(v,f,axis,s)
  if not len(p):continue
  c=(p.min(0)+p.max(0))/2;hits=[]
  for bn,l in locators.items():
   cp,dd=closest(l,np.array([c]));wp,wd=closest(l,p);hits.append((float(wd.min()),bn,cp[0],float(dd[0])))
  gap,bn,cp,cd=min(hits,key=lambda x:x[0]);rows.append(dict(coordinate=float(s),centre=c.tolist(),closest=cp.tolist(),closestBone=bn,minimumWallGapMm=gap,centreGapMm=cd))
 return rows
for side,sign in [('right',1),('left',-1)]:
 for family,axis,stations in [('superior_petrosal',0,sign*np.arange(16.5,27,.5)),('inferior_petrosal',2,np.arange(49,63,.5))]:
  name='vein.'+family+'.'+side;rows=screen(name,axis,stations);screens.append(dict(node=name,axis=axis,baseline=rows));centres=np.array([r['centre'] for r in rows]);deltas=[]
  for r,c in zip(rows,centres):
   d=np.array(r['closest'])-c;deltas.append(d*max(r['minimumWallGapMm']-.35,0)/max(r['centreGapMm'],1e-6))
  deltas=gaussian_filter1d(np.array(deltas),1.4,axis=0)
  # The very medial SPS is the cavernous outlet. Its variable free transition
  # stays fixed; taper the local fit into it rather than shift the entire CS.
  if family=='superior_petrosal':
   weight=smooth((sign*centres[:,0]-18.2)/2.5)*smooth((26-sign*centres[:,0])/3)
  else:weight=smooth((centres[:,2]-50)/3)*smooth((62.5-centres[:,2])/3.5)
  deltas*=weight[:,None]
  fields.append((centres,deltas,family,side))
def field(q):
 delta=np.zeros_like(q)
 for c,d,family,side in fields:
  # Compact inverse-distance interpolation along the local sinus shaft.
  # Euclidean distance also avoids moving the opposite side or remote vessels.
  dist,idx=cKDTree(c).query(q,k=4);w=1/(dist+.35)**2;vec=(d[idx]*w[:,:,None]).sum(1)/w.sum(1)[:,None]
  influence=smooth((7-dist[:,0])/3)
  delta+=vec*influence[:,None]
 return q+delta
previous=json.loads((OUT/'revision.json').read_text()) if (OUT/'revision.json').exists() else {}
new_labels=previous.get('newLabels',[])
changed=[r for r in previous.get('changed',[]) if r['node'] in new_labels]
targets={'vein.'+f+'.'+s for f in ['superior_petrosal','inferior_petrosal'] for s in ['right','left']}
other_vertices=np.concatenate([load(n)[0] for n in FILES if n.startswith('vein.') and n not in targets])
other_tree=cKDTree(other_vertices)
arterial_vertices=np.concatenate([load(n)[0] for n,fn in FILES.items() if fn in ['complete-circulation.glb','complete-anastomoses.glb']])
arterial_tree=cKDTree(arterial_vertices)
for p in OUT.glob('*.bin'):
 if p.name.rsplit('.',2)[0] not in new_labels:p.unlink()
for n in FILES:
 if n not in targets:continue
 v,f=load(n);q=field(v)
 if 'inferior_petrosal' in n:
  q=v+(q-v)*smooth((v[:,2]-50)/3)[:,None]*smooth((63-v[:,2])/3)[:,None]
 shared=other_tree.query(v)[0]<1e-5
 if shared.any():
  distance=cKDTree(v[shared]).query(v)[0]
  q=v+(q-v)*smooth(distance/3.5)[:,None]
  q[shared]=v[shared]
 q=v+(q-v)*smooth((arterial_tree.query(v)[0]-2.0)/2.5)[:,None]
 movement=np.linalg.norm(q-v,axis=1)
 if movement.max()<1e-5:continue
 write(n,q,f);changed.append(dict(node=n,file=FILES[n],vertices=len(v),triangles=len(f),maxShiftMm=float(movement.max()),topologyPreserved=True))
for s in screens:s['candidate']=screen(s['node'],s['axis'],[r['coordinate'] for r in s['baseline']],OUT)
for side,sign in [('right',1),('left',-1)]:
 screens.append(dict(node='vein.transverse.'+side,axis=0,baseline=screen('vein.transverse.'+side,0,sign*np.arange(44,60,2)),status='Original audit omitted the adjacent parietal bone. Full local skull screen shows existing apposition; geometry retained.'))
rev=dict(release='0.9.50',baselineRelease='0.9.49',baselineAssetHashes=json.loads((DATA/'source-assets.json').read_text()),newLabels=new_labels,changed=changed,groups=[dict(reason='Local petrosal surface fitting with fixed native collars; cavernous outlets and all other existing veins retained.',nodes=[r['node'] for r in changed if r['node'] not in new_labels])],method='Compact coordinate field around petrosal shafts, attenuated to zero at every existing shared neighbouring interface; selected new companion and CPA venous tubes.',limitations=['Medial free cavernous-to-petrosal transitions are retained.','Small canal containment cannot be assessed from this skull.'])
(OUT/'revision.json').write_text(json.dumps(rev,indent=2)+'\n');(OUT/'sinus-screens.json').write_text(json.dumps(screens,indent=2)+'\n')
print(json.dumps(changed,indent=2))
