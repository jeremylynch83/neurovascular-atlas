# Regional fitting continuation

The runnable app remains v0.9.21 with its existing checked pontine and posterior-fossa changes. No PCA or deep venous trial from this continuation has been applied.

The recovered regional trial was rejected after 39 new or increased arterial comparisons, venous wall failures, lost joins and poor sections. Three more local strategies were tested: compact medial displacement, combined medial/inferior venous displacement, and canonical basal-vein guide fitting with original calibre profiles and fixed native collars. These also failed independent exported-wall checks.

The latest candidate retains source labelled triangles, the closed venous collision solid and the actual shared native label interfaces. It is rejected for new/increased tissue and arterial contacts. See `continuation-status.json` and `continuation-region/local-veins-validation.json` for exact results and geometry hashes. Original source calibre varies along the basal vein; a constant 1.65 mm fitting radius was too conservative for anterior portions and is replaced in the latest authoring script.

## Next work

Reconcile the Galenic/ICV outlets and the adjacent medial temporal, peduncular and deep brain surfaces as one connected region, using appropriate anatomical references and maintaining skull/dural relations. Then fit the PCA and basal/mesencephalic courses into the resulting cisternal space. Whole-region inferior or medial shifts failed. Independent triangle intersections, containment for closed tissues, full-wall arterial separation, source-bound joins and actual free cross-sections must pass before integration.

The saved inputs and experiments are self-contained in the checkpoint archive. Unzip it and run `python3 fit_basal_corridors.py`, then `python3 validate_local_region.py veins` to reproduce the latest failed candidate. NumPy, SciPy, trimesh, VTK and manifold3d are required for authoring. These scripts do not modify production app assets.
