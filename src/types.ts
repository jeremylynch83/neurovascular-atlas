export type SystemId = 'bone' | 'artery' | 'vein' | 'brain';
export type Side = 'left' | 'right' | 'midline';
export type GeometryStatus = 'planned' | 'placeholder' | 'master' | 'web-optimised';
export type LayerState = 'on' | 'ghost' | 'off';

export interface AssetRef { file: string; node: string }
export interface SurfaceAnchor {
  structureId: string;
  triangleIndex: number;
  barycentric: [number, number, number];
  position: [number, number, number];
  assetSha256: string;
  registrationId: string;
}
export interface BrainRegistration {
  id: string;
  coordinateSystem: 'RAS';
  units: 'mm';
  matrixFromSourceOrientation: number[][];
  sourceAssetSha256: string;
  registeredAssetSha256: string;
  method: string;
  status: string;
  limitations: string;
}
export type VesselCourseMode = 'dural-attachment' | 'dural-free-edge' | 'bony-groove' | 'cisternal' | 'pial' | 'opercular' | 'insular' | 'sulcal' | 'surface-vein' | 'bridging' | 'deep-venous' | 'subependymal' | 'penetrating' | 'choroidal';
export interface VesselCourse {
  vesselId: string;
  side: Side;
  scope: 'intracranial' | 'intracranial-and-upper-cervical' | 'protected-baseline' | 'potential-anastomosis' | 'reference-corridor';
  geometry: AssetRef;
  geometrySha256: string;
  registrationId: string;
  brainAssetSha256: string;
  summary: string;
  targetStructureIds: string[];
  stationIds: string[];
  stationOrder: 'anatomical-sequence' | 'regional-references-only' | 'not-applicable';
  radiusPolicy: 'preserve-delivered-profile' | 'preserve-source-profile-with-measured-wall-deformation';
  reviewStatus: 'requires-anatomical-review' | 'requires-anatomical-target' | 'protected-baseline';
  missingTargets: string[];
  attachments: { parentId: string | null; incoming: Relationship[]; outgoing: Relationship[]; status: string };
  coursePaths?: { source: string; sourceStructureId: string; sourcePart: number; pointCount: number; pointSha256: string; lengthMm: number }[];
  segments: { pathIndex?: number; pointRange?: [number, number]; arcRangeMm?: [number, number]; summary?: string; order: number; mode: VesselCourseMode; targetStructureIds: string[]; stationIds: string[]; stationRole: string;
    constraints: { wallClearance: 'radius-aware'; allowTissueEntry: boolean; avoidAtlasCutFaces: boolean; preserveJoinedAttachments: boolean }; reviewStatus: string }[];
}
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
  anatomy?: { category: string; sourceLabel: string; registrationId: string; bounds: number[][]; centroid: [number, number, number]; surfaceRole?: 'sulcal-reference' | 'csf-boundary' | 'dural-surface' | 'parenchymal-surface' };
  surfaceAnchor?: SurfaceAnchor;
  secondarySurfaceAnchors?: SurfaceAnchor[];
  vesselCourse?: VesselCourse;
  anatomicalReview?: { status: string; issueIds: string[]; summary: string };
  vesselGuide?: { role: 'course-guide'; vesselNames: string[]; vesselIds: string[]; surfaceStructureIds: string[]; anchorIds?: string[] };
  landmark?: {
    kind?: 'brain-surface' | 'brain-course';
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
  brainRegistration?: BrainRegistration;
  vesselCourseSchemaVersion?: string;
  vesselCourseState?: 'specified-not-fitted' | 'partially-fitted-awaiting-review';
  brainAdjustmentPolicy?: { scope: string; preserve: string[]; afterAdjustment: string[]; bounds: string; appliedAdjustments: unknown[] };
  structures: Structure[];
  relationships: Relationship[];
  sources: SourceRef[];
  roots: string[];
  warning: string;
}
