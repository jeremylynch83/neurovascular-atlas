// Canonical authoring input for geometry-bound injection course guides.
export function authoredCourseSource(manifest) {
 const guides=manifest.structures.filter(s=>s.flowCourseGuide).map(s=>[s.id,{geometrySha256:s.flowCourseGuide.geometrySha256,points:s.flowCourseGuide.points}]).sort(([a],[b])=>a<b?-1:a>b?1:0);
 return guides.length?JSON.stringify(guides):'';
}
