import {createRequire} from 'node:module';
import {spawn} from 'node:child_process';
import {writeFile} from 'node:fs/promises';
import assert from 'node:assert/strict';
const require=createRequire(import.meta.url);
const {chromium}=require(process.env.CODEX_PRIMARY_RUNTIME_NODE_MODULES ? process.env.CODEX_PRIMARY_RUNTIME_NODE_MODULES+'/playwright' : 'playwright');
const base=process.env.ATLAS_APP_DIR || new URL('../../',import.meta.url).pathname;
const server=spawn('python3',[base+'run.py','--port','8788','--no-open'],{stdio:['ignore','pipe','ignore']});
await new Promise((resolve,reject)=>{server.stdout.once('data',resolve);server.once('exit',code=>reject(new Error('Server exited '+code)));});
let browser;
try {
 browser=await chromium.launch({headless:true,executablePath:process.env.ATLAS_TEST_CHROMIUM,args:['--no-sandbox','--disable-dev-shm-usage','--use-gl=angle','--use-angle=swiftshader','--enable-unsafe-swiftshader']});
 const page=await browser.newPage({viewport:{width:1280,height:900},deviceScaleFactor:0.25,hasTouch:true});
 const errors=[],warnings=[],loaded=[];
 page.on('pageerror',error=>errors.push(error.message));
 page.on('console',message=>{if(message.type()==='error')errors.push(message.text());if(message.type()==='warning'&&message.text().includes('resolve'))warnings.push(message.text());});
 page.on('response',response=>{if(response.url().includes('.glb')){loaded.push({url:response.url().split('/').pop(),status:response.status()});}else if(response.status()>=400)errors.push(response.url()+' '+response.status());});
 await page.goto('http://127.0.0.1:8788',{waitUntil:'domcontentloaded'});
 await page.waitForFunction(()=>document.querySelector('[aria-label="Anatomical presets"]')?.disabled===false,{},{timeout:180000});
 assert.equal(await page.locator('.load-error').count(),0);
 if(loaded.length<5)await page.waitForEvent('response',{predicate:r=>r.url().includes('brain-context.glb'),timeout:180000});
 assert.equal(loaded.length,5);assert(loaded.every(x=>x.status===200));
 assert.deepEqual(errors,[]);assert.deepEqual(warnings,[]);
 await page.getByRole('textbox',{name:'Search anatomy'}).fill('External carotid artery right');
 await page.locator('.search-results button').first().click();
 const selected=await page.locator('.structure-title').textContent();
 assert.equal(selected,'External carotid artery right');
 const focus=page.getByRole('button',{name:'Focus',exact:true});
 await focus.click();assert.equal(await focus.getAttribute('aria-pressed'),'true');
 const tests=[];
 async function check(name,action){await action();assert.equal(await page.locator('.structure-title').textContent(),selected,name);assert.equal(await focus.getAttribute('aria-pressed'),'true',name);tests.push({name,passed:true});}
 await check('full atlas rotation retains selected vessel and Focus',async()=>{await page.mouse.move(600,280);await page.mouse.down();await page.mouse.move(850,450,{steps:12});await page.mouse.up();});
 await check('full atlas right-button pan retains selected vessel and Focus',async()=>{await page.mouse.move(600,280);await page.mouse.down({button:'right'});await page.mouse.move(730,400,{steps:8});await page.mouse.up({button:'right'});});
 await check('full atlas out-and-back drag retains selected vessel and Focus',async()=>{await page.mouse.move(600,280);await page.mouse.down();await page.mouse.move(850,450,{steps:8});await page.mouse.move(600,280,{steps:8});await page.mouse.up();});
 const report={passed:true,productionAppLoaded:true,modelAssets:loaded,unresolvedNodes:warnings,errors,tests,scope:'Prebuilt production app on Chromium with software WebGL; full scene startup, search selection, Focus and mouse rotate/pan. Anatomical acceptance not assessed.'};
 await writeFile(base+'docs/full-atlas-runtime.json',JSON.stringify(report,null,2)+'\n');
 console.log(JSON.stringify(report));
} finally {if(browser)await browser.close();server.kill();}
