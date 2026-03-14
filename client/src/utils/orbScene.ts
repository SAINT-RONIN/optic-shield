import * as THREE from 'three'

export type OrbState = 'idle' | 'thinking' | 'analyzing' | 'alert' | 'complete'

const TEAL = new THREE.Color(0x00C9A7)
const PURPLE = new THREE.Color(0x7C5CFC)
const MAGENTA = new THREE.Color(0xF04E98)

interface OrbConfig {
  rotationSpeed: number
  wireframeOpacity: number
  glowIntensity: number
  wobbleX: boolean
}

const STATE_CONFIGS: Record<OrbState, OrbConfig> = {
  idle: { rotationSpeed: 0.003, wireframeOpacity: 0.2, glowIntensity: 0, wobbleX: false },
  thinking: { rotationSpeed: 0.008, wireframeOpacity: 0.3, glowIntensity: 0.15, wobbleX: false },
  analyzing: { rotationSpeed: 0.012, wireframeOpacity: 0.4, glowIntensity: 0.25, wobbleX: true },
  alert: { rotationSpeed: 0.003, wireframeOpacity: 0.2, glowIntensity: 0.3, wobbleX: false },
  complete: { rotationSpeed: 0.003, wireframeOpacity: 0.2, glowIntensity: 0.1, wobbleX: false },
}

export class OrbScene {
  private renderer: THREE.WebGLRenderer
  private scene: THREE.Scene
  private camera: THREE.PerspectiveCamera
  private sphere: THREE.Mesh
  private wireframe: THREE.LineSegments
  private sphereMaterial: THREE.MeshPhysicalMaterial
  private wireframeMaterial: THREE.LineBasicMaterial
  private animationId: number = 0
  private state: OrbState = 'idle'
  private clock = new THREE.Clock()
  private alertTime: number = 0
  private completeTime: number = 0
  private particles: THREE.Points | null = null

  constructor(container: HTMLElement) {
    const width = container.clientWidth
    const height = container.clientHeight

    this.renderer = new THREE.WebGLRenderer({ alpha: true, antialias: true })
    this.renderer.setSize(width, height)
    this.renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2))
    container.appendChild(this.renderer.domElement)

    this.scene = new THREE.Scene()
    this.camera = new THREE.PerspectiveCamera(45, width / height, 0.1, 100)
    this.camera.position.z = 3

    const ambient = new THREE.AmbientLight(0xffffff, 0.4)
    this.scene.add(ambient)
    const directional = new THREE.DirectionalLight(0xffffff, 0.8)
    directional.position.set(-2, 3, 2)
    this.scene.add(directional)

    const geometry = new THREE.SphereGeometry(1, 64, 64)
    this.sphereMaterial = new THREE.MeshPhysicalMaterial({
      color: PURPLE,
      emissive: TEAL,
      emissiveIntensity: 0.15,
      transparent: true,
      opacity: 0.7,
      roughness: 0.2,
      metalness: 0.1,
      clearcoat: 1.0,
      clearcoatRoughness: 0.1,
    })
    this.sphere = new THREE.Mesh(geometry, this.sphereMaterial)
    this.scene.add(this.sphere)

    const wireGeo = new THREE.SphereGeometry(1.02, 32, 32)
    const edgesGeo = new THREE.EdgesGeometry(wireGeo)
    this.wireframeMaterial = new THREE.LineBasicMaterial({
      color: 0xffffff,
      transparent: true,
      opacity: 0.2,
    })
    this.wireframe = new THREE.LineSegments(edgesGeo, this.wireframeMaterial)
    this.scene.add(this.wireframe)

    this.createParticles()
    this.animate()
  }

  private createParticles(): void {
    const count = 25
    const positions = new Float32Array(count * 3)
    for (let i = 0; i < count; i++) {
      const theta = Math.random() * Math.PI * 2
      const phi = Math.random() * Math.PI
      const r = 1.3 + Math.random() * 0.4
      positions[i * 3] = r * Math.sin(phi) * Math.cos(theta)
      positions[i * 3 + 1] = r * Math.sin(phi) * Math.sin(theta)
      positions[i * 3 + 2] = r * Math.cos(phi)
    }
    const geo = new THREE.BufferGeometry()
    geo.setAttribute('position', new THREE.BufferAttribute(positions, 3))
    const mat = new THREE.PointsMaterial({
      color: 0xC77DFF,
      size: 0.04,
      transparent: true,
      opacity: 0,
    })
    this.particles = new THREE.Points(geo, mat)
    this.scene.add(this.particles)
  }

  setState(newState: OrbState): void {
    if (newState === 'alert' && this.state !== 'alert') {
      this.alertTime = this.clock.getElapsedTime()
    }
    if (newState === 'complete' && this.state !== 'complete') {
      this.completeTime = this.clock.getElapsedTime()
    }
    this.state = newState
  }

  private animate = (): void => {
    this.animationId = requestAnimationFrame(this.animate)
    const t = this.clock.getElapsedTime()
    const config = STATE_CONFIGS[this.state]

    this.sphere.rotation.y += config.rotationSpeed
    this.wireframe.rotation.y += config.rotationSpeed
    if (config.wobbleX) {
      this.sphere.rotation.x = Math.sin(t * 0.5) * 0.05
      this.wireframe.rotation.x = this.sphere.rotation.x
    }

    const breathe = 1.0 + Math.sin(t * (this.state === 'thinking' ? 2 : 1.5)) * 0.02
    this.sphere.scale.setScalar(breathe)
    this.wireframe.scale.setScalar(breathe * 1.02)

    if (this.state === 'thinking') {
      this.wireframeMaterial.opacity = 0.2 + Math.sin(t * 4) * 0.1
    } else {
      this.wireframeMaterial.opacity = config.wireframeOpacity
    }

    if (this.particles) {
      const particleMat = this.particles.material as THREE.PointsMaterial
      particleMat.opacity = this.state === 'analyzing' ? 0.6 : 0
      if (this.state === 'analyzing') {
        this.particles.rotation.y += 0.005
        this.particles.rotation.x += 0.002
      }
    }

    this.updateEmissive(t, config)
    this.renderer.render(this.scene, this.camera)
  }

  private updateEmissive(t: number, config: OrbConfig): void {
    if (this.state === 'alert') {
      const elapsed = t - this.alertTime
      if (elapsed < 0.5) {
        const flash = Math.sin(elapsed * Math.PI / 0.5)
        this.sphereMaterial.emissive.lerpColors(TEAL, MAGENTA, flash)
        this.sphereMaterial.emissiveIntensity = 0.15 + flash * 0.3
      } else {
        this.sphereMaterial.emissive.copy(TEAL)
        this.sphereMaterial.emissiveIntensity = 0.15
      }
      return
    }

    if (this.state === 'complete') {
      const elapsed = t - this.completeTime
      if (elapsed < 0.4) {
        const pulse = Math.sin(elapsed * Math.PI / 0.4)
        this.sphere.scale.setScalar(1.0 + pulse * 0.08)
        this.sphereMaterial.emissive.lerpColors(PURPLE, TEAL, pulse)
        this.sphereMaterial.emissiveIntensity = 0.15 + pulse * 0.4
      } else {
        this.sphereMaterial.emissive.copy(TEAL)
        this.sphereMaterial.emissiveIntensity = 0.15
      }
      return
    }

    this.sphereMaterial.emissive.copy(TEAL)
    this.sphereMaterial.emissiveIntensity = 0.15 + config.glowIntensity
  }

  resize(width: number, height: number): void {
    this.camera.aspect = width / height
    this.camera.updateProjectionMatrix()
    this.renderer.setSize(width, height)
  }

  dispose(): void {
    cancelAnimationFrame(this.animationId)
    this.renderer.dispose()
    this.scene.clear()
    this.renderer.domElement.remove()
  }
}
