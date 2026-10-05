"""Check edited primary sulcal walls against retained arterial labels."""
import json,numpy as np,trimesh
from fit_vessels import APP
from verify_fitting import collisions

def main():
 old=trimesh.load(APP/'.authoring/arteries-baseline.glb',process=False);new=trimesh.load(APP/'.authoring/arteries-fitted.glb',process=False)
 changed=[k for k,m in old.geometry.items() if not np.array_equal(m.vertices,new.geometry[k].vertices)]
 retained=trimesh.util.concatenate([m for k,m in old.geometry.items() if k not in changed])
 rows=[]
 for side in ['left','right']:
  key='Central '+side
  if key not in changed:continue
  counts=[]
  for scene in [old,new]:
   m=scene.geometry[key];m=trimesh.Trimesh(m.vertices,m.faces[np.all(m.vertices[m.faces,2]>=120,axis=1)],process=False);counts.append(collisions(m,retained))
  rows.append({'node':key,'phase':'sulcal wall, z >= 120 mm','beforeContactsWithRetainedArteries':counts[0],'afterContactsWithRetainedArteries':counts[1]})
 out={'release':'0.9.17','editedFamilyExcludedAsSharedJunctions':changed,'checks':rows,'limitations':['Checks the primary sulcal wall against retained labels. It does not establish lumen patency or every branch/branch relationship.']}
 (APP/'docs/validation/fitting-arterial-neighbours-v0.9.17.json').write_text(json.dumps(out,indent=2)+'\n')
 print(json.dumps(rows,indent=2));assert all(r['afterContactsWithRetainedArteries']<=r['beforeContactsWithRetainedArteries'] for r in rows)
if __name__=='__main__':main()
