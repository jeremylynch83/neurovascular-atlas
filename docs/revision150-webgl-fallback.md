# Revision 0.9.150: explanation independent of WebGL

The initial HTML contains the atlas description, background and educational context. This content is generated at build time from the same source used by the existing About panel. It is available without JavaScript, a downloaded catalogue, React or WebGL. No additional content page or crawler-specific response is added.

## Loading and success

The explanation is visible while the viewer loads automatically, with progress information above it. The React viewer remains behind it and is not keyboard- or screen-reader-accessible until its first primary scene has rendered.

The engine reports success after drawing the prepared primary scene and checking that the WebGL context has not been lost. Catalogue completion, model preparation and a successful WebGL constructor alone do not hide the explanation. On success, the explanation panel is hidden and the original viewer is enabled. The same explanation remains available through About. The atlas-startup performance measure now ends at this first rendered primary scene.

## Failure

The explanation sits outside the React root. Catalogue and module-loading failures are caught during boot. A React error boundary handles rendering and effect errors, including failure to create a WebGL renderer. Initial geometry-loading and scene-rendering failures restore the explanation, stop the failed engine and show a retry link. Retry reloads the current page. A late success callback cannot hide a recorded failure.

If JavaScript is disabled, the explanation is still visible and a noscript message explains the viewer requirements. Loading and error messages are marked data-nosnippet so the factual explanation can be used for search snippets instead of transient status text.

The behaviour is based on the actual viewer lifecycle, with no Googlebot or user-agent detection. Availability of HTML content does not guarantee indexing or ranking; the published page should be checked with Google's URL Inspection tool after deployment.

## Validation

- Production build, TypeScript and anatomy validation pass.
- Startup tests cover initial HTML content, isolation from the React root, loading/progress, success visibility, keyboard focus transfer, failure/retry state and protection against late success callbacks.
- The initial explanation and About share one content source, with escaped text and HTTPS reference links.
- The actual WebGL-disabled browser was checked: the explanation remained readable, the failure message and retry link appeared, and retry returned to loading with the explanation still visible.
- Viewer catalogue regression checks compare descriptions, search, focus geometry, geometry dependencies, vessel counts, relationships and all 15 DSA preset/side combinations against the full manifest.
- The 3D models remain byte-for-byte unchanged. Full GPU-rendered success could not be visually checked in the test browser, which disables WebGL. Success-state DOM transitions were tested separately and are not claimed as a GPU rendering benchmark.

Run npm run web:startup after a production build to repeat the startup checks. The source ZIP uses the existing npm ci / npm run build installation process. The live website was not updated.
