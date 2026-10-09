"""Apply a shared, compact deformation to the connected anterior venous group."""
from common import *
from scipy.spatial import cKDTree
names=json.loads((WORK/'connected-nodes.json').read_text())
venous={r['name']:load(r['name']) for r in META if r['file']=='venous.glb'}
changed=[]; checks=[]
accepted={};recovery=[]
for name in names:
    v,f=venous[name]; q=shift(v)
    if name=='vein.preolivary.right':
        from round_wall import recover
        other=np.concatenate([a for n,(a,b) in venous.items() if n!=name])
        q,amount=recover(v,f,q,other)
        recovery.append(dict(node=name,maximumRoundRecoveryMm=amount,sharedCollarVerticesRetained=True))
    accepted[name]=q
    d=np.linalg.norm(q-v,axis=1)
    if name!='vein.preolivary.right':assert np.array_equal(v[:,2],q[:,2])
    tri=q[f]; area=np.linalg.norm(np.cross(tri[:,1]-tri[:,0],tri[:,2]-tri[:,0]),axis=1)
    t0=v[f]; area0=np.linalg.norm(np.cross(t0[:,1]-t0[:,0],t0[:,2]-t0[:,0]),axis=1)
    assert not np.any((area<1e-10)&(area0>=1e-10)), name+' new degenerate triangle'
    q.astype('<f4').tofile(OUT/(name+'.positions.bin')); f.tofile(OUT/(name+'.indices.bin'))
    changed.append(dict(node=name,file='venous.glb',maximumDisplacementMm=float(d.max()),topology='retained'))
    checks.append(dict(node=name,medianXBeforeMm=float(np.median(v[:,0])),medianXAfterMm=float(np.median(q[:,0])),
                       vertices=len(v),triangles=len(f),minimumDoubleTriangleAreaMm2=float(area.min()),
                       existingDegenerateTriangles=int(np.sum(area0<1e-10)),newDegenerateTriangles=0))
# Detect a missed incident label before exporting. Identical interface vertices
# must get identical positions, including labels outside this selected group.
moving=np.concatenate([venous[n][0][np.any(shift(venous[n][0])!=venous[n][0],axis=1)] for n in names])
tree=cKDTree(moving); lo=moving.min(0)-1e-5; hi=moving.max(0)+1e-5
for name,(v,f) in venous.items():
    if name in names: continue
    inside=np.all((v>=lo)&(v<=hi),axis=1)
    assert not np.any(tree.query(v[inside])[0]<1e-5), 'Missing connected label: '+name
# Reconstruct area-weighted normals on welded positions across every venous label.
samples=np.concatenate([venous[n][0] for n in names]).astype(float)
columns=[]
for j in range(3):
    delta=np.zeros(3);delta[j]=.01
    columns.append((shift(samples+delta)-shift(samples-delta))/.02)
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
revision=dict(release='0.9.46',baselineRelease='0.9.45',baselineAssetHashes=json.loads((DATA/'source-assets.json').read_text()),
              newLabels=[],changed=changed,checks=checks,sharedInterfaceClosurePassed=True,
              roundWallRecovery=recovery,
              minimumSampledDeformationJacobian=float(determinants.min()),deformationJacobianSampleVertices=len(samples),
              deformation='Common smooth spatial field; x and y only; compact support. See common.py.',
              anatomicalDecision='Correct the median alignment and individual branch clearances; retain the pial course behind the basilar artery. A blanket anterior-to-all-arteries rule is not anatomically justified.')
(OUT/'revision.json').write_text(json.dumps(revision,indent=2)+'\n')
print(json.dumps(checks,indent=2),flush=True)
