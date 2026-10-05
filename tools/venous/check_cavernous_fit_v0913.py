"""Independent checks of the displayed venous volume around ICA and medial bone."""
import json
import numpy as np
import vtk
from scipy.spatial import cKDTree
from refine_cavernous import read_glb,accessor,whole_veins,closed_artery,retained_ica_courses
from reference import APP,ROOT,poly,records,arrays,hits,locator
from vtk.util.numpy_support import numpy_to_vtk,vtk_to_numpy

bp,bf=arrays(next(r for r in records if r['name']=='bone.sphenoid'));bone=poly(bp,bf)
bone_sdf=vtk.vtkImplicitPolyDataDistance();bone_sdf.SetInput(bone)
bone_centres=bp[bf].mean(1)
bone_normals=np.cross(bp[bf[:,1]]-bp[bf[:,0]],bp[bf[:,2]]-bp[bf[:,0]])
bone_normals/=np.maximum(np.linalg.norm(bone_normals,axis=1)[:,None],1e-12)
d,b=read_glb(APP/'.authoring/circulation-refined.glb');arteries={};continued=retained_ica_courses()
for node in d['nodes']:
    if 'ICA cavernous' not in node['name']:continue
    q=d['meshes'][node['mesh']]['primitives'][0]
    p=accessor(d,b,q['attributes']['POSITION']).copy();n=accessor(d,b,q['attributes']['NORMAL']).copy()
    f=accessor(d,b,q['indices']).reshape(-1,3).copy()
    edge=np.sort(np.r_[f[:,[0,1]],f[:,[1,2]],f[:,[2,0]]],axis=1)
    e,c=np.unique(edge,axis=0,return_counts=True);ends=p[np.unique(e[c==1])]
    samples=p+.45*n
    end_distance=cKDTree(ends).query(p)[0]
    bg=np.array([bone_sdf.EvaluateFunction(pt) for pt in samples])
    # Existing low petrous/lacerum bone overlap and labelled end ports cannot
    # support a complete closed venous envelope while those source assets stay.
    closed=closed_artery(*continued[node['name'].split()[-1]]);cloud=vtk.vtkPolyData();cloud_points=vtk.vtkPoints()
    cloud_points.SetData(numpy_to_vtk(samples,deep=True));cloud.SetPoints(cloud_points)
    selection=vtk.vtkSelectEnclosedPoints();selection.SetInputData(cloud);selection.SetSurfaceData(closed)
    selection.SetTolerance(1e-6);selection.CheckSurfaceOn();selection.Update()
    in_artery=vtk_to_numpy(selection.GetOutput().GetPointData().GetArray('SelectedPoints')).astype(bool)
    artery_sdf=vtk.vtkImplicitPolyDataDistance();artery_sdf.SetInput(closed)
    artery_gap=np.abs(np.array([artery_sdf.EvaluateFunction(pt) for pt in samples]))
    # A normal offset may fall into another part of the tight siphon or beside
    # a label cap. Such a point cannot independently test venous enclosure.
    eligible=(p[:,2]>57)&(p[:,2]<67.5)&(end_distance>1.5)&(bg>.4)&(~in_artery)&(artery_gap>.35)
    arteries[node['name'].split()[-1]]=(p,f,n,samples,eligible,end_distance,bg,in_artery,artery_gap)

results={}
for release,path in [('0.9.12',ROOT/'baseline-v0.9.12/venous-raw.glb'),('0.9.13',ROOT/'venous-raw.glb')]:
    p,f,_,_=whole_veins(path);pd=poly(p,f);sdf=vtk.vtkImplicitPolyDataDistance();sdf.SetInput(pd);ray=locator(pd)
    current={}
    for side,(ap,af,an,samples,eligible,end_distance,bg,in_artery,artery_gap) in arteries.items():
        distances=np.array([sdf.EvaluateFunction(pt) for pt in samples[eligible]])
        cloud=vtk.vtkPolyData();cloud_points=vtk.vtkPoints();cloud_points.SetData(numpy_to_vtk(samples[eligible],deep=True));cloud.SetPoints(cloud_points)
        selection=vtk.vtkSelectEnclosedPoints();selection.SetInputData(cloud);selection.SetSurfaceData(pd);selection.SetTolerance(1e-6);selection.CheckSurfaceOn();selection.Update()
        enclosed=vtk_to_numpy(selection.GetOutput().GetPointData().GetArray('SelectedPoints')).astype(bool)&(np.abs(distances)>.025)
        test={'eligible_surface_samples':len(distances),'samples_in_venous_volume':int(enclosed.sum()),
              'surface_neighbourhood_enclosure_fraction':float(enclosed.mean()),
              'minimum_inward_distance_mm':float(-distances.max()),
              'missed_surface_neighbourhood_coordinates':samples[eligible][~enclosed].tolist(),
              'exclusions':{'total_excluded_samples':int((~eligible).sum()),'low_region_z_at_or_below_57mm':int((ap[:,2]<=57).sum()),'upper_arterial_course_excluded_from_inferior_enclosure_test':int((ap[:,2]>=67.5).sum()),'within_1_5mm_of_label_ports':int((end_distance<=1.5).sum()),'neighbour_within_0_4mm_of_sphenoid':int((bg<=.4).sum()),'normal_neighbour_inside_closed_arterial_mask':int(in_artery.sum()),'normal_neighbour_within_0_35mm_of_any_arterial_mask_surface':int((artery_gap<=.35).sum()),'counts_overlap':True}}
        test['passed']=bool(enclosed.mean()>.99)
        # Independently select facing sphenoid triangles, rather than reuse
        # authoring seeds or ask the generated distance field whether it fits.
        sign=1 if side=='right' else -1;lat=bone_centres[:,0] if sign==1 else 1.3-bone_centres[:,0]
        candidate=(lat>5)&(lat<13)&(bone_centres[:,1]>-53)&(bone_centres[:,1]<-37)&(bone_centres[:,2]>57)&(bone_centres[:,2]<68)&(sign*bone_normals[:,0]>.4)
        q=bone_centres[candidate];qn=bone_normals[candidate]
        aloc=vtk.vtkStaticCellLocator();aloc.SetDataSet(poly(ap,af));aloc.BuildLocator()
        probes=[]
        for pt,normal in zip(q,qn):
            closest=[0.,0.,0.];cid=vtk.reference(0);sub=vtk.reference(0);dd=vtk.reference(0.)
            aloc.FindClosestPoint(pt,closest,cid,sub,dd);v=np.array(closest)-pt;gap=np.linalg.norm(v)
            if .9<gap<2.8 and sign*v[0]>.6*gap and np.dot(v,normal)>.5*gap:
                probes.append((pt,normal))
        # One probe per 0.6 mm patch keeps the ray test small and reproducible.
        probes=sorted(probes,key=lambda item:tuple(item[0]));seen=set();chosen=[]
        for pt,normal in probes:
            key=tuple(np.rint(pt/.6).astype(int))
            if key in seen:continue
            seen.add(key);chosen.append((pt,normal))
        gaps=[];missing=[]
        for pt,normal in chosen:
            crossings=hits(ray,pt+normal*.02,pt+normal*1.1)
            if len(crossings):gaps.append(float(np.linalg.norm(crossings-pt,axis=1).min()))
            else:missing.append(pt.tolist())
        apposition={'independent_bone_patch_probes':len(chosen),'rays_reaching_venous_surface_within_1_1mm':len(gaps),
                    'fraction_reaching_surface':len(gaps)/len(chosen),'median_bone_to_venous_surface_gap_mm':float(np.median(gaps)) if gaps else None,
                    'p95_bone_to_venous_surface_gap_mm':float(np.percentile(gaps,95)) if gaps else None,
                    'missing_probe_coordinates':missing}
        apposition['passed']=bool(len(chosen)>=30 and len(gaps)/len(chosen)>.95 and np.percentile(gaps,95)<.55)
        current[side]={'ica_neighbourhood':test,'medial_sphenoid_apposition':apposition}
    results[release]=current
result={'release':'0.9.13','comparisons':results,'scope':'Actual watertight venous meshes. ICA samples are 0.45 mm along retained surface normals, more than 1.5 mm from arterial label ports, between z=57 and 67.5 mm in the inferior intracavernous test slab, at least 0.4 mm outside sphenoid bone, outside the independently closed continuing-ICA mask and over 0.35 mm from any continuing-ICA mask surface. Normal offsets inside another part of the siphon or near a temporary cap cannot test venous enclosure. Apposition uses independent facing sphenoid triangle centroids and ray intersections. The arterial label is not the sinus boundary. The upper extension is checked separately for absence. These are numerical mesh checks, not patient morphometry. The retained low ICA/bone overlap prevents a universal enclosure claim.'}
(APP/'docs/validation/cavernous-ica-bone-fit-v0.9.13.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))

assert all(x['ica_neighbourhood']['passed'] and x['medial_sphenoid_apposition']['passed'] for x in results['0.9.13'].values()),'Independent ICA/bone fit checks failed; inspect saved report'
