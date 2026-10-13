import {decodeCoordinates,prepareFlowSurface,splitFlowSurface,closedSurfaceError,type FlowEntry,type PreparedFlowSurface} from './flowGeometry';

type Surface={positions:Float32Array;indices:Uint32Array;row:FlowEntry};
const surfaces=new Map<string,Surface&{coordinate:Float32Array;prepared:PreparedFlowSurface}>();
self.onmessage=({data}:{data:{request:number;id:string;inlet:number;surface?:Surface}})=>{
  const {request,id,inlet,surface}=data;
  try{
    if(surface){const coordinate=decodeCoordinates(surface.row,surface.positions);surfaces.set(id,{...surface,coordinate,prepared:prepareFlowSurface(surface.positions,surface.indices,coordinate)})}
    const cached=surfaces.get(id);if(!cached)throw Error(`Missing injection surface: ${id}`);
    const sections=splitFlowSurface(cached.positions,cached.indices,cached.coordinate,cached.row.length,inlet,18,cached.prepared);
    if(sections.some(closedSurfaceError))throw Error(`Open injection section: ${id}`);
    self.postMessage({request,sections},{transfer:sections.flatMap(s=>[s.positions.buffer,s.indices.buffer]) as Transferable[]});
  }catch(error){self.postMessage({request,error:error instanceof Error?error.message:String(error)})}
};
