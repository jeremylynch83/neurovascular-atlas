"""Validate delivered-skin fitting against baseline and solid atlas surfaces."""
import json,zipfile,hashlib
from pathlib import Path
import numpy as np,trimesh,vtk
from scipy.spatial import cKDTree
from fit_vessels import APP,PUB,read_glb,mesh_records,curve_from_mesh,ray_tree,front
from build_targets import poly

def distances(p,m):
    loc=vtk.vtkStaticCellLocator();loc.SetDataSet(poly(m));loc.BuildLocator()
    q=[0.,0.,0.];cell,sub,d=vtk.reference(0),vtk.reference(0),vtk.reference(0.)
    out=[]
    for x in p:
        loc.FindClosestPoint(x,q,cell,sub,d);out.append(float(d)**.5)
    return np.array(out)

def inside(p,m):
    assert m.is_watertight,'Containment requires a closed surface'
    data=vtk.vtkPolyData();pts=vtk.vtkPoints()
    for x in p:pts.InsertNextPoint(*x)
    data.SetPoints(pts);test=vtk.vtkSelectEnclosedPoints();test.SetInputData(data);test.SetSurfaceData(poly(m));test.SetTolerance(1e-7);test.Update()
    return np.array([test.IsInside(i) for i in range(len(p))],bool)

def stats(a):return {'minimumMm':float(a.min()),'medianMm':float(np.median(a)),'p95Mm':float(np.quantile(a,.95)),'maximumMm':float(a.max())}

def collisions(m,target):
    if np.any(m.bounds[1]<target.bounds[0]) or np.any(target.bounds[1]<m.bounds[0]):return 0
    # Broad-phase rejection retains every target triangle whose box could
    # intersect the vessel box, avoiding repeated whole-skull BVH builds.
    tri=target.vertices[target.faces];lo,hi=m.bounds
    keep=np.all(tri.max(1)>=lo,axis=1)&np.all(tri.min(1)<=hi,axis=1)
    if not keep.any():return 0
    target=trimesh.Trimesh(target.vertices,target.faces[keep],process=False)
    test=vtk.vtkCollisionDetectionFilter();test.SetInputData(0,poly(m));test.SetInputData(1,poly(target))
    test.SetTransform(0,vtk.vtkTransform());test.SetTransform(1,vtk.vtkTransform());test.SetCollisionModeToAllContacts();test.SetBoxTolerance(0);test.SetCellTolerance(0);test.Update()
    return int(test.GetNumberOfContacts())

def main():
    manifest=json.loads((APP/'anatomy/generated/complete_manifest.json').read_text());rows={s['id']:s for s in manifest['structures']}
    brain=trimesh.load(PUB/'models/brain-context.glb',process=False)
    baseline_brain=trimesh.load(APP/'.authoring/brain-baseline.glb',process=False)
    audit={'release':'0.9.17','baseline':'0.9.15','geometry':[],'relationships':[],'authoringGeometryHashes':{k:hashlib.sha256((APP/f'.authoring/{k}-fitted.glb').read_bytes()).hexdigest() for k in ['veins','arteries']},'brainAdjustments':manifest.get('brainAdjustmentPolicy',{}).get('appliedAdjustments',[])}
    scenes={}
    for kind in ['veins','arteries']:
        old=trimesh.load(APP/f'.authoring/{kind}-baseline.glb',process=False)
        new=trimesh.load(APP/f'.authoring/{kind}-fitted.glb',process=False);scenes[kind]=[old,new]
        assert set(old.geometry)==set(new.geometry)
        op=np.concatenate([m.vertices for m in old.geometry.values()]);np_=np.concatenate([m.vertices for m in new.geometry.values()])
        # Every duplicate old coordinate at a labelled skin junction must map to
        # the same new coordinate. Check every label, not just catalogue edges.
        rounded=np.round(op,5);_,inverse=np.unique(rounded,axis=0,return_inverse=True)
        order=np.argsort(inverse);same=np.diff(inverse[order])==0
        gaps=np.linalg.norm(np.diff(np_[order],axis=0)[same],axis=1)
        assert gaps.max(initial=0)<2e-4, (kind,float(gaps.max()))
        unchanged=[];changed=[]
        for key,m in old.geometry.items():
            n=new.geometry[key];assert np.array_equal(m.faces,n.faces)
            delta=np.linalg.norm(m.vertices-n.vertices,axis=1)
            if delta.max()<1e-6:unchanged.append(key)
            else:changed.append(key)
        audit['geometry'].append({'asset':kind,'labelsRetained':len(new.geometry),'unchangedLabels':unchanged,'changedLabels':changed,'maximumSharedLabelBoundaryGapMm':float(gaps.max(initial=0)),'triangleIndicesRetainedExactly':True})
    assert all('cavernous' not in k for k in audit['geometry'][0]['changedLabels'])
    assert all(any(s in k for s in ['Central','MCA superior division']) for k in audit['geometry'][1]['changedLabels'])
    # Primary arterial bank tests apply to the fitted sulcal phase, excluding
    # the retained proximal Sylvian approach and parent collar.
    for side in ['left','right']:
        key='Central '+side
        targets=[brain.geometry['brain.'+k+'.'+side] for k in ['precentral-gyrus','postcentral-gyrus']]
        record={'id':'artery.anterior.central_'+side,'status':'fitted' if not np.array_equal(scenes['arteries'][0].geometry[key].vertices,scenes['arteries'][1].geometry[key].vertices) else 'retained-rejected-trial','phase':'sulcal wall, z >= 120 mm','before':{},'after':{}}
        for state,scene,context in zip(['before','after'],scenes['arteries'],[baseline_brain,brain]):
            targets=[context.geometry['brain.'+k+'.'+side] for k in ['precentral-gyrus','postcentral-gyrus']]
            wall=scene.geometry[key].vertices;wall=wall[wall[:,2]>=120]
            contained=np.zeros(len(wall),bool)
            for target in targets:
                if target.is_watertight:contained|=inside(wall,target)
            record[state]={'wallToBanks':stats(distances(wall,trimesh.util.concatenate(targets))),'wallVerticesInsideBanks':int(contained.sum()),'wallVerticesChecked':len(wall)}
            m=scene.geometry[key]
            phase=trimesh.Trimesh(m.vertices,m.faces[np.all(m.vertices[m.faces,2]>=120,axis=1)],process=False)
            record[state]['triangleContactsWithBanks']=collisions(phase,trimesh.util.concatenate(targets))
            record[state]['closedSurfacesForContainment']=sum(t.is_watertight for t in targets)
            if not record[state]['closedSurfacesForContainment']:record[state]['wallVerticesInsideBanks']=None
        audit['relationships'].append(record)
    kinds=['medulla-oblongata','pons','midbrain','base-of-peduncle'];targets=[brain.geometry[f'brain.{k}.{side}'] for k in kinds for side in ['left','right']]
    allstem=trimesh.util.concatenate(targets);tree=ray_tree(allstem)
    for key in ['vein.anterior_medullary','vein.anterior_pontine','vein.anterior_pontomesencephalic']+[f'vein.{k}.{s}' for k in ['lateral_mesencephalic','transverse_pontine','pontomedullary'] for s in ['left','right']]:
        record={'id':key,'phase':'exported vessel wall, including outlet collars','before':{},'after':{}}
        for state,scene,context in zip(['before','after'],scenes['veins'],[baseline_brain,brain]):
            targets=[context.geometry[f'brain.{k}.{side}'] for k in kinds for side in ['left','right']];allstem=trimesh.util.concatenate(targets)
            wall=scene.geometry[key].vertices;contained=np.zeros(len(wall),bool)
            for target in targets:
                if target.is_watertight:contained|=inside(wall,target)
            record[state]={'wallToBrainstem':stats(distances(wall,allstem)),'wallVerticesInsideBrainstem':int(contained.sum()),'wallVerticesChecked':len(wall)}
            record[state]['triangleContactsWithBrainstem']=collisions(scene.geometry[key],allstem)
            record[state]['closedSurfacesForContainment']=sum(t.is_watertight for t in targets)
        audit['relationships'].append(record)
    seam=np.array(rows['brain.landmark.falcotentorial']['landmark']['course'])
    def line_dist(p):
        a,b=seam[:-1],seam[1:];v=b-a;t=np.clip(np.sum((p[:,None,:]-a)*v,axis=2)/np.sum(v*v,axis=1),0,1)
        return np.linalg.norm(p[:,None,:]-(a+t[:,:,None]*v),axis=2).min(1)
    record={'id':'vein.straight','phase':'wall along retained AP extent of sinus','before':{},'after':{}}
    for state,scene in zip(['before','after'],scenes['veins']):
        seam=np.array(({s['id']:s for s in json.loads((APP/'.authoring/manifest-baseline.json').read_text())['structures']} if state=='before' else rows)['brain.landmark.falcotentorial']['landmark']['course'])
        m=scene.geometry['vein.straight'];record[state]={'wallToAttachmentLine':stats(line_dist(m.vertices))}
    audit['relationships'].append(record)
    assert all(r['after']['triangleContactsWithBanks']==0 for r in audit['relationships'] if r.get('status')=='fitted' and 'triangleContactsWithBanks' in r['after']),'Edited sulcal wall intersects tissue banks'
    audit['limitations']=['Vertex containment is reported only for closed surfaces. Triangle contact tests separately include all named open and closed tissue surfaces.','Open sulcal and dural references are excluded from solid tissue containment tests.','All venous geometry is retained. Dural and brainstem trials were rejected and their baseline contacts remain unresolved.','Preserved skin connectivity does not establish a separately segmented lumen or patient anatomical accuracy.']
    (APP/'docs/validation/fitting-geometry-v0.9.17.json').write_text(json.dumps(audit,indent=2)+'\n')
    print(json.dumps({'sharedSkinBoundaries':'passed','protectedCavernousGeometry':'passed','relationships':audit['relationships']},indent=2))

if __name__=='__main__':main()
