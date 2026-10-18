from loft import *
from vtk.util.numpy_support import vtk_to_numpy
from scipy.spatial.transform import Rotation
def round_collar(z,scale,side="right",stem="ACA falcine branch",parentstem="ACA A5",inside=False):
 n=stem+' '+side;parent=parentstem+' '+side;original,oldf=mesh(n);w,g=mesh(parent)
 plane=vtk.vtkPlane();plane.SetOrigin(0,0,z);plane.SetNormal(0,0,1);clip=vtk.vtkClipPolyData();clip.SetInputData(poly(original,oldf));clip.SetClipFunction(plane);clip.SetInsideOut(inside);clip.Update();o=clip.GetOutput();v=vtk_to_numpy(o.GetPoints().GetData()).astype('<f4').astype(float);f=vtk_to_numpy(o.GetPolys().GetData()).reshape(-1,4)[:,1:].astype(np.uint32)
 rs=rims(v,f);rp=rims(w,g);i=min(range(len(rs)),key=lambda i:abs(v[rs[i],2].mean()-z));original_rims=rims(original,oldf);oi,j=min(((oi,j)for oi in range(len(original_rims))for j in range(len(rp))),key=lambda ij:np.linalg.norm(original[original_rims[ij[0]]].mean(0)-w[rp[ij[1]]].mean(0)))
 src=directed(v,f,rs[i]);dst0=directed(w,g,rp[j])[::-1];a=v[src];c0=a.mean(0);u=a-c0
 def normal(q):
  vv=np.cross(q,np.roll(q,-1,axis=0)).sum(0);return vv/np.linalg.norm(vv)
 n0=normal(u);b0=w[dst0];c1=b0.mean(0);n1=normal(b0-c1);axis=np.cross(n0,n1);sin=np.linalg.norm(axis);angle=np.arctan2(sin,np.dot(n0,n1));axis/=max(sin,1e-12);R=Rotation.from_rotvec(axis*angle)
 ka=np.r_[0,np.cumsum(np.linalg.norm(np.roll(a,-1,axis=0)-a,axis=1))];ka/=ka[-1];best=None
 for k in range(len(dst0)):
  dst=np.roll(dst0,k);b=w[dst];kb=np.r_[0,np.cumsum(np.linalg.norm(np.roll(b,-1,axis=0)-b,axis=1))];kb/=kb[-1];local=R.inv().apply(b-c1)
  sample=np.column_stack([np.interp(ka[:-1],kb,np.r_[local[:,q],local[0,q]])for q in range(3)])
  err=np.sum((u-sample)**2)
  if best is None or err<best[0]:best=(err,dst,sample,kb)
 dst=best[1];sample=best[2];delta=c1-c0;length=np.linalg.norm(delta);T0=n0*np.sign(np.dot(n0,delta))*length*scale;T1=n1*np.sign(np.dot(n1,delta))*length*scale
 q=v.copy();ff=f.tolist();rings=[src];params=[ka[:-1]]
 for t in np.linspace(0,1,18)[1:-1]:
  centre=(2*t**3-3*t*t+1)*c0+(t**3-2*t*t+t)*T0+(-2*t**3+3*t*t)*c1+(t**3-t*t)*T1
  radial=Rotation.from_rotvec(axis*angle*t).apply((1-t)*u+t*sample);ring=centre+radial;ix=np.arange(len(q),len(q)+len(ring));q=np.vstack([q,ring]);rings.append(ix);params.append(ka[:-1])
 endpoint=np.arange(len(q),len(q)+len(dst));q=np.vstack([q,w[dst]]);rings.append(endpoint);params.append(best[3][:-1])
 for r,s,ra,sa in zip(rings[:-1],rings[1:],params[:-1],params[1:]):
  ii=jj=0
  while ii<len(r)or jj<len(s):
   an=ra[ii+1]if ii+1<len(r)else 1.;bn=sa[jj+1]if jj+1<len(s)else 1.
   if ii<len(r)and(jj==len(s)or an<=bn):ff.append([int(r[ii%len(r)]),int(s[jj%len(s)]),int(r[(ii+1)%len(r)])]);ii+=1
   else:ff.append([int(r[ii%len(r)]),int(s[jj%len(s)]),int(s[(jj+1)%len(s)])]);jj+=1
 p=q.astype('<f4').astype(float);h=np.array(ff,dtype=np.uint32);d={'sourceRim':endpoint.tolist(),'parentRim':dst.tolist(),'originalVertexCount':len(original),'originalPrefixRetained':False,'clipZ':z,'retainBelow':inside,'method':'Hermite centreline and rotating cross-sections between native parent rim and proximal falcine cut; original distal interfaces fixed','transitionLengthMm':float(length),'tangentScale':scale,'rimShapeRmsMismatchMm':float(np.sqrt(best[0]/len(src))),'maxShiftMm':0.,'fixedDistalRimVertices':int(np.sum(original[:,2]<=z if inside else original[:,2]>=z)),'distalRimExact':True}
 return q,h,p,d
