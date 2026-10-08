from model import *
from build_geometry import shared
from venous import field
rr,_=shared('vein.basilar_plexus','vein.prepontine_bridge.right');rr=(rr+field(rr)).astype('<f4');c=rr.mean(0);v,f=load('vein.basilar_plexus',True);p,d=closest(locator(poly(v,f)),c);v,f=clip(v,f,np.linalg.norm(v-p,axis=1)-1.0);loops=rings(v,f,np.flatnonzero(np.linalg.norm(v-p,axis=1)<1.1));assert len(loops)==1;o=len(v);v=np.concatenate([v,rr]);f=np.concatenate([f,bridge(v,loops[0],np.arange(o,len(v)))]);save('vein.basilar_plexus',v,f);(OUT/'basilar-prepontine-graft.json').write_text(json.dumps({'branch':'vein.prepontine_bridge.right','nativeRingVertices':len(rr),'nearestNewWallGapMm':d,'graftHoleRadiusMm':1,'method':'Preserved native branch ring; continuous wall cut and ordered triangulated collar'},indent=2))
