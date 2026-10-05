# Third-party anatomy

## BodyParts3D legacy context
The temporary skull context is inherited from the Dental Scope starter project and remains subject to its recorded BodyParts3D attribution/share-alike terms. It is not the final INR skull.

## Z-Anatomy vascular seed
v0.2 includes selected vascular paths derived from Z-Anatomy `Startup.blend`, licensed CC BY-SA 4.0. The Dental Scope source pipeline sampled Z-Anatomy Bezier curves and registered the Z-Anatomy mandible/maxillae to BodyParts3D by similarity ICP before sweeping the curves into meshes. v0.2 reuses only structures documented by that pipeline as atlas-derived.

These are not scan-derived vascular segmentations. The app records them as `atlas-derived` and `placeholder` geometry.

## TopBrain Challenge Data Release v3
TopBrain Challenge Organizers, Zenodo record 21972006, 17 August 2026. The release permits non-commercial use with source attribution; commercial use requires prior permission from the data owner. The v0.3.5 archive includes derived case 001 reference surfaces and the unchanged original surface master from the previously built CTA reference. Vessel surfaces originate in the supplied labels; the skull is a CT intensity-threshold surface. Display meshes are smoothed, with processing measurements recorded in the catalogue patch. The raw CTA and label archive is not redistributed. Source: [TopBrain Challenge Data Release v3](https://zenodo.org/records/21972006). The application code licence does not replace the dataset terms.

## Right ECA reference reconstruction (v0.3.6)

The new vessel tree is manually authored geometry guided by Kiyosue angiograms and cross-checked against Borden. It is a teaching reconstruction, not a patient segmentation. No book pages or reference angiogram image files are embedded in this archive. The aligned skull context is derived from the existing BodyParts3D model and retains the attribution/share-alike terms above. The vessel reconstruction is not a replacement for clinical imaging or a validated anatomical reference.

- **Z-Anatomy brain and dura**: 172 selected surfaces from the official PC-Version FBX collection, registered and labelled for Neurovascular Atlas. CC BY-SA 4.0 (https://creativecommons.org/licenses/by-sa/4.0/), with original BodyParts3D / Database Center for Life Science credit retained. Both `anatomy/source/brain/source-orientation.glb` and `public/anatomy/models/brain-context.glb` are share-alike model assets. Adaptations: object transforms baked, units converted, shared skull registration, triangulation, normals and label metadata. Original licence: `public/anatomy/licenses/Z_Anatomy_Source_Licence.txt`.
