import { useEffect, useRef } from 'react';
import { ANATOMICAL_PRESETS, type PresetId, type PresetSide } from './presets';

export function BookmarkIcon() {
  return <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.7" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true"><path d="M6 3h12v18l-6-4-6 4V3Z" /></svg>;
}

export function PresetModal({ side, onSideChange, onApply, onClose }: {
  side: PresetSide; onSideChange: (side: PresetSide) => void;
  onApply: (preset: PresetId) => void; onClose: () => void;
}) {
  const dialog = useRef<HTMLDivElement>(null);
  const close = useRef<HTMLButtonElement>(null);
  useEffect(() => {
    const previous = document.activeElement as HTMLElement | null;
    close.current?.focus();
    const handleKey = (event: KeyboardEvent) => {
      if (event.key === 'Escape') { event.preventDefault(); onClose(); }
      if (event.key !== 'Tab') return;
      const buttons = dialog.current?.querySelectorAll<HTMLButtonElement>('button:not(:disabled)');
      if (!buttons?.length) return;
      const first = buttons[0], last = buttons[buttons.length - 1];
      if (event.shiftKey && document.activeElement === first) { event.preventDefault(); last.focus(); }
      else if (!event.shiftKey && document.activeElement === last) { event.preventDefault(); first.focus(); }
    };
    document.addEventListener('keydown', handleKey);
    return () => { document.removeEventListener('keydown', handleKey); previous?.focus(); };
  }, [onClose]);
  return <div className="modal-scrim presets-scrim" onClick={onClose}>
    <div className="presets-modal panel" ref={dialog} role="dialog" aria-modal="true" aria-labelledby="presets-title" onClick={event => event.stopPropagation()}>
      <header className="presets-header">
        <h2 id="presets-title"><BookmarkIcon />Anatomical presets</h2>
        <button ref={close} className="presets-close" aria-label="Close anatomical presets" onClick={onClose}>×</button>
      </header>
      <div className="preset-side" role="group" aria-label="Side">
        {(['left', 'right', 'both'] as const).map(value => <button key={value} aria-pressed={side === value} onClick={() => onSideChange(value)}>{value[0].toUpperCase() + value.slice(1)}</button>)}
      </div>
      <div className="presets-grid">
        {ANATOMICAL_PRESETS.map(preset => <button className="preset-card" key={preset.id} onClick={() => onApply(preset.id)} aria-label={`${preset.label}, ${side}`}>
          <img src={`${import.meta.env.BASE_URL}presets/${preset.id}-${side}.webp`} alt="" width="480" height="320" />
          <span>{preset.label}</span>
        </button>)}
      </div>
    </div>
  </div>;
}
