from geometry import *
import json,time
OUT=ROOT/'candidate';revision=json.loads((OUT/'revision.json').read_text());changed=[r['node'] for r in revision['changed']]
new={}
for n in changed:
 v=np.fromfile(OUT/(n+'.positions.bin'),'<f4').reshape(-1,3).astype(float);f=np.fromfile(OUT/(n+'.indices.bin'),'<u4').reshape(-1,3);new[n]=poly(v,f)
def after(n):return new.get(n,meshes[n].pd)
report={'release':'0.9.29','checkedPairs':0,'newContacts':[],'baselineContacts':[],'resolvedAuditContacts':[]}
audit=json.loads((ROOT.parent/'audit-work/measurements.json').read_text())
for r in audit['previousPosteriorFlaggedPairsRemeasured']:
 if r['contacts'] and r['two'].startswith('vein.'):
  n=contacts(after(r['one']),after(r['two']));report['resolvedAuditContacts'].append({'one':r['one'],'two':r['two'],'baselineAllContacts':r['contacts'],'candidateHalfContacts':n});print(r['one'],r['two'],n,flush=True)
# Test all changed vessels against every potential artery/brain/skull neighbour,
# including partial overlap and changes that touch receiver labels.
for k,n in enumerate(changed):
 for other,m in meshes.items():
  if other==n:continue
  # Only independent compartment conflicts. Arterial collars and venous shared
  # junctions within their own network are inspected separately.
  if m.file==meshes[n].file:continue
  if m.file not in ['brain-context.glb','craniofacial.glb','complete-circulation.glb','complete-anastomoses.glb','venous.glb']:continue
  ap=after(n);bp=after(other);a=np.array(ap.GetBounds()).reshape(3,2);b=np.array(bp.GetBounds()).reshape(3,2)
  if np.any(a[:,1]<b[:,0]) or np.any(b[:,1]<a[:,0]):continue
  report['checkedPairs']+=1
  hits=contacts(ap,bp,True)
  if hits:
   old=contacts(meshes[n].pd,m.pd,True)
   (report['newContacts'] if not old else report['baselineContacts']).append({'one':n,'two':other})
 print('Neighbours',k+1,'/',len(changed),'new',len(report['newContacts']),flush=True)
(OUT/'clearance.json').write_text(json.dumps(report,indent=2)+'\n');print('Saved clearance',report['checkedPairs'],len(report['newContacts']),flush=True)
