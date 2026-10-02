# Anatomy data contract

Each structure has a stable `id`, display `name`, `parent`, `children`, `system`, explicit `side`, aliases, geometry status and provenance. Geometry is optional.

Example:

```json
{
  "id": "artery.eca.apa.hypoglossal.right",
  "name": "Hypoglossal branch",
  "parent": "artery.eca.apa.neuromeningeal_trunk.right",
  "system": "artery",
  "side": "right",
  "geometryStatus": "planned",
  "provenance": {
    "sourceType": "reference-defined",
    "confidence": "reference-only",
    "reviewStatus": "unreviewed",
    "sourceRefs": ["ref.kiyosue2020"]
  }
}
```

Geometry attaches through an asset reference:

```json
"asset": { "file": "models/skull-base.glb", "node": "foramen-spinosum-right" }
```

The logical catalogue is intentionally independent of GLB packaging. Multiple logical structures may later share a GLB file while remaining independently selectable.

## Relationship graph

`anatomy/relationships.json` stores relationships such as `passes_through`, `tributary` and `potential_anastomosis`. A potential anastomosis is not the same as a demonstrated connection in a reference subject.
