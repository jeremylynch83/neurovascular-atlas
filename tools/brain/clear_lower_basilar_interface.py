"""A small posterior-anchored correction at the basilar lower stem interface."""
import argparse,json,shutil
import numpy as np,trimesh,vtk
from scipy.interpolate import RegularGridInterpolator
from scipy.ndimage import distance_transform_edt
from fit_vessels import APP,read_glb,mesh_records,smoothstep
from build_targets import poly
from refine_context_skin import save_replaced
from reconcile_brainstem import sha

def main():
    p=argparse.ArgumentParser();p.add_argument('--brain-directory',default='.authoring/posterior-context33');p.add_argument('--output-directory',default='.authoring/posterior-context34');a=p.parse_args();src=APP/a.brain_directory;w=APP/a.output_directory;w.mkdir(parents=True,exist_ok=True)
    scene=trimesh.load(src/'brain-trial.glb',process=False);m=trimesh.util.concatenate([m for k,m in scene.geometry.items() if any(t in k for t in ['pons.','medulla-oblongata','midbrain.','base-of-peduncle'])]);loc=vtk.vtkStaticCellLocator();loc.SetDataSet(poly(m));loc.BuildLocator()
    xx=np.arange(-10.,12.);zz=np.arange(38.,56.);back=np.full((len(xx),len(zz)),np.nan);front=back.copy()
    for i,x in enumerate(xx):
        for j,z in enumerate(zz):
            pts=vtk.vtkPoints();ids=vtk.vtkIdList();loc.IntersectWithLine([x,-130,z],[x,-35,z],1e-8,pts,ids)
            if pts.GetNumberOfPoints():ys=[pts.GetPoint(k)[1] for k in range(pts.GetNumberOfPoints())];back[i,j]=min(ys);front[i,j]=max(ys)
    _,nearest=distance_transform_edt(~np.isfinite(back),return_indices=True);back=back[tuple(nearest)];front=front[tuple(nearest)]
    bf=RegularGridInterpolator((xx,zz),back,bounds_error=False,fill_value=None);ff=RegularGridInterpolator((xx,zz),front,bounds_error=False,fill_value=None)
    d,b=read_glb(src/'brain-trial.glb');records=mesh_records(d,b);target={};changes=[]
    manifest=json.loads((APP/'.authoring/brainstem19/manifest-baseline.json').read_text());selected={r['id'] for r in manifest['structures'] if r.get('anatomy',{}).get('category') in ['brainstem','cerebellum']}|{'brain.fourth-ventricle'}
    for key,r in records.items():
        if key not in selected:continue
        v,f=r['old'],r['faces'];q=v.copy();active=(abs(v[:,0]-.65)<10)&(v[:,2]>39)&(v[:,2]<54)
        p=v[active];xz=p[:,[0,2]];bb=bf(xz);tt=ff(xz)
        weight=(1-smoothstep((abs(p[:,0]-.65)-4)/6))*smoothstep((p[:,2]-39)/4)*(1-smoothstep((p[:,2]-49)/5))
        inside_front=1-smoothstep((p[:,1]-tt)/4)
        addition=.28*np.maximum(0,p[:,1]-bb)*weight*inside_front
        q[active,1]-=addition
        if addition.max(initial=0)<1e-5:continue
        mesh=trimesh.Trimesh(q,f,process=False);target[key]=(q,f,mesh.vertex_normals);changes.append({'node':key,'maximumAdditionalPosteriorDisplacementMm':float(addition.max())})
    save_replaced(w/'brain-trial.glb',d,b,target);shutil.copyfile(src/'brain-source.glb',w/'brain-source.glb');shutil.copyfile(src/'volume-map.npz',w/'volume-map.npz')
    report=json.loads((src/'registration.json').read_text());report['parentBrainSha256']=report['brainSha256'];report['brainSha256']=sha(w/'brain-trial.glb');report['lowerBasilarInterface']={'method':'28 percent column contraction within X/Z support, posterior boundary retained','changes':changes};report['volumeMapDescribesOnlyParentAPReduction']=True;(w/'registration.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report['lowerBasilarInterface'],indent=2),flush=True)

if __name__=='__main__':main()
