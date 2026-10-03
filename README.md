# INR Anatomy Atlas v0.7.4

Place `inr-anatomy-atlas-v0.7.4.zip` beside the updated `inr-anatomy.sh`, then run `./inr-anatomy.sh`. It clones or updates `https://github.com/jeremylynch83/neurovascular-atlas.git` into `~/Documents/GitHub/neurovascular-atlas`, imports the app, starts it with Docker on port 5173, verifies the served release, commits and pushes to `main`, and configures GitHub Pages through Actions. GitHub CLI handles your login; on Linux Mint/Ubuntu the script installs it with apt if missing. Docker, Git, Python 3 and curl must already be installed. You need write access to the repository and permission to configure Pages.

The complete model is bundled; no historical CT data are downloaded or restored. The old `~/INR-Anatomy-Atlas` installation and anatomy data remain available. Review screenshots are excluded from this install ZIP.

Subsequent updates use the newest adjacent ZIP when it is newer than the checkout, or the latest `main` when there is no newer ZIP. The checkout must be clean; the script uses fast-forward pulls and never force-pushes. `./inr-anatomy.sh local` installs without publishing; `./inr-anatomy.sh publish` publishes a prepared checkout or retries a failed push/deployment. `restart`, `status`, `stop` and `logs` manage the local app. Override the checkout with `INR_CHECKOUT=/your/path`.

The Pages workflow builds with the repository subpath from `actions/configure-pages`, so model and application URLs work at `https://jeremylynch83.github.io/neurovascular-atlas/`. Local Docker builds continue to use `/`. GitHub Actions reports whether deployment succeeded; requesting deployment does not mean the site is live yet.

A release that fails to build is not pushed. If the served manifest has the wrong version, the installer restores the previous Docker image and does not publish. Files imported into the checkout remain available for inspection after a failed build.

## Panel changes in v0.7.4

Layers/Anatomy and structure details are stacked on the left. Click either title bar to collapse or expand it; the lower panel moves with the upper panel. The 3/4 and Face camera buttons are removed. Details and relationships show structure names without internal IDs, and the reconstruction/provenance/confidence/review fields are removed from the panel. Anatomy assets are unchanged from v0.7.3.

## Corrections in v0.7.3

M1 leaves the terminal ICA laterally with the folded junction corrected. Both A1 surfaces are preserved from v0.7.2. The ophthalmic origins are lower, the cavernous bends are more medial/posterior, and the inferior alveolar/mental routes now follow the mandibular body and visible mental-foramen regions. See `docs/REFINEMENT_v0.7.3.md`.

## ICA correction in v0.7.2

Both upper cervical/petrous entries now approach the carotid entry region anterior and lateral to the jugular fossa. The cavernous courses follow the parasellar corridor and ascend medial to the anterior clinoids. The prior overly medial entry and excessive lateral sweep are corrected. Under **Skull → ICA skull-base landmarks**, 33 entries identify the relevant bone surfaces, canal regions and estimated dural boundaries. Select a row to focus its marker; entries with a recorded course also show that course. The regular anatomy visibility controls and collapsed tree behaviour apply. See `docs/ICA_v0.7.2.md` for the method and remaining canal limitations.

## Included

- One combined anterior, posterior and bilateral ECA circulation.
- Revised infraorbital, meningeal, petrous ICA, ophthalmic, rotundum and ovale courses, with propagated branch attachments.
- 64 skull-opening types in a searchable, side-specific register under **Skull → Foramina and passages**. Selecting a located entry shows its regional marker and any saved course. Unresolved entries have no invented marker.
- Shared, smoothed vascular junctions and independently selectable vessel parts.
- Complete original skull context, both maxillae, mandible, condyles, alveolar processes and all 32 teeth.
- Potential ECA–ICA and ECA–vertebral connections on both sides, always enabled in gold with the artery layer.
- Simplified UI: removed the screenshot-identified banners, strapline, release subtitle, source list, About explanation, layer instructions, connection toggle and presets.
- Ghosted bone and teeth are click-through. Opaque bone remains selectable.

This is a reference-guided teaching reconstruction, not an individual patient segmentation. Vessel calibre, small canals, cervical vertebral and brain-surface relationships remain approximate. The left ECA uses the right template with independent bone fitting. It is not an independent angiographic reconstruction.

## Anatomy tree

Every row has a visibility checkbox. Unticking hides its geometry and all descendants, including collapsed branches. Ticking restores the subtree. A partial tick means some descendants are hidden. Detail-panel Show/Hide uses the same visibility state; global layer settings still apply. Landmark markers appear only while selected; their checkboxes enable or hide that selected marker. Unlocated entries have disabled checkboxes. The Anatomy tab starts fully collapsed each time it opens, independently of model visibility. Potential connections are nested under their recorded ECA source branches; their receiving arteries remain in the connection graph and detail panel.

## Download and serving

The release contains only three anatomy assets. Meshopt compression preserves the original floating-point positions, normals and index data exactly. There is no coordinate quantisation or triangle reduction. Model requests carry content hashes; nginx serves gzip and caches unchanged assets. The manifest is revalidated so a new release loads the new hashes.

## Development

`npm ci`, then `npm run dev`. `npm run build` validates the bundled catalogue and creates the production site. The normal installation needs Docker, not the Python modelling libraries. The modelling workflow and release-specific checks are in `docs/`. The one-off foraminal/compartment review is **not** part of `npm run build`, Docker, or the installer. Revisit it only after changing artery or bone geometry. See `docs/FORAMINA_v0.7.0.md` for the remaining canal limitations.
