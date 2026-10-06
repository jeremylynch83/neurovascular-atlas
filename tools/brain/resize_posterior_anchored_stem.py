"""Posterior-anchored local AP reduction, staged for combined anatomy review.

The posterior brainstem boundary, measured independently in every X/Z
column, anchors the reduction. All overlapping tissue labels receive the
same ordered field. Skull, dura and vessels are never moved by this tool.
"""
import argparse, json
import numpy as np, trimesh, vtk
from scipy.ndimage import distance_transform_edt, gaussian_filter, gaussian_filter1d, minimum_filter1d
from fit_vessels import APP, read_glb, mesh_records, smoothstep
from build_targets import poly
from reconcile_local_volume import VolumeMap
from reconcile_brainstem import sha
from refine_context_skin import save_replaced

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--fraction',type=float,default=.4)
    parser.add_argument('--output-directory',default='.authoring/posterior-anchor25')
    parser.add_argument('--lock-surrounding-tissue',action='store_true')
    parser.add_argument('--transition-cap',type=float,default=1.25)
    parser.add_argument('--anatomical-only',action='store_true')
    parser.add_argument('--basilar-guided',action='store_true')
    parser.add_argument('--basilar-margin',type=float,default=3.)
    args=parser.parse_args()
    assert 0<args.fraction<.65
    work=APP/args.output_directory;work.mkdir(parents=True,exist_ok=True)
    v=np.load(APP/'.authoring/brainstem20-lower-final/volume-map.npz')
    old=VolumeMap.__new__(VolumeMap);old.origin=v['origin'];old.delta=v['delta'];old.shape=np.array(old.delta.shape)
    new=VolumeMap.__new__(VolumeMap);new.origin=old.origin;new.shape=old.shape;new.mask=np.zeros(old.shape,bool)
    axes=[np.arange(n)+o for n,o in zip(old.shape,old.origin)]
    brain=trimesh.load(APP/'public/anatomy/models/brain-context.glb',process=False)
    stem=trimesh.util.concatenate([m for k,m in brain.geometry.items() if any(t in k for t in ['pons.','medulla-oblongata','midbrain.','base-of-peduncle'])])
    loc=vtk.vtkStaticCellLocator();loc.SetDataSet(poly(stem));loc.BuildLocator()
    back=np.full((len(axes[0]),len(axes[2])),np.nan);front=back.copy()
    for i,x in enumerate(axes[0]):
        for k,z in enumerate(axes[2]):
            pts=vtk.vtkPoints();cells=vtk.vtkIdList()
            loc.IntersectWithLine([x,-135,z],[x,-30,z],1e-8,pts,cells)
            if pts.GetNumberOfPoints():
                ys=[pts.GetPoint(j)[1] for j in range(pts.GetNumberOfPoints())]
                back[i,k]=min(ys);front[i,k]=max(ys)
    valid=np.isfinite(back)
    _,nearest=distance_transform_edt(~valid,return_indices=True)
    back=back[tuple(nearest)];front=front[tuple(nearest)]
    # Smooth only the anchor measured on posterior tissue, then cap it at
    # the original boundary so no requested point can cross behind it.
    anchor=np.maximum(back,gaussian_filter(back,1))
    x,y,z=np.meshgrid(*axes,indexing='ij');current=y-old.delta
    vertical=smoothstep((z-12)/12)*(1-smoothstep((z-79)/8))
    lateral=1-smoothstep((abs(x-.65)-20)/5)
    anterior=1-smoothstep((current-front[:,None,:]-2)/10)
    fraction=args.fraction;basilar_profile=None
    if args.basilar_guided:
        ba=trimesh.load(APP/'.authoring/brainstem19/arteries-baseline.glb',process=False).geometry['Basilar']
        grid=np.arange(40.,82.25,.25);envelope=np.full(len(grid),np.inf)
        ids=np.clip(np.floor((ba.vertices[:,2]-grid[0])/.25).astype(int),0,len(grid)-1)
        np.minimum.at(envelope,ids,ba.vertices[:,1]);good=np.isfinite(envelope)
        envelope=np.interp(grid,grid[good],envelope[good]);envelope=gaussian_filter1d(minimum_filter1d(envelope,5),2)
        cap=np.interp(axes[2],grid,envelope)-args.basilar_margin
        cap=cap[None,:]-.012*(axes[0][:,None]-.65)**2
        fraction=np.clip((front-cap)/np.maximum(front-anchor,1.),0,.7)[:,None,:]
        basilar_profile={'z':grid.tolist(),'posteriorWallY':envelope.tolist(),'surfaceToPosteriorWallMarginMm':args.basilar_margin,'lateralCurvatureCoefficient':.012}
    addition=fraction*np.maximum(0,current-anchor[:,None,:])*vertical*lateral*anterior
    if args.lock_surrounding_tissue:
        new.mask=v['mask'].copy()
        distance=distance_transform_edt(~new.mask)
        addition=np.minimum(addition,args.transition_cap*distance)
        addition[new.mask]=0
    new.delta=old.delta+addition
    # Retain AP order including transitions into the accepted registration.
    for j in range(1,len(axes[1])):
        new.delta[:,j,:]=np.minimum(new.delta[:,j,:],new.delta[:,j-1,:]+.65)
    assert np.min(new.delta-old.delta)>-1e-8
    minimum=float(1-np.diff(new.delta,axis=1).max());assert minimum>=.35-1e-8
    d,b=read_glb(APP/'.authoring/brainstem19-coordinated/brain-source-refined.glb')
    records=mesh_records(d,b);base_doc,base_data=read_glb(APP/'public/anatomy/models/brain-context.glb')
    source={};target={};changes=[]
    manifest=json.loads((APP/'.authoring/brainstem19/manifest-baseline.json').read_text())
    selected={r['id'] for r in manifest['structures'] if r.get('anatomy',{}).get('category') in ['brainstem','cerebellum']}|{'brain.fourth-ventricle','brain.aqueduct-of-midbrain'}
    for k,r in records.items():
        if any(t in k for t in ['tentorium-cerebelli','falx-cerebri']):continue
        if args.anatomical_only and k not in selected:continue
        p,f=r['old'],r['faces'];a=old.apply(p);q=new.apply(p)
        amount=np.linalg.norm(q-a,axis=1).max()
        if amount<1e-5:continue
        aa=trimesh.Trimesh(a,f,process=False);bb=trimesh.Trimesh(q,f,process=False)
        source[k]=(a,f,aa.vertex_normals);target[k]=(q,f,bb.vertex_normals)
        changes.append({'node':k,'maximumAdditionalPosteriorDisplacementMm':float(amount),'closedSource':bool(aa.is_watertight),'closedCandidate':bool(bb.is_watertight),'volumeChangeFraction':float(abs(bb.volume)/abs(aa.volume)-1) if aa.is_watertight else None})
    save_replaced(work/'brain-source.glb',base_doc,base_data,source)
    save_replaced(work/'brain-trial.glb',base_doc,base_data,target)
    np.savez_compressed(work/'volume-map.npz',origin=new.origin,delta=new.delta,mask=new.mask)
    np.savez_compressed(work/'posterior-boundaries.npz',x=axes[0],z=axes[2],posterior=back,anterior=front,anchor=anchor,measured=valid)
    report={'method':'column-wise posterior-anchored local AP reduction','requestedReductionFraction':args.fraction,'surroundingTissueLocked':args.lock_surrounding_tissue,'anatomicallyLimitedToPosteriorFossaLabels':args.anatomical_only,'minimumAPJacobian':minimum,'brainSha256':sha(work/'brain-trial.glb'),'sourceSha256':sha(work/'brain-source.glb'),'baselineBrainSha256':sha(APP/'public/anatomy/models/brain-context.glb'),'changes':changes,'appliedToApp':False,'requiresInterlabelBoundaryCheck':args.anatomical_only}
    if basilar_profile:report['method']='posterior-anchored AP reduction guided by retained basilar posterior wall';report['requestedReductionFraction']=None;report['basilarProfile']=basilar_profile
    (work/'registration.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2),flush=True)

if __name__=='__main__':main()
