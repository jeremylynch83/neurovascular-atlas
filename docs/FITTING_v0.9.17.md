# v0.9.17: expanded fitting validation checkpoint

The runnable atlas retains all five production geometry assets exactly. No fitting candidate has met the complete connected-family acceptance criteria. The cavernous sinus and ICA corrections from v0.9.13, registered brain and dura, central sulcal targets, catalogue and viewer remain available.

This checkpoint adds a broader cortical-family tissue check, an exact exported-buffer check, and a separate refinement tool that uses the dominant sampling axis for lateral cortical branches. Shared junction topology is cached between passes. The additional candidate remains rejected and is supplied only as review evidence.

## Additional trial result

The main left and right central arteries cleared the named banks in the checked sulcal phase and had no contacts with retained arterial labels. The connected family did not pass: the left cortical branch introduced 584 postcentral contacts, the left distal ramus introduced 188, and the left cortical branch introduced 134 skull contacts. Those relationships had zero corresponding baseline contacts. The right cortical branch retained a pre-existing postcentral contact relationship but increased its contact count from 44 to 706. These counts describe triangle contacts, not volumes or clinical risk.

The attempt to compare all attached branches at the previous matched vertical section stations also failed because a right cortical branch no longer crossed some of those planes. This is a limitation of matched-world-plane calibre comparisons for moved, oblique branches. It does not establish lumen loss or patency.

The main vessel result cannot approve its connected branch family. The entire candidate is withheld. Brainstem and dural candidates remain blocked by the previously documented clival/tonsillar and cerebellar/callosal relationships. Their original geometry is retained too.

## Evidence

- `validation/advanced-central-trial-v0.9.17.json`: displacement and skin-junction records for the additional candidate.
- `validation/advanced-central-primary-trial-v0.9.17.json`: primary sulcal wall checks.
- `validation/advanced-central-tissue-trial-v0.9.17.json`: complete named cortical-family tissue check.
- `validation/advanced-central-skull-trial-v0.9.17.json`: skull regression that rejected the candidate.
- `validation/advanced-central-calibre-limit-v0.9.17.json`: incomplete matched-plane comparison.
- `validation/advanced-trial-central-comparison-v0.9.17.png`: matched baseline and explicitly rejected candidate views.
- `anatomy/source/brain/trials/advanced-central-v0.9.17.glb`: the eight exact rejected mesh labels, isolated from the normal viewer assets.

The earlier trial evidence remains in [the v0.9.16 checkpoint report](FITTING_v0.9.16.md). The current release checks describe retained production geometry. Publication guards require matching authoring hashes and reject changed geometry in this checkpoint. The normal app never loads trial meshes or runs fitting.

## Review and reproduce

Use v0.9.15's delivered geometry as the authoring baseline, following the preparation steps in the preceding checkpoint report. The production assets in v0.9.16 and v0.9.17 are identical to that baseline. The separate `refine_cortical_trial.py` requires `--experimental` and writes review-only authoring outputs. Its `--branch-only`, `--family-only` and `--terminal-only` modes resume a prepared trial. It does not change production assets or publish geometry.

To render the supplied exact candidate, decode its GLB to `.authoring/advanced-central-trial.glb` with `tools/decode_glb.mjs`, retain the decoded baseline arterial skin and original brain asset, then run `tools/brain/render_advanced_trial.py`. The normal production build has no additional dependencies.

The next modelling step is to define supported courses for each attached branch and reconstruct the joined regional skin with fixed external collars. The brainstem/tonsillar/clival and falcotentorial/Galenic tissue corridors require their own target reconciliation. Baseline tissue contacts remain recorded as unresolved. Atlas contact checks do not establish patient anatomy or a separately segmented lumen.
