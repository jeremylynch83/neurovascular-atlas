import json,trimesh,numpy as np,argparse
from pathlib import Path
from scipy.spatial import cKDTree
from scipy.optimize import least_squares
from scipy.spatial.transform import Rotation
parser=argparse.ArgumentParser(description='Authoring-only skull correspondence fit; requires source skull GLB in source-orientation coordinates and decoded app reference.')
parser.add_argument('--source-skull',type=Path,required=True);parser.add_argument('--reference',type=Path,required=True);parser.add_argument('--output',type=Path,required=True);args=parser.parse_args()
ref=args.reference;records=json.load(open(ref/'reference.json'));src=trimesh.load(args.source_skull,force='scene');pairs=[]
for n in src.geometry:
 side='.left' if n.endswith('.l') else '.right' if n.endswith('.r') else ''
 name='bone.'+n.split(' ')[0].lower()+side;r=next(r for r in records if r['name']==name)
 tgt=np.array(np.memmap(ref/'reference.bin',dtype='<f4',offset=r['positionOffset'],shape=(r['vertices'],3),mode='r'))
 p=np.array(src.geometry[n].vertices);p=p@np.array([[-1,0,0],[0,0,1],[0,1,0]]).T
 rng=np.random.default_rng(34);p=p[rng.choice(len(p),min(7000,len(p)),replace=False)]
 pairs.append((n,p,tgt,cKDTree(tgt)))
x=np.array([0.,0.,0.,np.log(.97),.65,-58,87])
def move(p,x):return np.exp(x[3])*(p@Rotation.from_rotvec(x[:3]).as_matrix().T)+x[4:]
for i in range(35):
 a=[];b=[]
 for n,p,tgt,kd in pairs:
  q=move(p,x);d,ix=kd.query(q);keep=d<np.percentile(d,85);a.append(p[keep]);b.append(tgt[ix[keep]])
 a=np.concatenate(a);b=np.concatenate(b)
 res=least_squares(lambda v:(move(a,v)-b).ravel(),x,max_nfev=15,loss='soft_l1',f_scale=1.);x=res.x
 if i%5==0:print(i,x.tolist(),flush=True)
T=np.eye(4);T[:3,:3]=np.exp(x[3])*Rotation.from_rotvec(x[:3]).as_matrix()@np.array([[-1,0,0],[0,0,1],[0,1,0]]);T[:3,3]=x[4:]
stats={}
for n,p,tgt,kd in pairs:
 d,_=kd.query(move(p,x));stats[n]={'median_vertex_distance_mm':float(np.median(d)),'p95_vertex_distance_mm':float(np.percentile(d,95))};print(n,stats[n])
report={'matrix':T.tolist(),'scale':float(np.exp(x[3])),'rotation_radians_after_RAS':x[:3].tolist(),'skull_residuals':stats,'method':'Bone-correspondence similarity ICP, 85% trimmed nearest vertices, robust least squares; 7 cranial bone meshes; source Z-Anatomy skull to retained v0.9.13 skull. No independent brain deformation.'}
args.output.write_text(json.dumps(report,indent=2));print(T)
