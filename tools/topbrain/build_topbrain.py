#!/usr/bin/env python3
from pathlib import Path
import sys,json
import nibabel as nib
import numpy as np
from skimage import measure
import trimesh
from common import ensure_unpacked,find_case_files

raw=Path(sys.argv[1]); case=sys.argv[2].zfill(3); root=ensure_unpacked(raw)
imgp,labp=find_case_files(root,case,'ct')
if not imgp or not labp: raise SystemExit(f'Could not locate CTA image and v1 CTA label mask for case {case}')
img=nib.load(str(imgp)); lab=nib.load(str(labp)); data=np.asanyarray(img.dataobj); labels=np.asanyarray(lab.dataobj).astype(np.int16)
if data.shape!=labels.shape: raise SystemExit(f'Image/label shape mismatch {data.shape} vs {labels.shape}')

# TopBrain v1 CTA label map, official values 1-40.
MAP={
1:'artery.basilar',2:'artery.pca.right.p1p2',3:'artery.pca.left.p1p2',4:'artery.carotid.internal.right',5:'artery.mca.right.m1',6:'artery.carotid.internal.left',7:'artery.mca.left.m1',8:'artery.ica.pcom.right',9:'artery.ica.pcom.left',10:'artery.acom',11:'artery.aca.right.a1a2',12:'artery.aca.left.a1a2',13:'artery.aca.right.a3',14:'artery.aca.left.a3',17:'artery.mca.right.m2',18:'artery.mca.right.m3',19:'artery.mca.left.m2',20:'artery.mca.left.m3',21:'artery.pca.right.p3p4',22:'artery.pca.left.p3p4',23:'artery.vertebral.right',24:'artery.vertebral.left',25:'artery.sca.right',26:'artery.sca.left',27:'artery.aica.right',28:'artery.aica.left',29:'artery.pica.right',30:'artery.pica.left',31:'artery.ica.anterior_choroidal.right',32:'artery.ica.anterior_choroidal.left',33:'artery.ica.ophthalmic.right',34:'artery.ica.ophthalmic.left',35:'vein.deep.galen',36:'vein.sinus.straight',37:'vein.deep.internal_cerebral.pair',38:'vein.deep.basal_rosenthal.right',39:'vein.deep.basal_rosenthal.left',40:'vein.sinus.superior_sagittal'}
# Labels 15/16 are variant third A2/A3 arteries and are retained as source data but not rendered until variant catalogue support lands.

def mesh_mask(mask,step=1):
    if mask.sum()<8:return None
    verts,faces,normals,_=measure.marching_cubes(mask.astype(np.uint8),0.5,step_size=step,allow_degenerate=False)
    # marching_cubes coordinates follow the NIfTI array axes; apply voxel-to-world affine.
    verts=nib.affines.apply_affine(img.affine,verts)
    m=trimesh.Trimesh(vertices=verts,faces=faces,process=False)
    m.remove_unreferenced_vertices()
    return m

scene=trimesh.Scene(); patch=[]
for value,sid in MAP.items():
    mask=labels==value
    m=mesh_mask(mask,1)
    if m is None: continue
    scene.add_geometry(m,node_name=sid,geom_name=sid)
    patch.append({'id':sid,'geometryStatus':'master','provenance':{'sourceType':'scan-derived','confidence':'high','reviewStatus':'unreviewed','sourceRefs':['dataset.topbrain.v3']},'asset':{'file':'models/topbrain-reference.glb','node':sid}})
    print(f'{value:02d} {sid}: {int(mask.sum())} voxels, {len(m.faces)} faces')

# CT-derived skull context. Retain only large high-density components to suppress most contrast-filled vessels.
finite=data[np.isfinite(data)]
threshold=500.0 if finite.size and np.percentile(finite,99)>700 else float(np.percentile(finite,98.5))
bone=data>threshold
cc=measure.label(bone,connectivity=1); counts=np.bincount(cc.ravel()); keep=np.argsort(counts[1:])[-12:]+1 if len(counts)>1 else []
bone=np.isin(cc,keep)
bm=mesh_mask(bone,2)
if bm is not None:
    sid='bone.skull.scan_reference'; scene.add_geometry(bm,node_name=sid,geom_name=sid)
    patch.append({'id':sid,'new':True,'name':f'CT-derived reference skull (TopBrain {case})','parent':'bone.skull','system':'bone','side':'midline','kind':'structure','aliases':['reference skull'],'geometryStatus':'master','provenance':{'sourceType':'scan-derived','confidence':'moderate','reviewStatus':'unreviewed','sourceRefs':['dataset.topbrain.v3']},'asset':{'file':'models/topbrain-reference.glb','node':sid}})
    print(f'skull threshold {threshold:.1f}: {len(bm.faces)} faces')

out=Path('/work/public/anatomy/models/topbrain-reference.glb'); out.parent.mkdir(parents=True,exist_ok=True); scene.export(out)
gen=Path('/work/anatomy/generated');gen.mkdir(parents=True,exist_ok=True)
(gen/'topbrain_patch.json').write_text(json.dumps({'case':case,'image':imgp.name,'label':labp.name,'patch':patch},indent=2)+'\n')
print(f'Wrote {out} and generated catalogue patch for case {case}.')
