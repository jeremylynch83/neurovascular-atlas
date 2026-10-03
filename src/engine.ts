import * as THREE from 'three';
import { GLTFLoader } from 'three/examples/jsm/loaders/GLTFLoader.js';
import { MeshoptDecoder } from 'three/examples/jsm/libs/meshopt_decoder.module.js';
import { OrbitControls } from 'three/examples/jsm/controls/OrbitControls.js';
import type { AnatomyManifest, LayerState, Structure, SystemId } from './types';
import { anatomicalView, coordinateSystem, sectionNormal, type AnatomicalView, type SectionAxis } from './coordinates';

const COLOURS: Record<SystemId, number> = { bone: 0xd9d1c0, artery: 0xc4433c, vein: 0x416aa8, brain: 0xc5a7a1 };

type Entry = { structure: Structure; mesh: THREE.Mesh; baseOpacity: number; batch?: { mesh: THREE.BatchedMesh; instanceId: number } };

function gltfNameCandidates(name: string): string[] {
  // GLTFLoader sanitises node names through PropertyBinding.sanitizeNodeName().
  // Stable anatomy IDs deliberately contain dots, so look up both the original
  // GLB name and the Three.js-sanitised runtime name.
  const safe = THREE.PropertyBinding.sanitizeNodeName(name);
  return safe === name ? [name] : [name, safe];
}

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

export function pickAnatomy(raycaster: THREE.Raycaster, entries: Entry[], layers: Record<SystemId, LayerState>, clip: THREE.Plane | null) {
  const selectable = entries
    .filter(e => e.mesh.visible && !(e.structure.system === 'bone' && layers.bone === 'ghost'))
    .map(e => e.mesh);
  return raycaster.intersectObjects(selectable, false)
    .find(hit => !clip || clip.distanceToPoint(hit.point) >= 0);
}

export class AnatomyEngine {
  private container: HTMLElement;
  private manifest: AnatomyManifest;
  private scene = new THREE.Scene();
  private camera = new THREE.PerspectiveCamera(35, 1, 0.01, 1000);
  private renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
  private controls: OrbitControls;
  private root = new THREE.Group();
  private landmarkMarker = new THREE.Group();
  private entries = new Map<string, Entry>();
  private vascularBatches: THREE.BatchedMesh[] = [];
  private objectToId = new Map<THREE.Object3D, string>();
  private loader = new GLTFLoader();
  private raycaster = new THREE.Raycaster();
  private pointer = new THREE.Vector2();
  private resize?: ResizeObserver;
  private raf = 0;
  private started = false;
  private renderRequested = false;
  private bounds = new THREE.Box3();
  private cameraInteracting = false;
  private qualityRestoreAt = 0;
  private selected: string | null = null;
  private hidden = new Set<string>();
  private layers: Record<SystemId, LayerState> = { bone: 'ghost', artery: 'on', vein: 'off', brain: 'off' };
  private clipPlane = new THREE.Plane(new THREE.Vector3(1, 0, 0), 0);
  private clipEnabled = false;
  private onSelect: (id: string | null) => void;
  private onFps?: (fps: number | null) => void;
  private fpsStart: number | null = null;
  private fpsFrames = 0;
  private fpsLastFrame = 0;
  private displayedFps: number | null = null;
  private disposed = false;

  constructor(container: HTMLElement, manifest: AnatomyManifest, onSelect: (id: string | null) => void, onFps?: (fps: number | null) => void) {
    this.container = container;
    this.manifest = manifest;
    const initialView = anatomicalView(coordinateSystem(manifest), 'three-quarter');
    this.camera.up.fromArray(initialView.up);
    this.camera.position.fromArray(initialView.direction);
    this.onSelect = onSelect;
    this.onFps = onFps;
    this.loader.setMeshoptDecoder(MeshoptDecoder);
    this.renderer.setPixelRatio(Math.min(devicePixelRatio, 2));
    this.renderer.outputColorSpace = THREE.SRGBColorSpace;
    this.renderer.localClippingEnabled = true;
    this.renderer.domElement.className = 'atlas-canvas';
    this.renderer.domElement.tabIndex = 0;
    this.container.appendChild(this.renderer.domElement);
    this.scene.add(this.root);
    this.root.add(this.landmarkMarker);
    this.scene.add(new THREE.HemisphereLight(0xffffff, 0x8d877d, 2.2));
    const key = new THREE.DirectionalLight(0xffffff, 2.7); key.position.set(4, 7, 6); this.scene.add(key);
    const fill = new THREE.DirectionalLight(0xdde6ff, 1.1); fill.position.set(-5, 1, -3); this.scene.add(fill);
    this.controls = this.makeControls();
    this.renderer.domElement.addEventListener('pointerup', this.pick);
    this.resize = new ResizeObserver(() => this.onResize());
    this.resize.observe(container);
    this.onResize();
  }

  private makeControls() {
    const controls = new OrbitControls(this.camera, this.renderer.domElement);
    controls.enableDamping = true;
    controls.dampingFactor = 0.08;
    controls.addEventListener('start', () => {
      this.cameraInteracting = true;
      if (this.useMotionResolution()) this.render();
    });
    controls.addEventListener('end', () => {
      this.cameraInteracting = false;
      this.qualityRestoreAt = performance.now() + 180;
    });
    controls.addEventListener('change', () => {
      this.useMotionResolution();
      this.render();
    });
    return controls;
  }

  private useMotionResolution() {
    // Keep resolution low through drag/zoom and the remaining damping glide.
    this.qualityRestoreAt = performance.now() + 180;
    const ratio = Math.min(devicePixelRatio, 1);
    if (this.renderer.getPixelRatio() === ratio) return false;
    this.renderer.setPixelRatio(ratio);
    return true;
  }

  private restoreSettledResolution() {
    if (this.cameraInteracting || !this.qualityRestoreAt || performance.now() < this.qualityRestoreAt) return;
    this.qualityRestoreAt = 0;
    const ratio = Math.min(devicePixelRatio, 2);
    if (this.renderer.getPixelRatio() !== ratio) {
      this.renderer.setPixelRatio(ratio);
      this.render();
    }
  }

  private setCameraUp(up: [number, number, number], reset = false) {
    const next = new THREE.Vector3(...up);
    if (this.camera.up.equals(next) && !reset) return;
    // OrbitControls caches its up-vector quaternion at construction. Recreate
    // it when a view changes the display up direction, and clear residual drag
    // damping so a view-button click snaps to the requested orientation.
    const target = this.controls.target.clone();
    this.controls.dispose();
    this.camera.up.copy(next);
    this.controls = this.makeControls();
    this.controls.target.copy(target);
  }

  async load(): Promise<void> {
    const withAssets = this.manifest.structures.filter((s) => s.asset);
    const files = [...new Set(withAssets.map((s) => s.asset!.file))];
    for (const file of files) {
      const revision = this.manifest.assetRevisions?.[file] ?? this.manifest.release;
      const gltf = await this.loader.loadAsync(`${import.meta.env.BASE_URL}anatomy/${file}?v=${encodeURIComponent(revision)}`);
      if (this.disposed) {
        gltf.scene.traverse((o) => { if ((o as THREE.Mesh).isMesh) (o as THREE.Mesh).geometry.dispose(); });
        return;
      }
      gltf.scene.updateMatrixWorld(true);
      const nodes = new Map<string, THREE.Mesh>();
      const parser = gltf.parser as unknown as {
        json?: { nodes?: Array<{ name?: string }> };
        associations?: Map<THREE.Object3D, { nodes?: number }>;
      };
      gltf.scene.traverse((o) => {
        if (!(o as THREE.Mesh).isMesh) return;
        const mesh = o as THREE.Mesh;
        // GLTFLoader sanitises Object3D.name (notably removing dots from our
        // stable anatomy IDs). Recover the original glTF node name through the
        // parser association where possible, and also index runtime/sanitised
        // names as fallbacks. This lets already-built TopBrain GLBs load without
        // rebuilding the 2 GB source dataset or regenerating the reference case.
        let cursor: THREE.Object3D | null = o;
        while (cursor) {
          const assoc = parser.associations?.get(cursor);
          if (assoc?.nodes !== undefined) {
            const original = parser.json?.nodes?.[assoc.nodes]?.name;
            if (original) nodes.set(original, mesh);
            break;
          }
          cursor = cursor.parent;
        }
        if (o.name) nodes.set(o.name, mesh);
        if (o.parent?.name) nodes.set(o.parent.name, mesh);
      });
      const unresolved: string[] = [];
      for (const structure of withAssets.filter((s) => s.asset!.file === file)) {
        const src = gltfNameCandidates(structure.asset!.node).map((name) => nodes.get(name)).find(Boolean);
        if (!src) { unresolved.push(structure.asset!.node); continue; }
        const geometry = toFloatGeometry(src.geometry);
        geometry.applyMatrix4(src.matrixWorld);
        // Trimesh-generated TopBrain GLBs contain positions/indices but may not
        // carry a NORMAL accessor. MeshStandardMaterial then receives zero/default
        // normals and the scan-derived surfaces can appear effectively invisible.
        // Compute normals after baking the node transform so lighting is correct.
        if (!geometry.getAttribute('normal')) geometry.computeVertexNormals();
        geometry.computeBoundingBox(); geometry.computeBoundingSphere();
        this.bounds.union(geometry.boundingBox!);
        const skullContext = structure.system === 'bone' && structure.provenance.sourceType === 'legacy-placeholder';
        const material = new THREE.MeshStandardMaterial({ color: structure.color ?? COLOURS[structure.system], roughness: structure.system === 'bone' ? 0.72 : 0.37, metalness: 0, side: skullContext ? THREE.FrontSide : THREE.DoubleSide });
        const mesh = new THREE.Mesh(geometry, material);
        mesh.name = structure.id;
        this.root.add(mesh);
        this.entries.set(structure.id, { structure, mesh, baseOpacity: 1 });
        this.objectToId.set(mesh, structure.id);
      }
      if (unresolved.length) {
        console.warn(`Could not resolve ${unresolved.length} GLB node(s) in ${file}:`, unresolved);
      }
    }
    if (withAssets.length > 0 && this.entries.size === 0) {
      throw new Error(`The manifest declares ${withAssets.length} geometry assets, but none could be matched to GLB nodes. Check GLB node naming/manifest integration.`);
    }
    this.buildVascularBatches();
    this.refreshMaterials();
    this.fitAll(false);
    this.render();
  }

  private buildVascularBatches() {
    // Without native multi-draw, retain the original path rather than add
    // batching texture work to millions of vertices without reducing draws.
    if (!this.renderer.extensions.has('WEBGL_multi_draw')) return;
    const groups = new Map<boolean, Entry[]>();
    for (const e of this.entries.values()) {
      if (e.structure.system !== 'artery' || e.baseOpacity !== 1) continue;
      const indexed = !!e.mesh.geometry.index;
      const group = groups.get(indexed) ?? [];
      group.push(e); groups.set(indexed, group);
    }
    for (const group of groups.values()) {
      if (group.length < 2) continue;
      const vertices = group.reduce((n, e) => n + e.mesh.geometry.getAttribute('position').count, 0);
      const indices = group.reduce((n, e) => n + (e.mesh.geometry.index?.count ?? 0), 0);
      const material = (group[0].mesh.material as THREE.MeshStandardMaterial).clone();
      material.color.setHex(0xffffff);
      material.emissive.setHex(0x000000);
      material.opacity = 1; material.transparent = false; material.depthWrite = true;
      const batch = new THREE.BatchedMesh(group.length, vertices, indices, material);
      batch.name = 'Opaque vasculature';
      for (const e of group) {
        // Copy every position, normal and triangle exactly. The individual
        // mesh stays available for picking, bounds, highlighting and ghosting.
        const instanceId = batch.addInstance(batch.addGeometry(e.mesh.geometry));
        batch.setColorAt(instanceId, new THREE.Color(e.structure.color ?? COLOURS[e.structure.system]));
        e.batch = { mesh: batch, instanceId };
      }
      batch.computeBoundingBox(); batch.computeBoundingSphere();
      this.vascularBatches.push(batch); this.root.add(batch);
    }
  }

  private onResize() {
    const w = Math.max(1, this.container.clientWidth), h = Math.max(1, this.container.clientHeight);
    this.camera.aspect = w / h; this.camera.updateProjectionMatrix(); this.renderer.setSize(w, h, false); this.render();
  }

  private pick = (ev: PointerEvent) => {
    const rect = this.renderer.domElement.getBoundingClientRect();
    this.pointer.set(((ev.clientX - rect.left) / rect.width) * 2 - 1, -((ev.clientY - rect.top) / rect.height) * 2 + 1);
    this.raycaster.setFromCamera(this.pointer, this.camera);
    const hit = pickAnatomy(this.raycaster, [...this.entries.values()], this.layers, this.clipEnabled ? this.clipPlane : null);
    this.onSelect(hit ? this.objectToId.get(hit.object) ?? null : null);
  };

  setTheme(dark: boolean) {
    this.renderer.setClearColor(dark ? 0x111317 : 0xebe8e1, 1);
    this.render();
  }

  private clearLandmarkMarker() {
    this.landmarkMarker.traverse(o => {
      const item = o as THREE.Mesh;
      item.geometry?.dispose();
      const material = item.material as THREE.Material & { map?: THREE.Texture } | undefined;
      material?.map?.dispose();
      material?.dispose();
    });
    this.landmarkMarker.clear();
  }

  setSelected(id: string | null) {
    this.selected = id;
    this.clearLandmarkMarker();
    const s = this.manifest.structures.find(s => s.id === id);
    const landmark = s?.landmark;
    if (landmark?.point) {
      const colour = landmark.status === 'visible' ? 0x75d3cc : 0xf2b84b;
      const dot = new THREE.Mesh(new THREE.SphereGeometry(0.6, 12, 8), new THREE.MeshBasicMaterial({color: colour, depthTest: false}));
      dot.position.fromArray(landmark.point); dot.renderOrder = 20;
      this.landmarkMarker.add(dot);
      if (landmark.course.length > 1) {
        const geometry = new THREE.BufferGeometry().setFromPoints(landmark.course.map(p => new THREE.Vector3(...p)));
        const line = new THREE.Line(geometry, new THREE.LineDashedMaterial({color: colour, dashSize: 1, gapSize: 0.65, depthTest: false}));
        line.computeLineDistances(); line.renderOrder = 20;
        this.landmarkMarker.add(line);
      }
      const canvas = document.createElement('canvas'); canvas.width = 768; canvas.height = 96;
      const ctx = canvas.getContext('2d');
      if (ctx) {
        ctx.fillStyle = 'rgba(17,19,23,0.9)'; ctx.fillRect(0,0,768,96);
        ctx.fillStyle = '#f5efe2'; ctx.font = '26px sans-serif'; ctx.textAlign = 'center';
        ctx.fillText(s!.name,384,35,748); ctx.fillStyle = '#e4bf80'; ctx.font = '21px sans-serif';
        ctx.fillText(landmark.status === 'visible' ? 'Opening landmark' : 'Estimated region · lumen not verified',384,72,748);
        const texture = new THREE.CanvasTexture(canvas);
        const label = new THREE.Sprite(new THREE.SpriteMaterial({map:texture,depthTest:false,depthWrite:false}));
        label.position.fromArray(landmark.point); label.position.z += 5; label.scale.set(38,4.75,1); label.renderOrder = 21;
        this.landmarkMarker.add(label);
      }
    }
    this.refreshMaterials();
  }
  setLayers(layers: Record<SystemId, LayerState>) {
    if ((Object.keys(layers) as SystemId[]).every(system => this.layers[system] === layers[system])) return;
    this.layers = { ...layers };
    this.refreshMaterials();
  }
  setHiddenIds(ids: ReadonlySet<string>) { this.hidden = new Set(ids); this.refreshMaterials(); }

  private refreshMaterials() {
    this.landmarkMarker.visible = this.layers.bone !== 'off' && !!this.selected && !this.hidden.has(this.selected);
    for (const [id, e] of this.entries) {
      const state = this.layers[e.structure.system];
      e.mesh.visible = state !== 'off' && !this.hidden.has(id);
      const mat = e.mesh.material as THREE.MeshStandardMaterial;
      const selected = id === this.selected || e.structure.segmentOf === this.selected;
      mat.color.set(selected ? 0xf2b84b : e.structure.color ?? COLOURS[e.structure.system]);
      mat.emissive.setHex(selected ? 0x4a2b00 : 0x000000);
      const skullContext = e.structure.system === 'bone' && e.structure.provenance.sourceType === 'legacy-placeholder';
      const craniofacial = /mandib|maxill|tooth-/.test(e.structure.asset?.node ?? '');
      const opacity = state === 'ghost' ? (craniofacial ? 0.25 : skullContext ? 0.11 : 0.16) : selected ? 1 : e.baseOpacity;
      const transparent = opacity < 1;
      if (mat.transparent !== transparent) { mat.transparent = transparent; mat.needsUpdate = true; }
      mat.opacity = opacity; mat.depthWrite = opacity > 0.4;
      this.updateClipping(mat);
      if (e.batch) {
        const useBatch = e.mesh.visible && !selected && !transparent;
        e.batch.mesh.setVisibleAt(e.batch.instanceId, useBatch);
        // Detached meshes remain the authoritative per-structure pick/bounds
        // proxies. Only highlighted or transparent meshes render separately.
        if (useBatch) {
          if (e.mesh.parent === this.root) this.root.remove(e.mesh);
        } else if (e.mesh.parent !== this.root) this.root.add(e.mesh);
      }
    }
    for (const batch of this.vascularBatches) {
      batch.visible = this.layers.artery === 'on';
      this.updateClipping(batch.material as THREE.Material);
    }
    this.render();
  }

  private updateClipping(material: THREE.Material) {
    const planeCount = this.clipEnabled ? 1 : 0;
    if ((material.clippingPlanes?.length ?? 0) === planeCount) return;
    material.clippingPlanes = this.clipEnabled ? [this.clipPlane] : [];
    material.needsUpdate = true;
  }

  focus(id: string) {
    const landmark = this.manifest.structures.find(s => s.id === id)?.landmark;
    if (landmark?.point) {
      const box = new THREE.Box3().setFromCenterAndSize(new THREE.Vector3(...landmark.point), new THREE.Vector3(38,38,38));
      for (const p of landmark.course) box.expandByPoint(new THREE.Vector3(...p));
      this.fitBox(box,true); return;
    }
    const box = new THREE.Box3();
    for (const [key, e] of this.entries) if (key === id || e.structure.segmentOf === id) box.expandByObject(e.mesh);
    if (!box.isEmpty()) this.fitBox(box, true);
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
    if (!Number.isFinite(dir.x) || dir.lengthSq() < 0.1) dir.fromArray(anatomicalView(coordinateSystem(this.manifest), 'three-quarter').direction).normalize();
    this.controls.target.copy(centre); this.camera.position.copy(centre).addScaledVector(dir, distance);
    this.camera.near = Math.max(0.01, distance / 100); this.camera.far = distance * 20; this.camera.updateProjectionMatrix();
    this.controls.update(); this.render();
  }
  setView(view: AnatomicalView) {
    const box = new THREE.Box3(); for (const e of this.entries.values()) if (e.mesh.visible) box.expandByObject(e.mesh);
    if (box.isEmpty()) return;
    const c=box.getCenter(new THREE.Vector3()), size=box.getSize(new THREE.Vector3()), r=Math.max(size.x,size.y,size.z)*2.2;
    const orientation = anatomicalView(coordinateSystem(this.manifest), view);
    this.controls.target.copy(c);
    this.camera.position.copy(c).addScaledVector(new THREE.Vector3(...orientation.direction).normalize(), r);
    this.setCameraUp(orientation.up, true);
    this.controls.update(); this.fitAll(false);
  }
  fitCraniofacial() {
    const box = new THREE.Box3();
    for (const e of this.entries.values()) {
      if (e.mesh.visible && /mandib|maxill|tooth-/.test(e.structure.asset?.node ?? '')) box.expandByObject(e.mesh);
    }
    if (box.isEmpty()) return;
    const centre=box.getCenter(new THREE.Vector3());
    const view=anatomicalView(coordinateSystem(this.manifest), 'front');
    this.controls.target.copy(centre);
    this.camera.position.copy(centre).addScaledVector(new THREE.Vector3(...view.direction), 500);
    this.setCameraUp(view.up, true);
    this.fitBox(box, false);
  }
  setClip(enabled: boolean, axis: SectionAxis, offset: number) {
    this.clipEnabled=enabled;
    const box=this.bounds;
    const c=box.getCenter(new THREE.Vector3()), sz=box.getSize(new THREE.Vector3());
    const n = new THREE.Vector3(...sectionNormal(coordinateSystem(this.manifest), axis));
    const span = Math.abs(n.x)*sz.x + Math.abs(n.y)*sz.y + Math.abs(n.z)*sz.z;
    this.clipPlane.set(n, -(c.dot(n)+offset*span*0.5));
    for (const e of this.entries.values()) this.updateClipping(e.mesh.material as THREE.Material);
    for (const batch of this.vascularBatches) this.updateClipping(batch.material as THREE.Material);
    this.render();
  }
  hasGeometry(id: string) { return this.entries.has(id) || [...this.entries.values()].some(e => e.structure.segmentOf === id); }
  // All changes in one browser frame share one render, including React effects
  // and OrbitControls damping. Idle controls still tick without redrawing.
  render() { if (this.disposed) return; this.renderRequested = true; this.requestFrame(); }
  private requestFrame() { if (!this.raf) this.raf = requestAnimationFrame(this.tick); }
  private updateFps(now: number, rendered: boolean) {
    if (!this.onFps) return;
    if (rendered) {
      this.fpsLastFrame = now;
      if (this.fpsStart === null) { this.fpsStart = now; return; }
      this.fpsFrames++;
      const elapsed = now - this.fpsStart;
      if (elapsed < 500) return;
      const fps = Math.round(this.fpsFrames * 1000 / elapsed);
      if (fps !== this.displayedFps) { this.displayedFps = fps; this.onFps(fps); }
      this.fpsStart = now; this.fpsFrames = 0;
    } else if (this.fpsStart !== null && now - this.fpsLastFrame >= 500) {
      this.fpsStart = null; this.fpsFrames = 0;
      if (this.displayedFps !== null) { this.displayedFps = null; this.onFps(null); }
    }
  }
  private tick = () => {
    if (this.disposed) return;
    if (this.started) this.controls.update();
    this.restoreSettledResolution();
    const rendered = this.renderRequested;
    const frameTime = performance.now();
    if (rendered) {
      this.renderRequested = false;
      this.renderer.render(this.scene, this.camera);
    }
    if (this.started) this.updateFps(frameTime, rendered);
    this.raf = 0;
    if (this.started || this.renderRequested) this.requestFrame();
  };
  start() { if (this.disposed) return; this.started = true; this.render(); }
  dispose() { this.disposed = true; cancelAnimationFrame(this.raf); this.resize?.disconnect(); this.renderer.domElement.removeEventListener('pointerup',this.pick); this.controls.dispose(); this.clearLandmarkMarker(); for(const e of this.entries.values()){e.mesh.geometry.dispose();(e.mesh.material as THREE.Material).dispose()} for(const batch of this.vascularBatches){batch.dispose();(batch.material as THREE.Material).dispose()} this.renderer.dispose(); this.renderer.domElement.remove(); }
}
