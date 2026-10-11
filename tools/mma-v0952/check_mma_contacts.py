from common import *
vtk.vtkLogger.SetStderrVerbosity(vtk.vtkLogger.VERBOSITY_OFF)
rev=json.loads((OUT/'revision.json').read_text());changed={r['node'] for r in rev['changed']}
# Include named potential connections as well as primary MMA branches.
names=[n for n in FILES if 'MMA' in n or n.startswith('Middle meningeal')]
mesh={n:load(n,OUT) if n in changed else load(n) for n in FILES}
rows=[]
for n in names:
    v,f=mesh[n];lo=v.min(0)-.2;hi=v.max(0)+.2
    for bn in FILES:
        if not bn.startswith('brain.'):continue
        w,g=mesh[bn]
        if np.any(w.max(0)<lo) or np.any(w.min(0)>hi):continue
        tri=w[g];take=np.all(tri.max(1)>=lo,axis=1)&np.all(tri.min(1)<=hi,axis=1)
        nc=contacts(v,f,w,g[take])
        if nc:rows.append(dict(artery=n,brain=bn,triangleContacts=nc));print(rows[-1],flush=True)
(OUT/'full-mma-brain-check.json').write_text(json.dumps(dict(passed=not rows,checkedLabels=names,contacts=rows),indent=2))
print('MMA brain contact pairs',len(rows),flush=True)
