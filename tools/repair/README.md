# Native repair pipeline

This is an offline authoring tool. It caches source geometry, finds bounded native wall gaps, aligns explicitly paired rims, stages candidates and records local validation. It never writes production models or closes an anatomical issue automatically.

Install the app's Node dependencies with `npm ci`. The tool needs Python 3, NumPy and SciPy. VTK is needed only for the historical comparison in benchmark.py. No new browser or ordinary application dependency is introduced.

## Commands

Prepare the geometry cache:

```bash
npm run repair:prepare
```

Scan the current tentorial network:

```bash
npm run repair:scan -- --config tools/repair/configs/tentorial-current.json
```

Replay the pre-v0.9.92 gaps, stage candidates and validate them:

```bash
npm run repair:run -- --config tools/repair/configs/tentorial-v0.9.92-replay.json --output /tmp/atlas-repair-review
```

Use `--cache-dir /absolute/path` to keep authoring caches outside the checkout. The default is `.repair-cache`. Missing caches rebuild automatically. Repeating a recorded rejection reuses its report. `--retry` explicitly repeats a recorded trial and all local checks. Cached accepted files are hashed before reuse and copied to the requested staging folder. Different source geometry, bindings, configuration or tool code creates a new trial signature.

Run regressions and a reproducible benchmark:

```bash
npm run repair:test
npm run repair:benchmark -- --work /tmp/atlas-new-benchmark --repeats 3
```

The benchmark directory must be new. It compares source preparation, patching, local checks and staging against the prior authoring scripts. It verifies the exact seven-triangle repair surface, includes an empty authoring cache run and repeats the complete new checks on warm runs. It excludes export, DSA preparation, release builds, human review and archive transfers. It does not predict the time for regional anatomical reconstruction.

## Configuration

Each `networks` entry has an `id`, a `target` label receiving wall triangles, and explicit neighbouring `nodes`. Detection uses their combined exact native boundaries. Small mixed-label gaps are eligible; a single-label opening is retained as a possible intentional port. Large or ambiguous components remain for regional review. No particular coordinate, side or vessel name is built into the detector.

For bounded alignment, add an explicit pairing:

```json
{
  "schema": 1,
  "seams": [{"target": "Child label", "parent": "Parent label"}]
}
```

Seam fitting requires complete compatible rims, preserves all other native boundaries and exact attachments to other labels, and limits displacement to 0.05 mm by default. Wider offsets are rejected for regional work. `limits` can override the documented defaults in repair.py. Changing limits creates a distinct trial. `baselineOverrides` is for explicit authoring/replay fixtures with required file hashes. It does not change production geometry.

## Validation and outputs

The cache hashes each source asset on every invocation, rather than trusting timestamps. Immutable decoded buffers and triangle BVHs are addressed by the decoded position/index bytes. Updating one label retains spatial indexes for unchanged labels, even when they share a GLB. Spatial indexes use numeric arrays, not executable pickle data. The decode cache schema must be bumped when decoding semantics change.

Every changed face is checked against the whole scene using cached AABB/BVH queries. Tests include adjacent triangles, positive coplanar overlaps, degeneracy, reversed source faces and combined native edge incidence. Closed, consistently oriented target surfaces use ray parity samples. Open or non-manifold bone/brain targets use an empty-ball clearance bound around unchanged source anchors; edits too close to such targets require regional review. The tool records this limitation and does not treat open-mesh ray parity as proof of volume membership.

`report.json` contains source identities, classifications, validation, cache statistics and timings. `accepted-corrections.json` lists only candidates that pass the local numerical gates. Position and index buffers are written beneath `candidate/` or `rejected/`. The cache's `trials/journal.jsonl` records accepted and rejected trial signatures and reasons. A local numerical pass is not whole-region anatomical acceptance.

These buffers are authoring inputs. Patch metadata records the source of appended native coordinates/normals. Seam fitting stages positions/indices and requires the usual affected-normal refresh at export. The existing release export and DSA integration remain a later batch step. In particular, the replay uses pre-v0.9.92 child buffers and must never be installed over the current model as an additional repair.

The shipped v0.9.93 production geometry and DSA data remain byte-exact to v0.9.92. Six recorded attachment failures and the regional anatomical issues remain open.

## Nearly parallel intersections, v0.9.101

When the sine of the angle between the face normals is below 1e-6, triangle crossing checks use exact rational arithmetic on the supplied binary coordinates. Plane-side signs, line intervals and coplanar positive-area clipping are evaluated without tolerance expansion. This avoids turning a shared vertex into a false crossing interval. All other pairs retain the existing fast path. The default spatial tolerance is unchanged. Genuine shallow crossings and arbitrarily thin positive coplanar overlaps remain rejected; point/shared-edge contacts are allowed.

The actual right A5 false-positive fixture, winding/symmetry, dyadic transform, parallel separation and genuine near-parallel crossings are covered by regression tests. The authoring trial signature already hashes geometry.py, so previously cached decisions are invalidated automatically. There is no browser/runtime dependency or performance change. See docs/INTERSECTION_BATCH9_v0.9.101.md.
