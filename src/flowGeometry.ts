export type Point = [number, number, number];
export type FlowEntry = { points: Point[]; arc: number[]; length: number; vertexCount: number; coordinates: string; selectable: boolean; safeRanges?: [number,number][] };
export type FlowEdge = { to: string; at: number };
export type FlowData = { schema: number; sourceHashes: Record<string, string>; graphHash: string; graphSource: string; entries: Record<string, FlowEntry>; edges: Record<string, FlowEdge[]>; veinSites: Record<string, Point> };
export type InjectionPoint = { id: string; distance: number; point: Point };
export type FlowSection = { start: number; end: number; positions: Float32Array; indices: Uint32Array };

export function flowGraphSource(manifest: AnatomyManifest) {
  const rows=manifest.structures.filter(s=>s.system==='artery'&&s.asset&&s.displayGroup!=='anastomoses');
  return JSON.stringify({rows:rows.map(s=>[s.id,s.parent,s.segmentOf,s.asset]),relations:manifest.relationships.filter(r=>['branches_to','has_segment'].includes(r.type))});
}

export function downstreamFlow(data: FlowData, inlets: {id:string;distance:number}[], allowed: ReadonlySet<string>) {
  const result=new Map<string,{start:number;distance:number}>(),locked=new Map(inlets.map(p=>[p.id,p.distance]));
  const queue=inlets.map(p=>({id:p.id,start:p.distance,distance:0}));
  for(let i=0;i<queue.length;i++) {
    const v=queue[i];if(!allowed.has(v.id)||!data.entries[v.id])continue;
    if(locked.has(v.id)&&v.start<locked.get(v.id)!)continue;
    const old=result.get(v.id);if(old&&old.distance-old.start<=v.distance-v.start+1e-6)continue;
    result.set(v.id,{start:v.start,distance:v.distance});
    for(const edge of data.edges[v.id]??[])if(edge.at>=v.start-1e-5)queue.push({id:edge.to,start:0,distance:v.distance+edge.at-v.start});
  }
  return result;
}

export function projectToPath(points: Point[], arc: number[], p: ArrayLike<number>) {
  let best = Infinity, distance = 0, point: Point = points[0];
  for (let i=1;i<points.length;i++) {
    const a=points[i-1], b=points[i], dx=b[0]-a[0],dy=b[1]-a[1],dz=b[2]-a[2];
    const u=Math.max(0,Math.min(1,((p[0]-a[0])*dx+(p[1]-a[1])*dy+(p[2]-a[2])*dz)/(dx*dx+dy*dy+dz*dz || 1)));
    const q: Point=[a[0]+u*dx,a[1]+u*dy,a[2]+u*dz];
    const d=(q[0]-p[0])**2+(q[1]-p[1])**2+(q[2]-p[2])**2;
    if(d<best){best=d;distance=arc[i-1]+u*(arc[i]-arc[i-1]);point=q;}
  }
  return {distance,point,error:Math.sqrt(best)};
}
export function pathPoint(row: FlowEntry, distance: number): Point {
  const s=Math.max(0,Math.min(row.length,distance));
  let i=1;while(i<row.arc.length-1 && row.arc[i]<s)i++;
  const a=row.points[i-1],b=row.points[i],u=(s-row.arc[i-1])/(row.arc[i]-row.arc[i-1] || 1);
  return [a[0]+u*(b[0]-a[0]),a[1]+u*(b[1]-a[1]),a[2]+u*(b[2]-a[2])];
}
export function injectionOnPath(row: FlowEntry,p: ArrayLike<number>) {
  let distance=Math.min(row.length-.005,projectToPath(row.points,row.arc,p).distance);
  const ranges=row.safeRanges??[[0,row.length]];
  if(!ranges.some(([a,b])=>distance>=a&&distance<=b)) {
    const candidates=ranges.flatMap(([a,b])=>[a+Math.min(.001,(b-a)/2),Math.min(row.length-.005,b-Math.min(.001,(b-a)/2))]).filter(s=>s>=0);
    if(!candidates.length)throw Error('No safe catheter position on this course');
    distance=candidates.reduce((best,s)=>Math.abs(s-distance)<Math.abs(best-distance)?s:best);
  }
  return {distance,point:pathPoint(row,distance)};
}
export function decodeCoordinates(row: FlowEntry, positions: Float32Array) {
  const bytes=Uint8Array.from(atob(row.coordinates),c=>c.charCodeAt(0));
  const view=new DataView(bytes.buffer),s=new Float32Array(positions.length/3);
  if(bytes.length!==row.vertexCount*2)throw Error('Invalid flow coordinates');
  for(let i=0;i<row.vertexCount;i++)s[i]=view.getUint16(i*2,true)/65535*row.length;
  for(let i=row.vertexCount;i<s.length;i++)s[i]=projectToPath(row.points,row.arc,positions.subarray(i*3,i*3+3)).distance;
  return s;
}

/** Clip closed projection surfaces by a piecewise-linear path coordinate.
 * Every newly exposed boundary is capped. These are private DSA proxies;
 * the original atlas geometry and coordinates are never changed. */
export function splitFlowSurface(positions: Float32Array, indices: Uint32Array, coordinate: Float32Array, length: number, inlet=0, step=18): FlowSection[] {
  if(inlet>=length-.001)return [];
  const count=Math.max(1,Math.ceil((length-inlet)/step)),size=(length-inlet)/count;
  const sections: FlowSection[]=[];
  for(let section=0;section<count;section++) {
    const lo=inlet+section*size,hi=section===count-1?length:inlet+(section+1)*size;
    const p: number[]=[],f: number[]=[],keys=new Map<string,number>(),caps=new Map<string,[number,number]>();
    type Vertex={p:Point;s:number;key:string};
    const add=(v: Vertex)=>{
      const key=v.key;
      let i=keys.get(key);if(i===undefined){i=p.length/3;keys.set(key,i);p.push(...v.p)}return i;
    };
    const clip=(poly:Vertex[],cut:number,above:boolean)=>{
      const result: typeof poly=[];
      for(let i=0;i<poly.length;i++) {
        const a=poly[i],b=poly[(i+1)%poly.length],inside=above?a.s>=cut:a.s<=cut,next=above?b.s>=cut:b.s<=cut;
        if(inside)result.push(a);
        if(inside!==next){
          const first=a.key<b.key?a:b,last=a.key<b.key?b:a,u=(cut-first.s)/(last.s-first.s);
          result.push(u===0?first:u===1?last:{p:[first.p[0]+u*(last.p[0]-first.p[0]),first.p[1]+u*(last.p[1]-first.p[1]),first.p[2]+u*(last.p[2]-first.p[2])],s:cut,key:`(${first.key}|${last.key})@${cut}`});
        }
      }return result;
    };
    for(let i=0;i<indices.length;i+=3) {
      const ids=[indices[i],indices[i+1],indices[i+2]],ss=ids.map(v=>coordinate[v]);
      if(Math.max(...ss)<lo || (section<count-1&&Math.min(...ss)>hi))continue;
      let poly=ids.map((v,j)=>({p:Array.from(positions.subarray(v*3,v*3+3)) as Point,s:ss[j],key:Array.from(positions.subarray(v*3,v*3+3)).join(',')}));
      if(lo>0)poly=clip(poly,lo,true);
      if(hi<length)poly=clip(poly,hi,false);
      const verts=poly.map(add);
      for(let j=1;j<verts.length-1;j++)if(new Set([verts[0],verts[j],verts[j+1]]).size===3)f.push(verts[0],verts[j],verts[j+1]);
      for(let j=0;j<poly.length;j++) {
        const k=(j+1)%poly.length,a=verts[j],b=verts[k];if(a===b)continue;
        if((lo>0 && poly[j].s===lo && poly[k].s===lo)||(hi<length && poly[j].s===hi && poly[k].s===hi)) {
          const key=a<b?`${a},${b}`:`${b},${a}`;
          if(caps.has(key))caps.delete(key);else caps.set(key,[b,a]);
        }
      }
    }
    const outgoing=new Map<number,number[]>();
    for(const [a,b] of caps.values())outgoing.set(a,[...(outgoing.get(a)??[]),b]);
    while(outgoing.size) {
      const first=outgoing.keys().next().value!,loop=[first];let current=first;
      for(let guard=0;guard<=caps.size;guard++) {
        const choices=outgoing.get(current);if(!choices?.length)throw Error('Open flow-section boundary');
        const next=choices.pop()!;if(!choices.length)outgoing.delete(current);
        if(next===first)break;loop.push(next);current=next;
        if(guard===caps.size)throw Error('Unclosed flow-section boundary');
      }
      if(loop.length<3)continue;
      const centre: Point=[0,0,0];for(const v of loop)for(let k=0;k<3;k++)centre[k]+=p[v*3+k]/loop.length;
      const c=p.length/3;p.push(...centre);
      for(let j=0;j<loop.length;j++)f.push(c,loop[j],loop[(j+1)%loop.length]);
    }
    if(f.length)sections.push({start:lo,end:hi,positions:new Float32Array(p),indices:new Uint32Array(f)});
  }
  return sections;
}

export function closedSurfaceError(section: FlowSection) {
  const edges=new Map<string,number>();
  for(let i=0;i<section.indices.length;i+=3)for(let j=0;j<3;j++) {
    const a=section.indices[i+j],b=section.indices[i+(j+1)%3];if(a===b)continue;
    const key=a<b?`${a},${b}`:`${b},${a}`;
    edges.set(key,(edges.get(key)??0)+(a<b?1:-1));
  }
  return [...edges.values()].filter(n=>n!==0).length;
}

/** Oriented ray crossings, including closed components that touch. */
export function pointInsideSurface(positions: Float32Array,indices: Uint32Array,p: ArrayLike<number>) {
  const dx=.872913,dy=.391127,dz=.288731;let winding=0;
  for(let i=0;i<indices.length;i+=3) {
    const a=indices[i]*3,b=indices[i+1]*3,c=indices[i+2]*3;
    const x1=positions[b]-positions[a],y1=positions[b+1]-positions[a+1],z1=positions[b+2]-positions[a+2];
    const x2=positions[c]-positions[a],y2=positions[c+1]-positions[a+1],z2=positions[c+2]-positions[a+2];
    const hx=dy*z2-dz*y2,hy=dz*x2-dx*z2,hz=dx*y2-dy*x2,det=x1*hx+y1*hy+z1*hz;
    if(Math.abs(det)<1e-12)continue;
    const sx=p[0]-positions[a],sy=p[1]-positions[a+1],sz=p[2]-positions[a+2],u=(sx*hx+sy*hy+sz*hz)/det;
    if(u<0||u>1)continue;
    const qx=sy*z1-sz*y1,qy=sz*x1-sx*z1,qz=sx*y1-sy*x1,v=(dx*qx+dy*qy+dz*qz)/det;
    if(v<0||u+v>1)continue;
    if((x2*qx+y2*qy+z2*qz)/det>1e-7)winding+=det<0?1:-1;
  }
  return winding!==0;
}
import type { AnatomyManifest } from './types';

