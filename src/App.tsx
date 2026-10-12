import { useCallback, useEffect, useMemo, useRef, useState, type ReactNode } from 'react';
import type { AnatomyManifest, LayerState, Structure, SystemId } from './types';
import { geometrySubtrees, searchStructures, uniqueVesselCounts } from './catalogue';
import { AnatomyEngine } from './engine';
import { Description } from './Description';
import { Loading } from './Loading';
import { BookmarkIcon, PresetModal } from './PresetModal';
import { ANATOMICAL_PRESETS, injectionPreset, presetDirection, presetVesselIds, presetVisibility, type PresetId, type PresetSide } from './presets';
import { DsaControls, DsaIcon, InjectionControls } from './DsaControls';
import { makeDsaRun, DSA_END, type DsaRun } from './dsa';
import type { InjectionPoint } from './flowGeometry';

const DEFAULT_VISIBILITY: Record<SystemId, LayerState> = { bone: 'ghost', artery: 'on', vein: 'on', brain: 'off' };
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
  const [presetsOpen, setPresetsOpen] = useState(false);
  const [presetSide, setPresetSide] = useState<PresetSide>('left');
  const [activePreset, setActivePreset] = useState<{id: PresetId; side: PresetSide}>({id: 'ica', side: 'left'});
  const [dsa, setDsa] = useState(false);
  const [dsaSelectedId,setDsaSelectedId]=useState<string|null>(null);
  const [dsaInspectionOpen,setDsaInspectionOpen]=useState(false);
  const [dsaBusy, setDsaBusy] = useState(false);
  const [dsaError, setDsaError] = useState<string | null>(null);
  const [dsaTime, setDsaTime] = useState(2);
  const [playing, setPlaying] = useState(false);
  const [injection,setInjection]=useState<InjectionPoint|null>(null);
  const [injectionReady,setInjectionReady]=useState(false);
  const [placing,setPlacing]=useState(false);
  const [placementVessel,setPlacementVessel]=useState<string|null>(null);
  const runRef=useRef<DsaRun|null>(null);
  const closePresets = useCallback(() => setPresetsOpen(false), []);
  const byId = useMemo(() => new Map(manifest.structures.map((s) => [s.id, s])), [manifest]);
  const subtrees = useMemo(() => geometrySubtrees(byId), [byId]);
  const selected = selectedId ? byId.get(selectedId) ?? null : null;
  const inspected=dsa?(dsaSelectedId?byId.get(dsaSelectedId)??null:null):selected;
  const selectedGeometry = selected ? subtrees.get(selected.id) ?? [] : [];
  const selectedHidden = selectedGeometry.length > 0 && selectedGeometry.every(id => visibility.get(id) === 'off');
  const canFocus = !!selected && !!(selected.asset || selected.landmark?.point || (selected.system === 'brain' && selectedGeometry.length) || manifest.structures.some(s => s.segmentOf === selected.id));
  const results = useMemo(() => searchStructures(manifest.structures, query).filter(s=>!placing||engine.current?.getDsaFlow()?.entries[s.id]?.selectable), [manifest.structures, query,placing]);

  useEffect(() => {
    if (!stage.current) return;
    let cancelled = false;
    setReady(false); setLoadError(null); setLoadProgress(0);
    const e = new AnatomyEngine(stage.current, manifest, (id,isDsa) => { if(isDsa){setDsaSelectedId(id);setDsaInspectionOpen(!!id);setPlaying(false);}else{setSelectedId(id);setFocusedId(null);} }, fps => {
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
  useEffect(() => { engine.current?.setDsaSelected(dsaSelectedId); }, [dsaSelectedId]);
  useEffect(() => { engine.current?.setFocus(focusedId); }, [focusedId, ready]);
  useEffect(() => { engine.current?.setClip(clip.enabled, clip.axis, clip.offset); }, [clip]);
  useEffect(() => { engine.current?.setVisibility(visibility); }, [visibility, ready]);
  useEffect(() => { engine.current?.setPaused(presetsOpen || about); }, [presetsOpen, about, ready]);
  useEffect(() => { engine.current?.setDsaTime(dsaTime); }, [dsaTime]);
  useEffect(() => {
    if (!dsa || !playing || placing || presetsOpen || about) return;
    const timer = window.setInterval(() => { if (!document.hidden) setDsaTime(t => Math.min(DSA_END,t+.5)); },500);
    return () => clearInterval(timer);
  }, [dsa, playing, placing,presetsOpen, about]);
  useEffect(() => { if (dsaTime===DSA_END) setPlaying(false); }, [dsaTime]);

  const clearDsaInspection=()=>{setDsaSelectedId(null);setDsaInspectionOpen(false);};
  const toggleDsa = async () => {
    clearDsaInspection();
    setDsaBusy(true); setDsaError(null); setPlaying(false);
    try {
      const e = engine.current;
      if (!e) return;
      if (dsa) { await e.setDsa(null); setDsa(false);setPlacing(false);setQuery(''); }
      else {
        const flow=await e.prepareDsa();
        const run = injectionReady?makeDsaRun(manifest,activePreset.id,activePreset.side,flow,injection):{arteries:[],vessels:[],blush:[]};
        await e.setDsa(run); setDsaTime(2); e.setDsaTime(2);
        runRef.current=injectionReady?run:null;setDsa(true);
        if(!injectionReady)startPlacement(null);
      }
    } catch (error) { setDsaError(error instanceof Error ? error.message : String(error)); }
    finally { setDsaBusy(false); }
  };

  const cancelPlacement=()=>{engine.current?.endInjectionPlacement();setPlacing(false);setQuery('');if(!runRef.current){void engine.current?.setDsa(null);setDsa(false);}};
  const startPlacement=(id:string|null)=>{setPlaying(false);setQuery('');setDsaError(null);setPlacementVessel(id);setPlacing(true);engine.current?.beginInjectionPlacement(id,commitInjection);};
  const commitInjection=async (id:string,point:InjectionPoint|null)=>{
    if(!point){setPlacementVessel(id);return;}
    const e=engine.current,flow=e?.getDsaFlow();if(!e||!flow)return;
    setDsaBusy(true);setDsaError(null);
    try{
      const preset=injectionPreset(id),side=byId.get(id)?.side==='right'?'right':'left';
      const run=makeDsaRun(manifest,preset,side,flow,point);
      if(!run.arteries.length)throw Error('No downstream vessels at this point');
      await e.setDsa(run);clearDsaInspection();runRef.current=run;setInjection(point);setInjectionReady(true);setActivePreset({id:preset,side});setPresetSide(side);
      setDsaTime(0);e.setDsaTime(0);cancelPlacement();
    }catch(error){setDsaError(error instanceof Error?error.message:String(error));}
    finally{setDsaBusy(false);}
  };
  const beginPlacement=()=>{
    const e=engine.current,flow=e?.getDsaFlow();if(!e||!flow)return;
    const first=runRef.current?.inlets?.find(p=>byId.get(p.id)?.side==='left')??runRef.current?.inlets?.[0];
    const candidate=injection?.id??(dsaSelectedId&&flow.entries[dsaSelectedId]?.selectable?dsaSelectedId:null)??(selectedId&&flow.entries[selectedId]?.selectable?selectedId:first?.id??null);
    const id=candidate&&flow.entries[candidate]?.selectable?candidate:null;
    startPlacement(id);
  };
  const resetInjection=async ()=>{
    const e=engine.current,flow=e?.getDsaFlow();if(!e||!flow)return;
    setDsaBusy(true);setPlaying(false);
    try{const run=makeDsaRun(manifest,activePreset.id,activePreset.side,flow);await e.setDsa(run);clearDsaInspection();runRef.current=run;setInjection(null);setDsaTime(2);e.setDsaTime(2);setDsaError(null);}
    catch(error){setDsaError(error instanceof Error?error.message:String(error));}finally{setDsaBusy(false);}
  };
  useEffect(()=>{
    if(!placing)return;const key=(e:KeyboardEvent)=>{if(e.key==='Escape')cancelPlacement();};
    window.addEventListener('keydown',key);return()=>window.removeEventListener('keydown',key);
  },[placing]);

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
    if(placing){setPlacementVessel(s.id);setQuery('');engine.current?.selectInjectionVessel(s.id);return;}
    if(dsa){setDsaSelectedId(s.id);setDsaInspectionOpen(true);setPlaying(false);return;}
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

  const applyPreset = async (preset: PresetId) => {
    const ids = presetVesselIds(manifest, preset, presetSide);
    if (!ready || !ids.length) return;
    if (dsa) {
      try {
        const flow=await engine.current!.prepareDsa(),run = makeDsaRun(manifest,preset,presetSide,flow);
        await engine.current?.setDsa(run); setPlaying(false); setDsaTime(2); engine.current?.setDsaTime(2);
        runRef.current=run;clearDsaInspection();setInjection(null);setInjectionReady(true);cancelPlacement();
        engine.current?.framePreset(run.arteries,presetDirection(preset,presetSide));
        setActivePreset({id: preset, side: presetSide}); setPresetsOpen(false); setDsaError(null);
      } catch (error) { setDsaError(error instanceof Error ? error.message : String(error)); setPresetsOpen(false); }
      return;
    }
    setActivePreset({id: preset, side: presetSide});
    setInjection(null);setInjectionReady(true);
    const next = presetVisibility(manifest, visibility, ids);
    setSelectedId(null); setFocusedId(null); setQuery('');
    setVisibility(next); setClip(old => ({ ...old, enabled: false }));
    engine.current?.setSelected(null);
    engine.current?.setFocus(null);
    engine.current?.setClip(false, clip.axis, clip.offset);
    engine.current?.setVisibility(next);
    engine.current?.framePreset(ids, presetDirection(preset, presetSide));
    setPresetsOpen(false);
  };

  return <div className="atlas-app" onClickCapture={e => {
    // Canvas selection clears focus through the engine callback. A browser
    // click emitted after dragging must not clear the focused structure.
    if (!dsa && focusedId && !(e.target as Element).closest('[data-focus-control], .clip-tools, .atlas-canvas, .presets-scrim')) setFocusedId(null);
  }}>
    <div className="atlas-stage" ref={stage} inert={presetsOpen || about} />
    <header className="identity">
      <h1>Neurovascular Atlas</h1>
    </header>
    <div className="top-actions">
      <div className="search-wrap">
        <span className="search-icon">⌕</span>
        <input disabled={(dsa&&!placing) || dsaBusy} value={query} onChange={(e)=>setQuery(e.target.value)} placeholder={placing?'Search an artery…':'Search anatomy or alternate name…'} aria-label="Search anatomy" />
        {query && (!dsa||placing) && <button className="clear" onClick={()=>setQuery('')} aria-label="Clear search">×</button>}
        {query && (!dsa||placing) && <div className="search-results panel">
          {results.length ? results.map((s)=><button key={s.id} onClick={()=>select(s)}>
            <span className={`sys-dot ${s.system}`} /><span><strong>{s.name}</strong></span><em>{s.landmark?'landmark':s.asset?'geometry':s.kind==='group'?'group':''}</em>
          </button>) : <div className="empty">No matching structure</div>}
        </div>}
      </div>
      <button className="icon-btn" disabled={dsa} onClick={()=>setDark(!dark)} title="Toggle theme">{dark?'☀':'◐'}</button>
      <button className="icon-btn" onClick={()=>setAbout(true)} title={`About v${manifest.release}`}>i</button>
    </div>

    <div className="bottom-dock">
    <div className={`panel-stack${dsa?' dsa-inspection':''}`} hidden={dsa&&(!inspected||placing)}>
    <section className="left-panel panel" hidden={dsa}>
      <button className="panel-title" aria-expanded={controlsOpen} aria-controls="anatomy-panel-body" onClick={()=>setControlsOpen(!controlsOpen)}>Layers and anatomy</button>
      <div className="panel-body" id="anatomy-panel-body" hidden={!controlsOpen}>
      <StructureTree manifest={manifest} byId={byId} subtrees={subtrees} visibility={visibility} selectedId={selectedId} onSelect={select} onVisibility={changeVisibility} />
      </div>
    </section>

    {inspected && <Detail open={dsa?dsaInspectionOpen:inspectionOpen} onOpenChange={dsa?setDsaInspectionOpen:setInspectionOpen} structure={inspected} manifest={manifest} byId={byId} onSelect={select} />}
    </div>

    <div className="camera-bar panel">
      {!dsa && <div className="selection-actions">
        <button data-focus-control aria-pressed={focusedId !== null} disabled={!ready || !canFocus} onClick={() => {
          if (!selected) return;
          setFocusedId(focusedId === selected.id ? null : selected.id);
          if (focusedId !== selected.id) engine.current?.focus(selected.id);
        }}>Focus</button>
        <button disabled={!ready || !selectedGeometry.length} onClick={() => changeVisibility(selectedGeometry, selectedHidden ? 'on' : 'off')}>{selectedHidden ? 'Show' : 'Hide'}</button>
      </div>}
      <div className="views"><button onClick={()=>engine.current?.setView('front')}>AP</button><button onClick={()=>engine.current?.setView('left')}>L</button><button onClick={()=>engine.current?.setView('right')}>R</button><button onClick={()=>engine.current?.setView('superior')}>Sup</button><button onClick={()=>engine.current?.setView('inferior')}>Inf</button></div>
      <button className="bookmark-button" data-focus-control disabled={!ready} aria-label="Anatomical presets" aria-haspopup="dialog" aria-expanded={presetsOpen} onClick={() => setPresetsOpen(true)}><BookmarkIcon /></button>
      <button className="bookmark-button dsa-button" data-focus-control disabled={!ready || dsaBusy} aria-label="DSA mode" title={dsaBusy ? 'Preparing DSA…' : 'DSA mode'} aria-pressed={dsa} onClick={toggleDsa}><DsaIcon /></button>
      {!dsa && <div className="clip-tools"><label><input type="checkbox" checked={clip.enabled} onChange={(e)=>changeClip({...clip,enabled:e.target.checked})}/> Section</label><select value={clip.axis} onChange={(e)=>changeClip({...clip,axis:e.target.value as typeof clip.axis})}><option value="sagittal">Sagittal</option><option value="coronal">Coronal</option><option value="axial">Axial</option></select><input type="range" min="-1" max="1" step="0.01" value={clip.offset} onChange={(e)=>changeClip({...clip,offset:Number(e.target.value)})}/></div>}
    </div>
    {dsa && (placing?<InjectionControls name={placementVessel?byId.get(placementVessel)?.name??null:null} busy={dsaBusy} onChange={()=>{setPlacementVessel(null);engine.current?.selectInjectionVessel(null);}} onCancel={cancelPlacement}/>:<DsaControls time={dsaTime} playing={playing} territory={injection?byId.get(injection.id)!.name:`${ANATOMICAL_PRESETS.find(p=>p.id===activePreset.id)!.label} · ${activePreset.side}`} onTime={setDsaTime} onPlaying={setPlaying} onPlacement={beginPlacement} onReset={resetInjection} custom={!!injection} busy={dsaBusy}/>)}
    {dsaError && <div className="dsa-error panel" role="alert">{dsaError}<button aria-label="Dismiss DSA error" onClick={()=>setDsaError(null)}>×</button></div>}
    </div>

    <div className="fps-readout" ref={fpsReadout} aria-label="Frame rate" aria-live="off" hidden />
    {!ready && !loadError && <Loading progress={loadProgress} />}
    {loadError && <div className="loading panel load-error"><b>Anatomy failed to load</b><span>{loadError}</span></div>}
    {about && <About manifest={manifest} onClose={()=>setAbout(false)} />}
    {presetsOpen && <PresetModal side={presetSide} onSideChange={setPresetSide} onApply={applyPreset} onClose={closePresets} />}
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
    <h2 className="detail-name">{structure.name}</h2>
    {structure.aliases.length>0&&<section><h3>Alternate names</h3><p>{structure.aliases.join(' · ')}</p></section>}
    {structure.description?.trim()&&<Description text={structure.description} byId={byId} onSelect={onSelect} />}
    {groups.size>0&&<section><h3>Relationships</h3>{[...groups].map(([type,ids])=><div className="relationship" key={type}><b>{type.replaceAll('_',' ').replace(/^./,letter=>letter.toUpperCase())}: </b>{[...ids].map((id,i)=><span key={id}>{i>0?', ':''}<a href={`#structure-${id}`} onClick={e=>{e.preventDefault();onSelect(byId.get(id)!);}}>{byId.get(id)!.name}</a></span>)}</div>)}</section>}
    </div>
  </section>;
}

function About({manifest,onClose}:{manifest:AnatomyManifest;onClose:()=>void}) {
  const counts = uniqueVesselCounts(manifest.structures);
  return <div className="modal-scrim" onClick={onClose}><div className="about panel" role="dialog" aria-modal="true" aria-labelledby="about-title" onClick={(e)=>e.stopPropagation()}>
    <button className="detail-close" aria-label="Close information" onClick={onClose}>×</button>
    <h2 id="about-title">Neurovascular Atlas v{manifest.release}</h2>
    <p>An interactive 3D atlas of neurovascular anatomy. Vascular structures original, skull and brain from existing sources (see below).</p>
    <p>{counts.artery} unique arteries and {counts.vein} unique veins, sinuses and venous plexuses.</p>
    <p>Jeremy Lynch, Sean McIlhone</p>
    <div className="about-credits" role="region" aria-label="Credits" tabIndex={0}>
      <h3>Anatomical references</h3>
      <ul>
        <li><strong>Jeremy Lynch, Shelley Renowden and Philip White</strong>, editors. <a href="https://academic.oup.com/book/63036" target="_blank" rel="noopener noreferrer"><em>Neurointervention</em></a>. Oxford Specialist Handbooks. Oxford University Press, 2026.</li>
        <li><strong>Neil M. Borden</strong>. <em>3D Angiographic Atlas of Neurovascular Anatomy and Pathology</em>. 2006.</li>
        <li><strong>Hiro Kiyosue</strong>, editor. <em>External Carotid Artery: Imaging Anatomy Atlas for Endovascular Treatment</em>. 2020.</li>
        <li><strong>Gianni Boris Bradač</strong>. <em>Applied Cerebral Angiography: Normal Anatomy and Vascular Pathology</em>. 2017.</li>
        <li><strong><a href="https://neuroangio.org/" target="_blank" rel="noopener noreferrer">Neuroangio.org</a></strong>, by Maksim Shapiro, MD: angiographic anatomy, arterial relationships, venous drainage and anatomical variants.</li>
        <li><strong>BodyParts3D</strong>, © The Database Center for Life Science: source geometry for bony anatomical context. CC BY-SA 2.1 Japan.</li><li><strong><a href="https://www.z-anatomy.com/" target="_blank" rel="noopener noreferrer">Z-Anatomy</a></strong>: brain, ventricles, falx and tentorium, registered to this atlas. Adapted surfaces: CC BY-SA 4.0, with original BodyParts3D credit retained. <a href={`${import.meta.env.BASE_URL}anatomy/licenses/Z_Anatomy_Source_Licence.txt`} target="_blank" rel="noopener noreferrer">Source licence and credits</a>.</li>
      </ul>
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
    </div>
    <button className="primary" onClick={onClose}>Close</button>
  </div></div>;
}
