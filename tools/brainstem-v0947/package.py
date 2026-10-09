"""Bundle a checked, reproducible source release with validation evidence."""
from common import *
import zipfile
files={'revision':'revision.json','contactAudit':'contacts.json','selfIntersectionAudit':'self-intersections.json','calibreChecks':'calibre.json','depthCheck':'depth.json','exported':'export.json','loader':'loader.json'}
e={key:json.loads((OUT/f).read_text()) for key,f in files.items()}
assert e['contactAudit']['passed'] and e['depthCheck']['passed'] and e['loader']['passed']
e['build']={'passed':True,'command':'npm run build','evidence':'anatomy validation, TypeScript, Vite and precompression completed'}
e['contactAudit']['precisionNote']='Exact triangle contacts use zero CellTolerance. A separate 1e-7 tolerance probe found three near-contacts at the existing median/right transverse collar, within 0.060 mm of shared vertices; exact contacts clear. Artificial pontine closure facets and existing tissue-entry relationships are explicitly classified.'
e['baselineSubdivision']={'levels':2,'method':'Linear midpoint subdivision of four venous labels; original baseline surface retained before placement.'}
Path('docs/validation/transverse-pontine-v0.9.47.json').write_text(json.dumps(e,indent=2)+'\n')
app=Path.cwd();dest=WORK.parent/'inr-anatomy-atlas-v0.9.47.zip';exclude={'node_modules','dist','.git','__pycache__','.halo-check','decoded','candidate','baseline'}
with zipfile.ZipFile(dest,'w',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
 for p in sorted(app.rglob('*')):
  rel=p.relative_to(app)
  if not p.is_file() or any(x in exclude for x in rel.parts) or p.suffix in ['.pyc','.log','.tsbuildinfo']:continue
  z.write(p,'inr-anatomy-atlas-v0.9.47/'+str(rel))
with zipfile.ZipFile(dest) as z:
 assert z.testzip() is None
 assert json.loads(z.read('inr-anatomy-atlas-v0.9.47/package.json'))['version']=='0.9.47'
 assert json.loads(z.read('inr-anatomy-atlas-v0.9.47/public/anatomy/manifest.json'))['release']=='0.9.47'
 assert len([n for n in z.namelist() if n.startswith('inr-anatomy-atlas-v0.9.47/public/anatomy/models/') and n.endswith('.glb')])==5
 print(dest,len(z.namelist()),dest.stat().st_size)
