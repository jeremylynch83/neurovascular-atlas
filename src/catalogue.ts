import type { AnatomyManifest, Structure } from './types';

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
