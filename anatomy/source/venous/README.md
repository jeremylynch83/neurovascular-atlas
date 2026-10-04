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
python3 tools/venous/build_veins.py --paths-only
python3 tools/venous/implicit_veins.py
node tools/compress-venous.mjs
python3 tools/import_veins.py
npm run build
```

Morphology amendments are in `tools/venous/morphology.py`. These define the
selected calibre profiles, sinus cross-sections and broad skull-constrained
courses. `fitted-paths.json` also records the bone-facing frame for each major
sinus; the implicit mesher preserves these profiles. Run the paths-only pass
before the final implicit mesher to avoid the unnecessary intermediate boolean
mesh. See `docs/VENOUS_v0.9.2.md` for the angiographic references and validation.

Intermediate reference meshes, exclusion surfaces and inspection output go into
`.authoring/venous`. The reference extraction can exceed 100 MB and the meshing
pass uses several GB of memory. It is deliberately excluded from the installer
and browser workflow. The paths-only pass retains fitted curves; the implicit pass creates the final
joined skin. It also stores the unfitted skin for surface inspection.

Only if changing the orbital course or skull should you run
`python3 tools/venous/orbital_route.py` before regenerating sparse courses.
`review_veins.py` and `check_contacts.py` are optional one-off authoring checks.
`audit_morphology.py` additionally requires Trimesh and checks the final mesh;
optional baseline snapshots add comparisons with the preceding release.
They are not proof of clinical accuracy; see `docs/VENOUS_v0.9.0.md` for limitations.

The existing artery and bone assets are read as fixed references and are never
rewritten by these commands. Reference images and the notes PDF are not included.
