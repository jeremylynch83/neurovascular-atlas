"""Write the review hand-off using final measured results."""
import json, sys
from pathlib import Path

root = Path.cwd()
work = Path(sys.argv[1]).resolve()
dest = Path(sys.argv[2]).resolve()
report = json.loads((work / 'candidate/acceptance-continuation.json').read_text())
assert report['safeCheckpoint']
routes = '\n'.join('- ' + name for name in report['remainingRoutes'])
reference = '\n'.join('- ' + r['brain'] + ' / ' + r['reference'] for r in report['cortexTentoriumContacts'])
text = f'''Neurovascular Atlas: MMA continuation checkpoint v0.9.60

STATUS: UNRELEASED CANDIDATE. The recovered public app remains v0.9.51.
This is a recoverable authoring checkpoint and review, not an accepted
anatomical release. No candidate geometry has been published into the app.

Installed reference-fit change
The cerebral reference and selected cerebral vessels receive a bounded
superior correction against the existing tentorial roof. The skull, falx,
tentorium, brainstem and cerebellum remain in the prior frame. Native shared
attachment coordinates are held exactly. The fit is reduced around fixed
dural routes and unsuitable source detail. The entire left lateral
occipitotemporal parcel stays in the prior frame to avoid a new fixed-dural
artery contact. Source-detail neighbourhoods are blended back towards the
prior geometry where the larger correction would otherwise create folds.

Cortex/tentorium contact pairs fall from 10 in v0.9.59 to
{report['cortexTentoriumContactPairs']} in this candidate. There are
{report['referenceFitChangedLabels']} changed labels, a maximum additional
shift of {report['referenceFitMaximumShiftMm']:.3f} mm and minimum sampled
ambient-field Jacobian determinant of
{report['referenceFitMinimumJacobianDeterminant']:.6f}. Separate scalar-blend
reconstruction checks match the exported float32 buffers exactly and retain
positive sampled composed Jacobians. These vertex samples and triangle
tests do not establish a continuous clinical registration certificate.

The final triangle audits find zero new label-pair contacts relative to
v0.9.59 across moved/fixed vascular, neural and bone surfaces. Existing pairs
remain recorded, and their continued presence is not anatomical approval.
No new per-label triangle folds are found. Every shared native coordinate
remains exact: {report['nativeInterfaceMismatchMm']:.3f} mm maximum mismatch,
{report['missingNativeCoordinatePairs']} missing coordinate pairs.

Retained repairs
The left and right anterior falcine/MMA paramedian bodies and the right
occipital mastoid/MMA petrosquamosal body are byte-exact to v0.9.59. No new
collateral repair was installed. Bounded body, whole-sheet and fixed dural
arterial trials failed their combined constraints and remain diagnostics.
The left cavernous route and parent retain the previous rollback.

Remaining release conditions
{report['mmaNeuralContactPairs']} neural surface-contact pairs remain across
these six routes:
{routes}

{report['strictContainmentPairCount']} strict containment pair remains.
The left mastoid connection has 140 vertices inside the closed left lateral
occipitotemporal parcel, with maximum depth approximately 0.960 mm. Only
{report['eligibleContainmentBrainParcels']} neural parcels qualify for strict
containment screening; {report['excludedContainmentBrainParcels']} are
excluded. Full brain separation is not certified.

The remaining cortex/tentorium pairs are:
{reference}

Both reconstructed receiving-vein exteriors retain one connected component,
zero duplicate exterior triangles, zero non-manifold edges, zero degenerate
triangles and zero self-intersections. Their native cavernous boundary
coordinates remain exact and they clear the current neural and arterial
surfaces. {report['receiverBoneContactPairs']} vein/bone label pairs remain
unreviewed. Lumen continuity, clinical calibre and independent anatomical
review remain incomplete. Preserving delivered radial profiles does not
establish measured vessel diameter or normal patency.

Review files
- Neurovascular_Atlas_MMA_review_v0.9.60.html: self-contained interactive
  recovered v0.9.51 versus candidate v0.9.60 comparison. Source and candidate
  have independent exact position/index buffers. All changed reference-fit
  labels and original MMA review labels are included.
- Neurovascular_Atlas_MMA_comparison_v0.9.60.png: exact software renders of
  v0.9.59 versus v0.9.60 posterior cerebral/tentorial reference surfaces.
- MMA_validation_v0.9.60.json: measured final results, unresolved conditions
  and current buffer hashes.
- Neurovascular_Atlas_MMA_checkpoint_v0.9.60.zip: recoverable project and
  the latest two authoring checkpoints with one shared decoded source.

Browser execution remains unverified because no local browser executable is
available. The review JavaScript passes syntax checks and every embedded
source/candidate position and index buffer is hash-verified. The software
renders were visually inspected. These checks do not replace browser QA.

Project layout and reproducibility
recovered-app-v0.9.51 contains the unchanged public assets/application,
attribution/licences, tools, review sources, decoded source, work-v0959
and work-v0960. The current candidate retains complete normal
buffers. Redundant prior/source normals are omitted and can be regenerated
from their exact positions and faces. Original FBX, dependency directories,
older working histories, the v0.9.58 binary snapshot and app build output
remain omitted. Older authoring tools requiring work-v0958 need that
historical snapshot from the previous v0.9.59 archive. All current checks
listed below use the included current and v0.9.59 buffers.
Rejected proposals are marked as diagnostic files and are never loaded as
current candidate geometry. The installed state is work-v0960/candidate.

From recovered-app-v0.9.51, run these read-only checks:
  python3 tools/mma-v0958/check_all_mma.py work-v0960
  python3 tools/mma-v0958/check_native_interfaces.py work-v0960
  python3 tools/mma-v0958/check_installed_receiver.py work-v0960
  python3 tools/mma-v0959/check_neural_containment.py work-v0960
  python3 tools/mma-v0960/check_dural_reference_fit.py work-v0960
  python3 tools/mma-v0960/check_changed_network.py work-v0960
  python3 tools/mma-v0960/check_fixed_vessels.py work-v0960
  python3 tools/mma-v0960/check_composed_detail_field.py work-v0960
  python3 tools/mma-v0960/assess_checkpoint.py work-v0960

The reference-fit application script is an authoring operation, not a
read-only check. Re-running it requires restoring the candidate binary
buffers and revision from immutable work-v0959 first. It must not be
applied repeatedly to already transformed geometry. Its guard/control
point files are included in work-v0960.

Python, NumPy, SciPy, VTK and Pillow are required for the modelling checks.
The supplied native triangle checker targets Linux x86-64 / VTK 9.3.1;
its C source is included for rebuilding. The unchanged public app can be
run with npm ci and npm run dev, or built with npm run build. The separate
review source uses npx vite build --config review-v0960/vite.config.js.

Anatomical references retained for review
Ota T. Anatomy of the Middle Meningeal Artery. JNET 2026;20(1).
https://doi.org/10.5797/jnet.ra.2025-0131
Bonasia S et al. Middle Meningeal Artery: Anatomy and Variations.
AJNR 2020;41:1777-1785. https://www.ajnr.org/content/41/10/1777
San Millan Ruiz D et al. The Sphenoparietal Sinus of Breschet: Does It Exist?
AJNR 2004;25:112-120. https://www.ajnr.org/content/25/1/112
The potential-anastomosis overlays remain teaching reconstructions.
'''
dest.mkdir(parents=True, exist_ok=True)
(dest / 'README_MMA_v0.9.60.txt').write_text(text)
(dest / 'MMA_validation_v0.9.60.json').write_text(json.dumps(report, indent=2))
print('Wrote README and standalone validation report')
