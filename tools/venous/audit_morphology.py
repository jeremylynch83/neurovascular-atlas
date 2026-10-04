"""Audit the authored surface, attachments and major sinus courses.

Run after implicit_veins.py. Optional baseline-*.json/bin snapshots in ROOT add
before/after comparisons; these measurements describe this mesh, not patients.
"""
import hashlib
import json
import numpy as np
import trimesh
from scipy.ndimage import gaussian_filter1d
from scipy.spatial import cKDTree
from reference import APP, ROOT, bone_surface, vtk

spec = json.loads((APP/'anatomy/source/venous/courses.json').read_text())
paths = json.loads((APP/'anatomy/source/venous/fitted-paths.json').read_text())
main = {}
for row in paths:
    main.setdefault(row['id'], row)
data = np.load(ROOT/'venous-mesh.npz')
p, f, labels = data['positions'], data['faces'], data['labels']
mesh = trimesh.Trimesh(p, f, process=False)
assert np.isfinite(p).all() and np.isfinite(data['normals']).all()
assert mesh.is_watertight and mesh.is_winding_consistent and mesh.volume > 0
assert len(mesh.split(only_watertight=False)) == 1
assert float(mesh.area_faces.min()) > 1e-10
assert len(np.unique(labels)) == len(spec['structures']) == 104
report = dict(release=spec['release'], vertices=len(p), triangles=len(f),
              named_structures=104, watertight=True, winding_consistent=True,
              connected_components=1, positive_volume=True,
              minimum_triangle_area_mm2=float(mesh.area_faces.min()),
              scope='Authoring geometry checks, not calibrated anatomical measurements')
if (ROOT/'venous-unfitted-mesh.npz').exists():
    raw=np.load(ROOT/'venous-unfitted-mesh.npz');before=raw['positions']
    assert np.array_equal(f,raw['faces'])
    n0=np.cross(before[f[:,1]]-before[f[:,0]],before[f[:,2]]-before[f[:,0]])
    n1=np.cross(p[f[:,1]]-p[f[:,0]],p[f[:,2]]-p[f[:,0]])
    major=np.isin(labels,[i for i,s in enumerate(spec['structures']) if s.get('profile')])
    flipped=int(np.sum(np.einsum('ij,ij->i',n0,n1)[major]<0))
    assert flipped==0
    report['major_sinus_faces_flipped_by_final_fit']=flipped

errors=[]
for row in spec['structures']:
    for end in (0, -1):
        anchor=row['points'][end]
        if not isinstance(anchor,dict): continue
        q=np.asarray(main[anchor['structure']]['points'])
        x=anchor['fraction']*(len(q)-1); i=min(int(x),len(q)-2)
        expected=q[i]*(1-(x-i))+q[i+1]*(x-i)
        errors.append(float(np.linalg.norm(np.asarray(main[row['id']]['points'][end])-expected)))
assert max(errors)<1e-4
report['main_attachment_endpoints']={'count':len(errors),'maximum_error_mm':max(errors)}

def turning(row):
    q=np.asarray(row['points']); arc=np.r_[0,np.cumsum(np.linalg.norm(np.diff(q,axis=0),axis=1))]
    s=np.arange(0,arc[-1],1.)
    q=np.column_stack([np.interp(s,arc,q[:,i]) for i in range(3)])
    t=gaussian_filter1d(np.gradient(q,axis=0),.8,axis=0)
    t/=np.linalg.norm(t,axis=1)[:,None]
    angles=np.degrees(np.arccos(np.clip(np.sum(t[4:]*t[:-4],axis=1),-1,1)))
    return dict(median=float(np.median(angles)),p95=float(np.percentile(angles,95)),maximum=float(angles.max()))

major=['vein.superior_sagittal']+[f'vein.{name}.{side}' for name in ['transverse','sigmoid'] for side in ['right','left']]
baseline={}
if (ROOT/'baseline-fitted-paths.json').exists():
    for row in json.loads((ROOT/'baseline-fitted-paths.json').read_text()): baseline.setdefault(row['id'],row)
report['turn_degrees_over_4mm']={sid:{'after':turning(main[sid]),**({'before':turning(baseline[sid])} if baseline else {})} for sid in major}

sdf=vtk.vtkImplicitPolyDataDistance(); sdf.SetInput(bone_surface())
def bone_gap(pp, ff, row):
    # Closest surface-to-bone distance within each 2 mm course bin. Exclude
    # collector junctions (first/last 5%) and the open lower sigmoid outlet.
    q=np.asarray(row['points']);arc=np.r_[0,np.cumsum(np.linalg.norm(np.diff(q,axis=0),axis=1))]
    _,nearest=cKDTree(q).query(pp);along=arc[nearest];fraction=along/arc[-1]
    keep=(fraction>.05)&(fraction<(.72 if 'sigmoid' in row['id'] else .95))
    dist=np.array([sdf.EvaluateFunction(v) for v in pp])
    bins=np.floor(along[keep]/2).astype(int);dd=dist[keep]
    minima=np.array([dd[bins==b].min() for b in np.unique(bins)])
    centres=pp[ff].mean(1);_,ix=cKDTree(q).query(centres);frac=arc[ix]/arc[-1]
    cc=centres[(frac>.05)&(frac<(.72 if 'sigmoid' in row['id'] else .95))]
    cd=np.array([sdf.EvaluateFunction(v) for v in cc])
    return dict(bins=len(minima),median_closest_gap_mm=float(np.median(minima)),
                p90_closest_gap_mm=float(np.percentile(minima,90)),
                minimum_vertex_signed_distance_mm=float(dd.min()),
                minimum_face_centroid_signed_distance_mm=float(cd.min()))

report['bone_apposition']={'method':'Signed distance to retained inner skull; closest surface point per 2 mm course bin. Junction end 5% excluded; sigmoid distal 28% excluded at open skull base. Positive is outside bone. Vertex and centroid sampling does not prove absence of triangle intersections.','structures':{}}
old_records={r['name']:r for r in json.loads((ROOT/'baseline-reference.json').read_text())} if (ROOT/'baseline-reference.json').exists() else {}
for sid in major:
    index=next(i for i,s in enumerate(spec['structures']) if s['id']==sid)
    ff=f[labels==index];used,inv=np.unique(ff,return_inverse=True)
    result={'after':bone_gap(p[used],inv.reshape(-1,3),main[sid])}
    if sid in old_records:
        rec=old_records[sid]
        pp=np.memmap(ROOT/'baseline-reference.bin',dtype='<f4',mode='r',offset=rec['positionOffset'],shape=(rec['vertices'],3))
        ff=np.memmap(ROOT/'baseline-reference.bin',dtype='<u4',mode='r',offset=rec['indexOffset'],shape=(rec['indices']//3,3))
        result['before']=bone_gap(pp,ff,baseline[sid])
    report['bone_apposition']['structures'][sid]=result

if (ROOT/'baseline-asset-hashes.json').exists():
    old=json.loads((ROOT/'baseline-asset-hashes.json').read_text());retained={}
    for name,expected in old.items():
        if name=='venous.glb':continue
        actual=hashlib.sha256((APP/'public/anatomy/models'/name).read_bytes()).hexdigest()
        assert actual==expected,name
        retained[name]=actual
    report['unchanged_asset_sha256']=retained
dest=APP/'docs/validation/venous-morphology-v0.9.2.json'
dest.write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2),flush=True)
