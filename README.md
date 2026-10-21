# Neurovascular Atlas v0.9.153

This release loads and displays the skull first, then adds arteries progressively. Incremental pack generation and compression caching are retained. See [revision 151](docs/revision151-progressive-loading.md) for details and validation limits.

The retained anatomy corrects both optic canal roofs and opening transitions. The existing lesser-wing bone is reshaped locally into a longer roof and shorter floor, with a variable oval bore and smooth fitting of the adjacent ophthalmic arterial segments and nearby veins. No separate projecting collars are added.

The mandible, temporal repairs, ethmoid rollback and other anatomy from v0.9.145 are retained. Short vessel segments beside the new roofs are fitted locally; their flow projections and injection courses are updated. The optic nerves are not segmented. This is a reference-guided teaching reconstruction rather than patient CT anatomy. See docs/foramina-revision146.md for the measured geometry and scope.

## Install locally

Keep the ZIP intact beside the existing installer:

```bash
./inr-anatomy.sh local ./inr-anatomy-atlas-v0.9.153.zip
```

Open http://localhost:5173.

## Update the configured online website

```bash
./inr-anatomy.sh update ./inr-anatomy-atlas-v0.9.153.zip
```

This builds locally and publishes through the existing configured GitHub Pages workflow. Wait for the workflow to complete, then refresh the website without its old cache.

## Standalone build

Extract and run `./docker.sh restart`, or use Node 22 or later with `npm ci` and `npm run build`. Runtime anatomy is bundled. Optional authoring tools can require additional scientific Python packages.

The app retains its existing mobile interaction, loading, DSA and PICA features. Historical QA reports and comparison images are omitted from this app package. Source provenance and native source snapshots are retained for future corrections. Third-party anatomy terms remain in THIRD_PARTY_ANATOMY.md.

## Progressive loading (0.9.151)

The normal build automatically maintains lossless arterial download packs and a content-based gzip cache. Edit the complete source models as before, not generated packs. See [the loading/build notes](docs/revision151-progressive-loading.md) for ordering, validation, benchmarks and browser-test limits.

See [revision 152](docs/revision152-skull-first.md) for the revised initial loading order.

Revision 153 continues loading during touch/drag and camera damping. See [interaction pacing](docs/revision153-loading-interaction.md).
