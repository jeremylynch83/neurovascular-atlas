import fs from 'node:fs';
import assert from 'node:assert/strict';
import {spawn} from 'node:child_process';
import {chromium} from '/opt/codex/runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright/index.mjs';
const server=spawn(process.execPath,['node_modules/vite/bin/vite.js','preview','--host','127.0.0.1','--port','5177'],{stdio:'ignore'});
let browser;
try{
  for(let i=0;i<50;i++){try{await fetch('http://127.0.0.1:5177');break;}catch{await new Promise(r=>setTimeout(r,100));}}
  browser=await chromium.launch({executablePath:'/workspace/scratch/c716cd2ac4cf/browser_runtime133/chromium',headless:true,env:{...process.env,LD_LIBRARY_PATH:'/workspace/scratch/c716cd2ac4cf/browser_runtime133'},args:['--no-sandbox','--use-gl=angle','--use-angle=swiftshader','--enable-unsafe-swiftshader','--in-process-gpu','--disable-dev-shm-usage']});
  const manifest=await (await fetch('http://127.0.0.1:5177/anatomy/manifest.json')).json();assert.equal(manifest.release,'0.9.21');
  const page=await browser.newPage({viewport:{width:1400,height:1050}});const errors=[],warnings=[];
  page.on('pageerror',e=>errors.push(e.message));page.on('console',m=>{if(m.type()==='error'||m.type()==='warning')warnings.push(m.text());});
  await page.goto('http://127.0.0.1:5177');await page.locator('.loading').waitFor({state:'hidden',timeout:180000});assert.equal(await page.locator('.load-error').count(),0);
  const search=page.getByRole('textbox',{name:'Search anatomy'});
  for(const side of ['left','right']){
    await search.fill('Posterior spinal '+side);const result=page.locator('.search-results button').filter({hasText:new RegExp('Posterior spinal.*'+side,'i')});await result.first().click();
    const detail=page.locator('.detail-body');if(!await detail.isVisible())await page.locator('.detail .panel-title').click();
    assert.match(await detail.innerText(),/PICA|posterior inferior cerebellar/i);await page.getByRole('button',{name:'Focus',exact:true}).click();
    await page.screenshot({path:`docs/validation/posterior-spinal-${side}-browser-v0.9.21.png`});
  }
  await search.fill('Upper cervical cord');await page.locator('.search-results button').first().click();assert.match(await page.locator('.detail-body').innerText(),/illustrative/i);
  for (const term of ['PCA P2-P3 left','Basal vein','Lateral mesencephalic vein','Vein of Galen']) { await search.fill(term); const results=page.locator('.search-results button'); assert(await results.count()>0,term); await results.first().click(); await page.getByRole('button',{name:'Focus',exact:true}).click(); }
  await search.fill('Pons right');await page.locator('.search-results button').first().click();await page.getByRole('button',{name:'Focus',exact:true}).click();await page.screenshot({path:'docs/validation/pontine-browser-v0.9.21.png'});
  assert.equal(errors.length,0,errors.join('\n'));assert(!warnings.some(s=>/Could not resolve|GL_INVALID|context lost/.test(s)),warnings.join('\n'));
  fs.writeFileSync('docs/validation/regional-browser-v0.9.21.json',JSON.stringify({release:'0.9.21',productionBuild:true,loaded:true,manifestReleaseCorrect:true,pontineSearchAndFocus:true,PcaBasalLmvGalenSearchAndFocus:true,posteriorSpinalSearchSelectionAndParentLinks:true,illustrativeCord:true,pageErrors:errors,warnings},null,2)+'\n');console.log('Posterior browser checks passed');
}finally{await browser?.close();server.kill();}
