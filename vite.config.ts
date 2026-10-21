import { defineConfig, loadEnv } from 'vite';
import react from '@vitejs/plugin-react';
import viewerCatalogueAsset from './src/viewerCatalogueAsset.json' with { type: 'json' };
import { explanationMarkup } from './src/explanationMarkup.ts';

export default defineConfig(({mode}) => {
  const env = loadEnv(mode, process.cwd(), 'INR_');
  const site = new URL(env.INR_SITE_URL || 'https://www.neurovascularatlas.com/');
  if (site.protocol !== 'https:' || site.search || site.hash) throw new Error('INR_SITE_URL must be an HTTPS site URL without a query or fragment');
  if (!site.pathname.endsWith('/')) site.pathname += '/';
  const url = site.href;
  const authors = ['Jeremy Lynch', 'Sean McIlhone'].map((name, i) => ({'@type':'Person','@id':`${url}#author-${i+1}`,name}));
  const schema = {
    '@context':'https://schema.org',
    '@graph': [
      ...authors,
      {'@type':'WebSite','@id':`${url}#website`,url,name:'Neurovascular Atlas',inLanguage:'en-GB',author:authors.map(a=>({'@id':a['@id']}))},
      {'@type':'WebPage','@id':`${url}#webpage`,url,name:'Neurovascular Atlas | 3D Anatomy for Neurointervention',isPartOf:{'@id':`${url}#website`},mainEntity:{'@id':`${url}#application`},inLanguage:'en-GB'},
      {'@type':'WebApplication','@id':`${url}#application`,url,name:'Neurovascular Atlas',description:'An interactive 3D atlas of neurovascular anatomy for neurointervention and interventional neuroradiology education.',applicationCategory:'EducationalApplication',operatingSystem:'Web browser',browserRequirements:'JavaScript and WebGL',author:authors.map(a=>({'@id':a['@id']})),keywords:['anatomy','neurovascular anatomy','neurointervention','interventional neuroradiology','cerebral circulation','brain aneurysm anatomy','stroke anatomy','thrombectomy anatomy','embolisation anatomy'],inLanguage:'en-GB'}
    ]
  };
  return {
  plugins: [react(), {
    name:'atlas-search-metadata',
    transformIndexHtml: {order:'pre',handler(html) {
      return {html:html.replaceAll('%ATLAS_SITE_URL%',url).replaceAll('%ATLAS_CATALOGUE%',viewerCatalogueAsset.file).replaceAll('%ATLAS_EXPLANATION%',explanationMarkup()),tags:[{tag:'script',attrs:{type:'application/ld+json'},children:JSON.stringify(schema).replaceAll('<','\\u003c'),injectTo:'head'}]};
    }},
    generateBundle() {
      this.emitFile({type:'asset',fileName:'robots.txt',source:`User-agent: *\nAllow: /\n\nSitemap: ${url}sitemap.xml\n`});
      const escaped=url.replaceAll('&','&amp;').replaceAll('<','&lt;').replaceAll('"','&quot;');
      this.emitFile({type:'asset',fileName:'sitemap.xml',source:`<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"><url><loc>${escaped}</loc></url></urlset>\n`});
    }
  }],
  base: process.env.INR_BASE ?? '/',
  server: { allowedHosts: ['terminal.local'] },
  build: { target: 'es2022', chunkSizeWarningLimit: 900 },
  };
});
