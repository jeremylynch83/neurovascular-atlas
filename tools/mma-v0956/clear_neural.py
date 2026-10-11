"""Experimental shared arterial flow; never modifies the brain or public assets.

Open source parcels cannot define reliable remote signed interiors. A negative
distance outside a parcel AABB is therefore made unsigned. Exact triangle
intersection checks remain independent of this optimisation objective.
"""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).parents[1]/'mma-v0952'))
from smooth_fields import *
from scipy.ndimage import gaussian_filter1d
vtk.vtkLogger.SetStderrVerbosity(vtk.vtkLogger.VERBOSITY_OFF)

class Neural:
    def __init__(self):
        self.items=[]
        for name in FILES:
            if not name.startswith('brain.') or name.startswith(('brain.falx','brain.tentorium')):continue
            v,f=load(name);fn=vtk.vtkImplicitPolyDataDistance();fn.SetInput(poly(v,f))
            self.items.append((name,fn,v.min(0),v.max(0)))
    def evaluate(self,p,margin=4):
        d=np.full(len(p),margin,dtype=float);grad=np.zeros_like(p)
        for name,fn,lo,hi in self.items:
            ids=np.flatnonzero(np.all(p>=lo-margin,axis=1)&np.all(p<=hi+margin,axis=1))
            for i in ids:
                ds=fn.EvaluateFunction(p[i]);outside=np.any(p[i]<lo) or np.any(p[i]>hi)
                sign=-1 if ds<0 and outside else 1
                ds*=sign
                if ds<d[i]:
                    g=[0.,0.,0.];fn.EvaluateGradient(p[i],g)
                    d[i]=ds;grad[i]=np.asarray(g)*sign
        return d,grad

class Step:
    def __init__(self,p,d,sigma=2.0,support=8.):
        self.points=p;self.vectors=d;self.sigma=sigma;self.support=support
        self.tree=cKDTree(p)
    def __call__(self,v):
        result=v.copy()
        for start in range(0,len(v),3000):
            p=v[start:start+3000];dd,ii=self.tree.query(p,k=min(48,len(self.points)),distance_upper_bound=self.support)
            valid=np.isfinite(dd);safe=np.minimum(ii,len(self.points)-1)
            w=np.exp(-dd**2/(2*self.sigma**2))*smooth((self.support-dd)/(self.support-self.sigma))
            shift=np.sum(w[:,:,None]*self.vectors[safe],axis=1)/np.maximum(w.sum(1)[:,None],1e-30)
            taper=smooth((self.support-dd[:,0])/(self.support-self.sigma))*smooth((p[:,2]-44)/9)
            result[start:start+len(p)]+=shift*taper[:,None]
        return result

def run():
    guides=json.loads((WORK/'tree-guides.json').read_text())
    old=np.concatenate([np.asarray(g['oldPoints'])[::3] for g in guides])
    radii=np.concatenate([np.asarray(g['radiusMm'])[::3] for g in guides])
    outward=-np.concatenate([np.asarray(g['innerTableNormals'])[::3] for g in guides])
    outward/=np.linalg.norm(outward,axis=1)[:,None]
    q=arterial_field()(old);initial=q.copy();neural=Neural();steps=[];history=[]
    spans=[];start=0
    for g in guides:
        size=len(np.asarray(g['oldPoints'])[::3]);spans.append(slice(start,start+size));start+=size
    for it in range(100):
        dist,grad=neural.evaluate(q)
        if '--outward' in sys.argv:grad=outward
        deficit=np.maximum(radii+.45-dist,0)
        delta=grad*np.minimum(deficit*.6,.22)[:,None]
        for span in spans:delta[span]=gaussian_filter1d(delta[span],1.2,axis=0)
        # The original foraminal entrance remains fixed.
        delta*=smooth((old[:,2]-44)/9)[:,None]
        step=Step(q.copy(),delta);nq=step(q);steps.append((q.copy(),delta));q=nq
        row=dict(iteration=it,minimumClearanceMm=float(np.min(dist-radii)),deficientStations=int(np.sum(deficit>.05)),maximumShiftMm=float(np.linalg.norm(q-initial,axis=1).max()))
        history.append(row)
        if it%10==0:print(row,flush=True)
        if row['deficientStations']==0:break
    stem='outward-flow' if '--outward' in sys.argv else 'neural-flow'
    np.savez_compressed(WORK/(stem+'.npz'),points=np.asarray([p for p,d in steps]),vectors=np.asarray([d for p,d in steps]),old=old,initial=initial,final=q,radii=radii)
    (WORK/(stem+'-report.json')).write_text(json.dumps(dict(method=__doc__,direction='source inner-table outward normal' if '--outward' in sys.argv else 'neural distance gradient',history=history),indent=2))

if __name__=='__main__':run()
