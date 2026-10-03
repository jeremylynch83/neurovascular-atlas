export type SystemId = 'bone' | 'artery' | 'vein' | 'brain';
export type Side = 'left' | 'right' | 'midline';
export type GeometryStatus = 'planned' | 'placeholder' | 'master' | 'web-optimised';
export type LayerState = 'on' | 'ghost' | 'off';

export interface AssetRef { file: string; node: string }
export interface Provenance {
  sourceType: 'scan-derived' | 'atlas-derived' | 'teaching-reconstruction' | 'reference-defined' | 'legacy-placeholder';
  confidence: string;
  reviewStatus: 'unreviewed' | 'reviewed' | 'revision-required' | 'approved';
  sourceRefs: string[];
}
export interface Structure {
  id: string;
  name: string;
  parent: string | null;
  children: string[];
  system: SystemId;
  side: Side;
  kind: 'structure' | 'group';
  aliases: string[];
  geometryStatus: GeometryStatus;
  provenance: Provenance;
  asset?: AssetRef;
  segmentOf?: string;
  description?: string;
  notes?: string;
  color?: string;
  displayGroup?: 'anastomoses';
  landmark?: {
    status: 'visible' | 'partial' | 'regional' | 'unresolved' | 'variant-unresolved' | 'bone-unavailable';
    point: [number, number, number] | null;
    course: [number, number, number][];
    connects: string;
    contents: string;
  };
}
export interface Relationship { from: string; to: string; type: string; note?: string }
export interface SourceRef { id: string; title: string; year?: number; role: string; licence?: string; redistribution?: string; notes?: string }
export interface AnatomyManifest {
  schemaVersion: string;
  release: string;
  title?: string;
  description?: string;
  units: string;
  coordinateSystem?: 'RAS' | 'legacy-y-up';
  assetRevisions?: Record<string, string>;
  assetByteSizes?: Record<string, number>;
  reference?: { case: string; pipelineVersion: string };
  structures: Structure[];
  relationships: Relationship[];
  sources: SourceRef[];
  roots: string[];
  warning: string;
}
