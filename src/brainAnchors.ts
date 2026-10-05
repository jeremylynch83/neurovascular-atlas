import { BufferGeometry, Vector3 } from 'three';
import type { AnatomyManifest, SurfaceAnchor } from './types';

/** Resolve a persisted anatomical anchor against the exact registered mesh.
 * Stale mesh bindings fail explicitly rather than silently moving a vessel.
 * This is a surface location, not a vessel lumen or a completed vessel route.
 */
export function resolveSurfaceAnchor(anchor: SurfaceAnchor, geometry: BufferGeometry, assetSha256: string): Vector3 {
  if (anchor.assetSha256 !== assetSha256) throw new Error('Brain anchor asset revision mismatch');
  const p = geometry.getAttribute('position'), ix = geometry.index;
  const offset = anchor.triangleIndex * 3;
  const w = anchor.barycentric;
  if (!Number.isInteger(anchor.triangleIndex) || offset < 0 || offset + 2 >= (ix?.count ?? p.count)
    || w.length !== 3 || w.some(x => !Number.isFinite(x) || x < -1e-6 || x > 1 + 1e-6)
    || Math.abs(w.reduce((a, b) => a + b, 0) - 1) > 1e-6) throw new Error('Invalid brain surface anchor');
  const point = new Vector3();
  for (let i = 0; i < 3; i++) point.addScaledVector(new Vector3().fromBufferAttribute(p, ix ? ix.getX(offset + i) : offset + i), w[i]);
  return point;
}

export function vesselCourseGuides(manifest: AnatomyManifest, vesselId: string) {
  return manifest.structures.filter(s => s.vesselGuide?.vesselIds.includes(vesselId));
}

export function vesselCourseSpecification(manifest: AnatomyManifest, vesselId: string) {
  const specification = manifest.structures.find(s => s.id === vesselId)?.vesselCourse;
  if (specification && (specification.registrationId !== manifest.brainRegistration?.id
    || specification.brainAssetSha256 !== manifest.brainRegistration?.registeredAssetSha256)) {
    throw new Error('Vessel course brain asset revision mismatch');
  }
  return specification;
}
