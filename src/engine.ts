import * as THREE from 'three';
import { GLTFLoader } from 'three/examples/jsm/loaders/GLTFLoader.js';
import { MeshoptDecoder } from 'three/examples/jsm/libs/meshopt_decoder.module.js';
import { OrbitControls } from 'three/examples/jsm/controls/OrbitControls.js';
import type { AnatomyManifest, LayerState, Structure, SystemId } from './types';

const COLOURS: Record<SystemId, number> = { bone: 0xd9d1c0, artery: 0xc4433c, vein: 0x416aa8, brain: 0xc5a7a1 };
const DEFAULT_VIEW = new THREE.Vector3(0.75, 0.18, 1);

type Entry = { structure: Structure; mesh: THREE.Mesh; baseOpacity: number };

/**
 * Convert quantised/interleaved GLTF attributes to writable Float32 arrays
 * before baking node transforms. The legacy BodyParts3D assets use
 * KHR_mesh_quantization; applying transforms directly to their integer-backed
 * position attributes clamps/truncates coordinates and turns the skull into a
 * box-like artefact.
 */
function toFloatGeometry(src: THREE.BufferGeometry): THREE.BufferGeometry {
  const geo = new THREE.BufferGeometry();
  for (const name of ['position', 'normal'] as const) {
    const a = src.getAttribute(name) as THREE.BufferAttribute | THREE.InterleavedBufferAttribute | undefined;
    if (!a) continue;
    const arr = new Float32Array(a.count * 3);
    for (let i = 0; i < a.count; i++) {
      arr[i * 3] = a.getX(i);
      arr[i * 3 + 1] = a.getY(i);
      arr[i * 3 + 2] = a.getZ(i);
    }
    geo.setAttribute(name, new THREE.BufferAttribute(arr, 3));
  }
  if (src.index) geo.setIndex(src.index);
  return geo;
}

export class AnatomyEngine {
  private container: HTMLElement;
  private manifest: AnatomyManifest;
  private scene = new THREE.Scene();
  private camera = new THREE.PerspectiveCamera(35, 1, 0.01, 1000);
  private renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
  private controls: OrbitControls;
  private root = new THREE.Group();
  private entries = new Map<string, Entry>();
  private objectToId = new Map<THREE.Object3D, string>();
  private loader = new GLTFLoader();
  private raycaster = new THREE.Raycaster();
  private pointer = new THREE.Vector2();
  private resize?: ResizeObserver;
  private raf = 0;
  private selected: string | null = null;
  private hidden = new Set<string>();
  private layers: Record<SystemId, LayerState> = { bone: 'ghost', artery: 'on', vein: 'off', brain: 'off' };
  private clipPlane = new THREE.Plane(new THREE.Vector3(1, 0, 0), 0);
  private clipEnabled = false;
  private onSelect: (id: string | null) => void;

  constructor(container: HTMLElement, manifest: AnatomyManifest, onSelect: (id: string | null) => void) {
    this.container = container;
    this.manifest = manifest;
    this.onSelect = onSelect;
    this.loader.setMeshoptDecoder(MeshoptDecoder);
    this.renderer.setPixelRatio(Math.min(devicePixelRatio, 2));
    this.renderer.outputColorSpace = THREE.SRGBColorSpace;
    this.renderer.localClippingEnabled = true;
    this.renderer.domElement.className = 'atlas-canvas';
    this.renderer.domElement.tabIndex = 0;
    this.container.appendChild(this.renderer.domElement);
    this.scene.add(this.root);
    this.scene.add(new THREE.HemisphereLight(0xffffff, 0x8d877d, 2.2));
    const key = new THREE.DirectionalLight(0xffffff, 2.7); key.position.set(4, 7, 6); this.scene.add(key);
    const fill = new THREE.DirectionalLight(0xdde6ff, 1.1); fill.position.set(-5, 1, -3); this.scene.add(fill);
    this.controls = new OrbitControls(this.camera, this.renderer.domElement);
    this.controls.enableDamping = true;
    this.controls.dampingFactor = 0.08;
    this.controls.addEventListener('change', () => this.render());
    this.renderer.domElement.addEventListener('pointerup', this.pick);
    this.resize = new ResizeObserver(() => this.onResize());
    this.resize.observe(container);
    this.onResize();
  }

  async load(): Promise<void> {
    const withAssets = this.manifest.structures.filter((s) => s.asset);
    const files = [...new Set(withAssets.map((s) => s.asset!.file))];
    for (const file of files) {
      const gltf = await this.loader.loadAsync(`${import.meta.env.BASE_URL}anatomy/${file}`);
      gltf.scene.updateMatrixWorld(true);
      const nodes = new Map<string, THREE.Mesh>();
      gltf.scene.traverse((o) => { if ((o as THREE.Mesh).isMesh) { const key = o.name && !o.name.startsWith('mesh_') ? o.name : o.parent?.name || o.name; nodes.set(key, o as THREE.Mesh); } });
      for (const structure of withAssets.filter((s) => s.asset!.file === file)) {
        const src = nodes.get(structure.asset!.node);
        if (!src) continue;
        const geometry = toFloatGeometry(src.geometry);
        geometry.applyMatrix4(src.matrixWorld);
        geometry.computeBoundingBox(); geometry.computeBoundingSphere();
        const material = new THREE.MeshStandardMaterial({ color: COLOURS[structure.system], roughness: 0.72, metalness: 0, side: THREE.DoubleSide });
        const mesh = new THREE.Mesh(geometry, material);
        mesh.name = structure.id;
        this.root.add(mesh);
        this.entries.set(structure.id, { structure, mesh, baseOpacity: 1 });
        this.objectToId.set(mesh, structure.id);
      }
    }
    this.refreshMaterials();
    this.fitAll(false);
    this.render();
  }

  private onResize() {
    const w = Math.max(1, this.container.clientWidth), h = Math.max(1, this.container.clientHeight);
    this.camera.aspect = w / h; this.camera.updateProjectionMatrix(); this.renderer.setSize(w, h, false); this.render();
  }

  private pick = (ev: PointerEvent) => {
    const rect = this.renderer.domElement.getBoundingClientRect();
    this.pointer.set(((ev.clientX - rect.left) / rect.width) * 2 - 1, -((ev.clientY - rect.top) / rect.height) * 2 + 1);
    this.raycaster.setFromCamera(this.pointer, this.camera);
    const visible = [...this.entries.values()].map((e) => e.mesh).filter((m) => m.visible);
    const hit = this.raycaster.intersectObjects(visible, false)[0];
    this.onSelect(hit ? this.objectToId.get(hit.object) ?? null : null);
  };

  setTheme(dark: boolean) {
    this.renderer.setClearColor(dark ? 0x111317 : 0xebe8e1, 1);
    this.render();
  }

  setSelected(id: string | null) { this.selected = id; this.refreshMaterials(); }
  setLayer(system: SystemId, state: LayerState) { this.layers[system] = state; this.refreshMaterials(); }
  setHidden(id: string, hidden: boolean) { hidden ? this.hidden.add(id) : this.hidden.delete(id); this.refreshMaterials(); }
  isHidden(id: string) { return this.hidden.has(id); }

  private refreshMaterials() {
    for (const [id, e] of this.entries) {
      const state = this.layers[e.structure.system];
      e.mesh.visible = state !== 'off' && !this.hidden.has(id);
      const mat = e.mesh.material as THREE.MeshStandardMaterial;
      const selected = id === this.selected;
      mat.color.setHex(selected ? 0xf2b84b : COLOURS[e.structure.system]);
      mat.emissive.setHex(selected ? 0x4a2b00 : 0x000000);
      const opacity = state === 'ghost' ? 0.16 : selected ? 1 : e.baseOpacity;
      mat.opacity = opacity; mat.transparent = opacity < 1; mat.depthWrite = opacity > 0.4;
      mat.clippingPlanes = this.clipEnabled ? [this.clipPlane] : [];
      mat.needsUpdate = true;
    }
    this.render();
  }

  focus(id: string) {
    const e = this.entries.get(id); if (!e) return;
    const box = new THREE.Box3().setFromObject(e.mesh); this.fitBox(box, true);
  }
  fitAll(animate = true) {
    const box = new THREE.Box3();
    for (const e of this.entries.values()) if (e.mesh.visible) box.expandByObject(e.mesh);
    if (!box.isEmpty()) this.fitBox(box, animate);
  }
  private fitBox(box: THREE.Box3, _animate: boolean) {
    const centre = box.getCenter(new THREE.Vector3()); const size = box.getSize(new THREE.Vector3());
    const radius = Math.max(size.x, size.y, size.z) * 0.64 || 1;
    const distance = radius / Math.tan(THREE.MathUtils.degToRad(this.camera.fov / 2)) * 1.22;
    const dir = this.camera.position.clone().sub(this.controls.target).normalize();
    if (!Number.isFinite(dir.x) || dir.lengthSq() < 0.1) dir.copy(DEFAULT_VIEW).normalize();
    this.controls.target.copy(centre); this.camera.position.copy(centre).addScaledVector(dir, distance);
    this.camera.near = Math.max(0.01, distance / 100); this.camera.far = distance * 20; this.camera.updateProjectionMatrix();
    this.controls.update(); this.render();
  }
  setView(view: 'front'|'left'|'right'|'superior'|'inferior'|'three-quarter') {
    const box = new THREE.Box3(); for (const e of this.entries.values()) if (e.mesh.visible) box.expandByObject(e.mesh);
    if (box.isEmpty()) return;
    const c=box.getCenter(new THREE.Vector3()), size=box.getSize(new THREE.Vector3()), r=Math.max(size.x,size.y,size.z)*2.2;
    const dirs={front:new THREE.Vector3(0,0,1),left:new THREE.Vector3(-1,0,0),right:new THREE.Vector3(1,0,0),superior:new THREE.Vector3(0,1,0),inferior:new THREE.Vector3(0,-1,0),'three-quarter':DEFAULT_VIEW.clone()} as const;
    this.controls.target.copy(c); this.camera.position.copy(c).addScaledVector(dirs[view].clone().normalize(),r); this.camera.up.set(0,1,0); this.controls.update(); this.fitAll(false);
  }
  setClip(enabled: boolean, axis: 'sagittal'|'coronal'|'axial', offset: number) {
    this.clipEnabled=enabled;
    const normals={sagittal:new THREE.Vector3(1,0,0),coronal:new THREE.Vector3(0,0,1),axial:new THREE.Vector3(0,1,0)};
    const box=new THREE.Box3(); for(const e of this.entries.values()) box.expandByObject(e.mesh);
    const c=box.getCenter(new THREE.Vector3()), sz=box.getSize(new THREE.Vector3()); const n=normals[axis];
    const span=axis==='sagittal'?sz.x:axis==='coronal'?sz.z:sz.y;
    this.clipPlane.set(n, -(c.dot(n)+offset*span*0.5)); this.refreshMaterials();
  }
  hasGeometry(id: string) { return this.entries.has(id); }
  render() { if (!this.renderer) return; this.renderer.render(this.scene,this.camera); }
  start() { const loop=()=>{this.controls.update(); this.renderer.render(this.scene,this.camera); this.raf=requestAnimationFrame(loop)}; loop(); }
  dispose() { cancelAnimationFrame(this.raf); this.resize?.disconnect(); this.renderer.domElement.removeEventListener('pointerup',this.pick); this.controls.dispose(); for(const e of this.entries.values()){e.mesh.geometry.dispose();(e.mesh.material as THREE.Material).dispose()} this.renderer.dispose(); this.renderer.domElement.remove(); }
}
