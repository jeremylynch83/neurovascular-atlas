"""Reject stale or failed family validation before release metadata changes."""
import json,subprocess,sys
from pathlib import Path
APP=Path(__file__).resolve().parents[2]
geo=APP/'docs/validation/fitting-geometry-v0.9.17.json'
tissue=APP/'docs/validation/fitting-surrounding-tissue-v0.9.17.json'
paths=[APP/p for p in ['anatomy/generated/complete_manifest.json','public/anatomy/vessel-courses.json','package.json','package-lock.json']]
reports={p:p.read_bytes() for p in [geo,tissue]};before={p:p.read_bytes() for p in paths}
try:
 for case in ['stale','family-contact']:
  for p,b in reports.items():p.write_bytes(b)
  if case=='stale':
   data=json.loads(reports[geo]);data['authoringGeometryHashes']['arteries']='stale-test-fixture';geo.write_text(json.dumps(data));message='Missing or stale geometry validation'
  else:
   data=json.loads(reports[tissue]);data['checks']=[{'contacts':[{'beforeTriangleContacts':0,'afterTriangleContacts':1}]}];tissue.write_text(json.dumps(data));message='New tissue contacts in edited family'
  result=subprocess.run([sys.executable,str(APP/'tools/brain/publish_fitting.py')],cwd=APP,capture_output=True,text=True)
  assert result.returncode!=0 and message in result.stderr
  assert all(p.read_bytes()==b for p,b in before.items())
  print(f'{case}: rejected; release metadata retained exactly.')
finally:
 for p,b in reports.items():p.write_bytes(b)
