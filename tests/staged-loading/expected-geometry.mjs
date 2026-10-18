import fs from'node:fs';import crypto from'node:crypto';import * as THREE from'three';import{GLTFLoader}from'three/addons/loaders/GLTFLoader.js';import{MeshoptDecoder}from'meshoptimizer';
await MeshoptDecoder.ready;const loader=new GLTFLoader().setMeshoptDecoder(MeshoptDecoder),manifest=JSON.parse(fs.readFileSync('public/anatomy/manifest.json'));
const hash=array=>crypto.createHash('sha256').update(new Uint8Array(array.buffer,array.byteOffset,array.byteLength)).digest('hex'),expected={};
for(const file of [...new Set(manifest.structures.filter(s=>s.asset).map(s=>s.asset.file))]){
 const b=fs.readFileSync('public/anatomy/'+file),gltf=await loader.parseAsync(b.buffer.slice(b.byteOffset,b.byteOffset+b.byteLength),'');gltf.scene.updateMatrixWorld(true);const nodes=new Map();
 gltf.scene.traverse(object=>{if(!object.isMesh)return;for(let cursor=object;cursor;cursor=cursor.parent){const i=gltf.parser.associations.get(cursor)?.nodes;if(i!==undefined){const name=gltf.parser.json.nodes[i]?.name;if(name)nodes.set(name,object);break;}}if(object.name)nodes.set(object.name,object);if(object.parent?.name)nodes.set(object.parent.name,object)});
 for(const s of manifest.structures.filter(s=>s.asset?.file===file)){
  const mesh=nodes.get(s.asset.node)??nodes.get(THREE.PropertyBinding.sanitizeNodeName(s.asset.node));if(!mesh)throw Error('Missing '+s.id);const geo=new THREE.BufferGeometry();
  for(const name of ['position','normal']){const a=mesh.geometry.getAttribute(name);if(!a)continue;const out=new Float32Array(a.count*3);for(let i=0;i<a.count;i++){out[i*3]=a.getX(i);out[i*3+1]=a.getY(i);out[i*3+2]=a.getZ(i)}geo.setAttribute(name,new THREE.BufferAttribute(out,3));}
  if(mesh.geometry.index)geo.setIndex(mesh.geometry.index);geo.applyMatrix4(mesh.matrixWorld);if(!geo.getAttribute('normal'))geo.computeVertexNormals();
  expected[s.id]={position:hash(geo.getAttribute('position').array),normal:hash(geo.getAttribute('normal').array),index:geo.index?hash(Uint32Array.from(geo.index.array)):null};
 }
 console.log('Reference',file);
}
fs.writeFileSync('tests/staged-loading/expected-geometry.json',JSON.stringify(expected));console.log('Expected geometry',Object.keys(expected).length);
