import { dsaPhase, DSA_END } from './dsa';

export function DsaIcon() {
  return <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.7" aria-hidden="true"><rect x="3" y="3" width="18" height="18" rx="2"/><path d="M12 19v-7m0 2-5-4m5 2 5-4m-5 4V5m-5 5V7m10 1V5"/></svg>;
}

export function DsaControls({ time, playing, territory, onTime, onPlaying,onPlacement,onReset,custom,busy }: {
  time: number; playing: boolean; territory: string; onTime: (time: number) => void; onPlaying: (playing: boolean) => void;
  onPlacement:()=>void;onReset:()=>void;custom:boolean;busy:boolean;
}) {
  const step = (delta: number) => { onPlaying(false); onTime(Math.max(0,Math.min(DSA_END,time+delta))); };
  return <div className="dsa-controls panel" data-focus-control role="group" aria-label="DSA contrast phase">
    <div className="dsa-caption"><strong>{territory}</strong><span>{time.toFixed(1)} s · {dsaPhase(time)}</span></div>
    <input type="range" aria-label="Contrast time" aria-valuetext={`${time.toFixed(1)} seconds, ${dsaPhase(time)}`} min="0" max={DSA_END} step="0.5" value={time} onChange={e => { onPlaying(false); onTime(Number(e.target.value)); }}/>
    <div className="dsa-playback">
      <button aria-label="Previous frame" disabled={time===0} onClick={() => step(-.5)}>◀</button>
      <button aria-label={playing ? 'Pause DSA' : 'Play DSA'} onClick={() => { if (!playing && time===DSA_END) onTime(0); onPlaying(!playing); }}>{playing ? 'Pause' : 'Play'}</button>
      <button aria-label="Next frame" disabled={time===DSA_END} onClick={() => step(.5)}>▶</button>
      <button aria-label="Replay DSA" onClick={() => { onTime(0); onPlaying(true); }}>Replay</button>
      <span>2 frames/s</span>
    </div>
    <div className="injection-actions"><button disabled={busy} onClick={onPlacement}>Injection point</button><button disabled={!custom||busy} onClick={onReset}>Reset origin</button></div>
  </div>;
}

export function InjectionControls({name,onChange,onCancel,busy}:{name:string|null;onChange:()=>void;onCancel:()=>void;busy:boolean}) {
  return <div className="dsa-controls injection-controls panel" data-focus-control role="group" aria-label="Injection point placement">
    <strong>{name??'Select an artery'}</strong>
    <p>{busy?'Preparing injection…':name?'Click the injection point on this artery.':'Select an artery in the view or search.'}</p>
    <div className="injection-actions"><button disabled={busy||!name} onClick={onChange}>Change artery</button><button disabled={busy} onClick={onCancel}>Cancel</button></div>
  </div>;
}
