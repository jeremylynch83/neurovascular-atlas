from model import *
import shutil,sys
alpha=float(sys.argv[1]);RAW=ROOT/'undamped';RAW.mkdir(exist_ok=True)
r=json.load(open(OUT/'revision.json'));rows=[a for a in r['changed'] if a['file']=='venous.glb'];vv=[];ff=[];ranges=[];offset=0
for a in rows:
 n=a['node'];p=RAW/(n+'.positions.bin')
 if not p.exists():shutil.copy2(OUT/(n+'.positions.bin'),p)
 source,f=load(n);target=np.fromfile(p,'<f4').reshape(-1,3);v=(source+alpha*(target-source)).astype('<f4');vv.append(v);ff.append(f+offset);ranges.append((n,offset,offset+len(v),f));offset+=len(v)
v=np.concatenate(vv);k=np.ascontiguousarray(v).view('V12').ravel();_,ids,inv=np.unique(k,return_index=True,return_inverse=True);mesh=normals(poly(v[ids].astype(float),inv[np.concatenate(ff)]));nn=vtk_to_numpy(mesh.GetPointData().GetNormals()).astype('<f4');nn/=np.maximum(np.linalg.norm(nn,axis=1)[:,None],1e-12)
for n,a,b,f in ranges:
 v[a:b].tofile(OUT/(n+'.positions.bin'));nn[inv[a:b]].astype('<f4').tofile(OUT/(n+'.normals.bin'))
(OUT/'damping.json').write_text(json.dumps({'venousDisplacementFraction':alpha,'reason':'Retain a smaller posterior chamber while avoiding inversion of delicate venous collar triangles'},indent=2));print('Venous displacement fraction',alpha,flush=True)
