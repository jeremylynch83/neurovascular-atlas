"""Refresh selected changed DSA recipes from retained faces and current native boundaries."""
import sys,json,itertools,numpy as np
from pathlib import Path
from collections import defaultdict,deque
W=Path(sys.argv[1]);A=Path(sys.argv[2]);m=json.load(open(A/'public/anatomy/manifest.json'));d=json.load(open(A/'public/anatomy/dsa-surfaces.json'));reports=[]
N=[r['node']for r in json.load(open(W/'accepted-patches.json'))['changes']]
for node in N:
 sid=next(s['id']for s in m['structures']if s.get('asset',{}).get('node')==node);old=d['entries'][sid];p=np.fromfile(W/'candidate'/(node+'.positions.bin'),'<f4').reshape(-1,3).astype(float);f=np.fromfile(W/'candidate'/(node+'.indices.bin'),'<u4').reshape(-1,3);v=np.fromfile(W/'decoded'/(node+'.positions.bin'),'<f4').reshape(-1,3).astype(float);g=np.fromfile(W/'decoded'/(node+'.indices.bin'),'<u4').reshape(-1,3)
 def key(q):return tuple(sorted(tuple(x)for x in q))
 source=defaultdict(deque)
 for i,t in enumerate(g):source[key(v[t])].append(i)
 removed=[];flips=[];unmatched=[];oldrem=set(old['removed']);oldflips=set(old['flips'])
 for i,t in enumerate(f):
  pool=source.get(key(p[t]));idx=pool.popleft()if pool else None
  if idx is None:unmatched.append(i)
  if idx in oldrem:removed.append(i)
  if idx in oldflips:flips.append(i)
 # Propagate orientation constraints from the retained DSA faces to
 # the new wall triangles. Each paired edge must have opposite directions.
 newids=set(unmatched);canonical=np.unique(np.round(p,8),axis=0,return_inverse=True)[1]
 incidences=defaultdict(list);removed_set=set(removed);source_flips=set(flips)
 for i,t in enumerate(f):
  if i in removed_set:continue
  q=canonical[t[::-1]if(old['reverse']!=(i in source_flips))else t]
  for x,y in zip(q,np.roll(q,-1)):
   if x!=y:incidences[tuple(sorted([int(x),int(y)]))].append((i,int(x<y)))
 adj=defaultdict(list);state={};todo=deque()
 def assign(i,value):
  if i in state:assert state[i]==value,('inconsistent-new-face-orientation',node,i)
  else:state[i]=value;todo.append(i)
 for edge,rows in incidences.items():
  if len(rows)!=2:continue
  (i,di),(j,dj)=rows;parity=di==dj
  if i in newids and j in newids:adj[i].append((j,parity));adj[j].append((i,parity))
  elif i in newids:assign(i,parity)
  elif j in newids:assign(j,parity)
 def propagate():
  while todo:
   i=todo.popleft()
   for j,parity in adj[i]:assign(j,state[i]^parity)
 propagate()
 for i in sorted(newids):
  if i not in state:assign(i,False);propagate()
 flips=sorted(source_flips|{i for i,value in state.items()if value})
 rem=set(removed);flipset=set(flips);faces=np.array([t[::-1]if(old['reverse']!=(i in flipset))else t for i,t in enumerate(f)if i not in rem]);u,first,inv=np.unique(np.round(p,8),axis=0,return_index=True,return_inverse=True);edges={};directed={}
 for t in inv[faces]:
  for k in range(3):
   a,b=map(int,t[[k,(k+1)%3]])
   if a==b:continue
   e=tuple(sorted([a,b]));rr=edges.setdefault(e,[0,0]);rr[0]+=1;rr[1]+=1 if a<b else -1;directed[e]=(a,b)
 bad=[(e,c)for e,c in edges.items()if c[0]!=1 and(c[0]%2 or c[1])];assert not bad,(node,bad[:10])
 unused={directed[e]for e,c in edges.items()if c[0]==1};extra=[];caps=[]
 while unused:
  start,nxt=next(iter(unused));unused.remove((start,nxt));trail=[start,nxt];locations={start:0,nxt:1}
  while True:
   if trail[-1]in trail[:-1]:
    j=trail[:-1].index(trail[-1]);loop=[int(first[x])for x in trail[j:-1]]
    if len(loop)>=3:
     centre=len(p)+len(extra);extra.append(p[loop].mean(0).tolist())
     for a,b in zip(loop,np.roll(loop,-1)):caps.extend([centre,int(b),int(a)])
    trail=trail[:j+1]
   candidates=[e for e in unused if e[0]==trail[-1]]
   if not candidates:break
   e=candidates[0];unused.remove(e);trail.append(e[1])
  assert len(trail)==1,(node,trail[-10:])
 verts=np.vstack([p,extra]);tri=np.vstack([faces,np.array(caps).reshape(-1,3)]);q=verts[tri];volume=float(np.einsum('ij,ij->i',q[:,0],np.cross(q[:,1],q[:,2])).sum()/6);assert volume>0,(node,volume)
 _,canonical=np.unique(np.round(verts,8),axis=0,return_inverse=True);balances={}
 for t in canonical[tri]:
  for k in range(3):
   a,b=map(int,t[[k,(k+1)%3]])
   if a==b:continue
   e=tuple(sorted([a,b]));c=balances.setdefault(e,[0,0]);c[0]+=1;c[1]+=1 if a<b else -1
 assert all(c>=2 and c%2==0 and bal==0 for c,bal in balances.values()),node
 new={'vertexCount':len(p),'extra':extra,'reverse':old['reverse'],'flips':flips,'removed':removed,'caps':caps,'faces':len(tri),'removedSeamFaces':len(removed),'volumeMm3':volume};d['entries'][sid]=new;reports.append({'node':node,'id':sid,'vertices':len(p),'faces':len(tri),'capLoops':len(extra),'volumeMm3':volume,'closedAndOriented':True});print(reports[-1],flush=True)
(W/'updated-dsa-surfaces.json').write_text(json.dumps(d));(W/'projection-refresh.json').write_text(json.dumps({'passed':True,'changes':reports},indent=2)+'\n')
