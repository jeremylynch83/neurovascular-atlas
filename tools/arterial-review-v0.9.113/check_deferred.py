"""Reuse exclusions only while source assets and review code are byte-identical."""
from pathlib import Path
import hashlib,json,argparse

def check_assets(app,registry):
    changed=[]
    for name,expected in registry['requiredSourceAssetSha256'].items():
        p=app/'public/anatomy'/name
        if not p.is_file():
            changed.append({'asset':name,'reason':'missing'})
            continue
        h=hashlib.sha256()
        with p.open('rb')as stream:
            for block in iter(lambda:stream.read(1024*1024),b''):h.update(block)
        if h.hexdigest()!=expected:changed.append({'asset':name,'reason':'source-bytes-changed'})
    implementation=registry.get('requiredImplementationSha256')
    if not implementation:
        changed.append({'asset':'review-implementation','reason':'implementation-hashes-not-recorded'})
    else:
        for name,expected in implementation.items():
            p=app/name
            if not p.is_file():changed.append({'asset':name,'reason':'implementation-missing'})
            elif hashlib.sha256(p.read_bytes()).hexdigest()!=expected:changed.append({'asset':name,'reason':'implementation-bytes-changed'})
    return changed

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('app',nargs='?',type=Path,default=Path(__file__).resolve().parents[2])
    p.add_argument('--registry',type=Path)
    args=p.parse_args();app=args.app.resolve()
    current=app/'anatomy/source/intersection-predicate-v0.9.114/deferred-repairs.json'
    path=args.registry or(current if current.is_file()else app/'anatomy/source/arterial-review-v0.9.113/deferred-repairs.json')
    registry=json.loads(path.read_text());assert registry['schema']==1 and registry['appliesOnlyToRecordedSearchScopes']
    changed=check_assets(app,registry)
    report={'status':'baseline-changed-review-required'if changed else'baseline-unchanged-reuse-recorded-exclusions','sourceAssetsChecked':len(registry['requiredSourceAssetSha256']),'implementationFilesChecked':len(registry.get('requiredImplementationSha256',{})),'reviewedCases':len(registry['cases']),'changedAssets':changed,'appliesOnlyToRecordedSearchScopes':True,'allCasesRemainOpen':True,'policy':registry['policy']}
    print(json.dumps(report,indent=2))
    return 2 if changed else 0

if __name__=='__main__':raise SystemExit(main())
