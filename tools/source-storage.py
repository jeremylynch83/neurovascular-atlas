#!/usr/bin/env python3
"""Store the large authoring GLB using existing lossless packs and small fragments.
Restoration reproduces every original byte, including metadata and unused buffers.
No geometry decoding, re-encoding, simplification or runtime loader changes.
"""
import argparse
import hashlib
import importlib.util
import json
import os
from pathlib import Path, PurePosixPath
import tempfile

ROOT = Path(__file__).resolve().parents[1]
SOURCE = 'public/anatomy/models/complete-circulation.glb'
STORE = 'anatomy/source-storage'
INDEX = STORE + '/index.json'
CHUNK = 16 * 1024 * 1024


def sha(data):
    return hashlib.sha256(data).hexdigest()


def local(root, name):
    p = PurePosixPath(name)
    if p.is_absolute() or '..' in p.parts or '\\' in name:
        raise ValueError('Unsafe source storage path: ' + name)
    result = root / name
    if not result.resolve().is_relative_to(root.resolve()):
        raise ValueError('Source storage path escapes checkout: ' + name)
    return result


def atomic(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists() and path.read_bytes() == data:
        path.chmod(0o644)
        return
    fd, name = tempfile.mkstemp(dir=path.parent, prefix='.' + path.name)
    try:
        with os.fdopen(fd, 'wb') as f:
            os.fchmod(f.fileno(), 0o644)
            f.write(data)
        os.replace(name, path)
    finally:
        Path(name).unlink(missing_ok=True)


def load_index(root):
    index = json.loads((root / INDEX).read_text())
    if index.get('schema') != 1 or index.get('source') != SOURCE:
        raise ValueError('Unsupported source storage index')
    return index


def dependencies(root, index):
    files = {}
    for name, expected in index['dependencies'].items():
        data = local(root, name).read_bytes()
        if len(data) != expected['bytes'] or sha(data) != expected['sha256']:
            raise ValueError('Source storage dependency is corrupt: ' + name)
        files[name] = data
    return files


def restore(root):
    target = root / SOURCE
    # Existing authoring edits always win. Packing records them before publishing.
    if target.exists():
        return {'restored': False, 'reason': 'authoring file already present'}
    index = load_index(root)
    files = dependencies(root, index)
    result = bytearray()
    for piece in index['pieces']:
        name, offset, length = piece
        data = files[name]
        if offset < 0 or length <= 0 or offset + length > len(data):
            raise ValueError('Invalid source storage range')
        result.extend(data[offset:offset + length])
    if len(result) != index['bytes'] or sha(result) != index['sha256']:
        raise ValueError('Restored authoring GLB checksum mismatch')
    atomic(target, result)
    return {'restored': True, 'bytes': len(result), 'sha256': index['sha256']}


def pack(root):
    restore(root)
    source = (root / SOURCE).read_bytes()
    previous = load_index(root) if (root / INDEX).exists() else None
    if previous and previous['sha256'] == sha(source):
        try:
            dependencies(root, previous)
            return {'reused': True, 'sourceBytes': len(source)}
        except (OSError, ValueError):
            pass
    spec = importlib.util.spec_from_file_location('loading_packs', root / 'tools/build-loading-packs.py')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    doc, blob = module.read_glb(root / SOURCE)
    source_bin = len(source) - len(blob)
    packs = json.loads((root / 'public/anatomy/packs/index.json').read_text())['packs']
    payloads = {}
    pack_bytes = {}

    def ranges(document):
        for view in document.get('bufferViews', []):
            storage = view.get('extensions', {}).get('EXT_meshopt_compression', view)
            if storage.get('buffer', 0) == 0:
                yield storage.get('byteOffset', 0), storage['byteLength']

    for row in packs:
        if row['source'] != 'models/complete-circulation.glb':
            continue
        name = 'public/anatomy/' + row['file']
        data = local(root, name).read_bytes()
        if sha(data) != row['sha256']:
            raise ValueError('Loading pack checksum mismatch: ' + name)
        pd, pb = module.read_glb(local(root, name))
        base = len(data) - len(pb)
        pack_bytes[name] = data
        for offset, length in ranges(pd):
            payloads.setdefault((length, sha(pb[offset:offset + length])), (name, base + offset))
    matches = []
    for offset, length in ranges(doc):
        match = payloads.get((length, sha(blob[offset:offset + length])))
        if match:
            matches.append((source_bin + offset, length, *match))
    pieces = []
    residual = bytearray()
    cursor = 0

    def gap(end):
        nonlocal cursor
        if end > cursor:
            pieces.append((None, len(residual), end - cursor))
            residual.extend(source[cursor:end])
            cursor = end

    for start, length, name, offset in sorted(set(matches), key=lambda x: (x[0], -x[1])):
        end = start + length
        if end <= cursor:
            continue
        gap(start)
        trim = cursor - start
        pieces.append((name, offset + trim, length - trim))
        cursor = end
    gap(len(source))
    fragments = []
    for start in range(0, len(residual), CHUNK):
        data = residual[start:start + CHUNK]
        name = STORE + '/fragment-' + sha(data) + '.bin'
        atomic(local(root, name), data)
        fragments.append(name)
    final = []
    for name, offset, length in pieces:
        if name is not None:
            final.append([name, offset, length])
        else:
            while length:
                part, at = divmod(offset, CHUNK)
                take = min(length, CHUNK - at)
                final.append([fragments[part], at, take])
                offset += take
                length -= take
    used = {p[0] for p in final}
    deps = {}
    for name in sorted(used):
        data = pack_bytes[name] if name in pack_bytes else local(root, name).read_bytes()
        deps[name] = {'bytes': len(data), 'sha256': sha(data)}
    index = {'schema': 1, 'source': SOURCE, 'bytes': len(source), 'sha256': sha(source),
             'dependencies': deps, 'pieces': final}
    atomic(root / INDEX, (json.dumps(index, separators=(',', ':')) + '\n').encode())
    for path in (root / STORE).glob('fragment-*.bin'):
        if path.relative_to(root).as_posix() not in used:
            path.unlink()
    return {'reused': False, 'sourceBytes': len(source), 'reusedPackBytes': len(source) - len(residual),
            'fragmentBytes': len(residual), 'fragments': len(fragments)}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action', choices=['restore', 'pack'])
    args = parser.parse_args()
    try:
        print('Authoring source: ' + json.dumps(globals()[args.action](ROOT)))
    except (OSError, ValueError, KeyError) as error:
        raise SystemExit('Error: ' + str(error))
