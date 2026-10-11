from common import *
vtk.vtkLogger.SetStderrVerbosity(vtk.vtkLogger.VERBOSITY_OFF)
guides=json.loads((WORK/'mma-guides.json').read_text());points=np.concatenate([g['points'] for g in guides]);direction=np.concatenate([g['innerTableNormals'] for g in guides]);tree=cKDTree(points)
names=['Middle meningeal','Middle meningeal left','MMA frontal','MMA frontal left']
vessels={n:load(n,OUT) for n in names};brain={n:load(n) for n in FILES if n.startswith('brain.')};results=[]
for amp in [2.,3.5]:
 rows=[];total=0
 for bn,(v,f) in brain.items():
  dist,k=tree.query(v,k=8);w=np.exp(-dist**2/8);vec=np.einsum('ij,ijk->ik',w,direction[k]);vec/=np.maximum(np.linalg.norm(vec,axis=1)[:,None],1e-12);weight=smooth((9-dist[:,0])/7)
  if not weight.any():continue
  q=v+amp*weight[:,None]*vec
  for n,(u,g) in vessels.items():
   if np.any(q.max(0)<u.min(0)) or np.any(q.min(0)>u.max(0)):continue
   num=contacts(u,g,q,f)
   if num:rows.append(dict(artery=n,brain=bn,contacts=num));total+=num
 print(amp,total,flush=True);results.append(dict(amplitudeMm=amp,contacts=rows,totalContacts=total));(WORK/'normal-corridor-test.json').write_text(json.dumps(results,indent=2))
