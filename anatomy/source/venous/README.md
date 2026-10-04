# Editable venous reconstruction

`courses.json` contains the authored control points, intended connections,
illustrative radius profiles, descriptions and source-page mapping.
`fitted-paths.json` preserves the final dense paths after fitting.
`orbital-corridors.json` records the independently fitted superior orbital fissure
routes. These are geometric authoring inputs, not patient imaging.

The normal app build consumes the bundled GLB and manifest. It does not run the
authoring pipeline, download source images, or require scientific Python tools.

To reproduce or edit the geometry, use a separate Python environment with
NumPy, SciPy, VTK 9.5 and Manifold3D. Run from the app root after `npm ci`:

```sh
node tools/decode-reference.mjs
python3 tools/venous/make_cavities.py
python3 tools/author_veins.py
python3 tools/venous/build_veins.py
python3 tools/venous/implicit_veins.py
node tools/compress-venous.mjs
python3 tools/import_veins.py
npm run build
```

Intermediate reference meshes, exclusion surfaces and inspection output go into
`.authoring/venous`. The reference extraction can exceed 100 MB and the meshing
pass uses several GB of memory. It is deliberately excluded from the installer
and browser workflow. The first mesh pass retains fitted paths and an intermediate
swept surface; the implicit pass replaces that surface with the final joined skin.

Only if changing the orbital course or skull should you run
`python3 tools/venous/orbital_route.py` before regenerating sparse courses.
`review_veins.py` and `check_contacts.py` are optional one-off authoring checks.
They are not proof of clinical accuracy; see `docs/VENOUS_v0.9.0.md` for limitations.

The existing artery and bone assets are read as fixed references and are never
rewritten by these commands. Reference images and the notes PDF are not included.
