export class SelectionGesture {
    tolerance;
    active = new Set();
    candidate = null;
    constructor(tolerance = 5){
        this.tolerance = tolerance;
    }
    pointerDown(event) {
        const alone = this.active.size === 0;
        this.active.add(event.pointerId);
        this.candidate = alone && event.isPrimary && event.button === 0 && event.buttons === 1 && !event.ctrlKey && !event.metaKey && !event.shiftKey && !event.altKey ? {
            id: event.pointerId,
            x: event.clientX,
            y: event.clientY,
            dragged: false
        } : null;
    }
    pointerMove(event) {
        const start = this.candidate;
        if (!start || start.id !== event.pointerId) return;
        if (Math.hypot(event.clientX - start.x, event.clientY - start.y) > this.tolerance || event.ctrlKey || event.metaKey || event.shiftKey || event.altKey || event.pointerType !== 'touch' && event.buttons !== 1) start.dragged = true;
    }
    pointerUp(event) {
        const start = this.candidate;
        this.active.delete(event.pointerId);
        if (!start || start.id !== event.pointerId) return false;
        this.candidate = null;
        return this.active.size === 0 && !start.dragged && event.button === 0 && !event.ctrlKey && !event.metaKey && !event.shiftKey && !event.altKey && Math.hypot(event.clientX - start.x, event.clientY - start.y) <= this.tolerance;
    }
    pointerCancel(event) {
        this.active.delete(event.pointerId);
        this.invalidate();
    }
    invalidate() {
        this.candidate = null;
    }
    reset() {
        this.active.clear();
        this.invalidate();
    }
}
export function bindSelectionGesture(canvas, pick) {
    const gesture = new SelectionGesture();
    const down = (event)=>gesture.pointerDown(event);
    const move = (event)=>gesture.pointerMove(event);
    const cancel = (event)=>gesture.pointerCancel(event);
    const wheel = ()=>gesture.invalidate();
    const blur = ()=>gesture.reset();
    const up = (event)=>{
        if (!gesture.pointerUp(event)) return;
        const rect = canvas.getBoundingClientRect();
        if (event.clientX >= rect.left && event.clientX < rect.right && event.clientY >= rect.top && event.clientY < rect.bottom) pick(event);
    };
    canvas.addEventListener('pointerdown', down, {
        capture: true
    });
    canvas.addEventListener('pointermove', move, {
        capture: true
    });
    canvas.addEventListener('pointerup', up, {
        capture: true
    });
    canvas.addEventListener('pointercancel', cancel, {
        capture: true
    });
    canvas.addEventListener('lostpointercapture', cancel, {
        capture: true
    });
    canvas.addEventListener('wheel', wheel, {
        capture: true,
        passive: true
    });
    const view = canvas.ownerDocument.defaultView;
    view?.addEventListener('blur', blur);
    return ()=>{
        canvas.removeEventListener('pointerdown', down, {
            capture: true
        });
        canvas.removeEventListener('pointermove', move, {
            capture: true
        });
        canvas.removeEventListener('pointerup', up, {
            capture: true
        });
        canvas.removeEventListener('pointercancel', cancel, {
            capture: true
        });
        canvas.removeEventListener('lostpointercapture', cancel, {
            capture: true
        });
        canvas.removeEventListener('wheel', wheel, {
            capture: true
        });
        view?.removeEventListener('blur', blur);
        gesture.reset();
    };
}
