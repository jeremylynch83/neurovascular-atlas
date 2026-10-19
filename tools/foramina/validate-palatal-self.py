from pathlib import Path
import sys,json,numpy as np
A=Path(__file__).resolve().parents[2];sys.path.insert(0,str(A/'tools/foramina'));from geometry import Glb
from surface_contacts import contacts
M=json.load(open(A/'public/anatomy/manifest.json'));rows={s['id']:s for s in M['structures']};changes=json.load(open(A/'anatomy/source/foramina/palatal-changes.json'));baseline=json.load(open(A/'anatomy/source/foramina/palatal-source-contacts.json'));loaded={};report=[];tolerance=.002
for sid in changes:
 s=rows[sid];file=s['asset']['file']
 if file not in loaded:loaded[file]=Glb(A/'public/anatomy'/file)
 p,f,n=loaded[file].mesh(s['asset']['node']);pairs,bound=contacts(p,f);material=pairs[bound>tolerance];old=baseline.get(sid);introduced=[]
 if old:
  origin=np.array(old['newFaceToSourceFace']);assert len(origin)==len(f),sid;allowed={tuple(sorted(p))for p in old['sourceNonAdjacentPairs']};source_faces={i for pair in allowed for i in pair}
  for pair in material:
   mapped=tuple(sorted(origin[pair].tolist()))
   if mapped not in allowed and mapped[0]!=mapped[1] and not all(i in source_faces for i in mapped):introduced.append(pair.tolist())
 else:introduced=material.tolist()
 r={'id':sid,'nonAdjacentContacts':len(pairs),'materialContacts':len(material),'inheritedSourceContactPairs':len(material)-len(introduced),'introducedMaterialPairs':introduced,'maximumPenetrationBoundMm':float(max(bound,default=0)),'toleranceMm':tolerance};report.append(r);print(r,flush=True)
(A/'docs/foramina-batch5-self-contact-validation.json').write_text(json.dumps(report,indent=2)+'\n');assert all(not r['introducedMaterialPairs']for r in report),'New material face pairs introduced in the repaired region'
