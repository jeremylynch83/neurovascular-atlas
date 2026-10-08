from pathlib import Path
import subprocess
ROOT=Path(__file__).resolve().parent;APP=ROOT.parents[1];b=ROOT/'baseline';d=ROOT/'decoded'
for p in (APP/'public/anatomy/models').glob('*.glb'):
 if not (b/p.name).exists():(b/p.name).symlink_to(p)
subprocess.run(['node',str(APP/'tools/decode-posterior-baseline.mjs'),str(b),str(d)],check=True,cwd=APP)
