"""Freeze the accepted round-wall candidate and reconstruct joined normals."""
import sys, json
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'anatomical-fixes-v0929'))
from geometry import *
OUT = ROOT.parent / 'corrections-work'
C = OUT / 'candidate-final'
revision = json.loads((OUT / 'candidate/revision.json').read_text())
rounding = json.loads((C / 'rounding.json').read_text())
assert not rounding['newContacts'] and not any(rounding['allAuditContactCounts'])
changed = []
for p in sorted(C.glob('*.positions.bin')):
    name = p.name.removesuffix('.positions.bin')
    m = meshes[name]
    m.new = np.fromfile(p, '<f4').reshape(-1, 3)
    m.f.astype('<u4').tofile(C / (name + '.indices.bin'))
    changed.append({'node': name, 'file': m.file,
                    'maximumDisplacementMm': float(np.linalg.norm(m.new-m.v, axis=1).max()),
                    'topology': 'retained'})
revision['changed'] = changed
revision['roundWallRecovery'] = rounding
revision['placementStageValidation'] = 'anatomical-placement-stage-v0.9.31.json'
revision['fields']['finalBrainRecess'] = {
    'centre': rounding['centre'], 'extent': [6, 6, 6],
    'delta': [0, -rounding['magnitude'], 0], 'plateau': .3}
(C / 'revision.json').write_text(json.dumps(revision, indent=2)+'\n')
changed_names = {r['node'] for r in changed}
for file in {r['file'] for r in changed}:
    names = [n for n,m in meshes.items() if m.file == file]
    vertices, faces, offset = [], [], 0
    for n in names:
        m = meshes[n]; v = m.new.astype('<f4')
        vertices.append(v); faces.append(m.f + offset); offset += len(v)
    v = np.vstack(vertices); f = np.vstack(faces)
    _, first, inv = np.unique(v, axis=0, return_index=True, return_inverse=True)
    uv = v[first].astype(float); uf = inv[f]; tri = uv[uf]
    fn = np.cross(tri[:,1]-tri[:,0], tri[:,2]-tri[:,0]); normal = np.zeros_like(uv)
    for j in range(3): np.add.at(normal, uf[:,j], fn)
    normal /= np.maximum(np.linalg.norm(normal, axis=1)[:,None], 1e-20)
    normal = normal[inv]; offset = 0
    for n in names:
        m = meshes[n]
        if n in changed_names:
            normal[offset:offset+len(m.new)].astype('<f4').tofile(C/(n+'.normals.bin'))
        offset += len(m.new)
print('Final candidate:', len(changed), 'labels')
