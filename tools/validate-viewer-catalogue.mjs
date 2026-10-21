import fs from 'node:fs';
import path from 'node:path';
import assert from 'node:assert/strict';
import crypto from 'node:crypto';
import { performance } from 'node:perf_hooks';
import { gzipSync } from 'node:zlib';
import { createServer } from 'vite';

const root = path.resolve(import.meta.dirname,'..');
const pointer = JSON.parse(fs.readFileSync(root+'/src/viewerCatalogueAsset.json','utf8'));
const fullText = fs.readFileSync(root+'/public/anatomy/manifest.json','utf8');
const viewerText = fs.readFileSync(root+'/public/anatomy/'+pointer.file,'utf8');
const full = JSON.parse(fullText), viewer = JSON.parse(viewerText);
assert.equal(crypto.createHash('sha256').update(viewerText).digest('hex'),pointer.sha256);
assert.equal(viewer.release,pointer.release);
assert.equal(viewer.release,JSON.parse(fs.readFileSync(root+'/package.json')).version);
const server = await createServer({root,server:{middlewareMode:true},appType:'custom'});
const report = {release:viewer.release,structures:viewer.structures.length,checks:[],measurements:{}};
try {
  const catalogue = await server.ssrLoadModule('/src/catalogue.ts');
  const {createViewerCatalogue} = await server.ssrLoadModule('/src/viewerCatalogue.ts');
  const {structureDependencies} = await server.ssrLoadModule('/src/stagedLoading.ts');
  const presets = await server.ssrLoadModule('/src/presets.ts');
  const {makeDsaRun} = await server.ssrLoadModule('/src/dsa.ts');
  const {flowGraphSource} = await server.ssrLoadModule('/src/flowGeometry.ts');
  assert.deepEqual(viewer,createViewerCatalogue(full));
  const originalFetch=globalThis.fetch;
  try {
    const requests=[];
    globalThis.fetch=async (url,options)=>{requests.push({url,options});return new Response(url.endsWith('manifest.json')?fullText:viewerText)};
    assert.deepEqual(await catalogue.loadCatalogue(),viewer);
    assert(requests[0].url.endsWith('/anatomy/'+pointer.file));
    assert.equal(requests[0].options.cache,'default');
    assert.deepEqual(await catalogue.loadCatalogue('manifest.json'),full);
    assert.equal(requests[1].options.cache,'no-cache');
    globalThis.fetch=async()=>new Response('',{status:404});
    await assert.rejects(catalogue.loadCatalogue(),/404/);
    globalThis.fetch=async()=>new Response(JSON.stringify({...viewer,release:'unexpected-release'}));
    await assert.rejects(catalogue.loadCatalogue(),/release does not match/);
  } finally {globalThis.fetch=originalFetch}
  report.checks.push('Startup URL, caching, explicit full-manifest access, HTTP failure and release-mismatch handling');
  const maps = [full,viewer].map(m=>new Map(m.structures.map(s=>[s.id,s])));
  const subtrees = maps.map(catalogue.geometrySubtrees);
  assert.deepEqual(subtrees[0],subtrees[1]);
  assert.deepEqual(catalogue.segmentGeometryMembers(full.structures),catalogue.segmentGeometryMembers(viewer.structures));
  assert.deepEqual(catalogue.uniqueVesselCounts(full.structures),catalogue.uniqueVesselCounts(viewer.structures));
  report.checks.push('Same geometry groups, subtrees and vessel counts');
  for (const s of full.structures) {
    const row=maps[1].get(s.id);
    assert.deepEqual(row.description,s.description,s.id+' description');
    assert.deepEqual(row.aliases,s.aliases,s.id+' search aliases');
    assert.deepEqual(row.landmark,s.landmark,s.id+' landmark');
    assert.deepEqual(row.surfaceAnchor,s.surfaceAnchor,s.id+' brain anchor');
    assert.deepEqual(catalogue.focusGeometryMembers(full,s.id),catalogue.focusGeometryMembers(viewer,s.id),s.id+' focus');
    assert.deepEqual(structureDependencies(s.id,maps[0],subtrees[0]),structureDependencies(s.id,maps[1],subtrees[1]),s.id+' dependencies');
  }
  for (const q of ['ICA','ophthalmic','optic canal','PICA','MCA','vertebral','cavernous','superior orbital fissure','vein','anterior cerebral']) {
    assert.deepEqual(catalogue.searchStructures(full.structures,q).map(s=>s.id),catalogue.searchStructures(viewer.structures,q).map(s=>s.id));
  }
  report.checks.push('Same descriptions, aliases, landmarks, anchors, focus and dependencies for every structure; representative search results match');
  assert.deepEqual(full.relationships,viewer.relationships);
  assert.equal(flowGraphSource(full),flowGraphSource(viewer));
  const flow=JSON.parse(fs.readFileSync(root+'/public/anatomy/dsa-flow.json','utf8'));
  for(const p of presets.ANATOMICAL_PRESETS) for(const side of ['left','right','both']) {
    assert.deepEqual(presets.presetVesselIds(full,p.id,side),presets.presetVesselIds(viewer,p.id,side));
    assert.deepEqual(makeDsaRun(full,p.id,side,flow),makeDsaRun(viewer,p.id,side,flow),p.id+' '+side+' DSA');
  }
  report.checks.push('Same relationships, flow validation graph and all 15 preset/side DSA runs');
  for (const side of ['left','right','both']) {
    const ids=presets.presetVesselIds(viewer,'vertebrobasilar',side);
    const visible=presets.presetVisibility(viewer,new Map(),ids);
    const run=makeDsaRun(viewer,'vertebrobasilar',side,flow);
    for (const vesselSide of ['left','right']) {
      const expected=side==='both'||side===vesselSide;
      const pica=viewer.structures.filter(s=>s.asset&&s.system==='artery'&&s.displayGroup!=='anastomoses'&&s.id.startsWith('artery.posterior.pica_')&&s.side===vesselSide);
      assert(pica.length>=11,'PICA segments and branches must be present in catalogue');
      for (const row of pica) {
        assert.equal(ids.includes(row.id),expected,side+' bookmark '+row.id);
        assert.equal(visible.get(row.id),expected?'on':'off',side+' visibility '+row.id);
        assert.equal(run.arteries.includes(row.id),expected,side+' DSA '+row.id);
        assert.equal(presets.injectionPreset(row.id),'vertebrobasilar');
      }
      for(let i=1;i<=5;i++)assert(pica.some(s=>s.id===`artery.posterior.pica_${vesselSide}.segment.p${i}`));
    }
  }
  report.checks.push('Vertebrobasilar presets include all PICA segments and branches for the selected side; opposite PICA excluded from unilateral bookmarks and DSA');

  function parseMedian(text) {
    for(let i=0;i<5;i++) JSON.parse(text);
    const times=[];
    for(let i=0;i<25;i++){const start=performance.now();JSON.parse(text);times.push(performance.now()-start)}
    return times.sort((a,b)=>a-b)[12];
  }
  const compactFull=JSON.stringify(full);
  report.measurements={
    comparison:'Full compact catalogue versus startup catalogue, same release and geometry',
    full:{bytes:Buffer.byteLength(compactFull),gzipBytes:gzipSync(compactFull,{level:9}).length,nodeParseMedianMs:parseMedian(compactFull)},
    viewer:{bytes:Buffer.byteLength(viewerText),gzipBytes:gzipSync(viewerText,{level:9}).length,nodeParseMedianMs:parseMedian(viewerText)},
    parseSamples:25,
    limitation:'Controlled Node parsing benchmark; not a mobile browser loading time or Core Web Vitals result',
  };
  fs.writeFileSync(root+'/docs/revision'+viewer.release.split('.').at(-1)+'-catalogue-validation.json',JSON.stringify(report,null,2)+'\n');
  console.log(JSON.stringify(report,null,2));
} finally {await server.close()}
