# INR Anatomy Atlas

Interactive 3D anatomy atlas foundation for interventional neuroradiology.

**Release:** v0.2 Vascular Seed.

v0.2 adds the first visible vascular geometry while preserving the provenance rules established in v0.1. The current skull is temporary legacy BodyParts3D context. Selected ECA and extracranial venous structures are atlas-derived from Z-Anatomy and are **not** CTA-derived or accepted as final INR master anatomy.

## Run

```bash
./docker.sh
```

The script builds and starts the application in the background and prints both local and Tailscale URLs when available.

Stop it with:

```bash
./docker.sh stop
```

## v0.2 visible geometry

- legacy skull/skull-base context
- bilateral external carotid arteries
- bilateral facial arteries
- bilateral maxillary arteries
- bilateral inferior alveolar arteries
- bilateral posterior superior alveolar arteries
- bilateral descending palatine arteries
- bilateral buccal arteries
- bilateral internal jugular veins
- bilateral retromandibular veins
- bilateral maxillary veins
- bilateral facial veins

The old Dental Scope schematic pterygoid plexus and inferior alveolar vein are intentionally not imported.

## Anatomy catalogue

The complete logical catalogue is substantially larger than the currently visible geometry. It already defines the planned skull-base landmarks, detailed ECA/APA system, intracranial arteries, dural sinuses, superficial/deep veins and brain context using stable IDs. Search therefore finds both available and planned structures.

## Provenance

Geometry is explicitly classified. Current values include:

- `legacy-placeholder`: temporary inherited context
- `atlas-derived`: geometry derived from an anatomical atlas, not source imaging
- `scan-derived`: reserved for future geometry extracted from source imaging
- `teaching-reconstruction`: explicit reconstruction when source resolution is insufficient

See `docs/V0.2.md`, `docs/ANATOMY_DATA_CONTRACT.md`, `THIRD_PARTY_ANATOMY.md` and `ATTRIBUTIONS.md`.

## Build validation

```bash
./build-anatomy.sh
```

This validates catalogue IDs, parent relationships, laterality, provenance, source references, GLB files and GLB node names before writing the browser manifest.

## Intended use

Educational anatomy atlas under development. It is not a diagnostic device and must not be used for clinical decision-making.

## v0.3 scan-derived reference build

The app runs immediately with the v0.2 atlas seed geometry. To build the real TopBrain reference anatomy on a machine with Docker and internet access:

```sh
./anatomy.sh download
./anatomy.sh inspect
./anatomy.sh build 001   # replace 001 with the selected case
./docker.sh restart
```

`inspect` ranks cases only by image geometry and label completeness. It does **not** determine whether a case is clinically suitable as the definitive reference subject. The generated GLB and catalogue patch are local build products. TopBrain raw data are not included in this archive.
