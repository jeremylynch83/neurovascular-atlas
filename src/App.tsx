import { useEffect, useMemo, useRef, useState, type ReactNode } from 'react';
import type { AnatomyManifest, LayerState, Structure, SystemId } from './types';
import { searchStructures } from './catalogue';
import { AnatomyEngine } from './engine';

const SYSTEMS: { id: SystemId; label: string; hint: string }[] = [
  { id: 'bone', label: 'Bone', hint: 'Skull and skull-base landmarks' },
  { id: 'artery', label: 'Arteries', hint: 'Cervical, ECA and intracranial' },
  { id: 'vein', label: 'Veins', hint: 'Sinuses, superficial and deep veins' },
  { id: 'brain', label: 'Brain', hint: 'Parenchymal context' },
];
const NEXT: Record<LayerState, LayerState> = { on: 'ghost', ghost: 'off', off: 'on' };

export function App({ manifest }: { manifest: AnatomyManifest }) {
  const stage = useRef<HTMLDivElement>(null);
  const engine = useRef<AnatomyEngine | null>(null);
  const [selectedId, setSelectedId] = useState<string | null>(null);
  const [query, setQuery] = useState('');
  const [layers, setLayers] = useState<Record<SystemId, LayerState>>({ bone: 'ghost', artery: 'on', vein: 'off', brain: 'off' });
  const [tab, setTab] = useState<'layers'|'tree'>('layers');
  const [dark, setDark] = useState(false);
  const [ready, setReady] = useState(false);
  const [clip, setClip] = useState({ enabled: false, axis: 'sagittal' as 'sagittal'|'coronal'|'axial', offset: 0 });
  const [about, setAbout] = useState(false);
  const byId = useMemo(() => new Map(manifest.structures.map((s) => [s.id, s])), [manifest]);
  const selected = selectedId ? byId.get(selectedId) ?? null : null;
  const results = useMemo(() => searchStructures(manifest.structures, query), [manifest.structures, query]);

  useEffect(() => {
    if (!stage.current) return;
    const e = new AnatomyEngine(stage.current, manifest, setSelectedId); engine.current = e; e.setTheme(dark);
    e.load().then(() => { setReady(true); e.start(); }).catch((err) => console.error(err));
    return () => { e.dispose(); engine.current = null; };
  }, [manifest]);
  useEffect(() => { document.documentElement.dataset.theme = dark ? 'dark' : 'light'; engine.current?.setTheme(dark); }, [dark]);
  useEffect(() => { engine.current?.setSelected(selectedId); }, [selectedId]);
  useEffect(() => { for (const [k,v] of Object.entries(layers) as [SystemId,LayerState][]) engine.current?.setLayer(k,v); }, [layers]);
  useEffect(() => { engine.current?.setClip(clip.enabled, clip.axis, clip.offset); }, [clip]);

  const select = (s: Structure) => { setSelectedId(s.id); setQuery(''); if (s.asset) engine.current?.focus(s.id); };
  const geometryCount = (system: SystemId) => manifest.structures.filter((s) => s.system === system && s.asset).length;
  const plannedCount = (system: SystemId) => manifest.structures.filter((s) => s.system === system && !s.asset && s.kind !== 'group').length;

  return <div className="atlas-app">
    <div className="atlas-stage" ref={stage} />
    <header className="identity">
      <div className="eyebrow">Interventional neuroradiology</div>
      <h1>INR Anatomy Atlas</h1>
      <div className="release">v0.3 scan-derived pipeline</div>
    </header>
    <div className="top-actions">
      <div className="search-wrap">
        <span className="search-icon">⌕</span>
        <input value={query} onChange={(e)=>setQuery(e.target.value)} placeholder="Search vessel, vein, bone or landmark…" aria-label="Search anatomy" />
        {query && <button className="clear" onClick={()=>setQuery('')} aria-label="Clear search">×</button>}
        {query && <div className="search-results panel">
          {results.length ? results.map((s)=><button key={s.id} onClick={()=>select(s)}>
            <span className={`sys-dot ${s.system}`} /><span><strong>{s.name}</strong><small>{s.id}</small></span><em>{s.asset?'geometry':'planned'}</em>
          </button>) : <div className="empty">No matching structure</div>}
        </div>}
      </div>
      <button className="icon-btn" onClick={()=>setDark(!dark)} title="Toggle theme">{dark?'☀':'◐'}</button>
      <button className="icon-btn" onClick={()=>setAbout(true)} title="About v0.3">i</button>
    </div>

    <aside className="left-panel panel">
      <div className="tabs"><button className={tab==='layers'?'active':''} onClick={()=>setTab('layers')}>Layers</button><button className={tab==='tree'?'active':''} onClick={()=>setTab('tree')}>Anatomy</button></div>
      {tab==='layers' ? <>
        <p className="panel-intro">Three-state controls cycle through <b>shown</b>, <b>ghosted</b> and <b>hidden</b>.</p>
        <div className="layer-list">{SYSTEMS.map((sys)=><div className="layer-row" key={sys.id}>
          <button className={`state ${layers[sys.id]}`} onClick={()=>setLayers((x)=>({...x,[sys.id]:NEXT[x[sys.id]]}))} aria-label={`${sys.label}: ${layers[sys.id]}`}><span /></button>
          <button className="layer-name" onClick={()=>setTab('tree')}><span>{sys.label}</span><small>{sys.hint}</small></button>
          <div className="counts"><b>{geometryCount(sys.id)}</b><small>mesh</small><b>{plannedCount(sys.id)}</b><small>planned</small></div>
        </div>)}</div>
        <div className="preset-row"><button onClick={()=>setLayers({bone:'ghost',artery:'on',vein:'on',brain:'off'})}>Overview</button><button onClick={()=>setLayers({bone:'ghost',artery:'on',vein:'off',brain:'off'})}>Arterial</button><button onClick={()=>setLayers({bone:'ghost',artery:'off',vein:'on',brain:'off'})}>Venous</button></div>
      </> : <StructureTree manifest={manifest} byId={byId} selectedId={selectedId} onSelect={select} />}
    </aside>

    {selected && <Detail structure={selected} manifest={manifest} engine={engine.current} onClose={()=>setSelectedId(null)} />}

    <div className="foundation-note panel"><b>v0.3</b><span>TopBrain scan-derived reference pipeline</span><span className="sep">•</span><span>{manifest.warning}</span></div>

    <div className="camera-bar panel">
      <div className="views"><button onClick={()=>engine.current?.setView('front')}>AP</button><button onClick={()=>engine.current?.setView('left')}>L</button><button onClick={()=>engine.current?.setView('right')}>R</button><button onClick={()=>engine.current?.setView('superior')}>Sup</button><button onClick={()=>engine.current?.setView('inferior')}>Inf</button><button onClick={()=>engine.current?.setView('three-quarter')}>3/4</button><button onClick={()=>engine.current?.fitAll()}>Fit</button></div>
      <div className="clip-tools"><label><input type="checkbox" checked={clip.enabled} onChange={(e)=>setClip({...clip,enabled:e.target.checked})}/> Section</label><select value={clip.axis} onChange={(e)=>setClip({...clip,axis:e.target.value as typeof clip.axis})}><option value="sagittal">Sagittal</option><option value="coronal">Coronal</option><option value="axial">Axial</option></select><input type="range" min="-1" max="1" step="0.01" value={clip.offset} onChange={(e)=>setClip({...clip,offset:Number(e.target.value)})}/></div>
    </div>

    {!ready && <div className="loading panel">Loading v0.3 scan-derived pipeline…</div>}
    {about && <About manifest={manifest} onClose={()=>setAbout(false)} />}
  </div>;
}

function StructureTree({manifest,byId,selectedId,onSelect}:{manifest:AnatomyManifest;byId:Map<string,Structure>;selectedId:string|null;onSelect:(s:Structure)=>void}) {
  const [open,setOpen]=useState<Set<string>>(new Set(['bone','artery','vein','brain','bone.skull','artery.eca','artery.intracranial','vein.sinus']));
  const toggle=(id:string)=>setOpen((old)=>{const n=new Set(old);n.has(id)?n.delete(id):n.add(id);return n});
  const node=(id:string,depth=0):ReactNode=>{const s=byId.get(id);if(!s)return null;const has=s.children.length>0;return <div key={id}>
    <div className={`tree-row ${selectedId===id?'selected':''} ${s.asset?'has-geometry':'planned'}`} style={{paddingLeft:8+depth*14}}>
      <button className="twisty" onClick={()=>has&&toggle(id)}>{has?(open.has(id)?'⌄':'›'):''}</button>
      <button className="tree-name" onClick={()=>onSelect(s)}><span>{s.name}</span>{s.kind!=='group'&&<small>{s.asset?'mesh':'planned'}</small>}</button>
    </div>{has&&open.has(id)&&s.children.map((c)=>node(c,depth+1))}
  </div>};
  return <div className="tree">{manifest.roots.map((r)=>node(r))}</div>;
}

function Detail({structure,manifest,engine,onClose}:{structure:Structure;manifest:AnatomyManifest;engine:AnatomyEngine|null;onClose:()=>void}) {
  const sources=structure.provenance.sourceRefs.map((id)=>manifest.sources.find((s)=>s.id===id)).filter(Boolean);
  const rels=manifest.relationships.filter((r)=>r.from===structure.id||r.to===structure.id);
  const [hidden,setHidden]=useState(false);
  useEffect(()=>setHidden(engine?.isHidden(structure.id)??false),[structure.id,engine]);
  return <aside className="detail panel">
    <button className="detail-close" onClick={onClose}>×</button><div className="detail-system"><span className={`sys-dot ${structure.system}`}/>{structure.system}</div>
    <h2>{structure.name}</h2><code>{structure.id}</code>
    <div className={`geometry-status ${structure.asset?'available':'planned'}`}>{structure.asset?(structure.provenance.sourceType==='atlas-derived'?'Atlas-derived seed geometry':'Temporary context geometry'):'Geometry planned'}</div>
    <dl><dt>Side</dt><dd>{structure.side}</dd><dt>Provenance</dt><dd>{structure.provenance.sourceType}</dd><dt>Confidence</dt><dd>{structure.provenance.confidence}</dd><dt>Review</dt><dd>{structure.provenance.reviewStatus}</dd></dl>
    {structure.asset?<div className="detail-actions"><button onClick={()=>engine?.focus(structure.id)}>Focus</button><button onClick={()=>{engine?.setHidden(structure.id,!hidden);setHidden(!hidden)}}>{hidden?'Show':'Hide'}</button></div>:<p className="planned-copy">The logical structure exists now so models, search, relationships and saved views can use a stable ID before geometry is added.</p>}
    {rels.length>0&&<section><h3>Relationships</h3>{rels.map((r,i)=><div className="relationship" key={i}><b>{r.type.replaceAll('_',' ')}</b><span>{r.from===structure.id?r.to:r.from}</span>{r.note&&<small>{r.note}</small>}</div>)}</section>}
    <section><h3>Reference / source</h3>{sources.map((s)=><div className="source" key={s!.id}><b>{s!.title}</b><small>{s!.role}</small></div>)}</section>
    {structure.notes&&<section><h3>Notes</h3><p>{structure.notes}</p></section>}
  </aside>;
}

function About({manifest,onClose}:{manifest:AnatomyManifest;onClose:()=>void}) {
  return <div className="modal-scrim" onMouseDown={onClose}><div className="about panel" onMouseDown={(e)=>e.stopPropagation()}><button className="detail-close" onClick={onClose}>×</button><div className="eyebrow">Scan-derived reference release</div><h2>INR Anatomy Atlas v0.3</h2><p>This release adds the reproducible TopBrain source-data pipeline for a real CTA-derived reference subject, while retaining the atlas seed geometry until a reference case is built locally.</p><p><b>{manifest.structures.length}</b> logical structures and <b>{manifest.relationships.length}</b> explicit cross-structure relationships are currently defined.</p><h3>Geometry status</h3><p>When a TopBrain case has been built, its labelled CTA vessels and CT-derived skull are loaded as scan-derived geometry in source NIfTI physical coordinates. Legacy Z-Anatomy ECA seed geometry is not registered to that reference and remains clearly provenance-labelled.</p><h3>Next source-data gate</h3><p>Run ./anatomy.sh download, ./anatomy.sh inspect, then ./anatomy.sh build CASE to generate the local scan-derived reference. Borden and Kiyosue remain validation references; their copyrighted figures are not embedded or converted into app geometry.</p><button className="primary" onClick={onClose}>Close</button></div></div>;
}
