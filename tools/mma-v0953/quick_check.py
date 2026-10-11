from common import *
vtk.vtkLogger.SetStderrVerbosity(vtk.vtkLogger.VERBOSITY_OFF)
r=json.loads((OUT/'revision.json').read_text());changed={x['node'] for x in r['changed']};after={n:load(n,OUT) for n in changed};mesh={n:load(n) for n in FILES};rows=[]
for n in ['Middle meningeal','Middle meningeal left','MMA frontal','MMA frontal left','MMA frontal anterior division','MMA frontal anterior division left','MMA orbital','MMA orbital left']:
 v,f=mesh[n];q,g=after.get(n,(v,f));lo=np.minimum(v.min(0),q.min(0));hi=np.maximum(v.max(0),q.max(0))
 for other,(w,h) in mesh.items():
  if not other.startswith('brain.') or np.any(w.max(0)<lo) or np.any(w.min(0)>hi):continue
  ww,hh=after.get(other,(w,h));before=contacts(v,f,w,h);now=contacts(q,g,ww,hh)
  if before or now:row=dict(a=n,b=other,before=before,after=now);rows.append(row);print(row,flush=True)
(OUT/'quick-brain.json').write_text(json.dumps(rows,indent=2))
