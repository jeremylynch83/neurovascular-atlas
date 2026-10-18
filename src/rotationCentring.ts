import { Vector3, type Camera } from 'three';

/** Blend the orbit target during an intentional one-finger/left-button drag. */
export class RotationCentring {
  private pointers = new Set<number>();
  private start: { id: number; x: number; y: number } | null = null;
  private rotating = false;
  private blocked = false;
  private progress = 0;
  private lastFrame: number | null = null;
  private delta = new Vector3();

  constructor(private canvas: HTMLCanvasElement) {
    canvas.addEventListener('pointerdown', this.down, true);
    canvas.addEventListener('pointermove', this.move, true);
    canvas.addEventListener('pointerup', this.up, true);
    canvas.addEventListener('pointercancel', this.up, true);
    canvas.addEventListener('lostpointercapture', this.up, true);
    canvas.addEventListener('wheel', this.interrupt, { capture: true, passive: true });
    canvas.ownerDocument.defaultView?.addEventListener('blur', this.blur);
  }

  reset() { this.progress = 0; this.lastFrame = null; }
  get active() { return this.rotating && !this.blocked; }

  private down = (event: PointerEvent) => {
    if (!this.pointers.size) {
      this.blocked = event.button !== 0 || event.ctrlKey || event.metaKey || event.shiftKey || event.altKey;
      this.start = { id: event.pointerId, x: event.clientX, y: event.clientY };
      this.rotating = false; this.lastFrame = null;
      if (this.progress === 1) this.reset();
    }
    this.pointers.add(event.pointerId);
    if (this.pointers.size > 1) this.interrupt();
  };
  private move = (event: PointerEvent) => {
    if (event.ctrlKey || event.metaKey || event.shiftKey || event.altKey) this.interrupt();
    if (this.blocked || this.pointers.size !== 1 || this.start?.id !== event.pointerId) return;
    if (Math.hypot(event.clientX - this.start.x, event.clientY - this.start.y) > 5) this.rotating = true;
  };
  private up = (event: PointerEvent) => {
    this.pointers.delete(event.pointerId);
    this.rotating = false; this.lastFrame = null;
    if (!this.pointers.size) { this.start = null; this.blocked = false; }
  };
  private interrupt = () => { this.blocked = true; this.rotating = false; this.reset(); };
  private blur = () => { this.pointers.clear(); this.start = null; this.interrupt(); };

  step(camera: Camera, target: Vector3, centre: Vector3 | null, enabled: boolean, now: number) {
    if (!enabled || !this.active || !centre || this.progress === 1) { this.lastFrame = null; return false; }
    if (this.lastFrame === null) { this.lastFrame = now; return false; }
    const dt = Math.max(0, Math.min(50, now - this.lastFrame)); this.lastFrame = now;
    const next = Math.min(1, this.progress + dt / 400);
    const ease = (t: number) => t * t * (3 - 2 * t);
    const previousEase = ease(this.progress);
    const fraction = next === 1 || previousEase > 1 - 1e-10
      ? 1 : (ease(next) - previousEase) / (1 - previousEase);
    this.progress = fraction === 1 ? 1 : next;
    this.delta.subVectors(centre, target).multiplyScalar(fraction);
    if (this.delta.lengthSq() < 1e-16) return false;
    // Parallel translation preserves camera direction and orbit distance.
    target.add(this.delta); camera.position.add(this.delta);
    return true;
  }

  dispose() {
    this.canvas.removeEventListener('pointerdown', this.down, true);
    this.canvas.removeEventListener('pointermove', this.move, true);
    this.canvas.removeEventListener('pointerup', this.up, true);
    this.canvas.removeEventListener('pointercancel', this.up, true);
    this.canvas.removeEventListener('lostpointercapture', this.up, true);
    this.canvas.removeEventListener('wheel', this.interrupt, true);
    this.canvas.ownerDocument.defaultView?.removeEventListener('blur', this.blur);
    this.blur();
  }
}
