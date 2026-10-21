import type { AnatomyManifest, Structure } from './types';

export type GeometryStatus = 'pending' | 'loading' | 'ready' | 'error';
export type LoadState = { status: GeometryStatus; error?: string };
export type PreparedMesh = {
  id: string; positions: Float32Array; normals?: Float32Array; indices?: Uint32Array;
  bounds: [number[], number[]]; sphere: { centre: number[]; radius: number };
};
export interface GeometrySource {
  load(file: string): Promise<void>;
  prepare(structures: Structure[]): Promise<PreparedMesh[]>;
  release(): Promise<void>;
  dispose(): void;
}
export type LoadAsset = { file: string; structures: Structure[]; critical: boolean; order: number };

/** Fixed download order; anatomical source bindings remain unchanged. */
export function loadingAssets(manifest: AnatomyManifest): LoadAsset[] {
  const byId = new Map(manifest.structures.map(s => [s.id, s]));
  const assigned = new Set<string>();
  const assets: LoadAsset[] = [];
  for (const pack of manifest.loadingPacks ?? []) {
    const structures = pack.ids.map(id => {
      const row = byId.get(id);
      if (!row?.asset || row.system !== 'artery' || assigned.has(id)) throw new Error('Invalid loading pack binding: ' + id);
      assigned.add(id); return row;
    });
    assets.push({ file: pack.file, structures, critical: false, order: pack.stage + 1 });
  }
  const files = new Map<string, Structure[]>();
  for (const s of manifest.structures) if (s.asset && !assigned.has(s.id)) {
    if (manifest.loadingPacks && s.system === 'artery') throw new Error('Artery missing from loading packs: ' + s.id);
    const rows = files.get(s.asset.file) ?? []; rows.push(s); files.set(s.asset.file, rows);
  }
  for (const [file, structures] of files) {
    const stage = Math.min(...structures.map(s => s.system === 'bone' ? 0 : s.system === 'vein' ? 5 : s.system === 'brain' ? 6 : 2));
    assets.push({ file, structures, critical: manifest.loadingPacks ? structures.some(s => s.system === 'bone') : structures.some(s => s.system === 'bone' || s.system === 'artery'), order: stage });
  }
  if (!assets.some(a => a.critical)) throw new Error('No initial anatomy in loading plan');
  return assets.sort((a,b) => Number(b.critical) - Number(a.critical) || a.order - b.order);
}
type Waiter = { ids: string[]; resolve: () => void; reject: (error: Error) => void };

/** Serial downloads in fixed anatomical order and bounded geometry installation. */
export class StagedLoader {
  readonly states = new Map<string, LoadState>();
  private assets: LoadAsset[];
  private waiters = new Set<Waiter>();
  private running: Promise<void> | null = null;
  private background = false;
  private closed = false;

  constructor(manifest: AnatomyManifest, private source: GeometrySource,
    private install: (meshes: PreparedMesh[], background: boolean) => Promise<void>,
    private slot: (background: boolean) => Promise<void>, private changed: () => void) {
    this.assets = loadingAssets(manifest);
    for (const asset of this.assets) for (const s of asset.structures) this.states.set(s.id, { status: 'pending' });
  }

  private notify() {
    for (const w of this.waiters) {
      const failed = w.ids.find(id => this.states.get(id)?.status === 'error');
      if (failed) { this.waiters.delete(w); w.reject(new Error(this.states.get(failed)!.error ?? 'Could not load structure')); }
      else if (w.ids.every(id => this.states.get(id)?.status === 'ready')) { this.waiters.delete(w); w.resolve(); }
    }
    this.changed();
  }
  async loadCritical() {
    await this.pump();
    if (this.closed) return;
    const failed = this.assets.filter(a => a.critical).flatMap(a => a.structures).find(s => this.states.get(s.id)?.status !== 'ready');
    if (failed) throw new Error(this.states.get(failed.id)?.error ?? 'Initial anatomy did not load');
  }
  startBackground() { this.background = true; void this.pump(); }
  ensure(ids: readonly string[]): Promise<void> {
    if (this.closed) return Promise.reject(new Error('Atlas closed'));
    const required = [...new Set(ids)].filter(id => this.states.has(id));
    for (const id of required) {
      if (this.states.get(id)?.status === 'error') this.states.set(id, { status: 'pending' });
    }
    const result = new Promise<void>((resolve, reject) => this.waiters.add({ ids: required, resolve, reject }));
    this.notify(); void this.pump(); return result;
  }
  private pending(asset: LoadAsset) { return asset.structures.filter(s => this.states.get(s.id)?.status === 'pending'); }
  private pump(): Promise<void> {
    if (this.running) return this.running;
    if (this.closed) return Promise.resolve();
    this.running = this.run().finally(() => {
      this.running = null;
      if (!this.closed && this.assets.some(a => (a.critical || this.background) && this.pending(a).length)) void this.pump();
    });
    return this.running;
  }
  private async run() {
    while (!this.closed) {
      const assets = this.assets.filter(a => (a.critical || this.background) && this.pending(a).length);
      const asset = assets[0]; if (!asset) return;
      try {
        for (const s of this.pending(asset)) this.states.set(s.id, { status: 'loading' });
        this.notify(); await this.source.load(asset.file);
        while (!this.closed) {
          const pending = asset.structures.filter(s => this.states.get(s.id)?.status === 'loading');
          if (!pending.length) break;
          const meshes = await this.source.prepare(pending.slice(0, 16));
          if (this.closed) break;
          if (!meshes.length) throw new Error('No geometry returned for requested structures');
          await this.slot(this.background);
          if (this.closed) break;
          await this.install(meshes, this.background);
          if (this.closed) break;
          for (const mesh of meshes) { this.states.set(mesh.id, { status: 'ready' }); }
          this.notify();
        }
      } catch (error) {
        if (this.closed) return;
        const message = error instanceof Error ? error.message : String(error);
        for (const s of asset.structures) if (this.states.get(s.id)?.status !== 'ready') {
          this.states.set(s.id, { status: 'error', error: message });
        }
        this.notify();
      } finally { if (!this.closed) await this.source.release().catch(() => {}); }
    }
  }
  dispose() {
    this.closed = true; this.source.dispose();
    for (const w of this.waiters) w.reject(new Error('Atlas closed'));
    this.waiters.clear();
  }
}

/** Include parcel geometry needed by landmarks as well as group descendants. */
export function structureDependencies(id: string, byId: ReadonlyMap<string, Structure>, subtrees: ReadonlyMap<string, string[]>): string[] {
  const ids = new Set<string>();
  for (const key of subtrees.get(id) ?? [id]) {
    const s = byId.get(key); if (!s) continue;
    if (s.asset) ids.add(key);
    if (s.surfaceAnchor) ids.add(s.surfaceAnchor.structureId);
    for (const target of s.vesselGuide?.surfaceStructureIds ?? []) if (byId.get(target)?.asset) ids.add(target);
  }
  return [...ids];
}
