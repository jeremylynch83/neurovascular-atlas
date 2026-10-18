#!/usr/bin/env python3
"""Replay v0.9.92 with the old scripts and the reusable cached pipeline."""
import argparse,json,shutil,subprocess,time,statistics,sys,tempfile
from pathlib import Path
import numpy as np
from cache import atomic_json

APP=Path(__file__).resolve().parents[2]
CONFIG=APP/'tools/repair/configs/tentorial-v0.9.92-replay.json'
NAMES=['Tentorial marginal left','Tentorial marginal right']
def run(args,log):
    with open(log,'w')as stream:subprocess.run(args,cwd=APP,stdout=stream,stderr=subprocess.STDOUT,check=True)
def fingerprint(v,f):return {tuple(sorted(map(tuple,v[t])))for t in f}
def compare(folder):
    source=APP/'anatomy/source/tentorial-attachment-v0.9.92';rows=[]
    for n in NAMES:
        p=np.fromfile(folder/'candidate'/(n+'.positions.bin'),'<f4').reshape(-1,3);f=np.fromfile(folder/'candidate'/(n+'.indices.bin'),'<u4').reshape(-1,3)
        v=np.fromfile(source/'candidate'/(n+'.positions.bin'),'<f4').reshape(-1,3);g=np.fromfile(source/'candidate'/(n+'.indices.bin'),'<u4').reshape(-1,3)
        oldv=np.fromfile(source/'baseline'/(n+'.positions.bin'),'<f4').reshape(-1,3);oldf=np.fromfile(source/'baseline'/(n+'.indices.bin'),'<u4').reshape(-1,3)
        assert np.array_equal(p[:len(oldv)],oldv)and np.array_equal(f[:len(oldf)],oldf)
        assert len(f)-len(oldf)==(4 if n.endswith('left')else 3)
        assert fingerprint(p,f[len(oldf):])==fingerprint(v,g[len(oldf):]),n+' patch surface differs'
        rows.append({'node':n,'addedTriangles':len(f)-len(oldf),'patchTrianglesMatchV092Exactly':True,'sourceCoordinatesAndFacesExact':True})
    return rows
def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--work',type=Path,required=True,help='A new directory, so the empty-cache run is reproducible');parser.add_argument('--repeats',type=int,default=3);args=parser.parse_args();work=args.work.resolve()
    if work.exists():raise SystemExit('Use a new benchmark directory; existing results are never deleted')
    if args.repeats<1:raise SystemExit('--repeats must be positive')
    work.mkdir(parents=True);fixture=json.loads(CONFIG.read_text());legacy=[]
    for i in range(args.repeats):
        case=work/f'legacy-{i}';case.mkdir();start=time.perf_counter()
        run(['node','tools/decode-posterior-baseline.mjs','public/anatomy/models',str(case/'decoded')],case/'decode.log')
        for n,entry in fixture['baselineOverrides'].items():
            shutil.copyfile(APP/entry['positions'],case/'decoded'/(n+'.positions.bin'));shutil.copyfile(APP/entry['indices'],case/'decoded'/(n+'.indices.bin'))
        run([sys.executable,'tools/tentorial-attachment-v0.9.92/repair.py',str(case)],case/'repair.log')
        run([sys.executable,'tools/tentorial-attachment-v0.9.92/validate.py',str(case)],case/'validation.log')
        elapsed=time.perf_counter()-start;compare(case);legacy.append(elapsed);print('legacy',i,round(elapsed,3),flush=True)
    cache=work/'cache';modern=[];reports=[]
    for i in range(args.repeats+1):
        case=work/('empty-cache'if i==0 else f'warm-{i}');start=time.perf_counter()
        run([sys.executable,'tools/repair/repair.py','run','--config',str(CONFIG),'--cache-dir',str(cache),'--output',str(case),'--retry'],work/f'pipeline-{i}.log')
        elapsed=time.perf_counter()-start;r=json.loads((case/'report.json').read_text());assert r['status']=='accepted'and not r['reusedRecordedTrial'];assert sum(x['eligible']for x in r['proposals'])==4
        same=compare(case);modern.append(elapsed);reports.append(r);print('pipeline',i,round(elapsed,3),flush=True)
    warm=statistics.median(modern[1:]);old=statistics.median(legacy)
    result={'schema':1,'scope':'Authoring replay of four known small native wall gaps, including source preparation, detection/patching, local validation and staging. Excludes export, DSA, release build, human review, archive transfer and regional reconstruction. OS page cache is uncontrolled; empty cache means an empty authoring cache.','repeats':args.repeats,'legacySeconds':legacy,'legacyMedianSeconds':old,'pipelineEmptyCacheSeconds':modern[0],'pipelineWarmSeconds':modern[1:],'pipelineWarmMedianSeconds':warm,'warmSpeedupVsLegacy':old/warm,'warmSpeedupVsEmptyAuthoringCache':modern[0]/warm,'warmTimeReductionVsLegacyPercent':100*(1-warm/old),'knownGapsRepaired':4,'trianglesAdded':7,'replayComparison':same,'warmRunsRepeatedAllLocalChecks':True,'emptyCacheStats':reports[0]['cache'],'warmCacheStats':reports[-1]['cache'],'sourceHashes':reports[-1]['sourceHashes'],'validation':reports[-1]['validation']}
    atomic_json(work/'benchmark.json',result);print(json.dumps({k:v for k,v in result.items()if k not in ['validation','sourceHashes']}),flush=True)
if __name__=='__main__':main()
