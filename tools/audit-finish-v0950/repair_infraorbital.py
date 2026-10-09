"""Regenerate infraorbital reference stems with outward arterial clearance."""
from vein_geometry import *
revision=json.loads((OUT/'revision.json').read_text());paths=json.loads((OUT/'new-vein-paths.json').read_text())
for side,sign in [('right',1),('left',-1)]:
 if '--left-only' in sys.argv and side!='left':continue
 name='Infraorbital'+(' left' if side=='left' else '');q=np.load(WORK/(name+'.curve.npz'))['q'];q=q if q[0,1]>q[-1,1] else q[::-1];q=q+([-1,0,1] if side=='left' else [-sign*1.5,0,.5]);receiver='vein.pterygoid_plexus.'+side;q,attachment=connect(q,receiver);q,adjust=repel_arteries(q,.25,receiver,outward_arteries=True);v,f=tube(q,.25*(.65+.35*smooth(np.arange(len(q))/8)));node='vein.infraorbital.'+side;write(node,v,f)
 for row in revision['changed']:
  if row['node']==node:row.update(vertices=len(v),triangles=len(f))
 for path in paths:
  if path['node']==node:path.update(points=q.tolist(),attachment=attachment,arterialClearanceAdjustmentMm=adjust)
 print('Built',node,len(v),flush=True)
(OUT/'revision.json').write_text(json.dumps(revision,indent=2)+'\n');(OUT/'new-vein-paths.json').write_text(json.dumps(paths,indent=2)+'\n')
