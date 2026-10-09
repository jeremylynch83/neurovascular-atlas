"""Apply a shared, compact deformation to the connected anterior venous group."""
from common import *
from scipy.spatial import cKDTree
names=json.loads((WORK/'connected-nodes.json').read_text())
venous={r['name']:load(r['name']) for r in META if r['file']=='venous.glb' or r['name'].startswith('brain.pons.')}
changed=[]; checks=[]
accepted={};recovery=[]
for name in names:
    v,f=venous[name]; q=brain_shift(v) if name.startswith('brain.') else vein_shift(v)
    accepted[name]=q
    d=np.linalg.norm(q-v,axis=1)
    if name!='vein.transverse_pontine.left':assert np.array_equal(v[:,2],q[:,2])
    tri=q[f]; area=np.linalg.norm(np.cross(tri[:,1]-tri[:,0],tri[:,2]-tri[:,0]),axis=1)
    t0=v[f]; area0=np.linalg.norm(np.cross(t0[:,1]-t0[:,0],t0[:,2]-t0[:,0]),axis=1)
    assert not np.any((area<1e-10)&(area0>=1e-10)), name+' new degenerate triangle'
    q.astype('<f4').tofile(OUT/(name+'.positions.bin')); f.tofile(OUT/(name+'.indices.bin'))
    changed.append(dict(node=name,file=next(r['file'] for r in META if r['name']==name),maximumDisplacementMm=float(d.max()),topology='linear subdivision of original venous facets' if name.startswith('vein.') else 'retained'))
    checks.append(dict(node=name,medianXBeforeMm=float(np.median(v[:,0])),medianXAfterMm=float(np.median(q[:,0])),
                       vertices=len(v),triangles=len(f),minimumDoubleTriangleAreaMm2=float(area.min()),
                       existingDegenerateTriangles=int(np.sum(area0<1e-10)),newDegenerateTriangles=0))
# Detect a missed incident label before exporting. Identical interface vertices
# must get identical positions, including labels outside this selected group.
moving=np.concatenate([venous[n][0][np.any((brain_shift(venous[n][0]) if n.startswith('brain.') else vein_shift(venous[n][0]))!=venous[n][0],axis=1)] for n in names])
tree=cKDTree(moving); lo=moving.min(0)-1e-5; hi=moving.max(0)+1e-5
for name,(v,f) in venous.items():
    if name in names: continue
    inside=np.all((v>=lo)&(v<=hi),axis=1)
    assert not np.any(tree.query(v[inside])[0]<1e-5), 'Missing connected label: '+name
# Reconstruct area-weighted normals on welded positions across every venous label.
samples=np.concatenate([venous[n][0] for n in names if n.startswith('brain.')]).astype(float)
columns=[]
for j in range(3):
    delta=np.zeros(3);delta[j]=.01
    columns.append((brain_shift(samples+delta)-brain_shift(samples-delta))/.02)
determinants=np.linalg.det(np.stack(columns,axis=2))
assert determinants.min()>0, 'Folded coordinate deformation'
vv=[];ff=[];offset=0
for name,(v,f) in venous.items():
    q=accepted[name] if name in names else v
    vv.append(q);ff.append(f+offset);offset+=len(v)
v=np.vstack(vv);f=np.vstack(ff)
_,first,inv=np.unique(v,axis=0,return_index=True,return_inverse=True)
uv=v[first].astype(float);uf=inv[f];t=uv[uf]
fn=np.cross(t[:,1]-t[:,0],t[:,2]-t[:,0]);nn=np.zeros_like(uv)
for j in range(3):np.add.at(nn,uf[:,j],fn)
nn/=np.maximum(np.linalg.norm(nn,axis=1)[:,None],1e-20)
valid=np.linalg.norm(nn,axis=1)>.99
if not valid.all():
    nn[~valid]=nn[valid][cKDTree(uv[valid]).query(uv[~valid])[1]]
nn=nn[inv];offset=0
for name,(v,f) in venous.items():
    if name in names:
        assert np.all(np.linalg.norm(nn[offset:offset+len(v)],axis=1)>.99)
        nn[offset:offset+len(v)].astype('<f4').tofile(OUT/(name+'.normals.bin'))
    offset+=len(v)
revision=dict(release='0.9.47',baselineRelease='0.9.46',baselineAssetHashes=json.loads((DATA/'source-assets.json').read_text()),
              newLabels=[],changed=changed,checks=checks,sharedInterfaceClosurePassed=True,
              roundWallRecovery=recovery,
              minimumSampledDeformationJacobian=float(determinants.min()),deformationJacobianSampleVertices=len(samples),
              deformation='Shared x/z-dependent y displacement for veins (Jacobian determinant exactly 1), with separate compact y-only pontine groove adjustment and linear venous surface subdivision. See common.py.',
              anatomicalDecision='Correct the transverse pontine midline crossing to pass behind the basilar artery, between artery and pons. Smaller arterial crossings are checked individually.')
(OUT/'revision.json').write_text(json.dumps(revision,indent=2)+'\n')
print(json.dumps(checks,indent=2),flush=True)
