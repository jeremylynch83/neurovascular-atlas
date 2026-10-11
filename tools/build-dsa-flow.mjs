// Automatic authoring step. Ordinary builds reuse data whose geometry and
// anatomical graph hashes match. No Python or new browser dependency needed.
import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import {spawnSync} from 'node:child_process';
import {Triangle,Vector3} from 'three';
import {GLTFLoader} from 'three/examples/jsm/loaders/GLTFLoader.js';
import {MeshoptDecoder} from 'three/examples/jsm/libs/meshopt_decoder.module.js';
import {projectToPath,pointInsideSurface,splitFlowSurface,decodeCoordinates,closedSurfaceError,flowGraphSource,pathPoint} from '../src/flowGeometry.ts';
const root=path.resolve(import.meta.dirname,'..'),base=root+'/public/anatomy/';
const manifest=JSON.parse(fs.readFileSync(base+'manifest.json'));
const surfaces=JSON.parse(fs.readFileSync(base+'dsa-surfaces.json'));
const rows=manifest.structures.filter(s=>s.system==='artery'&&s.asset&&s.displayGroup!=='anastomoses');
const veins=manifest.structures.filter(s=>s.system==='vein'&&s.asset);
const hash=x=>crypto.createHash('sha256').update(x).digest('hex');
const sourceHashes=Object.fromEntries([...new Set([...rows,...veins].map(s=>s.asset.file))].map(file=>[file,hash(fs.readFileSync(base+file))]));
const graphSource=flowGraphSource(manifest),graphHash=hash(graphSource);
const generatorHash=hash(fs.readFileSync(import.meta.filename)+fs.readFileSync(root+'/src/flowGeometry.ts'));
const output=base+'dsa-flow.json';
const only=process.argv.includes('--only')?new Set(process.argv[process.argv.indexOf('--only')+1].split(',')):null;
if(!process.argv.includes('--force')&&fs.existsSync(output)) {
  const old=JSON.parse(fs.readFileSync(output));
  if(old.schema===1&&old.generatorHash===generatorHash&&old.graphHash===graphHash&&JSON.stringify(old.sourceHashes)===JSON.stringify(sourceHashes)){console.log('DSA flow data match the geometry and branch graph.');process.exit(0)}
}
if(Object.entries(sourceHashes).some(([file,h])=>surfaces.sourceHashes[file]!==h)) {
  console.log('Geometry changed: regenerating DSA projection surfaces.');
  const repair=spawnSync(process.execPath,[root+'/tools/build-dsa-surfaces.mjs'],{stdio:'inherit'});if(repair.status!==0)throw Error('Automatic DSA surface regeneration failed');
  Object.assign(surfaces,JSON.parse(fs.readFileSync(base+'dsa-surfaces.json')));
}
const meshes=new Map(),veinSites={},byId=new Map(manifest.structures.map(s=>[s.id,s]));
const loader=new GLTFLoader().setMeshoptDecoder(MeshoptDecoder);
for(const file of Object.keys(sourceHashes)) {
  const bytes=fs.readFileSync(base+file),gltf=await loader.parseAsync(bytes.buffer.slice(bytes.byteOffset,bytes.byteOffset+bytes.byteLength),'');
  gltf.scene.traverse(o=>{
    if(!o.isMesh)return;
    const name=gltf.parser.json.nodes[gltf.parser.associations.get(o).nodes].name;
    const s=[...rows,...veins].find(s=>s.asset.file===file&&s.asset.node===name);if(!s)return;
    const p=o.geometry.attributes.position,a=new Float32Array(p.count*3);
    for(let i=0;i<p.count;i++)for(let k=0;k<3;k++)a[i*3+k]=p.getComponent(i,k);
    if(s.system==='vein') {
      const lo=[Infinity,Infinity,Infinity],hi=[-Infinity,-Infinity,-Infinity];
      for(let i=0;i<a.length;i++) {const k=i%3;lo[k]=Math.min(lo[k],a[i]);hi[k]=Math.max(hi[k],a[i]);}
      veinSites[s.id]=lo.map((v,k)=>(v+hi[k])/2);
    }else meshes.set(s.id,{p:a,index:new Uint32Array(o.geometry.index.array)});
  });
}
function projection(id) {
  const original=meshes.get(id),row=surfaces.entries[id],p=new Float32Array(original.p.length+row.extra.length*3);p.set(original.p);
  row.extra.forEach((v,i)=>p.set(v,original.p.length+i*3));
  const f=[],removed=new Set(row.removed),flips=new Set(row.flips),index=original.index;
  for(let i=0;i<index.length/3;i++)if(!removed.has(i)){const a=index[i*3],b=index[i*3+1],c=index[i*3+2];f.push(...(row.reverse!==flips.has(i)?[a,c,b]:[a,b,c]));}
  f.push(...row.caps);return {p,index:new Uint32Array(f)};
}
const orders=['cervical','petrous','cavernous','paraophthalmic','posterior-communicating','anterior-choroidal','terminus','v1','v2','v3','v4','a1','a2','a3','a4','a5'];
const groups=new Map();
for(const s of rows)if(s.segmentOf)groups.set(s.segmentOf,[...(groups.get(s.segmentOf)??[]),s.id]);
for(const ids of groups.values())ids.sort((a,b)=>orders.indexOf(a.split('.segment.')[1])-orders.indexOf(b.split('.segment.')[1]));
const declared=new Map();
const connect=(a,b)=>{if(a&&a!==b)declared.set(b,new Set([...(declared.get(b)??[]),a]));};
for(const s of rows)if(!s.segmentOf)connect(s.parent,s.id);
for(const r of manifest.relationships)if(r.type==='branches_to')connect(r.from,r.to);
for(const [parent,ids] of groups)for(let i=0;i<ids.length;i++) {
  declared.delete(ids[i]);connect(i?ids[i-1]:byId.get(parent)?.parent,ids[i]);
}
// Named arterial confluences, rather than inferred spatial contacts.
for(const side of ['left','right']) {
  connect(`artery.posterior.anterior_spinal_root_${side}`,'artery.posterior.anterior_spinal');
  connect(`artery.anterior.aca_a1_${side}`,'artery.anterior.anterior_communicating');
}

// Surface-geodesic level-set centroids give an automatic tubular course.
// Inlet orientation comes from DECLARED parents, never inferred connections.
function centreline(id) {
  const {p,index}=meshes.get(id),n=p.length/3;
  const points=[],canonical=new Uint32Array(n),keys=new Map();
  for(let i=0;i<n;i++) {
    const q=Array.from(p.subarray(i*3,i*3+3)),key=q.map(v=>Math.round(v*1e4)).join(',');
    let v=keys.get(key);if(v===undefined){v=points.length;keys.set(key,v);points.push(q)}canonical[i]=v;
  }
  const neighbours=Array.from({length:points.length},()=>new Map());
  for(let i=0;i<index.length;i+=3)for(let j=0;j<3;j++) {
    const a=canonical[index[i+j]],b=canonical[index[i+(j+1)%3]];if(a===b)continue;
    const d=Math.hypot(...points[a].map((v,k)=>v-points[b][k]));neighbours[a].set(b,d);neighbours[b].set(a,d);
  }
  const component=new Int32Array(points.length).fill(-1),components=[];
  for(let i=0;i<points.length;i++)if(component[i]<0&&neighbours[i].size) {
    const queue=[i],id=components.length;component[i]=id;
    for(let at=0;at<queue.length;at++)for(const v of neighbours[queue[at]].keys())if(component[v]<0){component[v]=id;queue.push(v)}
    components.push(queue);
  }
  const main=components.reduce((a,b)=>a.length>b.length?a:b),mainSet=new Set(main),used=components.reduce((sum,c)=>sum+c.length,0);
  const parents=[...(declared.get(id)??[])].flatMap(a=>groups.get(a)??[a]).filter(a=>meshes.has(a));
  const extras=surfaces.entries[id]?.extra??[];
  const candidates=[...extras];
  for(let axis=0;axis<3;axis++)for(const sign of [-1,1]) {
    const order=main.map(i=>[sign*points[i][axis],i]).sort((a,b)=>a[0]-b[0]).slice(0,Math.max(3,Math.ceil(main.length*.005)));
    candidates.push([0,1,2].map(k=>order.reduce((sum,v)=>sum+points[v[1]][k],0)/order.length));
  }
  const validCandidates=candidates.filter(c=>{
    let nearest=0,best=Infinity;for(let i=0;i<points.length;i++)if(neighbours[i].size){const d=points[i].reduce((sum,v,k)=>sum+(v-c[k])**2,0);if(d<best){best=d;nearest=i}}
    return mainSet.has(nearest);
  });
  let inlet=validCandidates[0],score=Infinity,sourceParent=null;
  for(const parent of parents) {
    const p=meshes.get(parent).p;
    for(const c of validCandidates)for(let i=0;i<p.length;i+=3) {
      const d=(p[i]-c[0])**2+(p[i+1]-c[1])**2+(p[i+2]-c[2])**2;
      if(d<score){score=d;inlet=c;sourceParent=parent;}
    }
  }
  if(!sourceParent)inlet=validCandidates.reduce((a,b)=>a[2]<b[2]?a:b); // Unparented inlet: inferior end.
  let best=Infinity;for(const i of main){const d=Math.hypot(...points[i].map((x,k)=>x-inlet[k]));if(d<best)best=d}
  const d=new Float64Array(points.length).fill(Infinity),heap=[];
  const push=(v,cost)=>{let i=heap.length;heap.push([v,cost]);while(i){let parent=(i-1)>>1;if(heap[parent][1]<=cost)break;heap[i]=heap[parent];i=parent;}heap[i]=[v,cost]};
  const pop=()=>{const top=heap[0],last=heap.pop();if(heap.length){let i=0;while(i*2+1<heap.length){let child=i*2+1;if(child+1<heap.length&&heap[child+1][1]<heap[child][1])child++;if(heap[child][1]>=last[1])break;heap[i]=heap[child];i=child;}heap[i]=last;}return top};
  const radius=Math.max(.02,best);
  for(const i of main)if(Math.hypot(...points[i].map((x,k)=>x-inlet[k]))<=radius*1.12+.01){d[i]=0;push(i,0)}
  while(heap.length){const [v,cost]=pop();if(cost!==d[v])continue;for(const [to,w] of neighbours[v])if(cost+w<d[to]){d[to]=cost+w;push(to,d[to]);}}
  const finite=Array.from(d).filter(Number.isFinite),maximum=finite.reduce((a,b)=>Math.max(a,b),0);
  if(maximum<.0001)return {points:[inlet,inlet],arc:[0,0],length:0,vertexCount:n,coordinates:Buffer.alloc(n*2).toString('base64'),selectable:false,sourceParent};
  const count=Math.max(2,Math.min(250,Math.ceil(maximum/1.25))),bins=Array.from({length:count+1},()=>[]);
  for(let i=0;i<d.length;i++)if(Number.isFinite(d[i]))bins[Math.min(count,Math.floor(d[i]/maximum*count))].push(i);
  let line=bins.filter(b=>b.length).map(b=>[0,1,2].map(k=>b.reduce((sum,i)=>sum+points[i][k],0)/b.length));
  line=line.map((p,i)=>i===0||i===line.length-1?p:p.map((_,k)=>(line[i-1][k]+2*p[k]+line[i+1][k])/4));
  const surface=projection(id),inside=p=>pointInsideSurface(surface.p,surface.index,p);
  const triangle=new Triangle(),target=new Vector3(),closest=new Vector3(),normal=new Vector3();
  const repairPoint=point=>{
    if(inside(point))return point;
    target.fromArray(point);let best=Infinity,boundary=null,inward=null;
    for(let i=0;i<surface.index.length;i+=3){
      triangle.a.fromArray(surface.p,surface.index[i]*3);triangle.b.fromArray(surface.p,surface.index[i+1]*3);triangle.c.fromArray(surface.p,surface.index[i+2]*3);
      triangle.getNormal(normal);if(normal.lengthSq()<.5)continue;
      triangle.closestPointToPoint(target,closest);const distance=closest.distanceToSquared(target);
      if(distance<best){best=distance;boundary=closest.toArray();inward=normal.toArray();}
    }
    if(boundary)for(const offset of [.025,.05,.1,.2,.4,.8,1.6,2.4]){
      const q=boundary.map((v,k)=>v-inward[k]*offset);if(inside(q))return q;
    }
    return point;
  };
  line=line.map(repairPoint);
  while(line.length>2&&!inside(line[0]))line.shift();
  while(line.length>2&&!inside(line.at(-1)))line.pop();
  // Refine any chord that leaves the lumen. Unsupported compound courses
  // remain renderable, but cannot be selected as an injection source.
  for(let pass=0;pass<8;pass++) {
    const refined=[line[0]];
    for(let i=1;i<line.length;i++){
      for(const u of [.25,.5,.75]){const middle=line[i].map((v,k)=>v*u+line[i-1][k]*(1-u));if(!inside(middle))refined.push(repairPoint(middle));}
      refined.push(line[i]);
    }
    // Bound work for compound or irregular meshes. Their verified ranges
    // remain usable; unresolved portions cannot accept an injection tip.
    if(refined.length===line.length||refined.length>512)break;line=refined;
  }
  const validPoints=line.map(inside),validChords=[];
  for(let i=1;i<line.length;i++)validChords.push(validPoints[i-1]&&validPoints[i]&&[.25,.5,.75].every(u=>inside(line[i].map((v,k)=>v*u+line[i-1][k]*(1-u)))));
  const arc=[0];for(let i=1;i<line.length;i++)arc.push(arc[i-1]+Math.hypot(...line[i].map((p,k)=>p-line[i-1][k])));
  const length=arc.at(-1),coordinates=Buffer.alloc(n*2);
  for(let i=0;i<n;i++)coordinates.writeUInt16LE(Math.round(projectToPath(line,arc,p.subarray(i*3,i*3+3)).distance/length*65535),i*2);
  const directionKnown=sourceParent||id.endsWith('.segment.v1');
  const safeRanges=[];let safeLength=0;
  for(let i=0;i<validChords.length;i++)if(validChords[i]) {
    safeLength+=arc[i+1]-arc[i];const previous=safeRanges.at(-1);
    if(previous&&previous[1]===arc[i])previous[1]=arc[i+1];else safeRanges.push([arc[i],arc[i+1]]);
  }
  const result={points:line.map(p=>p.map(v=>+v.toFixed(6))),arc:arc.map(v=>+v.toFixed(6)),length:+length.toFixed(6),vertexCount:n,coordinates:coordinates.toString('base64'),safeRanges:safeRanges.map(r=>r.map(v=>+v.toFixed(6))),selectable:!!directionKnown&&!id.includes('anterior_communicating')&&finite.length/used>.9&&length>.05&&safeLength/length>.9,sourceParent};
  if(result.selectable&&result.safeRanges.some(([a,b])=>[.01,.5,.99].some(u=>!inside(pathPoint(result,a+(b-a)*u)))))result.selectable=false;
  if(result.selectable)for(const inlet of [0,result.length*.37])for(const section of splitFlowSurface(surface.p,surface.index,decodeCoordinates(result,surface.p),result.length,inlet))if(closedSurfaceError(section))throw Error('Invalid closed flow section '+id);
  return result;
}
const entries=only?JSON.parse(fs.readFileSync(output)).entries:{};let completed=0;
for(const s of rows)if(surfaces.entries[s.id]) {
  if(only&&!only.has(s.id))continue;
  entries[s.id]=centreline(s.id);
  if(++completed%30===0)console.log('Flow courses generated',completed);
}
const edges={};
const addEdge=(from,to,at)=>{if(!entries[from]||!entries[to]||from===to)return;const list=edges[from]??=[];if(!list.some(e=>e.to===to))list.push({to,at:+Math.max(0,Math.min(entries[from].length,at)).toFixed(5)});edges[from]=list};
for(const s of rows)if(entries[s.id]) {
  for(const parent of declared.get(s.id)??[]) {
    const sources=groups.get(parent)??[parent];
    const choices=sources.filter(a=>entries[a]).map(a=>({id:a,...projectToPath(entries[a].points,entries[a].arc,entries[s.id].points[0])})).sort((a,b)=>a.error-b.error);
    if(choices.length)addEdge(choices[0].id,s.id,s.segmentOf&&byId.get(choices[0].id)?.segmentOf===s.segmentOf?entries[choices[0].id].length:choices[0].distance);
  }
}
// Both vertebrals feed the declared basilar confluence.
for(const side of ['left','right'])addEdge(`artery.posterior.vertebral_${side}.segment.v4`,'artery.posterior.basilar',entries[`artery.posterior.vertebral_${side}.segment.v4`]?.length??0);
for(const row of Object.values(entries))delete row.sourceParent;
fs.writeFileSync(output,JSON.stringify({schema:1,sourceHashes,graphHash,graphSource,generatorHash:only?'partial':generatorHash,entries,edges,veinSites}));
console.log('DSA flow data written:',Object.keys(entries).length,'arterial courses.');
