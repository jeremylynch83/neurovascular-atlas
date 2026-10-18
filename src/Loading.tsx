import { useEffect, useRef, useState } from 'react';

export function Loading({ progress = 0 }: { progress?: number }) {
  const actual = useRef(0);
  const current = useRef(0);
  const [shown, setShown] = useState(0);
  useEffect(() => {
    actual.current = Math.max(actual.current, Math.min(99, Math.max(0, progress)));
    if (matchMedia('(prefers-reduced-motion: reduce)').matches) {
      current.current = actual.current; setShown(actual.current);
    }
  }, [progress]);
  useEffect(() => {
    if (matchMedia('(prefers-reduced-motion: reduce)').matches) return;
    let frame = 0, previous = performance.now();
    const tick = (now: number) => {
      const dt = Math.min(.1, (now - previous) / 1000); previous = now;
      // Follow measured progress smoothly, with a small estimated advance
      // during download/decode gaps. Never report completion before readiness.
      const speed = Math.max(0, actual.current - current.current) * 3 + (99 - current.current) * .004;
      current.current = Math.min(99, current.current + speed * dt);
      setShown(current.current);
      frame = requestAnimationFrame(tick);
    };
    frame = requestAnimationFrame(tick);
    return () => cancelAnimationFrame(frame);
  }, []);
  const percent = Math.min(99, Math.round(shown));
  return <div className="loading panel" role="status">
    <span>Loading anatomy, please wait</span>
    <div className="loading-progress" role="progressbar" aria-label="Loading anatomy" aria-valuemin={0} aria-valuemax={100} aria-valuenow={percent}>
      <div className="loading-fill" style={{ width: `${shown}%` }} />
      <span className="loading-percent">{percent}%</span>
    </div>
  </div>;
}
