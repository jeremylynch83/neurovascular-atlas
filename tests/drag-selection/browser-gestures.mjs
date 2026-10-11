import { createRequire } from 'node:module';
import { readFile, writeFile } from 'node:fs/promises';
import assert from 'node:assert/strict';
const require=createRequire(import.meta.url);
const {chromium}=require(process.env.CODEX_PRIMARY_RUNTIME_NODE_MODULES ? process.env.CODEX_PRIMARY_RUNTIME_NODE_MODULES+'/playwright' : 'playwright');
const browser=await chromium.launch({headless:true,executablePath:process.env.ATLAS_TEST_CHROMIUM,args:['--no-sandbox','--disable-dev-shm-usage']});
const page=await browser.newPage({viewport:{width:900,height:650},hasTouch:true});
await page.setContent('<canvas id="atlas" class="atlas-canvas" width="600" height="400" style="touch-action:none;background:#eee"></canvas>');
const source=await readFile(new URL('./selectionGesture.mjs',import.meta.url),'utf8');
await page.addScriptTag({type:'module',content:source+`
 const canvas=document.querySelector('#atlas');
 window.picks=0;window.selected='existing-vessel';
 window.cleanup=bindSelectionGesture(canvas,()=>{window.picks++;window.selected='release-vessel';});
 // Same capture/release behaviour used by camera controls. Release capture
 // in their pointerup handler to test interaction with lostpointercapture.
 canvas.addEventListener('pointerdown',e=>canvas.setPointerCapture(e.pointerId));
 canvas.addEventListener('pointerup',e=>{if(canvas.hasPointerCapture(e.pointerId))canvas.releasePointerCapture(e.pointerId);});
 window.loaded=true;
`});
await page.waitForFunction(()=>window.loaded);
const results=[];
async function check(name,act,expected){await page.evaluate(()=>{window.picks=0;window.selected='existing-vessel';});await act();const actual=await page.evaluate(()=>({picks:window.picks,selected:window.selected}));assert.equal(actual.picks,expected,name);if(expected===0)assert.equal(actual.selected,'existing-vessel',name);results.push({name,passed:true,...actual});}
await check('normal mouse click still selects',()=>page.mouse.click(80,80),1);
await check('rotate drag retains selection',async()=>{await page.mouse.move(80,80);await page.mouse.down();await page.mouse.move(220,180,{steps:12});await page.mouse.up();},0);
await check('drag out and back retains selection',async()=>{await page.mouse.move(80,80);await page.mouse.down();await page.mouse.move(220,180,{steps:8});await page.mouse.move(80,80,{steps:8});await page.mouse.up();},0);
await check('right mouse pan retains selection',async()=>{await page.mouse.move(80,80);await page.mouse.down({button:'right'});await page.mouse.move(220,180,{steps:8});await page.mouse.up({button:'right'});},0);
await check('modifier pan retains selection',async()=>{await page.keyboard.down('Shift');await page.mouse.move(80,80);await page.mouse.down();await page.mouse.move(120,120,{steps:8});await page.mouse.up();await page.keyboard.up('Shift');},0);
await check('release outside captured canvas retains selection',async()=>{await page.mouse.move(80,80);await page.mouse.down();await page.mouse.move(850,590,{steps:10});await page.mouse.up();},0);
await check('wheel while held suppresses selection',async()=>{await page.mouse.move(80,80);await page.mouse.down();await page.mouse.wheel(0,100);await page.mouse.up();},0);
await check('touch tap selects',()=>page.touchscreen.tap(80,80),1);
const cdp=await page.context().newCDPSession(page);
await check('one-finger touch rotation retains selection',async()=>{
 await cdp.send('Input.dispatchTouchEvent',{type:'touchStart',touchPoints:[{x:80,y:80,id:1}]});
 await cdp.send('Input.dispatchTouchEvent',{type:'touchMove',touchPoints:[{x:200,y:180,id:1}]});
 await cdp.send('Input.dispatchTouchEvent',{type:'touchEnd',touchPoints:[]});
},0);
await check('two-finger pinch retains selection',async()=>{
 await cdp.send('Input.dispatchTouchEvent',{type:'touchStart',touchPoints:[{x:80,y:80,id:1},{x:180,y:80,id:2}]});
 await cdp.send('Input.dispatchTouchEvent',{type:'touchMove',touchPoints:[{x:50,y:80,id:1},{x:210,y:80,id:2}]});
 await cdp.send('Input.dispatchTouchEvent',{type:'touchEnd',touchPoints:[]});
},0);
await check('cancelled touch does not select',async()=>{
 await cdp.send('Input.dispatchTouchEvent',{type:'touchStart',touchPoints:[{x:80,y:80,id:1}]});
 await cdp.send('Input.dispatchTouchEvent',{type:'touchCancel',touchPoints:[]});
},0);
await check('next click after cancelled touch still works',()=>page.mouse.click(80,80),1);
await check('disposed binding cannot select',async()=>{await page.evaluate(()=>window.cleanup());await page.mouse.click(80,80);},0);
const report={browser:'Chromium',scope:'Real mouse and touch input against production gesture binding, with camera-style pointer capture. Full atlas rendering and deployment not exercised.',passed:results.length,failed:0,results};
await writeFile(new URL('./browser-results.json',import.meta.url),JSON.stringify(report,null,2)+'\n');
console.log(JSON.stringify(report,null,2));
await browser.close();
