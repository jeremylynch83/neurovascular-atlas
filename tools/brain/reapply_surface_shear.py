"""Apply the cached surface shear with the final physical bone limits."""
import json,numpy as np,trimesh,vtk
from vtk.util.numpy_support import vtk_to_numpy
from scipy.interpolate import RegularGridInterpolator
from fit_vessels import APP,read_glb,mesh_records,smoothstep,neighbours
from reconcile_brainstem import ANTERIOR,TRANSVERSE,LATERAL
from scipy.spatial import cKDTree
from fit_brainstem_shear import ShearGrid
from refine_context_skin import save_replaced
from build_targets import poly
from reconcile_brainstem import sha

def main():
    out=APP/'.authoring/posterior-shear51';cache=np.load(out/'surface-shear.npz');g=ShearGrid();g.x=cache['x'];g.z=cache['z'];g.shape=(len(g.x),len(g.z));g.delta=cache['delta']
    bones=trimesh.load(APP/'.authoring/bones-baseline.glb',process=False);bone=trimesh.util.concatenate([m for k,m in bones.geometry.items() if k in ['bone.occipital','bone.sphenoid','bone.temporal.right','bone.temporal.left']]);implicit=vtk.vtkImplicitPolyDataDistance();implicit.SetInput(poly(bone));sample=vtk.vtkSampleFunction();sample.SetImplicitFunction(implicit);sample.SetModelBounds(-35,36,-135,-40,-5,96);sample.SetSampleDimensions(72,96,102);sample.ComputeNormalsOff();sample.Update();volume=abs(vtk_to_numpy(sample.GetOutput().GetPointData().GetScalars()).reshape(102,96,72).transpose(2,1,0));D=RegularGridInterpolator((np.arange(-35.,37.),np.arange(-135.,-39.),np.arange(-5.,97.)),volume,bounds_error=False,fill_value=0)
    d,b=read_glb(out/'veins-source.glb');rr=mesh_records(d,b);targets={}
    keys=set(ANTERIOR+TRANSVERSE+LATERAL+['vein.anterior_spinal']+[f'vein.{k}.{s}' for k in ['superior_petrosal_vein','cerebellopontine_fissure'] for s in ['left','right']]);keys=neighbours(rr,keys)-{'vein.basilar_plexus'}
    outer=cKDTree(np.concatenate([r['old'] for k,r in rr.items() if k not in keys]));fixed=np.concatenate([r['old'][outer.query(r['old'])[0]<2e-5] for k,r in rr.items() if k in keys]);frozen=cKDTree(fixed) if len(fixed) else None
    for k,r in rr.items():
        if k not in keys:continue
        v=r['old'];q=g.apply(v);shift=q[:,1]-v[:,1];shift*=smoothstep((v[:,1]+135)/20)*(1-smoothstep((v[:,1]+51)/11))
        if frozen:shift*=smoothstep(frozen.query(v)[0]/8)
        limit=.9*np.maximum(D(v)-.05,0);q[:,1]=v[:,1]+np.clip(shift,-limit,limit)
        if np.max(abs(q-v))<1e-7:continue
        m=trimesh.Trimesh(q,r['faces'],process=False);targets[k]=(q,r['faces'],m.vertex_normals)
    save_replaced(out/'veins-trial.glb',d,b,targets);r=json.loads((out/'trial.json').read_text());r.pop('excludedOutletCollarMm',None);r['physicalBoneLimitCoefficient']=.9;r['physicalBoneLimitBufferMm']=.05;r['coordinateJacobianAppliesToUncappedShearOnly']=True;r['hashes']['veins']=sha(out/'veins-trial.glb');(out/'trial.json').write_text(json.dumps(r,indent=2)+'\n');print('Applied cached section fit',len(targets),'labels',flush=True)

if __name__=='__main__':main()
