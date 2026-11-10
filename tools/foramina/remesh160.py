"""Rebuild a tubular proximal IMA wall with explicit side-port boundaries.
Constrained planar Delaunay packaging and VTK clipping are authoring-only operations.
"""
import numpy as np,vtk
from collections import defaultdict
from scipy.interpolate import CubicSpline
from scipy.ndimage import gaussian_filter1d
from scipy.optimize import isotonic_regression
from vtk.util.numpy_support import numpy_to_vtk,numpy_to_vtkIdTypeArray,vtk_to_numpy
vtk.vtkLogger.SetStderrVerbosity(vtk.vtkLogger.VERBOSITY_OFF)
def polydata(p,f):
 o=vtk.vtkPolyData();vp=vtk.vtkPoints();vp.SetData(numpy_to_vtk(p,deep=True));o.SetPoints(vp);c=vtk.vtkCellArray();c.SetCells(len(f),numpy_to_vtkIdTypeArray(np.c_[np.full(len(f),3),f].astype('int64').ravel(),deep=True));o.SetPolys(c);return o

def loops(p,f):
 edges,c=np.unique(np.sort(np.r_[f[:,[0,1]],f[:,[1,2]],f[:,[2,0]]],axis=1),axis=0,return_counts=True);assert not(c>2).any();adj=defaultdict(list)
 for a,b in edges[c==1]:adj[a].append(b);adj[b].append(a)
 assert all(len(v)==2 for v in adj.values());seen=set();out=[]
 for a in adj:
  if a in seen:continue
  loop=[a];prev=None;current=a
  while True:
   seen.add(current);nxt=next(v for v in adj[current]if v!=prev)
   if nxt==a:break
   assert nxt not in seen;loop.append(nxt);prev,current=current,nxt
  out.append(np.array(loop))
 return out

def area(x):return .5*np.sum(x[:,0]*np.roll(x[:,1],-1)-x[:,1]*np.roll(x[:,0],-1))

def rebuild(p,f,side,centre):
 sign=1 if side=='right'else -1;n=np.array([-.6*sign,.8,0]);basis=np.array([[.8*sign,.6,0],[0,0,1]]).T;radius=1.05;cut=-47.6;root=-72.9
 _,ix,remap=np.unique(np.round(p,6),axis=0,return_index=True,return_inverse=True);p=p[ix];f=remap[f];sourceLoops=loops(p,f)
 def frame(s):
  s=np.asarray(s);v=np.clip(s,-72.9,-46.5);c=centre(v);slope=centre(v,1);shape=np.broadcast_to(np.eye(2),(len(s),2,2)).copy()+np.einsum('ni,nj->nij',slope,slope);return c,np.linalg.cholesky(shape)*radius
 def chart(q):
  s=q@n;c,L=frame(s);u=np.linalg.solve(L,(q@basis-c)[...,None])[...,0];return np.c_[s,np.arctan2(u[:,1],u[:,0])*radius]
 def world(xy):
  s=xy[:,0];theta=xy[:,1]/radius;c,L=frame(s);return s[:,None]*n+(c+np.einsum('nij,nj->ni',L,np.c_[np.cos(theta),np.sin(theta)]))@basis.T
 rootLoop=min(sourceLoops,key=lambda ids:np.mean(p[ids]@n));assert np.mean(p[rootLoop]@n)<-71
 holes=[];controls=[];desired=[]
 for ids in sourceLoops:
  if ids is rootLoop or np.mean(p[ids]@n)>cut:continue
  q=p[ids];xy=chart(q);theta=np.unwrap(xy[:,1]/radius);xy[:,1]=theta*radius
  c=xy.mean(0);val,V=np.linalg.eigh(np.cov(xy.T)*2);r=np.sqrt(val)*.88;arc=np.r_[0,np.linalg.norm(np.diff(np.r_[xy,xy[:1]],axis=0),axis=1).cumsum()];angle=np.arctan2(*(((xy[0]-c)@V)/r)[::-1]);direction=(1 if area(xy)>0 else -1)*np.linalg.det(V);t=angle+direction*2*np.pi*arc[:-1]/arc[-1];regular=c+np.c_[np.cos(t)*r[0],np.sin(t)*r[1]]@V.T;holes.append((ids,regular))
 # Pick the periodic seam through a root vertex, clear of every side port.
 rootQ=p[rootLoop];rootXY=chart(rootQ);arc=np.r_[0,np.linalg.norm(np.diff(np.r_[rootQ,rootQ[:1]],axis=0),axis=1).cumsum()];theta0=rootXY[0,1]/radius
 if np.unwrap(rootXY[:,1]/radius)[-1]<theta0:rootLoop=rootLoop[::-1];rootQ=p[rootLoop];rootXY=chart(rootQ);arc=np.r_[0,np.linalg.norm(np.diff(np.r_[rootQ,rootQ[:1]],axis=0),axis=1).cumsum()];theta0=rootXY[0,1]/radius
 rootTheta=theta0+2*np.pi*arc[:-1]/arc[-1]
 def clearance(theta):
  return min(np.min(abs(np.angle(np.exp(1j*(xy[:,1]/radius-theta)))))for _,xy in holes)
 seam=float(max(rootTheta,key=clearance));assert clearance(seam)>.025
 rootTheta=seam+np.mod(rootTheta-seam,2*np.pi);order=np.argsort(rootTheta);rootLoop=rootLoop[order];rootTheta=rootTheta[order];rootTheta[0]=seam
 rootChart=np.c_[np.full(len(rootLoop),root),rootTheta*radius];rootWorld=world(rootChart);controls.extend(p[rootLoop]);desired.extend(rootWorld)
 # Retain the entire distal wall and create an exact matching cut interface.
 plane=vtk.vtkPlane();plane.SetOrigin(cut*n);plane.SetNormal(n);clip=vtk.vtkClipPolyData();clip.SetInputData(polydata(p,f));clip.SetClipFunction(plane);clip.Update();clipped=clip.GetOutput();dp=vtk_to_numpy(clipped.GetPoints().GetData()).copy();df=vtk_to_numpy(clipped.GetPolys().GetData()).reshape(-1,4)[:,1:].astype(int)
 _,di,dr=np.unique(np.round(dp,7),axis=0,return_index=True,return_inverse=True);dp=dp[di];df=dr[df]
 cutLoop=min(loops(dp,df),key=lambda ids:abs(np.mean(dp[ids]@n)-cut));assert np.max(abs(dp[cutLoop]@n-cut))<1e-5
 cutXY=chart(dp[cutLoop]);angles=seam+np.mod(cutXY[:,1]/radius-seam,2*np.pi);order=np.argsort(angles);cutLoop=cutLoop[order];angles=angles[order]
 # Split the one native cut edge that the chosen periodic seam crosses.
 a,b=int(cutLoop[-1]),int(cutLoop[0]);a0=angles[-1];b0=angles[0]+2*np.pi;t=(seam+2*np.pi-a0)/(b0-a0);point=dp[a]*(1-t)+dp[b]*t;extra=len(dp);dp=np.r_[dp,point[None]];newfaces=[]
 for tri in df:
  if a in tri and b in tri:
   for k in range(3):
    if {int(tri[k]),int(tri[(k+1)%3])}=={a,b}:
     aa,bb,cc=tri[k],tri[(k+1)%3],tri[(k+2)%3];newfaces.extend([[aa,extra,cc],[extra,bb,cc]]);break
  else:newfaces.append(tri)
 df=np.array(newfaces,int);cutLoop=np.r_[extra,cutLoop];angles=np.r_[seam,angles];cutChart=np.c_[np.full(len(cutLoop),cut),angles*radius];cutWorld=dp[cutLoop]
 # Periodic interpolation matches the native cut ring exactly, including its
 # slight residual asymmetry. The last 2 mm blend into the retained distal wall.
 periodicAngles=np.r_[angles,seam+2*np.pi];periodicPoints=np.r_[cutWorld,cutWorld[:1]];cutSpline=CubicSpline(periodicAngles,periodicPoints,bc_type='periodic')
 def surface(xy):
  q=world(xy);s=xy[:,0];w=np.clip((s-(cut-2))/2,0,1);w=w*w*(3-2*w);theta=seam+np.mod(xy[:,1]/radius-seam,2*np.pi);idealAtCut=world(np.c_[np.full(len(s),cut),xy[:,1]]);return q+w[:,None]*(cutSpline(theta)-idealAtCut)
 steps=np.linspace(root,cut,90);bottom=np.c_[steps,np.full(len(steps),seam*radius)];top=np.c_[steps[::-1],np.full(len(steps),(seam+2*np.pi)*radius)];outer=np.r_[bottom,cutChart[1:],[[cut,(seam+2*np.pi)*radius]],top[1:],rootChart[:0:-1]]
 contours=[outer];portMaps=[]
 for ids,xy in holes:
  theta=xy[:,1]/radius;offset=round((seam+np.pi-np.mean(theta))/(2*np.pi))*2*np.pi;xy=xy.copy();xy[:,1]+=offset*radius
  assert xy[:,1].min()>seam*radius and xy[:,1].max()<(seam+2*np.pi)*radius
  if area(xy)>0:xy=xy[::-1];ids=ids[::-1]
  contours.append(xy);portMaps.append((ids,xy));controls.extend(p[ids]);desired.extend(surface(xy))
 from scipy.spatial import Delaunay,cKDTree
 points=np.concatenate(contours);segments=[];constraints=[];offset=0
 for contour in contours:
  ids=np.arange(offset,offset+len(contour));constraints.extend(np.c_[ids,np.roll(ids,-1)]);segments.extend(np.c_[contour,np.roll(contour,-1,axis=0)]);offset+=len(contour)
 segments=np.array(segments);constraints=np.array(constraints)
 def inside(poly,query):
  result=np.zeros(len(query),bool);x,y=query.T
  for a,b in zip(poly,np.roll(poly,-1,axis=0)):
   if a[1]==b[1]:continue
   result^=((a[1]>y)!=(b[1]>y))&(x<(b[0]-a[0])*(y-a[1])/(b[1]-a[1])+a[0])
  return result
 xx,yy=np.meshgrid(np.arange(root+.11,cut,.22),np.arange(seam*radius+.11,(seam+2*np.pi)*radius,.22));grid=np.c_[xx.ravel(),yy.ravel()];keep=inside(outer,grid)
 for hole in contours[1:]:keep&=~inside(hole,grid)
 grid=grid[keep];tree=cKDTree(grid);keep=np.ones(len(grid),bool)
 # Keep boundary segments Gabriel edges, so unconstrained Delaunay recovers
 # every explicit port edge. The assertion below verifies this, not assumes it.
 for edge in segments:
  mid=(edge[:2]+edge[2:])/2;r=np.linalg.norm(edge[:2]-edge[2:])/2+1e-7;keep[tree.query_ball_point(mid,r)]=False
 xy=np.r_[points,grid[keep]];tf=Delaunay(xy).simplices
 def cross(a,b):return a[0]*b[1]-a[1]*b[0]
 def intersects(a,b,c,d):
  return cross(b-a,c-a)*cross(b-a,d-a)<-1e-20 and cross(d-c,a-c)*cross(d-c,b-c)<-1e-20
 protected={tuple(sorted(e))for e in constraints}
 existing={tuple(e)for e in np.unique(np.sort(np.r_[tf[:,[0,1]],tf[:,[1,2]],tf[:,[2,0]]],axis=1),axis=0)}
 for aa,bb in constraints:
  if tuple(sorted((int(aa),int(bb))))in existing:continue
  target=tuple(sorted((int(aa),int(bb))))
  for iteration in range(100):
   edgeFaces={}
   for i,tri in enumerate(tf):
    for a,b in zip(tri,np.roll(tri,-1)):edgeFaces.setdefault(tuple(sorted((int(a),int(b)))),[]).append(i)
   if target in edgeFaces:break
   recovered=False
   for (a,b),faces in edgeFaces.items():
    if len(faces)!=2 or(a,b)in protected or not intersects(xy[aa],xy[bb],xy[a],xy[b]):continue
    i,j=faces;c=next(v for v in tf[i]if v not in(a,b));d=next(v for v in tf[j]if v not in(a,b))
    if not intersects(xy[a],xy[b],xy[c],xy[d])or intersects(xy[aa],xy[bb],xy[c],xy[d]):continue
    tf[i]=[c,d,a];tf[j]=[d,c,b];recovered=True;break
   assert recovered,('Cannot recover constrained port edge',target)
  else:raise AssertionError('Port edge recovery did not converge')
 middle=xy[tf].mean(1);keep=inside(outer,middle)
 for hole in contours[1:]:keep&=~inside(hole,middle)
 tf=tf[keep];turn=(xy[tf[:,1],0]-xy[tf[:,0],0])*(xy[tf[:,2],1]-xy[tf[:,0],1])-(xy[tf[:,1],1]-xy[tf[:,0],1])*(xy[tf[:,2],0]-xy[tf[:,0],0]);tf[turn<0]=tf[turn<0,::-1];edge1=xy[tf[:,1]]-xy[tf[:,0]];edge2=xy[tf[:,2]]-xy[tf[:,0]];actual=np.sum(abs(edge1[:,0]*edge2[:,1]-edge1[:,1]*edge2[:,0]))*.5;expected=abs(area(outer))-sum(abs(area(c))for c in contours[1:]);assert abs(actual-expected)<1e-6*expected,(actual,expected)
 tp=surface(xy);radial=tp-(xy[:,0,None]*n+centre(np.clip(xy[:,0],-72.9,-46.5))@basis.T);normal=np.cross(tp[tf[:,1]]-tp[tf[:,0]],tp[tf[:,2]]-tp[tf[:,0]]);dot=(normal*radial[tf].mean(1)).sum(1)
 if np.median(dot)<0:tf=tf[:,::-1]
 # Make shared interfaces exact, independent of interpolation roundoff.
 for contour,coords in [(rootChart,rootWorld),(cutChart,cutWorld)]:
  for a,b in zip(contour,coords):
   d=np.linalg.norm(xy-a,axis=1);tp[d<1e-7]=b
   aa=a.copy();aa[1]+=2*np.pi*radius;d=np.linalg.norm(xy-aa,axis=1);tp[d<1e-7]=b
 qp=np.r_[dp,tp];qf=np.r_[df,tf+len(dp)];_,qi,qr=np.unique(np.round(qp,6),axis=0,return_index=True,return_inverse=True);qp=qp[qi];qf=qr[qf];assert not((qf[:,0]==qf[:,1])|(qf[:,0]==qf[:,2])|(qf[:,1]==qf[:,2])).any()
 outputLoops=loops(qp,qf);assert len(outputLoops)==len(sourceLoops),(len(outputLoops),len(sourceLoops))
 return qp,qf,np.array(controls),np.array(desired),{'retainedDistalCutS':cut,'rootS':root,'sidePortsRebuilt':len(holes),'sourceVertices':len(p),'vertices':len(qp),'faces':len(qf),'boundaryLoops':len(outputLoops),'triangulatedAreaError':float(abs(actual-expected))}
