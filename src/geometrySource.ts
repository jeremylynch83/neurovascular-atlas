import type { GeometrySource, PreparedMesh } from './stagedLoading';
import type { AnatomyManifest, Structure } from './types';

export class WorkerGeometrySource implements GeometrySource {
  private worker!: Worker;
  private failure: Error | null = null;
  private closed = false;
  private sequence = 0;
  private pending = new Map<number, { resolve: (data: unknown) => void; reject: (error: Error) => void }>();
  constructor(private manifest: AnatomyManifest, private budget: () => number = () => 50_000) {}
  private createWorker() {
    this.worker = new Worker(new URL('./geometryWorker.ts', import.meta.url), { type: 'module' });
    this.worker.onmessage = ({ data }) => {
      const request = this.pending.get(data.request); if (!request) return;
      this.pending.delete(data.request);
      if (data.error) request.reject(new Error(data.error)); else request.resolve(data.result);
    };
    this.worker.onerror = event => {
      this.failure = new Error(event.message || 'Geometry worker failed');
      for (const request of this.pending.values()) request.reject(this.failure);
      this.pending.clear();
    };
  }
  private call<T>(action: string, payload: object = {}): Promise<T> {
    if (this.closed || this.failure || !this.worker) return Promise.reject(this.failure ?? new Error('Geometry worker unavailable'));
    const request = ++this.sequence;
    return new Promise((resolve, reject) => {
      this.pending.set(request, { resolve: data => resolve(data as T), reject });
      this.worker.postMessage({ request, action, ...payload });
    });
  }
  load(file: string) {
    if (this.failure && !this.closed) { this.worker.terminate(); this.failure = null; this.createWorker(); }
    if (!this.worker && !this.closed) this.createWorker();
    const revision = this.manifest.assetRevisions?.[file] ?? this.manifest.release;
    const url = new URL(`${import.meta.env.BASE_URL}anatomy/${file}?v=${encodeURIComponent(revision)}`, window.location.href).href;
    return this.call<void>('load', { url });
  }
  prepare(structures: Structure[]) { return this.call<PreparedMesh[]>('prepare', { vertexBudget: this.budget(), structures: structures.map(s => ({ id: s.id, node: s.asset!.node })) }); }
  release() { return this.call<void>('release'); }
  dispose() {
    this.closed = true;
    this.worker?.terminate();
    for (const request of this.pending.values()) request.reject(new Error('Atlas closed'));
    this.pending.clear();
  }
}
