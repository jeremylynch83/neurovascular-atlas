#!/usr/bin/env python3
"""Regression checks for exact source storage and rejected-push recovery."""
import importlib.util
import json
from pathlib import Path
import shutil
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[1]


def module(name, file):
    spec = importlib.util.spec_from_file_location(name, ROOT / 'tools' / file)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


storage = module('storage', 'source-storage.py')
publish = module('publish', 'prepare-github.py')


def cmd(root, *args):
    return subprocess.check_output(['git', '-C', str(root), *args], stderr=subprocess.PIPE).decode().strip()


storage.restore(ROOT)
report = {}
with tempfile.TemporaryDirectory() as folder:
    root = Path(folder)
    index = storage.load_index(ROOT)
    for name in [storage.INDEX, 'tools/build-loading-packs.py', 'public/anatomy/packs/index.json', *index['dependencies']]:
        target = root / name
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(ROOT / name, target)
    assert not (root / storage.SOURCE).exists()
    result = storage.restore(root)
    restored = (root / storage.SOURCE).read_bytes()
    assert storage.sha(restored) == index['sha256']
    assert restored == (ROOT / storage.SOURCE).read_bytes()
    assert storage.restore(root)['restored'] is False
    # Existing authoring changes survive restore; packing captures new bytes.
    changed = restored[:-4] + bytes(b ^ 1 for b in restored[-4:])
    (root / storage.SOURCE).write_bytes(changed)
    storage.restore(root)
    assert (root / storage.SOURCE).read_bytes() == changed
    storage.pack(root)
    (root / storage.SOURCE).unlink()
    storage.restore(root)
    assert (root / storage.SOURCE).read_bytes() == changed
    # A missing dependency must fail closed without installing a partial source.
    (root / storage.SOURCE).unlink()
    dependency = next(iter(storage.load_index(root)['dependencies']))
    (root / dependency).unlink()
    try:
        storage.restore(root)
        raise AssertionError('Missing dependency accepted')
    except OSError:
        pass
    assert not (root / storage.SOURCE).exists()
    report['exactRestoration'] = result
    report['editedSourceRoundTrip'] = True
    report['missingDependencyRejected'] = True

with tempfile.TemporaryDirectory() as folder:
    base = Path(folder)
    remote = base / 'remote.git'
    repo = base / 'repo'
    subprocess.run(['git', 'init', '--bare', str(remote)], check=True, capture_output=True)
    subprocess.run(['git', 'clone', str(remote), str(repo)], check=True, capture_output=True)
    cmd(repo, 'checkout', '-b', 'main')
    cmd(repo, 'config', 'user.name', 'Atlas test')
    cmd(repo, 'config', 'user.email', 'atlas-test@example.invalid')
    (repo / 'README').write_text('Published baseline\n')
    cmd(repo, 'add', '.')
    cmd(repo, 'commit', '-m', 'Published baseline')
    cmd(repo, 'push', '-u', 'origin', 'main')
    published = cmd(repo, 'rev-parse', 'HEAD')
    source = repo / storage.SOURCE
    source.parent.mkdir(parents=True)
    for text in ['first rejected model', 'second rejected model']:
        source.write_bytes((text * 1000).encode())
        cmd(repo, 'add', '.')
        cmd(repo, 'commit', '-m', text)
    old = cmd(repo, 'rev-parse', 'HEAD')
    (repo / '.gitignore').write_text('/' + storage.SOURCE + '\n')
    (repo / 'README').write_text('Current release\n')
    cmd(repo, 'add', '.')
    cmd(repo, 'rm', '--cached', storage.SOURCE)
    final_tree = cmd(repo, 'write-tree')
    result = publish.prepare(repo, limit=1024)
    assert result['repaired'] and result['removedOversizedBlobsFromPush'] == 2
    assert cmd(repo, 'rev-parse', 'HEAD^') == published
    assert cmd(repo, 'rev-parse', 'HEAD^{tree}') == final_tree
    assert cmd(repo, 'rev-parse', result['backupBranch']) == old
    assert cmd(repo, 'diff', '--cached') == ''
    assert source.exists()
    assert cmd(repo, 'show', 'HEAD:README') == 'Current release'
    assert not publish.prepare(repo, limit=1024)['repaired']
    # Actual bare-remote receive hook: reject pending oversized blobs.
    hook = remote / 'hooks/pre-receive'
    hook.write_text('''#!/usr/bin/env python3
import subprocess,sys
for line in sys.stdin:
 old,new,ref=line.split()
 args=['git','rev-list','--objects','--no-object-names',new]
 if old.strip('0'): args+=['^'+old]
 ids=subprocess.check_output(args)
 rows=subprocess.check_output(['git','cat-file','--batch-check=%(objecttype) %(objectsize)'],input=ids).decode().splitlines()
 if any(kind=='blob' and int(size)>1024 for kind,size in (r.split() for r in rows)):
  sys.exit(1)
''')
    hook.chmod(0o755)
    cmd(repo, 'push', 'origin', 'main')
    assert cmd(remote, 'rev-parse', 'main') == cmd(repo, 'rev-parse', 'HEAD')
    # A different oversized staged file is rejected without changing refs.
    (repo / 'unexpected.bin').write_bytes(b'x' * 2048)
    cmd(repo, 'add', 'unexpected.bin')
    head = cmd(repo, 'rev-parse', 'HEAD')
    try:
        publish.prepare(repo, limit=1024)
        raise AssertionError('Oversized index accepted')
    except ValueError:
        pass
    assert cmd(repo, 'rev-parse', 'HEAD') == head
    cmd(repo, 'reset', '--', 'unexpected.bin')
    # A remote change after the local branch diverges is never overwritten.
    (repo / 'README').write_text('Local change\n')
    cmd(repo, 'add', 'README'); cmd(repo, 'commit', '-m', 'Local change')
    head = cmd(repo, 'rev-parse', 'HEAD')
    other = base / 'other'
    subprocess.run(['git', 'clone', '-b', 'main', str(remote), str(other)], check=True, capture_output=True)
    cmd(other, 'config', 'user.name', 'Other'); cmd(other, 'config', 'user.email', 'other@example.invalid')
    (other / 'README').write_text('Remote change\n')
    cmd(other, 'add', '.'); cmd(other, 'commit', '-m', 'Remote change'); cmd(other, 'push', 'origin', 'main')
    try:
        publish.prepare(repo, limit=1024)
        raise AssertionError('Divergence accepted')
    except ValueError as error:
        assert 'diverged' in str(error)
    assert cmd(repo, 'rev-parse', 'HEAD') == head
    report['unpublishedHistoryRepair'] = result
    report['realPushWithBlobLimitHook'] = True
    report['oversizedIndexRejected'] = True
    report['remoteDivergenceProtected'] = True

print(json.dumps(report, indent=2))
