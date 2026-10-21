import type { AnatomyManifest } from './types';

// The full manifest remains the authoring/validation record. This projection
// keeps the fields consumed by the viewer, including every description,
// relationship, search alias, surface anchor and geometry dependency.
const manifestFields = [
  'schemaVersion', 'release', 'title', 'description', 'units', 'coordinateSystem',
  'assetRevisions', 'assetByteSizes', 'brainRegistration', 'relationships',
  'sources', 'roots', 'warning', 'loadingPacks', 'startupBounds',
] as const;
const structureFields = [
  'id', 'name', 'parent', 'children', 'system', 'side', 'kind', 'aliases',
  'geometryStatus', 'provenance', 'asset', 'segmentOf', 'description', 'color',
  'displayGroup', 'surfaceAnchor', 'vesselGuide', 'landmark',
] as const;

export function createViewerCatalogue(full: AnatomyManifest): AnatomyManifest {
  const result: Record<string, unknown> = Object.fromEntries(manifestFields.filter(key => key in full).map(key => [key, full[key]]));
  result.structures = full.structures.map(row => Object.fromEntries(
    structureFields.filter(key => key in row).map(key => [key, row[key]]),
  ));
  return result as unknown as AnatomyManifest;
}
