"""Content-addressed gzip cache survives Vite's dist clean, with exact output reuse."""
from pathlib import Path
import gzip, hashlib, json, os
root=Path(__file__).resolve().parents[1]
cache=root/'.build-cache/gzip';cache.mkdir(parents=True,exist_ok=True)
built=reused=0
for p in (root/'dist').rglob('*'):
 if p.is_file() and p.suffix in {'.html','.xml','.glb','.bin','.json','.js','.css','.svg'} and p.stat().st_size>1024:
  data=p.read_bytes();key=hashlib.sha256(b'gzip-level9-mtime0-v1\0'+data).hexdigest();entry=cache/(key+'.gz')
  if entry.exists():compressed=entry.read_bytes();reused+=1
  else:
   compressed=gzip.compress(data,compresslevel=9,mtime=0)
   temporary=entry.with_suffix('.tmp-'+str(os.getpid()));temporary.write_bytes(compressed);temporary.replace(entry);built+=1
  target=p.with_name(p.name+'.gz')
  if len(compressed)<len(data)*.95:target.write_bytes(compressed)
  elif target.exists():target.unlink()
print('Gzip cache: '+json.dumps({'built':built,'reused':reused}))
