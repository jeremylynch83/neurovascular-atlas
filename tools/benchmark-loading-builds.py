#!/usr/bin/env python3
"""Opt-in build benchmark. Temporarily translate one non-DSA anastomosis.
Always restore exact source bytes and rebuild, even after a benchmark failure.
No synthetic edit is included in the released model.
"""
import json, shutil, subprocess, time, importlib.util, hashlib
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('packs',ROOT/'tools/build-loading-packs.py');packs=importlib.util.module_from_spec(spec);spec.loader.exec_module(packs)
logs=ROOT/'.build-cache/benchmarks';logs.mkdir(parents=True,exist_ok=True)
report={'release':json.loads((ROOT/'package.json').read_text())['version'],'definition':'Single host, warm installed dependencies. Clean removes dist, generated packs and gzip cache. Timings include validation, pack generation, DSA hash checks, TypeScript, Vite and gzip.','runs':[]}
def run(label):
 start=time.perf_counter();r=subprocess.run(['npm','run','build'],cwd=ROOT,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True);elapsed=time.perf_counter()-start
 (logs/(label+'.log')).write_text(r.stdout)
 if r.returncode:raise RuntimeError(label+' failed: '+r.stdout[-5000:])
 metrics={}
 for line in r.stdout.splitlines():
  for prefix,key in [('Loading packs: ','packs'),('Gzip cache: ','gzip')]:
   if line.startswith(prefix):metrics[key]=json.loads(line[len(prefix):])
 row={'scenario':label,'seconds':round(elapsed,3),**metrics};report['runs'].append(row);print(json.dumps(row),flush=True)
for d in [ROOT/'dist',ROOT/'public/anatomy/packs',ROOT/'.build-cache/gzip']:
 if d.exists():shutil.rmtree(d)
run('clean')
run('unchanged')
files=[ROOT/'public/anatomy/models/complete-anastomoses.glb',ROOT/'anatomy/generated/complete_manifest.json',ROOT/'public/anatomy/vessel-courses.json']
backups={p:p.read_bytes() for p in files}
try:
 doc,blob=packs.read_glb(files[0]);node=doc['nodes'][0];node['translation']=[.01,0,0]
 files[0].write_bytes(packs.glb(doc,blob));h=hashlib.sha256(files[0].read_bytes()).hexdigest()
 full=json.loads(files[1].read_bytes())
 for s in full['structures']:
  if s.get('asset',{}).get('file')=='models/complete-anastomoses.glb' and s.get('vesselCourse'):s['vesselCourse']['geometrySha256']=h
 files[1].write_text(json.dumps(full,indent=2)+'\n')
 export=json.loads(files[2].read_bytes())
 for c in export['courses']:
  if c['geometry']['file']=='models/complete-anastomoses.glb':c['geometrySha256']=h
 files[2].write_text(json.dumps(export,indent=2)+'\n')
 report['syntheticEdit']={'node':node['name'],'translationMm':[.01,0,0],'scope':'One anastomosis. These illustrative connections are excluded from DSA; this does not benchmark DSA regeneration after an injection-vessel edit.'}
 run('single-anastomosis-edit')
 assert report['runs'][-1]['packs']['built']==1
 assert report['runs'][-1]['packs']['assembled']==1
 assert report['runs'][-1]['packs']['reused']==12
finally:
 for p,b in backups.items():p.write_bytes(b)
 run('restored-source')
report['sourceRestoredExactly']=all(p.read_bytes()==b for p,b in backups.items())
(ROOT/'docs/revision151-build-benchmark.json').write_text(json.dumps(report,indent=2)+'\n')
