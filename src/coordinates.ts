import type { AnatomyManifest } from './types';

export type AnatomicalView = 'front' | 'left' | 'right' | 'superior' | 'inferior' | 'three-quarter';
export type SectionAxis = 'sagittal' | 'coronal' | 'axial';
type Vector = [number, number, number];

export function coordinateSystem(manifest: AnatomyManifest) {
  // Existing TopBrain exports are also RAS, even before the explicit metadata
  // was introduced. Do not change or mirror the stored source geometry.
  return manifest.coordinateSystem ?? (manifest.structures.some(
    (s) => s.asset && s.provenance.sourceType === 'scan-derived',
  ) ? 'RAS' : 'legacy-y-up');
}

export function anatomicalView(system: 'RAS' | 'legacy-y-up', view: AnatomicalView): { direction: Vector; up: Vector } {
  if (system === 'RAS') {
    const directions: Record<AnatomicalView, Vector> = {
      front: [0, 1, 0], left: [-1, 0, 0], right: [1, 0, 0],
      superior: [0, 0, 1], inferior: [0, 0, -1], 'three-quarter': [0.75, 1, 0.18],
    };
    return { direction: directions[view], up: view === 'superior' || view === 'inferior' ? [0, 1, 0] : [0, 0, 1] };
  }
  const directions: Record<AnatomicalView, Vector> = {
    front: [0, 0, 1], left: [-1, 0, 0], right: [1, 0, 0],
    superior: [0, 1, 0], inferior: [0, -1, 0], 'three-quarter': [0.75, 0.18, 1],
  };
  return { direction: directions[view], up: view === 'superior' || view === 'inferior' ? [0, 0, 1] : [0, 1, 0] };
}

export function sectionNormal(system: 'RAS' | 'legacy-y-up', axis: SectionAxis): Vector {
  return axis === 'sagittal' ? [1, 0, 0] : (axis === 'coronal') === (system === 'RAS') ? [0, 1, 0] : [0, 0, 1];
}
