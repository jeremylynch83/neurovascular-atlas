# v0.9.155: dark introduction

Uses the approved title, tagline, educational description and “Loading 3D anatomy…” status. The loading-order explanation is omitted. No author name or professional background is rendered in the intro; existing author information and credits remain in About. Search metadata is retained.

The initial HTML includes the intro before JavaScript, with the app’s dark palette, display/UI/monospaced font families, panel border, radius and shadow. The initial dark theme matches the app’s existing default. The progress bar and a visible measured percentage remain beneath the status. Both are hidden on failure, when Retry appears. No-JavaScript visitors retain the description and a short feature-requirement message.

The full About text is kept separately from the concise intro. Startup success/failure behaviour, skull-first loading and the absence of timed loading pauses are retained. No geometry or DSA changes. Build and existing startup checks are rerun. GPU rendering remains unverified in this environment.
