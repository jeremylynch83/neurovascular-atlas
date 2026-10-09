from common import *
vtk.vtkLogger.SetStderrVerbosity(vtk.vtkLogger.VERBOSITY_OFF)
rev=json.loads((OUT/'revision.json').read_text());changed={r['node'] for r in rev['changed']};calibre=[];comparisons=[]
for name in sorted(changed):
 v,f=load(name);q,g=load(name,OUT)
 if len(v)!=len(q):continue
 axis=int(np.argmax(v.max(0)-v.min(0)));lo=v[:,axis].min()+1;hi=v[:,axis].max()-1;ratios=[]
 for value in np.linspace(lo,hi,32):
  a=section(v,f,axis,value);b=section(q,g,axis,value)
  if len(a)<3 or len(b)<3:continue
  dims=[i for i in range(3) if i!=axis];ra=np.median(np.linalg.norm(a[:,dims]-(a[:,dims].min(0)+a[:,dims].max(0))/2,axis=1));rb=np.median(np.linalg.norm(b[:,dims]-(b[:,dims].min(0)+b[:,dims].max(0))/2,axis=1))
  if ra>1e-7:ratios.append(rb/ra)
 ratios=np.array(ratios);calibre.append(dict(node=name,method='Median contour radius around a bounding-box midpoint in 32 world-axis sections, using the longest baseline extent. Records deformation, not calibrated normal-plane vessel calibre.',axis='xyz'[axis],ratioP05MedianP95=np.percentile(ratios,[5,50,95]).tolist(),p95AbsoluteFractionalRadiusChange=float(np.percentile(np.abs(ratios-1),95))))
for side in ['right','left']:
 suff='' if side=='right' else ' left'
 for art,vein,low,high in [('Vertebral V2 '+side,'vein.vertebral.'+side,-82,-13),('Facial'+suff,'vein.facial.'+side,1,28),('Superficial temporal'+suff,'vein.superficial_temporal.'+side,40,82)]:
  a,f=load(art);v,g=load(vein);q,h=load(vein,OUT);rows=[]
  for z in np.arange(low,high,2.):
   pa=section(a,f,2,z);pb=section(v,g,2,z);pc=section(q,h,2,z)
   if not len(pa) or not len(pb) or not len(pc):continue
   ca=(pa.min(0)+pa.max(0))/2;cb=(pb.min(0)+pb.max(0))/2;cc=(pc.min(0)+pc.max(0))/2;rows.append(dict(z=z,beforeDelta=(cb-ca).tolist(),afterDelta=(cc-ca).tolist(),beforeSeparationMm=float(np.linalg.norm(cb-ca)),afterSeparationMm=float(np.linalg.norm(cc-ca))))
  comparisons.append(dict(artery=art,vein=vein,sections=rows,medianSeparationBeforeMm=float(np.median([r['beforeSeparationMm'] for r in rows])),medianSeparationAfterMm=float(np.median([r['afterSeparationMm'] for r in rows]))))
 for name,lm in [('Hypoglossal branch'+suff,'hypoglossal'),('Labyrinthine '+side,'internal-acoustic')]:
  m=json.loads((WORK.parent/'inr-anatomy-atlas-v0.9.49/anatomy/generated/complete_manifest.json').read_text());s=next(s for s in m['structures'] if s['id']=='landmark.'+lm+'.'+side);point=s['landmark']['point'];v,f=load(name);q,g=load(name,OUT);_,old=closest(locator(v,f),[point]);_,new=closest(locator(q,g),[point]);comparisons.append(dict(vessel=name,guide=s['id'],status=s['landmark']['status'],guideToWallBeforeMm=float(old[0]),guideToWallAfterMm=float(new[0]),notIndependentCanalValidation=True))
 name='MMA frontal'+suff;v,f=load(name);q,g=load(name,OUT);bones=[load(n) for n in ['bone.frontal','bone.temporal.'+side,'bone.sphenoid','bone.parietal.'+side]];ls=[locator(a,b) for a,b in bones];r=[]
 for z in [85,87,89,91,93,103,105]:
  old=section(v,f,2,z);new=section(q,g,2,z);r.append(dict(z=z,minWallGapBeforeMm=float(min(closest(l,old)[1].min() for l in ls)),minWallGapAfterMm=float(min(closest(l,new)[1].min() for l in ls))))
 comparisons.append(dict(vessel=name,innerTableScreen=r))
attachments=[]
for family in ['acoustic','meningeal']:
 for side in ['right','left']:
  x=np.load(OUT/(family+'-network-'+side+'.npz'));pd=poly(x['v'].astype(float),x['f']);ip=vtk.vtkImplicitPolyDataDistance();ip.SetInput(pd)
  child=('Labyrinthine '+side) if family=='acoustic' else ('MMA frontal'+(' left' if side=='left' else ''));parent=('AICA '+side) if family=='acoustic' else ('Middle meningeal'+(' left' if side=='left' else ''));v,f=load(child);a,b=load(parent);shared=v[cKDTree(a).query(v)[0]<1e-5];d=np.array([ip.EvaluateFunction(p) for p in shared]);centre=shared.mean(0);inside=float(ip.EvaluateFunction(centre));attachments.append(dict(family=family,side=side,parent=parent,sourceSharedVertices=len(shared),insideNativeInterfaceVertices=int(np.sum(d<=0)),fractionInside=float(np.mean(d<=0)),interfaceCentreSignedDistanceMm=inside,continuousVolumeAttachment=inside<0,scope='Volume connection at the native parent location. Whole-atlas surface welding is not claimed.'))
assert all(r['continuousVolumeAttachment'] for r in attachments)
out=dict(release='0.9.49',calibre=calibre,comparisons=comparisons,attachments=attachments)
(OUT/'metrics.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out['attachments'],indent=2));print(json.dumps(comparisons,indent=2))
