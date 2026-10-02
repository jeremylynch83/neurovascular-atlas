from pathlib import Path
import re, zipfile

def ensure_unpacked(raw:Path)->Path:
    out=raw/'unpacked'
    if any(out.rglob('*.nii.gz')): return out
    zips=list(raw.glob('TopBrain*.zip'))
    if not zips: raise SystemExit('TopBrain archive not found. Run ./anatomy.sh download first.')
    out.mkdir(parents=True,exist_ok=True)
    print(f'Unpacking {zips[0].name} (one-time operation)...',flush=True)
    with zipfile.ZipFile(zips[0]) as z:z.extractall(out)
    return out

def find_case_files(root:Path, case:str, modality='ct'):
    case=case.zfill(3)
    imgs=[p for p in root.rglob('*.nii.gz') if re.search(fr'topcow_{modality}_{case}_0000\.nii\.gz$',p.name,re.I)]
    labs=[p for p in root.rglob('*.nii.gz') if case in p.name and 'label' in str(p.parent).lower() and modality in str(p.parent).lower()]
    # Prefer v1 TopBrain modality-specific masks, which have CTA labels 1-40.
    labs=sorted(labs,key=lambda p:(0 if 'v1' in str(p).lower() or 'labelsTr_topbrain_ct'.lower() in str(p.parent).lower() else 1,len(str(p))))
    return (imgs[0] if imgs else None, labs[0] if labs else None)
