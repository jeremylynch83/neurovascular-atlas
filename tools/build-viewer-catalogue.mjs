import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import { createViewerCatalogue } from '../src/viewerCatalogue.ts';

const root = path.resolve(import.meta.dirname, '..');
const full = JSON.parse(fs.readFileSync(root+'/public/anatomy/manifest.json', 'utf8'));
const catalogue = JSON.stringify(createViewerCatalogue(full));
const sha256 = crypto.createHash('sha256').update(catalogue).digest('hex');
const directory = root+'/public/anatomy/viewer';
fs.mkdirSync(directory, {recursive:true});
// Only remove previous outputs owned by this generator.
for (const name of fs.readdirSync(directory)) if (/^catalogue-[a-f0-9]{20}\.json$/.test(name)) fs.unlinkSync(path.join(directory,name));
const file = `viewer/catalogue-${sha256.slice(0,20)}.json`;
fs.writeFileSync(root+'/public/anatomy/'+file, catalogue);
fs.writeFileSync(root+'/src/viewerCatalogueAsset.json', JSON.stringify({file,release:full.release,sha256},null,2)+'\n');
console.log(`Viewer catalogue: ${Buffer.byteLength(catalogue)} bytes; full authoring manifest retained.`);
