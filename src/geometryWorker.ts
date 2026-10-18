import * as THREE from 'three';
import { GLTFLoader } from 'three/examples/jsm/loaders/GLTFLoader.js';
import { MeshoptDecoder } from 'three/examples/jsm/libs/meshopt_decoder.module.js';
import type { PreparedMesh } from './stagedLoading';

// All shipped GLBs contain geometry/materials only, without external images.
// Parsing, decompression, Float32 conversion, transforms, normals and bounds
// stay in this dedicated worker. A pull protocol bounds transferred memory.
const context = self as unknown as { onmessage: (event: MessageEvent) => void; postMessage: (data: unknown, transfer?: Transferable[]) => void };
const loader = new GLTFLoader().setMeshoptDecoder(MeshoptDecoder);
const nodes = new Map<string, THREE.Mesh>();
let scene: THREE.Group | null = null;
function release() {
  scene?.traverse(object => {
    const mesh = object as THREE.Mesh; mesh.geometry?.dispose();
    const materials = Array.isArray(mesh.material) ? mesh.material : [mesh.material];
    for (const material of materials) material?.dispose();
  });
  scene = null; nodes.clear();
}
context.onmessage = async ({ data }) => {
  try {
    let result: unknown;
    const transfer: Transferable[] = [];
    if (data.action === 'load') {
      release();
      const gltf = await loader.loadAsync(data.url);
      scene = gltf.scene; scene.updateMatrixWorld(true);
      const parser = gltf.parser as unknown as { json: { nodes: { name?: string }[] }; associations: Map<THREE.Object3D, { nodes?: number }> };
      scene.traverse(object => {
        if (!(object as THREE.Mesh).isMesh) return;
        const mesh = object as THREE.Mesh;
        for (let cursor: THREE.Object3D | null = object; cursor; cursor = cursor.parent) {
          const index = parser.associations.get(cursor)?.nodes;
          if (index !== undefined) { const name = parser.json.nodes[index]?.name; if (name) nodes.set(name, mesh); break; }
        }
        if (object.name) nodes.set(object.name, mesh);
        if (object.parent?.name) nodes.set(object.parent.name, mesh);
      });
    } else if (data.action === 'prepare') {
      const meshes: PreparedMesh[] = []; let vertices = 0;
      for (const row of data.structures as { id: string; node: string }[]) {
        const src = nodes.get(row.node) ?? nodes.get(THREE.PropertyBinding.sanitizeNodeName(row.node));
        if (!src) throw new Error(`Could not find geometry for ${row.id}`);
        const count = src.geometry.getAttribute('position').count;
        if (meshes.length && vertices + count > Math.max(8_000, Math.min(50_000, data.vertexBudget ?? 50_000))) break;
        vertices += count;
        const geo = new THREE.BufferGeometry();
        for (const name of ['position', 'normal']) {
          const attribute = src.geometry.getAttribute(name); if (!attribute) continue;
          const array = new Float32Array(attribute.count * 3);
          for (let i = 0; i < attribute.count; i++) {
            array[i * 3] = attribute.getX(i); array[i * 3 + 1] = attribute.getY(i); array[i * 3 + 2] = attribute.getZ(i);
          }
          geo.setAttribute(name, new THREE.BufferAttribute(array, 3));
        }
        if (src.geometry.index) geo.setIndex(new THREE.BufferAttribute(Uint32Array.from(src.geometry.index.array), 1));
        geo.applyMatrix4(src.matrixWorld);
        if (!geo.getAttribute('normal')) geo.computeVertexNormals();
        geo.computeBoundingBox(); geo.computeBoundingSphere();
        const positions = geo.getAttribute('position').array as Float32Array;
        const normals = geo.getAttribute('normal')?.array as Float32Array | undefined;
        const indices = geo.index?.array as Uint32Array | undefined;
        const packet: PreparedMesh = { id: row.id, positions, normals, indices,
          bounds: [geo.boundingBox!.min.toArray(), geo.boundingBox!.max.toArray()],
          sphere: { centre: geo.boundingSphere!.center.toArray(), radius: geo.boundingSphere!.radius } };
        meshes.push(packet); transfer.push(positions.buffer);
        if (normals) transfer.push(normals.buffer); if (indices) transfer.push(indices.buffer);
      }
      result = meshes;
    } else if (data.action === 'release') release();
    else throw new Error('Unknown geometry request');
    context.postMessage({ request: data.request, result }, transfer);
  } catch (error) { context.postMessage({ request: data.request, error: error instanceof Error ? error.message : String(error) }); }
};
