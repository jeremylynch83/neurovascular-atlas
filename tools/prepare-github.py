#!/usr/bin/env python3
"""Preflight GitHub's blob limit and repair rejected, unpublished atlas commits.
Keep published history intact. Retain the previous local tip on a backup branch.
The replacement commit contains the complete current index, not an old snapshot.
"""
import datetime
import subprocess
import sys
from pathlib import Path

LIMIT = 100 * 1024 * 1024
SOURCE = 'public/anatomy/models/complete-circulation.glb'


def git(root, *args, data=None, check=True):
    result = subprocess.run(['git', '-C', str(root), *args], input=data,
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if check and result.returncode:
        raise ValueError(result.stderr.decode(errors='replace').strip())
    return result


def oversized(root, objects, limit):
    if not objects:
        return []
    rows = git(root, 'cat-file', '--batch-check=%(objectname) %(objecttype) %(objectsize)',
               data=('\n'.join(objects) + '\n').encode()).stdout.decode().splitlines()
    return [(oid, int(size)) for oid, kind, size in (r.split() for r in rows)
            if kind == 'blob' and int(size) > limit]


def prepare(root, limit=LIMIT):
    branch = git(root, 'symbolic-ref', '--short', 'HEAD').stdout.strip()
    if branch != b'main':
        raise ValueError('Switch to main before publishing.')
    indexed = git(root, 'ls-files', '--stage', '-z').stdout.split(b'\0')
    paths = {}
    for row in indexed:
        if not row:
            continue
        metadata, name = row.split(b'\t', 1)
        mode, oid, stage = metadata.split()
        if stage != b'0':
            raise ValueError('Resolve index conflicts before publishing.')
        paths[oid.decode()] = name.decode()
    large = oversized(root, paths, limit)
    if large:
        names = ', '.join(paths[oid] for oid, _ in large)
        raise ValueError('GitHub file-size limit exceeded in staged files: ' + names)
    git(root, 'fetch', 'origin')
    old = git(root, 'rev-parse', '--verify', 'HEAD', check=False)
    if old.returncode:
        return {'repaired': False}
    old = old.stdout.decode().strip()
    base = git(root, 'rev-parse', '--verify', 'refs/remotes/origin/main', check=False)
    base = base.stdout.decode().strip() if base.returncode == 0 else None
    if base and git(root, 'merge-base', '--is-ancestor', base, old, check=False).returncode:
        raise ValueError('Remote main has diverged. Reconcile it before publishing; no local history was changed.')
    revision_args = ['rev-list', '--objects', old] + (['^' + base] if base else [])
    history = {}
    for row in git(root, *revision_args).stdout.decode().splitlines():
        oid, _, name = row.partition(' ')
        history[oid] = name
    large = oversized(root, history, limit)
    if not large:
        return {'repaired': False}
    unexpected = [history[oid] or oid for oid, _ in large if history[oid] != SOURCE]
    if unexpected:
        raise ValueError('Other oversized files exist in unpublished history: ' + ', '.join(unexpected)
                         + '. No history was changed.')
    tree = git(root, 'write-tree').stdout.decode().strip()
    message = ('Publish atlas using lossless source storage\n\n'
               'Combine unpublished commits rejected for oversized model blobs.\n'
               'The previous local history is retained on a backup branch.\n')
    args = ['commit-tree', tree] + (['-p', base] if base else [])
    replacement = git(root, *args, data=message.encode()).stdout.decode().strip()
    stamp = datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%d-%H%M%S')
    backup = f'backup/atlas-before-size-fix-{stamp}-{old[:12]}'
    # Atomic ref transaction: either both the backup and replacement are created,
    # or neither is. The index/worktree already describe the replacement tree.
    transaction = f'start\ncreate refs/heads/{backup} {old}\nupdate refs/heads/main {replacement} {old}\nprepare\ncommit\n'
    git(root, 'update-ref', '--stdin', data=transaction.encode())
    return {'repaired': True, 'backupBranch': backup, 'removedOversizedBlobsFromPush': len(large)}


if __name__ == '__main__':
    import json
    try:
        result = prepare(Path(sys.argv[1]).resolve())
        print('GitHub preflight: ' + json.dumps(result))
    except (OSError, ValueError) as error:
        raise SystemExit('Error: ' + str(error))
