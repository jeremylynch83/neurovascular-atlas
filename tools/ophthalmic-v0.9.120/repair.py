from probe import *
from geometry import edge_table,cycles
from branch import bridge
from scipy.interpolate import CubicSpline
from vtk.util.numpy_support import vtk_to_numpy
O=W/'candidate';O.mkdir(exist_ok=True)
def arrays(p):return vtk_to_numpy(p.GetPoints().GetData()).copy(),vtk_to_numpy(p.GetPolys().GetData()).reshape(-1,4)[:,1:].copy()
def smooth(t):
 t=np.clip(t,0,1);return t*t*(3-2*t)
def combine(parts):
 pp=[];ff=[];off=0
 for v,f in parts:pp.append(v);ff.append(f+off);off+=len(v)
 p=np.vstack(pp).astype('<f4');f=np.vstack(ff);u,inv=np.unique(p,axis=0,return_inverse=True);f=inv[f];used=np.unique(f);mp=np.full(len(u),-1);mp[used]=np.arange(len(used))
 return u[used],mp[f].astype('<u4')
def hole(v,f,query,outward,radius=.9):
 outward=np.array(outward,float);outward/=np.linalg.norm(outward)
 _,q=distance(locator(v,f),query);centre=np.array(q)+.25*outward
 scalar=np.square(v-centre).sum(1)-radius**2
 local=np.any(scalar[f]<0,axis=1)
 pd=poly(v,f[local]);pd.GetPointData().SetScalars(numpy_to_vtk(scalar,deep=True));clip=vtk.vtkClipPolyData();clip.SetInputData(pd);clip.SetValue(0);clip.Update();p,g=arrays(clip.GetOutput());p=p.astype('<f4');t=p[g].astype(float);g=g[np.linalg.norm(np.cross(t[:,1]-t[:,0],t[:,2]-t[:,0]),axis=1)>1e-12]
 p,g=combine([(v,f[~local]),(p,g)])
 u,e,c,b,d,_=edge_table(p,g);loops=cycles(d[c==1]);ring=min(loops,key=lambda x:np.linalg.norm(u[x].mean(0)-centre));a=u[ring]
 assert np.linalg.norm(a.mean(0)-centre)<radius
 return p,g,a,{'query':query,'cutSphereCentre':centre.tolist(),'cutSphereRadiusMm':radius,'rimCentre':a.mean(0).tolist(),'rimVertices':len(a)}
results=[]
for side,sign in [('right',1),('left',-1)]:
 iov='vein.inferior_ophthalmic.'+side;sov='vein.superior_ophthalmic.'+side
 v,f=scene.mesh(iov);v=np.array(v,float);f=np.array(f);sv,sf=scene.mesh(sov);sv=np.array(sv,float);sf=np.array(sf)
 baseline=v.copy()
 if side=='left':
  # Bounded superior displacement, preserving the anterior orbit and the
  # entire native pterygoid rim. Remove the sharp dip without shrinking calibre.
  y=v[:,1];weight=np.exp(-np.square((y+15.8)/1.25))*smooth((y+18)/.6)*(1-smooth((y+13.6)/.6))
  correction=.8*weight
  v[:,2]+=correction
  shared=set(map(tuple,scene.mesh('vein.pterygoid_plexus.left')[0]));locked=np.array([tuple(q)in shared for q in baseline]);v[locked]=baseline[locked]
 x=lambda a: a if side=='right' else -a+1.3
 p,g,a,ha=hole(v,f,[x(29.5),-8,47.5],[0,-.35,1],.95)
 # Enter the inferior/anterior wall of the SOV within the orbital apex,
 # anterior to its already fitted cavernous collar.
 q,h,b,hb=hole(sv,sf,[x(23),-20,69.5],[.1,.8,-.6],.85)
 via=np.array([[x(29),-10,48.5],[x(29),-14,54],[x(27),-16,60],[x(25),-17,65],[x(24),-18.5,68]],float)
 bv,bf,br=bridge(a,b[::-1],via=via,steps=92)
 iv,iff=combine([(p,g),(bv,bf)])
 # The shared distal ring is one physical surface boundary on each label.
 vv,ff=combine([(q,h)])
 for n,pp,gg in [(iov,iv,iff),(sov,vv,ff)]:
  pp.tofile(O/(n+'.positions.bin'));gg.tofile(O/(n+'.indices.bin'))
 bv.tofile(O/(iov+'.branch.positions.bin'));bf.tofile(O/(iov+'.branch.indices.bin'))
 result={'side':side,'iov':iov,'sov':sov,'iovHole':ha,'sovHole':hb,'branch':br,'leftSmoothingMaximumMm':float(np.linalg.norm(v-baseline,axis=1).max()),'vertices':{iov:len(iv),sov:len(vv)},'triangles':{iov:len(iff),sov:len(ff)}}
 print(json.dumps({k:v for k,v in result.items()if k!='branch'}),flush=True);results.append(result)
(O/'authoring.json').write_text(json.dumps({'release':'0.9.120','results':results},indent=2))
