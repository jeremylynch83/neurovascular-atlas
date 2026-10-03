#!/usr/bin/env python3
"""Offline integration tests: real Git; simulated Docker, gh and HTTP."""
import json, os, shutil, subprocess, tempfile, zipfile
from pathlib import Path

APP = Path(__file__).resolve().parent / 'app'
if not APP.is_dir(): APP = Path(__file__).resolve().parents[1]
SCRIPT = APP / 'inr-anatomy.sh'

def run(args, env=None, ok=True):
    p = subprocess.run(list(map(str, args)), env=env, text=True, capture_output=True)
    if ok and p.returncode:
        raise AssertionError(f'{args}: {p.returncode}\n{p.stdout}\n{p.stderr}')
    return p

with tempfile.TemporaryDirectory(prefix='inr-installer-tests-') as tmp:
    root = Path(tmp)
    bindir = root/'bin'; bindir.mkdir()
    mock = '''#!/usr/bin/env python3
import json,os,sys
from pathlib import Path
s=Path(os.environ['MOCK_STATE']); s.mkdir(exist_ok=True)
cmd=Path(sys.argv[0]).name; a=sys.argv[1:]
with (s/'calls').open('a') as f: f.write(cmd+' '+repr(a)+'\\n')
if cmd=='sleep': sys.exit(0)
if cmd=='curl':
 if os.environ.get('MOCK_STALE'): print('{"release":"0.3.0"}'); sys.exit(0)
 if not (s/'running').exists(): sys.exit(22)
 print(json.dumps({'release':(s/'running').read_text()})); sys.exit(0)
if cmd=='docker':
 if a[0]=='inspect':
  if not (s/'running').exists(): sys.exit(1)
  print('sha256:'+ (s/'running').read_text())
 elif a[0]=='build':
  if os.environ.get('MOCK_BUILD_FAIL'): sys.exit(1)
  (s/'built').write_text(json.load(open('package.json'))['version'])
 elif a[0]=='rm': (s/'running').unlink(missing_ok=True)
 elif a[0]=='run':
  image=a[-1]
  if os.environ.get('MOCK_RUN_FAIL') and not image.startswith('sha256:'): sys.exit(1)
  (s/'running').write_text(image.split(':',1)[1] if image.startswith('sha256:') else (s/'built').read_text())
 elif a[0]=='ps': print('mock container')
 sys.exit(0)
if cmd=='gh':
 if a[:2]==['auth','status'] and os.environ.get('MOCK_NEEDS_LOGIN') and not (s/'login').exists(): sys.exit(1)
 if a[:2]==['auth','login']: (s/'login').touch()
 if a[0]=='auth' or a[:2]==['workflow','run']: sys.exit(0)
 if a[0]=='api':
  if a[1]=='user':
   if '--include' in a: print('x-oauth-scopes: repo, read:org\\n')
   print('{"login":"jeremylynch83","id":12345,"name":"Jeremy Lynch"}'); sys.exit(0)
  if os.environ.get('MOCK_PAGES_DENY'): print('gh: permission denied (HTTP 403)',file=sys.stderr); sys.exit(1)
  if '-X' in a:
   method=a[a.index('-X')+1]; data=json.load(sys.stdin)
   assert data=={'build_type':'workflow'},data
   assert method in {'POST','PUT'}
   (s/'pages').write_text(json.dumps({'build_type':'workflow','html_url':'https://jeremylynch83.github.io/neurovascular-atlas/','cname':'preserved.example'}))
   print((s/'pages').read_text()); sys.exit(0)
  if not (s/'pages').exists(): print('gh: Not Found (HTTP 404)',file=sys.stderr); sys.exit(1)
  if '--jq' in a: print(json.loads((s/'pages').read_text())['html_url'])
  else: print((s/'pages').read_text())
  sys.exit(0)
sys.exit('Unexpected mock call: '+cmd+' '+repr(a))
'''
    for name in ['gh','docker','curl','sleep']:
        p=bindir/name; p.write_text(mock); p.chmod(0o755)
    fixture=root/'fixture'; fixture.mkdir()
    for p in ['src','tools','anatomy','public/anatomy/models']:
        (fixture/p).mkdir(parents=True,exist_ok=True)
        (fixture/p/'fixture.txt').write_text('fixture\n')
    for name in ['package.json','package-lock.json']:
        (fixture/name).write_text(json.dumps({'version':'0.7.1'}))
    manifest={'release':'0.7.1','structures':[{'asset':{'file':'models/test.glb'}}]}
    (fixture/'public/anatomy/manifest.json').write_text(json.dumps(manifest))
    (fixture/'public/anatomy/models/test.glb').write_bytes(b'glTF fixture')
    for name in ['Dockerfile','vite.config.ts','README.md']:
        (fixture/name).write_text('fixture\n')
    for name in ['anatomy.sh','build-anatomy.sh']:
        (fixture/name).write_text('#!/bin/sh\nexit 0\n')
    shutil.copy2(APP/'docker.sh',fixture/'docker.sh')
    # Deliberately ignore models: the installer must force-add only manifest assets.
    (fixture/'.gitignore').write_text('*.glb\n')
    download=root/'downloads'; download.mkdir()
    installer=download/'inr-anatomy.sh'; shutil.copy2(SCRIPT,installer)
    archive=download/'inr-anatomy-atlas-v0.7.1.zip'
    with zipfile.ZipFile(archive,'w') as z:
        for p in fixture.rglob('*'):
            if p.is_file(): z.write(p,'wrapped-app/'+str(p.relative_to(fixture)))

    def scenario(name, seed=False):
        folder=root/name; folder.mkdir(); remote=folder/'origin.git'
        run(['git','init','--bare','--initial-branch=main',remote])
        if seed:
            seedrepo=folder/'seed'; run(['git','clone',remote,seedrepo])
            (seedrepo/'README.md').write_text('old app')
            (seedrepo/'.gitignore').write_text('custom-private-file\n')
            (seedrepo/'package.json').write_text('{"version":"0.6.0"}')
            p=seedrepo/'public/anatomy/models/obsolete.glb'; p.parent.mkdir(parents=True);p.write_text('obsolete')
            run(['git','-C',seedrepo,'add','.'])
            run(['git','-C',seedrepo,'-c','user.name=Test','-c','user.email=test@example.com','commit','-m','old'])
            run(['git','-C',seedrepo,'push','origin','main'])
        state=folder/'state';state.mkdir()
        env=dict(os.environ,PATH=str(bindir)+':'+os.environ['PATH'],MOCK_STATE=str(state),INR_REPO_URL=str(remote),INR_CHECKOUT=str(folder/'checkout'))
        env.pop('GIT_AUTHOR_NAME',None);env.pop('GIT_AUTHOR_EMAIL',None)
        return folder,remote,state,env

    folder,remote,state,env=scenario('empty')
    env['MOCK_NEEDS_LOGIN']='1'
    p=run(['bash',installer],env)
    checkout=folder/'checkout'
    assert (state/'login').exists()
    assert "'refresh'" in (state/'calls').read_text()
    assert (checkout/'src/fixture.txt').exists()
    assert (state/'running').read_text()=='0.7.1'
    assert json.loads((state/'pages').read_text())['build_type']=='workflow'
    assert run(['git','-C',checkout,'status','--porcelain']).stdout==''
    assert run(['git','--git-dir',remote,'show','main:public/anatomy/models/test.glb']).stdout=='glTF fixture'
    assert run(['git','--git-dir',remote,'show','main:package.json']).stdout=='{"version": "0.7.1"}'
    before=run(['git','-C',checkout,'rev-parse','HEAD']).stdout
    run(['bash',installer],env)
    assert run(['git','-C',checkout,'rev-parse','HEAD']).stdout==before
    print('PASS: empty-repository clone, browser login, wrapped ZIP, ignored model tracking, push, Pages creation and repeat update')

    (checkout/'README.md').write_text('local work')
    calls=(state/'calls').read_text()
    p=run(['bash',installer],env,False)
    assert p.returncode and 'uncommitted changes' in p.stderr
    assert "docker ['build'" not in (state/'calls').read_text()[len(calls):]
    run(['git','-C',checkout,'restore','README.md'])
    print('PASS: dirty checkout preserved')

    folder,remote,state,env=scenario('old-release',True)
    (state/'pages').write_text('{"build_type":"legacy","html_url":"https://example.invalid/","cname":"preserved.example"}')
    run(['bash',installer],env)
    assert not (folder/'checkout/public/anatomy/models/obsolete.glb').exists()
    assert 'custom-private-file' in (folder/'checkout/.gitignore').read_text()
    assert "'PUT'" in (state/'calls').read_text()
    print('PASS: previous release upgraded, obsolete assets removed, legacy Pages switched to Actions without resetting cname')

    folder,remote,state,env=scenario('local-then-publish')
    run(['bash',installer,'local'],env)
    assert not run(['git','--git-dir',remote,'rev-parse','--verify','main'],ok=False).returncode==0
    run(['bash',installer,'publish'],env)
    assert run(['git','--git-dir',remote,'show','main:src/fixture.txt']).stdout=='fixture\n'
    assert run(['git','-C',folder/'checkout','status','--porcelain']).stdout==''
    print('PASS: local-only import subsequently published in full')

    folder,remote,state,env=scenario('stale')
    (state/'running').write_text('0.6.0'); env['MOCK_STALE']='1'
    p=run(['bash',installer],env,False)
    assert p.returncode and 'Expected v0.7.1' in p.stderr
    assert (state/'running').read_text()=='0.6.0'
    assert "gh ['workflow', 'run'" not in (state/'calls').read_text()
    assert run(['git','--git-dir',remote,'rev-parse','--verify','main'],ok=False).returncode!=0
    print('PASS: stale served version rejected, previous image restored, no push')

    folder,remote,state,env=scenario('build-fails')
    (state/'running').write_text('0.6.0'); env['MOCK_BUILD_FAIL']='1'
    p=run(['bash',installer],env,False)
    assert p.returncode and (state/'running').read_text()=='0.6.0'
    assert run(['git','--git-dir',remote,'rev-parse','--verify','main'],ok=False).returncode!=0
    print('PASS: build failure leaves previous running container and remote untouched')

    folder,remote,state,env=scenario('startup-fails')
    (state/'running').write_text('0.6.0');env['MOCK_RUN_FAIL']='1'
    p=run(['bash',installer],env,False)
    assert p.returncode and (state/'running').read_text()=='0.6.0'
    assert run(['git','--git-dir',remote,'rev-parse','--verify','main'],ok=False).returncode!=0
    print('PASS: failed container startup restores previous image without pushing')

    folder,remote,state,env=scenario('bad-zip')
    bad=root/'unsafe.zip'
    with zipfile.ZipFile(bad,'w') as z:z.writestr('../escape.txt','bad')
    p=run(['bash',installer,'update',bad],env,False)
    assert p.returncode and 'unsafe ZIP entry' in p.stderr
    assert not (root/'escape.txt').exists()
    print('PASS: ZIP traversal rejected')

    folder,remote,state,env=scenario('pages-denied')
    env['MOCK_PAGES_DENY']='1'
    p=run(['bash',installer],env,False)
    assert p.returncode and 'app was pushed' in p.stderr
    assert (state/'running').read_text()=='0.7.1'
    assert run(['git','--git-dir',remote,'rev-parse','--verify','main']).returncode==0
    env.pop('MOCK_PAGES_DENY');run(['bash',installer,'publish'],env)
    print('PASS: Pages permission failure reported accurately and publish retry succeeds')

    # Genuine divergent Git history must never be overwritten.
    folder,remote,state,env=scenario('diverged',True)
    run(['bash',installer],env)
    checkout=folder/'checkout'
    (checkout/'README.md').write_text('local committed work')
    run(['git','-C',checkout,'add','README.md']);run(['git','-C',checkout,'commit','-m','local'])
    other=folder/'other';run(['git','clone',remote,other])
    (other/'README.md').write_text('remote committed work')
    run(['git','-C',other,'add','README.md'])
    run(['git','-C',other,'-c','user.name=Test','-c','user.email=test@example.com','commit','-m','remote'])
    run(['git','-C',other,'push','origin','main'])
    before=run(['git','-C',checkout,'rev-parse','HEAD']).stdout
    p=run(['bash',installer],env,False)
    assert p.returncode and run(['git','-C',checkout,'rev-parse','HEAD']).stdout==before
    print('PASS: divergent branches rejected without resetting local work')

print('All installer integration checks passed. Docker/gh/HTTP calls were simulated; Git operations were real.')
