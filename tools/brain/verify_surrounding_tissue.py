"""Audit all named surrounding tissue in the edited cortical phase."""
import json,hashlib,numpy as np,trimesh
from fit_vessels import APP
from verify_fitting import collisions

def main():
 brain=trimesh.load(APP/'.authoring/brain-baseline.glb',process=False)
 old=trimesh.load(APP/'.authoring/arteries-baseline.glb',process=False);new=trimesh.load(APP/'.authoring/arteries-fitted.glb',process=False)
 changed=[k for k,m in old.geometry.items() if not np.array_equal(m.vertices,new.geometry[k].vertices)]
 rows=[]
 for key in changed:
  phases=[trimesh.Trimesh(m.vertices,m.faces[np.all(m.vertices[m.faces,2]>=120,axis=1)],process=False) for m in [old.geometry[key],new.geometry[key]]]
  if not len(phases[1].faces):rows.append({'node':key,'phase':'z >= 120 mm','status':'no triangles in cortical test phase','contacts':[]});continue
  contacts=[]
  for name,m in brain.geometry.items():
   if any(k in name for k in ['tentorium','falx','sulcus','fissure','ventricle','lat-fis']):continue
   after=collisions(phases[1],m)
   if after:
    before=collisions(phases[0],m);contacts.append({'tissue':name,'beforeTriangleContacts':before,'afterTriangleContacts':after})
  rows.append({'node':key,'phase':'z >= 120 mm','contacts':contacts})
 out={'release':'0.9.17','authoringGeometrySha256':hashlib.sha256((APP/'.authoring/arteries-fitted.glb').read_bytes()).hexdigest(),'checks':rows,'excludedReferenceSheets':['falx','tentorium','sulcal/fissural references','ventricular references'],'limitations':['Parent transitions below z = 120 mm remain outside this cortical-phase check. Open tissue contacts are tested, but full solid containment cannot be inferred from them.']}
 (APP/'docs/validation/fitting-surrounding-tissue-v0.9.17.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(rows,indent=2))
if __name__=='__main__':main()
