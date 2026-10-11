"""Restore two extracranial courses while retaining exact shared collars.

The intracranial flow must not carry superficial temporal or deep temporal
shafts through the skull. Preserve current shared interfaces, blending back to
the original extracranial course over 3–12 mm from those native interfaces.
"""
from clear_neural import *
revision=json.loads((OUT/'revision.json').read_text())
interfaces=json.loads((OUT/'field-interface-check.json').read_text())['exactSharedInterfaces']
report=[]
for name in ['STA frontal','Anterior deep temporal']:
    v,f=load(name);q,_=load(name,OUT);anchors=[]
    for row in interfaces:
        if name not in [row['a'],row['b']]:continue
        other=row['a'] if row['b']==name else row['b'];w,_=load(other)
        distance,_=cKDTree(w).query(v);anchors.extend(v[distance<1e-8])
    anchors=np.unique(anchors,axis=0);distance=cKDTree(anchors).query(v)[0]
    weight=1-smooth((distance-3)/9);new=v+(q-v)*weight[:,None]
    write(name,new,f)
    for row in revision['changed']:
        if row['node']==name:row.update(field='native-extracranial-course-with-shared-collars',maxShiftMm=float(np.linalg.norm(new-v,axis=1).max()))
    report.append(dict(node=name,nativeSharedCoordinates=len(anchors),unchangedCollarMaximumMm=float(np.linalg.norm(new[distance<1e-8]-q[distance<1e-8],axis=1).max()),exactRestoredVertices=int((weight==0).sum())))
(OUT/'revision.json').write_text(json.dumps(revision,indent=2))
(OUT/'extracranial-restoration.json').write_text(json.dumps(dict(method=__doc__,records=report),indent=2))
print(report,flush=True)
