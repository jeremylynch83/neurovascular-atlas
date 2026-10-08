from model import *
import hashlib

vtk.vtkLogger.SetStderrVerbosity(vtk.vtkLogger.VERBOSITY_OFF)
for p in OUT.glob('*.bin'):p.unlink()
report=[]
for side in ['right','left']:
 name='vein.internal_jugular.'+side;v,f=load(name);lo=-30.;hi=22.
 bv,bf=clip(v,f,v[:,2]-lo,False);tv,tf=clip(v,f,v[:,2]-hi,True)
 br=next(r for r in rings(bv,bf) if np.max(abs(bv[r,2]-lo))<1e-6)
 tr=next(r for r in rings(tv,tf) if np.max(abs(tv[r,2]-hi))<1e-6)
 bcentre=bv[br].mean(0);tcentre=tv[tr].mean(0)
 radii=[np.median(np.linalg.norm(bv[br,:2]-bcentre[:2],axis=1)),np.median(np.linalg.norm(tv[tr,:2]-tcentre[:2],axis=1))]
 vv=[bv,tv];ff=[bf,tf+len(bv)];offset=len(bv)+len(tv);last=br
 # A straight oblique cervical trunk, with its exact native end rings retained.
 for z in np.linspace(lo+.6,hi-.6,103):
  t=(z-lo)/(hi-lo);centre=bcentre*(1-t)+tcentre*t;centre[2]=z
  # Keep the middle upper neck posterior to the carotid origin.
  centre[1]-=2.0*np.sin(np.pi*t)**2
  radius=radii[0]*(1-t)+radii[1]*t
  ang=np.arange(64)*2*np.pi/64;ring=centre+np.c_[np.cos(ang)*radius,np.sin(ang)*radius,np.zeros(64)]
  vv.append(ring);allv=np.concatenate(vv);ids=np.arange(offset,offset+64);ff.append(bridge(allv,last,ids));last=ids;offset+=64
 allv=np.concatenate(vv);ff.append(bridge(allv,last,tr+len(bv)));allf=np.concatenate(ff)
 save(name,allv,allf)
 report.append({'side':side,'replacedCervicalRangeZmm':[lo,hi],'radiusAtEndpointsMm':radii,'nativeTributaryInterfacesRetained':True})

# Keep artery origin and remote scalp course fixed. Smoothly move the crossing
# towards the lateral surface of the revised jugular, with a broad local falloff.
for side in ['right','left']:
 name='Occipital' if side=='right' else 'Occipital left';v,f=load(name);j,jf=load('vein.internal_jugular.'+side,True);loc=locator(poly(j,jf));sign=1 if side=='right' else -1
 # Crossing is the ascending proximal OA in the upper neck, anterior to -90 mm.
 mask=(v[:,2]>3)&(v[:,2]<29)&(v[:,1]>-92)&(v[:,1]<-63)
 active=v[mask];centre=np.mean(active,axis=0);amp=0.
 # Use a lateral translation, broad enough to make the whole arterial tube clear.
 for attempt in range(45):
  amp=attempt*.5
  q=active.copy();w=smooth((q[:,2]-1)/5)*smooth((32-q[:,2])/8)*smooth((-q[:,1]-61)/7)*smooth((q[:,1]+102)/15)
  q[:,0]+=sign*amp*w
  if contacts(poly(np.column_stack([v[:,0]+sign*amp*(smooth((v[:,2]-1)/5)*smooth((32-v[:,2])/8)*smooth((-v[:,1]-61)/7)*smooth((v[:,1]+102)/15)),v[:,1:]]),f),poly(j,jf))==0:break
 else:raise RuntimeError('No clear OA crossing')
 def move(v,amp=amp,sign=sign,centre=centre):
  w=smooth((v[:,2]-1)/5)*smooth((32-v[:,2])/8)*smooth((-v[:,1]-61)/7)*smooth((v[:,1]+102)/15)
  # Adjacent branches receive the same displacement near their shared origins.
  lateral=1-smooth((abs(v[:,0]-centre[0])-9)/14)
  d=np.zeros_like(v);d[:,0]=sign*amp*w*lateral;return d
 for row in META:
  if row['file'] not in ['complete-circulation.glb','complete-anastomoses.glb']:continue
  n=row['name'];a,af=load(n);d=move(a)
  # Restrict changes to occipital trunk and connected child surfaces by proximity
  # to its crossing, keeping the carotid trunks exact.
  if n==name or (('occipital' in n.lower() or 'Occipital' in n) and (('left' in n)==(side=='left'))):
   if np.max(np.linalg.norm(d,axis=1))>.0001:save(n,a+d,af)
 report[-2 if side=='right' else -1]['occipitalLateralShiftMm']=amp
changed=[]
for row in META:
 if (OUT/(row['name']+'.positions.bin')).exists():changed.append({'node':row['name'],'file':row['file']})
revision={'release':'0.9.38','changed':changed,'newLabels':[],'baselineAssetHashes':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in (ROOT/'baseline').glob('*.glb')}}
(OUT/'revision.json').write_text(json.dumps(revision,indent=2)+'\n');(OUT/'repair.json').write_text(json.dumps(report,indent=2)+'\n');print(report);print('changed',len(changed),changed)
