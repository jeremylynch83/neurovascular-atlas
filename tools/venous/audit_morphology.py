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
from reference import APP, ROOT, bone_surface, vtk, records, arrays, poly

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
baseline={};baseline_mesh=None
checkpoint=ROOT/'checkpoint-v0.9.5'
if (checkpoint/'fitted-paths.json').exists():
    for row in json.loads((checkpoint/'fitted-paths.json').read_text()):baseline.setdefault(row['id'],row)
    baseline_mesh=np.load(checkpoint/'venous-mesh.npz')
    report['comparison_baseline_release']='0.9.5'
elif (ROOT/'baseline-fitted-paths.json').exists():
    for row in json.loads((ROOT/'baseline-fitted-paths.json').read_text()):baseline.setdefault(row['id'],row)
    report['comparison_baseline_release']='historical authoring snapshot'

report['turn_degrees_over_4mm']={sid:{'after':turning(main[sid]),**({'before':turning(baseline[sid])} if baseline else {})} for sid in major}

sdf=vtk.vtkImplicitPolyDataDistance(); sdf.SetInput(bone_surface())
def bone_gap(pp, ff, row, distance_field=None):
    distance_field=distance_field or sdf
    # Closest surface-to-bone distance within each 2 mm course bin. Exclude
    # collector junctions (first/last 5%) and the open lower sigmoid outlet.
    q=np.asarray(row['points']);arc=np.r_[0,np.cumsum(np.linalg.norm(np.diff(q,axis=0),axis=1))]
    _,nearest=cKDTree(q).query(pp);along=arc[nearest];fraction=along/arc[-1]
    keep=(fraction>.05)&(fraction<(.72 if 'sigmoid' in row['id'] else .95))
    dist=np.array([distance_field.EvaluateFunction(v) for v in pp])
    bins=np.floor(along[keep]/2).astype(int);dd=dist[keep]
    minima=np.array([dd[bins==b].min() for b in np.unique(bins)])
    centres=pp[ff].mean(1);_,ix=cKDTree(q).query(centres);frac=arc[ix]/arc[-1]
    cc=centres[(frac>.05)&(frac<(.72 if 'sigmoid' in row['id'] else .95))]
    cd=np.array([distance_field.EvaluateFunction(v) for v in cc])
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
    if baseline_mesh is not None:
        old_f=baseline_mesh['faces'][baseline_mesh['labels']==index];used_old,inv_old=np.unique(old_f,return_inverse=True)
        result['before']=bone_gap(baseline_mesh['positions'][used_old],inv_old.reshape(-1,3),baseline[sid])
    elif sid in old_records:
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
report['skullbase_apposition']={}
for index,structure in enumerate(spec['structures']):
    profile=structure.get('profile',{})
    names=profile.get('bone_names')
    if not profile.get('bone_apposition') or not names:continue
    append=vtk.vtkAppendPolyData()
    for rec in records:
        if rec['name'] in names:append.AddInputData(poly(*arrays(rec)))
    append.Update();local=vtk.vtkImplicitPolyDataDistance();local.SetInput(append.GetOutput())
    ff=f[labels==index];used,inv=np.unique(ff,return_inverse=True)
    report['skullbase_apposition'][structure['id']]={'named_bones':names,'surface':bone_gap(p[used],inv.reshape(-1,3),main[structure['id']],local)}
    assert report['skullbase_apposition'][structure['id']]['surface']['median_closest_gap_mm']<.5,structure['id']
    if baseline_mesh is not None:
        old_f=baseline_mesh['faces'][baseline_mesh['labels']==index];used_old,inv_old=np.unique(old_f,return_inverse=True)
        report['skullbase_apposition'][structure['id']]['before']=bone_gap(baseline_mesh['positions'][used_old],inv_old.reshape(-1,3),baseline[structure['id']],local)
# Check the actual sinus skin around both retained cavernous ICAs.
report['cavernous_ica_clearance']={}
for side in ['right','left']:
    rec=next(rec for rec in records if rec['name']=='ICA cavernous '+side)
    arterial_surface=poly(*arrays(rec))
    artery=vtk.vtkImplicitPolyDataDistance();artery.SetInput(arterial_surface)
    index=next(i for i,row in enumerate(spec['structures']) if row['id']=='vein.cavernous.'+side)
    vertices=p[np.unique(f[labels==index])];centroids=p[f[labels==index]].mean(1)
    # Named arterial segments have open label boundaries, so their signed
    # distances can be negative outside the true lumen. Use surface distance
    # and an actual triangle intersection check rather than that ambiguous sign.
    vertex_min=min(abs(artery.EvaluateFunction(v)) for v in vertices)
    centroid_min=min(abs(artery.EvaluateFunction(v)) for v in centroids)
    intersections=vtk.vtkIntersectionPolyDataFilter()
    intersections.SetInputData(0,poly(p,f[labels==index]));intersections.SetInputData(1,arterial_surface)
    intersections.SplitFirstOutputOff();intersections.SplitSecondOutputOff();intersections.Update()
    lines=intersections.GetOutput(0).GetNumberOfLines()
    assert lines==0,(side,lines)
    assert min(vertex_min,centroid_min)>.05,(side,vertex_min,centroid_min)
    report['cavernous_ica_clearance'][side]={'minimum_vertex_surface_distance_mm':vertex_min,'minimum_face_centroid_surface_distance_mm':centroid_min,'triangle_intersection_lines':lines}
# Check that the thin authored basilar channels survived common-surface meshing.
# Near an ICA attachment a path centre may be in the deliberate ICA exclusion.
final_sdf=vtk.vtkImplicitPolyDataDistance();final_sdf.SetInput(poly(p,f))
coverage=[]
for row in paths:
    if row['id']!='vein.basilar_plexus':continue
    qq=np.asarray(row['points']);rr=np.asarray(row['radii']);keep=np.arange(len(qq))[max(1,int(len(qq)*.1)):max(2,int(len(qq)*.9))]
    distance=np.array([final_sdf.EvaluateFunction(v) for v in qq[keep]])
    coverage.append({'interior_samples':len(keep),'fraction_inside_or_within_0_3mm':float(np.mean(distance<=.3)), 'maximum_distance_mm':float(distance.max())})
assert len(coverage)==11
assert min(c['fraction_inside_or_within_0_3mm'] for c in coverage)>.85,coverage
report['basilar_channel_coverage']=coverage
report['unresolved_bone_detail']='The retained hypoglossal canal lumen is not resolved. Anterior condylar routing remains a regional teaching representation.'
dest=APP/('docs/validation/venous-morphology-v'+spec['release']+'.json')
dest.write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2),flush=True)
