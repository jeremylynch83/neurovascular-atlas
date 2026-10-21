// Compact distribution JSON only. Authoring data and all numerical values stay intact.
import fs from 'node:fs';
import path from 'node:path';
const root = path.resolve(import.meta.dirname, '../dist');
let before = 0, after = 0, files = 0;
for (const entry of fs.readdirSync(root, {recursive:true,withFileTypes:true})) {
  if (!entry.isFile() || !entry.name.endsWith('.json')) continue;
  const file = path.join(entry.parentPath, entry.name);
  const original = fs.readFileSync(file, 'utf8');
  const compact = JSON.stringify(JSON.parse(original));
  before += Buffer.byteLength(original); after += Buffer.byteLength(compact); files++;
  fs.writeFileSync(file,compact);
}
console.log(`Compacted ${files} distribution JSON files: ${before} -> ${after} bytes; values preserved.`);
