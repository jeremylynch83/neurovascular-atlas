# Final integrated review, batch 8

Release v0.9.141 completes the eight-batch skull-foramina programme. The represented regional passage repairs pass their regression checks. The broader screen has open findings, so this release does not give unqualified whole-model anatomical acceptance.

## Results

| Check | Result |
|---|---|
| Delivered mesh arrays decoded | 1258 |
| Invalid indices or non-finite arrays | 0 |
| Artery and vein meshes screened against bone | 1005 |
| Regional DSA, geometry, section and brain-binding checks | 16 passed |
| DSA projection surfaces checked | 605 closed |
| Tested DSA injection split sections | 848 closed |
| Injection-range gate checks | 594 passed |
| Whole-surface self-contact screens of repaired arteries | 106 |
| Public catalogue region corrections | 2 |

The two mylohyoid-groove entries now correctly belong to Mandible in the public catalogue. No application behaviour, vessel graph, DSA data or model geometry changes in this batch. All five model files, both DSA files and application source are byte-identical to v0.9.140; the existing mandibular shading repair is preserved.

## Findings that prevent global acceptance

The whole-bone screen found 195 contacting pairs, including four ICA/condylar pairs at the upper cervical/petrous transition. Earlier regional carotid tests did not include the separately modelled condyles. The proximal anterior tympanic/jaw relationship is also still open. The source parietal meshes have non-manifold edges, and the full-surface screen records inherited vessel folds outside some earlier regional windows.

See [the prioritised issue register](skull-foramina-residual-issues.md), its companion JSON and [direct carotid/condylar sections](foramina-batch8-carotid-condyle-sections.png). Contact counts are screening evidence and do not automatically diagnose a wrong anatomical route. Potential connections, venous apposition and dural grooves need separate review.

DSA closure and safe-range gating passed, while stored coverage restrictions and sampled guide-probe findings are retained in the register. This review does not make disabled sites selectable or replace restricted ranges with full-length eligibility.

## Scope and reproducibility

`tools/foramina/validate-whole-model.py` checks decoded mesh arrays and screens every represented arterial and venous surface against all craniofacial bone parts, including teeth and hyoid. It does not prove complete vessel containment, measure penetration volume or validate every microscopic anatomical feature. The repaired-surface test screens full surfaces rather than repeating only historical local windows. All seven regional DSA suites, six regional geometry suites, two section/passage suites and the brain surface binding check pass on the delivered geometry.

The new whole-delivery reports were run on v0.9.140 geometry. Byte-identity evidence makes those results applicable to this metadata-and-report release. Historical reports retained in the archive describe their original regions/releases and must not be read as global certificates.

The source-limited microcanals and optional variants listed in batch 7 remain unresolved or unselected. Completion of the planned programme means the correction and review cycle is documented; the residual register defines the further anatomical work still required.
