// v0.9.79 reference for byte-for-byte geometry regression checks.
import type {Point,FlowSection} from "../../src/flowGeometry";
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

