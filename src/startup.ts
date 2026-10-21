// This panel is outside the React root so it survives bundle, catalogue,
// WebGL and rendering failures. No user-agent or crawler detection is used.
let state: 'loading' | 'ready' | 'error' = 'loading';
function elements() {
  return {
    panel: document.getElementById('atlas-fallback'),
    root: document.getElementById('root'),
    status: document.getElementById('atlas-startup-status'),
    progress: document.getElementById('atlas-startup-progress') as HTMLProgressElement | null,
    retry: document.getElementById('atlas-startup-retry'),
  };
}
export function reportStartupProgress(percent: number) {
  if (state !== 'loading') return;
  const {progress} = elements();
  if (progress) { progress.value = Math.max(0, Math.min(99, percent)); progress.removeAttribute('hidden'); }
}
export function reportStartupReady() {
  if (state !== 'loading') return;
  state = 'ready';
  const {panel, root} = elements();
  const transferFocus = !!panel?.contains(document.activeElement);
  if (root) { root.inert = false; root.removeAttribute('aria-hidden'); }
  if (panel) panel.hidden = true;
  document.documentElement.dataset.atlasState = state;
  if (transferFocus && root) { root.tabIndex = -1; root.focus({preventScroll:true}); }
}
export function reportStartupFailure(error: unknown) {
  state = 'error';
  console.error('Atlas viewer could not render', error);
  const {panel, root, status, progress, retry} = elements();
  if (panel) panel.hidden = false;
  if (root) { root.inert = true; root.setAttribute('aria-hidden', 'true'); }
  if (status) status.textContent = 'The 3D viewer could not start. The atlas information remains available below.';
  if (progress) progress.hidden = true;
  if (retry) retry.hidden = false;
  document.documentElement.dataset.atlasState = state;
}
