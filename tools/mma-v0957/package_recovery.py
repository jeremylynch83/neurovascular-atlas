"""Save a self-contained recovery package without promoting failed anatomy."""
import sys,json,hashlib,zipfile
from pathlib import Path
root=Path.cwd();dest=Path('/workspace/scratch/687560554b74/deliverables')
out=dest/'Neurovascular_Atlas_MMA_checkpoint_v0.9.57.zip'
acceptance=json.loads((root/'work-v0957/candidate/acceptance.json').read_text())
assert acceptance['passed']is False
files={}
def addtree(directory,prefix):
 for p in sorted(directory.rglob('*')):
  rel=p.relative_to(directory)
  if not p.is_file()or p.is_symlink()or '__pycache__'in rel.parts or any(part.startswith('.')for part in rel.parts):continue
  if p.suffix in ['.pyc','.br','.gz']:continue
  files[prefix+'/'+str(rel)]=p
app='recovered-app-v0.9.51'
for name in ['src','public','anatomy','tools','docs','review-v0957']:
 p=root/name
 if p.exists():addtree(p,app+'/'+name)
for p in sorted(root.iterdir()):
 if p.is_file()and not p.name.startswith('.')and (p.suffix in ['.json','.ts','.js','.html','.sh']or p.name.startswith(('README','LICENSE','COPYING'))):files[app+'/'+p.name]=p
for name in ['work-v0956-outward','work-v0957']:
 addtree(root/name,app+'/'+name)
# The current source reference is physically included once, not as a symlink.
addtree(root/'work-v0954/decoded',app+'/work-v0957/decoded')
for name in ['SkeletalSystem100.fbx','NervousSystem100.fbx']:
 files['native-source/'+name]=Path('/workspace/scratch/687560554b74/recovered_sources')/name
for name in ['README_MMA_v0957.txt','Neurovascular_Atlas_MMA_review_v0.9.57.html','MMA_geometry_comparison_v0957.png']:
 files[name]=dest/name
with zipfile.ZipFile(out,'w',zipfile.ZIP_DEFLATED,compresslevel=6,allowZip64=True)as z:
 for i,(name,p)in enumerate(files.items()):
  z.write(p,name)
  if i%1000==0:print('Packaged',i,'of',len(files),flush=True)
with zipfile.ZipFile(out)as z:
 assert z.testzip()is None
 for name,expected in acceptance['candidateBufferSha256'].items():
  assert hashlib.sha256(z.read(app+'/work-v0957/candidate/'+name)).hexdigest()==expected,name
 for name,expected in acceptance['acceptedAssetSha256'].items():
  assert hashlib.sha256(z.read(app+'/public/anatomy/models/'+name)).hexdigest()==expected,name
 assert z.read('native-source/SkeletalSystem100.fbx')==files['native-source/SkeletalSystem100.fbx'].read_bytes()
report=dict(filename=str(out),bytes=out.stat().st_size,entries=len(files),crcPassed=True,candidateBuffersVerified=len(acceptance['candidateBufferSha256']),sourcePublicAssetsVerified=len(acceptance['acceptedAssetSha256']),acceptedApp='0.9.51',candidateRelease='0.9.57',candidateAccepted=False,sha256=hashlib.sha256(out.read_bytes()).hexdigest())
(root/'work-v0957/package-verification.json').write_text(json.dumps(report,indent=2));print(json.dumps(report),flush=True)
