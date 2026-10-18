#!/usr/bin/env python3
"""Reusable native gap/seam authoring: cache, scan, stage, validate, record.

This tool never installs a model or certifies an anatomical network.
"""
import argparse,json,time,sys,os,shutil
from pathlib import Path
import numpy as np
from cache import Scene,atomic_json,digest,locked,file_hash
from geometry import scan_network,patch_mesh,snap_seam
from validation import validate

APP=Path(__file__).resolve().parents[2]
LIMITS={'maxComponentVertices':12,'maxComponentSpanMm':.5,'maxSpanMm':.25,'maxPatchAreaMm2':.02,'maxWarpMm':.05,'minTriangleAreaMm2':1e-9,'maxSnapMm':.05,'snapSupportMm':1.0}
VERSION='1.0.0'
def tool_hash():return digest(b''.join(p.read_bytes() for p in sorted(Path(__file__).parent.glob('*.py')))+Path(__file__).with_name('decode.mjs').read_bytes())

def execute(app,config,cache,output,force=False,scan_only=False):
    begun=time.perf_counter();config=json.loads(json.dumps(config));limits={**LIMITS,**config.get('limits',{})};output=Path(output).resolve();cache=Path(cache).resolve()
    if config.get('schema')!=1:raise ValueError('Unsupported repair configuration')
    scene=Scene(app,cache,config.get('baselineOverrides'));loaded=time.perf_counter()
    signature=digest(json.dumps({'scene':scene.fingerprint,'config':config,'limits':limits,'tool':tool_hash()},sort_keys=True).encode())
    record=cache/'trials'/f'{signature}.json'
    if record.exists() and not force and not scan_only:
        prior=json.loads(record.read_text())
        # A known rejection can be reused even if its scratch staging was pruned.
        if prior['status']=='rejected' or all(Path(x['path']).is_file() and file_hash(x['path'])==x['sha256'] for x in prior.get('candidateArtifacts',[])):
            output.mkdir(parents=True,exist_ok=True)
            if prior['status']=='accepted':
                folder=output/'candidate';folder.mkdir(exist_ok=True)
                for artifact in prior['candidateArtifacts']:
                    source=Path(artifact['path']);target=folder/source.name
                    if source.resolve()!=target.resolve():shutil.copyfile(source,target)
                    artifact['path']=str(target)
                prior['candidateFiles']=[x['path']for x in prior['candidateArtifacts']]
            atomic_json(output/'accepted-corrections.json',{'accepted':prior['acceptedCorrections']})
            prior['reusedRecordedTrial']=True;prior['timingSeconds']={'total':time.perf_counter()-begun};prior['cache']=scene.stats
            output.mkdir(parents=True,exist_ok=True);atomic_json(output/'report.json',prior);return prior
    networks=config.get('networks',[]);proposals=[];candidates={};metadata={};scan_hits=0;scan_errors=[]
    for network in networks:
        key=digest(json.dumps({'network':network,'meshes':{n:scene.rows[n]['key']for n in network['nodes']},'limits':limits,'tool':tool_hash()},sort_keys=True).encode());p=cache/'boundaries'/f'{key}.json'
        if p.exists():rows=json.loads(p.read_text());scan_hits+=1
        else:
            try:rows=scan_network(scene,network,limits)
            except ValueError as ex:
                rows=[{'network':network['id'],'target':network['target'],'eligible':False,'error':True,'reason':str(ex)}]
            atomic_json(p,rows)
        scan_errors.extend({'network':network['id'],'reason':r['reason']}for r in rows if r.get('error'))
        proposals.extend(rows)
        if not scan_only:
            selected=[r for r in rows if r['eligible']]
            if selected:
                target=network['target']
                if target in candidates:raise ValueError('Put all neighbours of one target in one network')
                v,f,sources=patch_mesh(scene,target,selected);candidates[target]=(v,f);metadata[target]={'operation':'patch','appendedVertices':sources,'patchCount':len(selected)}
    scanned=time.perf_counter();operation_errors=list(scan_errors)
    if not scan_only:
        for seam in config.get('seams',[]):
            n=seam['target']
            if n in candidates:raise ValueError('Patch and seam operations require separate trials for the same target')
            try:
                p,g,detail=snap_seam(scene,seam,limits);candidates[n]=(p,g);metadata[n]={'operation':'snap',**detail}
            except ValueError as ex:operation_errors.append({'node':n,'reason':str(ex)})
    staged=time.perf_counter()
    active=[n for n in networks if n['target']in candidates]
    active += [{'id':'seam-'+x['target'],'target':x['target'],'nodes':[x['target'],x['parent']]} for x in config.get('seams',[])if x['target']in candidates]
    validation={'passed':None,'problems':[],'scope':'Scan only; no candidates validated.'} if scan_only else validate(scene,candidates,active,limits) if candidates else {'passed':False,'problems':[{'reason':'no-bounded-repair-candidate'}]}
    validation['problems'].extend(operation_errors)
    if operation_errors:validation['passed']=False
    checked=time.perf_counter();status='scan' if scan_only else 'accepted' if validation['passed'] else 'rejected'
    output.mkdir(parents=True,exist_ok=True);files=[];accepted=[]
    if not scan_only:
        folder=output/('candidate' if status=='accepted' else 'rejected');folder.mkdir(exist_ok=True)
        for n,(v,f) in candidates.items():
            for suffix,data in [('positions.bin',v.astype('<f4')),('indices.bin',f.astype('<u4'))]:
                path=folder/(n+'.'+suffix);data.tofile(path);files.append(str(path))
            accepted.append({'node':n,'passed':status=='accepted',**metadata[n]})
        atomic_json(output/'accepted-corrections.json',{'accepted':accepted if status=='accepted' else []})
    artifacts=[{'path':p,'sha256':file_hash(p)}for p in files]
    report={'schema':1,'toolVersion':VERSION,'signature':signature,'status':status,'stagedOnly':True,'sourceFingerprint':scene.fingerprint,'sourceHashes':scene.source_hashes,'baselineOverrides':scene.overrides,'limits':limits,'proposals':proposals,'operations':metadata,'validation':validation,'candidateFiles':files,'candidateArtifacts':artifacts,'acceptedCorrections':accepted if status=='accepted'else [],'reusedRecordedTrial':False,'cache':{**scene.stats,'boundaryCacheHits':scan_hits},'timingSeconds':{'prepare':loaded-begun,'scan':scanned-loaded,'seamFit':staged-scanned,'validate':checked-staged,'total':time.perf_counter()-begun}}
    atomic_json(output/'report.json',report)
    if not scan_only:
        atomic_json(record,report)
        with locked(cache/'trials/journal.lock'):
            with (cache/'trials/journal.jsonl').open('a')as journal:journal.write(json.dumps({'signature':signature,'status':status,'sourceFingerprint':scene.fingerprint,'output':str(output),'problems':validation['problems'],'timeUnix':time.time()})+'\n')
    return report

def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('command',choices=['prepare','scan','run']);parser.add_argument('--app',type=Path,default=APP);parser.add_argument('--config',type=Path);parser.add_argument('--cache-dir',type=Path);parser.add_argument('--output',type=Path);parser.add_argument('--retry',action='store_true',help='Explicitly repeat a recorded trial, including a rejection')
    args=parser.parse_args();root=(args.cache_dir or args.app/'.repair-cache').resolve()
    if args.command=='prepare':
        start=time.perf_counter();scene=Scene(args.app,root);print(json.dumps({'cache':scene.stats,'sourceFingerprint':scene.fingerprint,'seconds':time.perf_counter()-start}));return
    if not args.config:parser.error('--config is required for scan/run')
    config=json.loads(args.config.read_text());out=args.output or root/'latest';r=execute(args.app,config,root,out,args.retry,args.command=='scan')
    print(json.dumps({'status':r['status'],'report':str(out/'report.json'),'cache':r['cache'],'timingSeconds':r['timingSeconds'],'eligibleGaps':sum(x['eligible']for x in r.get('proposals',[])),'reusedRecordedTrial':r['reusedRecordedTrial']}))
    if args.command=='run' and r['status']=='rejected':sys.exit(2)

if __name__=='__main__':main()
