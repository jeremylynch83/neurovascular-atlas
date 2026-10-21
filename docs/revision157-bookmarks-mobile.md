# Revision157: PICA bookmarks and mobile structure details

The vertebrobasilar preset referred to the old PICA group IDs after the main vessels were split into P1-P5 segments. Those groups have no mesh, so the preset omitted the main PICA courses. The ten existing segment IDs are now included in the existing preset vessel list. Left, right and bilateral filtering, geometry loading and injection classification reuse the current implementation.

At mobile widths up to 680px, the detail panel keeps the structure name in its tappable header. The repeated body heading is hidden and the first detail section loses its redundant top divider and spacing. Subsequent section dividers and the desktop layout are retained.

Validation: production build, catalogue/DSA comparisons, explicit PICA membership and side checks, staged-loader selection before and after geometry is ready, and startup validation passed. Mobile CSS was checked against actual React-rendered structure markup. The browser visual check was unavailable. All source and loading-pack GLBs are byte-identical to revision156.
