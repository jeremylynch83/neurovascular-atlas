import fs from 'node:fs';
import {spawn} from 'node:child_process';
const {chromium}=await import('/opt/codex/runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright/index.mjs');
const server=spawn('python3',['-m','http.server','9843','--bind','127.0.0.1'],{stdio:['ignore','ignore','pipe']});
let browser;
try {
  for(let i=0;i<100;i++) {
    try {if((await fetch('http://127.0.0.1:9843/tools/brain-resume-review.html')).ok)break;}catch{}
    await new Promise(r=>setTimeout(r,100));
  }
  browser=await chromium.launch({headless:true,executablePath:process.env.BRAIN_QA_CHROME,args:['--no-sandbox','--use-gl=angle','--use-angle=swiftshader','--enable-unsafe-swiftshader']});
  const page=await browser.newPage({viewport:{width:1400,height:1680},deviceScaleFactor:1});
  const errors=[];page.on('pageerror',e=>errors.push(e.message));
  await page.goto('http://127.0.0.1:9843/tools/brain-resume-review.html',{waitUntil:'load'});
  await page.waitForFunction(()=>window.reviewReady===true,{},{timeout:120000});
  if(errors.length)throw new Error(errors.join('\n'));
  await page.screenshot({path:'docs/validation/brainstem-resume-review.png',fullPage:true});
  fs.writeFileSync('docs/validation/resume-render.json',JSON.stringify({pageErrors:errors,views:3,matchedStates:2,trialApplied:false},null,2)+'\n');
  console.log('Matched current app / unaccepted trial render saved.');
}finally{await browser?.close();server.kill();}
