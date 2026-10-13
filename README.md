# Neurovascular Atlas v0.9.80

Installer-compatible source release with DSA vessel inspection and selectable injection points, the five anatomical bookmarks and one compressed model set.

Place inr-anatomy-atlas-v0.9.80.zip beside your existing inr-anatomy.sh, then run:

```bash
./inr-anatomy.sh update ./inr-anatomy-atlas-v0.9.80.zip
```

This imports the source release, rebuilds Docker locally, verifies v0.9.80 and publishes through your configured GitHub Pages workflow.

The models use meshopt compression, a shared 16-bit position grid and 12-bit octahedral normals. Original coordinates are retained around tiny faces wherever rounding would collapse or reverse them. Vertex and triangle order are preserved. No simplification or anatomical structures removed. Surface anchors, coordinates and asset hashes are refreshed. See docs/compression-validation.json for measured displacement and normal error.

Click the detector/vessel icon beside bookmarks to enter DSA mode without changing the view. Choose injection point asks for an artery through search or a click, then a point along its course. The complete arterial tree appears without veins. Change artery appears after vessel selection. Geometry preparation runs in the background and is cached. Bookmarks supply proximal injection defaults. Playback starts at the first opacified 0.5 s frame and loops at 2 frames/s until paused. Standard previous, play, pause and next icons control playback. Click or tap an opacified artery or vein to inspect it and pause the frame. The inspection pane keeps its ordinary position and open/closed state. Rotate to separate overlapping vessels. See docs/DSA_MODE.md for implementation and validation.

For a local source build, run npm ci and npm run build. For Docker, run ./docker.sh restart.

Jeremy Lynch, Sean McIlhone. See attribution and licence files.
