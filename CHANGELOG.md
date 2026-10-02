# Changelog

## 0.2.0
- Added first visible vascular geometry: 14 ECA arterial structures and 8 extracranial venous structures from Z-Anatomy-derived atlas paths.
- Added explicit `atlas-derived` provenance so these meshes cannot be mistaken for CTA-derived anatomy.
- Added extracranial venous catalogue entries for retromandibular, maxillary and facial veins.
- Deliberately excluded the starter project's schematic pterygoid plexus and inferior alveolar vein.
- Default view now ghosts bone and emphasises arteries.
- Updated UI and generated manifest to v0.2.

## 0.1.2
- Fixed quantised legacy GLB transform rendering.
- Detached Docker startup and added Tailscale URL reporting.

## 0.3.0
- Added reproducible TopBrain v3 download, inventory and scan-derived mesh build pipeline.
- Added official CTA label mapping for 34 shared arterial classes plus six CTA venous classes.
- Added CT-derived reference skull generation in the same NIfTI physical coordinate system.
- Added generated-catalogue overlay so scan-derived geometry replaces matching atlas/planned structures without editing the hand-authored catalogue.
- Added M1/M2/M3, A1-A2/A3 and P1-P2/P3-P4 logical segment structures required by the TopBrain labels.
- Raw 2 GB TopBrain data are intentionally excluded from the distributable application archive.
