"""Subdivide moving venous faces in the baseline so curved placement is sampled faithfully."""
from common import *
import shutil
backup=WORK/'unrefined';backup.mkdir(exist_ok=True)
for name in json.loads((WORK/'connected-nodes.json').read_text()):
 if name.startswith('brain.'):continue
 for kind in ['positions','indices']:
  p=DATA/(name+'.'+kind+'.bin');dest=backup/p.name
  if not dest.exists():shutil.copy2(p,dest)
 v,f=load(name,backup)
 for level in range(2):
  # Uniform linear subdivision retains the original piecewise-planar surface.
  edges=np.sort(np.concatenate([f[:,[0,1]],f[:,[1,2]],f[:,[2,0]]]),axis=1)
  unique,inv=np.unique(edges,axis=0,return_inverse=True)
  ids=inv.reshape(3,-1).T+len(v);a,b,c=f.T;ab,bc,ca=ids.T
  f=np.concatenate([np.column_stack([a,ab,ca]),np.column_stack([ab,b,bc]),np.column_stack([ca,bc,c]),np.column_stack([ab,bc,ca])]).astype('<u4')
  v=np.concatenate([v,(v[unique[:,0]].astype(float)+v[unique[:,1]])/2]).astype('<f4')
 v.tofile(DATA/(name+'.positions.bin'));f.tofile(DATA/(name+'.indices.bin'))
 print(name,len(v),len(f),flush=True)
