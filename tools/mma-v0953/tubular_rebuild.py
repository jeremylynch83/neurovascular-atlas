"""Fresh tapered implicit shafts and bifurcations, exact native receiver collars."""
from geometry import *
from scipy.ndimage import gaussian_filter,gaussian_filter1d
from scipy.spatial.distance import cdist
vtk.vtkLogger.SetStderrVerbosity(vtk.vtkLogger.VERBOSITY_OFF)
r=json.loads((OUT/'revision.json').read_text());guides=json.loads((WORK/'mma-guides.json').read_text());results=[]
x=np.load(WORK/'coordinate-fields.npz');cc=x['c'];coeff=x['coeff'];sigma=9.
def arteryfield(v):return np.exp(-cdist(v,cc)**2/(2*sigma*sigma))@coeff*smooth((v[:,2]-43)/10)[:,None]
for side in ['right','left']:
 suffix=' left' if side=='left' else '';names=[base+suffix for base in ['Middle meningeal','MMA frontal','MMA frontal anterior division','MMA frontal posterior division']];vv=[];ff=[];owners=[]
 for j,n in enumerate(names):
  v,f=load(n);ff.append(f+sum(len(a) for a in vv));vv.append(v);owners.extend([j]*len(v))
 old=np.concatenate(vv);faces=np.concatenate(ff);owners=np.array(owners);uv,first,inv=np.unique(old,axis=0,return_index=True,return_inverse=True);uf=inv[faces];oldloops=rings(uv,uf);ports=[]
 for loop in oldloops:
  ring=uv[loop];node=names[int(np.bincount(owners[first[loop]]).argmax())];ports.append(dict(owner=node,ring=ring+arteryfield(ring),original=ring,centre=(ring+arteryfield(ring)).mean(0)))
 curves=[];radii=[]
 for j,n in enumerate(names):
  if j==0:
   g=next(g for g in guides if g['side']==side and 'node' not in g);q=np.array(g['points']);rad=np.array(g['radiusMm']);mask=np.array(g['oldPoints'])[:,2]<78.4;q=q[mask];rad=rad[mask]
  elif j==1:
   g=next(g for g in guides if g['side']==side and 'node' not in g);q=np.array(g['points']);rad=np.array(g['radiusMm']);mask=np.array(g['oldPoints'])[:,2]>77.9;q=q[mask];rad=rad[mask]
  else:
   g=next(g for g in guides if g.get('node')==n);q=np.array(g['points']);rad=np.array(g['radiusMm'])
  # Retain labelled peripheral root collars through independently guided stems.
  q=gaussian_filter1d(q,2,axis=0);rad=np.clip(rad,.24 if j else .42,.50 if j else .63)
  curves.append(q);radii.append(rad)
 # Fill guide gaps at native branch points by a short shaft of parent calibre.
 connectors=[]
 for j in range(1,len(curves)):
  a=curves[j];targets=[curves[0],curves[1]] if j>1 else [curves[0]];tt=np.concatenate(targets);d,k=cKDTree(tt).query(a[[0,-1]]);end=int(np.argmin(d));source=a[0 if end==0 else -1];dest=tt[k[end]];connectors.append((np.linspace(source,dest,max(8,int(np.linalg.norm(source-dest)/.2))),np.full(max(8,int(np.linalg.norm(source-dest)/.2)),min(.44,radii[j][0 if end==0 else -1]))))
 for port in ports:
  j=names.index(port['owner']);d,k=cKDTree(curves[j]).query(port['centre']);dest=curves[j][k];dist=np.linalg.norm(dest-port['centre']);rad=min(.65,max(.20,np.median(np.linalg.norm(port['ring']-port['centre'],axis=1))));count=max(8,int(dist/.18));connectors.append((np.linspace(port['centre'],dest,count),np.full(count,rad)))
 allq=np.concatenate(curves+[a for a,b in connectors]);lo=allq.min(0)-1.2;hi=allq.max(0)+1.2;spacing=.16;dims=np.ceil((hi-lo)/spacing).astype(int)+1;sp=(hi-lo)/(dims-1);field=np.full(dims,10.,np.float32);print(side,'grid',dims.tolist(),'ports',len(ports),flush=True)
 for q,rad in list(zip(curves,radii))+connectors:
  for a,b,ra,rb in zip(q[:-1],q[1:],rad[:-1],rad[1:]):
   pad=max(ra,rb)+.45;low=np.maximum(np.floor((np.minimum(a,b)-pad-lo)/sp).astype(int),0);high=np.minimum(np.ceil((np.maximum(a,b)+pad-lo)/sp).astype(int)+1,dims);sl=tuple(slice(int(x),int(y)) for x,y in zip(low,high));p=np.stack(np.meshgrid(*[lo[k]+np.arange(low[k],high[k])*sp[k] for k in range(3)],indexing='ij'),axis=-1);ab=b-a;t=np.clip(np.sum((p-a)*ab,axis=-1)/max(np.dot(ab,ab),1e-12),0,1);sdf=np.linalg.norm(p-a-t[...,None]*ab,axis=-1)-(ra*(1-t)+rb*t);field[sl]=np.minimum(field[sl],sdf)
 field=gaussian_filter(field,.65);v,f=iso(field,lo,sp);del field
 # Graft each opening to the identical native polygon, avoiding overlap caps.
 for port in ports:
  ring=port['ring'];centre=port['centre'];rad=np.median(np.linalg.norm(ring-centre,axis=1));cut=max(.36,rad*1.5);v,f=clip(v,f,np.linalg.norm(v-centre,axis=1)-cut);loop=min(rings(v,f),key=lambda a:np.linalg.norm(v[a].mean(0)-centre));o=len(v);v=np.concatenate([v,ring]);f=np.concatenate([f,bridge(v,loop,np.arange(o,len(v)))])
 # Assign the common exterior only once. Shared patch edges use exact coordinates.
 scores=[];centres=v[f].mean(1)
 for q,rad in zip(curves,radii):d,k=cKDTree(q).query(centres);scores.append(d-rad[k])
 owner=np.argmin(scores,axis=0)
 # Each native port is assigned to its original parent label.
 for port in ports:
  mask=np.linalg.norm(centres-port['centre'],axis=1)<1.6;owner[mask]=names.index(port['owner'])
 nn=normals(v,f)
 for j,n in enumerate(names):
  fs=f[owner==j];ids,inv=np.unique(fs,return_inverse=True);write(n,v[ids],inv.reshape(-1,3));nn[ids].astype('<f4').tofile(OUT/(n+'.normals.bin'));row=next(z for z in r['changed'] if z['node']==n);row.update(vertices=len(ids),triangles=len(fs),topology='labelled exterior of fresh tapered implicit tube tree',field='fresh tubular reconstruction')
 np.savez(OUT/('mma-network-'+side+'.npz'),v=v.astype('<f4'),f=f.astype('<u4'))
 for j,n in enumerate(names):np.savez(WORK/(n+'.rebuilt-curve.npz'),q=curves[j],r=radii[j])
 results.append(dict(side=side,ports=len(ports),vertices=len(v),triangles=len(f),spacingMm=spacing));print('Rebuilt',side,flush=True)
r['tubularRebuild']=results;r['method']+='; fresh implicit trunk/frontal tube tree with exact native collar grafts';(OUT/'revision.json').write_text(json.dumps(r,indent=2)+'\n')
