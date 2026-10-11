/** Separate intentional picking from camera controls sharing the same canvas. */
type PointerSample = Pick<PointerEvent, 'pointerId' | 'clientX' | 'clientY' |
  'button' | 'buttons' | 'isPrimary' | 'pointerType' | 'ctrlKey' | 'metaKey' | 'shiftKey' | 'altKey'>;

export class SelectionGesture {
  private active = new Set<number>();
  private candidate: { id: number; x: number; y: number; dragged: boolean } | null = null;

  constructor(private readonly tolerance = 5) {}

  pointerDown(event: PointerSample) {
    const alone = this.active.size === 0;
    this.active.add(event.pointerId);
    this.candidate = alone && event.isPrimary && event.button === 0 && event.buttons === 1 &&
      !event.ctrlKey && !event.metaKey && !event.shiftKey && !event.altKey
      ? { id: event.pointerId, x: event.clientX, y: event.clientY, dragged: false } : null;
  }

  pointerMove(event: PointerSample) {
    const start = this.candidate;
    if (!start || start.id !== event.pointerId) return;
    // Latch the maximum excursion. A drag returning to its starting point
    // must still remain a drag, rather than becoming an accidental click.
    if (Math.hypot(event.clientX - start.x, event.clientY - start.y) > this.tolerance ||
        event.ctrlKey || event.metaKey || event.shiftKey || event.altKey ||
        (event.pointerType !== 'touch' && event.buttons !== 1)) start.dragged = true;
  }

  pointerUp(event: PointerSample) {
    const start = this.candidate;
    this.active.delete(event.pointerId);
    if (!start || start.id !== event.pointerId) return false;
    this.candidate = null;
    return this.active.size === 0 && !start.dragged && event.button === 0 &&
      !event.ctrlKey && !event.metaKey && !event.shiftKey && !event.altKey &&
      Math.hypot(event.clientX - start.x, event.clientY - start.y) <= this.tolerance;
  }

  pointerCancel(event: Pick<PointerEvent, 'pointerId'>) {
    this.active.delete(event.pointerId);
    this.invalidate();
  }

  invalidate() { this.candidate = null; }
  reset() { this.active.clear(); this.invalidate(); }
}

export function bindSelectionGesture(canvas: HTMLCanvasElement, pick: (event: PointerEvent) => void) {
  const gesture = new SelectionGesture();
  const down = (event: PointerEvent) => gesture.pointerDown(event);
  const move = (event: PointerEvent) => gesture.pointerMove(event);
  const cancel = (event: PointerEvent) => gesture.pointerCancel(event);
  const wheel = () => gesture.invalidate();
  const blur = () => gesture.reset();
  const up = (event: PointerEvent) => {
    if (!gesture.pointerUp(event)) return;
    const rect = canvas.getBoundingClientRect();
    if (event.clientX >= rect.left && event.clientX < rect.right &&
        event.clientY >= rect.top && event.clientY < rect.bottom) pick(event);
  };
  // Capture before OrbitControls can release capture or handle pointerup.
  canvas.addEventListener('pointerdown', down, { capture: true });
  canvas.addEventListener('pointermove', move, { capture: true });
  canvas.addEventListener('pointerup', up, { capture: true });
  canvas.addEventListener('pointercancel', cancel, { capture: true });
  canvas.addEventListener('lostpointercapture', cancel, { capture: true });
  canvas.addEventListener('wheel', wheel, { capture: true, passive: true });
  const view = canvas.ownerDocument.defaultView;
  view?.addEventListener('blur', blur);
  return () => {
    canvas.removeEventListener('pointerdown', down, { capture: true });
    canvas.removeEventListener('pointermove', move, { capture: true });
    canvas.removeEventListener('pointerup', up, { capture: true });
    canvas.removeEventListener('pointercancel', cancel, { capture: true });
    canvas.removeEventListener('lostpointercapture', cancel, { capture: true });
    canvas.removeEventListener('wheel', wheel, { capture: true });
    view?.removeEventListener('blur', blur);
    gesture.reset();
  };
}
