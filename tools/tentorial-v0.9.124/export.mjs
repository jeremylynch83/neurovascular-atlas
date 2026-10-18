import fs from'node:fs';import path from'node:path';import assert from'node:assert/strict';import crypto from'node:crypto';
const app=path.resolve(import.meta.dirname,'../..'),old=path.resolve(process.argv[2]),target=path.resolve(process.argv[3]??app),work=app+'/anatomy/source/tentorial-v0.9.124',mode='export';assert.notEqual(old,target);assert.equal(JSON.parse(fs.readFileSync(old+'/package.json')).version,'0.9.123');
const {MeshoptDecoder,MeshoptEncoder}=await import(app+'/node_modules/meshoptimizer/index.js');await Promise.all([MeshoptDecoder.ready,MeshoptEncoder.ready]);
const manifest=JSON.parse(fs.readFileSync(old+'/public/anatomy/manifest.json'));const rows=JSON.parse(fs.readFileSync(work+'/authoring.json'));const names=new Set(rows.map(x=>x.node));
for(const file of ['complete-circulation.glb','complete-anastomoses.glb']){
 const raw=fs.readFileSync(old+'/public/anatomy/models/'+file);assert.equal(crypto.createHash('sha256').update(raw).digest('hex'),JSON.parse(fs.readFileSync(work+'/source-assets.json')).sourceHashes['models/'+file]);const jl=raw.readUInt32LE(12),doc=JSON.parse(raw.subarray(20,20+jl)),binary=raw.subarray(28+jl),cache=new Map();
 const decode=(id)=>{const a=doc.accessors[id],v=doc.bufferViews[a.bufferView];let bytes=cache.get(a.bufferView);if(!bytes){bytes=Buffer.alloc(v.byteLength);const e=v.extensions?.EXT_meshopt_compression;if(e)MeshoptDecoder.decodeGltfBuffer(bytes,e.count,e.byteStride,binary.subarray(e.byteOffset,e.byteOffset+e.byteLength),e.mode,e.filter);else binary.copy(bytes,0,v.byteOffset??0,(v.byteOffset??0)+v.byteLength);cache.set(a.bufferView,bytes)}return{a,v,bytes}};
 let eo=binary.length,offset=doc.buffers[1].byteLength;const chunks=[binary],changed=[];
 function add(bytes,count,stride,accessor,kind='ATTRIBUTES'){
  const encoded=Buffer.from(MeshoptEncoder.encodeGltfBuffer(bytes,count,stride,kind)),test=Buffer.alloc(bytes.length);MeshoptDecoder.decodeGltfBuffer(test,count,stride,encoded,kind);assert(test.equals(bytes));const view=doc.bufferViews.length;doc.bufferViews.push({buffer:1,byteOffset:offset,byteLength:bytes.length,...(kind==='ATTRIBUTES'?{byteStride:stride}:{}),target:kind==='ATTRIBUTES'?34962:34963,extensions:{EXT_meshopt_compression:{buffer:0,byteOffset:eo,byteLength:encoded.length,count,byteStride:stride,mode:kind}}});const id=doc.accessors.length;doc.accessors.push({...accessor,count,bufferView:view,byteOffset:0});const pad=Buffer.alloc((-encoded.length)&3);chunks.push(encoded,pad);eo+=encoded.length+pad.length;offset+=bytes.length;return id;
 }
 for(const node of doc.nodes.filter(x=>names.has(x.name))){
  const p=doc.meshes[node.mesh].primitives[0];const name=node.name;
  if(mode==='normals'){
   const{a,v,bytes}=decode(p.attributes.NORMAL);assert(a.componentType===5122&&a.normalized);const out=Buffer.alloc(a.count*8);for(let i=0;i<a.count;i++)for(let j=0;j<3;j++)out.writeInt16LE(bytes.readInt16LE((a.byteOffset??0)+i*(v.byteStride??6)+j*2),i*8+j*2);fs.writeFileSync(work+'/'+name+'.source-normals.bin',out);continue;
  }
  const pos=fs.readFileSync(work+'/'+name+'.positions.bin'),ind=fs.readFileSync(work+'/'+name+'.indices.bin'),norm=fs.readFileSync(work+'/'+name+'.normal-snorm16.bin');const count=pos.length/12;assert.equal(norm.length,count*8);const lo=[Infinity,Infinity,Infinity],hi=[-Infinity,-Infinity,-Infinity];for(let i=0;i<count;i++)for(let k=0;k<3;k++){const x=pos.readFloatLE(i*12+k*4);assert(Number.isFinite(x));lo[k]=Math.min(lo[k],x);hi[k]=Math.max(hi[k],x)}
  p.attributes.POSITION=add(pos,count,12,{componentType:5126,type:'VEC3',min:lo,max:hi});p.attributes.NORMAL=add(norm,count,8,{componentType:5122,type:'VEC3',normalized:true});p.indices=add(ind,ind.length/4,4,{componentType:5125,type:'SCALAR'},'INDICES');changed.push({node:name,vertices:count,triangles:ind.length/12});
 }
 if(mode==='normals')continue;
 if(!changed.length){fs.copyFileSync(old+'/public/anatomy/models/'+file,target+'/public/anatomy/models/'+file);continue;}
 doc.buffers[0].byteLength=eo;doc.buffers[1].byteLength=offset;let j=Buffer.from(JSON.stringify(doc));j=Buffer.concat([j,Buffer.alloc((-j.length)&3,32)]);const b=Buffer.concat(chunks),h=Buffer.alloc(20),bh=Buffer.alloc(8);h.write('glTF');h.writeUInt32LE(2,4);h.writeUInt32LE(28+j.length+b.length,8);h.writeUInt32LE(j.length,12);h.writeUInt32LE(0x4e4f534a,16);bh.writeUInt32LE(b.length);bh.writeUInt32LE(0x004e4942,4);const result=Buffer.concat([h,j,bh,b]);fs.writeFileSync(target+'/public/anatomy/models/'+file,result);console.log({file,bytes:result.length,changed,sha256:crypto.createHash('sha256').update(result).digest('hex')});
}
