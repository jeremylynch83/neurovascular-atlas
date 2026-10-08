from model import *
from fit import artery_field
changed=[a['name'] for a in META if a['file']=='complete-circulation.glb' and (OUT/(a['name']+'.positions.bin')).exists()];k=np.ascontiguousarray(np.concatenate([load(n)[0] for n in changed]).astype('<f4')).view('V12').ravel()
for row in META:
 if row['file']!='complete-anastomoses.glb':continue
 v,f=load(row['name']);hit=np.isin(np.ascontiguousarray(v.astype('<f4')).view('V12').ravel(),k)
 if not hit.any():continue
 nv=v+artery_field(v,'right')+artery_field(v,'left')
 if not np.array_equal(v.astype('<f4'),nv.astype('<f4')):save(row['name'],nv,f)
