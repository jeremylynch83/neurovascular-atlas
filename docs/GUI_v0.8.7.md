# Interface changes, v0.8.7

- Use Neurovascular Atlas in the header, browser title, info box and startup
  error text. Replace the info-box reconstruction summary and technical
  counts with a brief introduction and “Authored by Jeremy Lynch, 2026.”
- Show “Loading anatomy, please wait” with a percentage inside the progress
  bar, including while the catalogue is loading. The build records each
  model's byte size. Actual downloaded bytes account for 0–90%; final scene
  preparation reports 95%; completion follows the first scene render.
  Missing transfer-length headers are supported. Older manifests fall back
  to file download/completion stages. Progress is monotonic, with no timed
  increments. Load errors replace the bar with the existing error message.
- Hide the FPS readout on the existing idle callback, retaining direct DOM
  updates without panel rerenders or extra rendering.
- Give mobile panels equal side margins, using the larger safe-area inset
  on both sides. Reduce title padding from 9px to 6px vertically.
- Remove scrolling from the outer panel stack. Use flex sections with title
  buttons and shrinkable scrollable bodies, preserving panel and tree state
  when collapsed. Titles remain outside the scrolling bodies. Native buttons
  provide keyboard toggling and expose aria-expanded and aria-controls.
- Remove Fit, the separate Side row, planned counts and visible planned
  labels. Keep initial framing, mesh counts and laterality in structure names.
- Group relationships by type, deduplicate each type's structure IDs and
  show comma-separated linked names. Links use the existing select/focus
  handler and retain the current collapse state.

The anatomy assets, structure definitions, names, descriptions, source
records and relationship data are unchanged from v0.8.6. The installer and
Pages workflow are retained.

## Checks

Production builds for `/` and `/neurovascular-atlas/`; actual component
handlers for titles, grouped relationship links, loading success/error/
cancellation and FPS visibility; actual engine progress for known model
sizes without transfer lengths, legacy manifests and failures; retained
FPS/render coalescing; all 735 descriptions and 1,758 links; byte-identical
model assets and unchanged anatomical data.

Interaction and engine checks use renderer/hook fixtures. A browser binary
was unavailable for visual viewport testing. The panel CSS confines overflow
to the two shrinkable bodies and uses symmetric mobile insets.
