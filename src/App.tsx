import { useEffect, useMemo, useRef, useState, type ReactNode } from 'react';
import type { AnatomyManifest, LayerState, Structure, SystemId } from './types';
import { geometrySubtrees, searchStructures } from './catalogue';
import { AnatomyEngine } from './engine';
import { Description } from './Description';
import { Loading } from './Loading';

const DEFAULT_VISIBILITY: Record<SystemId, LayerState> = { bone: 'ghost', artery: 'on', vein: 'off', brain: 'off' };
const NEXT: Record<LayerState, LayerState> = { on: 'ghost', ghost: 'off', off: 'on' };
const STATE_LABEL = { on: 'fully visible', ghost: 'translucent', off: 'absent' };

export function App({ manifest }: { manifest: AnatomyManifest }) {
  const stage = useRef<HTMLDivElement>(null);
  const engine = useRef<AnatomyEngine | null>(null);
  const fpsReadout = useRef<HTMLDivElement>(null);
  const [selectedId, setSelectedId] = useState<string | null>(null);
  const [query, setQuery] = useState('');
  const [visibility, setVisibility] = useState<Map<string, LayerState>>(() => new Map(manifest.structures
    .filter(s => s.asset || s.landmark?.point).map(s => [s.id, DEFAULT_VISIBILITY[s.system]])));
  const [controlsOpen, setControlsOpen] = useState(false);
  const [inspectionOpen, setInspectionOpen] = useState(false);
  const [focusedId, setFocusedId] = useState<string | null>(null);
  const [dark, setDark] = useState(true);
  const [ready, setReady] = useState(false);
  const [loadProgress, setLoadProgress] = useState(0);
  const [loadError, setLoadError] = useState<string | null>(null);
  const [clip, setClip] = useState({ enabled: false, axis: 'sagittal' as 'sagittal'|'coronal'|'axial', offset: 0 });
  const [about, setAbout] = useState(false);
  const byId = useMemo(() => new Map(manifest.structures.map((s) => [s.id, s])), [manifest]);
  const subtrees = useMemo(() => geometrySubtrees(byId), [byId]);
  const selected = selectedId ? byId.get(selectedId) ?? null : null;
  const selectedGeometry = selected ? subtrees.get(selected.id) ?? [] : [];
  const selectedHidden = selectedGeometry.length > 0 && selectedGeometry.every(id => visibility.get(id) === 'off');
  const canFocus = !!selected && !!(selected.asset || selected.landmark?.point || (selected.system === 'brain' && selectedGeometry.length) || manifest.structures.some(s => s.segmentOf === selected.id));
  const results = useMemo(() => searchStructures(manifest.structures, query), [manifest.structures, query]);

  useEffect(() => {
    if (!stage.current) return;
    let cancelled = false;
    setReady(false); setLoadError(null); setLoadProgress(0);
    const e = new AnatomyEngine(stage.current, manifest, id => { setSelectedId(id); setFocusedId(null); }, fps => {
      // Update this small readout without rerendering the anatomy panels.
      if (fpsReadout.current) {
        fpsReadout.current.textContent = fps === null ? '' : `${fps} FPS`;
        fpsReadout.current.hidden = fps === null;
      }
    }); engine.current = e; e.setTheme(dark);
    e.load(percent => { if (!cancelled) setLoadProgress(percent); }).then(() => { if (cancelled) return; setReady(true); setLoadError(null); e.start(); }).catch((err) => { if (cancelled) return; console.error(err); setLoadError(err instanceof Error ? err.message : String(err)); });
    return () => { cancelled = true; e.dispose(); engine.current = null; };
  }, [manifest]);
  useEffect(() => { document.documentElement.dataset.theme = dark ? 'dark' : 'light'; engine.current?.setTheme(dark); }, [dark]);
  useEffect(() => { engine.current?.setSelected(selectedId); }, [selectedId]);
  useEffect(() => { engine.current?.setFocus(focusedId); }, [focusedId, ready]);
  useEffect(() => { engine.current?.setClip(clip.enabled, clip.axis, clip.offset); }, [clip]);
  useEffect(() => { engine.current?.setVisibility(visibility); }, [visibility, ready]);

  const changeVisibility = (ids: string[], state: LayerState) => setVisibility(old => {
    const next = new Map(old);
    for (const id of ids) next.set(id, state);
    return next;
  });
  const changeClip = (next: typeof clip) => {
    setFocusedId(null);
    setClip(next);
  };

  const select = (s: Structure) => {
    setSelectedId(s.id); setFocusedId(null); setQuery('');
    if (s.system === 'vein' && s.asset) {
      const veins = manifest.structures.filter(row => row.system === 'vein' && row.asset).map(row => row.id);
      if (veins.every(id => visibility.get(id) === 'off')) changeVisibility(veins, 'on');
    }
    if (s.system === 'brain') {
      const ids = s.landmark ? [s.id, ...(s.vesselGuide?.surfaceStructureIds ?? [])] : subtrees.get(s.id) ?? [];
      changeVisibility(ids.filter(id => visibility.get(id) === 'off'), 'on');
    }
    if (engine.current?.hasGeometry(s.id) || s.landmark?.point) engine.current?.focus(s.id);
  };

  return <div className="atlas-app" onClickCapture={e => {
    if (focusedId && !(e.target as Element).closest('[data-focus-control], .clip-tools')) setFocusedId(null);
  }}>
    <div className="atlas-stage" ref={stage} />
    <header className="identity">
      <h1>Neurovascular Atlas</h1>
    </header>
    <div className="top-actions">
      <div className="search-wrap">
        <span className="search-icon">⌕</span>
        <input value={query} onChange={(e)=>setQuery(e.target.value)} placeholder="Search anatomy or alternate name…" aria-label="Search anatomy" />
        {query && <button className="clear" onClick={()=>setQuery('')} aria-label="Clear search">×</button>}
        {query && <div className="search-results panel">
          {results.length ? results.map((s)=><button key={s.id} onClick={()=>select(s)}>
            <span className={`sys-dot ${s.system}`} /><span><strong>{s.name}</strong></span><em>{s.landmark?'landmark':s.asset?'geometry':s.kind==='group'?'group':''}</em>
          </button>) : <div className="empty">No matching structure</div>}
        </div>}
      </div>
      <button className="icon-btn" onClick={()=>setDark(!dark)} title="Toggle theme">{dark?'☀':'◐'}</button>
      <button className="icon-btn" onClick={()=>setAbout(true)} title={`About v${manifest.release}`}>i</button>
    </div>

    <div className="bottom-dock">
    <div className="panel-stack">
    <section className="left-panel panel">
      <button className="panel-title" aria-expanded={controlsOpen} aria-controls="anatomy-panel-body" onClick={()=>setControlsOpen(!controlsOpen)}>Layers and anatomy</button>
      <div className="panel-body" id="anatomy-panel-body" hidden={!controlsOpen}>
      <StructureTree manifest={manifest} byId={byId} subtrees={subtrees} visibility={visibility} selectedId={selectedId} onSelect={select} onVisibility={changeVisibility} />
      </div>
    </section>

    {selected && <Detail open={inspectionOpen} onOpenChange={setInspectionOpen} structure={selected} manifest={manifest} byId={byId} onSelect={select} />}
    </div>

    <div className="camera-bar panel">
      <div className="selection-actions">
        <button data-focus-control aria-pressed={focusedId !== null} disabled={!ready || !canFocus} onClick={() => {
          if (!selected) return;
          setFocusedId(focusedId === selected.id ? null : selected.id);
          if (focusedId !== selected.id) engine.current?.focus(selected.id);
        }}>Focus</button>
        <button disabled={!ready || !selectedGeometry.length} onClick={() => changeVisibility(selectedGeometry, selectedHidden ? 'on' : 'off')}>{selectedHidden ? 'Show' : 'Hide'}</button>
      </div>
      <div className="views"><button onClick={()=>engine.current?.setView('front')}>AP</button><button onClick={()=>engine.current?.setView('left')}>L</button><button onClick={()=>engine.current?.setView('right')}>R</button><button onClick={()=>engine.current?.setView('superior')}>Sup</button><button onClick={()=>engine.current?.setView('inferior')}>Inf</button></div>
      <div className="clip-tools"><label><input type="checkbox" checked={clip.enabled} onChange={(e)=>changeClip({...clip,enabled:e.target.checked})}/> Section</label><select value={clip.axis} onChange={(e)=>changeClip({...clip,axis:e.target.value as typeof clip.axis})}><option value="sagittal">Sagittal</option><option value="coronal">Coronal</option><option value="axial">Axial</option></select><input type="range" min="-1" max="1" step="0.01" value={clip.offset} onChange={(e)=>changeClip({...clip,offset:Number(e.target.value)})}/></div>
    </div>
    </div>

    <div className="fps-readout" ref={fpsReadout} aria-label="Frame rate" aria-live="off" hidden />
    {!ready && !loadError && <Loading progress={loadProgress} />}
    {loadError && <div className="loading panel load-error"><b>Anatomy failed to load</b><span>{loadError}</span></div>}
    {about && <About manifest={manifest} onClose={()=>setAbout(false)} />}
  </div>;
}

function StructureTree({manifest,byId,subtrees,visibility,selectedId,onSelect,onVisibility}:{manifest:AnatomyManifest;byId:Map<string,Structure>;subtrees:Map<string,string[]>;visibility:ReadonlyMap<string,LayerState>;selectedId:string|null;onSelect:(s:Structure)=>void;onVisibility:(ids:string[],state:LayerState)=>void}) {
  const [open,setOpen]=useState<Set<string>>(() => new Set());
  const toggle=(id:string)=>setOpen((old)=>{const n=new Set(old);n.has(id)?n.delete(id):n.add(id);return n});
  const node=(id:string,depth=0):ReactNode=>{const s=byId.get(id);if(!s)return null;const has=s.children.length>0;const ids=subtrees.get(id)??[];
    const states=new Set(ids.map(key=>visibility.get(key)??DEFAULT_VISIBILITY[s.system]));
    const state:LayerState|'mixed'=states.size>1?'mixed':states.values().next().value??'off';
    const next=state==='mixed'?'on':NEXT[state];return <div key={id}>
    <div className={`tree-row ${selectedId===id?'selected':''} ${ids.length?'has-geometry':'planned'}`} style={{paddingLeft:8+depth*14}}>
      <button className="twisty" onClick={()=>has&&toggle(id)} aria-label={`${open.has(id)?'Collapse':'Expand'} ${s.name}`} aria-expanded={has?open.has(id):undefined}>{has?(open.has(id)?'⌄':'›'):''}</button>
      <button className="tree-name" onClick={()=>onSelect(s)}><span>{s.name}</span>{s.landmark&&<small>{s.landmark.point?'landmark':'unlocated'}</small>}</button>
      <button className={`tree-visibility state ${state}`} data-state={state} disabled={!ids.length} aria-label={`${s.name}: ${state==='mixed'?'mixed visibility':STATE_LABEL[state]}. Set ${STATE_LABEL[next]}`} aria-pressed={state==='mixed'?'mixed':state==='on'} onClick={()=>onVisibility(ids,next)}><span /></button>
    </div>{has&&open.has(id)&&s.children.map((c)=>node(c,depth+1))}
  </div>};
  return <div className="tree">{manifest.roots.map((r)=>node(r))}</div>;
}

function Detail({open,onOpenChange,structure,manifest,byId,onSelect}:{open:boolean;onOpenChange:(open:boolean)=>void;structure:Structure;manifest:AnatomyManifest;byId:ReadonlyMap<string,Structure>;onSelect:(structure:Structure)=>void}) {
  const rels=manifest.relationships.filter((r)=>r.type!=='associated_passage'&&(r.from===structure.id||r.to===structure.id||(structure.displayGroup==='anastomoses'&&r.type==='potential_anastomosis'&&r.note===structure.name)));
  const groups=new Map<string,Set<string>>();
  for (const r of rels) {
    const ids=r.from===structure.id?[r.to]:r.to===structure.id?[r.from]:[r.from,r.to];
    const type = r.type === 'drains_to' && r.to === structure.id ? 'receives_from' : r.type;
    if (!groups.has(type)) groups.set(type,new Set());
    for (const id of ids) if (byId.has(id)) groups.get(type)!.add(id);
  }
  return <section className="detail panel">
    <button className="panel-title" aria-expanded={open} aria-controls="structure-panel-body" onClick={()=>onOpenChange(!open)}><span className="structure-title">{structure.name}</span></button>
    <div className="detail-body" id="structure-panel-body" hidden={!open}>
    <div className="detail-system">{structure.system}</div>
    {structure.aliases.length>0&&<section><h3>Alternate names</h3><p>{structure.aliases.join(' · ')}</p></section>}
    {structure.landmark&&<div className="geometry-status planned">Landmark · {structure.landmark.status.replaceAll('-',' ')}</div>}
    {structure.description?.trim()&&<Description text={structure.description} byId={byId} onSelect={onSelect} />}
    {structure.anatomicalReview&&<section className="anatomical-review"><h3>Model review</h3><p>{structure.anatomicalReview.summary}</p></section>}
    {structure.vesselCourse?.scope==='intracranial'&&<section><h3>Anatomical course</h3><p>{structure.vesselCourse.summary}</p>
      {structure.vesselCourse.coursePaths&&<ol>{structure.vesselCourse.segments.map(segment=><li key={segment.order}><strong>{segment.mode==='pial'?'Surface / fissural course':segment.mode==='cisternal'?'Cisternal outlet':segment.mode.replaceAll('-',' ')}:</strong> {segment.summary}</li>)}</ol>}
      <p>{structure.vesselCourse.targetStructureIds.map((id,i)=><span key={id}>{i>0?', ':''}<a href={`#structure-${id}`} onClick={e=>{e.preventDefault();const target=byId.get(id);if(target)onSelect(target);}}>{byId.get(id)?.name}</a></span>)}</p>
    </section>}
    {structure.vesselGuide&&<section><h3>Vessel course guides</h3><p>{structure.vesselGuide.vesselNames.join(' · ')}</p><p>Regional orientation points; vessel courses require individual fitting.</p></section>}
    {groups.size>0&&<section><h3>Relationships</h3>{[...groups].map(([type,ids])=><div className="relationship" key={type}><b>{type.replaceAll('_',' ').replace(/^./,letter=>letter.toUpperCase())}: </b>{[...ids].map((id,i)=><span key={id}>{i>0?', ':''}<a href={`#structure-${id}`} onClick={e=>{e.preventDefault();onSelect(byId.get(id)!);}}>{byId.get(id)!.name}</a></span>)}</div>)}</section>}
    </div>
  </section>;
}

function About({manifest,onClose}:{manifest:AnatomyManifest;onClose:()=>void}) {
  return <div className="modal-scrim" onClick={onClose}><div className="about panel" role="dialog" aria-modal="true" aria-labelledby="about-title" onClick={(e)=>e.stopPropagation()}>
    <button className="detail-close" aria-label="Close information" onClick={onClose}>×</button>
    <h2 id="about-title">Neurovascular Atlas v{manifest.release}</h2>
    <p>An interactive 3D atlas of neurovascular anatomy, with selectable structures, anatomical descriptions and vascular relationships.</p>
    <p>Authored by Jeremy Lynch, 2026.</p>
    <div className="about-credits" role="region" aria-label="Credits" tabIndex={0}>
      <h3>Software credits</h3>
      <ul>
        <li><strong>React and React DOM</strong>: user interface. MIT licence.</li>
        <li><strong>Three.js</strong>: interactive 3D rendering. MIT licence.</li>
        <li><strong>Meshoptimizer</strong>: mesh optimisation and compression. MIT licence.</li>
        <li><strong>Vite</strong>: development and build tooling. MIT licence.</li>
        <li><strong>TypeScript</strong>: application development. Apache 2.0 licence.</li>
        <li><strong>NumPy, SciPy and VTK</strong>: anatomical geometry processing and validation. BSD licences.</li>
        <li><strong>Manifold3D</strong>: solid geometry operations. Apache 2.0 licence.</li>
        <li><strong>Trimesh</strong>: mesh inspection and validation. MIT licence.</li>
        <li><strong>Inter Tight, JetBrains Mono and Source Serif 4</strong>, distributed through Fontsource: interface typography. SIL Open Font Licence 1.1.</li>
      </ul>
      <h3>Anatomical model credits</h3>
      <ul><li><strong>BodyParts3D</strong>, © The Database Center for Life Science: source geometry for bony anatomical context. CC BY-SA 2.1 Japan.</li><li><strong><a href="https://www.z-anatomy.com/" target="_blank" rel="noopener noreferrer">Z-Anatomy</a></strong>: brain, ventricles, falx and tentorium, registered to this atlas. Adapted surfaces: CC BY-SA 4.0, with original BodyParts3D credit retained. <a href={`${import.meta.env.BASE_URL}anatomy/licenses/Z_Anatomy_Source_Licence.txt`} target="_blank" rel="noopener noreferrer">Source licence and credits</a>.</li></ul>
      <h3>Anatomical references</h3>
      <ul>
        <li><strong>Jeremy Lynch, Shelley Renowden and Philip White</strong>, editors. <a href="https://academic.oup.com/book/63036" target="_blank" rel="noopener noreferrer"><em>Neurointervention</em></a>. Oxford Specialist Handbooks. Oxford University Press, 2026.</li>
        <li><strong>Neil M. Borden</strong>. <em>3D Angiographic Atlas of Neurovascular Anatomy and Pathology</em>. 2006.</li>
        <li><strong>Hiro Kiyosue</strong>, editor. <em>External Carotid Artery: Imaging Anatomy Atlas for Endovascular Treatment</em>. 2020.</li>
        <li><strong>Gianni Boris Bradač</strong>. <em>Applied Cerebral Angiography: Normal Anatomy and Vascular Pathology</em>. 2017.</li>
        <li><strong><a href="https://neuroangio.org/" target="_blank" rel="noopener noreferrer">Neuroangio.org</a></strong>, by Maksim Shapiro, MD: angiographic anatomy, arterial relationships, venous drainage and anatomical variants.</li>
      </ul>
      <p>Anatomical references inform the atlas’s reconstructions and descriptions. Referenced book figures are not reproduced in the application.</p>
    </div>
    <button className="primary" onClick={onClose}>Close</button>
  </div></div>;
}
