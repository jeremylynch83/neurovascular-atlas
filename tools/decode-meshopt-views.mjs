// Build-time buffer decoding for the Python surface-anchor validator.
import fs from 'node:fs';
import {MeshoptDecoder} from 'three/examples/jsm/libs/meshopt_decoder.module.js';
await MeshoptDecoder.ready;
const data=fs.readFileSync(process.argv[2]);
const length=data.readUInt32LE(12),doc=JSON.parse(data.subarray(20,20+length));
const binary=data.subarray(28+length);
const output=Buffer.alloc(Math.max(...doc.bufferViews.map(v=>(v.byteOffset??0)+v.byteLength)));
for(const v of doc.bufferViews){
 const start=v.byteOffset??0,e=v.extensions?.EXT_meshopt_compression;
 if(e)MeshoptDecoder.decodeGltfBuffer(output.subarray(start,start+v.byteLength),e.count,e.byteStride,binary.subarray(e.byteOffset,e.byteOffset+e.byteLength),e.mode,e.filter);
 else binary.copy(output,start,start,start+v.byteLength);
}
process.stdout.write(output);
