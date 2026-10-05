"""Test absence of the previous upper ICA sleeve on actual exported surfaces."""
import json
import numpy as np
import vtk
from refine_cavernous import read_glb,accessor,whole_veins
from reference import APP,ROOT,poly

doc,data=read_glb(APP/'.authoring/circulation-refined.glb')
results={}
for node in doc['nodes']:
    if 'ICA cavernous' not in node['name']:continue
    side=node['name'].split()[-1]
    prim=doc['meshes'][node['mesh']]['primitives'][0]
    p=accessor(doc,data,prim['attributes']['POSITION']).copy()
    n=accessor(doc,data,prim['attributes']['NORMAL']).copy()
    # Fixed upper-course slab independent of the new sinus geometry.
    samples=(p+.45*n)[(p[:,2]>72.5)&(p[:,2]<75)]
    assert len(samples)>100
    current={}
    for version,path in [('0.9.12',ROOT/'baseline-v0.9.12/venous-raw.glb'),('0.9.13',ROOT/'venous-raw.glb')]:
        vp,vf,vl,ids=whole_veins(path)
        ff=vf[vl==ids.index('vein.cavernous.'+side)]
        sdf=vtk.vtkImplicitPolyDataDistance();sdf.SetInput(poly(vp,ff))
        gaps=np.abs(np.array([sdf.EvaluateFunction(q) for q in samples]))
        current[version]={'upper_course_samples':len(samples),'minimum_distance_to_cavernous_surface_mm':float(gaps.min()),'fraction_within_1mm_of_cavernous_surface':float((gaps<1).mean()),'maximum_cavernous_label_height_mm':float(vp[np.unique(ff),2].max())}
    results[side]=current
report={'release':'0.9.13','results':results,'scope':'Actual cavernous label surface, with fixed arterial slab z=72.5 to 75 mm. Tests absence of upper sleeve, independently of the positive inferior enclosure test. The inferred roof is constrained by model clinoid bone landmarks; it is not a segmented dural ring.'}
(APP/'docs/validation/cavernous-roof-v0.9.13.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
assert all(r['0.9.13']['minimum_distance_to_cavernous_surface_mm']>1 and r['0.9.13']['fraction_within_1mm_of_cavernous_surface']==0 for r in results.values())
