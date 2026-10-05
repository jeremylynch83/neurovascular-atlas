"""Rebuild from the supplied compact seed in an isolated authoring directory."""
import hashlib,json,sys,tempfile,shutil
from pathlib import Path
import rebuild_central_branches as fitter

def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def main():
 app=fitter.APP;expected=sha(app/'.authoring/central-rebuilt-trial.glb')
 with tempfile.TemporaryDirectory(prefix='central-reproduction-',dir=app/'.authoring') as directory:
  root=Path(directory)
  for folder in ['.authoring','docs/validation','public/anatomy/models']:(root/folder).mkdir(parents=True)
  for name in ['arteries-baseline.glb','bones-baseline.glb','central-primary-seed.glb']:(root/'.authoring'/name).symlink_to(app/'.authoring'/name)
  (root/'public/anatomy/models/brain-context.glb').symlink_to(app/'public/anatomy/models/brain-context.glb')
  fitter.APP=root;sys.argv=['rebuild_central_branches.py','--experimental','--primary-checkpoint',str(root/'.authoring/central-primary-seed.glb')]
  fitter.main();actual=sha(root/'.authoring/central-rebuilt-trial.glb');fitter.APP=app
  if actual!=expected:shutil.copyfile(root/'.authoring/central-rebuilt-trial.glb',app/'.authoring/central-reproduction-difference.glb')
  report={'release':'0.9.18','suppliedPrimarySeedSha256':sha(app/'anatomy/source/brain/trials/central-primary-seed-v0.9.18.glb'),'decodedPrimarySeedSha256':sha(app/'.authoring/central-primary-seed.glb'),'expectedAuthoringSha256':expected,'reproducedAuthoringSha256':actual,'byteIdentical':actual==expected,'isolatedFromAppAssets':True}
  (app/'docs/validation/central-reproduction-v0.9.18.json').write_text(json.dumps(report,indent=2)+'\n')
  assert actual==expected,'Full reconstruction differs from accepted authoring asset'
 print('Full reconstruction from compact seed is byte-identical.',flush=True)
if __name__=='__main__':main()
