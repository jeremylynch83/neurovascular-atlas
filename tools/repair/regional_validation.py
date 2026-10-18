"""Numerical gates for explicit regional retopology and compound interfaces."""
import numpy as np
from cache import BVH
from geometry import edge_table,triangle_crosses
from validation import ray_inside

def enclosed_samples(vertices,faces,points):
    # Regional collars have thousands of samples. VTK performs the same
    # closed-volume ray test in compiled code, rather than a Python ray loop.
    import vtk
    from vtk.util.numpy_support import numpy_to_vtk,numpy_to_vtkIdTypeArray,vtk_to_numpy
    surface=vtk.vtkPolyData();vp=vtk.vtkPoints();vp.SetData(numpy_to_vtk(np.asarray(vertices,dtype=float),deep=True));surface.SetPoints(vp);cells=vtk.vtkCellArray();cells.SetCells(len(faces),numpy_to_vtkIdTypeArray(np.c_[np.full(len(faces),3),faces].astype(np.int64).ravel(),deep=True));surface.SetPolys(cells)
    data=vtk.vtkPolyData();p=vtk.vtkPoints();p.SetData(numpy_to_vtk(np.asarray(points,dtype=float),deep=True));data.SetPoints(p);test=vtk.vtkSelectEnclosedPoints();test.SetSurfaceData(surface);test.SetInputData(data);test.SetTolerance(1e-7);test.CheckSurfaceOff();test.Update();return vtk_to_numpy(test.GetOutput().GetPointData().GetArray('SelectedPoints')).astype(bool)

def face_key(t):return tuple(sorted(map(tuple,t)))
def validate_regional(scene,candidates,networks):
    changed={};trees={};retained={};rows=[];issues=[]
    for name,(p,g)in candidates.items():
        v,f=scene.mesh(name);source={face_key(v[t])for t in f};ids=np.array([i for i,t in enumerate(g)if face_key(p[t])not in source],dtype=int);changed[name]=ids;retained[name]=source;trees[name]=BVH.build(p,g)
        if not np.isfinite(p).all()or g.max()>=len(p):raise ValueError('Invalid regional arrays')
        t=p[g[ids]].astype(float);area=np.linalg.norm(np.cross(t[:,1]-t[:,0],t[:,2]-t[:,0]),axis=1)/2
        if len(area)and area.min()<1e-10:issues.append({'node':name,'reason':'degenerate-changed-face'})
        # Check every coordinate shared with another source label, including
        # duplicate seam positions. Retopology must preserve these attachments.
        oldkeys=set(map(tuple,v));newkeys=set(map(tuple,p));protected=[]
        for other in scene.nearby(v.min(0),v.max(0)):
            if other==name or other in candidates:continue
            w,h=scene.mesh(other);common=oldkeys&set(map(tuple,w))
            if common:
                missing=common-newkeys;protected.append({'other':other,'coordinates':len(common),'missing':len(missing)})
                if missing:issues.append({'node':name,'other':other,'reason':'lost-source-attachment','missing':len(missing)})
        rows.append({'node':name,'sourceVertices':len(v),'sourceTriangles':len(f),'candidateVertices':len(p),'candidateTriangles':len(g),'retainedSourceTriangles':len(g)-len(ids),'changedTriangles':len(ids),'protectedSourceAttachments':protected})
    crossings=[];checks=0;clearance=[]
    for name,(p,g)in candidates.items():
        for i in changed[name]:
            a=p[g[i]].astype(float);lo=a.min(0)-1e-7;hi=a.max(0)+1e-7
            for other in sorted(set(scene.nearby(lo,hi))|set(candidates)):
                w,h=candidates.get(other,scene.mesh(other));tree=trees[other]if other in trees else scene.bvh(other)
                for j in tree.query(lo,hi):
                    if other==name and i==j:continue
                    b=w[h[j]].astype(float)
                    if np.any(b.max(0)<lo)or np.any(b.min(0)>hi):continue
                    checks+=1
                    if triangle_crosses(a,b):crossings.append({'node':name,'face':int(i),'other':other,'otherFace':int(j)})
        if not len(changed[name]):continue
        t=p[g[changed[name]]].astype(float);lo=t.min((0,1));hi=t.max((0,1));samples=np.unique(np.vstack([t.reshape(-1,3),t.mean(1),((t+np.roll(t,-1,axis=1))/2).reshape(-1,3)]),axis=0)
        for other in scene.nearby(lo,hi):
            if scene.systems[other]not in ['bone','brain']or any(s in other for s in ['.falx-','.tentorium-','.petroclinoid-']):continue
            topology=scene.volume_topology(other);w,h=scene.mesh(other);bad=0;uncertain=0;minimum=float('inf')
            if topology['closedOrientedManifold']:
                bad=int(enclosed_samples(w,h,samples).sum())
            else:
                # For explicit reconstruction, all new face balls must remain
                # separated from open target surfaces. Absolute membership is
                # deliberately not inferred from an open target.
                for tri in t:
                    anchor=tri[0];radius=float(np.linalg.norm(tri-anchor,axis=1).max());distance=scene.bvh(other).nearest(anchor,w,h);minimum=min(minimum,distance-radius)
                    if distance<=radius+1e-6:bad+=1
            row={'node':name,'target':other,'closedTarget':topology['closedOrientedManifold'],'badSamplesOrFaceBalls':int(bad),'ambiguousSamples':int(uncertain),'sampleCount':len(samples),'minimumOpenTargetClearanceMarginMm':minimum if np.isfinite(minimum)else None};clearance.append(row)
            if bad or uncertain:issues.append({'node':name,'other':other,'reason':'tissue-clearance-failed','count':int(bad),'ambiguous':int(uncertain)})
    if crossings:issues.append({'reason':'changed-face-crossing','count':len(crossings)})
    native=[]
    for net in networks:
        old=[];new=[];a=b=0
        for n in net['nodes']:
            v,f=scene.mesh(n);p,g=candidates.get(n,(v,f));old.append((v,f+a));new.append((p,g+b));a+=len(v);b+=len(p)
        def edges(parts):
            u,e,c,b,_,_=edge_table(np.vstack([v for v,f in parts]),np.vstack([f for v,f in parts]));bad={tuple(map(tuple,u[x]))for x,k,bal in zip(e,c,b)if k>2 or(k==2 and bal!=0)};return int(sum(c==1)),bad
        before,prebad=edges(old);after,postbad=edges(new);extra=postbad-prebad
        if extra or after>=before:issues.append({'network':net['id'],'reason':'native-interface-regression','newBadEdges':len(extra),'boundaryEdgesBefore':before,'boundaryEdgesAfter':after})
        native.append({'id':net['id'],'boundaryEdgesBefore':before,'boundaryEdgesAfter':after,'preExistingBadEdges':len(prebad),'candidateBadEdges':len(postbad),'newBadEdges':len(extra)})
    return {'passed':not issues,'changes':rows,'crossings':crossings,'trianglePairsChecked':checks,'clearance':clearance,'nativeNetworks':native,'issues':issues,'scope':'All changed faces against all named surfaces; exact source attachments; no new bad native edges. Unchanged remote defects and regional anatomical acceptance remain open.'}
