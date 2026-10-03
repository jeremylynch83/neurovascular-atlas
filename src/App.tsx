import { useEffect, useMemo, useRef, useState, type ReactNode } from 'react';
import type { AnatomyManifest, LayerState, Structure, SystemId } from './types';
import { geometrySubtrees, searchStructures } from './catalogue';
import { AnatomyEngine } from './engine';

const SYSTEMS: { id: SystemId; label: string; hint: string }[] = [
  { id: 'bone', label: 'Bone', hint: 'Skull, maxillae, mandible and teeth' },
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
  const [controlsOpen, setControlsOpen] = useState(true);
  const [inspectionOpen, setInspectionOpen] = useState(true);
  const [dark, setDark] = useState(true);
  const [ready, setReady] = useState(false);
  const [loadError, setLoadError] = useState<string | null>(null);
  const [clip, setClip] = useState({ enabled: false, axis: 'sagittal' as 'sagittal'|'coronal'|'axial', offset: 0 });
  const [about, setAbout] = useState(false);
  const [hiddenIds, setHiddenIds] = useState<Set<string>>(() => new Set());
  const byId = useMemo(() => new Map(manifest.structures.map((s) => [s.id, s])), [manifest]);
  const subtrees = useMemo(() => geometrySubtrees(byId), [byId]);
  const selected = selectedId ? byId.get(selectedId) ?? null : null;
  const results = useMemo(() => searchStructures(manifest.structures, query), [manifest.structures, query]);

  useEffect(() => {
    if (!stage.current) return;
    let cancelled = false;
    setReady(false); setLoadError(null);
    const e = new AnatomyEngine(stage.current, manifest, setSelectedId); engine.current = e; e.setTheme(dark);
    e.load().then(() => { if (cancelled) return; setReady(true); setLoadError(null); e.start(); }).catch((err) => { if (cancelled) return; console.error(err); setLoadError(err instanceof Error ? err.message : String(err)); });
    return () => { cancelled = true; e.dispose(); engine.current = null; };
  }, [manifest]);
  useEffect(() => { document.documentElement.dataset.theme = dark ? 'dark' : 'light'; engine.current?.setTheme(dark); }, [dark]);
  useEffect(() => { engine.current?.setSelected(selectedId); }, [selectedId]);
  useEffect(() => { for (const [k,v] of Object.entries(layers) as [SystemId,LayerState][]) engine.current?.setLayer(k,v); }, [layers]);
  useEffect(() => { engine.current?.setClip(clip.enabled, clip.axis, clip.offset); }, [clip]);
  useEffect(() => { engine.current?.setHiddenIds(hiddenIds); }, [hiddenIds, ready]);

  const setHidden = (ids: string[], hidden: boolean) => setHiddenIds(old => {
    const next = new Set(old);
    for (const id of ids) hidden ? next.add(id) : next.delete(id);
    return next;
  });

  const select = (s: Structure) => { setSelectedId(s.id); setQuery(''); if (engine.current?.hasGeometry(s.id) || s.landmark?.point) engine.current?.focus(s.id); };
  const geometryCount = (system: SystemId) => manifest.structures.filter((s) => s.system === system && s.asset).length;
  const plannedCount = (system: SystemId) => manifest.structures.filter((s) => s.system === system && !s.asset && !s.landmark && s.kind !== 'group').length;

  return <div className="atlas-app">
    <div className="atlas-stage" ref={stage} />
    <header className="identity">
      <h1>INR Anatomy Atlas</h1>
    </header>
    <div className="top-actions">
      <div className="search-wrap">
        <span className="search-icon">⌕</span>
        <input value={query} onChange={(e)=>setQuery(e.target.value)} placeholder="Search vessel, vein, bone or landmark…" aria-label="Search anatomy" />
        {query && <button className="clear" onClick={()=>setQuery('')} aria-label="Clear search">×</button>}
        {query && <div className="search-results panel">
          {results.length ? results.map((s)=><button key={s.id} onClick={()=>select(s)}>
            <span className={`sys-dot ${s.system}`} /><span><strong>{s.name}</strong></span><em>{s.landmark?'landmark':s.asset?'geometry':s.kind==='group'?'group':'planned'}</em>
          </button>) : <div className="empty">No matching structure</div>}
        </div>}
      </div>
      <button className="icon-btn" onClick={()=>setDark(!dark)} title="Toggle theme">{dark?'☀':'◐'}</button>
      <button className="icon-btn" onClick={()=>setAbout(true)} title={`About v${manifest.release}`}>i</button>
    </div>

    <div className="panel-stack">
    <details className="left-panel panel" open={controlsOpen} onToggle={e=>setControlsOpen(e.currentTarget.open)}>
      <summary className="panel-title">Layers and anatomy</summary>
      <div className="panel-body">
      <div className="tabs"><button className={tab==='layers'?'active':''} onClick={()=>setTab('layers')}>Layers</button><button className={tab==='tree'?'active':''} onClick={()=>setTab('tree')}>Anatomy</button></div>
      {tab==='layers' ? <>
        <div className="layer-list">{SYSTEMS.filter(sys=>geometryCount(sys.id)>0).map((sys)=><div className="layer-row" key={sys.id}>
          <button className={`state ${layers[sys.id]}`} onClick={()=>setLayers((x)=>({...x,[sys.id]:NEXT[x[sys.id]]}))} aria-label={`${sys.label}: ${layers[sys.id]}`}><span /></button>
          <button className="layer-name" onClick={()=>setTab('tree')}><span>{sys.label}</span><small>{sys.hint}</small></button>
          <div className="counts"><b>{geometryCount(sys.id)}</b><small>mesh</small><b>{plannedCount(sys.id)}</b><small>planned</small></div>
        </div>)}</div>
      </> : <StructureTree manifest={manifest} byId={byId} subtrees={subtrees} hiddenIds={hiddenIds} selectedId={selectedId} onSelect={select} onVisibility={(ids,shown)=>setHidden(ids,!shown)} />}
      </div>
    </details>

    {selected && <Detail open={inspectionOpen} onOpenChange={setInspectionOpen} structure={selected} manifest={manifest} engine={engine.current} hidden={(subtrees.get(selected.id)??[]).length>0&&(subtrees.get(selected.id)??[]).every(id=>hiddenIds.has(id))} onHidden={(hidden)=>setHidden(subtrees.get(selected.id)??[],hidden)} onClose={()=>setSelectedId(null)} />}
    </div>

    <div className="camera-bar panel">
      <div className="views"><button onClick={()=>engine.current?.setView('front')}>AP</button><button onClick={()=>engine.current?.setView('left')}>L</button><button onClick={()=>engine.current?.setView('right')}>R</button><button onClick={()=>engine.current?.setView('superior')}>Sup</button><button onClick={()=>engine.current?.setView('inferior')}>Inf</button><button onClick={()=>engine.current?.fitAll()}>Fit</button></div>
      <div className="clip-tools"><label><input type="checkbox" checked={clip.enabled} onChange={(e)=>setClip({...clip,enabled:e.target.checked})}/> Section</label><select value={clip.axis} onChange={(e)=>setClip({...clip,axis:e.target.value as typeof clip.axis})}><option value="sagittal">Sagittal</option><option value="coronal">Coronal</option><option value="axial">Axial</option></select><input type="range" min="-1" max="1" step="0.01" value={clip.offset} onChange={(e)=>setClip({...clip,offset:Number(e.target.value)})}/></div>
    </div>

    {!ready && !loadError && <div className="loading panel">Loading {manifest.title ?? 'CT-derived reference'}…</div>}
    {loadError && <div className="loading panel load-error"><b>Anatomy failed to load</b><span>{loadError}</span></div>}
    {about && <About manifest={manifest} onClose={()=>setAbout(false)} />}
  </div>;
}

function StructureTree({manifest,byId,subtrees,hiddenIds,selectedId,onSelect,onVisibility}:{manifest:AnatomyManifest;byId:Map<string,Structure>;subtrees:Map<string,string[]>;hiddenIds:ReadonlySet<string>;selectedId:string|null;onSelect:(s:Structure)=>void;onVisibility:(ids:string[],shown:boolean)=>void}) {
  const [open,setOpen]=useState<Set<string>>(() => new Set());
  const toggle=(id:string)=>setOpen((old)=>{const n=new Set(old);n.has(id)?n.delete(id):n.add(id);return n});
  const node=(id:string,depth=0):ReactNode=>{const s=byId.get(id);if(!s)return null;const has=s.children.length>0;const ids=subtrees.get(id)??[];const shown=ids.filter(id=>!hiddenIds.has(id)).length;return <div key={id}>
    <div className={`tree-row ${selectedId===id?'selected':''} ${ids.length?'has-geometry':'planned'}`} style={{paddingLeft:8+depth*14}}>
      <button className="twisty" onClick={()=>has&&toggle(id)} aria-label={`${open.has(id)?'Collapse':'Expand'} ${s.name}`} aria-expanded={has?open.has(id):undefined}>{has?(open.has(id)?'⌄':'›'):''}</button>
      <input className="tree-visibility" type="checkbox" checked={ids.length>0&&shown===ids.length} ref={el=>{if(el)el.indeterminate=shown>0&&shown<ids.length;}} disabled={!ids.length} aria-label={`Show ${s.name} and descendants`} onChange={e=>onVisibility(ids,e.target.checked)} />
      <button className="tree-name" onClick={()=>onSelect(s)}><span>{s.name}</span>{s.kind!=='group'&&<small>{s.landmark?(s.landmark.point?'landmark':'unlocated'):s.asset?'mesh':'planned'}</small>}</button>
    </div>{has&&open.has(id)&&s.children.map((c)=>node(c,depth+1))}
  </div>};
  return <div className="tree">{manifest.roots.map((r)=>node(r))}</div>;
}

function Detail({open,onOpenChange,structure,manifest,engine,hidden,onHidden,onClose}:{open:boolean;onOpenChange:(open:boolean)=>void;structure:Structure;manifest:AnatomyManifest;engine:AnatomyEngine|null;hidden:boolean;onHidden:(hidden:boolean)=>void;onClose:()=>void}) {
  const rels=manifest.relationships.filter((r)=>r.type!=='associated_passage'&&(r.from===structure.id||r.to===structure.id||(structure.displayGroup==='anastomoses'&&r.type==='potential_anastomosis'&&r.note===structure.name)));
  const nameFor=(id:string)=>manifest.structures.find(s=>s.id===id)?.name??'Unknown structure';
  return <details className="detail panel" open={open} onToggle={e=>onOpenChange(e.currentTarget.open)}>
    <summary className="panel-title"><span className={`sys-dot ${structure.system}`}/><h2>{structure.name}</h2></summary>
    <button className="detail-close" onClick={onClose} aria-label="Close structure details">×</button>
    <div className="detail-body">
    <div className="detail-system">{structure.system}</div>
    {structure.landmark&&<div className="geometry-status planned">Landmark · {structure.landmark.status.replaceAll('-',' ')}</div>}
    <dl><dt>Side</dt><dd>{structure.side}</dd></dl>
    {structure.asset||structure.landmark?.point||manifest.structures.some(s=>s.segmentOf===structure.id)?<div className="detail-actions"><button onClick={()=>engine?.focus(structure.id)}>Focus</button><button onClick={()=>onHidden(!hidden)}>{hidden?'Show':'Hide'}</button></div>:!structure.landmark&&structure.kind!=='group'&&<p className="planned-copy">The logical structure exists now so models, search, relationships and saved views can use a stable ID before geometry is added.</p>}
    {rels.length>0&&<section><h3>Relationships</h3>{rels.map((r,i)=><div className="relationship" key={i}><b>{r.type.replaceAll('_',' ')}</b><span>{r.from===structure.id?nameFor(r.to):r.to===structure.id?nameFor(r.from):`${nameFor(r.from)} → ${nameFor(r.to)}`}</span></div>)}</section>}
    </div>
  </details>;
}

function About({manifest,onClose}:{manifest:AnatomyManifest;onClose:()=>void}) {
  return <div className="modal-scrim" onClick={onClose}><div className="about panel" onClick={(e)=>e.stopPropagation()}><button className="detail-close" onClick={onClose}>×</button><h2>INR Anatomy Atlas v{manifest.release}</h2><p>{manifest.description}</p><p><b>{manifest.structures.length}</b> logical structures and <b>{manifest.relationships.length}</b> explicit cross-structure relationships are currently defined.</p><button className="primary" onClick={onClose}>Close</button></div></div>;
}
