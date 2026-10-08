import type { AnatomyManifest, Structure } from './types';

// Count modelled vessels, folding segment meshes into their whole vessel and
// pairing bilateral names. Potential connection overlays are not vessels.
export function uniqueVesselCounts(structures: Structure[]): { artery: number; vein: number } {
  const byId = new Map(structures.map(s => [s.id, s]));
  const names = { artery: new Set<string>(), vein: new Set<string>() };
  for (let vessel of structures) {
    if ((vessel.system !== 'artery' && vessel.system !== 'vein') || !vessel.asset || vessel.displayGroup === 'anastomoses') continue;
    const system = vessel.system;
    const visited = new Set<string>();
    while (vessel.segmentOf && !visited.has(vessel.id)) {
      visited.add(vessel.id);
      const owner = byId.get(vessel.segmentOf);
      if (!owner) break;
      vessel = owner;
    }
    const name = vessel.name.replace(/\b(left|right|midline)\b/gi, '').replace(/[\s,]+/g, ' ').trim().toLowerCase();
    names[system].add(name);
  }
  return { artery: names.artery.size, vein: names.vein.size };
}

// Segment ownership can nest: whole ACA -> pericallosal -> A2-A5.
// Ordinary arterial branches are not members of the parent vessel's surface.
export function segmentGeometryMembers(structures: Structure[]): Map<string, Set<string>> {
  const byId = new Map(structures.map(s => [s.id, s]));
  const members = new Map<string, Set<string>>();
  for (const structure of structures) {
    if (!structure.asset) continue;
    let cursor: Structure | undefined = structure;
    const visited = new Set<string>();
    while (cursor && !visited.has(cursor.id)) {
      visited.add(cursor.id);
      if (!members.has(cursor.id)) members.set(cursor.id, new Set());
      members.get(cursor.id)!.add(structure.id);
      // Brain parcels are parts of their containing anatomy, so a hemisphere
      // or brainstem group can be focused/highlighted without duplicate meshes.
      const owner: string | null = cursor.segmentOf ?? (cursor.system === 'brain' ? cursor.parent : null);
      cursor = owner ? byId.get(owner) : undefined;
    }
  }
  return members;
}

export function geometrySubtrees(byId: ReadonlyMap<string, Structure>): Map<string, string[]> {
  const subtrees = new Map<string, string[]>();
  const collect = (id: string): string[] => {
    const cached = subtrees.get(id);
    if (cached) return cached;
    const s = byId.get(id);
    const ids = s ? [...(s.asset || s.landmark?.point ? [id] : []), ...s.children.flatMap(collect)] : [];
    subtrees.set(id, ids);
    return ids;
  };
  for (const id of byId.keys()) collect(id);
  return subtrees;
}

// Keep a vessel's own segments and its immediate named branches/tributaries
// clear, without following the entire downstream tree or potential connections.
export function focusGeometryMembers(manifest: AnatomyManifest, id: string): Set<string> {
  const guide = manifest.structures.find(s => s.id === id)?.vesselGuide;
  if (guide) return new Set(guide.surfaceStructureIds);
  const members = segmentGeometryMembers(manifest.structures);
  const own = members.get(id) ?? new Set<string>();
  const origins = new Set([id, ...own]);
  const targets = new Set(origins);
  for (const s of manifest.structures) {
    if (s.parent && origins.has(s.parent) && s.kind !== 'group' && s.displayGroup !== 'anastomoses') targets.add(s.id);
  }
  for (const r of manifest.relationships) {
    if (r.type === 'branches_to' && origins.has(r.from)) targets.add(r.to);
    if (r.type === 'drains_to' && origins.has(r.to)) targets.add(r.from);
  }
  return new Set([...targets].flatMap(target => [...(members.get(target) ?? [])]));
}

export async function loadCatalogue(file = 'manifest.json'): Promise<AnatomyManifest> {
  const response = await fetch(`${import.meta.env.BASE_URL}anatomy/${file}`, { cache: 'no-store' });
  if (!response.ok) throw new Error(`Could not load anatomy manifest (${response.status})`);
  return response.json() as Promise<AnatomyManifest>;
}

export function searchStructures(structures: Structure[], query: string): Structure[] {
  const q = query.trim().toLowerCase();
  if (!q) return [];
  const tokens = q.split(/\s+/).filter(Boolean);
  return structures
    .map((s) => {
      const name = s.name.toLowerCase();
      const id = s.id.toLowerCase();
      const aliases = s.aliases.join(' ').toLowerCase();
      const hay = `${name} ${id} ${aliases}`;
      if (!tokens.every((t) => hay.includes(t))) return null;
      let score = 10;
      if (name === q) score = 0;
      else if (name.startsWith(q)) score = 1;
      else if (name.includes(q)) score = 2;
      else if (id.includes(q)) score = 4;
      if (s.asset) score -= 0.25;
      return { s, score };
    })
    .filter((x): x is { s: Structure; score: number } => x !== null)
    .sort((a, b) => a.score - b.score || a.s.name.localeCompare(b.s.name))
    .slice(0, 40)
    .map((x) => x.s);
}
