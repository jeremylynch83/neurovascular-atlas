"""Monotone-height external temporal venous course, obstacle constrained."""
from common import *
from scipy.ndimage import gaussian_filter1d
from scipy.interpolate import CubicSpline
vtk.vtkLogger.SetStderrVerbosity(vtk.vtkLogger.VERBOSITY_OFF)
paths={}
for side,sign in [('right',1),('left',-1)]:
 vein='vein.superficial_temporal.'+side;artery='Superficial temporal'+(' left' if side=='left' else '');v,f=load(vein);av,af=load(artery);zs=np.arange(39.,89.,1.);xs=np.arange(42.,83.,1.);ys=np.arange(-70.,-18.,1.);grid=np.meshgrid(xs,ys,zs,indexing='ij');pts=np.c_[tuple(g.ravel() for g in grid)];world=pts.copy();world[:,0]*=sign;shape=grid[0].shape;clear=np.full(len(pts),100.);radii=[];vc=[];target=[]
 for z in zs:
  p=section(v,f,2,z);c=(p.min(0)+p.max(0))/2;vc.append(c);radii.append(np.max(np.linalg.norm(p[:,:2]-c[:2],axis=1)))
  p=section(av,af,2,min(z,82));c=(p.min(0)+p.max(0))/2;target.append([sign*c[0]+4.,c[1]-3.])
 for row in META:
  n=row['name']
  if row['file'] not in ['craniofacial.glb','complete-circulation.glb','complete-anastomoses.glb']:continue
  if row['file']=='craniofacial.glb' and not n.startswith('bone.'):continue
  a,b=load(n)
  if np.any(a.max(0)<world.min(0)-3)|np.any(a.min(0)>world.max(0)+3):continue
  ip=vtk.vtkImplicitPolyDataDistance();ip.SetInput(poly(a,b));values=np.array([ip.EvaluateFunction(p) for p in world]);clear=np.minimum(clear,values if n.startswith('bone.') else np.abs(values))
 clear=clear.reshape(shape);r=np.maximum(np.array(radii),1.7)+.35;free=clear>r[None,None,:];vc=np.array(vc);target=np.array(target)
 X,Y=np.meshgrid(xs,ys,indexing='ij');orig=vc.copy();orig[:,0]*=sign
 # Blend anatomical attraction to exact original lower and upper drainage courses.
 weight=smooth((zs-39)/10)*smooth((88-zs)/10);target=orig[:,:2]+weight[:,None]*(target-orig[:,:2])
 penalty=((X[:,:,None]-target[None,None,:,0])**2+(Y[:,:,None]-target[None,None,:,1])**2)*.035+1/np.maximum(clear,.1)**2
 begin=np.unravel_index(np.argmin(np.where(free[:,:,0],(X-orig[0,0])**2+(Y-orig[0,1])**2,np.inf)),X.shape);end=np.unravel_index(np.argmin(np.where(free[:,:,-1],(X-orig[-1,0])**2+(Y-orig[-1,1])**2,np.inf)),X.shape)
 cost=np.full(X.shape,np.inf);cost[begin]=0;parents=[];deltas=[(i,j) for i in [-2,-1,0,1,2] for j in [-2,-1,0,1,2] if i*i+j*j<=5]
 for k in range(1,len(zs)):
  new=np.full(X.shape,np.inf);parent=np.full(X.shape+(2,),-1,int)
  for di,dj in deltas:
   ss=(slice(max(0,-di),min(len(xs),len(xs)-di)),slice(max(0,-dj),min(len(ys),len(ys)-dj)));tt=(slice(max(0,di),min(len(xs),len(xs)+di)),slice(max(0,dj),min(len(ys),len(ys)+dj)));candidate=cost[ss]+.1*(di*di+dj*dj)+penalty[tt+(k,)];ok=(candidate<new[tt])&free[tt+(k,)];new[tt][ok]=candidate[ok];ii,jj=np.indices(cost[ss].shape);origin=np.c_[ii[ok]+max(0,-di),jj[ok]+max(0,-dj)];parent[tt][ok]=origin
  assert np.isfinite(new).any(),(side,k,'blocked temporal corridor');cost=new;parents.append(parent)
 assert np.isfinite(cost[end]),(side,'endpoint unreachable')
 indices=[end]
 for p in parents[::-1]:indices.append(tuple(p[indices[-1]]))
 indices=indices[::-1];q=np.array([[xs[i],ys[j],z] for (i,j),z in zip(indices,zs)]);q[:,0]*=sign;q=gaussian_filter1d(q,.8,axis=0);q[:,2]=zs;q[0]=vc[0];q[-1]=vc[-1]
 paths[side]=dict(z=zs.tolist(),centres=q.tolist(),baselineCentres=vc.tolist(),radiusBoundsMm=r.tolist(),method='Monotone z dynamic path through bone/artery wall clearance grid, with arterial attraction and fixed native drainage endpoints.')
 print(side, 'max delta',np.linalg.norm(q-vc,axis=1).max(), 'radius range',r.min(),r.max(),flush=True)
(WORK/'temporal-paths.json').write_text(json.dumps(paths,indent=2)+'\n')
