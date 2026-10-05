# Anatomical baseline audit v0.9.15

Stages 1 and 2 establish anatomical targets and course specifications. Vessel surfaces have not been fitted.

870 vascular labels audited; 290 intracranial course specifications. The four skull/vascular assets, existing vascular catalogue and original 172 brain meshes are retained exactly.

## First fitting targets

| Vessel | Target | Median wall distance mm | 95th percentile mm |
| --- | --- | ---: | ---: |
| Central right | Central sulcus | 5.60 | 10.45 |
| Central left | Central sulcus | 5.44 | 10.48 |
| Straight sinus | Falcotentorial line | 14.06 | 18.86 |
| Median anterior pontomesencephalic vein | Brainstem surface | 1.01 | 2.46 |
| Median anterior pontine vein | Brainstem surface | 1.69 | 2.98 |
| Median anterior medullary vein | Brainstem surface | 0.64 | 1.55 |

These are sampled unsigned distances of the displayed vessel wall to the atlas target, not required displacement or a centreline tolerance.

## Review state

- retained-baseline: 580
- requires-anatomical-review: 220
- requires-anatomical-target: 64
- requires-fitting: 6

## Remaining target gaps

- Reviewed choroidal fissure entry and plexal attachment: 16 vascular labels.
- Reviewed perforator entry sites and intraparenchymal course boundaries: 47 vascular labels.
- Cervical spinal cord surface: 1 vascular labels.

## Limits of this audit

- Sampled unsigned distance is not an exhaustive intersection or containment test.
- Attachment screens measure minimum vertex-to-triangle surface gaps, not lumen patency or shared junction topology. Catalogue relationships alone are not physical joins.
- Delivered labelled geometry is the authoritative radius/shape baseline; no fabricated centreline or numerical radius profile is substituted.
- Individual segment boundaries and tissue entry sites require review before fitting.
- Retained-baseline means unchanged, not independently verified anatomical correctness.
