export function Loading({ progress = 0 }: { progress?: number }) {
  const percent = Math.max(0, Math.min(100, Math.round(progress)));
  return <div className="loading panel" role="status">
    <span>Loading anatomy, please wait</span>
    <div className="loading-progress" role="progressbar" aria-label="Loading anatomy" aria-valuemin={0} aria-valuemax={100} aria-valuenow={percent}>
      <div className="loading-fill" style={{ width: `${percent}%` }} />
      <span className="loading-percent">{percent}%</span>
    </div>
  </div>;
}
