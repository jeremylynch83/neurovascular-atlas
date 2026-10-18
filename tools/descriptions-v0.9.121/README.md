# Description audit v0.9.121

The complete, exact before/after list with per-entry reasons is retained in `anatomy/metadata/description-corrections-v0.9.121.json` and the searchable report in `docs/Description_Audit_v0.9.121.html`.

The anatomy validator applies this description-only overlay during normal builds, including after catalogue regeneration. Update the reviewed overlay when changing one of its entries. It cannot alter IDs, names, parentage, segment ranges, graph edges or model geometry.

Run `python3 tools/descriptions-v0.9.121/validate.py /path/to/unpacked/v0.9.120` to verify the exact scope, all internal description links, unchanged model assets, unchanged DSA recipes/flow and unchanged runtime source.

The audit covers existing populated descriptions. It does not certify model geometry or settle every source-label ambiguity. Empty descriptions are inventoried separately in the report. The usual ophthalmic origin of medial palpebral arteries is described without changing the current angular-linked meshes or their catalogue parents.
