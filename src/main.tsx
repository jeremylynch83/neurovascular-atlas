import { StrictMode } from 'react';
import { createRoot } from 'react-dom/client';
import { ViewerBoundary } from './ViewerBoundary';
import { reportStartupFailure } from './startup';
import './fonts.css';
import './styles.css';

async function boot() {
  performance.mark('atlas-boot-start');
  const root=createRoot(document.getElementById('root')!);
  root.render(<div className="atlas-app"><header className="identity"><h1>Neurovascular Atlas</h1></header></div>);
  try {
    const [{App}, {loadCatalogue}] = await Promise.all([import('./App'), import('./catalogue')]);
    const manifest = await loadCatalogue();
    root.render(<StrictMode><ViewerBoundary><App manifest={manifest}/></ViewerBoundary></StrictMode>);
  } catch(error) { reportStartupFailure(error); root.render(null); }
}
void boot();
