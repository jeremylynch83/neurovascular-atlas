"""Ordered, directional posterior-space experiment with fixed bony/dural barriers."""
import argparse, json, numpy as np, trimesh, vtk
from fit_vessels import APP, read_glb, mesh_records, smoothstep
from build_targets import poly
from reconcile_local_volume import VolumeMap
from refine_context_skin import save_replaced
from reconcile_brainstem import sha
parser=argparse.ArgumentParser();parser.add_argument('--output-directory',default='.authoring/bounded-fossa23');parser.add_argument('--pin-retained-veins',action='store_true');args=parser.parse_args()
W=APP/args.output_directory;W.mkdir(exist_ok=True)
v=np.load(APP/'.authoring/brainstem20-lower-final/volume-map.npz')
m=VolumeMap.__new__(VolumeMap);m.origin=v['origin'];m.shape=np.array(v['delta'].shape);m.mask=np.zeros(m.shape,bool)
brain=trimesh.load(APP/'public/anatomy/models/brain-context.glb',process=False);bones=trimesh.load(APP/'.authoring/bones-baseline.glb',process=False)
parts=list(bones.geometry.values())+[r for k,r in brain.geometry.items() if any(t in k for t in ['falx-cerebri','tentorium-cerebelli'])]
if args.pin_retained_veins:
    from refit_brainstem_sections import KEYS
    veins=trimesh.load(APP/'.authoring/brainstem19/veins-baseline.glb',process=False)
    parts.extend(m for k,m in veins.geometry.items() if k not in KEYS)
obstacles=trimesh.util.concatenate(parts)
loc=vtk.vtkStaticCellLocator();loc.SetDataSet(poly(obstacles));loc.BuildLocator()
axes=[np.arange(n)+o for n,o in zip(m.shape,m.origin)];x,y,z=np.meshgrid(*axes,indexing='ij')
old=v['delta'];current=y-old
w=smoothstep((z-10)/14)*(1-smoothstep((z-72)/13));w*=1-smoothstep((abs(x-.65)-18)/13);w*=1-smoothstep((current+57)/13)
addition=12.*w;caps=np.full(m.shape,np.inf)
for i,xx in enumerate(axes[0]):
    for k,zz in enumerate(axes[2]):
        if not np.any(addition[i,:,k]>1e-8):continue
        points=vtk.vtkPoints();cells=vtk.vtkIdList();loc.IntersectWithLine([xx,-160,zz],[xx,25,zz],1e-7,points,cells)
        hits=np.sort(np.array([points.GetPoint(a)[1] for a in range(points.GetNumberOfPoints())]))
        if len(hits):
            q=current[i,:,k];index=np.searchsorted(hits,q-.01)-1;valid=index>=0
            barrier=hits[np.maximum(index,0)]
            caps[i,valid,k]=.75*np.maximum(0,q[valid]-barrier[valid]-.8)
    print('Barrier columns',i,flush=True)
addition=np.minimum(addition,caps);m.delta=old+addition
# Greatest feasible posterior offset under the directional caps and AP order.
# Each pass only reduces a proposal, so no bony/dural upper bound is relaxed.
for iteration in range(200):
    before=m.delta.copy()
    for j in range(1,m.shape[1]):m.delta[:,j,:]=np.minimum(m.delta[:,j,:],m.delta[:,j-1,:]+.35)
    for j in range(m.shape[1]-2,-1,-1):m.delta[:,j,:]=np.minimum(m.delta[:,j,:],m.delta[:,j+1,:]+.35)
    m.delta=np.maximum(m.delta,old)
    if abs(before-m.delta).max()<1e-9:break
assert float(1-np.diff(m.delta,axis=1).max())>.6
doc,data=read_glb(APP/'.authoring/brainstem19-coordinated/brain-source-refined.glb');records=mesh_records(doc,data)
old_map=VolumeMap.__new__(VolumeMap);old_map.origin=m.origin;old_map.shape=m.shape;old_map.delta=old
base_doc,base_data=read_glb(APP/'public/anatomy/models/brain-context.glb')
replacements={};matched={};changes=[]
for k,r in records.items():
    if any(t in k for t in ['falx-cerebri','tentorium-cerebelli']):continue
    p,f=r['old'],r['faces'];a=old_map.apply(p);b=m.apply(p);amount=np.linalg.norm(a-b,axis=1).max()
    if amount<1e-5:continue
    aa=trimesh.Trimesh(a,f,process=False);bb=trimesh.Trimesh(b,f,process=False)
    replacements[k]=(b,f,bb.vertex_normals);matched[k]=(a,f,aa.vertex_normals)
    changes.append({'node':k,'additionalDisplacementMm':float(amount),'volumeChangeFraction':float(abs(bb.volume)/abs(aa.volume)-1) if aa.is_watertight else None})
save_replaced(W/'brain-trial.glb',base_doc,base_data,replacements);save_replaced(W/'brain-source.glb',base_doc,base_data,matched)
np.savez_compressed(W/'volume-map.npz',origin=m.origin,delta=m.delta,mask=m.mask)
report={'method':'shared ordered AP map, directional posterior skull/dura caps','retainedVeinsUsedAsFixedBarriers':args.pin_retained_veins,'requestedAdditionalPosteriorShiftMm':12.,'minimumAPJacobian':float(1-np.diff(m.delta,axis=1).max()),'brainSha256':sha(W/'brain-trial.glb'),'sourceSha256':sha(W/'brain-source.glb'),'baselineBrainSha256':sha(APP/'public/anatomy/models/brain-context.glb'),'changes':changes,'appliedToApp':False}
(W/'registration.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2),flush=True)
