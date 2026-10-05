"""Check fitted sulcal artery walls against the wider named brain context."""
import json,numpy as np,trimesh
from fit_vessels import APP,PUB
from verify_fitting import collisions

def main():
 old=trimesh.load(APP/'.authoring/arteries-baseline.glb',process=False)
 new=trimesh.load(APP/'.authoring/arteries-fitted.glb',process=False)
 brain=trimesh.load(PUB/'models/brain-context.glb',process=False)
 checks=[]
 for side in ['left','right']:
  for family in ['Central ','Central cortical branch ','Central distal ramus ']:
   key=family+side;phases=[]
   for scene in [old,new]:
    m=scene.geometry[key]
    phases.append(trimesh.Trimesh(m.vertices,m.faces[np.all(m.vertices[m.faces,2]>=120,axis=1)],process=False))
   for target,m in brain.geometry.items():
    if any(k in target for k in ['sulc','lat-fis','falx','tentorium','ventricle','aqueduct']):continue
    counts=[collisions(p,m) for p in phases]
    if any(counts):
     checks.append({'node':key,'target':target,'beforeTriangleContacts':counts[0],
                   'afterTriangleContacts':counts[1],'newContactRelationship':counts[0]==0 and counts[1]>0})
 report={'release':'0.9.17','phase':'central sulcal families, z >= 120 mm',
         'checks':checks,'limitations':['Reference sheets and ventricular surfaces are excluded. Existing contact counts do not establish anatomical acceptability.']}
 (APP/'docs/validation/fitting-cortical-neighbours-v0.9.17.json').write_text(json.dumps(report,indent=2)+'\n')
 print(json.dumps(checks,indent=2),flush=True)
 assert not any(c['newContactRelationship'] for c in checks),'New cortical tissue contact relationship'
if __name__=='__main__':main()
