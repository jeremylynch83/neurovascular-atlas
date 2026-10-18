import {createRequire}from'node:module';import fs from'node:fs';import path from'node:path';
const require=createRequire(import.meta.url),{chromium}=require(process.env.CODEX_PRIMARY_RUNTIME_NODE_MODULES+'/playwright');
const root=new URL('../../',import.meta.url).pathname,{createServer}=await import(root+'node_modules/vite/dist/node/index.js');
const work=path.resolve(process.argv[2]),selected=process.argv[3]??'accepted';
const files={'/brain-comparison/old.glb':path.join(work,'baseline/public/anatomy/models/brain-context.glb'),'/brain-comparison/new.glb':path.join(work,selected,'brain-0.01.glb'),'/brain-comparison/manifest.json':path.join(work,'baseline/public/anatomy/manifest.json'),'/brain-comparison/trial.json':path.join(work,selected,'trial-0.01.json')};
const server=await createServer({root,server:{host:'127.0.0.1',port:8811},plugins:[{name:'brain-comparison-inputs',configureServer(server){server.middlewares.use((req,res,next)=>{const file=files[req.url];if(!file)return next();res.setHeader('Content-Type',file.endsWith('.json')?'application/json':'model/gltf-binary');fs.createReadStream(file).pipe(res)})}}]});await server.listen();
const browser=await chromium.launch({executablePath:process.env.ATLAS_TEST_CHROMIUM,headless:true,args:['--no-sandbox','--disable-dev-shm-usage','--use-gl=angle','--use-angle=swiftshader','--enable-unsafe-swiftshader']});
try{
 const page=await browser.newPage({viewport:{width:1000,height:605}});page.on('pageerror',e=>console.error(e));
 await page.goto('http://127.0.0.1:8811/tests/brain-simplification/compare.html');await page.waitForFunction(()=>window.comparisonReady,{},{timeout:120000});
 for(const[name,kind,direction]of [['cerebellum-posterior','cerebellum',[0,-1,.15]],['cerebellum-inferior','cerebellum',[0,-.2,-1]],['detail','detail',[1,-1,.3]],['cortex','cerebral_cortex',[1,-.3,.15]]]){
  await page.evaluate(([k,d])=>window.renderComparison(k,d),[kind,direction]);await page.screenshot({path:path.join(work,name+'.png')});console.log('Rendered',name);
 }
}finally{await browser.close();await server.close()}
