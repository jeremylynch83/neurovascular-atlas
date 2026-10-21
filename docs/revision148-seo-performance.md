# Revision 0.9.148: search metadata and loading improvements

This release adds no content pages, menus, introductory panels or changes to the viewer's layout. Anatomy, default views, model fidelity and existing interaction modules are retained.

## Search metadata

- Descriptive title and summary for neurovascular anatomy, neurointervention and interventional neuroradiology.
- Author metadata for Jeremy Lynch and Sean McIlhone.
- Canonical URL, English (UK) language and social sharing metadata with a 1200 x 630 preview image.
- JSON-LD for the website, page, educational web application and authors. Anatomical learning keywords include brain aneurysm, stroke, thrombectomy and embolisation; no treatment or outcome claims are added.
- A one-URL sitemap and robots.txt generated during the production build.

The default canonical URL is https://www.neurovascularatlas.com/. If the production site's preferred hostname differs, set `INR_SITE_URL` to the full HTTPS site URL before building. Existing `INR_BASE` support is retained. No DNS changes or live redirects were made.

## Loading

- Compact distribution JSON without dropping fields or reducing numerical precision as interpreted by the application.
- Load the DSA rendering module when injection/DSA preparation is requested. Existing DSA data loading and controls remain available.
- Replace catalogue `no-store` with mandatory cache revalidation so an unchanged catalogue can reuse a cached response.
- Retain the same fonts, weights and Unicode ranges using WOFF2, supported by the existing modern browser target.
- Retain geometry workers and staged loading, including the existing deferred vein and brain loading.
- Include HTML in production gzip precompression.
- Nginx serves immutable caching only for versioned model/DSA requests and hashed assets. Unversioned catalogue/model requests revalidate. Missing URLs return 404; there are no additional application routes.

Cache headers in nginx.conf apply to Docker/Nginx deployment. Other hosts, including GitHub Pages, control their own compression and cache headers. Gzip sidecar files alone do not prove that a host serves compressed responses.

## Measurements and validation

See revision148-web-validation.json for production asset sizes and the controlled Node catalogue parsing microbenchmark. These are local measurements, not live website timings or Core Web Vitals. The compact catalogue is approximately 35% smaller uncompressed and 12% smaller with gzip. Main startup JavaScript is approximately 1% smaller; the stylesheet is approximately 10% smaller uncompressed.

The complete production build, TypeScript checking, anatomy validation and all 28 updated flow courses pass. All five GLB model files are byte-for-byte unchanged. Every compacted JSON document is checked against its source after parsing. The catalogue matches the previous release apart from its release identifier. Viewer layout, interaction and staged loading modules are unchanged.

The browser preview reaches the new page title and application boot. Full rendering and interaction checks could not be completed because WebGL is disabled in the test browser. No live indexing, Search Console submission, Lighthouse score or user-device timing is claimed.

## Installation and deployment

Use the existing installation/update procedure. `npm ci` followed by `npm run build` produces the deployable `dist/` directory, including the sitemap, robots.txt, social image, metadata and compacted data. The release ZIP follows the existing source-package format and excludes dependencies and generated build output.

After deployment, verify the preferred hostname, actual cache/compression response headers and usable-viewer loading times on a WebGL-capable desktop and mobile browser. Sitemap submission to Google Search Console or Bing Webmaster Tools requires access to the relevant webmaster account and has not been performed.
