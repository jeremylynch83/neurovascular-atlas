"""Package both immutable candidates and one shared decoded source tree."""
import sys,zipfile,hashlib,json
from pathlib import Path
root=Path.cwd();dest=Path(sys.argv[1]);dest.mkdir(parents=True,exist_ok=True);prefix='recovered-app-v0.9.51';items=[]
for path in sorted(root.iterdir()):
 if path.is_file() and path.suffix not in ['.tsbuildinfo'] and not path.name.startswith('.'):
  items.append((path,prefix+'/'+path.name))
for name in ['src','public','anatomy','tools','docs','review-v0958','review-v0959','work-v0958','work-v0959']:
 for path in sorted((root/name).rglob('*')):
  if not path.is_file() or '__pycache__' in path.parts or 'decoded' in path.relative_to(root).parts or path.suffix=='.pyc':continue
  # Current normals are kept in full; prior comparison normals are derived
  # from its exact vertices/faces and need not be duplicated in this archive.
  if name=='work-v0958' and path.name.endswith('.normals.bin'):continue
  if name=='work-v0959' and path.name=='package-verification-continuation.json':continue
  items.append((path,prefix+'/'+path.relative_to(root).as_posix()))
source=(root/'work-v0958/decoded').resolve()
for path in sorted(source.rglob('*')):
 if path.is_file():items.append((path,prefix+'/decoded/'+path.relative_to(source).as_posix()))
for name in ['Neurovascular_Atlas_MMA_review_v0.9.59.html','Neurovascular_Atlas_MMA_comparison_v0.9.59.png','README_MMA_v0.9.59.txt','MMA_validation_v0.9.59.json']:
 path=dest/name;assert path.is_file();items.append((path,name))
path=dest/'Neurovascular_Atlas_MMA_checkpoint_v0.9.59.zip'
with zipfile.ZipFile(path,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=6,allowZip64=True) as z:
 for source,archive_name in items:z.write(source,archive_name)
with zipfile.ZipFile(path) as z:
 assert z.testzip() is None
 assert prefix+'/decoded/meshes.json' in z.namelist()
 current=json.loads(z.read(prefix+'/work-v0959/candidate/acceptance-continuation.json'));assert current['mmaNeuralContactPairs']==15 and not current['passed']
 assert 'WORK.parent' in z.read(prefix+'/tools/mma-v0952/common.py').decode()
 for name in ['Posterior cavernous MMA–posterolateral ILT left','MMA posterior cavernous left']:
  suffix='/candidate/'+name+'.positions.bin';assert z.read(prefix+'/work-v0959'+suffix)==z.read(prefix+'/work-v0958'+suffix)
sha=hashlib.sha256()
with path.open('rb') as f:
 for chunk in iter(lambda:f.read(8*1024*1024),b''):sha.update(chunk)
report=dict(file=str(path),bytes=path.stat().st_size,entries=len(items),sha256=sha.hexdigest(),crcPassed=True,sharedDecodedSource=True,leftCavernousRollbackExact=True)
(root/'work-v0959/package-verification-continuation.json').write_text(json.dumps(report,indent=2));print(json.dumps(report,indent=2))
