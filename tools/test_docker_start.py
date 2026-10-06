#!/usr/bin/env python3
"""Exercise the real Docker launcher without host Node/npm dependencies."""
import os
import shutil
import subprocess
import tempfile
from pathlib import Path

APP = Path(__file__).resolve().parents[1]

with tempfile.TemporaryDirectory(prefix='atlas-docker-start-') as tmp:
    root = Path(tmp)
    bindir = root / 'bin'
    bindir.mkdir()
    shutil.copy2(APP / 'docker.sh', root / 'docker.sh')
    # Host anatomy validation needs the mesh decoder from npm. Its execution
    # here must fail, proving the launcher leaves validation to Docker.
    for path in [root / 'anatomy.sh', bindir / 'node', bindir / 'npm']:
        path.write_text('#!/bin/sh\necho unexpected-host-dependency >&2\nexit 99\n')
        path.chmod(0o755)
    mock = bindir / 'docker'
    mock.write_text('''#!/bin/sh
printf '%s\\n' "$*" >> "$DOCKER_TEST_LOG"
if [ "$1" = build ] && [ "${DOCKER_TEST_BUILD_FAIL:-0}" = 1 ]; then exit 7; fi
''')
    mock.chmod(0o755)
    # Avoid probing a real Tailscale session during this isolated test.
    tailscale = bindir / 'tailscale'
    tailscale.write_text('#!/bin/sh\nexit 0\n')
    tailscale.chmod(0o755)
    log = root / 'docker-calls'
    env = dict(os.environ, PATH=str(bindir) + ':' + os.environ['PATH'], DOCKER_TEST_LOG=str(log))
    result = subprocess.run(['bash', str(root / 'docker.sh'), 'restart'], cwd=root, env=env, capture_output=True, text=True)
    assert result.returncode == 0, result.stderr
    calls = log.read_text().splitlines()
    assert len(calls) == 3 and calls[0].startswith('build ') and calls[1].startswith('rm ') and calls[2].startswith('run '), calls
    log.unlink()
    env['DOCKER_TEST_BUILD_FAIL'] = '1'
    result = subprocess.run(['bash', str(root / 'docker.sh'), 'restart'], cwd=root, env=env, capture_output=True, text=True)
    assert result.returncode != 0
    calls = log.read_text().splitlines()
    assert len(calls) == 1 and calls[0].startswith('build '), calls
    # Complete validation is still mandatory in the production image.
    dockerfile = (APP / 'Dockerfile').read_text()
    assert dockerfile.index('RUN npm ci') < dockerfile.index('RUN npm run build')
    assert './build-anatomy.sh' in (APP / 'package.json').read_text()
    assert 'tools/validate_anatomy.py --build' in (APP / 'build-anatomy.sh').read_text()

print('Docker startup passes without host npm dependencies; failed builds preserve the running container; full validation remains in the Docker build.')
