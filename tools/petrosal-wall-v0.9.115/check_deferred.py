from pathlib import Path
import sys,runpy
A=Path(__file__).resolve().parents[2]
if '--registry'not in sys.argv:sys.argv.extend(['--registry',str(A/'anatomy/source/petrosal-wall-v0.9.115/deferred-repairs.json')])
runpy.run_path(str(A/'tools/arterial-review-v0.9.113/check_deferred.py'),run_name='__main__')
