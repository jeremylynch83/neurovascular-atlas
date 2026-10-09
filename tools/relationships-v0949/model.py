"""Reference-course corrections from the v0.9.48 relationship audit.
All original topology is retained. Each change is a smooth coordinate shear;
shared labelled collars receive the same transformation.
"""
from common import *
from scipy.interpolate import PchipInterpolator
from scipy.ndimage import gaussian_filter1d
vtk.vtkLogger.SetStderrVerbosity(vtk.vtkLogger.VERBOSITY_OFF)
changed={};groups=[];fields=[]
def apply(names,fn,reason):
 affected=[]
 for name in names:
  if name not in FILES:continue
  v,f=load(name);v0=changed.get(name,(v,f))[0];after=fn(v0)
  if np.max(np.abs(after-v0))>1e-7:changed[name]=(after,f);affected.append(name)
 groups.append(dict(reason=reason,nodes=affected));fields.append((names,fn))
def axial_centre(name,z):
 v,f=load(name);pts=section(v,f,2,z);return (pts.min(0)+pts.max(0))/2 if len(pts) else None
def companion_fn(art,vein,dx,dy,low,high,taper=12):
 vv,_=load(vein);zs=np.arange(low,high+.01,1.);delta=[]
 for z in zs:
  a=axial_centre(art,z);b=axial_centre(vein,z);delta.append([a[0]+dx-b[0],a[1]+dy-b[1]])
 delta=gaussian_filter1d(np.array(delta),2,axis=0);interp=PchipInterpolator(zs,delta)
 def fn(v):
  q=v.copy();z=v[:,2];w=smooth((z-low)/taper)*smooth((high-z)/taper);q[:,:2]+=interp(np.clip(z,low,high))*w[:,None];return q
 return fn
for side,sign in [('right',1),('left',-1)]:
 suffix='' if side=='right' else ' left'
 # Bring the dominant venous channel around, rather than through, V2.
 art='Vertebral V2 '+side;vein='vein.vertebral.'+side;zs=np.arange(-84,0,1.);ac=[];vc=[]
 for z in zs:ac.append(axial_centre(art,z));vc.append(axial_centre(vein,z))
 ac=np.array(ac);vc=np.array(vc);ai=PchipInterpolator(zs,gaussian_filter1d(ac,2,axis=0));vi=PchipInterpolator(zs,gaussian_filter1d(vc,2,axis=0))
 def vertebral(v):
  z=v[:,2];zz=np.clip(z,zs[0],zs[-1]);w=smooth((z+84)/12)*smooth((-12-z)/12);a=ai(zz);b=vi(zz);delta=b[:,:2]-a[:,:2];angle=np.arctan2(delta[:,1],sign*delta[:,0]);radius=np.linalg.norm(delta,axis=1);theta=angle+w*(np.arctan2(3.,4.6)-angle);r=radius+w*(5.5-radius);target=np.c_[sign*r*np.cos(theta),r*np.sin(theta)];q=v.copy();q[:,:2]+=(a[:,:2]+target-b[:,:2]);q[z<=-84]=v[z<=-84];q[z>=-12]=v[z>=-12];return q
 apply(['vein.vertebral.'+side,'vein.suboccipital_plexus.'+side],vertebral,'Vertebral venous channel follows V2 ventrolaterally with curved transitions around its wall. Cervical bone is unavailable.')
 # Facial vein: local posterior and lateral course in the mandibular/cheek region.
 def facial(v):
  q=v.copy();z=v[:,2];w=smooth((z+16)/20)*smooth((32-z)/16)*smooth((v[:,1]+10)/30);q[:,0]+=sign*8*w;q[:,1]-=15*w;return q
 apply(['vein.facial.'+side,'vein.deep_facial.'+side,'vein.angular.'+side],facial,'Facial vein lies posterolateral to the tortuous artery in the lower cheek, with smooth fixed-end transitions.')
 def facial_crossing(v):
  q=v.copy();y=v[:,1];z=v[:,2];w=smooth(y/8)*smooth((19-y)/6)*smooth((z-18)/3)*smooth((28-z)/3);q[:,0]+=sign*w;q[:,1]-=3*w;return q
 apply(['vein.facial.'+side,'vein.deep_facial.'+side],facial_crossing,'Clear the retained transverse facial arterial connection while transporting the common venous collar.')
 def facial_connection(v):
  q=v.copy();x=sign*v[:,0];w=smooth((x-31)/4)*smooth((45-x)/4);q[:,1]+=6*w;return q
 apply(['Transverse facial–facial '+side],facial_connection,'Bow the illustrative transverse facial-to-facial arterial connection anterior to the corrected facial venous course; retain both endpoints.')
 # Temporal trunk: retain both lower drainage and upper scalp attachments.
 record=json.loads((WORK/'temporal-paths.json').read_text())[side];stations=np.array(record['z']);delta=np.array(record['centres'])-np.array(record['baselineCentres']);delta[:,2]=0;interpolate=PchipInterpolator(stations,delta)
 def temporal(v):
  z=v[:,2];q=v.copy();inside=(z>stations[0])&(z<stations[-1]);q[inside]+=interpolate(z[inside]);q[:,0]+=sign*.5*np.exp(-((z-55)/2)**2);return q
 apply(['vein.superficial_temporal.'+side],temporal,'Superficial temporal venous trunk follows the preauricular artery; distal scalp variation and retromandibular drainage are preserved.')
 # Hypoglossal route lowered towards the anterior condylar venous corridor.
 def hypoglossal(v):
  q=v.copy();x=sign*v[:,0];y=v[:,1];w=smooth((-y-65)/5)*smooth((y+78)/5)*smooth((x-11)/3);q[:,2]-=3.8*w*smooth((58-v[:,2])/16);return q
 apply(['Hypoglossal branch'+suffix,'Hypoglossal posterior meningeal'+suffix,'Medial clival'+suffix,'Odontoid descending'+suffix,'Neuromeningeal trunk'+suffix,'APhA odontoid–vertebral '+side,'APA prevertebral–odontoid '+side],hypoglossal,'Hypoglossal arterial branch shares the condylar corridor, preserving attached clival, posterior meningeal and odontoid collars.')
 # Labyrinthine artery: continuous ascent from the AICA collar to the porus region.
 from transport import acoustic_transport
 labyrinthine=acoustic_transport(side)
 apply(['Labyrinthine '+side,'Common cochlear '+side,'Anterior vestibular '+side],labyrinthine,'Labyrinthine branch reaches the internal acoustic region, retaining the AICA origin and cochlear/vestibular branch collars. The canal lumen and nerves are unsegmented.')
 # Local MMA apposition to the inner skull. Position sections with radius allowance.
 name='MMA frontal'+suffix;v,f=load(name);zs=np.arange(79,117,1.);centres=[];radii=[]
 for z in zs:
  pts=section(v,f,2,z);c=(pts.min(0)+pts.max(0))/2;centres.append(c);radii.append(np.median(np.linalg.norm(pts[:,:2]-c[:2],axis=1)))
 centres=np.array(centres);bones=['bone.frontal','bone.parietal.'+side,'bone.temporal.'+side,'bone.sphenoid'];cp=[];dd=[]
 for bone in bones:
  a,b=load(bone);p,d=closest(locator(a,b),centres);cp.append(p);dd.append(d)
 dd=np.array(dd);ix=np.argmin(dd,axis=0);cp=np.array(cp)[ix,np.arange(len(zs))];ds=dd[ix,np.arange(len(zs))];direction=(cp-centres)/np.maximum(ds[:,None],1e-8)
 target=direction*np.maximum(ds-np.array(radii)-1.2,0)[:,None];target[:,2]=0;target=gaussian_filter1d(target,1.2,axis=0);interp=PchipInterpolator(zs,target)
 def meningeal(v):
  z=v[:,2];w=smooth((z-81)/4)*smooth((116-z)/7);q=v.copy();q+=interp(np.clip(z,zs[0],zs[-1]))*w[:,None];return q
 apply([name],meningeal,'Frontal MMA local inner-table apposition, allowing a dural layer and preserving proximal and distal courses.')
 def meningeal_division(v):
  q=meningeal(v);return v+(q-v)*smooth((103-v[:,2])/3.9)[:,None]
 apply(['MMA frontal anterior division'+suffix],meningeal_division,'Transport frontal division collars, blending back to the existing distal branch.')
# Export original topology, with a reproducible source baseline contract.
checks=[]
for name,(v,f) in changed.items():
 old,_=load(name);tri=v[f];area=np.linalg.norm(np.cross(tri[:,1]-tri[:,0],tri[:,2]-tri[:,0]),axis=1);oldtri=old[f];oldarea=np.linalg.norm(np.cross(oldtri[:,1]-oldtri[:,0],oldtri[:,2]-oldtri[:,0]),axis=1);assert np.isfinite(v).all() and np.all(area[oldarea>1e-11]>1e-11),name
 write(name,v,f);checks.append(dict(node=name,vertices=len(v),triangles=len(f),maxShiftMm=float(np.linalg.norm(v-old,axis=1).max()),topologyPreserved=True,minDoubleTriangleAreaMm2=float(area.min())))
rev=dict(release='0.9.49',baselineRelease='0.9.48',baselineAssetHashes=json.loads((DATA/'source-assets.json').read_text()),newLabels=[],changed=[dict(node=n,file=FILES[n]) for n in changed],groups=groups,checks=checks,method='Smooth local coordinate shears with original indexed labelled surfaces and transported normals.',limitations=['Reference courses, not patient segmentation.','No cervical vertebrae, canal lumens or cranial nerves for independent canal containment validation.','Existing network label interfaces are retained; no whole-atlas watertightness claim.'])
(OUT/'revision.json').write_text(json.dumps(rev,indent=2)+'\n');print(json.dumps(checks,indent=2))
