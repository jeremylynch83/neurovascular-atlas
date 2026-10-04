"""Check rebuilt terminal surfaces, clearances and exported shared normals."""
import json
import numpy as np
import vtk
from refine_cavernous import read_glb,accessor,retained_ica_courses
from reference import APP,ROOT,poly,records,arrays

d,b=read_glb(ROOT/'venous-raw.glb');parts={}
for node in d['nodes']:
    prim=d['meshes'][node['mesh']]['primitives'][0]
    parts[node['name']]=tuple(accessor(d,b,prim['attributes'][key]).copy()
                             for key in ['POSITION','NORMAL'])+(accessor(d,b,prim['indices']).reshape(-1,3).copy(),)
arteries={side:poly(p,f) for side,(p,f) in retained_ica_courses().items()}
append=vtk.vtkAppendPolyData()
for r in records:
    if r['name'] in ['bone.sphenoid','bone.temporal.right','bone.temporal.left']:
        append.AddInputData(poly(*arrays(r)))
append.Update();bone=append.GetOutput();sdf=vtk.vtkImplicitPolyDataDistance();sdf.SetInput(bone)
report={}
for side in ['right','left']:
    cp,cn,_=parts['vein.cavernous.'+side]
    csnorm={tuple(q):n for q,n in zip(cp,cn)}
    for name in ['superficial_middle_cerebral','sphenoparietal','superior_ophthalmic','ovale_emissary','superior_petrosal','inferior_petrosal']:
        sid='vein.'+name+'.'+side;p,n,f=parts[sid]
        shared=[float(np.linalg.norm(nn-csnorm[tuple(q)])) for q,nn in zip(p,n) if tuple(q) in csnorm]
        assert len(shared)>10 and max(shared)==0,(sid,len(shared),max(shared,default=None))
        # Exact triangle geometry inside the rebuilt region; exclude the retained
        # overlap collar and unchanged peripheral course. No clipping caps added.
        lo=np.array([-24.6,-57.,45.3]);hi=np.array([26.1,-28.2,80.7])
        t=p[f];keep=np.all(t>lo+.1,axis=(1,2))&np.all(t<hi-.1,axis=(1,2));ff=f[keep]
        assert len(ff)>100,sid
        points=np.r_[p[np.unique(ff)],p[ff].mean(1)]
        distances=np.array([sdf.EvaluateFunction(q) for q in points])
        crossings={}
        for key,target in [('skull',bone),('ICA',arteries[side])]:
            inter=vtk.vtkIntersectionPolyDataFilter();inter.SetInputData(0,poly(p,ff));inter.SetInputData(1,target)
            inter.SplitFirstOutputOff();inter.SplitSecondOutputOff();inter.SetTolerance(1e-5);inter.Update()
            crossings[key]=int(inter.GetOutput(0).GetNumberOfLines())
            assert crossings[key]==0,(sid,key,crossings[key])
        assert distances.min()>0,(sid,float(distances.min()))
        report[sid]={'shared_junction_vertices':len(shared),'maximum_exported_junction_normal_difference':max(shared),
                     'local_terminal_triangles':len(ff),'surface_and_centroid_samples':len(points),
                     'minimum_sampled_skull_gap_mm':float(distances.min()),'triangle_intersection_lines':crossings}
result={'release':'0.9.12','entries':report,'scope':'ICA clearance includes the continuous retained petrous, cavernous and paraophthalmic skin. Actual rebuilt terminal triangles strictly inside the regional replacement bounds, excluding the retained overlap collar. Sampled gaps are mesh clearances, not patient measurements or wall thicknesses. Shared normals are checked on the exact exported GLB coordinates.'}
(APP/'docs/validation/cavernous-entry-clearances-v0.9.12.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
