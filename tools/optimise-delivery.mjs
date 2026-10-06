// Delivery-only optimisation. Positions are rounded to a 1/4096 mm grid; topology and UVs remain exact.
// The app does not use model vertex colours, so those are omitted.
// Float shading normals use high-precision octahedral packing. Brain triangle
// order is retained because its surface anchors address triangle indices.
import fs from 'node:fs';
import path from 'node:path';
import assert from 'node:assert/strict';
import {MeshoptEncoder,MeshoptDecoder} from 'meshoptimizer';
await Promise.all([MeshoptEncoder.ready,MeshoptDecoder.ready]);
const inputDir=process.argv[2]??'public/anatomy/models';
const outputDir=process.argv[3]??'.delivery-models';fs.mkdirSync(outputDir,{recursive:true});
const report=[];
for(const filename of fs.readdirSync(inputDir).filter(n=>n.endsWith('.glb'))){
 const raw=fs.readFileSync(path.join(inputDir,filename));const jl=raw.readUInt32LE(12);const doc=JSON.parse(raw.subarray(20,20+jl));const bin=raw.subarray(28+jl);
 assert(!doc.skins?.length&&!doc.animations?.length&&!doc.images?.length,'Unexpected animated or textured model');
 const views=doc.bufferViews.map(v=>{const out=new Uint8Array(v.byteLength);const e=v.extensions?.EXT_meshopt_compression;if(e)MeshoptDecoder.decodeGltfBuffer(out,e.count,e.byteStride,bin.subarray(e.byteOffset,e.byteOffset+e.byteLength),e.mode,e.filter);else out.set(bin.subarray(v.byteOffset??0,(v.byteOffset??0)+v.byteLength));return out;});
 const chunks=[],bufferViews=[],accessors=[];let encodedOffset=0,decodedOffset=0;let triangleCount=0,vertexCount=0,maxNormalAngle=0,maxPositionError=0;let buffersVerified=0;
 const sizes={5121:1,5122:2,5123:2,5125:4,5126:4};const counts={SCALAR:1,VEC2:2,VEC3:3,VEC4:4};
 function bytes(a){const v=doc.bufferViews[a.bufferView];assert.equal(v.byteStride??counts[a.type]*sizes[a.componentType],counts[a.type]*sizes[a.componentType]);return views[a.bufferView].subarray(a.byteOffset??0,(a.byteOffset??0)+a.count*counts[a.type]*sizes[a.componentType]);}
 function add(a,b,stride,mode,filter){const encoded=MeshoptEncoder.encodeGltfBuffer(b,a.count,stride,mode);const decoded=new Uint8Array(a.count*stride);MeshoptDecoder.decodeGltfBuffer(decoded,a.count,stride,encoded,mode,filter);if(!filter&&mode!=='TRIANGLES')assert(Buffer.from(decoded).equals(Buffer.from(b)),'Exact codec roundtrip');if(mode==='TRIANGLES'){const a=new Uint32Array(b.buffer,b.byteOffset,b.byteLength/4);const q=new Uint32Array(decoded.buffer);for(let i=0;i<q.length;i+=3){assert((q[i]===a[i]&&q[i+1]===a[i+1]&&q[i+2]===a[i+2])||(q[i]===a[i+1]&&q[i+1]===a[i+2]&&q[i+2]===a[i])||(q[i]===a[i+2]&&q[i+1]===a[i]&&q[i+2]===a[i+1]),'Triangle orientation roundtrip');}}buffersVerified++;
 const e={buffer:0,byteOffset:encodedOffset,byteLength:encoded.length,byteStride:stride,count:a.count,mode};if(filter)e.filter=filter;
 const vi=bufferViews.length;bufferViews.push({buffer:1,byteOffset:decodedOffset,byteLength:decoded.length,...(mode==='ATTRIBUTES'?{byteStride:stride,target:34962}:{target:34963}),extensions:{EXT_meshopt_compression:e}});decodedOffset+=decoded.length;
 const pad=(-encoded.length)&3;chunks.push(Buffer.from(encoded),Buffer.alloc(pad));encodedOffset+=encoded.length+pad;
 const ai=accessors.length;accessors.push({...a,bufferView:vi,byteOffset:0});return {ai,decoded};}
 for(const mesh of doc.meshes){for(const prim of mesh.primitives){assert.equal(prim.mode??4,4);assert(!prim.targets?.length);const ia=doc.accessors[prim.indices];const ib=bytes(ia);const oldIndices=ia.componentType===5125?new Uint32Array(ib.buffer,ib.byteOffset,ia.count):Uint32Array.from(new Uint16Array(ib.buffer,ib.byteOffset,ia.count));
 const reordered=oldIndices.slice();const [remap,unique]=MeshoptEncoder.reorderMesh(reordered,true,true);const retainOrder=filename==='brain-context.glb';const indices=retainOrder?Uint32Array.from(oldIndices,i=>remap[i]):reordered;
 const positionCount=doc.accessors[prim.attributes.POSITION].count;assert(unique<=positionCount);triangleCount+=indices.length/3;vertexCount+=unique;
 const referenced=new Set(oldIndices);for(let i=0;i<remap.length;i++)if(!referenced.has(i))remap[i]=0xffffffff;
 const inverse=new Uint32Array(unique);for(let i=0;i<remap.length;i++)if(remap[i]!==0xffffffff)inverse[remap[i]]=i;
 // Confirm that reordered triangle lists retain every original oriented face.
 if(!retainOrder){const signatures=new Map();for(let i=0;i<oldIndices.length;i+=3){let t=Array.from(oldIndices.subarray(i,i+3));let j=t.indexOf(Math.min(...t));const key=[...t.slice(j),...t.slice(0,j)].join(',');signatures.set(key,(signatures.get(key)??0)+1);}for(let i=0;i<indices.length;i+=3){let t=Array.from(indices.subarray(i,i+3),v=>inverse[v]);let j=t.indexOf(Math.min(...t));const key=[...t.slice(j),...t.slice(0,j)].join(',');assert(signatures.get(key)>0);signatures.set(key,signatures.get(key)-1);}assert([...signatures.values()].every(v=>v===0));}
 const result=add({...ia,count:indices.length,componentType:5125},new Uint8Array(indices.buffer),4,retainOrder?'INDICES':'TRIANGLES');prim.indices=result.ai;
 for(const [semantic,oldId] of Object.entries(prim.attributes)){if(semantic==='COLOR_0'){delete prim.attributes[semantic];continue;}const a=doc.accessors[oldId];const source=bytes(a);const stride=counts[a.type]*sizes[a.componentType];const dest=new Uint8Array(unique*stride);for(let i=0;i<remap.length;i++)if(remap[i]!==0xffffffff)dest.set(source.subarray(i*stride,(i+1)*stride),remap[i]*stride);
 if(semantic==='NORMAL'&&a.componentType===5126&&a.type==='VEC3'){
 const normals=new Float32Array(dest.buffer);const xyzw=new Float32Array(unique*4);for(let i=0;i<unique;i++)xyzw.set(normals.subarray(i*3,i*3+3),i*4);
 const filtered=MeshoptEncoder.encodeFilterOct(xyzw,unique,8,12);const packed=add({...a,count:unique,componentType:5122,normalized:true,min:undefined,max:undefined},filtered,8,'ATTRIBUTES','OCTAHEDRAL');const nn=new Int16Array(packed.decoded.buffer);
 for(let i=0;i<unique;i++){const ax=normals[i*3],ay=normals[i*3+1],az=normals[i*3+2],bx=nn[i*4]/32767,by=nn[i*4+1]/32767,bz=nn[i*4+2]/32767;const denom=Math.hypot(ax,ay,az)*Math.hypot(bx,by,bz);if(denom>1e-8)maxNormalAngle=Math.max(maxNormalAngle,Math.acos(Math.min(1,Math.max(-1,(ax*bx+ay*by+az*bz)/denom)))*180/Math.PI);}
 prim.attributes[semantic]=packed.ai;
 }else{let outAccessor={...a,count:unique};if(semantic==='POSITION'){const positions=new Float32Array(dest.buffer);const lo=[Infinity,Infinity,Infinity],hi=[-Infinity,-Infinity,-Infinity];for(let i=0;i<unique;i++){let error2=0;for(let j=0;j<3;j++){const old=positions[i*3+j];const rounded=Math.round(old*4096)/4096;positions[i*3+j]=rounded;error2+=(rounded-old)**2;lo[j]=Math.min(lo[j],rounded);hi[j]=Math.max(hi[j],rounded);}maxPositionError=Math.max(maxPositionError,Math.sqrt(error2));}outAccessor={...outAccessor,min:lo,max:hi};}const packed=add(outAccessor,dest,stride,'ATTRIBUTES');prim.attributes[semantic]=packed.ai;for(let i=0;i<remap.length;i++)if(remap[i]!==0xffffffff&&semantic!=='POSITION')assert(Buffer.from(packed.decoded.subarray(remap[i]*stride,(remap[i]+1)*stride)).equals(Buffer.from(source.subarray(i*stride,(i+1)*stride))),JSON.stringify({mesh:mesh.name,semantic,sourceCount:a.count,remapLength:remap.length,unique,i,newIndex:remap[i]}));}
 }
 }}
 doc.accessors=accessors;doc.bufferViews=bufferViews;doc.buffers=[{byteLength:encodedOffset},{byteLength:decodedOffset,extensions:{EXT_meshopt_compression:{fallback:true}}}];doc.extensionsUsed=[...(doc.extensionsUsed??[]).filter(x=>x!=='EXT_meshopt_compression'&&x!=='KHR_mesh_quantization'),'EXT_meshopt_compression','KHR_mesh_quantization'];doc.extensionsRequired=[...(doc.extensionsRequired??[]).filter(x=>x!=='EXT_meshopt_compression'&&x!=='KHR_mesh_quantization'),'EXT_meshopt_compression','KHR_mesh_quantization'];
 let j=Buffer.from(JSON.stringify(doc));j=Buffer.concat([j,Buffer.alloc((-j.length)&3,32)]);const b=Buffer.concat(chunks);const h=Buffer.alloc(20);h.write('glTF');h.writeUInt32LE(2,4);h.writeUInt32LE(28+j.length+b.length,8);h.writeUInt32LE(j.length,12);h.writeUInt32LE(0x4e4f534a,16);const bh=Buffer.alloc(8);bh.writeUInt32LE(b.length);bh.writeUInt32LE(0x004e4942,4);const out=path.join(outputDir,filename);fs.writeFileSync(out,Buffer.concat([h,j,bh,b]));
 const row={filename,inputBytes:raw.length,outputBytes:fs.statSync(out).size,triangleCount,vertexCount,maximumPositionErrorMm:maxPositionError,positionGridMm:1/4096,unusedVertexColoursRemoved:true,orientedTrianglesUnchanged:true,brainTriangleOrderPreserved:filename==='brain-context.glb',maximumNormalAngleDegrees:maxNormalAngle,buffersVerified};report.push(row);console.log(row);
}
fs.writeFileSync(path.join(outputDir,'optimisation-report.json'),JSON.stringify(report,null,2)+'\n');
