import vesselLists from './presetVessels.json';
import type { AnatomyManifest, LayerState } from './types';

export type PresetId = keyof typeof vesselLists;
export type PresetSide = 'left' | 'right' | 'both';
export const ANATOMICAL_PRESETS: { id: PresetId; label: string }[] = [
  { id: 'ica', label: 'ICA' },
  { id: 'eca', label: 'ECA' },
  { id: 'vertebrobasilar', label: 'Vertebrobasilar' },
  { id: 'mma', label: 'MMA' },
  { id: 'maxillary', label: 'Maxillary artery' },
];

export function presetVesselIds(manifest: AnatomyManifest, preset: PresetId, side: PresetSide): string[] {
  const byId = new Map(manifest.structures.map(s => [s.id, s]));
  return vesselLists[preset].filter(id => {
    const s = byId.get(id);
    return s?.asset && s.system === 'artery' && s.displayGroup !== 'anastomoses'
      && (side === 'both' || s.side === side || s.side === 'midline');
  });
}

export function presetVisibility(manifest: AnatomyManifest, current: ReadonlyMap<string, LayerState>, ids: readonly string[]): Map<string, LayerState> {
  const next = new Map(current);
  const shown = new Set(ids);
  for (const s of manifest.structures) {
    if (s.system === 'artery' || s.system === 'vein') next.set(s.id, shown.has(s.id) ? 'on' : 'off');
  }
  return next;
}

export function presetDirection(preset: PresetId, side: PresetSide): [number, number, number] {
  if (preset === 'vertebrobasilar' || side === 'both') return [0, 1, 0.08];
  const lateral = side === 'left' ? -1 : 1;
  return preset === 'ica' ? [lateral, 0.65, 0.16]
    : preset === 'maxillary' ? [lateral, 0.35, -0.04] : [lateral, 0.18, 0.06];
}
