# Neurovascular Atlas v0.9.74

Installer-compatible source release with DSA vessel inspection and selectable injection points, the five anatomical bookmarks and one compressed model set.

Place inr-anatomy-atlas-v0.9.74.zip beside your existing inr-anatomy.sh, then run:

```bash
./inr-anatomy.sh update ./inr-anatomy-atlas-v0.9.74.zip
```

This imports the source release, rebuilds Docker locally, verifies v0.9.74 and publishes through your configured GitHub Pages workflow.

The models use meshopt compression, a shared 16-bit position grid and 12-bit octahedral normals. Original coordinates are retained around tiny faces wherever rounding would collapse or reverse them. Vertex and triangle order are preserved. No simplification or anatomical structures removed. Surface anchors, coordinates and asset hashes are refreshed. See docs/compression-validation.json for measured displacement and normal error.

Click the detector/vessel icon beside bookmarks to enter DSA mode. Use the phase slider or 2 frames/s playback, and bookmarks to choose the injection territory. Choose Injection point, select an artery with search or a click, then click along its course to place the tip. Play starts at the tip; Reset origin returns to the bookmark origin. Click or tap an opacified artery or vein to open its information and pause the frame. Rotate to separate overlapping vessels. See docs/DSA_MODE.md for implementation and validation.

For a local source build, run npm ci and npm run build. For Docker, run ./docker.sh restart.

Jeremy Lynch, Sean McIlhone. See attribution and licence files.
