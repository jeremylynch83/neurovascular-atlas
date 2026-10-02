#!/usr/bin/env python3
from pathlib import Path
import hashlib, sys, urllib.request
out=Path(sys.argv[1]); out.mkdir(parents=True,exist_ok=True)
name='TopBrain_Data_Release_Batches1n2nTA36_081726.zip'
dst=out/name
url='https://zenodo.org/records/21972006/files/'+name+'?download=1'
expected='aab94bed377ad71bfbde3f7e26d652c5'
def md5file(p):
    h=hashlib.md5()
    with p.open('rb') as f:
        for b in iter(lambda:f.read(8*1024*1024),b''): h.update(b)
    return h.hexdigest()
if dst.exists():
    md5=md5file(dst)
    if md5==expected: print('TopBrain v3 already downloaded and checksum verified.'); raise SystemExit
    print('Existing archive checksum differs; downloading again.')
print('Downloading official TopBrain v3 archive (~2.0 GB) from Zenodo...')
with urllib.request.urlopen(url) as r, dst.open('wb') as f:
    total=int(r.headers.get('Content-Length') or 0); done=0
    while True:
        b=r.read(8*1024*1024)
        if not b: break
        f.write(b); done+=len(b)
        if total: print(f'  {done/1e9:.2f}/{total/1e9:.2f} GB ({100*done/total:.0f}%)',flush=True)
md5=md5file(dst)
if md5!=expected: raise SystemExit(f'Checksum mismatch: {md5} != {expected}')
print('Download complete; MD5 verified.')
