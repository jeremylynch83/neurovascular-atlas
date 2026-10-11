"""Package immutable comparison buffers, current candidate and shared source."""
import sys, json, zipfile, hashlib
from pathlib import Path

root = Path.cwd()
dest = Path(sys.argv[1]).resolve()
prefix = 'recovered-app-v0.9.51'
items = []
for path in sorted(root.iterdir()):
    if path.is_file() and path.suffix != '.tsbuildinfo' and not path.name.startswith('.'):
        items.append((path, prefix + '/' + path.name))
for name in ['src', 'public', 'anatomy', 'tools', 'docs', 'review-v0959', 'review-v0960', 'work-v0959', 'work-v0960']:
    for path in sorted((root / name).rglob('*')):
        if not path.is_file() or '__pycache__' in path.parts or 'decoded' in path.relative_to(root).parts or path.suffix == '.pyc':
            continue
        if name in ['work-v0958', 'work-v0959'] and path.name.endswith('.normals.bin'):
            continue
        if name == 'work-v0960' and path.name == 'package-verification-continuation.json':
            continue
        items.append((path, prefix + '/' + path.relative_to(root).as_posix()))
for path in sorted((root / 'decoded').rglob('*')):
    if path.is_file() and not path.name.endswith('.normals.bin'):
        items.append((path, prefix + '/decoded/' + path.relative_to(root / 'decoded').as_posix()))
for name in ['Neurovascular_Atlas_MMA_review_v0.9.60.html', 'Neurovascular_Atlas_MMA_comparison_v0.9.60.png', 'README_MMA_v0.9.60.txt', 'MMA_validation_v0.9.60.json']:
    path = dest / name
    assert path.is_file(), path
    items.append((path, name))
assert len({name for _, name in items}) == len(items)
path = dest / 'Neurovascular_Atlas_MMA_checkpoint_v0.9.60.zip'
with zipfile.ZipFile(path, 'w', compression=zipfile.ZIP_DEFLATED, compresslevel=6, allowZip64=True) as archive:
    for source, name in items:
        archive.write(source, name)
with zipfile.ZipFile(path) as archive:
    assert archive.testzip() is None
    assert prefix + '/decoded/meshes.json' in archive.namelist()
    report = json.loads(archive.read(prefix + '/work-v0960/candidate/acceptance-continuation.json'))
    assert report['safeCheckpoint'] and report['status'] == 'UNRELEASED'
    for name, digest in report['candidateBufferSha256'].items():
        assert hashlib.sha256(archive.read(prefix + '/work-v0960/candidate/' + name)).hexdigest() == digest
    for label in report['installedCollateralRepairs']:
        for suffix in ['.positions.bin', '.indices.bin']:
            assert archive.read(prefix + '/work-v0960/candidate/' + label + suffix) == archive.read(prefix + '/work-v0959/candidate/' + label + suffix)
    for name, digest in report['acceptedAssetSha256'].items():
        assert hashlib.sha256(archive.read(prefix + '/public/anatomy/models/' + name)).hexdigest() == digest
digest = hashlib.sha256()
with path.open('rb') as stream:
    for chunk in iter(lambda: stream.read(8 * 1024 * 1024), b''):
        digest.update(chunk)
result = dict(file=str(path), bytes=path.stat().st_size, entries=len(items), sha256=digest.hexdigest(), crcPassed=True, candidateHashesPassed=True, retainedRepairsExact=True, publicAssetHashesPassed=True, sharedDecodedSource=True)
(root / 'work-v0960/package-verification-continuation.json').write_text(json.dumps(result, indent=2))
print(json.dumps(result, indent=2))
