import { dsaPhase, DSA_START, DSA_END } from './dsa';

export function DsaIcon() {
  return <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.7" aria-hidden="true"><rect x="3" y="3" width="18" height="18" rx="2"/><path d="M12 19v-7m0 2-5-4m5 2 5-4m-5 4V5m-5 5V7m10 1V5"/></svg>;
}

const PlaybackIcon=({path}:{path:string})=><svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d={path}/></svg>;

export function DsaControls({ time, playing, territory, onTime, onPlaying,onPlacement,busy }: {
  time: number; playing: boolean; territory: string; onTime: (time: number) => void; onPlaying: (playing: boolean) => void;
  onPlacement:()=>void;busy:boolean;
}) {
  const step = (delta: number) => { onPlaying(false); onTime(Math.max(DSA_START,Math.min(DSA_END,time+delta))); };
  return <div className="dsa-controls panel" data-focus-control role="group" aria-label="DSA contrast phase">
    <div className="dsa-caption"><strong>{territory}</strong><span>{time.toFixed(1)} s · {dsaPhase(time)}</span></div>
    <input type="range" aria-label="Contrast time" aria-valuetext={`${time.toFixed(1)} seconds, ${dsaPhase(time)}`} min={DSA_START} max={DSA_END} step="0.5" value={time} onChange={e => { onPlaying(false); onTime(Number(e.target.value)); }}/>
    <div className="dsa-playback">
      <button aria-label="Previous frame" title="Previous frame" disabled={time===DSA_START} onClick={() => step(-.5)}><PlaybackIcon path="M4 4h2v16H4zM20 4 8 12l12 8z"/></button>
      <button aria-label="Play DSA" title="Play" disabled={playing} onClick={() => { if (time===DSA_END) onTime(DSA_START); onPlaying(true); }}><PlaybackIcon path="M6 4v16l14-8z"/></button>
      <button aria-label="Pause DSA" title="Pause" disabled={!playing} onClick={() => onPlaying(false)}><PlaybackIcon path="M5 4h5v16H5zM14 4h5v16h-5z"/></button>
      <button aria-label="Next frame" title="Next frame" disabled={time===DSA_END} onClick={() => step(.5)}><PlaybackIcon path="M18 4h2v16h-2zM4 4v16l12-8z"/></button>
      <span>2 frames/s</span>
    </div>
    <div className="injection-actions"><button disabled={busy} onClick={onPlacement}>Choose injection point</button></div>
  </div>;
}

export function InjectionControls({name,onChange,onCancel,busy}:{name:string|null;onChange:()=>void;onCancel:()=>void;busy:boolean}) {
  return <div className="dsa-controls injection-controls panel" data-focus-control role="group" aria-label="Injection point placement">
    <strong>{name??'Select an artery'}</strong>
    <p>{busy?'Preparing injection…':name?'Click the injection point on this artery.':'Select an artery in the view or search.'}</p>
    <div className="injection-actions">{name&&<button disabled={busy} onClick={onChange}>Change artery</button>}<button onClick={onCancel}>Cancel</button></div>
  </div>;
}
