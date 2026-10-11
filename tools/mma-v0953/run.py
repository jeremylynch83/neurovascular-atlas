"""Reproduce the candidate from the accepted atlas. Rejection is deliberate.
No public model is changed by this command.
"""
from pathlib import Path
import subprocess,sys,os
app=Path(__file__).resolve().parents[2];work=Path(sys.argv[1] if len(sys.argv)>1 else 'work-v0953').resolve();work.mkdir(exist_ok=True,parents=True);tool=app/'tools/mma-v0953';env=os.environ.copy();env.update(OPENBLAS_NUM_THREADS='1',OMP_NUM_THREADS='1')
def run(name,args=()):subprocess.run([sys.executable,str(tool/name),str(work),*args],cwd=app,env=env,check=True)
subprocess.run(['node','tools/decode-posterior-baseline.mjs','public/anatomy/models',str(work/'decoded')],cwd=app,env=env,check=True)
run('extract.py')
# The trunk and frontal source curves supplied with this review are recovered
# from the exact accepted assets. Preserve those before using a new work path.
for name in ['Middle meningeal','Middle meningeal left','MMA frontal','MMA frontal left']:
 if not (work/(name+'.curve.npz')).exists():raise SystemExit('Copy the supplied '+name+'.curve.npz into the work directory first.')
for name,args in [('reconstruct.py',['3.5']),('refit_context.py',['1.0']),('tubular_rebuild.py',[]),('meningeal.py',[]),('validate.py',[]),('self_check.py',[]),('check_components.py',[]),('render.py',[])]:run(name,args)
run('assess.py') # exits 2 when the candidate fails. Export is never automatic.
