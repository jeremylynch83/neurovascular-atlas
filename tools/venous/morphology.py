"""Angiogram-guided morphology amendments and bone-oriented sinus fitting.

Authoring only. Calibres are illustrative, not measurements from the figures.
See docs/VENOUS_v0.9.2.md for the reviewed cases and remaining limits.
"""
import numpy as np
from scipy.ndimage import gaussian_filter1d
from scipy.interpolate import CubicHermiteSpline


def amend_courses(rows):
    byid = {s['id']: s for s in rows}
    def update(key, **values):
        byid['vein.' + key].update(values)
    def attach(key, fraction=1):
        return {'structure': 'vein.' + key, 'fraction': fraction}
    def profile(kind, width, depth, centre, until=1):
        return dict(kind=kind, width=width, depth=depth, centre=centre,
                    bone_apposition=True, wall_clearance=.20, fit_until=until)
    centre = [.65, -65, 105]
    update('confluence', radius=3.15,
           profile=profile('oval', 1.08, .82, centre))
    update('superior_sagittal', radius=[.55, .95, 1.55, 2.2, 2.75, 3.2],
           profile=profile('rounded_triangle', 1.15, .90, centre))
    update('straight', radius=[2.15, 2.35, 2.65])
    update('inferior_sagittal', radius=[.28, .55, .9, 1.3])

    # Free peripheral origins are distinct from collecting-vein junctions.
    # Anastomotic veins remain patent at both connected ends.
    calibres = {
        'superficial_middle_cerebral': [.35, 1.05, 1.25, 1.45],
        'trolard': [.85, 1.15, 1.45, 1.7],
        'labbe': [.95, 1.2, 1.45, 1.7],
        'frontal_cortical': [.28, .5, .75, 1.0, 1.2],
        'parietal_cortical': [.28, .5, .75, 1.0, 1.2],
        'internal_cerebral': [1.05, 1.2, 1.45, 1.7],
        'basal': [1.05, 1.2, 1.4, 1.65],
        'thalamostriate': [.35, .65, .9, 1.15],
        'anterior_septal': [.26, .45, .7, .95],
        'superior_choroidal': [.25, .38, .55, .65],
        'anterior_cerebral': [.28, .45, .65, .8],
        'deep_middle_cerebral': [.30, .50, .75, .95],
        'cerebellopontine_fissure': [.35, .6, .85, 1.0],
        'inferior_vermian': [.30, .55, .8, 1.1],
        'inferior_hemispheric': [.28, .42, .65, .85],
    }
    for side, sign in [('right', 1), ('left', -1)]:
        def p(x, y, z):
            return [x if sign == 1 else 1.3-x, y, z if sign == 1 else z-.05]
        # The old entry was displaced anteriorly by the clearance pass, then
        # doubled back. This point lies in the observed jugular outlet corridor.
        byid['vein.internal_jugular.'+side]['points'][0]=p(29,-69,36)
        update('sigmoid.'+side,
               points=[p(59,-98,69),p(57,-90,59),p(49,-91,48),
                       p(40,-89,44),p(33,-81,42),p(30,-75,39),
                       attach('internal_jugular.'+side,0)],
               radius=([3.35,3.6,3.5,3.2,2.7,2.4] if sign == 1
                       else [2.95,3.2,3.1,2.85,2.6,2.4]),
               profile=profile('oval',1.05,.90,[.65,-105,65],.72),
               entry_tangent=[.18*sign,.95,-.25])
        update('transverse.'+side,
               points=[attach('confluence',.5),p(20,-144,66),
                       p(38,-134,66),p(52,-116,67),attach('sigmoid.'+side,0)],
               radius=([2.65,2.8,3.0,3.2,3.35] if sign == 1
                       else [2.3,2.4,2.6,2.8,2.95]),
               profile=profile('oval',1.15,.80,centre),
               continue_into='vein.sigmoid.'+side)
        byid['vein.sigmoid.'+side]['continue_into']='vein.internal_jugular.'+side
        for key, radius in calibres.items():
            update(key+'.'+side, radius=radius)
    update('superior_vermian', radius=[.3,.5,.75,.95])


def unit(v):
    return v / np.maximum(np.linalg.norm(v, axis=-1, keepdims=True), 1e-10)


def oriented_frames(q, profile, sdf=None):
    tangent = unit(np.gradient(q, axis=0))
    outward = unit(q - np.asarray(profile['centre']))
    if sdf is not None:
        raw=[]
        for p in q:
            grad=[0.,0.,0.]
            sdf.EvaluateGradient(p,grad)
            n=-np.asarray(grad)
            # Retain the intended intracranial side at ambiguous bone seams.
            if np.dot(n,p-np.asarray(profile['centre'])) < 0:
                n=-n
            raw.append(n)
        step=np.median(np.linalg.norm(np.diff(q,axis=0),axis=1))
        outward=unit(gaussian_filter1d(np.asarray(raw),max(1,3/max(step,.1)),axis=0,mode='nearest'))
    outward -= tangent * np.sum(outward*tangent,axis=1)[:,None]
    for i in np.flatnonzero(np.linalg.norm(outward,axis=1)<.1):
        axis=np.eye(3)[np.argmin(np.abs(tangent[i]))]
        outward[i]=axis-tangent[i]*np.dot(axis,tangent[i])
    outward=unit(outward)
    lateral=unit(np.cross(tangent,outward))
    return tangent,outward,lateral


def fit_sinus(q, r, profile, sdf, loc, fixed_start, fixed_end):
    """Fit to the inner skull without dodging small meningeal arteries.

    Smooth wall targets over millimetres, not individual mesh triangles. The
    lower sigmoid transitions to its jugular-foramen anchor before rays become
    unreliable in the open skull base. Final surface clearance is checked later.
    """
    import vtk
    centre=np.asarray(profile['centre']); target=q.copy()
    step=np.median(np.linalg.norm(np.diff(q,axis=0),axis=1))
    outward_extent=profile['depth']*(.87 if profile['kind']=='rounded_triangle' else 1)
    endfit=profile.get('fit_until',1)
    fractions=np.linspace(0,1,len(q))
    for i,(p,rad) in enumerate(zip(q,r)):
        if fractions[i]>endfit: continue
        points=vtk.vtkPoints();loc.IntersectWithLine(centre,centre+(p-centre)*4,points,None)
        if not points.GetNumberOfPoints(): continue
        wall=np.asarray(points.GetPoint(0));grad=[0.,0.,0.];sdf.EvaluateGradient(wall,grad)
        inward=unit(np.asarray(grad))
        if np.dot(inward,centre-wall)<0: inward=-inward
        target[i]=wall+inward*(rad*outward_extent+profile['wall_clearance'])
    # Fair the displacement, preserving the broad authored anatomical course.
    delta=gaussian_filter1d(target-q,max(1,3/max(step,.1)),axis=0,mode='nearest')
    weight=np.ones(len(q));arc=np.r_[0,np.cumsum(np.linalg.norm(np.diff(q,axis=0),axis=1))]
    if endfit<1:
        t=np.clip((endfit-fractions)/.14,0,1);weight*=t*t*(3-2*t)
    for fixed,distance in [(fixed_start,arc),(fixed_end,arc[-1]-arc)]:
        if fixed:
            t=np.clip(distance/12,0,1);weight*=t*t*(3-2*t)
    fitted=q+delta*weight[:,None]
    # Fair the course itself as well as its wall displacement. This prevents a
    # local bone ridge from surviving as a short hook in an otherwise broad arc.
    fair_mm=3.5 if endfit<1 else 1.5
    sigma=max(1,fair_mm/max(step,.1));pad=int(4*sigma)+1
    before=fitted[0]+np.arange(-pad,0)[:,None]*(fitted[1]-fitted[0])
    after=fitted[-1]+np.arange(1,pad+1)[:,None]*(fitted[-1]-fitted[-2])
    fair=gaussian_filter1d(np.vstack([before,fitted,after]),sigma,axis=0)[pad:-pad]
    # Endpoint attachment coordinates remain exact.
    u=np.linspace(0,1,len(q));fair+=(fitted[0]-fair[0])*(1-u[:,None])**3
    fair+=(fitted[-1]-fair[-1])*u[:,None]**3
    return fair


def continue_tangent(q, next_q, length=24):
    """Share a broad tangent across transverse/sigmoid and sigmoid/jugular joins."""
    arc=np.r_[0,np.cumsum(np.linalg.norm(np.diff(q,axis=0),axis=1))]
    start=max(1,np.searchsorted(arc,arc[-1]-length))
    span=arc[-1]-arc[start]
    if span<1: return q
    t0=unit(q[start+1]-q[start-1]);t1=unit(next_q[min(4,len(next_q)-1)]-next_q[0])
    spline=CubicHermiteSpline([0,span],[q[start],q[-1]],[t0,t1])
    q[start:]=spline(arc[start:]-arc[start])
    return q
