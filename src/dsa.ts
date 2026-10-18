import territories from './dsa-territories.json';
import { presetVesselIds, type PresetId, type PresetSide } from './presets';
import type { AnatomyManifest } from './types';
import { downstreamFlow, pathPoint, type FlowData, type InjectionPoint } from './flowGeometry';

export const DSA_START = .5, DSA_END = 12;
export type DsaVessel = { id: string; delay: number; vein: boolean };
export type DsaBlush = { centre: number[]; radius: number[] };
export type DsaRun = { arteries: string[]; vessels: DsaVessel[]; blush: DsaBlush[]; flow?: FlowData; travel?: Map<string,{start:number;distance:number}>; inlets?: InjectionPoint[] };
const smooth = (x: number, a: number, b: number) => {
  const u = Math.max(0, Math.min(1, (x - a) / (b - a)));
  return u * u * (3 - 2 * u);
};
const pulse = (t: number, rise: number, end: number, fall: number) => smooth(t, 0, rise) * (1 - smooth(t, end, fall));
// A sustained inlet bolus. Transit delays shift BOTH edges, retaining the
// proximal column while distal branches fill. No branch-order dilution.
export function dsaConcentration(v: DsaVessel, time: number) {
  return v.vein ? .43 * pulse(time - v.delay, 1.1, 2.3, 4.4)
    : pulse(time - v.delay, .4, 3.2, 4.3);
}
export const dsaBlushConcentration = (time: number) => .075 * pulse(time - 3.1, 1.2, 2.1, 3.7);
export function dsaPhase(time: number) {
  return time === 0 ? 'Baseline' : time < 1.5 ? 'Arterial filling' : time <= 3 ? 'Full arterial'
    : time < 4 ? 'Late arterial / blush' : time < 5.5 ? 'Blush / early venous'
    : time < 7 ? 'Venous' : time < 9.5 ? 'Late venous' : 'Washout';
}

export function makeDsaRun(manifest: AnatomyManifest, preset: PresetId, side: PresetSide, flow?: FlowData, injection?: InjectionPoint | null): DsaRun {
  const byId = new Map(manifest.structures.map(s => [s.id, s]));
  const children = new Map<string, string[]>(), outgoing = new Map<string, string[]>();
  const append = (map: Map<string, string[]>, from: string, to: string) => map.set(from, [...(map.get(from) ?? []), to]);
  for (const s of manifest.structures) if (s.parent && s.system === 'artery') append(children, s.parent, s.id);
  for (const r of manifest.relationships) {
    if (r.type === 'branches_to' || r.type === 'has_segment') append(children, r.from, r.to);
    if (r.type === 'drains_to') append(outgoing, r.from, r.to);
  }
  // Explicit routes absent from the source graph. Do not traverse venous
  // communications as though every valveless connection were downstream.
  for (const s of ['left', 'right']) for (const [a, b] of [
    ['sphenoparietal', 'cavernous'], ['cavernous', 'inferior_petrosal'],
    ['inferior_petrosal', 'internal_jugular'], ['inferior_alveolar', 'pterygoid_plexus'],
    ['infraorbital', 'pterygoid_plexus'],
  ]) append(outgoing, `vein.${a}.${s}`, `vein.${b}.${s}`);

  let arteries = new Set(presetVesselIds(manifest, preset, side));
  if (preset === 'vertebrobasilar') {
    // A unilateral vertebral injection supplies both sides AFTER the basilar
    // confluence. The other vertebral/PICA tree is not injected automatically.
    const queue = ['artery.posterior.basilar'], seen = new Set<string>();
    for (let i = 0; i < queue.length; i++) {
      const id = queue[i]; if (seen.has(id)) continue; seen.add(id);
      const s = byId.get(id); if (s?.asset && s.system === 'artery' && s.displayGroup !== 'anastomoses') arteries.add(id);
      queue.push(...(children.get(id) ?? []));
    }
  }
  const baselineCount=arteries.size;
  let travel: DsaRun['travel'],inlets: InjectionPoint[]=[];
  if(flow) {
    if(injection && (!flow.entries[injection.id]?.selectable || !arteries.has(injection.id)))throw Error('This artery does not have a validated injection course');
    const incoming=new Set([...arteries].flatMap(id=>(flow.edges[id]??[]).map(e=>e.to)));
    const origins=injection?[injection]:[...arteries].filter(id=>!incoming.has(id)&&flow.entries[id]).map(id=>({id,distance:0,point:pathPoint(flow.entries[id],0)}));
    travel=downstreamFlow(flow,origins,arteries);arteries=new Set(travel.keys());
    inlets=injection?[injection]:origins.filter(p=>!/anterior_communicating|anterior_spinal$/.test(p.id));
  }
  const delay = new Map<string, number>();
  const depth = (id: string, seen = new Set<string>()): number => {
    if (delay.has(id)) return delay.get(id)!;
    if (seen.has(id)) return 0;
    seen.add(id); const s = byId.get(id);
    const order = ['cervical', 'petrous', 'cavernous', 'paraophthalmic', 'posterior-communicating', 'anterior-choroidal', 'terminus'];
    const segment = s?.segmentOf ? order.indexOf(id.split('.segment.')[1]) : -1;
    const vertebral = id.match(/\.segment\.v([1-4])$/);
    const upstream = manifest.relationships.find(r => r.type === 'branches_to' && r.to === id)?.from ?? s?.parent;
    const value = segment >= 0 ? .1 + segment * .085 : vertebral ? .08 + Number(vertebral[1]) * .12
      : upstream && byId.get(upstream)?.system === 'artery' ? depth(upstream, seen) + (s?.asset ? .14 : 0) : .12;
    delay.set(id, Math.min(1, value)); return delay.get(id)!;
  };
  const vessels: DsaVessel[] = [...arteries].map(id => ({ id, delay: travel ? Math.min(1,travel.get(id)!.distance/350) : depth(id), vein: false }));
  const territory = territories[preset];
  const sides = side === 'both' || preset === 'vertebrobasilar' ? ['left', 'right'] : [side];
  let blush = sides.flatMap(s => territory.blush.map(b => ({ centre: [s === 'left' ? .65 - b[0] : .65 + b[0], b[1], b[2]], radius: b.slice(3) })));
  if (preset === 'vertebrobasilar') blush.push({centre: [.65, -71, 57], radius: [15, 14, 22]});
  let seeds=sides.flatMap(s=>territory.veins.map(v=>`vein.${v}.${s}`));
  if ('midlineVeins' in territory) seeds.push(...territory.midlineVeins.map(v=>`vein.${v}`));
  if(injection && flow && arteries.size<baselineCount*.9) {
    // Territory fields are teaching approximations. Restrict them to distal
    // supplied courses, then seed ONLY declared regional drainage routes.
    const leaves=[...arteries].filter(id=>!(flow.edges[id]??[]).some(e=>arteries.has(e.to)));
    const points=leaves.flatMap(id=>{
      const row=flow.entries[id],start=Math.max(travel!.get(id)!.start,row.length*.6);
      return row.points.filter((_,i)=>row.arc[i]>=start);
    });
    const fields=blush.flatMap(field=>{
      const inside=points.filter(p=>p.reduce((sum,v,k)=>sum+((v-field.centre[k])/field.radius[k])**2,0)<2.25);
      if(!inside.length)return [];
      const lo=[0,1,2].map(k=>Math.min(...inside.map(p=>p[k]))),hi=[0,1,2].map(k=>Math.max(...inside.map(p=>p[k])));
      return [{centre:lo.map((v,k)=>(v+hi[k])/2),radius:lo.map((v,k)=>Math.min(field.radius[k],Math.max(5,(hi[k]-v)/2+5)))}];
    });
    if(!fields.length && points.length)fields.push({centre:points.at(-1)!,radius:[6,6,6]});
    blush=fields;
    const ancestry:string[]=[];let parent: string|null=injection.id;
    while(parent && !ancestry.includes(parent)){ancestry.push(parent);parent=byId.get(parent)?.parent??null;}
    if(ancestry.some(id=>/ophthalmic_/.test(id)))seeds=[`vein.superior_ophthalmic.${side}`,`vein.inferior_ophthalmic.${side}`];
    if(preset==='eca'||preset==='maxillary'||preset==='mma') {
      const has=(pattern:RegExp)=>[...arteries].some(id=>pattern.test(id));
      seeds=seeds.filter(id=>!(/middle_meningeal/.test(id)&&!has(/\.mma\.|mma_cavernous|mma_orbital/))
        &&!(/inferior_alveolar/.test(id)&&!has(/inferior_alveolar/))&&!(/infraorbital/.test(id)&&!has(/infraorbital/)));
      if(ancestry.some(id=>/\.lingual\./.test(id)))seeds=[`vein.lingual.${side}`,`vein.deep_facial.${side}`];
      // These are the two companions of the FRONTAL MMA route, not two
      // territories. Their reviewed receiver comes from drains_to metadata.
      if(/\.frontal\./.test(injection.id)&&ancestry.some(id=>/\.mma\./.test(id)))seeds=['anterior','posterior'].map(p=>`vein.middle_meningeal.${p}.${side}`);
      if(/posterior_convexity|petrosquamosal/.test(injection.id))seeds=[]; // No corresponding posterior-division venous course is modelled.
    }
    const score=(id:string)=>{const p=flow.veinSites[id];return p&&blush.length?Math.min(...blush.map(f=>p.reduce((sum,v,k)=>sum+((v-f.centre[k])/Math.max(10,f.radius[k]))**2,0))):Infinity;};
    const ranked=seeds.filter(id=>byId.get(id)?.asset).sort((a,b)=>score(a)-score(b));
    const local=ranked.filter(id=>score(id)<4);seeds=local.length?local:ranked.slice(0,1);
    // A representative site can fall outside the approximate blush field.
    // Retain the other member of a selected, already eligible companion pair.
    for(const id of [...seeds]) {
      const partner=id.replace(/middle_meningeal\.(anterior|posterior)/,(_,p)=>`middle_meningeal.${p==='anterior'?'posterior':'anterior'}`);
      if(partner!==id&&ranked.includes(partner)&&!seeds.includes(partner))seeds.push(partner);
    }
  }
  const queue=seeds.map(id=>({id,delay:4.5}));
  const veins = new Map<string, number>();
  for (let i = 0; i < queue.length; i++) {
    const {id, delay: arrival} = queue[i];
    if (!byId.has(id) || (veins.get(id) ?? Infinity) <= arrival) continue;
    const collecting = /superior_sagittal|straight|confluence|transverse|sigmoid|cavernous|petrosal\.|galen/.test(id);
    const next = Math.max(arrival, /jugular/.test(id) ? 7 : collecting ? 6 : 4.5);
    veins.set(id, next);
    for (const to of outgoing.get(id) ?? []) queue.push({ id: to, delay: next + .3 });
  }
  for (const [id, arrival] of veins) if (byId.get(id)?.asset) vessels.push({id, delay: Math.min(7.5, arrival), vein: true});
  return { arteries: [...arteries], vessels, blush,flow,travel,inlets };
}
