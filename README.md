# Neurovascular Atlas v0.9.71

Installer-compatible source release with the five anatomical bookmarks and one compressed model set.

Place inr-anatomy-atlas-v0.9.71.zip beside your existing inr-anatomy.sh, then run:

```bash
./inr-anatomy.sh update ./inr-anatomy-atlas-v0.9.71.zip
```

This imports the source release, rebuilds Docker locally, verifies v0.9.71 and publishes through your configured GitHub Pages workflow.

The models use meshopt compression, a shared 16-bit position grid and 12-bit octahedral normals. Original coordinates are retained around tiny faces wherever rounding would collapse or reverse them. Vertex and triangle order are preserved. No simplification or anatomical structures removed. Surface anchors, coordinates and asset hashes are refreshed. See docs/compression-validation.json for measured displacement and normal error.

For a local source build, run npm ci and npm run build. For Docker, run ./docker.sh restart.

Jeremy Lynch, Sean McIlhone. See attribution and licence files.
