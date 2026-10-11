"""Read-only geometry validation of the recovered reconstruction checkpoint.

Run from a copy of accepted v0.9.51. This command deliberately exits 2 while
any reconstruction gate fails. It never exports candidate geometry.
"""
from pathlib import Path
import subprocess,sys,os,json,hashlib
app=Path(__file__).resolve().parents[2]
work=Path(sys.argv[1] if len(sys.argv)>1 else 'work-v0954').resolve()
rev=json.loads((work/'candidate/revision.json').read_text())
for n,h in rev['baselineAssetHashes'].items():
    assert hashlib.sha256((app/'public/anatomy/models'/n).read_bytes()).hexdigest()==h,'Wrong accepted baseline: '+n
env=os.environ.copy();env.update(OPENBLAS_NUM_THREADS='1',OMP_NUM_THREADS='1')
subprocess.run(['node','tools/decode-posterior-baseline.mjs','public/anatomy/models',str(work/'decoded')],cwd=app,env=env,check=True)
steps=[('check_smooth_field.py',['--tree','--cortical']),('self_check.py',['--arterial-only']),('self_check.py',['--venous-only']),('self_check.py',['--brain-only']),('check_mma_contacts.py',[]),('check_paired_veins.py',[]),('assess_checkpoint.py',[])]
if (work/'candidate/receiver-implicit-union-right.npz').exists():
    steps[-1:-1]=[('finish_receiver_seams.py',[]),('check_receiver_neighbours.py',[]),('check_reference_corridor.py',[])]
for name,args in steps:
    subprocess.run([sys.executable,str(app/'tools/mma-v0952'/name),str(work),*args],cwd=app,env=env,check=True)

