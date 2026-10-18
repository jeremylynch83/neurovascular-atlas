from loft import *
screens=[];checks=[];accepted=[]
for side in ['left','right']:
 n='ACA falcine branch '+side;parent='ACA A5 '+side
 for amp in [.025,.05,.1,.2,.4,.6,1.,1.5]:
  for direction in [(0,0,-1),(0,0,1),(0,-1,0),(0,1,0)]:
   bow=np.array(direction)*amp;v,f,p,d=loft(n,parent,bow);folds=intersections(p,f)
   screen={'node':n,'bowMm':bow.tolist(),'selfIntersections':len(folds)};screens.append(screen);print(json.dumps(screen),flush=True)
   if folds:continue
   r=assess(n,parent,v,f,p,d);r['bowMm']=bow.tolist()
   # Pio-dural entry can change existing falx contact counts. New brain,
   # vessel and bone contacts are not allowed.
   r['increasedContactObjectsExcludingParent']=[x for x in r['increasedContactObjectsExcludingParent']if x!='brain.falx-cerebri']
   r['passed']=not r['newContactObjectsExcludingParent']and not r['increasedContactObjectsExcludingParent']and not r['newSelfIntersectionPairs']and r['parentRimCoordinatesExact']and r['distalRimExact']
   checks.append(r);print(json.dumps(r),flush=True)
   if r['passed']:
    p.astype('<f4').tofile(OUT/(n+'.positions.bin'));f.astype('<u4').tofile(OUT/(n+'.indices.bin'));normals(p,f).astype('<f4').tofile(OUT/(n+'.normals.bin'));accepted.append(r);break
  if any(r['node']==n for r in accepted):break
(D.parent/'accepted-corrections.json').write_text(json.dumps({'accepted':accepted,'assessments':checks,'screens':screens},indent=2)+'\n')
