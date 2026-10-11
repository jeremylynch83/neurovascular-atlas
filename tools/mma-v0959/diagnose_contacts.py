import sys,json
from pathlib import Path
sys.path.insert(0,str(Path(__file__).parents[1]/'mma-v0952'))
from common import *
vtk.vtkLogger.SetStderrVerbosity(vtk.vtkLogger.VERBOSITY_OFF)
rev=json.loads((OUT/'revision.json').read_text());changed={r['node']for r in rev['changed']};native=json.loads((OUT/'native-interface-validation.json').read_text())['exactSharedInterfaces'];report=json.loads((OUT/'all-mma-neural-validation.json').read_text());bad=sorted({r['artery']for r in report['contacts']if not r['brain'].startswith(('brain.falx','brain.tentorium'))});results=[]
def hit(v,f,w,g):
 c=vtk.vtkCollisionDetectionFilter();c.SetInputData(0,poly(v,f));c.SetInputData(1,poly(w,g));t=vtk.vtkTransform();c.SetTransform(0,t);c.SetTransform(1,t);c.SetCollisionModeToHalfContacts();c.SetCellTolerance(1e-7);c.Update();return vtk_to_numpy(c.GetContactCells(0)).astype(int)if c.GetNumberOfContacts()else np.empty(0,int)
for n in bad:
 v,f=load(n,OUT)if n in changed else load(n);sv,sf=load(n);x=np.load(WORK/(n+'.continuation-curve.npz'));partners={r['b']if r['a']==n else r['a']for r in native if n in [r['a'],r['b']]};foreign=set()
 for k in partners:foreign.update(map(bytes,np.ascontiguousarray(load(k)[0].astype('<f4')).view('V12').ravel()))
 pin=np.array([bytes(k)in foreign for k in np.ascontiguousarray(sv.astype('<f4')).view('V12').ravel()]);pairs=[]
 for r in report['contacts']:
  if r['artery']!=n or r['brain'].startswith(('brain.falx','brain.tentorium')):continue
  bn=r['brain'];bv,bf=load(bn,OUT)if bn in changed else load(bn);ids=hit(v,f,bv,bf);vi=np.unique(f[ids]);p=v[vi];arc=x['param'][vi];pin_d=cKDTree(v[pin]).query(p)[0]if pin.any()else np.full(len(p),np.inf)
  pairs.append(dict(brain=bn,contacts=len(ids),contactBounds=[p.min(0).tolist(),p.max(0).tolist()],contactMean=p.mean(0).tolist(),arcRange=[float(arc.min()),float(arc.max())],distanceToClosestNativeAttachmentMm=float(pin_d.min()),collidingPinnedVertices=int(pin[vi].sum())))
 row=dict(node=n,pinnedVertices=v[pin].tolist(),partners=sorted(partners),arcLength=float(x['tt'][-1]-x['tt'][0]),contacts=pairs);results.append(row);print(json.dumps(row),flush=True)
(OUT/'residual-route-diagnosis.json').write_text(json.dumps(results,indent=2))
