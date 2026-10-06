"""Small smooth, common-field basilar correction towards the retained stem."""
import json
import numpy as np,trimesh,vtk
from scipy.interpolate import PchipInterpolator
from scipy.ndimage import gaussian_filter1d,maximum_filter1d
from fit_vessels import APP,read_glb,mesh_records,smoothstep,curve_from_mesh
from seat_posterior_candidate import locator,front_fn
from refine_context_skin import save_replaced
from build_targets import poly
from verify_fitting import collisions,distances,stats
from reconcile_brainstem import sha

def main():
    w=APP/'.authoring/posterior-tubular55';brain=trimesh.load(w/'brain-trial.glb',process=False);stem=trimesh.util.concatenate([m for k,m in brain.geometry.items() if any(t in k for t in ['pons.','midbrain.','medulla-oblongata','base-of-peduncle'])]);front=front_fn(locator(stem));d,b=read_glb(w/'arteries-source.glb');rr=mesh_records(d,b);old=trimesh.Trimesh(rr['Basilar']['old'],rr['Basilar']['faces'],process=False);v=np.vstack([old.vertices,old.triangles.mean(1)]);z=np.arange(40.,82.01,.1);need=np.full(len(z),-np.inf)
    for p in v:
        if not z[0]<=p[2]<=z[-1]:continue
        surface=front(p[0],p[2])
        if surface is not None:i=int(np.clip(round((p[2]-z[0])/.1),0,len(z)-1));need[i]=max(need[i],surface+.04-p[1])
    good=np.isfinite(need);need=np.interp(z,z[good],need[good]);need=maximum_filter1d(need,5);delta=np.max(need[None,:]-.12*abs(z[:,None]-z[None,:]),axis=1);delta=np.maximum(delta,gaussian_filter1d(delta,3));delta=np.clip(delta,-.15,0);zz=np.r_[z[0]-8,z,z[-1]+8];fn=PchipInterpolator(zz,np.r_[0,delta,0]);c=curve_from_mesh(old,axis=2,n=140);cy=PchipInterpolator(c[:,2],c[:,1]);bones=trimesh.load(APP/'.authoring/bones-baseline.glb',process=False);bone=trimesh.util.concatenate([m for k,m in bones.geometry.items() if k in ['bone.sphenoid','bone.occipital','bone.temporal.left','bone.temporal.right']]);implicit=vtk.vtkImplicitPolyDataDistance();implicit.SetInput(poly(bone));targets={};changed=[]
    for k,r in rr.items():
        p=r['old'];height=np.clip(p[:,2],zz[0],zz[-1]);weight=(1-smoothstep((abs(p[:,0]-.65)-4)/6))*(1-smoothstep((abs(p[:,1]-cy(np.clip(height,c[0,2],c[-1,2])))-4)/6));shift=fn(height)*weight*(p[:,2]>zz[0])*(p[:,2]<zz[-1]);active=np.flatnonzero(abs(shift)>1e-7)
        for i in active:shift[i]*=smoothstep((abs(implicit.EvaluateFunction(p[i]))-.2)/.8)
        if not np.max(abs(shift))>1e-7:continue
        q=p.copy();q[:,1]+=shift;m=trimesh.Trimesh(q,r['faces'],process=False);targets[k]=(q,r['faces'],m.vertex_normals);changed.append(k)
    save_replaced(w/'arteries-trial.glb',d,b,targets);new=trimesh.load(w/'arteries-trial.glb',process=False).geometry['Basilar'];plexus=trimesh.load(w/'veins-trial.glb',process=False).geometry['vein.basilar_plexus'];signed=[]
    for p in np.vstack([new.vertices,new.triangles.mean(1)]):
        y=front(p[0],p[2])
        if y is not None:signed.append(p[1]-y)
    report={'maximumPosteriorShiftMm':float(abs(delta).max()),'commonFieldChangedLabels':changed,'basilarStemContacts':collisions(new,stem),'basilarPlexusContacts':collisions(new,plexus),'basilarBoneContacts':collisions(new,bone),'sampledAnteriorWallPenetrations':int((np.array(signed)<-.05).sum()),'minimumAnteriorWallRayGapMm':float(min(signed)),'boneWallDistance':stats(distances(new.vertices,bone)),'accepted':False};(w/'basilar-apposition.json').write_text(json.dumps(report,indent=2)+'\n');trial=json.loads((w/'trial.json').read_text());trial['basilarRetained']=False;trial['gentleBasilarApposition']=report;trial['hashes']['arteries']=sha(w/'arteries-trial.glb');(w/'trial.json').write_text(json.dumps(trial,indent=2)+'\n');print(report,flush=True)

if __name__=='__main__':main()
