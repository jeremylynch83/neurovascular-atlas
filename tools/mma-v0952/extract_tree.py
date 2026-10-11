from common import *
import importlib.util
from types import SimpleNamespace
p=Path(__file__).resolve().parents[1]/'brainstem-quality-v0948/extract_curves.py'
spec=importlib.util.spec_from_file_location('sections_extract',p)
mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
names=[n for n in FILES if n.startswith('MMA ') or n.startswith('Middle meningeal')]
for n in names:
    path=WORK/(n+'.curve.npz')
    if path.exists():continue
    v,f=load(n)
    q,r,param,tt=mod.extract(SimpleNamespace(v=v,f=f))
    np.savez(path,q=q,r=r,param=param,tt=tt)
    print(n,len(q),np.percentile(r,[10,50,90]).round(3).tolist(),flush=True)
