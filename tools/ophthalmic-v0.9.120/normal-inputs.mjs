import fs from 'node:fs';import path from 'node:path';
const base=path.resolve(process.argv[2])+'/',work=path.resolve(process.argv[3]);
const{GLTFLoader}=await import(base+'node_modules/three/examples/jsm/loaders/GLTFLoader.js');const{MeshoptDecoder}=await import(base+'node_modules/three/examples/jsm/libs/meshopt_decoder.module.js');await MeshoptDecoder.ready;
const b=fs.readFileSync(base+'public/anatomy/models/venous.glb'),g=await new GLTFLoader().setMeshoptDecoder(MeshoptDecoder).parseAsync(b.buffer.slice(b.byteOffset,b.byteOffset+b.byteLength),'');
g.scene.traverse(o=>{if(!o.isMesh)return;const n=g.parser.json.nodes[g.parser.associations.get(o).nodes]?.name;if(!/vein\.(inferior_ophthalmic|superior_ophthalmic)\./.test(n))return;const a=o.geometry.attributes.normal,arr=new Int16Array(a.count*4);for(let i=0;i<a.count;i++)for(let k=0;k<3;k++)arr[i*4+k]=Math.round(a.getComponent(i,k)*32767);fs.writeFileSync(work+'/candidate/'+n+'.source-normals.bin',Buffer.from(arr.buffer));});
