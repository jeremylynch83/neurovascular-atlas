from round_geometry import *
from vtk.util.numpy_support import vtk_to_numpy

def transport_collar(z,source_scale,parent_scale,steps=44,bow=(0,0,0),parent_exit=None):
 N='MMA posterior cavernous left';P='MMA cavernous left';old,oldf=mesh(N);w,g=mesh(P);plane=vtk.vtkPlane();plane.SetOrigin(0,0,z);plane.SetNormal(0,0,1);clip=vtk.vtkClipPolyData();clip.SetInputData(poly(old,oldf));clip.SetClipFunction(plane);clip.Update();o=clip.GetOutput();v=vtk_to_numpy(o.GetPoints().GetData()).astype('<f4').astype(float);f=vtk_to_numpy(o.GetPolys().GetData()).reshape(-1,4)[:,1:].astype(np.uint32);rr=rims(v,f);src=directed(v,f,min(rr,key=lambda r:abs(v[r,2].mean()-z)));pr=rims(w,g);dst0=directed(w,g,pr[1])[::-1];a=v[src];c0=a.mean(0);c1=w[dst0].mean(0)
 def normal(q):
  x=q-q.mean(0);n=np.cross(x,np.roll(x,-1,axis=0)).sum(0);return n/np.linalg.norm(n)
 n0=normal(a);n1=normal(w[dst0]);length=np.linalg.norm(c1-c0);T0=-n0*length*source_scale;exit=n1 if parent_exit is None else np.asarray(parent_exit,dtype=float)/np.linalg.norm(parent_exit);T1=-exit*length*parent_scale;ts=np.linspace(0,1,steps);centres=[];frames=[];previous=n0;rotation=Rotation.identity()
 for t in ts:
  c=(2*t**3-3*t*t+1)*c0+(t**3-2*t*t+t)*T0+(-2*t**3+3*t*t)*c1+(t**3-t*t)*T1;der=(6*t*t-6*t)*c0+(3*t*t-4*t+1)*T0+(-6*t*t+6*t)*c1+(3*t*t-2*t)*T1;c=c+16*t*t*(1-t)*(1-t)*np.array(bow);der=der+32*t*(1-t)*(1-2*t)*np.array(bow);n=-der/np.linalg.norm(der);blend=smooth((t-.70)/.30) if parent_exit is not None else 0.;n=(1-blend)*n+blend*n1;n/=np.linalg.norm(n);axis=np.cross(previous,n);s=np.linalg.norm(axis);cos=np.dot(previous,n)
  if s>1e-12:rotation=Rotation.from_rotvec(axis/s*np.arctan2(s,cos))*rotation
  elif cos<0:raise ValueError('Transport step reverses tangent')
  centres.append(c);frames.append(rotation);previous=n
 ka=np.r_[0,np.cumsum(np.linalg.norm(np.roll(a,-1,axis=0)-a,axis=1))];ka/=ka[-1];best=None
 for shift in range(len(dst0)):
  dst=np.roll(dst0,shift);b=w[dst];kb=np.r_[0,np.cumsum(np.linalg.norm(np.roll(b,-1,axis=0)-b,axis=1))];kb/=kb[-1];local=frames[-1].inv().apply(b-c1);sample=np.column_stack([np.interp(ka[:-1],kb,np.r_[local[:,k],local[0,k]])for k in range(3)]);error=np.sum((a-c0-sample)**2)
  if best is None or error<best[0]:best=(error,dst,sample,kb)
 dst=best[1];parent_params=best[3][:-1];source_shape=np.column_stack([np.interp(parent_params,ka,np.r_[a[:,k]-c0[k],a[0,k]-c0[k]])for k in range(3)]);target_shape=frames[-1].inv().apply(w[dst]-c1);q=v.copy();rings=[src];params=[ka[:-1]]
 for i,t in enumerate(ts[1:-1],1):
  radial=frames[i].apply((1-t)*source_shape+t*target_shape);ring=centres[i]+radial;ix=np.arange(len(q),len(q)+len(ring));q=np.vstack([q,ring]);rings.append(ix);params.append(parent_params)
 endpoint=np.arange(len(q),len(q)+len(dst));q=np.vstack([q,w[dst]]);rings.append(endpoint);params.append(best[3][:-1]);faces=f.tolist()
 for r,s,ra,sa in zip(rings[:-1],rings[1:],params[:-1],params[1:]):
  ii=jj=0
  while ii<len(r)or jj<len(s):
   an=ra[ii+1]if ii+1<len(r)else 1.;bn=sa[jj+1]if jj+1<len(s)else 1.
   if ii<len(r)and(jj==len(s)or an<=bn):faces.append([int(r[ii%len(r)]),int(s[jj%len(s)]),int(r[(ii+1)%len(r)])]);ii+=1
   else:faces.append([int(r[ii%len(r)]),int(s[jj%len(s)]),int(s[(jj+1)%len(s)])]);jj+=1
 p=q.astype('<f4').astype(float);ff=np.array(faces,np.uint32);details={'node':N,'parent':P,'clipZ':z,'sourceTangentScale':source_scale,'parentTangentScale':parent_scale,'steps':steps,'retainedClippedVertexCount':len(v),'bowMm':list(bow),'parentExitDirection':exit.tolist(),'sourceRim':endpoint.tolist(),'parentRim':dst.tolist(),'cutRim':src.tolist(),'centrelineFromCutToParent':[x.tolist()for x in centres],'nativeEndpointPlanesRespected':True,'parentExitOblique':parent_exit is not None,'framesAlignedWithPathExceptNativeEndpointBlend':True,'method':'Cubic Hermite centreline with parallel-transported cross-sections and exact native endpoint rings.'};return p,ff,details
