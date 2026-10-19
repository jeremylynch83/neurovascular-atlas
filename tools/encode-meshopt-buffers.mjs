// Lossless authoring helper. Untouched production buffers are never re-encoded.
import {MeshoptEncoder} from 'meshoptimizer';
let input='';for await(const chunk of process.stdin)input+=chunk;
await MeshoptEncoder.ready;
const out=JSON.parse(input).map(row=>Buffer.from(MeshoptEncoder.encodeGltfBuffer(
 Buffer.from(row.bytes,'base64'),row.count,row.stride,row.mode)).toString('base64'));
process.stdout.write(JSON.stringify(out));
