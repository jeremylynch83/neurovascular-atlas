from weld import *
rows=[]
for side in ['left','right']:
 names=['MMA frontal'+(' left'if side=='left'else''),'MMA paramedian '+side];parts={n:(np.fromfile(OUT/(n+'.positions.bin'),'<f4').reshape(-1,3).astype(float),np.fromfile(OUT/(n+'.indices.bin'),'<u4').reshape(-1,3))for n in names};parts,r=weld_parts(parts);r['side']=side
 for n,(p,g)in parts.items():p.astype('<f4').tofile(OUT/(n+'.positions.bin'));g.astype('<u4').tofile(OUT/(n+'.indices.bin'))
 p,f=parts[names[0]];q,g=parts[names[1]];v=np.vstack([p,q]);h=np.vstack([f,g+len(p)]);u,e,c=boundary(v,h);r['nonManifoldEdges']=int(np.sum(c>2));r['boundaryEdges']=int(np.sum(c==1));r['combinedSelfIntersections']=len(intersections(v,h));assert not r['nonManifoldEdges']and not r['combinedSelfIntersections'];print(r,flush=True);rows.append(r)
(D.parent/'final-weld.json').write_text(json.dumps(rows,indent=2)+'\n')
