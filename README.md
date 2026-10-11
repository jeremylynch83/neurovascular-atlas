# Neurovascular Atlas v0.9.70

Installer-compatible source release. Contains one losslessly compressed model set, with unchanged decoded geometry and the five anatomical bookmarks.

Place inr-anatomy-atlas-v0.9.70.zip beside your existing inr-anatomy.sh, then run:

```bash
./inr-anatomy.sh update ./inr-anatomy-atlas-v0.9.70.zip
```

This imports the source release, rebuilds Docker locally, verifies v0.9.70 and publishes through your configured GitHub Pages workflow.

For a local source build, run npm ci and npm run build. For Docker, run ./docker.sh restart.

Jeremy Lynch, Sean McIlhone. See attribution and licence files.
