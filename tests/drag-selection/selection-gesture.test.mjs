import { test } from 'node:test';
import assert from 'node:assert/strict';
import { SelectionGesture } from './selectionGesture.mjs';
const sample = (values = {}) => ({pointerId:1,clientX:20,clientY:20,button:0,buttons:1,isPrimary:true,pointerType:'mouse',ctrlKey:false,metaKey:false,shiftKey:false,altKey:false,...values});
test('a click and a slightly jittery tap select',()=>{
 for(const pointerType of ['mouse','touch','pen']){
  const g=new SelectionGesture();g.pointerDown(sample({pointerType}));
  assert.equal(g.pointerUp(sample({pointerType,clientX:22,buttons:0})),true);
 }
});
test('rotation, pan and a drag returning to its origin do not select',()=>{
 for(const endX of [20,80]){
  const g=new SelectionGesture();g.pointerDown(sample());g.pointerMove(sample({clientX:80}));
  assert.equal(g.pointerUp(sample({clientX:endX,buttons:0})),false);
 }
});
test('release movement is checked even if no move event was received',()=>{
 const g=new SelectionGesture();g.pointerDown(sample());assert.equal(g.pointerUp(sample({clientX:80})),false);
});
test('right and middle mouse gestures cannot select',()=>{
 for(const button of [1,2]){const g=new SelectionGesture();g.pointerDown(sample({button}));assert.equal(g.pointerUp(sample({button})),false);}
});
test('modifier pan clicks and later modifiers do not select',()=>{
 for(const key of ['shiftKey','ctrlKey','metaKey','altKey']){
  const g=new SelectionGesture();g.pointerDown(sample({[key]:true}));assert.equal(g.pointerUp(sample()),false);
  g.pointerDown(sample());assert.equal(g.pointerUp(sample({[key]:true})),false);
 }
});
test('pinching or two-finger panning stays suppressed until all fingers lift',()=>{
 const g=new SelectionGesture();g.pointerDown(sample({pointerType:'touch'}));g.pointerDown(sample({pointerId:2,pointerType:'touch',isPrimary:false}));
 assert.equal(g.pointerUp(sample({pointerId:2,pointerType:'touch',isPrimary:false})),false);
 assert.equal(g.pointerUp(sample({pointerType:'touch'})),false);
 g.pointerDown(sample({pointerType:'touch'}));assert.equal(g.pointerUp(sample({pointerType:'touch'})),true);
});
test('cancelled gestures and window focus loss never select',()=>{
 for(const cancel of [g=>g.pointerCancel({pointerId:1}),g=>g.reset(),g=>g.invalidate()]){
  const g=new SelectionGesture();g.pointerDown(sample());cancel(g);assert.equal(g.pointerUp(sample()),false);
 }
});
test('a release without a matching press cannot select',()=>{
 const g=new SelectionGesture();assert.equal(g.pointerUp(sample()),false);g.pointerDown(sample());assert.equal(g.pointerUp(sample({pointerId:2})),false);
});
import {bindSelectionGesture} from './selectionGesture.mjs';
class Canvas extends EventTarget {
 ownerDocument={defaultView:new EventTarget()};
 getBoundingClientRect(){return {left:10,top:10,right:100,bottom:100};}
}
function send(canvas,type,values={}){const ev=new Event(type);Object.assign(ev,sample(values));canvas.dispatchEvent(ev);}
test('production DOM binding ignores drag release, then permits the next click',()=>{
 const c=new Canvas();let picks=0;const dispose=bindSelectionGesture(c,()=>picks++);
 send(c,'pointerdown');send(c,'pointermove',{clientX:80});send(c,'pointerup',{clientX:80,buttons:0});assert.equal(picks,0);
 send(c,'pointerdown');send(c,'pointerup',{buttons:0});assert.equal(picks,1);
 dispose();send(c,'pointerdown');send(c,'pointerup');assert.equal(picks,1);
});
test('production DOM binding rejects outside release and capture loss',()=>{
 const c=new Canvas();let picks=0;const dispose=bindSelectionGesture(c,()=>picks++);
 send(c,'pointerdown',{clientX:98});send(c,'pointerup',{clientX:102});assert.equal(picks,0);
 send(c,'pointerdown');send(c,'lostpointercapture');send(c,'pointerup');assert.equal(picks,0);dispose();
});
test('production DOM binding cancels selection on wheel and window blur',()=>{
 const c=new Canvas();let picks=0;const dispose=bindSelectionGesture(c,()=>picks++);
 send(c,'pointerdown');c.dispatchEvent(new Event('wheel'));send(c,'pointerup');assert.equal(picks,0);
 send(c,'pointerdown');c.ownerDocument.defaultView.dispatchEvent(new Event('blur'));send(c,'pointerup');assert.equal(picks,0);dispose();
});
