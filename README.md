# Neurovascular Atlas v0.9.127

App-only installation package. The initial progress bar animates smoothly between real loading updates. Reduced-motion preferences are respected. All anatomy and DSA data are unchanged from v0.9.126.

Place the ZIP beside your existing inr-anatomy.sh and run:

```bash
./inr-anatomy.sh local ./inr-anatomy-atlas-v0.9.127.zip
```

Open http://localhost:5173. Use `update` instead of `local` to also publish through your configured GitHub Pages workflow. Do not extract the ZIP before using the installer.

For a standalone Docker installation, extract the archive and run `./docker.sh restart` inside its folder. For a source build with Node 22 or later, run `npm ci`, then `npm run build`. This package includes the runtime assets and files needed by those builds. Historical repair inputs, audit reports, tests and development tools are excluded.
