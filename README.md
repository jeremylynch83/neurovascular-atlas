## v0.9.161: MCA morphology

Both MCA trees are rebuilt as smooth, tapered illustrative tubes along the reviewed courses. All 70 MCA parts and eight MCA-related potential connection channels are retained. Small lenticulostriate diameters are reduced. ACA meshes are retained for a subsequent revision. Brain intersections are accepted in this approximate fit; the final vessel walls pass the conservative inner-skull envelope check.

Named parts meet through overlapping closed exteriors. This is a display and DSA reconstruction, not a Boolean-unioned lumen suitable for physics export without further processing. Potential links retain their existing classification. Physical joins, unchanged geometry, mesh containment and all 70 changed DSA courses are checked in docs/revision161-*. The production build passes.

Run the included installer as for earlier atlas releases. The ordinary build restores the complete circulation authoring GLB from the included packs and source fragments. Do not reapply tools/remesh-mca.py during ordinary builds; it is an offline authoring tool requiring the original v0.9.160 baseline alongside this release.

## v0.9.160: proximal maxillary artery and distal ECA correction

The proximal maxillary walls and the ECA/superficial temporal junction are
corrected on both sides. Native small branches, their attachment rings and the
distal maxillary course are retained. Six main arterial nodes change; 601 retain
their original decoded geometry. The existing loading packs and GitHub file-size
handling remain in place.

```sh
bash ./inr-anatomy.sh update ./inr-anatomy-atlas-v0.9.160.zip
```

The source comparison render and validation records are in `docs/revision160-*`.
The reconstruction is an educational wall fit, not a measured patient lumen.
Small residual seam contacts are recorded in the surface checks; this release
does not claim that every source arterial surface is free of self-contact.

## v0.9.159 GitHub file-size repair

Use the **v0.9.159 installer** included in this release. Replace any older copy
of `inr-anatomy.sh` kept beside your release ZIPs, then run:

```sh
bash ./inr-anatomy.sh update ./inr-anatomy-atlas-v0.9.159.zip
```

Retain your existing `INR_CHECKOUT` override if you use one. This imports the
release into your existing checkout, builds the local app and publishes it.
No Git LFS installation or force-push is needed.

The publisher checks staged blobs before committing. If earlier unpublished
commits contain the oversized circulation GLB, it first fetches remote main,
requires remote main to be an ancestor, and combines only the unpublished
changes into one commit containing the current staged tree. It atomically
retains the previous tip on a `backup/atlas-before-size-fix-*` branch. Published
history is retained. Diverged branches and unrelated oversized files stop with
an explanatory error. Backup branches are local and are not pushed by the
installer. Keep the backup until you have checked the published release.

The complete circulation source is now an ignored, reconstructed authoring
file. The existing lossless loading packs plus 16 MiB source fragments retain
every byte of the original source. Builds, `npm run dev`, `./anatomy.sh validate`
and `npm test` restore it automatically when missing. For direct geometry tools,
run `npm run anatomy:restore` first. Existing source edits are never overwritten
by restoration. After editing, the ordinary build refreshes packs and source
storage; `npm run anatomy:store` can also update storage explicitly. Commit the
packs, `anatomy/source-storage/` and updated manifests together. Do not force-add
the reconstructed GLB. Source editing and browser loading retain their existing
file names, geometry and behaviour.

# Neurovascular Atlas v0.9.158

This release removes the tented bilateral V4 course at the PICA origins, retaining the connected branches. The bookmark, mobile panel and progressive-loading improvements are retained. See [revision158](docs/revision158-v4-pica.md).

The retained anatomy corrects both optic canal roofs and opening transitions. The existing lesser-wing bone is reshaped locally into a longer roof and shorter floor, with a variable oval bore and smooth fitting of the adjacent ophthalmic arterial segments and nearby veins. No separate projecting collars are added.

The mandible, temporal repairs, ethmoid rollback and other anatomy from v0.9.145 are retained. Short vessel segments beside the new roofs are fitted locally; their flow projections and injection courses are updated. The optic nerves are not segmented. This is a reference-guided teaching reconstruction rather than patient CT anatomy. See docs/foramina-revision146.md for the measured geometry and scope.

## Install locally

Keep the ZIP intact beside the existing installer:

```bash
./inr-anatomy.sh local ./inr-anatomy-atlas-v0.9.158.zip
```

Open http://localhost:5173.

## Update the configured online website

```bash
./inr-anatomy.sh update ./inr-anatomy-atlas-v0.9.158.zip
```

This builds locally and publishes through the existing configured GitHub Pages workflow. Wait for the workflow to complete, then refresh the website without its old cache.

## Standalone build

Extract and run `./docker.sh restart`, or use Node 22 or later with `npm ci` and `npm run build`. Runtime anatomy is bundled. Optional authoring tools can require additional scientific Python packages.

The app retains its existing mobile interaction, loading, DSA and PICA features. Historical QA reports and comparison images are omitted from this app package. Source provenance and native source snapshots are retained for future corrections. Third-party anatomy terms remain in THIRD_PARTY_ANATOMY.md.

## Progressive loading (0.9.151)

The normal build automatically maintains lossless arterial download packs and a content-based gzip cache. Edit the complete source models as before, not generated packs. See [the loading/build notes](docs/revision151-progressive-loading.md) for ordering, validation, benchmarks and browser-test limits.

See [revision 152](docs/revision152-skull-first.md) for the revised initial loading order.

Revision 153 continues loading during touch/drag and camera damping. See [interaction pacing](docs/revision153-loading-interaction.md).

Revision 154 removes all timed loading pauses and interaction/slow-frame pacing. See [loading without timed pauses](docs/revision154-no-loading-pause.md). Earlier revision notes are historical.

Revision 155 uses the approved concise introduction in a dark app-style panel. Author background remains in About. Progress bar and measured percentage are retained. See docs/revision155-intro.md.
