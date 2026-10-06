"""Acceptance checks for the complete reconstructed central arterial family."""
import argparse,hashlib,json,itertools
from pathlib import Path
import numpy as np,trimesh,vtk
from scipy.spatial import cKDTree,ConvexHull
from vtk.util.numpy_support import vtk_to_numpy,numpy_to_vtk
from fit_vessels import APP,read_glb,mesh_records,accessor,curve_from_mesh
from verify_fitting import collisions
from build_targets import poly

def contact_faces(a,b):
    if np.any(a.bounds[1]<b.bounds[0]) or np.any(b.bounds[1]<a.bounds[0]):return np.array([],int),np.array([],int)
    triangles=b.vertices[b.faces];lo,hi=a.bounds
    keep=np.all(triangles.max(1)>=lo,axis=1)&np.all(triangles.min(1)<=hi,axis=1)
    ids=np.flatnonzero(keep)
    if not len(ids):return np.array([],int),np.array([],int)
    target=trimesh.Trimesh(b.vertices,b.faces[ids],process=False)
    f=vtk.vtkCollisionDetectionFilter();f.SetInputData(0,poly(a));f.SetInputData(1,poly(target));f.SetTransform(0,vtk.vtkTransform());f.SetTransform(1,vtk.vtkTransform());f.SetCollisionModeToAllContacts();f.SetBoxTolerance(0);f.SetCellTolerance(0);f.Update()
    if not f.GetNumberOfContacts():return np.array([],int),np.array([],int)
    return vtk_to_numpy(f.GetContactCells(0)),ids[vtk_to_numpy(f.GetContactCells(1))]

def outside_join_contacts(a,b,old_a,old_b):
    da,db=contact_faces(a,b)
    if not len(da):return 0
    distance=cKDTree(old_b.vertices).query(old_a.vertices)[0];shared=old_a.vertices[distance<1e-5]
    if not len(shared):return len(da)
    # Recognise only the original anatomical join collar, using its exact
    # source triangle identities. Contacts elsewhere are never excused.
    tree=cKDTree(shared)
    close_a=tree.query(old_a.vertices[old_a.faces[da]].mean(1))[0]<2.
    close_b=tree.query(old_b.vertices[old_b.faces[db]].mean(1))[0]<2.
    return int((~(close_a&close_b)).sum())

def self_contacts(mesh):
    a,b=contact_faces(mesh,mesh);keep=a<b;a,b=a[keep],b[keep]
    p,q=mesh.vertices[mesh.faces[a]],mesh.vertices[mesh.faces[b]]
    # Coordinate adjacency recognises duplicated accessor seam vertices too.
    adjacent=(np.linalg.norm(p[:,:,None,:]-q[:,None,:,:],axis=3)<2e-5).any(axis=(1,2))
    return int((~adjacent).sum())

def plane_area(mesh,centre,tangent):
    plane=vtk.vtkPlane();plane.SetOrigin(*centre);plane.SetNormal(*tangent)
    cut=vtk.vtkCutter();cut.SetInputData(poly(mesh));cut.SetCutFunction(plane);cut.Update()
    points=cut.GetOutput().GetPoints()
    assert points is not None,'Missing perpendicular skin section'
    p=vtk_to_numpy(points.GetData());p=p[np.linalg.norm(p-centre,axis=1)<1.5]
    assert len(p)>=3,'Missing local skin envelope'
    tangent=tangent/np.linalg.norm(tangent);u=np.cross(tangent,[0,0,1]);u/=np.linalg.norm(u);v=np.cross(tangent,u)
    return float(ConvexHull(np.column_stack([(p-centre)@u,(p-centre)@v])).volume)

def material_section(before,after,centre,tangent,radius=1.5):
    # Interpolate the final wall position on the EXACT source intersection
    # edges. A moved, blended join does not share the proposal curve's planes.
    data=poly(before);values=numpy_to_vtk(after.vertices,deep=True);values.SetName('final_wall_position');data.GetPointData().AddArray(values)
    plane=vtk.vtkPlane();plane.SetOrigin(*centre);plane.SetNormal(*tangent)
    cut=vtk.vtkCutter();cut.SetInputData(data);cut.SetCutFunction(plane);cut.Update();out=cut.GetOutput()
    assert out.GetPoints() is not None,'Missing source skin section'
    p=vtk_to_numpy(out.GetPoints().GetData());q=vtk_to_numpy(out.GetPointData().GetArray('final_wall_position'))
    keep=np.linalg.norm(p-centre,axis=1)<radius;p,q=p[keep],q[keep]
    assert len(p)>=3,'Missing local source skin envelope'
    areas=[];warps=[]
    for points in [p,q]:
        _,_,axes=np.linalg.svd(points-points.mean(0),full_matrices=False)
        projected=(points-points.mean(0))@axes[:2].T
        areas.append(float(ConvexHull(projected).volume));warps.append(float(np.sqrt(np.mean(((points-points.mean(0))@axes[2])**2))))
    return areas,warps

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--candidate',default='.authoring/central-rebuilt-trial.glb');args=parser.parse_args()
    path=APP/args.candidate;od,ob=read_glb(APP/'.authoring/arteries-baseline.glb');nd,nb=read_glb(path)
    oldr,newr=mesh_records(od,ob),mesh_records(nd,nb)
    old={k:trimesh.Trimesh(r['positions'],r['faces'],process=False) for k,r in oldr.items()}
    new={k:trimesh.Trimesh(r['positions'],r['faces'],process=False) for k,r in newr.items()}
    report={'release':'0.9.18','baseline':'0.9.15','authoringSha256':hashlib.sha256(path.read_bytes()).hexdigest(),'geometry':[],'tissueChecks':[],'skullChecks':[],'arterialChecks':[],'selfIntersectionChecks':[],'primarySections':[],'branchSections':[],'failures':[]}
    def require(test,message):
        if not test:report['failures'].append(message)
    require(set(old)==set(new),'Changed arterial label inventory')
    changed=[];exact=[]
    for k in old:
        a,b=oldr[k],newr[k];require(np.array_equal(a['faces'],b['faces']),k+': changed triangle indices')
        if np.array_equal(a['positions'],b['positions']):
            require(np.array_equal(accessor(od,ob,a['primitive']['attributes']['NORMAL']),accessor(nd,nb,b['primitive']['attributes']['NORMAL'])),k+': changed retained normal buffer');exact.append(k);continue
        changed.append(k);p,q=a['positions'].astype(float),b['positions'].astype(float);f=a['faces'];area0=np.linalg.norm(np.cross(p[f[:,1]]-p[f[:,0]],p[f[:,2]]-p[f[:,0]]),axis=1);area=np.linalg.norm(np.cross(q[f[:,1]]-q[f[:,0]],q[f[:,2]]-q[f[:,0]]),axis=1);ratios=area[area0>1e-8]/area0[area0>1e-8]
        require(np.isfinite(q).all() and ratios.min()>1e-4,k+': non-finite or collapsed skin triangle')
        report['geometry'].append({'node':k,'maximumDisplacementMm':float(np.linalg.norm(q-p,axis=1).max()),'movedVertices':int((np.linalg.norm(q-p,axis=1)>1e-5).sum()),'minimumTriangleAreaRatio':float(ratios.min()),'medianTriangleAreaRatio':float(np.median(ratios)),'triangleIndicesRetained':True})
    expected={f'{label} {side}' for label in ['Central','Central cortical branch','Central distal ramus','MCA superior division'] for side in ['left','right']}
    require(set(changed)==expected,'Changed family differs from eight authorised regional labels')
    p=np.concatenate([r['positions'] for r in oldr.values()]);q=np.concatenate([r['positions'] for r in newr.values()]);_,inverse=np.unique(np.round(p,5),axis=0,return_inverse=True);order=np.argsort(inverse);same=np.diff(inverse[order])==0;gaps=np.linalg.norm(np.diff(q[order],axis=0)[same],axis=1)
    report['maximumSharedLabelBoundaryGapMm']=float(gaps.max(initial=0));require(gaps.max(initial=0)<2e-4,'Opened shared labelled skin junction')
    report['unchangedLabels']=exact
    brain=trimesh.load(APP/'public/anatomy/models/brain-context.glb',process=False);bones=trimesh.load(APP/'.authoring/bones-baseline.glb',process=False)
    report['brainAssetSha256']=hashlib.sha256((APP/'public/anatomy/models/brain-context.glb').read_bytes()).hexdigest()
    for k in changed:
        counts=[self_contacts(scene[k]) for scene in [old,new]]
        report['selfIntersectionChecks'].append({'node':k,'beforeNonadjacentTriangleContacts':counts[0],'afterNonadjacentTriangleContacts':counts[1]})
        require(counts[1]<=counts[0],k+': increased nonadjacent skin self-intersection')
        for target,m in brain.geometry.items():
            if any(t in target for t in ['sulc','lat-fis','falx','tentorium','ventricle','aqueduct']):continue
            counts=[collisions(scene[k],m) for scene in [old,new]]
            if any(counts):
                report['tissueChecks'].append({'node':k,'target':target,'beforeTriangleContacts':counts[0],'afterTriangleContacts':counts[1],'phase':'whole labelled wall'})
                require(counts[1]<=counts[0],k+': increased whole-wall tissue contact with '+target)
            if not k.startswith('MCA'):
                phase=trimesh.Trimesh(new[k].vertices,new[k].faces[np.all(new[k].vertices[new[k].faces,2]>=120,axis=1)],process=False)
                require(collisions(phase,m)==0,k+': cortical-phase tissue contact with '+target)
        for target,m in bones.geometry.items():
            counts=[collisions(scene[k],m) for scene in [old,new]]
            if any(counts):report['skullChecks'].append({'node':k,'target':target,'beforeTriangleContacts':counts[0],'afterTriangleContacts':counts[1]})
            require(counts[1]<=counts[0],k+': increased skull contact with '+target)
        print('Tissue and skull',k,flush=True)
    # Every edited label against retained arterial skin, including parent
    # transitions. Shared joins are excused only in their original 2 mm collar.
    for k in changed:
        for other in old:
            if other==k or (other in changed and other<k):continue
            before=outside_join_contacts(old[k],old[other],old[k],old[other]);after=outside_join_contacts(new[k],new[other],old[k],old[other])
            if before or after:report['arterialChecks'].append({'node':k,'target':other,'beforeOutsideJoinContacts':before,'afterOutsideJoinContacts':after})
            require(after<=before,k+': increased arterial contact outside original join with '+other)
        print('Arterial neighbours',k,flush=True)
    trial=json.loads((APP/'docs/validation/central-rebuilt-trial-v0.9.18.json').read_text());require(trial['authoringSha256']==report['authoringSha256'],'Stale branch correspondence report')
    for branch in trial['branches']:
        key=branch['node'];src,dst=np.array(branch['source']),np.array(branch['target']);areas=[[],[]];warps=[]
        for i in np.linspace(20,len(src)-25,25).astype(int):
            pair,warp=material_section(old[key],new[key],src[i],src[i+1]-src[i-1])
            for j in [0,1]:areas[j].append(pair[j])
            warps.append(warp[1])
        ratios=np.array(areas[1])/areas[0]
        report['branchSections'].append({'node':key,'method':'Exact material correspondence: source transverse wall intersections and barycentrically interpolated final wall positions on the same triangles, projected to each contour best-fit plane','beforeEnvelopeAreaMm2':areas[0],'afterEnvelopeAreaMm2':areas[1],'afterBestFitPlaneRmsResidualMm':warps,'minimumAreaRatio':float(ratios.min()),'medianAreaRatio':float(np.median(ratios)),'maximumAreaRatio':float(ratios.max())})
        require(ratios.min()>.55,key+': severe local skin-envelope narrowing')
    for side in ['left','right']:
        key='Central '+side;course=curve_from_mesh(old[key],axis=2,n=120)
        ids=np.flatnonzero((course[:,2]>=125)&(course[:,2]<=149));areas=[[],[]];warps=[]
        for i in ids[np.linspace(0,len(ids)-1,25).astype(int)]:
            pair,warp=material_section(old[key],new[key],course[i],course[i+1]-course[i-1])
            for j in [0,1]:areas[j].append(pair[j])
            warps.append(warp[1])
        ratio=np.array(areas[1])/areas[0]
        report['primarySections'].append({'node':key,'sourcePhase':'125 <= source z <= 149 mm','method':'Exact material contour correspondence, each contour projected to its best-fit plane','beforeEnvelopeAreaMm2':areas[0],'afterEnvelopeAreaMm2':areas[1],'afterBestFitPlaneRmsResidualMm':warps,'minimumAreaRatio':float(ratio.min()),'medianAreaRatio':float(np.median(ratio)),'maximumAreaRatio':float(ratio.max())})
        require(ratio.min()>.5,key+': severe primary skin-envelope narrowing')
    report['limitations']=['Checks concern the labelled atlas skin, not a separately segmented lumen or patient anatomy.','Open cortical tissue surfaces prevent reliable solid containment. Whole-wall triangle contacts and source-bound joins are checked separately.','Existing proximal tissue contacts are reported, including the retained Sylvian approach. No increase is accepted.','Guide sheets and ventricular reference surfaces are excluded from tissue contact checks.']
    report['passed']=not report['failures'];out=APP/'docs/validation/central-rebuilt-acceptance-v0.9.18.json';out.write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({'passed':report['passed'],'failures':report['failures'],'geometry':report['geometry'],'branchSections':[{k:r[k] for k in ['node','minimumAreaRatio','medianAreaRatio','maximumAreaRatio']} for r in report['branchSections']]},indent=2),flush=True)
    assert report['passed'],'Central connected-family candidate rejected'

if __name__=='__main__':main()
