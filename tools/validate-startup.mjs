import fs from 'node:fs';
import path from 'node:path';
import assert from 'node:assert/strict';
import {createServer} from 'vite';
import {explanationMarkup, explanationSummary} from '../src/explanationMarkup.ts';

const root=path.resolve(import.meta.dirname,'..');
const html=fs.readFileSync(root+'/dist/index.html','utf8');
assert(html.includes(explanationMarkup()),'Explanation must be in the served HTML, not injected only by the browser');
assert(!html.includes('%ATLAS_'));
const intro=html.slice(html.indexOf('<main'),html.indexOf('</main>'));
const approved=JSON.parse(fs.readFileSync(root+'/src/explanationContent.json','utf8')).intro;
assert(intro.includes(approved.tagline));assert(intro.includes(approved.description));
assert(!/Jeremy Lynch|Sean McIlhone|consultant|King’s College|Background/.test(intro));
assert(!intro.includes('The skull loads first'));
assert(intro.indexOf(approved.description)<intro.indexOf('Loading 3D anatomy…'));
assert.match(html,/<html[^>]+data-theme="dark"/);
assert(html.includes('background:#111317'));
assert.match(intro,/<progress[^>]+id="atlas-startup-progress"[^>]+value="0"/);
assert.match(intro,/<output[^>]+id="atlas-startup-percent"[^>]*>0%<\/output>/);
assert.match(html,/<main[^>]+id="atlas-fallback"[^>]*>/);
assert(!html.match(/<main[^>]+id="atlas-fallback"[^>]*>/)[0].includes('hidden'));
assert.match(html,/<div[^>]+id="root"[^>]+inert[^>]+aria-hidden="true"/);
assert(html.indexOf('</main>')<html.indexOf('id="root"'),'React must not own the fallback');
assert(html.includes('<noscript>'));
assert(!/googlebot|navigator\.userAgent/i.test(fs.readFileSync(root+'/src/startup.ts','utf8')));

// Exercise asynchronous-state and focus behaviour against the actual controller.
// Rendering itself is tested separately; this does not pretend to provide WebGL.
const oldDocument=globalThis.document;
const panel={hidden:false,contains:node=>node?.inPanel===true};
const viewer={inert:true,attributes:new Map([['aria-hidden','true']]),removeAttribute(name){this.attributes.delete(name)},setAttribute(name,value){this.attributes.set(name,value)},focus(){this.focused=true}};
const progress={value:0,hidden:false,removeAttribute(name){if(name==='hidden')this.hidden=false}};
const status={textContent:'Loading'},retry={hidden:true},percent={textContent:'0%',hidden:false},meter={hidden:false};
const elements={'atlas-fallback':panel,root:viewer,'atlas-startup-status':status,'atlas-startup-progress':progress,'atlas-startup-retry':retry,'atlas-startup-percent':percent,'atlas-startup-meter':meter};
globalThis.document={getElementById:id=>elements[id]??null,activeElement:{inPanel:true},documentElement:{dataset:{}}};
const server=await createServer({root,server:{middlewareMode:true},appType:'custom'});
try {
  const startup=await server.ssrLoadModule('/src/startup.ts');
  startup.reportStartupProgress(48);
  assert.equal(progress.value,48);assert.equal(percent.textContent,'48%');
  startup.reportStartupProgress(150);assert.equal(progress.value,99);assert.equal(percent.textContent,'99%');
  startup.reportStartupProgress(48); assert.equal(panel.hidden,false); assert.equal(viewer.inert,true);
  startup.reportStartupReady();
  assert.equal(panel.hidden,true); assert.equal(viewer.inert,false); assert.equal(viewer.attributes.has('aria-hidden'),false);assert.equal(viewer.focused,true);
  const originalError=console.error;
  try {console.error=()=>{};startup.reportStartupFailure(new Error('rendering failed'))} finally {console.error=originalError}
  assert.equal(panel.hidden,false);assert.equal(viewer.inert,true);assert.equal(retry.hidden,false);assert.equal(progress.hidden,true);assert.equal(percent.hidden,true);assert.equal(meter.hidden,true);
  startup.reportStartupReady();startup.reportStartupProgress(90);
  assert.equal(panel.hidden,false,'A late success callback must not hide a failed viewer');assert.equal(progress.hidden,true);
  const {About}=await server.ssrLoadModule('/src/App.tsx');
  const {createElement}=await import('react');const {renderToStaticMarkup}=await import('react-dom/server');
  const manifest=JSON.parse(fs.readFileSync(root+'/public/anatomy/manifest.json','utf8'));
  const about=renderToStaticMarkup(createElement(About,{manifest,onClose:()=>{}}));
  assert(about.includes(explanationSummary));assert(about.includes('Jeremy Lynch'));assert(about.includes('King’s College Hospital'));assert(about.includes('consultant'));
  for(const section of JSON.parse(fs.readFileSync(root+'/src/explanationContent.json','utf8')).sections)assert(about.includes(section.heading));
  fs.writeFileSync(root+'/docs/revision'+manifest.release.split('.').at(-1)+'-startup-validation.json',JSON.stringify({release:manifest.release,initialHtmlContent:'passed',reactRootIsolation:'passed',noJavascriptExplanation:'present in initial HTML',controllerChecks:['loading/progress','success hides fallback and enables viewer','focus transfer','failure restores fallback and retry','late success cannot hide a failed viewer'],approvedIntro:'passed; no author biography or loading-order explanation',darkInitialTheme:'passed',measuredProgressPercentage:'passed; clamped with progress and hidden on failure',sharedAboutContent:'passed; author name and professional background preserved',limitation:'Controller transitions use a DOM fixture. Full 3D success requires a WebGL-capable browser; the actual unsupported-WebGL case was checked separately.'},null,2)+'\n');
  console.log('Passed: initial HTML/no-JS content, React isolation, progress, success, focus, failure, late-callback protection and shared About content.');
}finally{await server.close();globalThis.document=oldDocument}
