# v0.9.154: no timed loading pause

Removes the 24 ms interaction interval and the adaptive slow-frame delay entirely. A touch, held drag, camera damping or slow frame no longer creates a loading quiet period or added timer interval. The now-unused loading-pacing state and frame-duration tracking are removed.

Background installation continues through the existing bounded worker packets, with a zero-delay yield after a browser paint so input and rendering can run between packets. There is no additional timed pause. This does not force the browser to execute background work while its tab is suspended, nor guarantee that GPU uploads are instantaneous.

Skull-first order, anatomical geometry, generated packs, visibility defaults, selection, DSA and the initial HTML fallback remain unchanged. The scheduling checks exercise the actual method during sustained motion, consecutive packets, slow rendering, idle, disposal and obsolete pacing deadlines. Production build and TypeScript validation are rerun; anatomy/pack/DSA bytes are checked against v0.9.153. Successful GPU rendering and real-device responsiveness remain unverified.
