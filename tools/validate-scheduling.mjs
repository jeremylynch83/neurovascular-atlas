import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';
import {createServer} from 'vite';
const root=path.resolve(import.meta.dirname,'..');
const server=await createServer({root,server:{middlewareMode:true},appType:'custom'});
const saved=Object.fromEntries(['performance','requestAnimationFrame','cancelAnimationFrame','setTimeout','clearTimeout'].map(k=>[k,globalThis[k]]));
const checks=[];
try {
 const {AnatomyEngine}=await server.ssrLoadModule('/src/engine.ts');
 let now=0,nextId=0;const frames=new Map(),timers=new Map();
 globalThis.performance={now:()=>now};
 globalThis.requestAnimationFrame=cb=>{const id=++nextId;frames.set(id,cb);return id};
 globalThis.cancelAnimationFrame=id=>frames.delete(id);
 globalThis.setTimeout=cb=>{const id=++nextId;timers.set(id,cb);return id};
 globalThis.clearTimeout=id=>timers.delete(id);
 async function frame(){now+=16;for(const [id,cb] of [...frames]){frames.delete(id);cb(now)}for(const [id,cb] of [...timers]){timers.delete(id);cb()}await Promise.resolve();await Promise.resolve()}
 const e=Object.assign(Object.create(AnatomyEngine.prototype),{disposed:false,interacting:true,movingUntil:Infinity,nextBackgroundSlot:0,lastRenderDuration:1,frameInterval:16,workWaiters:new Set()});
 async function slot(maxFrames){let done=false;const p=e.workSlot(true).then(()=>done=true);assert.equal(done,false);let count=0;while(!done&&count<maxFrames){await frame();count++}assert(done,'Loading blocked during sustained interaction');await p;assert.equal(e.workWaiters.size,0);return count}
 assert.equal(await slot(2),1);checks.push('Sustained drag and continually moving camera allow installation after a paint');
 assert.equal(await slot(3),2);checks.push('Active drag applies a finite 24 ms minimum spacing instead of waiting for release');
 e.lastRenderDuration=100;await slot(3);assert.equal(e.nextBackgroundSlot-now,64);assert.equal(await slot(5),4);checks.push('Slow rendering caps spacing at 64 ms, even during a sustained drag');
 e.interacting=false;e.lastRenderDuration=1;e.nextBackgroundSlot=0;
 assert.equal(await slot(2),1);assert.equal(e.nextBackgroundSlot,now);checks.push('Normal idle rendering has only the post-paint yield, with no motion quiet period');
 e.nextBackgroundSlot=Infinity;
 let ended=false;const disposed=e.workSlot(true).then(()=>ended=true);e.disposed=true;for(const finish of [...e.workWaiters])finish();await disposed;assert(ended);assert.equal(e.workWaiters.size,0);checks.push('Disposal releases an outstanding work-slot waiter');
 const p=e.workSlot(false);await p;assert.equal(frames.size,0);checks.push('Initial skull installation retains its existing startup path');
 const release=JSON.parse(fs.readFileSync(root+'/package.json')).version;
 fs.writeFileSync(root+'/docs/revision153-scheduling-validation.json',JSON.stringify({release,checks,scope:'Actual AnatomyEngine.workSlot method under controlled animation frames and timing; no GPU/browser performance claim'},null,2)+'\n');
}finally{Object.assign(globalThis,saved);await server.close()}
console.log(JSON.stringify({passed:true,checks},null,2));
