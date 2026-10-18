#!/usr/bin/env python3
"""Remove unreachable accessors and Meshopt payloads without re-encoding geometry.

Supports the atlas's static, embedded, Meshopt-compressed GLBs. Unknown resource
types fail closed. Accessor IDs change; vertex IDs and triangle order do not.
This only writes the requested output. Asset-hash-bound metadata must be rebound
after verifying decoded geometry, before publishing a changed model.
"""
import argparse
import copy
import hashlib
import json
import struct
from pathlib import Path


def unpack(data):
    assert len(data) >= 28 and struct.unpack_from('<III', data) == (0x46546C67, 2, len(data)), 'Invalid GLB header'
    length, kind = struct.unpack_from('<II', data, 12)
    assert kind == 0x4E4F534A and length % 4 == 0, 'Invalid JSON chunk'
    doc = json.loads(data[20:20 + length])
    size, kind = struct.unpack_from('<II', data, 20 + length)
    assert kind == 0x004E4942 and size == len(data) - 28 - length, 'Invalid BIN chunk'
    return doc, data[28 + length:]


def accessor_references(doc):
    assert not any(doc.get(k) for k in ('animations', 'skins', 'images')), 'Unsupported accessor or buffer consumers'
    assert set(doc.get('extensionsUsed', [])) <= {'EXT_meshopt_compression', 'KHR_mesh_quantization'}, 'Unsupported extensions'
    assert not doc.get('extensions'), 'Unsupported root extensions'
    refs = []
    for mesh in doc.get('meshes', []):
        for primitive in mesh['primitives']:
            assert not primitive.get('extensions'), 'Unsupported primitive extensions'
            refs.extend((primitive['attributes'], k) for k in primitive['attributes'])
            if 'indices' in primitive:
                refs.append((primitive, 'indices'))
            for target in primitive.get('targets', []):
                refs.extend((target, k) for k in target)
    return refs


def compact(data):
    original, binary = unpack(data)
    doc = copy.deepcopy(original)
    refs = accessor_references(doc)
    used = sorted({container[key] for container, key in refs})
    for i in used:
        assert not doc['accessors'][i].get('sparse') and not doc['accessors'][i].get('extensions'), 'Unsupported accessor storage'
        assert 'bufferView' in doc['accessors'][i], 'Missing accessor buffer view'
    views = sorted({doc['accessors'][i]['bufferView'] for i in used})
    amap = {old: new for new, old in enumerate(used)}
    vmap = {old: new for new, old in enumerate(views)}
    assert len(doc['buffers']) == 2 and not doc['buffers'][0].get('uri'), 'Expected an embedded compressed buffer'
    assert doc['buffers'][1].get('extensions', {}).get('EXT_meshopt_compression', {}).get('fallback') is True, 'Expected a virtual fallback buffer'
    # Avoid changing an already compact file at all, including JSON formatting.
    if len(used) == len(doc['accessors']) and len(views) == len(doc['bufferViews']):
        return data, {'removedAccessors': 0, 'removedBufferViews': 0, 'retainedPayloadsByteExact': True}
    doc['accessors'] = [doc['accessors'][i] for i in used]
    doc['bufferViews'] = [doc['bufferViews'][i] for i in views]
    for container, key in refs:
        container[key] = amap[container[key]]
    for accessor in doc['accessors']:
        accessor['bufferView'] = vmap[accessor['bufferView']]
    packed = bytearray()
    for old_id, view in zip(views, doc['bufferViews']):
        assert view['buffer'] == 1 and set(view.get('extensions', {})) == {'EXT_meshopt_compression'}, 'Unsupported buffer view'
        extension = view['extensions']['EXT_meshopt_compression']
        assert extension['buffer'] == 0, 'Unexpected compressed buffer'
        start, length = extension.get('byteOffset', 0), extension['byteLength']
        assert 0 <= start <= start + length <= len(binary), 'Payload outside BIN'
        payload = binary[start:start + length]
        packed.extend(b'\0' * (-len(packed) % 4))
        offset = len(packed)
        packed.extend(payload)
        extension['byteOffset'] = offset
        assert bytes(packed[offset:offset + length]) == payload
        # Virtual fallback offsets are retained. They do not occupy BIN bytes.
        assert view['byteOffset'] + view['byteLength'] <= doc['buffers'][1]['byteLength']
    packed.extend(b'\0' * (-len(packed) % 4))
    doc['buffers'][0]['byteLength'] = len(packed)
    js = json.dumps(doc, separators=(',', ':'), ensure_ascii=False).encode()
    js += b' ' * (-len(js) % 4)
    result = (struct.pack('<III', 0x46546C67, 2, 28 + len(js) + len(packed))
              + struct.pack('<II', len(js), 0x4E4F534A) + js
              + struct.pack('<II', len(packed), 0x004E4942) + packed)
    # Prove the scene, names, materials and transforms are untouched.
    for key in set(original) - {'accessors', 'bufferViews', 'buffers', 'meshes'}:
        assert doc[key] == original[key], key
    restored = copy.deepcopy(doc['meshes'])
    restored_doc = {'meshes': restored}
    for container, key in accessor_references(restored_doc):
        container[key] = used[container[key]]
    assert restored == original['meshes']
    for new_id, old_id in enumerate(used):
        restored_accessor = copy.deepcopy(doc['accessors'][new_id])
        restored_accessor['bufferView'] = views[restored_accessor['bufferView']]
        assert restored_accessor == original['accessors'][old_id]
    return result, {'removedAccessors': len(original['accessors']) - len(used),
                    'removedBufferViews': len(original['bufferViews']) - len(views),
                    'retainedPayloadsByteExact': True}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('source', type=Path)
    parser.add_argument('output', type=Path)
    args = parser.parse_args()
    before = args.source.read_bytes()
    after, proof = compact(before)
    assert compact(after)[0] == after, 'Compaction must be idempotent'
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_bytes(after)
    print(json.dumps({**proof, 'beforeBytes': len(before), 'afterBytes': len(after),
                      'beforeSha256': hashlib.sha256(before).hexdigest(),
                      'afterSha256': hashlib.sha256(after).hexdigest()}))


if __name__ == '__main__':
    main()
