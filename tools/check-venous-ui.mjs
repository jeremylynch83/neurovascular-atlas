import fs from 'node:fs';
import assert from 'node:assert/strict';
import path from 'node:path';
import {pathToFileURL} from 'node:url';
const deps=process.env.VENOUS_QA_MODULES;
const {build}=await import(deps?pathToFileURL(path.resolve(deps,'esbuild/lib/main.js')).href:'esbuild');
const {JSDOM}=await import(deps?pathToFileURL(path.resolve(deps,'jsdom/lib/api.js')).href:'jsdom');
const dom=new JSDOM('<!doctype html><div id="app"></div>',{url:'http://localhost/'});
Object.assign(globalThis,{window:dom.window,document:dom.window.document,HTMLElement:dom.window.HTMLElement,MouseEvent:dom.window.MouseEvent,Event:dom.window.Event,IS_REACT_ACT_ENVIRONMENT:true});
window.matchMedia=()=>({matches:true,addEventListener(){},removeEventListener(){}});
await build({entryPoints:['src/App.tsx'],bundle:true,platform:'node',format:'esm',packages:'external',jsx:'automatic',outfile:'tools/.qa/App-ui.mjs',plugins:[{name:'render-fixture',setup(b){b.onLoad({filter:/\/engine\.ts$/},()=>({contents:`
export class AnatomyEngine {
 constructor(container,manifest,onSelect){this.manifest=manifest;this.onSelect=onSelect;globalThis.engineFixture=this;}
 async load(cb){cb(100)} start(){} dispose(){} setTheme(){} setClip(){} setView(){}
 setLayers(l){this.layers=l} setSelected(id){this.selected=id} setHiddenIds(ids){this.hidden=new Set(ids)}
 hasGeometry(id){return !!this.manifest.structures.find(s=>s.id===id)?.asset} focus(id){this.focused=id}
}`,loader:'js'}))}}]});
const React=await import('react');const {createRoot}=await import('react-dom/client');const {App}=await import('./.qa/App-ui.mjs');const {act}=React;
const manifest=JSON.parse(fs.readFileSync('public/anatomy/manifest.json'));const root=createRoot(document.getElementById('app'));
await act(async()=>root.render(React.createElement(App,{manifest})));
const click=async(el)=>{assert(el);await act(async()=>el.dispatchEvent(new MouseEvent('click',{bubbles:true})))};
const button=(label)=>[...document.querySelectorAll('button')].find(b=>b.textContent===label);
assert(document.querySelector('#anatomy-panel-body').hidden);await click(button('Layers and anatomy'));
assert(document.querySelector('[aria-label="Veins: off"]'));
await click(button('Anatomy'));await click(document.querySelector('[aria-label="Expand Veins"]'));await click(document.querySelector('[aria-label="Expand Dural venous sinuses"]'));
const name=(text)=>[...document.querySelectorAll('.tree-name')].find(b=>b.querySelector('span')?.textContent===text);
await click(document.querySelector('[aria-label="Expand Confluence of sinuses"]'));await click(name('Straight sinus'));
assert.equal(globalThis.engineFixture.layers.vein,'on');assert.equal(globalThis.engineFixture.focused,'vein.straight');assert(document.querySelector('#structure-panel-body').hidden);
await click(document.querySelector('.detail .panel-title'));assert(!document.querySelector('#structure-panel-body').hidden);
const body=document.querySelector('#structure-panel-body');assert(body.textContent.includes('Receives from:'));assert(body.textContent.includes('Drains to:'));
const galen=[...body.querySelectorAll('a')].find(a=>a.getAttribute('href')==='#structure-vein.galen');assert(galen);await click(galen);
assert.equal(globalThis.engineFixture.selected,'vein.galen');assert.equal(globalThis.engineFixture.focused,'vein.galen');assert(!document.querySelector('#structure-panel-body').hidden);
await click(button('Hide'));assert(globalThis.engineFixture.hidden.has('vein.internal_cerebral.right'));assert(globalThis.engineFixture.hidden.has('vein.thalamostriate.left'));assert(!globalThis.engineFixture.hidden.has('vein.internal_jugular.right'));await click(button('Show'));
assert(!globalThis.engineFixture.hidden.has('vein.internal_cerebral.right'));
// An actual tree selection with no notes omits the entire Description section.
await click(document.querySelector('[aria-label="Expand Posterior fossa and spinal veins"]'));
await click(document.querySelector('[aria-label="Expand Superior petrosal vein right"]'));
await click(name('Transverse pontine vein right'));assert(!document.querySelector('.detail-body').textContent.includes('Description'));
await act(async()=>root.unmount());
const report={mobilePanelsInitiallyCollapsed:true,selectingVeinRevealsLayer:true,drainageDirectionLabels:true,descriptionLinksSelectAndFocus:true,selectionPreservesExpandedPanel:true,hideShowIncludesDescendants:true,missingDescriptionOmitted:true,scope:'Actual React components and event handlers in jsdom; rendering engine fixture, not a browser/GPU test'};
fs.writeFileSync('docs/validation/venous-ui-v0.9.0.json',JSON.stringify(report,null,2)+'\n');console.log(report);
