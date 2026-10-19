from pathlib import Path
import sys,json,numpy as np
A=Path(__file__).resolve().parents[2];sys.path.insert(0,str(A/'tools/foramina'));from geometry import Glb
from whole_surface_contacts import contacts
M=json.load(open(A/'public/anatomy/manifest.json'));rows={r['id']:r for r in M['structures']};selected=set()
for p in (A/'anatomy/source/foramina').glob('*changes.json'):
 for sid in json.load(open(p)):
  if sid in rows and rows[sid].get('asset')and rows[sid]['system']=='artery':selected.add(sid)
loaded={};report=[]
for sid in sorted(selected):
 r=rows[sid];file=r['asset']['file']
 if file not in loaded:loaded[file]=Glb(A/'public/anatomy'/file)
 p,f,n=loaded[file].mesh(r['asset']['node']);pairs,b=contacts(p,f);rec={'id':sid,'triangles':len(f),'materialSelfContacts':int(sum(b>.002)),'maximumPenetrationBoundMm':float(max(b,default=0)),'toleranceMm':.002};report.append(rec);print(rec,flush=True)
(A/'docs/foramina-batch8-repaired-surface-validation.json').write_text(json.dumps(report,indent=2))
