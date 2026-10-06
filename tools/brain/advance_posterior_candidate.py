"""Advance the review candidate and expand the pons through one common AP map.

Brain, arterial and venous material points use the same continuous field.
The basilar plexus, dural collectors and external attachment collars are fixed.
This stages a candidate only; it never edits production anatomy.
"""
import argparse,json,shutil
import numpy as np,trimesh,vtk
from vtk.util.numpy_support import vtk_to_numpy
from scipy.interpolate import RegularGridInterpolator
from scipy.ndimage import distance_transform_edt,gaussian_filter
from scipy.spatial import cKDTree
from fit_vessels import APP,read_glb,mesh_records,smoothstep
from build_targets import poly
from refine_context_skin import save_replaced
from reconcile_brainstem import sha,ANTERIOR,TRANSVERSE,LATERAL

def main():
    p=argparse.ArgumentParser();p.add_argument('--input',default='.authoring/posterior-family40');p.add_argument('--output',default='.authoring/posterior-forward42');p.add_argument('--advance',type=float,default=2.);p.add_argument('--fullness',type=float,default=3.);a=p.parse_args()
    src=APP/a.input;out=APP/a.output;out.mkdir(parents=True,exist_ok=True)
    scene=trimesh.load(src/'brain-trial.glb',process=False)
    stem=trimesh.util.concatenate([m for k,m in scene.geometry.items() if any(t in k for t in ['pons.','medulla-oblongata','midbrain.','base-of-peduncle'])])
    loc=vtk.vtkStaticCellLocator();loc.SetDataSet(poly(stem));loc.BuildLocator()
    xx=np.arange(-29.,31.);zz=np.arange(10.,94.);back=np.full((len(xx),len(zz)),np.nan);front=back.copy()
    for i,x in enumerate(xx):
        for j,z in enumerate(zz):
            pts=vtk.vtkPoints();ids=vtk.vtkIdList();loc.IntersectWithLine([x,-145,z],[x,-30,z],1e-8,pts,ids)
            if pts.GetNumberOfPoints():
                yy=[pts.GetPoint(k)[1] for k in range(pts.GetNumberOfPoints())];back[i,j]=min(yy);front[i,j]=max(yy)
    valid=np.isfinite(back);_,near=distance_transform_edt(~valid,return_indices=True)
    back=gaussian_filter(back[tuple(near)],.8);front=gaussian_filter(front[tuple(near)],.8)
    B=RegularGridInterpolator((xx,zz),back,bounds_error=False,fill_value=None);F=RegularGridInterpolator((xx,zz),front,bounds_error=False,fill_value=None)
    np.savez_compressed(out/'field-profiles.npz',x=xx,z=zz,back=back,front=front,advance=a.advance,fullness=a.fullness)
    bones=trimesh.load(APP/'.authoring/bones-baseline.glb',process=False)
    bone=trimesh.util.concatenate([m for k,m in bones.geometry.items() if k in ['bone.occipital','bone.sphenoid','bone.temporal.right','bone.temporal.left']])
    implicit=vtk.vtkImplicitPolyDataDistance();implicit.SetInput(poly(bone))
    sample=vtk.vtkSampleFunction();sample.SetImplicitFunction(implicit);sample.SetModelBounds(-30,31,-127,-29,9,94);sample.SetSampleDimensions(62,99,86);sample.ComputeNormalsOff();sample.Update()
    volume=abs(vtk_to_numpy(sample.GetOutput().GetPointData().GetScalars()).reshape(86,99,62).transpose(2,1,0))
    bone_distance=RegularGridInterpolator((np.arange(-30.,32.),np.arange(-127.,-28.),np.arange(9.,95.)),volume,bounds_error=False,fill_value=0)
    assets={};all_fixed=[]
    manifest=json.loads((APP/'.authoring/brainstem19/manifest-baseline.json').read_text())
    brain_keys={r['id'] for r in manifest['structures'] if r.get('anatomy',{}).get('category') in ['brainstem','cerebellum']}|{'brain.fourth-ventricle','brain.aqueduct-of-midbrain'}
    vein_keys=set(ANTERIOR+TRANSVERSE+LATERAL+['vein.anterior_spinal']+[f'vein.{k}.{s}' for k in ['superior_petrosal_vein','cerebellopontine_fissure','basal'] for s in ['left','right']])
    for kind,selected in [('brain',brain_keys),('veins',vein_keys),('arteries',None)]:
        d,data=read_glb(src/f'{kind}-trial.glb');records=mesh_records(d,data)
        if kind=='arteries':
            selected={k for k in records if k=='Basilar' or any(k.startswith(t) for t in ['Vertebral V4','PCA ','SCA ','AICA ','PICA ','Pontine ','Anterior spinal','Posterior spinal','VA medullary','Thalamoperforator','Thalamogeniculate','Peduncular perforator','Medial posterior choroidal','Lateral posterior choroidal','Labyrinthine','Common cochlear','Anterior vestibular'])}
        selected=selected&set(records)
        others=np.concatenate([r['old'] for k,r in records.items() if k not in selected]);outer=cKDTree(others)
        fixed=np.concatenate([r['old'][outer.query(r['old'])[0]<2e-5] for k,r in records.items() if k in selected]);all_fixed.append(fixed)
        assets[kind]=(d,data,records,selected)
    fixed_tree=cKDTree(np.concatenate(all_fixed))
    print('Common boundary anchors',sum(map(len,all_fixed)),flush=True)
    def field(p):
        x,y,z=p.T;dx=abs(x-.65)
        active=smoothstep((z-18)/10)*(1-smoothstep((z-78)/12))*(1-smoothstep((dx-19)/12))
        active*=smoothstep((y+126)/24)*(1-smoothstep((y+42)/12))
        coords=np.column_stack([np.clip(x,xx[0],xx[-1]),np.clip(z,zz[0],zz[-1])]);b=B(coords);f=F(coords)
        rounded=np.sin(np.pi*np.clip((z-45)/29,0,1))**2
        rounded*=1-smoothstep((dx-10)/15)
        # Analytic AP expansion avoids abrupt changes between sampled columns.
        # It adds anterior convexity while gently expanding the posterior pons.
        shift=active*(a.advance+a.fullness*rounded*np.tanh((y+75)/6))
        # One attachment collar is shared across all three asset families.
        shift*=smoothstep(fixed_tree.query(p)[0]/12.)
        # Keep at least 1.5 mm from bone where there is an existing free gap.
        # Existing near-bone surfaces are stationary rather than advanced.
        limit=.4*np.maximum(bone_distance(p)-1.5,0)
        shift=np.clip(shift,-limit,limit)
        q=p.copy();q[:,1]+=shift;return q
    report={'parentDirectory':a.input,'baseAnteriorShiftMm':a.advance,'maximumLocalPontineExpansionPerSurfaceMm':a.fullness,'method':'common AP map with anterior advancement and smoothly rounded pontine expansion','basilarPlexusFixed':True,'accepted':False,'appliedToApp':False,'assets':{}}
    for kind,(d,data,records,selected) in assets.items():
        changes=[];targets={}
        for k in sorted(selected):
            r=records[k];v=r['old'];q=field(v)
            if np.max(abs(q-v))<1e-7:continue
            m=trimesh.Trimesh(q,r['faces'],process=False);targets[k]=(q,r['faces'],m.vertex_normals)
            changes.append({'node':k,'maximumDisplacementMm':float(np.linalg.norm(q-v,axis=1).max()),'medianAPDisplacementMm':float(np.median(q[:,1]-v[:,1]))})
        save_replaced(out/f'{kind}-trial.glb',d,data,targets)
        shutil.copyfile(src/f'{kind}-trial.glb',out/f'{kind}-source.glb')
        report['assets'][kind]={'changes':changes,'sourceSha256':sha(out/f'{kind}-source.glb'),'trialSha256':sha(out/f'{kind}-trial.glb')}
        print(kind,'changed',len(changes),'maximum',max(r['maximumDisplacementMm'] for r in changes),flush=True)
    (out/'trial.json').write_text(json.dumps(report,indent=2)+'\n')

if __name__=='__main__':main()
