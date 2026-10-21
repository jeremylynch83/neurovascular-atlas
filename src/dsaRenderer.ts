import * as THREE from 'three';
import { dsaBlushConcentration, dsaConcentration, type DsaRun, type DsaVessel } from './dsa';
import type { AnatomyManifest } from './types';
import { flowGraphSource, injectionOnPath, pointInsideSurface, pathPoint, type FlowData, type FlowSection, type InjectionPoint } from './flowGeometry';

type Surface = { vertexCount: number; extra: number[][]; reverse: boolean; flips: number[]; removed: number[]; caps: number[]; faces: number };
type Surfaces = { schema: number; assetRevisions: Record<string, string>; sourceHashes: Record<string,string>; entries: Record<string, Surface> };
const vertex = `varying vec3 viewPoint; varying float depth;
  uniform vec3 anchor;
  void main(){ vec4 p=modelViewMatrix*vec4(position,1.);
    viewPoint=p.xyz; depth=-p.z+(modelViewMatrix*vec4(anchor,1.)).z;
    gl_Position=projectionMatrix*p; }`;
const screenVertex = `varying vec2 uvScreen; void main(){uvScreen=uv;gl_Position=vec4(position.xy,0.,1.);}`;

export async function loadInjectionFlow(manifest: AnatomyManifest): Promise<FlowData> {
  const response=await fetch(`${import.meta.env.BASE_URL}anatomy/dsa-flow.json?v=${manifest.release}`);
  if(!response.ok)throw Error('Could not load injection courses');
  const flow: FlowData=await response.json();
  if(flow.schema!==1||flow.graphSource!==flowGraphSource(manifest)||Object.entries(flow.sourceHashes).some(([file,h])=>!manifest.assetRevisions?.[file]||!h.startsWith(manifest.assetRevisions[file])))throw Error('Injection courses do not match the anatomy');
  return flow;
}

/** Closed-surface ray-length integral, with no depth occlusion. The per-mesh
 * depth origin reduces floating-point cancellation, especially on half floats.
 * Ordinary atlas meshes/materials are never replaced or reparented. */
export class DsaRenderer {
  private scene = new THREE.Scene();
  private screen = new THREE.Scene();
  private camera = new THREE.Camera();
  private target: THREE.WebGLRenderTarget;
  private plane = new THREE.PlaneGeometry(2, 2);
  private shapes = new Map<string, THREE.Mesh<THREE.BufferGeometry, THREE.ShaderMaterial>>();
  private flowShapes = new Map<string,{start:number;end:number;mesh:THREE.Mesh<THREE.BufferGeometry,THREE.ShaderMaterial>}[]>();
  private transient: THREE.Mesh<THREE.BufferGeometry,THREE.ShaderMaterial>[]=[];
  private worker=new Worker(new URL('./dsaWorker.ts',import.meta.url),{type:'module'});
  private workerSurfaces=new Set<string>();
  private requests=new Map<number,{resolve:(sections:FlowSection[])=>void;reject:(error:Error)=>void}>();
  private request=0;
  private sectionRequests=new Map<string,Promise<FlowSection[]>>();
  private workerError:Error|null=null;
  private markers = new THREE.Scene();
  private markerGeometry = new THREE.SphereGeometry(1.1,12,8);
  private markerMaterial = new THREE.MeshBasicMaterial({color:0xffbc55,depthTest:false,depthWrite:false,toneMapped:false});
  private active: { mesh: THREE.Mesh<THREE.BufferGeometry, THREE.ShaderMaterial>; vessel: DsaVessel }[] = [];
  private run: DsaRun | null = null;
  private field: THREE.ShaderMaterial;
  private display: THREE.ShaderMaterial;
  private selected: string|null=null;
  private selectionTarget=new THREE.WebGLRenderTarget(1,1,{depthBuffer:false});
  private selectionScene=new THREE.Scene();
  private selectionMaterial=new THREE.MeshBasicMaterial({color:0xffffff,side:THREE.DoubleSide,depthTest:false,depthWrite:false,toneMapped:false});
  private selectionMasks=new WeakMap<THREE.Mesh,THREE.Mesh>();
  private quad: THREE.Mesh;
  private drawingSize = new THREE.Vector2();
  readonly precision: 'float' | 'half-float';

  static async create(renderer: THREE.WebGLRenderer, manifest: AnatomyManifest, geometry: Map<string, THREE.BufferGeometry>, flow: FlowData) {
    const base = `${import.meta.env.BASE_URL}anatomy/dsa-surfaces`;
    const response = await fetch(`${base}.json?v=${manifest.release}`);
    if (!response.ok) throw Error('Could not load DSA surfaces');
    const metadata: Surfaces = await response.json();
    if (metadata.schema !== 1 || Object.keys(metadata.sourceHashes).some(file => manifest.assetRevisions?.[file] !== metadata.assetRevisions[file])) throw Error('DSA surfaces do not match the anatomy');
    if(flow.schema!==1||flow.graphSource!==flowGraphSource(manifest)||Object.entries(flow.sourceHashes).some(([file,h])=>metadata.sourceHashes[file]!==h))throw Error('Injection courses do not match the anatomy');
    return new DsaRenderer(renderer, geometry, metadata,flow);
  }

  private constructor(private renderer: THREE.WebGLRenderer, private geometry: Map<string, THREE.BufferGeometry>, private surfaces: Surfaces,readonly flow: FlowData) {
    this.worker.onmessage=({data})=>{const pending=this.requests.get(data.request);if(!pending)return;this.requests.delete(data.request);if(data.error)pending.reject(Error(data.error));else pending.resolve(data.sections)};
    this.worker.onerror=()=>{this.workerError=Error('Could not prepare injection surfaces');for(const pending of this.requests.values())pending.reject(this.workerError);this.requests.clear()};
    if (!renderer.extensions.has('EXT_color_buffer_float')) throw Error('DSA requires floating-point WebGL rendering');
    this.precision = renderer.extensions.has('EXT_float_blend') ? 'float' : 'half-float';
    const filter = this.precision === 'float' && !renderer.extensions.has('OES_texture_float_linear') ? THREE.NearestFilter : THREE.LinearFilter;
    this.target = new THREE.WebGLRenderTarget(1, 1, { type: this.precision === 'float' ? THREE.FloatType : THREE.HalfFloatType, minFilter: filter, magFilter: filter, depthBuffer: false, stencilBuffer: false });
    this.field = new THREE.ShaderMaterial({
      uniforms: { centre: {value: new THREE.Vector3()}, radius: {value: new THREE.Vector3()}, eye: {value: new THREE.Vector3()}, inverseProjection: {value: new THREE.Matrix4()}, cameraWorld: {value: new THREE.Matrix4()}, density: {value: 0} },
      vertexShader: screenVertex,
      fragmentShader: `varying vec2 uvScreen; uniform vec3 centre,radius,eye; uniform mat4 inverseProjection,cameraWorld; uniform float density;
        void main(){vec4 p=inverseProjection*vec4(uvScreen*2.-1.,1.,1.);
          vec3 worldRay=normalize(mat3(cameraWorld)*(p.xyz/p.w));
          vec3 o=(eye-centre)/radius,d=worldRay/radius; float a=dot(d,d),b=dot(o,d);
          float h=1.-dot(o,o)+b*b/a;
          float signal=h>0. && -b/a>0. ? density*(4./3.)*pow(h,1.5)/sqrt(a) : 0.;
          gl_FragColor=vec4(signal,0.,0.,1.); }`,
      depthTest: false, depthWrite: false, transparent: true, blending: THREE.CustomBlending, blendSrc: THREE.OneFactor, blendDst: THREE.OneFactor, toneMapped: false,
    });
    this.display = new THREE.ShaderMaterial({
      uniforms: { image: {value: this.target.texture}, selection: {value:this.selectionTarget.texture}, outline: {value:0}, pixel: {value:new THREE.Vector2()} }, vertexShader: screenVertex,
      fragmentShader: `varying vec2 uvScreen; uniform sampler2D image,selection; uniform vec2 pixel; uniform float outline;
        void main(){float column=max(0.,texture2D(image,uvScreen).r);
          float grey=(176./255.)*exp(-.9*column); float edge=0.;
          if(outline>0.){
            float inside=step(.01,texture2D(selection,uvScreen).r),nearby=0.;
            for(int x=-1;x<=1;x++)for(int y=-1;y<=1;y++)nearby=max(nearby,texture2D(selection,uvScreen+vec2(float(x),float(y))*pixel).r);
            edge=(1.-inside)*nearby*.55;
          }
          gl_FragColor=vec4(mix(vec3(grey),vec3(1.,.65,.22),edge),1.);}`,
      depthTest: false, depthWrite: false, toneMapped: false,
    });
    this.quad = new THREE.Mesh(this.plane, this.display); this.quad.frustumCulled = false; this.screen.add(this.quad);
  }

  private surface(id: string) {
      let mesh = this.shapes.get(id);
      if (!mesh) {
        const original = this.geometry.get(id), row = this.surfaces.entries[id];
        if (!original || !row) throw Error(`Missing DSA surface: ${id}`);
        const p = original.getAttribute('position');
        if (p.count !== row.vertexCount) throw Error(`DSA surface changed: ${id}`);
        const geo = new THREE.BufferGeometry();
        if (row.extra.length) {
          const positions = new Float32Array((p.count + row.extra.length)*3);
          for (let i=0;i<p.count;i++) positions.set([p.getX(i),p.getY(i),p.getZ(i)],i*3);
          row.extra.forEach((v,i) => positions.set(v,(p.count+i)*3));
          geo.setAttribute('position',new THREE.BufferAttribute(positions,3));
        } else geo.setAttribute('position',p);
        const source = original.getIndex()!, removed = new Set(row.removed), flips = new Set(row.flips);
        const indices = new Uint32Array((source.count/3-removed.size)*3+row.caps.length);
        let at = 0;
        for (let i=0;i<source.count/3;i++) if (!removed.has(i)) {
          const a=source.getX(i*3), b=source.getX(i*3+1), c=source.getX(i*3+2);
          indices.set(row.reverse !== flips.has(i) ? [a,c,b] : [a,b,c],at); at+=3;
        }
        indices.set(row.caps,at);
        if (indices.length !== row.faces*3) throw Error(`Invalid DSA recipe: ${id}`);
        geo.setIndex(new THREE.BufferAttribute(indices,1)); geo.computeBoundingBox(); geo.computeBoundingSphere();
        const material = new THREE.ShaderMaterial({
          uniforms: { concentration: {value: 0}, anchor: {value: geo.boundingBox!.getCenter(new THREE.Vector3())} }, vertexShader: vertex,
          fragmentShader: `varying vec3 viewPoint; varying float depth; uniform float concentration;
            void main(){float lengthAlongRay=depth*length(viewPoint)/max(.001,abs(viewPoint.z));
              gl_FragColor=vec4((gl_FrontFacing ? -1. : 1.)*lengthAlongRay*concentration,0.,0.,1.);}`,
          side: THREE.DoubleSide, forceSinglePass: true, depthTest: false, depthWrite: false,
          transparent: true, blending: THREE.CustomBlending, blendSrc: THREE.OneFactor, blendDst: THREE.OneFactor, toneMapped: false,
        });
        mesh = new THREE.Mesh(geo,material); this.shapes.set(id,mesh);
      }
    return mesh;
  }

  injectionPoint(id: string, clicked: number[]): InjectionPoint {
    const row=this.flow.entries[id];if(!row?.selectable)throw Error('No validated injection course');
    const geometry=this.surface(id).geometry,p=geometry.getAttribute('position'),positions=new Float32Array(p.count*3);
    for(let i=0;i<p.count;i++)positions.set([p.getX(i),p.getY(i),p.getZ(i)],i*3);
    const index=new Uint32Array(geometry.index!.array),tip=injectionOnPath(row,clicked);
    if(pointInsideSurface(positions,index,tip.point))return {id,...tip};
    // A final check at the chosen position guards unsampled tiny surface
    // irregularities. Snap to the nearest verified guide position if needed.
    for(const distance of [...row.arc].sort((a,b)=>Math.abs(a-tip.distance)-Math.abs(b-tip.distance))) {
      const candidate=injectionOnPath(row,pathPoint(row,distance));
      if(pointInsideSurface(positions,index,candidate.point))return {id,...candidate};
    }
    throw Error('No interior injection position on this artery');
  }

  private split(id:string,inlet:number):Promise<FlowSection[]> {
    if(this.workerError)return Promise.reject(this.workerError);
    const key=`${id}@${inlet}`,existing=this.sectionRequests.get(key);if(existing)return existing;
    const result=new Promise<FlowSection[]>((resolve,reject)=>{
      let surface;const transfer:Transferable[]=[];
      if(!this.workerSurfaces.has(id)){
        const geo=this.surface(id).geometry,p=geo.getAttribute('position'),positions=new Float32Array(p.count*3),indices=new Uint32Array(geo.index!.array);
        for(let i=0;i<p.count;i++)positions.set([p.getX(i),p.getY(i),p.getZ(i)],i*3);
        surface={positions,indices,row:this.flow.entries[id]};transfer.push(positions.buffer,indices.buffer);this.workerSurfaces.add(id);
      }
      const request=++this.request;this.requests.set(request,{resolve,reject});this.worker.postMessage({request,id,inlet,surface},transfer);
    }).finally(()=>this.sectionRequests.delete(key));
    this.sectionRequests.set(key,result);return result;
  }

  async setRun(run: DsaRun,valid=()=>true,warm=false) {
    const active:typeof this.active=[],transient:typeof this.transient=[];
    try{
    for (const vessel of run.vessels) {
      if(!valid())break;
      const mesh = this.surface(vessel.id);
      const row=this.flow.entries[vessel.id],travel=run.travel?.get(vessel.id);
      if(!vessel.vein && row?.selectable && travel) {
        let sections=travel.start===0?this.flowShapes.get(vessel.id):undefined;
        if(!sections&&travel.start===0&&row.length<=18)sections=[{start:0,end:row.length,mesh}];
        if(!sections) {
          const split=await this.split(vessel.id,travel.start);
          sections=travel.start===0?this.flowShapes.get(vessel.id):undefined;
          sections??=split.map(s=>{
            const geo=new THREE.BufferGeometry();geo.setAttribute('position',new THREE.BufferAttribute(s.positions,3));geo.setIndex(new THREE.BufferAttribute(s.indices,1));geo.computeBoundingBox();geo.computeBoundingSphere();
            const material=mesh!.material.clone();material.uniforms.anchor.value=geo.boundingBox!.getCenter(new THREE.Vector3());
            const part=new THREE.Mesh(geo,material);if(travel.start>0)transient.push(part);
            return {start:s.start,end:s.end,mesh:part};
          });
        }
        if(travel.start===0)this.flowShapes.set(vessel.id,sections);
        for(const section of sections)active.push({mesh:section.mesh,vessel:{...vessel,delay:Math.min(1,(travel.distance+section.start-travel.start)/350)}});
      }else active.push({mesh,vessel});
    }
    if(warm||!valid()){for(const mesh of transient){mesh.geometry.dispose();mesh.material.dispose()}return false}
    }catch(error){for(const mesh of transient){mesh.geometry.dispose();mesh.material.dispose()}throw error}
    for(const mesh of this.transient){mesh.geometry.dispose();mesh.material.dispose()}this.transient=transient;
    this.run=run;this.selected=null;this.selectionScene.clear();this.scene.clear();this.active=active;
    for(const {mesh} of active)this.scene.add(mesh);
    this.markers.clear();for(const inlet of run.inlets??[]){const marker=new THREE.Mesh(this.markerGeometry,this.markerMaterial);marker.position.fromArray(inlet.point);this.markers.add(marker)}
    return true;
  }

  setSelected(id: string|null) { this.selected=id; }

  /** Use exactly the closed sections contributing contrast to this frame. */
  pick(raycaster: THREE.Raycaster,time: number): string|null {
    const eligible=this.active.filter(({vessel})=>dsaConcentration(vessel,time)>.0001);
    const ids=new Map<THREE.Object3D,string>(eligible.map(({mesh,vessel})=>[mesh,vessel.id]));
    for(const {mesh} of eligible)mesh.updateMatrixWorld(true);
    const hit=raycaster.intersectObjects(eligible.map(v=>v.mesh),false)[0];
    return hit?ids.get(hit.object)??null:null;
  }

  render(camera: THREE.PerspectiveCamera, time: number) {
    const {renderer} = this; renderer.getDrawingBufferSize(this.drawingSize);
    const scale = Math.min(1.5,1500/Math.max(this.drawingSize.x,this.drawingSize.y));
    const w = Math.max(1,Math.round(this.drawingSize.x*scale)), h = Math.max(1,Math.round(this.drawingSize.y*scale));
    if (this.target.width !== w || this.target.height !== h) this.target.setSize(w,h);
    for (const {mesh,vessel} of this.active) {
      const c = dsaConcentration(vessel,time); mesh.visible = c > .0001; mesh.material.uniforms.concentration.value = c;
    }
    const savedTarget = renderer.getRenderTarget(), savedClear = renderer.getClearColor(new THREE.Color()), savedAlpha = renderer.getClearAlpha(), autoClear = renderer.autoClear;
    renderer.setClearColor(0,0); renderer.autoClear = false;
    try {
      renderer.setRenderTarget(this.target); renderer.clear(); renderer.render(this.scene,camera);
      const density = dsaBlushConcentration(time)*.08;
      if (density && this.run) {
        camera.updateMatrixWorld(); this.quad.material = this.field;
        this.field.uniforms.eye.value.copy(camera.position);
        this.field.uniforms.inverseProjection.value.copy(camera.projectionMatrixInverse);
        this.field.uniforms.cameraWorld.value.copy(camera.matrixWorld);
        this.field.uniforms.density.value = density;
        for (const blush of this.run.blush) {
          this.field.uniforms.centre.value.fromArray(blush.centre); this.field.uniforms.radius.value.fromArray(blush.radius);
          renderer.render(this.screen,this.camera);
        }
      }
      this.display.uniforms.outline.value=this.selected?1:0;
      if(this.selected){
        if(this.selectionTarget.width!==w||this.selectionTarget.height!==h)this.selectionTarget.setSize(w,h);
        this.selectionScene.clear();
        for(const {mesh,vessel} of this.active)if(vessel.id===this.selected&&mesh.visible){
          let mask=this.selectionMasks.get(mesh);
          if(!mask){mask=new THREE.Mesh(mesh.geometry,this.selectionMaterial);mask.matrixAutoUpdate=false;this.selectionMasks.set(mesh,mask)}
          mesh.updateMatrixWorld(true);mask.matrix.copy(mesh.matrixWorld);this.selectionScene.add(mask);
        }
        renderer.setRenderTarget(this.selectionTarget);renderer.clear();renderer.render(this.selectionScene,camera);
        const pixels=1.25*renderer.getPixelRatio()*scale;this.display.uniforms.pixel.value.set(pixels/w,pixels/h);
      }
      this.quad.material = this.display; renderer.setRenderTarget(savedTarget); renderer.render(this.screen,this.camera);
      renderer.render(this.markers,camera);
    } finally { renderer.setRenderTarget(savedTarget); renderer.setClearColor(savedClear,savedAlpha); renderer.autoClear = autoClear; }
  }

  dispose() {
    this.worker.terminate();for(const pending of this.requests.values())pending.reject(Error('Atlas closed'));this.requests.clear();
    const originals=new Set(this.shapes.values());
    for(const section of [...this.flowShapes.values()].flat())if(!originals.has(section.mesh)){section.mesh.geometry.dispose();section.mesh.material.dispose()}
    for(const mesh of this.transient){mesh.geometry.dispose();mesh.material.dispose()}
    this.markerGeometry.dispose();this.markerMaterial.dispose();
    for (const mesh of this.shapes.values()) { mesh.geometry.dispose(); mesh.material.dispose(); }
    this.selectionScene.clear();this.selectionTarget.dispose();this.selectionMaterial.dispose();
    this.shapes.clear(); this.target.dispose(); this.field.dispose(); this.display.dispose(); this.plane.dispose();
  }
}
