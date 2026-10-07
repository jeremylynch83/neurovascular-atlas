"""Reconcile the dural attachment rather than shifting a connected Galenic trunk."""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'anatomical-fixes-v0929'))
from geometry import *
from scipy.interpolate import PchipInterpolator
OUT=ROOT.parent/'corrections-work';q=np.array(json.loads((OUT/'curves.json').read_text())['vein.straight']['points']);order=np.argsort(q[:,1]);height=PchipInterpolator(q[order,1],q[order,2],extrapolate=True)
names=['brain.tentorium-cerebelli.right','brain.tentorium-cerebelli.left','brain.falx-cerebri'];original=meshes['brain.tentorium-cerebelli.right'].v
# Existing medial tentorial ridge, measured by bins to avoid using a lateral free edge.
ys=np.arange(-143,-96,2.);z=[]
for y in ys:
 points=original[(abs(original[:,0]-.636)<3)&(abs(original[:,1]-y)<3)]
 z.append(float(np.percentile(points[:,2],75)) if len(points) else float(np.median(original[:,2])))
old=PchipInterpolator(ys,z,extrapolate=True)
C=OUT/'dura';C.mkdir(exist_ok=True);candidate={};report=[]
for n in names:
 m=meshes[n];v=m.v.copy();x,y,h=v.T
 weight=(1-smooth((abs(x-.636)-1.5)/27))*(1-smooth((y+104)/8))*smooth((y+149)/6)
 if n=='brain.falx-cerebri':weight*=1-smooth((h-old(y)-3)/28)
 change=(height(np.clip(y,q[:,1].min(),q[:,1].max()))-old(y))*weight
 v[:,2]+=change;candidate[n]=poly(v,m.f);v.astype('<f4').tofile(C/(n+'.positions.bin'));report.append({'node':n,'maximumDisplacementMm':float(np.max(abs(change)))})
new=[]
for n,p in candidate.items():
 a=np.array(p.GetBounds()).reshape(3,2).T
 for o,m in meshes.items():
  if o in names or m.file not in ['brain-context.glb','craniofacial.glb','complete-circulation.glb']:continue
  if o.startswith('brain.') and any(t in o for t in ['ventricle','aqueduct']):continue
  b=m.bounds
  if np.any(a[1]<b[0]) or np.any(b[1]<a[0]):continue
  if contacts(p,m.pd,True) and not contacts(meshes[n].pd,m.pd,True):new.append([n,o])
r={'changed':report,'newContacts':new,'method':'Medial dural ridge follows the retained connected sinus; lateral skull attachments taper to the baseline','independentSegmentation':False};(C/'revision.json').write_text(json.dumps(r,indent=2)+'\n');print(r,flush=True)
