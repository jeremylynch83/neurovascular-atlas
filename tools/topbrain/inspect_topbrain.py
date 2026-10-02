#!/usr/bin/env python3
from pathlib import Path
import sys,re,nibabel as nib,numpy as np
from common import ensure_unpacked,find_case_files
raw=Path(sys.argv[1]); root=ensure_unpacked(raw)
cases=sorted({m.group(1) for p in root.rglob('topcow_ct_*_0000.nii.gz') if (m:=re.search(r'topcow_ct_(\d+)_0000',p.name))})
print('case\tshape\tspacing-mm\tlabels\tcoverage-score')
report=[]
for c in cases:
    imgp,labp=find_case_files(root,c,'ct')
    if not imgp or not labp: continue
    im=nib.load(str(imgp)); sp=im.header.get_zooms()[:3]; lab=nib.load(str(labp)); arr=np.asanyarray(lab.dataobj)
    labels=[int(x) for x in np.unique(arr) if x>0]
    # Geometry-only triage. This does not assess pathology or diagnostic suitability.
    score=(len(labels)/40)*0.65 + (min(sp)/max(sp))*0.15 + min(1,0.6/max(sp))*0.20
    report.append((score,c,imgp,labp,im.shape,sp,len(labels)))
for score,c,imgp,labp,shape,sp,nlab in sorted(report,reverse=True):
    print(f'{c}\t{shape}\t{tuple(round(x,3) for x in sp)}\t{nlab}/40\t{score:.3f}')
print('\nThis score only ranks resolution and label completeness. Inspect pathology/artefact before accepting a reference case.')
