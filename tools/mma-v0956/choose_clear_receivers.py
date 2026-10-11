"""Select nearby, neurally clear entry points on the unchanged native vein."""
from clear_neural import *
from vein_geometry import resample
neural=Neural();report=[]
document=json.loads((OUT/'paired-channel-candidates.json').read_text())
for side in ['right','left']:
    name='vein.middle_meningeal.anterior.'+side
    path=OUT/(name+'.curve.npz');data=np.load(path);q=data['q'];r=data['r'];old=data['stem']
    v,f=load('vein.sphenoparietal.'+side);centres=v[f].mean(1)
    centres=centres[np.linalg.norm(centres-old[-1],axis=1)<6]
    direction=centres-old[0];direction/=np.maximum(np.linalg.norm(direction,axis=1)[:,None],1e-12)
    ends=centres+direction*.3
    distance,_=neural.evaluate(ends);valid=distance>.5
    assert valid.any(), 'No clear native receiver entry within six millimetres'
    costs=np.linalg.norm(ends-old[0],axis=1)+.5*np.linalg.norm(ends-old[-1],axis=1);costs[~valid]=np.inf
    i=np.argmin(costs);end=ends[i];stem=resample(np.vstack([old[0],old[0]+.3*(end-old[0]),end]),.12)
    np.savez(path,q=q,r=r,stem=stem)
    row=next(x for x in document['channels'] if x['node']==name)
    row.update(receiverSurfaceEntryPoint=centres[i].tolist(),receiverStemLengthMm=float(np.linalg.norm(end-old[0])))
    report.append(dict(node=name,oldTerminal=old[-1].tolist(),newTerminal=end.tolist(),newNeuralClearanceMm=float(distance[i]),entryAdjustmentMm=float(np.linalg.norm(end-old[-1]))))
(OUT/'paired-channel-candidates.json').write_text(json.dumps(document,indent=2))
(OUT/'receiver-entry-adjustment.json').write_text(json.dumps(dict(method=__doc__,records=report),indent=2));print(report,flush=True)
