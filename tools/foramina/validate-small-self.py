from pathlib import Path
import sys,json,numpy as np
A=Path(__file__).resolve().parents[2];sys.path.insert(0,str(A/'tools/foramina'));from geometry import Glb
from facial_surface_contacts import contacts
M=json.load(open(A/'public/anatomy/manifest.json'));rows={r['id']:r for r in M['structures']};loaded={};report=[]
for sid in json.load(open(A/'anatomy/source/foramina/small-changes.json')):
 s=rows[sid];file=s['asset']['file']
 if file not in loaded:loaded[file]=Glb(A/'public/anatomy'/file)
 p,f,n=loaded[file].mesh(s['asset']['node']);pairs,bound=contacts(p,f);r={'id':sid,'materialContacts':int(sum(bound>.002)),'maximumPenetrationBoundMm':float(max(bound,default=0)),'toleranceMm':.002};report.append(r);print(r,flush=True);assert not r['materialContacts'],r
(A/'docs/foramina-batch7-self-contact-validation.json').write_text(json.dumps(report,indent=2))
