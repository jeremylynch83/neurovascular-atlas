import {test} from 'node:test';
import assert from 'node:assert/strict';
import {StagedLoader,structureDependencies} from '../../src/stagedLoading.ts';

const row=(id,system,file)=>({id,name:id,system,children:[],parent:null,...(file?{asset:{file,node:id}}:{})});
const bone=row('bone','bone','bone.glb'),artery=row('artery','artery','artery.glb'),vein=row('vein','vein','vein.glb'),vein2=row('vein2','vein','vein.glb'),brain=row('brain','brain','brain.glb');
const manifest={structures:[bone,artery,vein,vein2,brain]};
const until=async predicate=>{for(let i=0;i<100;i++){if(predicate())return;await new Promise(r=>setTimeout(r,0));}assert.fail('queue did not settle');};
function fixture(options={}){
 const files=[],installed=[],prepared=[];let releases=0;let closed=false;
 const source={async load(file){files.push(file);await options.load?.(file)},async prepare(rows){prepared.push(rows.map(s=>s.id));await options.prepare?.(rows);return rows.slice(0,options.packetSize??16).map(s=>({id:s.id}))},async release(){releases++},dispose(){closed=true}};
 const loader=new StagedLoader(manifest,source,async meshes=>{await options.install?.(meshes);installed.push(...meshes.map(s=>s.id))},options.slot??(async()=>{}),()=>{});
 return {loader,files,installed,prepared,get releases(){return releases},get closed(){return closed}};
}
test('primary readiness excludes veins and brain; background finishes serially',async()=>{
 const f=fixture();await f.loader.loadCritical();assert.deepEqual(f.files,['bone.glb','artery.glb']);assert.deepEqual(f.installed,['bone','artery']);assert.equal(f.loader.states.get('vein').status,'pending');
 f.loader.startBackground();await until(()=>f.loader.states.get('brain').status==='ready');assert.deepEqual(f.files,['bone.glb','artery.glb','vein.glb','brain.glb']);assert.deepEqual(f.installed,['bone','artery','vein','vein2','brain']);f.loader.dispose();
});
test('requested background file is promoted; a request resolves after installation',async()=>{
 let finish;const f=fixture({install:async meshes=>{if(meshes[0].id==='brain')await new Promise(r=>finish=r)}});await f.loader.loadCritical();let resolved=false;const request=f.loader.ensure(['brain']).then(()=>resolved=true);
 f.loader.startBackground();await until(()=>!!finish);assert.deepEqual(f.files,['bone.glb','artery.glb','brain.glb']);assert.equal(resolved,false);assert.equal(f.loader.states.get('brain').status,'loading');finish();await request;assert.equal(resolved,true);f.loader.dispose();
});
test('a click prioritises a pending structure within the active asset',async()=>{
 let releaseLoad;const f=fixture({packetSize:1,load:async file=>{if(file==='vein.glb')await new Promise(r=>releaseLoad=r)}});await f.loader.loadCritical();f.loader.startBackground();await until(()=>!!releaseLoad);const request=f.loader.ensure(['vein2']);releaseLoad();await request;assert.equal(f.prepared[2][0],'vein2');f.loader.dispose();
});
test('a background failure leaves primary anatomy usable and can be retried',async()=>{
 let failures=1;const f=fixture({load:async file=>{if(file==='vein.glb'&&failures-->0)throw Error('Offline')}});await f.loader.loadCritical();f.loader.startBackground();await until(()=>f.loader.states.get('vein').status==='error');assert.equal(f.loader.states.get('artery').status,'ready');await f.loader.ensure(['vein']);assert.equal(f.loader.states.get('vein').status,'ready');assert.equal(f.installed.filter(id=>id==='artery').length,1);assert.equal(f.files.filter(file=>file==='vein.glb').length,2);f.loader.dispose();
});
test('slot gating prevents insertion while interaction is active',async()=>{
 let unlock;const f=fixture({slot:async background=>{if(background)await new Promise(r=>unlock=r)}});await f.loader.loadCritical();f.loader.startBackground();await until(()=>!!unlock);assert.deepEqual(f.installed,['bone','artery']);unlock();await until(()=>f.installed.includes('vein'));f.loader.dispose();
});
test('disposal rejects waiting actions and discards late prepared geometry',async()=>{
 let finish;const f=fixture({prepare:async rows=>{if(rows[0].id==='vein')await new Promise(r=>finish=r)}});await f.loader.loadCritical();f.loader.startBackground();await until(()=>!!finish);const request=f.loader.ensure(['vein']);const rejected=assert.rejects(request,/Atlas closed/);f.loader.dispose();finish();await rejected;await new Promise(r=>setTimeout(r,0));assert.deepEqual(f.installed,['bone','artery']);assert(f.closed);
});
test('landmark requests include their parcel and course-guide surfaces',()=>{
 const parcel=row('parcel','brain','brain.glb');const landmark={...row('landmark','brain'),surfaceAnchor:{structureId:'parcel'},vesselGuide:{surfaceStructureIds:['vein']}};const group={...row('group','brain'),children:['landmark']};const byId=new Map([parcel,landmark,group,vein].map(s=>[s.id,s]));const subtrees=new Map([['group',['landmark']],['landmark',['landmark']]]);assert.deepEqual(structureDependencies('group',byId,subtrees),['parcel','vein']);
});
