// Authoring verification against a supplied previous venous GLB.
import fs from 'node:fs';import assert from 'node:assert/strict';
import {GLTFLoader} from 'three/examples/jsm/loaders/GLTFLoader.js';import {MeshoptDecoder} from 'three/examples/jsm/libs/meshopt_decoder.module.js';
const loader=new GLTFLoader().setMeshoptDecoder(MeshoptDecoder);
async function load(file){const b=fs.readFileSync(file),g=await loader.parseAsync(b.buffer.slice(b.byteOffset,b.byteOffset+b.byteLength),'');const out=new Map();g.scene.traverse(o=>{if(o.isMesh)out.set(g.parser.json.nodes[g.parser.associations.get(o).nodes].name,o.geometry)});return out}
const old=await load(process.argv[2]),current=await load(process.argv[3]??new URL('../public/anatomy/models/venous.glb',import.meta.url).pathname),rows=[];
for(const [name,g] of current){const a=old.get(name),p=g.attributes.position,op=a.attributes.position,n=g.attributes.normal,on=a.attributes.normal;const moved=new Set();for(let i=0;i<p.count;i++)if(p.getX(i)!==op.getX(i)||p.getY(i)!==op.getY(i)||p.getZ(i)!==op.getZ(i))moved.add(i);
 if(!moved.size){assert.deepEqual(n.array,on.array);continue}
 const edges=new Map(),affected=new Set(),index=g.index.array;
 for(let i=0;i<index.length;i+=3){const face=Array.from(index.slice(i,i+3));if(face.some(v=>moved.has(v)))face.forEach(v=>affected.add(v));for(let k=0;k<3;k++){const x=face[k],y=face[(k+1)%3],key=x<y?x+','+y:y+','+x;edges.set(key,(edges.get(key)??0)+1)}}
 const boundary=new Set([...edges].filter(([,v])=>v===1).flatMap(([k])=>k.split(',').map(Number)));let fixedMax=0;
 for(let i=0;i<p.count;i++)if(boundary.has(i)||!affected.has(i)){const error=Math.hypot(n.getX(i)-on.getX(i),n.getY(i)-on.getY(i),n.getZ(i)-on.getZ(i));fixedMax=Math.max(fixedMax,error)}
 assert(fixedMax<.002,'Native/unaffected normals changed beyond 12-bit round-trip tolerance '+name+' '+fixedMax);rows.push({name,boundaryVertices:boundary.size,unaffectedNormalMaximumVectorError:fixedMax})
}
assert.equal(rows.length,Number(process.argv[4]??3));console.log(JSON.stringify({passed:true,changedNormalStreams:rows,otherNormalStreamsExact:true},null,2));
