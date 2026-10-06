"""Independent triangle-wall and attachment checks for the staged revision."""
import json,time
from scipy.spatial import cKDTree,ConvexHull
from geometry import *
OUT=ROOT/'candidate';proposal=json.loads((OUT/'revision.json').read_text());changed={r['node'] for r in proposal['changed']}
for k in changed:meshes[k].new=np.fromfile(OUT/(k+'.positions.bin'),'<f4').reshape(-1,3).astype(float)
newpd={k:poly(m.new,m.f) if k in changed else m.pd for k,m in meshes.items()}
report={'release':'0.9.22','baseline':'0.9.21','proposedPonsAdvanceMm':proposal['additionalPonsAmplitudeMm'],'proposedMidbrainAdvanceMm':proposal['additionalMidbrainAmplitudeMm'],'contacts':[],'newUnintendedContactPairs':[],'checks':{},'passed':False,'scope':'Actual triangle surfaces, new intersection pairs, shared material interfaces, sampled anterior-wall adherence and relative section calibre. Existing atlas contacts are recorded separately; open tissue skins do not prove solid containment.'}
def save(): (OUT/'validation-progress.json').write_text(json.dumps(report,indent=2,default=lambda value:value.item() if isinstance(value,np.generic) else value)+'\n')
def check(a,b,domain):
 new=contacts(newpd[a],newpd[b],True);old=contacts(meshes[a].pd,meshes[b].pd,True) if new else 0
 if old or new:report['contacts'].append({'domain':domain,'one':a,'two':b,'baselineContact':bool(old),'newContact':bool(new)})
 if new and not old:
  # Exact source interfaces are distinguished from unintended crossings.
  ta=cKDTree(meshes[b].v);shared=int((ta.query(meshes[a].v)[0]<.0007).sum())
  if shared<3:report['newUnintendedContactPairs'].append({'domain':domain,'one':a,'two':b})
 return old,new

bones=[k for k,m in meshes.items() if m.file=='craniofacial.glb'];stem=[k for k in meshes if any(t in k for t in ['brain.pons.','brain.midbrain.','brain.base-of-peduncle.','brain.medulla-oblongata.'])]
vascular=[k for k in changed if meshes[k].file in ['complete-circulation.glb','venous.glb']]
# Keep restored clival geometry stationary and independently check it against
# the advancing brainstem, basilar artery and all changed local vessels.
for k in stem+vascular:check(k,'vein.basilar_plexus','restored-plexus')
print('Plexus wall checks complete',len(report['newUnintendedContactPairs']),flush=True);save()
for k in changed:
 for b in bones:check(k,b,'bone')
print('Skull wall checks complete',len(report['newUnintendedContactPairs']),flush=True);save()
# Changed vascular walls versus every actual tissue skin (reference sheets and
# intentional perforator entries are listed separately).
manifest=json.loads((ROOT/'app/public/anatomy/manifest.json').read_text())
ref={r['asset']['node'] for r in manifest['structures'] if r.get('asset',{}).get('file')=='models/brain-context.glb' and r.get('anatomy',{}).get('category') in ['ventricular_system','sulcal_landmarks']}
ref|={k for k in meshes if any(t in k for t in ['ventricle','aqueduct','sulcus','fissure','lat-fis','choroid-plexus'])}
tissue=[k for k,m in meshes.items() if m.file=='brain-context.glb' and k not in ref]
for i,k in enumerate(vascular):
 for b in tissue:
  before=len(report['newUnintendedContactPairs']);old,new=check(k,b,'tissue')
  if len(report['newUnintendedContactPairs'])>before and meshes[k].file=='complete-circulation.glb' and any(t in k.lower() for t in ['perforator','paramedian']) and any(r.get('asset',{}).get('node')==k and b in r.get('vesselCourse',{}).get('targetStructureIds',[]) for r in manifest['structures']):
   report.setdefault('intentionalArterialEntries',[]).append(report['newUnintendedContactPairs'].pop())
 if i%12==0:print('Tissue walls',i+1,'/',len(vascular),'new unintended pairs',len(report['newUnintendedContactPairs']),flush=True);save()
# Brainstem shape against neighbouring fixed/moving parenchyma and dural skins.
for k in [k for k in changed if meshes[k].file=='brain-context.glb']:
 for b in tissue:
  if k==b or (b in changed and b<k):continue
  check(k,b,'tissue-interface')
print('Tissue interface checks complete',len(report['newUnintendedContactPairs']),flush=True);save()
arteries=[k for k,m in meshes.items() if m.file=='complete-circulation.glb'];veins=[k for k,m in meshes.items() if m.file=='venous.glb']
for i,k in enumerate(arteries):
 for b in veins:
  if k in changed or b in changed:check(k,b,'artery-vein')
 if i%100==0:print('Crossings',i,'/',len(arteries),flush=True);save()
print('Vascular crossing checks complete',len(report['newUnintendedContactPairs']),flush=True);save()
# Material interfaces: equal input coordinates must stay equal, including
# the boundary between a transported vessel and a stationary dural collector.
for file in ['brain-context.glb','complete-circulation.glb','venous.glb']:
 selected=[m for m in meshes.values() if m.file==file];old=np.concatenate([m.v for m in selected]);new=np.concatenate([m.new for m in selected]);_,inverse=np.unique(old,axis=0,return_inverse=True);order=np.argsort(inverse);same=np.diff(inverse[order])==0;gap=np.linalg.norm(np.diff(new[order],axis=0)[same],axis=1).max(initial=0)
 report['checks'].setdefault('sharedInterfaces',[]).append({'file':file,'maximumGapMm':float(gap),'passed':gap<.001})
# Core exposed wall adherence in the anterior pons and midbrain.
sl=[locator(combine(stem,after=s)) for s in [False,True]]
for k in ['Basilar','vein.anterior_pontine','vein.anterior_pontomesencephalic','vein.transverse_pontine.left','vein.transverse_pontine.right']:
 m=meshes[k];indices=np.flatnonzero((m.v[:,2]>45)&(m.v[:,2]<81)&(abs(m.v[:,0]-.65)<13));indices=indices[::max(1,len(indices)//1800)];values=[[],[]]
 for i in indices:
  for state,loc in enumerate(sl):
   p=(m.new if state else m.v)[i];ys=ray(loc,p[0],p[2])
   if ys:values[state].append(p[1]-max(ys))
 row={'node':k,'states':[]}
 for val in values:
  val=np.array(val);row['states'].append({'samples':len(val),'minimumSignedGapMm':float(val.min()) if len(val) else None,'medianSignedGapMm':float(np.median(val)) if len(val) else None,'wallSamplesBehindExposedSurface':int((val<-.05).sum())})
 row['noAdditionalWallSamplesBehindSurface']=row['states'][1]['wallSamplesBehindExposedSurface']<=row['states'][0]['wallSamplesBehindExposedSurface'];report['checks'].setdefault('anteriorWallAdherence',[]).append(row)
# Basilar separation from stationary clival plexus, measured on all wall points.
pl=locator(meshes['vein.basilar_plexus'].pd);dist=[close(pl,p)[1] for p in meshes['Basilar'].new];report['checks']['basilarPlexusWallClearanceMm']={'minimumSampled':float(min(dist)),'median':float(np.median(dist)),'sampleCount':len(dist)}
# Relative calibre on material sections of the primary basilar and anterior veins.
for name,axis,stations in [('Basilar',2,np.arange(48,77,3)),('vein.anterior_pontine',2,np.arange(47,65,3)),('vein.anterior_pontomesencephalic',2,np.arange(69,78,2)),('vein.transverse_pontine.left',0,[-12,-8,-4]),('vein.transverse_pontine.right',0,[5,9,13])]:
 m=meshes[name];data=poly(m.v,m.f);arr=numpy_to_vtk(m.new,deep=True);arr.SetName('transported');data.GetPointData().AddArray(arr);ratios=[]
 for level in stations:
  origin=np.zeros(3);origin[axis]=level;normal=np.zeros(3);normal[axis]=1;plane=vtk.vtkPlane();plane.SetOrigin(origin);plane.SetNormal(normal);cut=vtk.vtkCutter();cut.SetInputData(data);cut.SetCutFunction(plane);cut.Update();pd=cut.GetOutput()
  if pd.GetNumberOfPoints()<5:continue
  p=vtk_to_numpy(pd.GetPoints().GetData());q=vtk_to_numpy(pd.GetPointData().GetArray('transported'));other=[j for j in range(3) if j!=axis]
  # Material-section width in the source plane isolates radius changes from
  # the harmless global anterior translation of that section.
  before=p[:,other];after=q[:,other];theta=np.linspace(0,np.pi,180,endpoint=False);direction=np.c_[np.cos(theta),np.sin(theta)];bw=np.ptp(before@direction.T,axis=0);aw=np.ptp(after@direction.T,axis=0);ok=bw>1e-5;ratios.append({'levelMm':float(level),'minimumWidthRatio':float((aw[ok]/bw[ok]).min()),'maximumWidthRatio':float((aw[ok]/bw[ok]).max())})
 report['checks'].setdefault('relativeMaterialCalibre',[]).append({'node':name,'sections':ratios,'passed':all(r['minimumWidthRatio']>.88 and r['maximumWidthRatio']<1.12 for r in ratios)})
report['checks']['restoredPlexusAndCavernousPositionsUnchanged']=all(np.array_equal(meshes[k].v,meshes[k].new) for k in proposal['protectedLabels'] if k in meshes)
report['checks']['cerebellarSCADistalSurfacesUnchanged']=all(np.array_equal(m.v,m.new) for k,m in meshes.items() if k.startswith('SCA ') and any(t in k for t in ['hemispheric','vermian']))
report['passed']=not report['newUnintendedContactPairs'] and all(r['passed'] for r in report['checks']['sharedInterfaces']) and all(r['passed'] for r in report['checks']['relativeMaterialCalibre']) and all(r['noAdditionalWallSamplesBehindSurface'] for r in report['checks']['anteriorWallAdherence']) and report['checks']['basilarPlexusWallClearanceMm']['minimumSampled']>.4
(OUT/'validation.json').write_text(json.dumps(report,indent=2,default=lambda value:value.item() if isinstance(value,np.generic) else value)+'\n');print('PASSED',report['passed'],'failures',report['newUnintendedContactPairs'],flush=True)
