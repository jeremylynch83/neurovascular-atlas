"""Shared geometry checks for reference-driven collateral reconstruction."""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).parents[1]/'mma-v0952'))
sys.path.insert(0,str(Path(__file__).parents[1]/'mma-v0958'))
from common import *
from fold_engine import intersections
vtk.vtkLogger.SetStderrVerbosity(vtk.vtkLogger.VERBOSITY_OFF)
rev=json.loads((OUT/'revision.json').read_text())
changed={r['node'] for r in rev['changed']}
def current(n): return load(n,OUT) if n in changed else load(n)
brain=[(n,*current(n)) for n in FILES if n.startswith('brain.') and not n.startswith(('brain.falx','brain.tentorium'))]
interfaces=json.loads((OUT/'native-interface-validation.json').read_text())['exactSharedInterfaces']
def pins(n):
    partners={r['b'] if r['a']==n else r['a'] for r in interfaces if n in (r['a'],r['b'])}
    foreign=set()
    for k in partners:foreign.update(map(bytes,np.ascontiguousarray(load(k)[0].astype('<f4')).view('V12').ravel()))
    return np.array([bytes(k) in foreign for k in np.ascontiguousarray(load(n)[0].astype('<f4')).view('V12').ravel()])
def matches(n,other):
    a,_=load(n);b,_=load(other);lookup={bytes(k):i for i,k in enumerate(np.ascontiguousarray(a.astype('<f4')).view('V12').ravel())}
    jj=[];ii=[]
    for j,k in enumerate(np.ascontiguousarray(b.astype('<f4')).view('V12').ravel()):
        if bytes(k) in lookup:jj.append(j);ii.append(lookup[bytes(k)])
    return np.array(ii,int),np.array(jj,int)
def neural(v,f):
    lo=v.min(0)-.05;hi=v.max(0)+.05;found=[]
    for n,w,g in brain:
        if np.any(w.max(0)<lo) or np.any(w.min(0)>hi):continue
        tri=w[g];take=np.all(tri.max(1)>=lo,axis=1)&np.all(tri.min(1)<=hi,axis=1)
        if take.any():
            count=contacts(v,f,w,g[take])
            if count:found.append(dict(brain=n,triangleContacts=count))
    return found
def assess(n,w,f,initial=None):
    sv,sf=load(n);v,_=current(n) if initial is None else (initial,f)
    pin=pins(n)
    return dict(neuralContacts=neural(w,f),newFoldPairs=len(intersections(w,f)-intersections(sv,sf)),nativePinsExact=bool(np.array_equal(w[pin].astype('<f4'),v[pin].astype('<f4'))),maximumAdditionalShiftMm=float(np.linalg.norm(w-v,axis=1).max()))
def tube(v,q,new,param,tt,rotation_weight=None):
    old=np.column_stack([np.interp(param,tt,q[:,k]) for k in range(3)])
    newp=np.column_stack([np.interp(param,tt,new[:,k]) for k in range(3)])
    a=np.gradient(q,axis=0);a/=np.maximum(np.linalg.norm(a,axis=1)[:,None],1e-12)
    b=np.gradient(new,axis=0);b/=np.maximum(np.linalg.norm(b,axis=1)[:,None],1e-12)
    if rotation_weight is not None:
        b=a*(1-rotation_weight[:,None])+b*rotation_weight[:,None]
        b/=np.maximum(np.linalg.norm(b,axis=1)[:,None],1e-12)
    a=np.column_stack([np.interp(param,tt,a[:,k]) for k in range(3)]);a/=np.maximum(np.linalg.norm(a,axis=1)[:,None],1e-12)
    b=np.column_stack([np.interp(param,tt,b[:,k]) for k in range(3)]);b/=np.maximum(np.linalg.norm(b,axis=1)[:,None],1e-12)
    cross=np.cross(a,b);dot=(a*b).sum(1);rad=v-old
    assert dot.min()>-.99,'Ambiguous tangent reversal'
    rotated=rad+np.cross(cross,rad)+np.cross(cross,np.cross(cross,rad))/np.maximum(1+dot[:,None],1e-12)
    return newp+rotated,old,newp
def save(n,w,f,field):
    write(n,w,f);sv,sf=load(n)
    row=dict(node=n,file=FILES[n],vertices=len(w),triangles=len(f),topologyExact=bool(np.array_equal(f,sf)),field=field,maxShiftMm=float(np.linalg.norm(w-sv,axis=1).max()))
    for i,r in enumerate(rev['changed']):
        if r['node']==n:rev['changed'][i]=row;break
    else:rev['changed'].append(row)
    changed.add(n)
    (OUT/'revision.json').write_text(json.dumps(rev,indent=2))
