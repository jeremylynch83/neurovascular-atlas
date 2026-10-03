import { StrictMode } from 'react';
import { createRoot } from 'react-dom/client';
import { App } from './App';
import { Loading } from './Loading';
import { loadCatalogue } from './catalogue';
import '@fontsource/inter-tight/400.css';
import '@fontsource/inter-tight/500.css';
import '@fontsource/inter-tight/600.css';
import '@fontsource/jetbrains-mono/400.css';
import '@fontsource-variable/source-serif-4/opsz.css';
import './styles.css';

async function boot() {
  const root=createRoot(document.getElementById('root')!);
  root.render(<Loading />);
  try { const manifest=await loadCatalogue(); root.render(<StrictMode><App manifest={manifest}/></StrictMode>); }
  catch(e){ console.error(e); root.render(<div className="fatal"><h1>Neurovascular Atlas</h1><p>Could not start the anatomy viewer.</p></div>); }
}
void boot();
