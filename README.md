# Neurovascular Atlas v0.9.143

This release restores the original ethmoid bone, retains the ethmoidal arteries, reconstructs the jagged temporal defects on both sides, and revises the optic, hypoglossal and facial canals. The artificial wide incisive opening is also reduced. See [the size audit, limitations and validation notes](docs/foramina-revision143.md) and [bilateral temporal comparisons](docs/temporal-bilateral-revision143.png). Earlier issue registers remain historical records, not acceptance certificates for this release.

Earlier repairs retained in this package:

App-only installation package. This release corrects inward shading normals on the mandibular alveolar surface, removing the dark, jagged lower-jaw patch while preserving its geometry and all vessels. The initial progress bar follows downloaded bytes and mesh preparation, with smooth interpolation and a slow estimated advance during gaps. Completion remains tied to initial readiness. Reduced-motion preferences are respected. The starting view is AP, centred and magnified around the skull rather than the full neck vessel extent. This release corrects both medial tentorial arteries around the cavernous ICA and along the registered tentorium, retaining their native MHT and neighbouring branch attachment coordinates. Their names, descriptions and DSA courses are updated; other anatomy is preserved.

On mobile, tapping a model leaves the camera still. The exact point tapped becomes the intended rotation pivot. The next rotation drag gently centres that point over about 400 ms of active dragging, without changing orbit distance. Short drags pause and resume the centring. Deliberate panning cancels further centring until a different structure is selected; a pure pinch zoom does not cancel it. Search and Layers retain their existing auto-focus.

Place the ZIP beside your existing inr-anatomy.sh and run:

```bash
./inr-anatomy.sh local ./inr-anatomy-atlas-v0.9.143.zip
```

Open http://localhost:5173. Use `update` instead of `local` to also publish through your configured GitHub Pages workflow. Do not extract the ZIP before using the installer.

For a standalone Docker installation, extract the archive and run `./docker.sh restart` inside its folder. For a source build with Node 22 or later, run `npm ci`, then `npm run build`. This package includes the runtime assets and files needed by those builds. Current validation reports and authoring tools are included; historical working files are excluded.

### PICA anatomy update

Bilateral PICA courses now show caudal and cranial tonsillar loops, with selectable p1–p5 segments, revised branches, descriptions, landmarks and DSA courses. Small local cerebellar fissure refinements provide clearance. Inferior olive and lower cranial nerve boundary positions are estimated because those fine structures are not segmented in this atlas.


Sphenoid foramina batch 1: bilateral rotundum, ovale and spinosum openings, markers and local vessel paths are updated. Repair notes and regional validation: `docs/foramina-batch1.md`. Batch 1 is retained; all eight planned audit batches are complete, with open findings recorded.
