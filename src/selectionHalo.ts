import * as THREE from 'three';

export function selectionHaloFade(elapsed: number): number {
  return 0.15 + 0.85 * (0.5 - 0.5 * Math.cos(elapsed * Math.PI * 2 / 6000));
}

const quadVertex = `
  varying vec2 vUv;
  void main() {
    vUv = uv;
    gl_Position = vec4(position.xy, 0.0, 1.0);
  }
`;

/** Selected silhouette only, with a Gaussian halo extending 24 CSS pixels. */
export class SelectionHalo {
  private sceneTarget = new THREE.WebGLRenderTarget(1, 1);
  private maskTarget = new THREE.WebGLRenderTarget(1, 1, { depthBuffer: false });
  private blurTargets = [0, 1].map(() => new THREE.WebGLRenderTarget(1, 1, { depthBuffer: false }));
  private maskScene = new THREE.Scene();
  private sources: THREE.Mesh[] = [];
  private masks: THREE.Mesh[] = [];
  private maskMaterial = new THREE.ShaderMaterial({
    uniforms: {
      sceneDepth: { value: null },
      resolution: { value: new THREE.Vector2(1, 1) },
      cameraNear: { value: 0.01 }, cameraFar: { value: 1000 },
    },
    vertexShader: `
      #include <clipping_planes_pars_vertex>
      void main() {
        vec4 mvPosition = modelViewMatrix * vec4(position, 1.0);
        gl_Position = projectionMatrix * mvPosition;
        #include <clipping_planes_vertex>
      }
    `,
    fragmentShader: `
      uniform sampler2D sceneDepth;
      uniform vec2 resolution;
      uniform float cameraNear;
      uniform float cameraFar;
      #include <clipping_planes_pars_fragment>
      float viewDistance(float depth) {
        return cameraNear * cameraFar / (cameraFar - depth * (cameraFar - cameraNear));
      }
      void main() {
        #include <clipping_planes_fragment>
        float sceneZ = viewDistance(texture2D(sceneDepth, gl_FragCoord.xy / resolution).r);
        float selectedZ = viewDistance(gl_FragCoord.z);
        if (selectedZ > sceneZ + max(0.002, sceneZ * 0.00002)) discard;
        gl_FragColor = vec4(1.0);
      }
    `,
    side: THREE.DoubleSide, depthTest: false, depthWrite: false,
    clipping: true, toneMapped: false,
  });
  private blurMaterial = new THREE.ShaderMaterial({
    uniforms: { image: { value: null }, stepSize: { value: new THREE.Vector2() } },
    vertexShader: quadVertex,
    fragmentShader: `
      uniform sampler2D image;
      uniform vec2 stepSize;
      varying vec2 vUv;
      void main() {
        float sum = 0.0;
        float total = 0.0;
        for (int i = -12; i <= 12; i++) {
          float offset = float(i);
          float weight = exp(-0.5 * offset * offset / 16.0);
          vec2 sampleUv = vUv + stepSize * offset;
          float inside = step(0.0, sampleUv.x) * step(sampleUv.x, 1.0)
                       * step(0.0, sampleUv.y) * step(sampleUv.y, 1.0);
          sum += texture2D(image, sampleUv).r * weight * inside;
          total += weight;
        }
        gl_FragColor = vec4(vec3(sum / total), 1.0);
      }
    `,
    depthTest: false, depthWrite: false, toneMapped: false,
  });
  private compositeMaterial = new THREE.ShaderMaterial({
    uniforms: {
      sceneImage: { value: null }, maskImage: { value: null }, haloImage: { value: null },
      colour: { value: new THREE.Color() }, strength: { value: 0.195 },
    },
    vertexShader: quadVertex,
    fragmentShader: `
      uniform sampler2D sceneImage;
      uniform sampler2D maskImage;
      uniform sampler2D haloImage;
      uniform vec3 colour;
      uniform float strength;
      varying vec2 vUv;
      void main() {
        vec4 sceneColour = texture2D(sceneImage, vUv);
        float outside = 1.0 - step(0.001, texture2D(maskImage, vUv).r);
        float halo = texture2D(haloImage, vUv).r * outside * strength;
        gl_FragColor = vec4(sceneColour.rgb + colour * halo, sceneColour.a);
        #include <colorspace_fragment>
      }
    `,
    depthTest: false, depthWrite: false, toneMapped: false,
  });
  private quad = new THREE.Mesh(new THREE.PlaneGeometry(2, 2), this.blurMaterial);
  private quadScene = new THREE.Scene();
  private quadCamera = new THREE.Camera();
  private savedColour = new THREE.Color();
  private horizontalStep = new THREE.Vector2();
  private verticalStep = new THREE.Vector2();

  constructor(private renderer: THREE.WebGLRenderer, colour: THREE.Color) {
    this.sceneTarget.depthTexture = new THREE.DepthTexture(1, 1, THREE.UnsignedIntType);
    this.sceneTarget.samples = Math.min(4, renderer.capabilities.maxSamples);
    this.maskTarget.texture.minFilter = this.maskTarget.texture.magFilter = THREE.NearestFilter;
    this.compositeMaterial.uniforms.colour.value.copy(colour);
    this.maskMaterial.uniforms.sceneDepth.value = this.sceneTarget.depthTexture;
    this.compositeMaterial.uniforms.sceneImage.value = this.sceneTarget.texture;
    this.compositeMaterial.uniforms.maskImage.value = this.maskTarget.texture;
    this.compositeMaterial.uniforms.haloImage.value = this.blurTargets[1].texture;
    this.quad.frustumCulled = false;
    this.quadScene.add(this.quad);
  }

  get active() { return this.sources.length > 0; }

  setMeshes(sources: THREE.Mesh[]) {
    this.sources = sources;
    this.maskScene.clear();
    this.masks = sources.map(source => {
      const mask = new THREE.Mesh(source.geometry, this.maskMaterial);
      mask.matrixAutoUpdate = false;
      mask.frustumCulled = false;
      this.maskScene.add(mask);
      return mask;
    });
  }

  setClip(planes: THREE.Plane[]) {
    if ((this.maskMaterial.clippingPlanes?.length ?? 0) !== planes.length) this.maskMaterial.needsUpdate = true;
    this.maskMaterial.clippingPlanes = planes;
  }

  setFade(fade: number) { this.compositeMaterial.uniforms.strength.value = 1.3 * fade; }

  resize(width: number, height: number) {
    const ratio = this.renderer.getPixelRatio();
    const physicalWidth = Math.max(1, Math.floor(width * ratio));
    const physicalHeight = Math.max(1, Math.floor(height * ratio));
    this.sceneTarget.setSize(physicalWidth, physicalHeight);
    this.maskTarget.setSize(physicalWidth, physicalHeight);
    this.maskMaterial.uniforms.resolution.value.set(physicalWidth, physicalHeight);
    // Blur at half CSS resolution. Each kernel step spans two CSS pixels,
    // keeping the falloff independent of camera zoom and device pixel ratio.
    const blurWidth = Math.max(1, Math.ceil(width / 2));
    const blurHeight = Math.max(1, Math.ceil(height / 2));
    for (const target of this.blurTargets) target.setSize(blurWidth, blurHeight);
    this.horizontalStep.set(2 / width, 0);
    this.verticalStep.set(0, 2 / height);
  }

  render(scene: THREE.Scene, camera: THREE.PerspectiveCamera) {
    if (!this.active) { this.renderer.render(scene, camera); return; }
    const renderer = this.renderer;
    renderer.getClearColor(this.savedColour);
    const savedAlpha = renderer.getClearAlpha();
    renderer.setRenderTarget(this.sceneTarget);
    renderer.render(scene, camera);
    this.sources.forEach((source, i) => {
      this.masks[i].matrix.copy(source.matrixWorld);
      this.masks[i].matrixWorldNeedsUpdate = true;
    });
    this.maskMaterial.uniforms.cameraNear.value = camera.near;
    this.maskMaterial.uniforms.cameraFar.value = camera.far;
    renderer.setClearColor(0x000000, 0);
    renderer.setRenderTarget(this.maskTarget);
    renderer.render(this.maskScene, camera);
    this.quad.material = this.blurMaterial;
    this.blurMaterial.uniforms.image.value = this.maskTarget.texture;
    this.blurMaterial.uniforms.stepSize.value.copy(this.horizontalStep);
    renderer.setRenderTarget(this.blurTargets[0]);
    renderer.render(this.quadScene, this.quadCamera);
    this.blurMaterial.uniforms.image.value = this.blurTargets[0].texture;
    this.blurMaterial.uniforms.stepSize.value.copy(this.verticalStep);
    renderer.setRenderTarget(this.blurTargets[1]);
    renderer.render(this.quadScene, this.quadCamera);
    renderer.setClearColor(this.savedColour, savedAlpha);
    renderer.setRenderTarget(null);
    this.quad.material = this.compositeMaterial;
    renderer.render(this.quadScene, this.quadCamera);
  }

  dispose() {
    this.setMeshes([]);
    this.sceneTarget.dispose();
    this.maskTarget.dispose();
    for (const target of this.blurTargets) target.dispose();
    this.maskMaterial.dispose(); this.blurMaterial.dispose(); this.compositeMaterial.dispose();
    this.quad.geometry.dispose();
  }
}
