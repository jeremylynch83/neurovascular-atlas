import{createRequire}from'node:module';import{writeFile}from'node:fs/promises';import assert from'node:assert/strict';
const require=createRequire(import.meta.url),{chromium}=require(process.env.CODEX_PRIMARY_RUNTIME_NODE_MODULES?process.env.CODEX_PRIMARY_RUNTIME_NODE_MODULES+'/playwright':'playwright');
const root=new URL('../../',import.meta.url).pathname,{preview}=await import(root+'node_modules/vite/dist/node/index.js'),server=await preview({root,preview:{host:'127.0.0.1',port:8800}});
const browser=await chromium.launch({executablePath:process.env.ATLAS_TEST_CHROMIUM,headless:true,args:['--no-sandbox','--disable-dev-shm-usage','--use-gl=angle','--use-angle=swiftshader','--enable-unsafe-swiftshader']});
const report={passed:false,errors:[],workerUrls:[],tests:[]};
try{
 const page=await browser.newPage({viewport:{width:1000,height:700},deviceScaleFactor:.15,reducedMotion:'reduce'});
 page.on('pageerror',e=>report.errors.push(e.message));page.on('console',m=>{if(m.type()==='error')report.errors.push(m.text())});page.on('worker',worker=>report.workerUrls.push(worker.url()));
 await page.goto('http://127.0.0.1:8800',{waitUntil:'domcontentloaded'});
 await page.waitForFunction(()=>document.querySelector('[aria-label="Anatomical presets"]')?.disabled===false,{},{timeout:120000});
 assert.equal(await page.locator('.loading').count(),0);await page.locator('.left-panel > .panel-title').click();
 for(const id of ['bone','artery']){const row=page.locator(`.tree-row[data-structure-id="${id}"]`);assert.equal(await row.getAttribute('aria-busy'),'false');assert.equal(await row.locator('.structure-retry').count(),0)}
 report.tests.push('Production bone/artery loading completes without errors or an overlay');
 await page.getByRole('button',{name:'Anatomical presets',exact:true}).click();await page.getByRole('button',{name:'MMA, left',exact:true}).click();
 await page.waitForFunction(()=>document.querySelector('[aria-label="DSA mode"]')?.disabled===false,{},{timeout:180000});
 assert(report.workerUrls.some(url=>/\/assets\/geometryWorker-[^/]+\.js$/.test(url)));assert.equal(await page.locator('.structure-retry').count(),0);
 report.tests.push('Bundled geometry worker loads deferred vascular data and enables DSA');
 assert.equal(await page.evaluate(()=>document.querySelector('canvas').getContext('webgl2').isContextLost()),false);
 report.tests.push('Production canvas retains its WebGL context');assert.deepEqual(report.errors,[]);report.passed=true;
}finally{await writeFile(root+'docs/staged-loading-production.json',JSON.stringify(report,null,2)+'\n');await browser.close();await new Promise(r=>server.httpServer.close(r))}
console.log(report);
