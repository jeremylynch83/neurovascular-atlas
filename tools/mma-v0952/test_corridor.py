from common import *
vtk.vtkLogger.SetStderrVerbosity(vtk.vtkLogger.VERBOSITY_OFF)
guides=json.loads((WORK/'mma-guides.json').read_text());tree=cKDTree(np.concatenate([g['points'] for g in guides]))
names=['Middle meningeal','Middle meningeal left','MMA frontal','MMA frontal left','MMA frontal anterior division','MMA frontal anterior division left']
vessels={n:load(n,OUT) for n in names}
brain={n:load(n) for n in FILES if n.startswith('brain.')}
result=[]
for amp in [0,1,2,3]:
 total=0;rows=[]
 for bn,(v,f) in brain.items():
  dist=tree.query(v)[0];weight=smooth((9-dist)/7)
  if not weight.any():continue
  direction=np.array([0.,-60.,95.])-v;direction/=np.linalg.norm(direction,axis=1)[:,None]
  q=v+amp*weight[:,None]*direction
  for name,(w,g) in vessels.items():
   if np.any(q.max(0)<w.min(0)) or np.any(q.min(0)>w.max(0)):continue
   num=contacts(w,g,q,f)
   if num:rows.append(dict(artery=name,brain=bn,contacts=num));total+=num
 print(amp,total,flush=True);result.append(dict(amplitudeMm=amp,totalContacts=total,contacts=rows))
 (WORK/'corridor-test.json').write_text(json.dumps(result,indent=2))
