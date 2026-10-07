Anatomical audit and v0.9.29 correction references are listed in [the correction report](docs/ANATOMICAL_CORRECTIONS_v0.9.29.md) and its linked machine-readable register. Article content and illustrations are not redistributed.

# Credits

Neurovascular Atlas, authored by Jeremy Lynch, 2026.

Software: React/React DOM, Three.js, Meshoptimizer, Vite, TypeScript, NumPy, SciPy, VTK, Manifold3D and Trimesh. Interface fonts: Inter Tight, JetBrains Mono and Source Serif 4, distributed through Fontsource. Licence summaries appear in the scrollable information modal; package licence files retain their own terms.

Bony context: **BodyParts3D**, © The Database Center for Life Science, CC BY-SA 2.1 Japan.

Anatomical reference catalogue informed by:

- Jeremy Lynch, Shelley Renowden and Philip White (eds.), *Neurointervention*, Oxford Specialist Handbooks, Oxford University Press (2026).
- Neil M. Borden, *3D Angiographic Atlas of Neurovascular Anatomy and Pathology* (2006).
- Hiro Kiyosue (ed.), *External Carotid Artery: Imaging Anatomy Atlas for Endovascular Treatment* (2020).
- Gianni Boris Bradač, *Applied Cerebral Angiography: Normal Anatomy and Vascular Pathology* (2017).
- [Neuroangio.org](https://neuroangio.org/), by Maksim Shapiro, MD.

The skull-base venous review also credits the primary studies by San Millán Ruïz et al., Tubbs et al., Ekanem et al. and Evans et al. listed with links in [VENOUS_v0.9.6.md](docs/VENOUS_v0.9.6.md). Detailed structure provenance is retained in the anatomy manifest.

References inform reconstructions and descriptions. Book figures and downloaded angiographic reference images are not distributed inside the application.

- **Z-Anatomy brain and dura**: 172 selected surfaces from the official PC-Version FBX collection, registered and labelled for Neurovascular Atlas. CC BY-SA 4.0 (https://creativecommons.org/licenses/by-sa/4.0/), with original BodyParts3D / Database Center for Life Science credit retained. Both `anatomy/source/brain/source-orientation.glb` and `public/anatomy/models/brain-context.glb` are share-alike model assets. Adaptations: object transforms baked, units converted, shared skull registration, triangulation, normals and label metadata. Original licence: `public/anatomy/licenses/Z_Anatomy_Source_Licence.txt`.
