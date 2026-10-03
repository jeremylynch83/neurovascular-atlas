from pathlib import Path
import gzip
root=Path(__file__).resolve().parents[1]/'dist'
for p in root.rglob('*'):
 if p.is_file() and p.suffix in {'.glb','.json','.js','.css','.svg'} and p.stat().st_size>1024:
  data=p.read_bytes();compressed=gzip.compress(data,compresslevel=9,mtime=0)
  if len(compressed)<len(data)*.95:p.with_name(p.name+'.gz').write_bytes(compressed)
