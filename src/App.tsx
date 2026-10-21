import { useCallback, useEffect, useMemo, useRef, useState, type ReactNode } from 'react';
import type { AnatomyManifest, LayerState, Structure, SystemId } from './types';
import { geometrySubtrees, searchStructures, uniqueVesselCounts } from './catalogue';
import { AnatomyEngine } from './engine';
import { Description } from './Description';
import { Loading } from './Loading';
import { loadingAssets, structureDependencies, type LoadState } from './stagedLoading';
import { BookmarkIcon, PresetModal } from './PresetModal';
import { injectionPreset, presetDirection, presetVesselIds, presetVisibility, type PresetId, type PresetSide } from './presets';
import { DsaControls, DsaIcon, InjectionControls } from './DsaControls';
import { makeDsaRun, DSA_START, DSA_END, type DsaRun } from './dsa';
import type { InjectionPoint } from './flowGeometry';
import { explanationSectionsMarkup, explanationSummary } from './explanationMarkup';
import { reportStartupFailure, reportStartupProgress, reportStartupReady } from './startup';

const DEFAULT_VISIBILITY: Record<SystemId, LayerState> = { bone: 'ghost', artery: 'on', vein: 'off', brain: 'off' };
const NEXT: Record<LayerState, LayerState> = { on: 'ghost', ghost: 'off', off: 'on' };
const STATE_LABEL = { on: 'fully visible', ghost: 'translucent', off: 'absent' };

export function App({ manifest }: { manifest: AnatomyManifest }) {
  const app = useRef<HTMLDivElement>(null);
  const header = useRef<HTMLElement>(null);
  const stage = useRef<HTMLDivElement>(null);
  const engine = useRef<AnatomyEngine | null>(null);
  const fpsReadout = useRef<HTMLDivElement>(null);
  const [selectedId, setSelectedId] = useState<string | null>(null);
  const [query, setQuery] = useState('');
  const [searchOpen, setSearchOpen] = useState(false);
  const searchInput = useRef<HTMLInputElement>(null);
  const [visibility, setVisibility] = useState<Map<string, LayerState>>(() => new Map(manifest.structures
    .filter(s => s.asset || s.landmark?.point).map(s => [s.id, DEFAULT_VISIBILITY[s.system]])));
  const [controlsOpen, setControlsOpen] = useState(false);
  const [inspectionOpen, setInspectionOpen] = useState(false);
  const [focusedId, setFocusedId] = useState<string | null>(null);
  const [dark, setDark] = useState(true);
  const [ready, setReady] = useState(false);
  const [progress, setProgress] = useState(0);
  const [geometryProgress, setGeometryProgress] = useState({ ready: 0, total: 0, errors: 0 });
  const initialGeometry = useMemo(() => loadingAssets(manifest).filter(a => a.critical).flatMap(a => a.structures.map(s => s.id)), [manifest]);
  const [loadStates, setLoadStates] = useState<ReadonlyMap<string, LoadState>>(() => new Map());
  const [vascularReady, setVascularReady] = useState(false);
  const [pendingId, setPendingId] = useState<string | null>(null);
  const actionRevision = useRef(0);
  const controlsOpenRef = useRef(false);
  const [clip, setClip] = useState({ enabled: false, axis: 'sagittal' as 'sagittal'|'coronal'|'axial', offset: 0 });
  const [about, setAbout] = useState(false);
  const [presetsOpen, setPresetsOpen] = useState(false);
  const [presetSide, setPresetSide] = useState<PresetSide>('left');
  const [activePreset, setActivePreset] = useState<{id: PresetId; side: PresetSide}>({id: 'ica', side: 'left'});
  const [dsa, setDsa] = useState(false);
  const [dsaSelectedId,setDsaSelectedId]=useState<string|null>(null);
  const [dsaBusy, setDsaBusy] = useState(false);
  const [dsaError, setDsaError] = useState<string | null>(null);
  const [dsaTime, setDsaTime] = useState(DSA_START);
  const [playing, setPlaying] = useState(false);
  const [injection,setInjection]=useState<InjectionPoint|null>(null);
  const [injectionReady,setInjectionReady]=useState(false);
  const [placing,setPlacing]=useState(false);
  const [placementVessel,setPlacementVessel]=useState<string|null>(null);
  const runRef=useRef<DsaRun|null>(null);
  const injectionPending=useRef(false);
  const placementRevision=useRef(0);
  const closePresets = useCallback(() => setPresetsOpen(false), []);
  const toggleLayers = () => {
    controlsOpenRef.current = !controlsOpen;
    setControlsOpen(!controlsOpen);
    if (!controlsOpen) setLoadStates(new Map(engine.current?.getLoadStates()));
  };
  useEffect(() => {
    const element = header.current;
    if (!element) return;
    const measure = () => app.current?.style.setProperty('--mobile-panel-top', `${element.offsetTop + element.offsetHeight + 8}px`);
    const observer = new ResizeObserver(measure);
    observer.observe(element);
    measure();
    return () => observer.disconnect();
  }, []);
  const byId = useMemo(() => new Map(manifest.structures.map((s) => [s.id, s])), [manifest]);
  const subtrees = useMemo(() => geometrySubtrees(byId), [byId]);
  const selected = selectedId ? byId.get(selectedId) ?? null : null;
  const inspected=dsa?(dsaSelectedId?byId.get(dsaSelectedId)??null:null):selected;
  const selectedGeometry = selected ? subtrees.get(selected.id) ?? [] : [];
  const selectedHidden = selectedGeometry.length > 0 && selectedGeometry.every(id => visibility.get(id) === 'off');
  const canFocus = !!selected && !!(selected.asset || selected.landmark?.point || (selected.system === 'brain' && selectedGeometry.length) || manifest.structures.some(s => s.segmentOf === selected.id));
  const results = useMemo(() => searchStructures(manifest.structures, query).filter(s=>!placing||(s.system==='artery'&&s.asset&&(!engine.current?.getDsaFlow()||engine.current.getDsaFlow()!.entries[s.id]?.selectable))), [manifest.structures, query,placing,dsaBusy]);

  useEffect(() => {
    if (!stage.current) return;
    let cancelled = false;
    setReady(false); setProgress(0); setVascularReady(false); setPendingId(null);
    const e = new AnatomyEngine(stage.current, manifest, (id,isDsa) => { actionRevision.current++; setPendingId(null); if(isDsa){setDsaSelectedId(id);setPlaying(false);}else{setSelectedId(id);setFocusedId(null);} }, fps => {
      // Update this small readout without rerendering the anatomy panels.
      if (fpsReadout.current) {
        fpsReadout.current.textContent = fps === null ? '' : `${fps} FPS`;
        fpsReadout.current.hidden = fps === null;
      }
    }); engine.current = e; e.setTheme(dark);
    let notification: ReturnType<typeof setTimeout> | undefined;
    let failed = false;
    let disposed = false;
    const dispose = () => { if (!disposed) { disposed = true; e.dispose(); } };
    const fail = (error: unknown) => {
      if (cancelled || failed) return;
      failed = true;
      clearTimeout(notification);
      dispose(); engine.current = null;
      setReady(false);
      reportStartupFailure(error);
    };
    const publish = () => {
      if (cancelled || failed) return;
      // Only initial skull preparation contributes to this bar. Deferred
      // geometry keeps its existing inline feedback inside Layers.
      const states = e.getLoadStates();
      const percent = Math.min(99, initialGeometry.length ? 75 * e.initialDownloadProgress() + 24 * initialGeometry.filter(id => states.get(id)?.status === 'ready').length / initialGeometry.length : 0);
      setProgress(percent); reportStartupProgress(percent);
      setVascularReady(e.vascularGeometryReady());
      const all = [...states.values()];
      setGeometryProgress({ ready: all.filter(s => s.status === 'ready').length, total: all.length, errors: all.filter(s => s.status === 'error').length });
      if (controlsOpenRef.current) setLoadStates(new Map(e.getLoadStates()));
    };
    e.onInitialRender = () => {
      if (cancelled || failed) return;
      setReady(true); publish(); reportStartupReady();
    };
    e.onRenderError = fail;
    e.onInteraction = () => { actionRevision.current++; setPendingId(null); };
    e.load(() => {
      if (!notification) notification = setTimeout(() => { notification = undefined; publish(); }, 100);
    }).then(() => { if (cancelled || failed) return; e.start(); publish(); }).catch(fail);
    return () => { cancelled = true; actionRevision.current++; clearTimeout(notification); dispose(); engine.current = null; };
  }, [manifest, initialGeometry]);
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
    const timer = window.setInterval(() => { if (!document.hidden) setDsaTime(t => t>=DSA_END?DSA_START:t+.5); },500);
    return () => clearInterval(timer);
  }, [dsa, playing, placing,presetsOpen, about]);

  const clearDsaInspection=()=>{setDsaSelectedId(null);};
  const toggleDsa = async () => {
    clearDsaInspection();
    setDsaBusy(true); setDsaError(null); setPlaying(false);
    try {
      const e = engine.current;
      if (!e) return;
      if (dsa) { cancelPlacement();await e.setDsa(null);setDsa(false); }
      else if(!injectionReady){runRef.current=null;setDsa(true);startPlacement(null);}
      else {
        const flow=await e.prepareDsa();
        const run = makeDsaRun(manifest,activePreset.id,activePreset.side,flow,injection);
        await e.setDsa(run); setDsaTime(DSA_START); e.setDsaTime(DSA_START);
        runRef.current=run;setDsa(true);
      }
    } catch (error) { setDsaError(error instanceof Error ? error.message : String(error)); }
    finally { setDsaBusy(false); }
  };

  const cancelPlacement=()=>{placementRevision.current++;injectionPending.current=false;setDsaBusy(false);engine.current?.endInjectionPlacement();setPlacing(false);setQuery('');if(!runRef.current){void engine.current?.setDsa(null);setDsa(false);}};
  const startPlacement=(id:string|null)=>{placementRevision.current++;injectionPending.current=false;setPlaying(false);setQuery('');setDsaError(null);setPlacementVessel(id);setPlacing(true);engine.current?.beginInjectionPlacement(id,commitInjection);};
  const changeArtery=()=>{placementRevision.current++;injectionPending.current=false;setDsaBusy(false);setPlacementVessel(null);setDsaError(null);engine.current?.selectInjectionVessel(null);};
  const commitInjection=async (id:string,point:InjectionPoint|null)=>{
    const e=engine.current;if(!e)return;
    if(!point){
      const revision=++placementRevision.current;
      injectionPending.current=false;
      setPlacementVessel(id);setQuery('');setDsaError(null);e.selectInjectionVessel(id);setDsaBusy(true);
      try{
        const flow=await e.prepareInjection();if(revision!==placementRevision.current)return;
        if(!flow.entries[id]?.selectable)throw Error('No validated injection course for this artery. Choose another artery.');
      }catch(error){if(revision===placementRevision.current){e.selectInjectionVessel(null);setPlacementVessel(null);setDsaError(error instanceof Error?error.message:String(error));}}
      finally{if(revision===placementRevision.current)setDsaBusy(false)}
      return;
    }
    if(injectionPending.current)return;injectionPending.current=true;
    const revision=placementRevision.current;
    setDsaBusy(true);setDsaError(null);
    try{
      const flow=await e.prepareDsa();if(revision!==placementRevision.current)return;
      point=e.validateInjectionPoint(point);
      const preset=injectionPreset(id),side=byId.get(id)?.side==='right'?'right':'left';
      const run=makeDsaRun(manifest,preset,side,flow,point);
      if(!run.arteries.length)throw Error('No downstream vessels at this point');
      if(!await e.setDsa(run)||revision!==placementRevision.current)return;clearDsaInspection();runRef.current=run;setInjection(point);setInjectionReady(true);setActivePreset({id:preset,side});setPresetSide(side);
      setDsaTime(DSA_START);e.setDsaTime(DSA_START);cancelPlacement();
    }catch(error){if(revision===placementRevision.current)setDsaError(error instanceof Error?error.message:String(error));}
    finally{if(revision===placementRevision.current){injectionPending.current=false;setDsaBusy(false);}}
  };
  useEffect(()=>{
    if(!placing)return;const key=(e:KeyboardEvent)=>{if(e.key==='Escape')cancelPlacement();};
    window.addEventListener('keydown',key);return()=>window.removeEventListener('keydown',key);
  },[placing]);

  const cancelPending = () => { actionRevision.current++; setPendingId(null); };
  const withGeometry = async (id: string, ids: readonly string[], action: () => void) => {
    const e = engine.current; if (!e) return;
    const revision = ++actionRevision.current;
    const pending = ids.some(key => e.getLoadStates().get(key)?.status !== 'ready');
    setPendingId(pending ? id : null);
    if (pending) {
      // Feedback is confined to the anatomy panel, including requests from search.
      controlsOpenRef.current = true; setControlsOpen(true);
      setLoadStates(new Map(e.getLoadStates()));
    }
    try {
      await e.ensureGeometry(ids);
      if (revision !== actionRevision.current || e !== engine.current) return;
      setPendingId(null); action();
    } catch {
      if (revision === actionRevision.current) { setPendingId(null); setLoadStates(new Map(e.getLoadStates())); }
    }
  };
  const changeVisibility = (ids: string[], state: LayerState) => setVisibility(old => {
    const next = new Map(old);
    for (const id of ids) next.set(id, state);
    return next;
  });
  const changeClip = (next: typeof clip) => {
    cancelPending(); setFocusedId(null);
    setClip(next);
  };

  const select = (s: Structure) => {
    if(placing){void commitInjection(s.id,null);return;}
    if(dsa){setDsaSelectedId(s.id);setPlaying(false);return;}
    setSelectedId(s.id); setFocusedId(null); setQuery(''); setSearchOpen(false);
    if (s.system === 'vein' && s.asset) {
      const veins = manifest.structures.filter(row => row.system === 'vein' && row.asset).map(row => row.id);
      if (veins.every(id => visibility.get(id) === 'off')) changeVisibility(veins, 'on');
    }
    if (s.system === 'brain') {
      const ids = s.landmark ? [s.id, ...(s.vesselGuide?.surfaceStructureIds ?? [])] : subtrees.get(s.id) ?? [];
      changeVisibility(ids.filter(id => visibility.get(id) === 'off'), 'on');
    }
    void withGeometry(s.id, structureDependencies(s.id, byId, subtrees), () => {
      engine.current?.setSelected(s.id);
      if (engine.current?.hasGeometry(s.id) || s.landmark?.point) engine.current?.focus(s.id);
    });
  };

  const applyPreset = async (preset: PresetId) => {
    const ids = presetVesselIds(manifest, preset, presetSide);
    if (!ready || !ids.length) return;
    cancelPending();
    try { await engine.current?.ensureGeometry(ids); } catch { controlsOpenRef.current = true; setControlsOpen(true); setLoadStates(new Map(engine.current?.getLoadStates())); return; }
    if (dsa) {
      try {
        const flow=await engine.current!.prepareDsa(),run = makeDsaRun(manifest,preset,presetSide,flow);
        await engine.current?.setDsa(run); setPlaying(false); setDsaTime(DSA_START); engine.current?.setDsaTime(DSA_START);
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

  return <div className="atlas-app" ref={app} onClickCapture={e => {
    // Canvas selection clears focus through the engine callback. A browser
    // click emitted after dragging must not clear the focused structure.
    if (!dsa && focusedId && !(e.target as Element).closest('[data-focus-control], .clip-tools, .atlas-canvas, .presets-scrim')) setFocusedId(null);
  }}>
    <div className="atlas-stage" ref={stage} inert={presetsOpen || about} />
    <header className="app-header" ref={header}>
    <div className="identity">
      <h1><span>Neurovascular</span>{' '}<span>Atlas</span></h1>
    </div>
    <div className="top-actions">
      <div className="search-wrap" data-open={searchOpen}>
        <button className="mobile-search-toggle icon-btn" aria-label={searchOpen?'Close search':'Open search'} aria-expanded={searchOpen} aria-controls="anatomy-search-input" disabled={(dsa&&!placing) || dsaBusy} onClick={()=>{setSearchOpen(!searchOpen);if(!searchOpen){setControlsOpen(false);controlsOpenRef.current=false;requestAnimationFrame(()=>searchInput.current?.focus());}else setQuery('');}}><svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8" aria-hidden="true"><circle cx="10" cy="10" r="6"/><path d="m15 15 5 5"/></svg></button>
        <span className="search-icon">⌕</span>
        <input id="anatomy-search-input" ref={searchInput} disabled={(dsa&&!placing) || dsaBusy} value={query} onChange={(e)=>setQuery(e.target.value)} onKeyDown={e=>{if(e.key==='Escape'){setSearchOpen(false);setQuery('');}}} placeholder={placing?'Search an artery…':'Search anatomy or alternate name…'} aria-label="Search anatomy" />
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
    <button className="mobile-layers panel panel-title" hidden={dsa} aria-label="Layers" title="Layers" aria-expanded={controlsOpen} aria-controls="anatomy-panel-body" onClick={()=>{setSearchOpen(false);toggleLayers();}}><span className="layers-label">Layers</span><svg className="layers-icon" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.6" aria-hidden="true"><path d="m3 7 9-4 9 4-9 4-9-4Zm0 5 9 4 9-4M3 17l9 4 9-4"/></svg></button>
    </header>

    <div className="bottom-dock">
    <div className="panel-stack" hidden={dsa&&(!inspected||placing)}>
    <section className="left-panel panel" hidden={dsa}>
      <button className="panel-title" aria-expanded={controlsOpen} aria-controls="anatomy-panel-body" onClick={toggleLayers}>Layers</button>
      <div className="panel-body" id="anatomy-panel-body" hidden={!controlsOpen}>
      {ready && geometryProgress.ready < geometryProgress.total && <div className="geometry-progress" role="status">
        <span>{geometryProgress.errors ? 'Some anatomy could not load. Use Retry below.' : 'Loading remaining anatomy…'} {geometryProgress.ready}/{geometryProgress.total}</span>
        <progress aria-label="Anatomy prepared" value={geometryProgress.ready} max={geometryProgress.total} />
      </div>}
      <StructureTree manifest={manifest} byId={byId} subtrees={subtrees} visibility={visibility} selectedId={selectedId} loadStates={loadStates} pendingId={pendingId} onSelect={select} onRetry={id=>{void withGeometry(id, structureDependencies(id, byId, subtrees), () => {});}} onVisibility={(ids, state, id) => {
        changeVisibility(ids, state);
        if (state === 'off') cancelPending();
        else void withGeometry(id, structureDependencies(id, byId, subtrees), () => {});
      }} />
      </div>
    </section>

    {inspected && <Detail open={inspectionOpen} onOpenChange={setInspectionOpen} structure={inspected} manifest={manifest} byId={byId} onSelect={select} />}
    </div>

    <div className="camera-bar panel">
      {!dsa && <div className="selection-actions">
        <button data-focus-control aria-pressed={focusedId !== null} disabled={!ready || !canFocus} onClick={() => {
          if (!selected) return;
          if (focusedId === selected.id) { cancelPending(); setFocusedId(null); }
          else void withGeometry(selected.id, structureDependencies(selected.id, byId, subtrees), () => { setFocusedId(selected.id); engine.current?.focus(selected.id); });
        }}>Focus</button>
        <button disabled={!ready || !selectedGeometry.length} onClick={() => {
          changeVisibility(selectedGeometry, selectedHidden ? 'on' : 'off');
          if (!selectedHidden) cancelPending();
          else if (selected) void withGeometry(selected.id, structureDependencies(selected.id, byId, subtrees), () => {});
        }}>{selectedHidden ? 'Show' : 'Hide'}</button>
      </div>}
      <div className="views"><button onClick={()=>{cancelPending();engine.current?.setView('front')}}>AP</button><button onClick={()=>{cancelPending();engine.current?.setView('left')}}>L</button><button onClick={()=>{cancelPending();engine.current?.setView('right')}}>R</button><button onClick={()=>{cancelPending();engine.current?.setView('superior')}}>Sup</button><button onClick={()=>{cancelPending();engine.current?.setView('inferior')}}>Inf</button></div>
      <button className="bookmark-button" data-focus-control disabled={!ready} aria-label="Anatomical presets" aria-haspopup="dialog" aria-expanded={presetsOpen} onClick={() => setPresetsOpen(true)}><BookmarkIcon /></button>
      <button className="bookmark-button dsa-button" data-focus-control disabled={!ready || !vascularReady || dsaBusy} aria-label="DSA mode" title={dsaBusy ? 'Preparing DSA…' : !vascularReady ? 'Loading vascular anatomy for DSA…' : 'DSA mode'} aria-pressed={dsa} onClick={toggleDsa}><DsaIcon /></button>
      {!dsa && <div className="clip-tools"><label><input type="checkbox" checked={clip.enabled} onChange={(e)=>changeClip({...clip,enabled:e.target.checked})}/> Section</label><select value={clip.axis} onChange={(e)=>changeClip({...clip,axis:e.target.value as typeof clip.axis})}><option value="sagittal">Sagittal</option><option value="coronal">Coronal</option><option value="axial">Axial</option></select><input type="range" min="-1" max="1" step="0.01" value={clip.offset} onChange={(e)=>changeClip({...clip,offset:Number(e.target.value)})}/></div>}
    </div>
    {dsa && (placing?<InjectionControls name={placementVessel?byId.get(placementVessel)?.name??null:null} busy={dsaBusy} onChange={changeArtery} onCancel={cancelPlacement}/>:<DsaControls time={dsaTime} playing={playing} onTime={setDsaTime} onPlaying={setPlaying} onPlacement={()=>startPlacement(null)} busy={dsaBusy}/>)}
    {dsaError && <div className="dsa-error panel" role="alert">{dsaError}<button aria-label="Dismiss DSA error" onClick={()=>setDsaError(null)}>×</button></div>}
    </div>

    {!ready && <Loading progress={progress} />}
    <div className="fps-readout" ref={fpsReadout} aria-label="Frame rate" aria-live="off" hidden />
    {about && <About manifest={manifest} onClose={()=>setAbout(false)} />}
    {presetsOpen && <PresetModal side={presetSide} onSideChange={setPresetSide} onApply={applyPreset} onClose={closePresets} />}
  </div>;
}

function StructureTree({manifest,byId,subtrees,visibility,selectedId,loadStates,pendingId,onSelect,onRetry,onVisibility}:{manifest:AnatomyManifest;byId:Map<string,Structure>;subtrees:Map<string,string[]>;visibility:ReadonlyMap<string,LayerState>;selectedId:string|null;loadStates:ReadonlyMap<string,LoadState>;pendingId:string|null;onSelect:(s:Structure)=>void;onRetry:(id:string)=>void;onVisibility:(ids:string[],state:LayerState,id:string)=>void}) {
  const [open,setOpen]=useState<Set<string>>(() => new Set());
  useEffect(() => {
    if (!pendingId) return;
    setOpen(old => { const next = new Set(old); let id: string | null | undefined = byId.get(pendingId)?.parent;
      while (id) { next.add(id); id = byId.get(id)?.parent; } return next; });
  }, [pendingId, byId]);
  const toggle=(id:string)=>setOpen((old)=>{const n=new Set(old);n.has(id)?n.delete(id):n.add(id);return n});
  const node=(id:string,depth=0):ReactNode=>{const s=byId.get(id);if(!s)return null;const has=s.children.length>0;const ids=subtrees.get(id)??[];
    const states=new Set(ids.map(key=>visibility.get(key)??DEFAULT_VISIBILITY[s.system]));
    const state:LayerState|'mixed'=states.size>1?'mixed':states.values().next().value??'off';
    const deps = structureDependencies(id, byId, subtrees);
    const failed = deps.some(key => loadStates.get(key)?.status === 'error');
    const loading = deps.some(key => loadStates.get(key)?.status !== 'ready');
    const waiting = pendingId === id || (pendingId !== null && ids.includes(pendingId));
    const next=state==='mixed'?'on':NEXT[state];return <div key={id}>
    <div className={`tree-row ${selectedId===id?'selected':''} ${ids.length?'has-geometry':'planned'}`} data-structure-id={id} aria-busy={loading && !failed} style={{paddingLeft:`min(${8+depth*14}px, var(--tree-indent-limit, 100%))`}}>
      <button className="twisty" onClick={()=>has&&toggle(id)} aria-label={`${open.has(id)?'Collapse':'Expand'} ${s.name}`} aria-expanded={has?open.has(id):undefined}>{has?(open.has(id)?'⌄':'›'):''}</button>
      <button className="tree-name" onClick={()=>onSelect(s)}><span>{s.name}</span>{s.landmark&&<small>{s.landmark.point?'landmark':'unlocated'}</small>}</button>
      {failed ? <button className="structure-retry" aria-label={`Retry loading ${s.name}`} onClick={()=>onRetry(id)}>Retry</button>
        : loading && <span className="structure-loading" role="status" aria-label={`${s.name}: ${waiting?'Please wait':'loading'}`}><span className="structure-spinner" aria-hidden="true" />{waiting&&<small>Please wait…</small>}</span>}
      <button className={`tree-visibility state ${state}`} data-state={state} disabled={!ids.length} aria-label={`${s.name}: ${state==='mixed'?'mixed visibility':STATE_LABEL[state]}. Set ${STATE_LABEL[next]}`} aria-pressed={state==='mixed'?'mixed':state==='on'} onClick={()=>onVisibility(ids,next,id)}><span /></button>
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

export function About({manifest,onClose}:{manifest:AnatomyManifest;onClose:()=>void}) {
  const counts = uniqueVesselCounts(manifest.structures);
  return <div className="modal-scrim" onClick={onClose}><div className="about panel" role="dialog" aria-modal="true" aria-labelledby="about-title" onClick={(e)=>e.stopPropagation()}>
    <button className="detail-close" aria-label="Close information" onClick={onClose}>×</button>
    <h2 id="about-title">Neurovascular Atlas v{manifest.release}</h2>
    <p>{explanationSummary}</p>
    <p>{counts.artery} unique arteries and {counts.vein} unique veins, sinuses and venous plexuses.</p>
    <p>Jeremy Lynch, Sean McIlhone</p>
    <div className="about-credits" role="region" aria-label="Credits" tabIndex={0}>
      <div dangerouslySetInnerHTML={{__html:explanationSectionsMarkup(3)}} />
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
