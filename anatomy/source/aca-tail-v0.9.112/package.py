from pathlib import Path
import zipfile,stat,json
R=Path('/workspace/scratch/3da1329b983b');A=R/'atlas/inr-anatomy-atlas-v0.9.91';out=R/'inr-anatomy-atlas-v0.9.112.zip';excluded={'node_modules','dist','.git','.repair-cache','__pycache__'};files=[]
for p in sorted(A.rglob('*')):
 rel=p.relative_to(A)
 if any(x in excluded for x in rel.parts)or p.suffix in ['.pyc','.tsbuildinfo']or not p.is_file():continue
 files.append((p,rel.as_posix()))
with zipfile.ZipFile(out,'w',zipfile.ZIP_DEFLATED,compresslevel=6)as z:
 for p,rel in files:z.write(p,'inr-anatomy-atlas-v0.9.112/'+rel)
with zipfile.ZipFile(out)as z:
 assert z.testzip()is None
 old=zipfile.ZipFile(R/'inr-anatomy-atlas-v0.9.111.zip');before={x.split('/',1)[1]for x in old.namelist()if not x.endswith('/')};after={x.split('/',1)[1]for x in z.namelist()};assert before<=after,sorted(before-after)
 for name in ['anatomy.sh','build-anatomy.sh','docker.sh']:assert(z.getinfo('inr-anatomy-atlas-v0.9.112/'+name).external_attr>>16)&stat.S_IXUSR
 assert json.loads(z.read('inr-anatomy-atlas-v0.9.112/package.json'))['version']=='0.9.112'
print({'path':str(out),'bytes':out.stat().st_size,'files':len(files),'allPriorReleaseFilesRetained':True,'archiveIntegrity':'passed','executableLaunchers':'passed'})
