"""Peripheral skin clearance; major sinus walls are clipped before meshing."""
import numpy as np
import vtk
from scipy.sparse import coo_matrix
from reference import records, arrays, poly
from morphology import unit


def fit_skin(p, f, labels, spec):
    ids=[s['id'] for s in spec['structures']]
    protected=np.zeros(len(p),bool)
    for side in ['right','left']:
        protected[np.unique(f[labels==ids.index('vein.anterior_condylar.'+side)])]=True
    major=np.zeros(len(p),bool)
    for i,s in enumerate(spec['structures']):
        if not s.get('profile'):continue
        mask=labels==i;vertices=np.unique(f[mask]);major[vertices]=True
    edges=np.concatenate([f[:,[0,1]],f[:,[1,2]],f[:,[2,0]]])
    edges=np.concatenate([edges,edges[:,::-1]])
    adj=coo_matrix((np.ones(len(edges)),(edges[:,0],edges[:,1])),shape=(len(p),len(p))).tocsr()
    degree=np.maximum(1,np.asarray(adj.sum(1)).ravel())[:,None]
    fields=[]
    for rec in records:
        if rec['name'] in ['bone.mandible','bone.temporal.left','bone.temporal.right','bone.occipital','bone.frontal','bone.parietal.left','bone.parietal.right']:
            sdf=vtk.vtkImplicitPolyDataDistance();sdf.SetInput(poly(*arrays(rec)))
            fields.append((sdf,np.array(rec['bounds'])))
    # Existing peripheral clearance, excluding dural walls. Separate gradients
    # can oppose one another at sutures and must not direct major sinus fitting.
    for iteration in range(12):
        delta=np.zeros_like(p);touched=0
        for sdf,(lo,hi) in fields:
            ix=np.flatnonzero(np.all((p>=lo-.25)&(p<=hi+.25),axis=1)&~protected&~major)
            for i in ix:
                d=sdf.EvaluateFunction(p[i])
                if d<.12:
                    g=[0.,0.,0.];sdf.EvaluateGradient(p[i],g)
                    delta[i]+=unit(np.asarray(g))*min(.4,.18-d);touched+=1
        if not touched:break
        for _ in range(2):delta=.7*delta+.3*(adj@delta)/degree
        delta[protected|major]=0;p+=delta

    # Preserve the established local mandibular correction for the deep facial
    # vein; it does not share a wall with a cranial sinus.
    rec=next(r for r in records if r['name']=='bone.mandible')
    sdf=vtk.vtkImplicitPolyDataDistance();sdf.SetInput(poly(*arrays(rec)))
    ff=f[labels==ids.index('vein.deep_facial.left')]
    for _ in range(16):
        delta=np.zeros_like(p);weights=np.zeros(len(p));bad=0
        for face,c in zip(ff,p[ff].mean(1)):
            d=sdf.EvaluateFunction(c)
            if d>=.04:continue
            g=[0.,0.,0.];sdf.EvaluateGradient(c,g);shift=unit(np.asarray(g))*min(.35,.1-d)
            for i in face:delta[i]+=shift;weights[i]+=1
            bad+=1
        if not bad:break
        delta/=np.maximum(1,weights)[:,None];p+=.8*delta+.2*(adj@delta)/degree
    return p
