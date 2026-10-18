from probe import *
from geometry import edge_table,cycles
from collections import defaultdict,deque
O=W/(sys.argv[1]if len(sys.argv)>1 else 'candidate');d=json.loads((A/'public/anatomy/dsa-surfaces.json').read_text());reports=[]
for side in ['right','left']:
 for part in ['inferior_ophthalmic','superior_ophthalmic']:
  n='vein.'+part+'.'+side;v=np.fromfile(O/(n+'.positions.bin'),'<f4').reshape(-1,3);f=np.fromfile(O/(n+'.indices.bin'),'<u4').reshape(-1,3);oldv,oldf=scene.mesh(n);old=d['entries'][n];oldflips=set(old['flips']);lookup=defaultdict(deque)
  for i,t in enumerate(oldv[oldf]):lookup[tuple(sorted(map(tuple,t)))].append(i)
  flips=[]
  for i,t in enumerate(v[f]):
   pool=lookup.get(tuple(sorted(map(tuple,t))));j=pool.popleft()if pool else None
   if j in oldflips:flips.append(i)
  g=f.copy();g[flips]=g[flips,::-1];u,e,c,b,di,_=edge_table(v,g);assert not np.any(c>2)and not np.any((c==2)&(b!=0)),n
  loops=cycles(di[c==1]);idx={tuple(q):i for i,q in enumerate(v)};extra=[];caps=[]
  for loop in loops:
   ring=np.array([idx[tuple(q)]for q in u[loop]]);centre=len(v)+len(extra);extra.append(v[ring].mean(0).astype(float).tolist())
   for a,b in zip(ring,np.roll(ring,-1)):caps.extend([centre,int(b),int(a)])
  vv=np.vstack([v,extra]);ff=np.vstack([g,np.array(caps).reshape(-1,3)]);t=vv[ff].astype(float);volume=float(np.einsum('ij,ij->i',t[:,0],np.cross(t[:,1],t[:,2])).sum()/6)
  _,_,c,b,*_=edge_table(vv,ff);assert np.all(c==2)and np.all(b==0)and volume>0,n
  d['entries'][n]={'vertexCount':len(v),'extra':extra,'reverse':False,'flips':flips,'removed':[],'caps':caps,'faces':len(ff),'removedSeamFaces':0,'volumeMm3':volume};row={'node':n,'capLoops':len(loops),'closedAndOriented':True,'volumeMm3':volume};reports.append(row);print(row,flush=True)
(O/'dsa-surfaces.json').write_text(json.dumps(d));(O/'projection-check.json').write_text(json.dumps({'passed':True,'results':reports},indent=2))
