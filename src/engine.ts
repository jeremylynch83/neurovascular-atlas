import * as THREE from 'three';
import { SelectionHalo, selectionHaloFade } from './selectionHalo';
import { bindSelectionGesture } from './selectionGesture';
import { RotationCentring } from './rotationCentring';
import { OrbitControls } from 'three/examples/jsm/controls/OrbitControls.js';
import type { AnatomyManifest, LayerState, Structure, SystemId } from './types';
import { focusGeometryMembers, segmentGeometryMembers } from './catalogue';
import { resolveSurfaceAnchor } from './brainAnchors';
import { anatomicalView, coordinateSystem, sectionNormal, type AnatomicalView, type SectionAxis } from './coordinates';
import { DsaRenderer, loadInjectionFlow } from './dsaRenderer';
import { injectionOnPath,type FlowData,type InjectionPoint } from './flowGeometry';
import type { DsaRun } from './dsa';
import { StagedLoader, type PreparedMesh } from './stagedLoading';
import { WorkerGeometrySource } from './geometrySource';

const COLOURS: Record<SystemId, number> = { bone: 0xd9d1c0, artery: 0xc4433c, vein: 0x416aa8, brain: 0xc5a7a1 };
const SELECTION_COLOUR = new THREE.Color(0xe99a42).multiplyScalar(1.1);
const SELECTION_EMISSIVE = 0xb56828;
const SELECTION_GLOW = 0.08;

function structureColour(structure: Structure): number | string {
  return structure.system === 'artery' || structure.system === 'vein'
    ? COLOURS[structure.system]
    : structure.color ?? COLOURS[structure.system];
}

type Entry = { structure: Structure; mesh: THREE.Mesh; baseOpacity: number; opaqueMaterial?: THREE.MeshStandardMaterial; ghostMaterial?: THREE.MeshLambertMaterial; batch?: { mesh: THREE.BatchedMesh; instanceId: number } };

export function pickAnatomy(raycaster: THREE.Raycaster, entries: Entry[], layers: Record<SystemId, LayerState>, clip: THREE.Plane | null, visibility?: ReadonlyMap<string, LayerState>) {
  const selectable = entries
    .filter(e => e.mesh.visible && !(['bone', 'brain'].includes(e.structure.system) && (visibility?.get(e.structure.id) ?? layers[e.structure.system]) === 'ghost'))
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
  private rotationCentring: RotationCentring;
  private root = new THREE.Group();
  private landmarkMarker = new THREE.Group();
  private entries = new Map<string, Entry>();
  private segmentMembers: Map<string, Set<string>>;
  private vascularBatches: THREE.BatchedMesh[] = [];
  private objectToId = new Map<THREE.Object3D, string>();
  private loading: StagedLoader | null = null;
  private downloads = new Map<string, number>();
  private interacting = false;
  private nextBackgroundSlot = 0;
  private lastRenderDuration = 0;
  private frameInterval = 16.7;
  private previousFrameTime = 0;
  private userChangedView = false;
  private vertexBudget = 30_000;
  private primaryPrepared = false;
  private workWaiters = new Set<() => void>();
  onInteraction?: () => void;
  private raycaster = new THREE.Raycaster();
  private pointer = new THREE.Vector2();
  private disposeSelectionGesture: () => void;
  private resize?: ResizeObserver;
  private raf = 0;
  private started = false;
  private paused = false;
  private renderRequested = false;
  private bounds = new THREE.Box3();
  private selected: string | null = null;
  private tappedPivot: { id: string; point: THREE.Vector3 } | null = null;
  private selectionHalo = new SelectionHalo(this.renderer, SELECTION_COLOUR);
  private selectionStarted = 0;
  private lastSelectionFrame = 0;
  private reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)');
  private mobileView = window.matchMedia('(max-width: 680px)');
  private focusedMembers: Set<string> | null = null;
  private hidden = new Set<string>();
  private visibility = new Map<string, LayerState>();
  private focusDistanceFloor = 0;
  private layers: Record<SystemId, LayerState> = { bone: 'ghost', artery: 'on', vein: 'off', brain: 'off' };
  private clipPlane = new THREE.Plane(new THREE.Vector3(1, 0, 0), 0);
  private clipEnabled = false;
  private onSelect: (id: string | null, dsa?: boolean) => void;
  private onFps?: (fps: number | null) => void;
  private fpsStart: number | null = null;
  private fpsFrames = 0;
  private fpsLastFrame = 0;
  private displayedFps: number | null = null;
  private disposed = false;
  private dsaRenderer: DsaRenderer | null = null;
  private injectionFlow: FlowData | null = null;
  private flowRequest: Promise<FlowData> | null = null;
  private dsaRequest: Promise<DsaRenderer> | null = null;
  private dsaTime = 2;
  private dsaArteries = new Set<string>();
  private dsaView: { camera: THREE.PerspectiveCamera; target: THREE.Vector3; focusFloor: number } | null = null;
  private injectionVessel: string|null=null;
  private injectionPick: ((id:string,point:InjectionPoint|null)=>void)|null=null;
  private dsaRevision=0;
  private movingUntil = 0;

  constructor(container: HTMLElement, manifest: AnatomyManifest, onSelect: (id: string | null, dsa?: boolean) => void, onFps?: (fps: number | null) => void) {
    this.container = container;
    this.manifest = manifest;
    this.segmentMembers = segmentGeometryMembers(manifest.structures);
    const initialView = anatomicalView(coordinateSystem(manifest), 'front');
    this.camera.up.fromArray(initialView.up);
    this.camera.position.fromArray(initialView.direction);
    this.onSelect = onSelect;
    this.onFps = onFps;
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
    this.rotationCentring = new RotationCentring(this.renderer.domElement);
    this.disposeSelectionGesture = bindSelectionGesture(this.renderer.domElement, this.pick);
    this.resize = new ResizeObserver(() => this.onResize());
    this.resize.observe(container);
    this.reducedMotion.addEventListener('change', this.onMotionPreference);
    this.onResize();
  }

  private makeControls() {
    this.interacting = false;
    const controls = new OrbitControls(this.camera, this.renderer.domElement);
    controls.enableDamping = true;
    controls.dampingFactor = 0.08;
    controls.addEventListener('start', () => {
      this.focusDistanceFloor = 0;
      this.interacting = true; this.userChangedView = true; this.onInteraction?.();
    });
    controls.addEventListener('end', () => { this.interacting = false; this.movingUntil = performance.now() + 180; });
    controls.addEventListener('change', () => { this.movingUntil = performance.now() + 180; this.render(); });
    return controls;
  }

  private setCameraUp(up: [number, number, number], reset = false) {
    this.rotationCentring.reset();
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

  async load(onChange?: () => void): Promise<void> {
    const source = new WorkerGeometrySource(this.manifest, () => this.vertexBudget, (file, fraction) => {
      if (this.disposed) return;
      this.downloads.set(file, fraction); onChange?.();
    });
    this.loading = new StagedLoader(this.manifest, source,
      async meshes => {
        if (this.disposed) return;
        const start = performance.now(); this.installMeshes(meshes);
        const duration = performance.now() - start;
        if (duration > 2) this.vertexBudget = Math.max(8_000, Math.floor(this.vertexBudget * .65));
        else if (duration < 1) this.vertexBudget = Math.min(50_000, Math.floor(this.vertexBudget * 1.15));
      },
      background => this.workSlot(background), () => { if (!this.disposed) onChange?.(); });
    onChange?.();
    await this.loading.loadCritical();
    if (this.disposed) return;
    await this.buildInitialVascularBatches();
    if (this.disposed) return;
    this.primaryPrepared = true;
    if (!this.userChangedView) {
      const skull = [...this.entries].filter(([, e]) => e.structure.system === 'bone' && e.structure.id !== 'bone.hyoid').map(([id]) => id);
      if (skull.length) {
        this.framePreset(skull, [0, 1, 0]);
        this.userChangedView = false;
      } else this.fitAll(false);
    }
    this.refreshMaterials(); this.render();
    performance.mark('atlas-primary-ready');
    // Resolve primary readiness before running the deferred asset queue.
    setTimeout(() => { if (!this.disposed) this.loading?.startBackground(); }, 0);
  }

  initialDownloadProgress() {
    const files = new Set(this.manifest.structures.filter(s => s.asset && (s.system === 'bone' || s.system === 'artery')).map(s => s.asset!.file));
    let loaded = 0, total = 0;
    for (const file of files) {
      const bytes = this.manifest.assetByteSizes?.[file] ?? 1;
      total += bytes; loaded += bytes * (this.downloads.get(file) ?? 0);
    }
    return total ? loaded / total : 0;
  }
  getLoadStates() { return this.loading?.states ?? new Map(); }
  ensureGeometry(ids: readonly string[]) { return this.loading?.ensure(ids) ?? Promise.resolve(); }
  vascularGeometryReady() {
    return !!this.loading && this.manifest.structures.filter(s => s.asset && ['artery', 'vein'].includes(s.system))
      .every(s => this.loading!.states.get(s.id)?.status === 'ready');
  }
  private async workSlot(background: boolean) {
    // Every initial packet already yields through the worker message queue.
    // The first scene draw follows framing, avoiding uploads from inside the skull.
    if (!background) return;
    // Resume after a paint, with one bounded packet in flight. During gestures
    // the worker may finish downloading, but no new scene/GPU work is added.
    do {
      await new Promise<void>(resolve => {
        let timer: ReturnType<typeof setTimeout> | undefined;
        const finish = () => { cancelAnimationFrame(frame); clearTimeout(timer); this.workWaiters.delete(finish); resolve(); };
        const frame = requestAnimationFrame(() => { timer = setTimeout(finish, 0); });
        this.workWaiters.add(finish);
      });
    } while (!this.disposed && background && (this.interacting || performance.now() < this.movingUntil || performance.now() < this.nextBackgroundSlot));
    if (background) this.nextBackgroundSlot = performance.now() + Math.min(150, Math.max(0, Math.max(this.lastRenderDuration, this.frameInterval) - 18) * 4);
  }
  private installMeshes(packets: PreparedMesh[]) {
    const added: Entry[] = [];
    for (const packet of packets) {
      if (this.entries.has(packet.id)) continue;
      const structure = this.manifest.structures.find(s => s.id === packet.id)!;
      const geometry = new THREE.BufferGeometry();
      geometry.setAttribute('position', new THREE.BufferAttribute(packet.positions, 3));
      if (packet.normals) geometry.setAttribute('normal', new THREE.BufferAttribute(packet.normals, 3));
      if (packet.indices) geometry.setIndex(new THREE.BufferAttribute(packet.indices, 1));
      geometry.boundingBox = new THREE.Box3(new THREE.Vector3().fromArray(packet.bounds[0]), new THREE.Vector3().fromArray(packet.bounds[1]));
      geometry.boundingSphere = new THREE.Sphere(new THREE.Vector3().fromArray(packet.sphere.centre), packet.sphere.radius);
      this.bounds.union(geometry.boundingBox);
      const skullContext = structure.system === 'bone' && structure.provenance.sourceType === 'legacy-placeholder';
      const material = new THREE.MeshStandardMaterial({ color: structureColour(structure), roughness: structure.system === 'bone' ? 0.72 : 0.37, metalness: 0, side: skullContext ? THREE.FrontSide : THREE.DoubleSide });
      const mesh = new THREE.Mesh(geometry, material); mesh.name = structure.id;
      const entry: Entry = { structure, mesh, baseOpacity: 1, opaqueMaterial: material };
      this.entries.set(structure.id, entry); this.objectToId.set(mesh, structure.id); added.push(entry);
      this.root.add(mesh);
    }
    // Each packet contains at most 16 meshes / 50k vertices (or one larger
    // source mesh). Existing batches and their GPU buffers are never rebuilt.
    if (this.primaryPrepared) this.buildVascularBatches(added);
    this.refreshMaterials(added);
  }

  private buildVascularBatches(entries: Entry[]) {
    for (const _ of this.vascularBatchSteps(entries)) { void _; }
  }
  private async buildInitialVascularBatches() {
    let start = performance.now();
    for (const _ of this.vascularBatchSteps([...this.entries.values()])) {
      void _; if (this.disposed) return;
      if (performance.now() - start > 2) { await new Promise(resolve => setTimeout(resolve, 0)); start = performance.now(); }
    }
  }
  private *vascularBatchSteps(entries: Entry[]) {
    // Without native multi-draw, retain the original path rather than add
    // batching texture work to millions of vertices without reducing draws.
    if (!this.renderer.extensions.has('WEBGL_multi_draw')) return;
    const groups = new Map<string, Entry[]>();
    for (const e of entries) {
      if (!['artery', 'vein'].includes(e.structure.system) || e.baseOpacity !== 1) continue;
      const indexed = !!e.mesh.geometry.index;
      const key = `${e.structure.system}:${indexed}`;
      const group = groups.get(key) ?? [];
      group.push(e); groups.set(key, group);
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
      batch.userData.system = group[0].structure.system;
      for (const e of group) {
        // Copy every position, normal and triangle exactly. The individual
        // mesh stays available for picking, bounds, highlighting and ghosting.
        const instanceId = batch.addInstance(batch.addGeometry(e.mesh.geometry));
        batch.setColorAt(instanceId, new THREE.Color(structureColour(e.structure)));
        e.batch = { mesh: batch, instanceId };
        yield;
      }
      batch.computeBoundingBox(); batch.computeBoundingSphere();
      this.vascularBatches.push(batch); this.root.add(batch);
    }
  }

  private onResize() {
    const w = Math.max(1, this.container.clientWidth), h = Math.max(1, this.container.clientHeight);
    this.selectionHalo.resize(w, h);
    this.camera.aspect = w / h; this.camera.updateProjectionMatrix(); this.renderer.setSize(w, h, false); this.render();
  }

  private pick = (ev: PointerEvent) => {
    const rect = this.renderer.domElement.getBoundingClientRect();
    this.pointer.set(((ev.clientX - rect.left) / rect.width) * 2 - 1, -((ev.clientY - rect.top) / rect.height) * 2 + 1);
    this.raycaster.setFromCamera(this.pointer, this.camera);
    if(this.injectionPick) {
      const hit=pickAnatomy(this.raycaster,[...this.entries.values()].filter(e=>e.structure.system==='artery'),this.layers,null);
      const id=hit?this.objectToId.get(hit.object)!:null;
      const row=id?this.injectionFlow?.entries[id]:undefined;
      if(!id||(this.injectionFlow&&!row?.selectable))return;
      if(id===this.injectionVessel&&row?.selectable)this.injectionPick(id,{id,...injectionOnPath(row,hit!.point.toArray())});
      else if(id!==this.injectionVessel)this.injectionPick(id,null);
      return;
    }
    if (this.dsaView) { this.onSelect(this.dsaRenderer!.pick(this.raycaster,this.dsaTime),true); return; }
    const hit = pickAnatomy(this.raycaster, [...this.entries.values()], this.layers, this.clipEnabled ? this.clipPlane : null, this.visibility);
    const id = hit ? this.objectToId.get(hit.object) ?? null : null;
    this.setSelected(id, hit?.point);
    this.onSelect(id);
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

  setSelected(id: string | null, tappedPoint?: THREE.Vector3) {
    if (id !== this.selected) {
      this.rotationCentring.arm();
      this.tappedPivot = null;
      this.selectionStarted = performance.now();
      this.lastSelectionFrame = 0;
    }
    if (id && tappedPoint) {
      this.tappedPivot = { id, point: tappedPoint.clone() };
      // A fresh point on the same vessel changes the pivot, while preserving
      // cancellation if the user has already deliberately panned this selection.
      this.rotationCentring.reset();
    }
    this.selected = id;
    this.clearLandmarkMarker();
    const s = this.manifest.structures.find(s => s.id === id);
    const landmark = s?.landmark;
    if (landmark?.point) {
      const colour = SELECTION_COLOUR;
      const dot = new THREE.Mesh(new THREE.SphereGeometry(0.6, 12, 8), new THREE.MeshBasicMaterial({color: colour, depthTest: false}));
      const anchoredPoint = s?.surfaceAnchor ? this.resolveBrainAnchor(s.id) : null;
      dot.position.copy(anchoredPoint ?? new THREE.Vector3(...landmark.point)); dot.renderOrder = 20;
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
        ctx.fillStyle = '#f5efe2'; ctx.font = landmark.kind ? '32px sans-serif' : '26px sans-serif'; ctx.textAlign = 'center';
        ctx.fillText(s!.name,384,35,748); ctx.fillStyle = '#e4bf80'; ctx.font = '21px sans-serif';
        ctx.fillText(landmark.kind ? 'Regional vessel course guide' : landmark.status === 'visible' ? 'Opening landmark' : 'Estimated region · lumen not verified',384,72,748);
        const texture = new THREE.CanvasTexture(canvas);
        const label = new THREE.Sprite(new THREE.SpriteMaterial({map:texture,depthTest:false,depthWrite:false}));
        label.position.fromArray(landmark.point); label.position.z += 5;
        label.scale.set(landmark.kind ? 76 : 38, landmark.kind ? 9.5 : 4.75, 1); label.renderOrder = 21;
        this.landmarkMarker.add(label);
      }
    }
    this.refreshMaterials();
  }
  private selectedMidpoint() {
    if (!this.selected) return null;
    const structure = this.manifest.structures.find(s => s.id === this.selected);
    if (structure?.landmark?.point) return this.landmarkMarker.visible
      ? this.resolveBrainAnchor(structure.id) ?? new THREE.Vector3(...structure.landmark.point) : null;
    const box = new THREE.Box3();
    for (const id of this.segmentMembers.get(this.selected) ?? []) {
      const mesh = this.entries.get(id)?.mesh;
      if (mesh?.visible) box.expandByObject(mesh);
    }
    return box.isEmpty() ? null : box.getCenter(new THREE.Vector3());
  }
  private selectedRotationPivot() {
    if (this.tappedPivot?.id === this.selected) return this.entries.get(this.tappedPivot.id)?.mesh.visible
      ? this.tappedPivot.point : null;
    return this.selectedMidpoint();
  }
  setLayers(layers: Record<SystemId, LayerState>) {
    if ((Object.keys(layers) as SystemId[]).every(system => this.layers[system] === layers[system])) return;
    this.layers = { ...layers };
    this.refreshMaterials();
  }
  setHiddenIds(ids: ReadonlySet<string>) { this.hidden = new Set(ids); this.refreshMaterials(); }
  setVisibility(states: ReadonlyMap<string, LayerState>) { this.visibility = new Map(states); this.refreshMaterials(); }
  setFocus(id: string | null) {
    this.focusedMembers = id ? focusGeometryMembers(this.manifest, id) : null;
    this.refreshMaterials();
  }

  private refreshMaterials(only?: Entry[]) {
    const placing=!!this.injectionPick;
    const haloSources: THREE.Mesh[] = [];
    const selectedStructure = this.manifest.structures.find(s => s.id === this.selected);
    const markerState = this.selected ? this.visibility?.get(this.selected) ?? this.layers[selectedStructure?.system ?? 'bone'] : 'off';
    this.landmarkMarker.visible = !placing && markerState !== 'off' && !!this.selected && !this.hidden.has(this.selected);
    const visibleBatches = new Set<THREE.BatchedMesh>();
    for (const e of only ?? this.entries.values()) {
      const id = e.structure.id;
      const state = placing ? (e.structure.system==='artery'?'on':'off') : this.visibility?.get(id) ?? this.layers[e.structure.system];
      e.mesh.visible = state !== 'off' && (placing || !this.hidden.has(id));
      const selected = placing ? id===this.injectionVessel : this.selected !== null && !!this.segmentMembers.get(this.selected)?.has(id);
      const skullContext = e.structure.system === 'bone' && e.structure.provenance.sourceType === 'legacy-placeholder';
      const craniofacial = /mandib|maxill|tooth-/.test(e.structure.asset?.node ?? '');
      const normalOpacity = placing ? 1 : state === 'ghost' ? (craniofacial ? 0.25 : skullContext ? 0.11 : 0.16) : selected ? 1 : e.baseOpacity;
      const opacity = !placing && this.focusedMembers ? (this.focusedMembers.has(id) ? 1 : Math.min(normalOpacity, 0.12)) : normalOpacity;
      const transparent = opacity < 1;
      // Reuse the original geometry; only faint context gets cheaper shading.
      // Cache materials so changing visibility does not repeatedly compile them.
      const opaqueMaterial = e.opaqueMaterial ??= e.mesh.material as THREE.MeshStandardMaterial;
      const mat = transparent
        ? (e.ghostMaterial ??= new THREE.MeshLambertMaterial({ side: opaqueMaterial.side, transparent: true, forceSinglePass: true }))
        : opaqueMaterial;
      e.mesh.material = mat;
      mat.color.set(selected ? SELECTION_COLOUR : structureColour(e.structure));
      mat.emissive.setHex(selected ? SELECTION_EMISSIVE : 0x000000);
      mat.emissiveIntensity = selected ? SELECTION_GLOW : 1;
      if (!placing && selected && e.mesh.visible && opacity > 0) haloSources.push(e.mesh);
      if (mat.transparent !== transparent) { mat.transparent = transparent; mat.needsUpdate = true; }
      mat.opacity = opacity; mat.depthWrite = opacity > 0.4;
      this.updateClipping(mat);
      if (e.batch) {
        const useBatch = e.mesh.visible && state === 'on' && !selected && !transparent;
        if (useBatch) visibleBatches.add(e.batch.mesh);
        e.batch.mesh.setVisibleAt(e.batch.instanceId, useBatch);
        // Detached meshes remain the authoritative per-structure pick/bounds
        // proxies. Only highlighted or transparent meshes render separately.
        if (useBatch) {
          if (e.mesh.parent === this.root) this.root.remove(e.mesh);
        } else if (e.mesh.parent !== this.root) this.root.add(e.mesh);
      }
    }
    for (const batch of only ? new Set(only.flatMap(e => e.batch ? [e.batch.mesh] : [])) : this.vascularBatches) {
      batch.visible = visibleBatches.has(batch);
      this.updateClipping(batch.material as THREE.Material);
    }
    const haloChanged = !only || only.some(e => this.selected !== null && this.segmentMembers.get(this.selected)?.has(e.structure.id));
    if (haloChanged) this.selectionHalo.setMeshes(only ? [...this.entries.values()].filter(e => e.mesh.visible && this.selected !== null && this.segmentMembers.get(this.selected)?.has(e.structure.id) && !placing).map(e => e.mesh) : haloSources);
    if (this.reducedMotion.matches) this.selectionHalo.setFade(0.65);
    this.selectionHalo.setClip(this.clipEnabled && !placing ? [this.clipPlane] : []);
    // Hidden background data do not alter the visible scene or need a redraw.
    if (!only || only.some(e => e.mesh.visible)) this.render();
  }

  private updateClipping(material: THREE.Material) {
    const planeCount = this.clipEnabled && !this.injectionPick ? 1 : 0;
    if ((material.clippingPlanes?.length ?? 0) === planeCount) return;
    material.clippingPlanes = planeCount ? [this.clipPlane] : [];
    material.needsUpdate = true;
  }

  focus(id: string) {
    if (this.tappedPivot?.id === id) this.tappedPivot = null;
    this.userChangedView = true;
    const landmark = this.manifest.structures.find(s => s.id === id)?.landmark;
    if (landmark?.point) {
      const box = new THREE.Box3().setFromCenterAndSize(new THREE.Vector3(...landmark.point), new THREE.Vector3(38,38,38));
      for (const p of landmark.course) box.expandByPoint(new THREE.Vector3(...p));
      this.fitBox(box,true,true); return;
    }
    const box = new THREE.Box3();
    for (const key of this.segmentMembers.get(id) ?? []) {
      const entry = this.entries.get(key);
      if (entry) box.expandByObject(entry.mesh);
    }
    if (!box.isEmpty()) this.fitBox(box, true, true);
  }
  fitAll(animate = true) {
    const box = new THREE.Box3();
    for (const e of this.entries.values()) if (e.mesh.visible) box.expandByObject(e.mesh);
    if (!box.isEmpty()) this.fitBox(box, animate);
  }
  private fitBox(box: THREE.Box3, _animate: boolean, gentle = false) {
    this.rotationCentring.reset();
    const centre = box.getCenter(new THREE.Vector3()); const size = box.getSize(new THREE.Vector3());
    const radius = Math.max(size.x, size.y, size.z) * 0.64 || 1;
    const framingScale = 1.22 / Math.tan(THREE.MathUtils.degToRad(this.camera.fov / 2));
    let distance = radius * framingScale;
    if (gentle) {
      const current = this.camera.position.distanceTo(this.controls.target);
      // Limit automatic magnification to 25%, without accumulating another
      // zoom on each selection. Manual navigation or a whole-scene view resets it.
      this.focusDistanceFloor ||= current * .8;
      const sceneSize = this.bounds.getSize(new THREE.Vector3());
      const context = Math.max(sceneSize.x, sceneSize.y, sceneSize.z) * .35 * .64 * framingScale;
      distance = Math.max(distance, current * .8, this.focusDistanceFloor, context);
    } else this.focusDistanceFloor = 0;
    const dir = this.camera.position.clone().sub(this.controls.target).normalize();
    if (!Number.isFinite(dir.x) || dir.lengthSq() < 0.1) dir.fromArray(anatomicalView(coordinateSystem(this.manifest), 'three-quarter').direction).normalize();
    this.controls.target.copy(centre); this.camera.position.copy(centre).addScaledVector(dir, distance);
    this.camera.near = Math.max(0.01, distance / 100); this.camera.far = distance * 20; this.camera.updateProjectionMatrix();
    this.controls.update(); this.render();
  }
  setView(view: AnatomicalView) {
    this.userChangedView = true;
    const box = new THREE.Box3(); for (const [id,e] of this.entries) if (this.dsaView ? this.dsaArteries.has(id) : e.mesh.visible) box.expandByObject(e.mesh);
    if (box.isEmpty()) return;
    const c=box.getCenter(new THREE.Vector3()), size=box.getSize(new THREE.Vector3()), r=Math.max(size.x,size.y,size.z)*2.2;
    const orientation = anatomicalView(coordinateSystem(this.manifest), view);
    this.controls.target.copy(c);
    this.camera.position.copy(c).addScaledVector(new THREE.Vector3(...orientation.direction).normalize(), r);
    this.setCameraUp(orientation.up, true);
    this.controls.update(); this.fitAll(false);
  }
  /** Frame the preset vessels, independently of the retained skull/brain context. */
  framePreset(ids: readonly string[], rasDirection: [number, number, number]) {
    this.userChangedView = true;
    const box = new THREE.Box3();
    for (const id of ids) {
      const entry = this.entries.get(id);
      if (entry) box.expandByObject(entry.mesh);
    }
    if (box.isEmpty()) return;
    const system = coordinateSystem(this.manifest);
    const direction = new THREE.Vector3(...(system === 'RAS'
      ? rasDirection : [rasDirection[0], rasDirection[2], rasDirection[1]])).normalize();
    const up = new THREE.Vector3(...anatomicalView(system, 'front').up);
    const right = new THREE.Vector3().crossVectors(up, direction).normalize();
    const screenUp = new THREE.Vector3().crossVectors(direction, right).normalize();
    const centre = box.getCenter(new THREE.Vector3());
    const tanVertical = Math.tan(THREE.MathUtils.degToRad(this.camera.fov / 2));
    const tanHorizontal = tanVertical * this.camera.aspect;
    let distance = 1;
    for (const x of [box.min.x, box.max.x]) for (const y of [box.min.y, box.max.y]) for (const z of [box.min.z, box.max.z]) {
      const corner = new THREE.Vector3(x, y, z).sub(centre);
      distance = Math.max(distance, corner.dot(direction) + 1.18 * Math.max(
        Math.abs(corner.dot(right)) / tanHorizontal, Math.abs(corner.dot(screenUp)) / tanVertical));
    }
    this.controls.target.copy(centre);
    this.setCameraUp(anatomicalView(system, 'front').up, true);
    this.camera.position.copy(centre).addScaledVector(direction, distance);
    this.camera.near = Math.max(0.01, distance / 200);
    this.camera.far = Math.max(distance * 20, this.bounds.getSize(new THREE.Vector3()).length() * 4);
    this.camera.updateProjectionMatrix();
    this.focusDistanceFloor = 0;
    this.controls.update(); this.render();
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
    this.selectionHalo.setClip(this.clipEnabled ? [this.clipPlane] : []);
    this.render();
  }
  hasGeometry(id: string) { return [...this.segmentMembers.get(id) ?? []].some(key => this.entries.has(key)); }
  async prepareInjection() {
    if(!this.flowRequest)this.flowRequest=loadInjectionFlow(this.manifest).catch(error=>{this.flowRequest=null;throw error});
    return this.injectionFlow=await this.flowRequest;
  }
  async prepareDsa() {
    await this.ensureGeometry(this.manifest.structures.filter(s => s.asset && ['artery', 'vein'].includes(s.system)).map(s => s.id));
    if (this.disposed) throw new Error('Atlas closed');
    if(!this.dsaRenderer) {
      this.dsaRequest??=(async()=>{
        const flow=await this.prepareInjection();
        const renderer=await DsaRenderer.create(this.renderer,this.manifest,new Map([...this.entries].map(([id,e])=>[id,e.mesh.geometry])),flow);
        if(this.disposed){renderer.dispose();throw Error('Atlas closed while loading injection courses')}
        return renderer;
      })().catch(error=>{this.dsaRequest=null;throw error});
      this.dsaRenderer=await this.dsaRequest;
    }
    return this.dsaRenderer.flow;
  }
  getDsaFlow() { return this.injectionFlow; }
  validateInjectionPoint(point: InjectionPoint) { return this.dsaRenderer!.injectionPoint(point.id,point.point); }
  beginInjectionPlacement(id: string|null,pick:(id:string,point:InjectionPoint|null)=>void) {
    this.dsaRevision++;
    this.dsaView??={camera:this.camera.clone(),target:this.controls.target.clone(),focusFloor:this.focusDistanceFloor};
    this.injectionPick=pick;this.selectInjectionVessel(id);
  }
  selectInjectionVessel(id: string|null) { this.dsaRevision++;this.injectionVessel=id;this.refreshMaterials(); }
  endInjectionPlacement() { this.dsaRevision++;this.injectionPick=null;this.injectionVessel=null;this.refreshMaterials(); }
  async setDsa(run: DsaRun | null) {
    const revision=++this.dsaRevision;
    if (run) {
      await this.prepareDsa();
      if(this.disposed||revision!==this.dsaRevision)return false;
      if(!await this.dsaRenderer!.setRun(run,()=>!this.disposed&&revision===this.dsaRevision))return false;
      this.dsaArteries = new Set(run.arteries);
      this.dsaView ??= { camera: this.camera.clone(), target: this.controls.target.clone(), focusFloor: this.focusDistanceFloor };
    } else {
      this.endInjectionPlacement();
      if(this.dsaView){
      const saved = this.dsaView; this.dsaView = null;
      this.controls.dispose(); this.camera.copy(saved.camera);
      this.camera.aspect = this.container.clientWidth / Math.max(1,this.container.clientHeight); this.camera.updateProjectionMatrix();
      this.controls = this.makeControls(); this.controls.target.copy(saved.target);
      this.focusDistanceFloor = saved.focusFloor; this.controls.update();
      }
    }
    this.render();
    return true;
  }
  setDsaSelected(id: string|null) { this.dsaRenderer?.setSelected(id);this.render(); }
  setDsaTime(time: number) { this.dsaTime = time; this.render(); }
  resolveBrainAnchor(id: string): THREE.Vector3 | null {
    const anchor = this.manifest.structures.find(s => s.id === id)?.surfaceAnchor;
    const registration = this.manifest.brainRegistration;
    if (!anchor || !registration) return null;
    if (anchor.registrationId !== registration.id) throw new Error('Brain anchor registration mismatch');
    const entry = this.entries.get(anchor.structureId);
    return entry ? resolveSurfaceAnchor(anchor, entry.mesh.geometry, registration.registeredAssetSha256) : null;
  }
  // All changes in one browser frame share one render, including React effects
  // and OrbitControls damping. Idle controls still tick without redrawing.
  render() { if (this.disposed) return; this.renderRequested = true; this.requestFrame(); }
  private requestFrame() { if (!this.paused && !this.raf) this.raf = requestAnimationFrame(this.tick); }
  setPaused(paused: boolean) {
    this.paused = paused;
    if (paused) { cancelAnimationFrame(this.raf); this.raf = 0; }
    else this.render();
  }
  private onMotionPreference = () => {
    this.lastSelectionFrame = 0;
    this.selectionHalo.setFade(this.reducedMotion.matches ? 0.65 : selectionHaloFade(performance.now() - this.selectionStarted));
    this.render();
  };
  private updateSelectionGlow(now: number) {
    if (!this.selectionHalo.active || this.reducedMotion.matches || document.hidden) return;
    // A smooth six-second fade affects only the surrounding halo.
    // Idle animation redraws remain capped at 30 Hz.
    if (!this.renderRequested && now - this.lastSelectionFrame < 1000 / 30) return;
    this.selectionHalo.setFade(selectionHaloFade(now - this.selectionStarted));
    this.lastSelectionFrame = now;
    this.renderRequested = true;
  }
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
    if (this.disposed || this.paused) { this.raf = 0; return; }
    if (!this.primaryPrepared && this.entries.size) { this.raf = 0; return; }
    if (this.started) this.controls.update();
    const frameTime = performance.now();
    const centreWhileRotating = this.started && this.mobileView.matches && !this.dsaView && !this.injectionPick;
    const pivot = centreWhileRotating && this.rotationCentring.active ? this.selectedRotationPivot() : null;
    if (this.rotationCentring.step(this.camera, this.controls.target, pivot, centreWhileRotating, frameTime)) this.renderRequested = true;
    const interval = frameTime - this.previousFrameTime;
    // Ignore tab suspension; ordinary slow frames reduce background throughput.
    if (this.previousFrameTime && interval < 250 && !document.hidden) this.frameInterval = this.frameInterval * .8 + interval * .2;
    this.previousFrameTime = frameTime;
    const interactionRenderRequested = this.renderRequested;
    if (this.started && !this.dsaView && !this.injectionPick) this.updateSelectionGlow(frameTime);
    const rendered = this.renderRequested;
    if (rendered) {
      this.renderRequested = false;
      if (this.dsaView && !this.injectionPick && this.dsaRenderer) this.dsaRenderer.render(this.camera,this.dsaTime);
      else this.selectionHalo.render(this.scene, this.camera);
      this.lastRenderDuration = performance.now() - frameTime;
    }
    if (this.started) this.updateFps(frameTime, rendered && interactionRenderRequested);
    this.raf = 0;
    if (this.dsaView && this.movingUntil && frameTime >= this.movingUntil) { this.movingUntil = 0; this.renderRequested = true; }
    if (this.started || this.renderRequested) this.requestFrame();
  };
  start() { if (this.disposed) return; this.started = true; this.render(); }
  dispose() { this.disposed = true; this.loading?.dispose(); for (const finish of this.workWaiters) finish(); this.dsaRenderer?.dispose(); cancelAnimationFrame(this.raf); this.resize?.disconnect(); this.reducedMotion.removeEventListener('change',this.onMotionPreference); this.disposeSelectionGesture(); this.rotationCentring.dispose(); this.controls.dispose(); this.clearLandmarkMarker(); this.selectionHalo.dispose(); for(const e of this.entries.values()){e.mesh.geometry.dispose();(e.opaqueMaterial ?? e.mesh.material as THREE.Material).dispose();e.ghostMaterial?.dispose()} for(const batch of this.vascularBatches){batch.dispose();(batch.material as THREE.Material).dispose()} this.renderer.dispose(); this.renderer.domElement.remove(); }
}
