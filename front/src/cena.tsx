// Cena do hero da home: um núcleo de metal dourado líquido com poeira dourada em
// volta, sobre o palco preto. Ela não decide nada sozinha: a cada quadro lê o
// progresso da rolagem que static/js/cinema.js publica (ver estado.ts). Nenhum
// texto mora aqui; título, botões e SEO ficam no HTML do Jinja.
import { MeshDistortMaterial, PerformanceMonitor } from '@react-three/drei'
import { Canvas, useFrame, useThree } from '@react-three/fiber'
import { easing } from 'maath'
import { StrictMode, useEffect, useMemo, useRef, useState, type ComponentRef } from 'react'
import { createRoot } from 'react-dom/client'
import * as THREE from 'three'
import { lerEstado, type OpcoesCinema } from './estado'
import { cores } from './tokens'

type MaterialDistorcido = ComponentRef<typeof MeshDistortMaterial>

// Pseudoaleatório com semente: as brasas nascem sempre no mesmo lugar, então o pôster
// (static/imagens/cinema-poster-*.webp) bate com a cena quando ela assume.
function sementeAleatoria(semente: number) {
  return () => {
    semente = (semente + 0x6d2b79f5) | 0
    let t = Math.imul(semente ^ (semente >>> 15), 1 | semente)
    t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296
  }
}

// Mancha radial macia, branca: vira o halo atrás do núcleo (a cor vem do material).
function criarTexturaHalo() {
  const tela = document.createElement('canvas')
  tela.width = tela.height = 128
  const contexto = tela.getContext('2d')!
  const brilho = contexto.createRadialGradient(64, 64, 0, 64, 64, 64)
  brilho.addColorStop(0, 'rgba(255,255,255,1)')
  brilho.addColorStop(0.35, 'rgba(255,255,255,0.35)')
  brilho.addColorStop(1, 'rgba(255,255,255,0)')
  contexto.fillStyle = brilho
  contexto.fillRect(0, 0, 128, 128)
  const textura = new THREE.CanvasTexture(tela)
  textura.colorSpace = THREE.SRGBColorSpace
  return textura
}

// Impulso de 0 a ~0,4 e de volta a 0 em 0,9 s a cada troca de manchete: o "golpe"
// que o núcleo leva e que espalha a poeira.
function useGolpe() {
  const golpe = useRef({ indice: 0, inicio: -10 })
  return (indice: number, agora: number) => {
    if (indice !== golpe.current.indice) golpe.current = { indice, inicio: agora }
    const t = (agora - golpe.current.inicio) / 0.9
    return t >= 0 && t < 1 ? Math.sin(t * Math.PI) * (1 - t) : 0
  }
}

// Brasas que sobem do metal: cada uma com velocidade, tamanho e fase próprios, num
// único <points> com shader (uma chamada de desenho para todas). O deslocamento é
// acumulado na CPU (uDeslocamento), então acelerar com a rolagem não dá salto.
const ALTURA_BRASAS = 5.6

const verticeBrasas = /* glsl */ `
  uniform float uDeslocamento;
  uniform float uTempo;
  uniform float uEscalaPixel;
  attribute float aVelocidade;
  attribute float aTamanho;
  attribute float aFase;
  varying float vBrilho;
  void main() {
    vec3 p = position;
    float metade = ${(ALTURA_BRASAS / 2).toFixed(2)};
    p.y = mod(p.y + metade + uDeslocamento * aVelocidade, ${ALTURA_BRASAS.toFixed(2)}) - metade;
    p.x += sin(uTempo * 0.7 + aFase) * 0.14;
    p.z += cos(uTempo * 0.5 + aFase * 1.3) * 0.14;
    vec4 posicaoVista = modelViewMatrix * vec4(p, 1.0);
    gl_Position = projectionMatrix * posicaoVista;
    gl_PointSize = aTamanho * uEscalaPixel / -posicaoVista.z;
    // Aparece embaixo e some em cima (sem estalo na volta) e cintila devagar.
    float borda = smoothstep(-metade, -metade + 0.9, p.y) * (1.0 - smoothstep(metade - 1.4, metade, p.y));
    vBrilho = borda * (0.55 + 0.45 * sin(uTempo * 1.7 + aFase * 6.0));
  }
`

const fragmentoBrasas = /* glsl */ `
  uniform vec3 uCor;
  varying float vBrilho;
  void main() {
    float distancia = length(gl_PointCoord - 0.5);
    float alfa = pow(smoothstep(0.5, 0.0, distancia), 1.6) * vBrilho;
    gl_FragColor = vec4(uCor * (1.0 + alfa), alfa);
    #include <colorspace_fragment>
  }
`

type PropsBrasas = { quantidade: number; espalhamento: number; semente: number; energia: { current: number } }

function Brasas({ quantidade, espalhamento, semente, energia }: PropsBrasas) {
  const material = useRef<THREE.ShaderMaterial>(null!)
  const uniformes = useMemo(
    () => ({
      uDeslocamento: { value: 0 },
      uTempo: { value: 0 },
      uEscalaPixel: { value: 400 },
      uCor: { value: new THREE.Color(cores.ouroClaro) },
    }),
    [],
  )
  const atributos = useMemo(() => {
    const aleatorio = sementeAleatoria(semente)
    const posicoes = new Float32Array(quantidade * 3)
    const velocidades = new Float32Array(quantidade)
    const tamanhos = new Float32Array(quantidade)
    const fases = new Float32Array(quantidade)
    for (let i = 0; i < quantidade; i++) {
      // Coluna larga em volta do núcleo, mais densa perto do eixo.
      const raio = 0.4 + espalhamento * Math.pow(aleatorio(), 0.8)
      const angulo = aleatorio() * Math.PI * 2
      posicoes.set(
        [Math.cos(angulo) * raio, (aleatorio() - 0.5) * ALTURA_BRASAS, Math.sin(angulo) * raio * 0.6],
        i * 3,
      )
      velocidades[i] = 0.12 + aleatorio() * 0.38
      // Quase todas pequenas; uma em cada doze é uma brasa grande e desfocada.
      tamanhos[i] = aleatorio() < 0.08 ? 0.22 + aleatorio() * 0.18 : 0.035 + aleatorio() * 0.06
      fases[i] = aleatorio() * Math.PI * 2
    }
    return { posicoes, velocidades, tamanhos, fases }
  }, [quantidade, espalhamento, semente])

  useFrame((state, delta) => {
    const u = material.current.uniforms
    u.uTempo.value = state.clock.elapsedTime
    u.uDeslocamento.value += delta * (0.5 + energia.current)
    u.uEscalaPixel.value = state.size.height * state.viewport.dpr * 0.5
  })

  return (
    <points frustumCulled={false}>
      <bufferGeometry>
        <bufferAttribute attach="attributes-position" args={[atributos.posicoes, 3]} />
        <bufferAttribute attach="attributes-aVelocidade" args={[atributos.velocidades, 1]} />
        <bufferAttribute attach="attributes-aTamanho" args={[atributos.tamanhos, 1]} />
        <bufferAttribute attach="attributes-aFase" args={[atributos.fases, 1]} />
      </bufferGeometry>
      <shaderMaterial
        ref={material}
        uniforms={uniformes}
        vertexShader={verticeBrasas}
        fragmentShader={fragmentoBrasas}
        transparent
        depthWrite={false}
        blending={THREE.AdditiveBlending}
      />
    </points>
  )
}

// Brilho dourado atrás do núcleo: um sprite (sempre de frente para a câmera).
function Halo({ escala }: { escala: number }) {
  const textura = useMemo(criarTexturaHalo, [])
  useEffect(() => () => textura.dispose(), [textura])
  return (
    <sprite scale={[escala, escala, 1]} position={[0, 0, -1.2]}>
      <spriteMaterial
        map={textura}
        color={cores.ouro}
        transparent
        opacity={0.18}
        depthWrite={false}
        blending={THREE.AdditiveBlending}
        toneMapped={false}
      />
    </sprite>
  )
}

// Cor do metal: um terço do caminho entre o ouro e o ouro claro da marca. O ouro puro,
// refletindo o céu dourado, puxava para o âmbar.
const COR_METAL = new THREE.Color(cores.ouro).lerp(new THREE.Color(cores.ouroClaro), 0.35)

function Conjunto({ estreito }: { estreito: boolean }) {
  const conjunto = useRef<THREE.Group>(null!)
  const nucleo = useRef<THREE.Mesh>(null!)
  const material = useRef<MaterialDistorcido>(null!)
  const energia = useRef(0)
  const golpe = useGolpe()

  useFrame((state, delta) => {
    const { progresso: p, indice } = lerEstado()
    const impulso = golpe(indice, state.clock.elapsedTime)
    const arco = Math.sin(p * Math.PI) // 0 no começo e no fim, 1 no meio do hero

    // Desktop: sempre à direita do título, sem invadir a coluna do texto.
    // Celular: embaixo, atrás do texto, subindo um pouco ao longo do hero.
    const alvo: [number, number, number] = estreito
      ? [0, -1.25 + 0.3 * p, 0]
      : [2.05 - 0.3 * p, -0.05 - 0.1 * p, 0]
    easing.damp3(conjunto.current.position, alvo, 0.35, delta)

    const escala = estreito ? 0.7 * (1 + 0.04 * arco + 0.08 * impulso) : 1 + 0.12 * arco + 0.1 * impulso
    easing.damp3(nucleo.current.scale, [escala, escala, escala], 0.15, delta)
    easing.dampE(
      nucleo.current.rotation,
      [0.6 * p - 0.15 * state.pointer.y, 1.5 * Math.PI * p + 0.25 * state.pointer.x, 0],
      0.45,
      delta,
    )
    easing.damp(material.current, 'distort', 0.3 + 0.15 * arco + 0.25 * impulso, 0.2, delta)

    // As brasas sobem mais rápido no meio do hero e disparam a cada golpe.
    energia.current = 0.6 * arco + 2.2 * impulso
  })

  const segmentos = estreito ? 72 : 112
  return (
    <group ref={conjunto} position={estreito ? [0, -1.25, 0] : [2.05, -0.05, 0]}>
      <Halo escala={estreito ? 4 : 5.2} />
      <mesh ref={nucleo}>
        <sphereGeometry args={[1.1, segmentos, segmentos]} />
        <MeshDistortMaterial
          ref={material}
          color={COR_METAL}
          metalness={1}
          roughness={0.2}
          distort={0.3}
          speed={1.1}
        />
      </mesh>
      <Brasas
        quantidade={estreito ? 160 : 380}
        espalhamento={estreito ? 1.8 : 2.8}
        semente={7}
        energia={energia}
      />
    </group>
  )
}

function Camera({ estreito }: { estreito: boolean }) {
  const foco = useMemo(() => new THREE.Vector3(estreito ? 0 : 0.55, estreito ? -0.5 : 0, 0), [estreito])
  useFrame((state, delta) => {
    const { progresso: p } = lerEstado()
    // No celular a câmera quase não se aproxima: o núcleo já ocupa a metade de baixo.
    const distancia = (estreito ? 7.4 - 0.25 * Math.sin(p * Math.PI) : 6.4 - 0.7 * Math.sin(p * Math.PI))
    easing.damp3(state.camera.position, [-0.6 * p, 0.2 - 0.4 * p, distancia], 0.4, delta)
    state.camera.lookAt(foco)
  })
  return null
}

// Céu do estúdio: um gradiente vertical (dourado claro em cima, preto embaixo) em
// volta de tudo. É ele que faz o metal parecer ouro em toda a superfície, e não só
// na borda; as placas por cima dão os brilhos nítidos.
function criarCeuDoEstudio() {
  const tela = document.createElement('canvas')
  tela.width = 2
  tela.height = 256
  const contexto = tela.getContext('2d')!
  const gradiente = contexto.createLinearGradient(0, 0, 0, 256)
  gradiente.addColorStop(0, cores.ouroClaro)
  gradiente.addColorStop(0.42, cores.ouro)
  gradiente.addColorStop(0.7, cores.ouroEscuro)
  gradiente.addColorStop(0.9, cores.preto)
  contexto.fillStyle = gradiente
  contexto.fillRect(0, 0, 2, 256)
  const textura = new THREE.CanvasTexture(tela)
  textura.colorSpace = THREE.SRGBColorSpace
  return textura
}

// Placas de luz: [cor, intensidade, posição, largura × altura]. Poucas e assimétricas,
// como numa foto de produto: luz principal no alto à esquerda, contraluz atrás.
const PLACAS: [string, number, [number, number, number], [number, number]][] = [
  [cores.branco, 3.2, [-3, 4.5, 3], [5, 1.4]], // luz principal, no alto à esquerda
  [cores.ouroClaro, 1.8, [-6, 0, 1], [1.2, 7]], // faixa lateral esquerda
  [cores.ouro, 2.8, [3, 1, -6], [6, 4]], // contraluz atrás, à direita: desenha a borda
]

// Estúdio de luz próprio, sem HDRI: o céu e as placas viram o mapa de reflexo (PMREM)
// uma vez só. O <Environment preset> do drei baixaria um HDRI de um CDN, que a CSP do
// site bloqueia, e o <Environment> com <Lightformer> custava 19 KB gzip a mais.
function Estudio() {
  const gl = useThree((estado) => estado.gl)
  const cena = useThree((estado) => estado.scene)
  useEffect(() => {
    const estudio = new THREE.Scene()
    const texturaCeu = criarCeuDoEstudio()
    const geometriaCeu = new THREE.SphereGeometry(20, 32, 16)
    const materialCeu = new THREE.MeshBasicMaterial({
      map: texturaCeu,
      side: THREE.BackSide,
      color: new THREE.Color(cores.branco).multiplyScalar(0.9),
    })
    estudio.add(new THREE.Mesh(geometriaCeu, materialCeu))

    const geometria = new THREE.PlaneGeometry(1, 1)
    const materiais = PLACAS.map(([cor, intensidade, posicao, [largura, altura]]) => {
      const material = new THREE.MeshBasicMaterial({
        color: new THREE.Color(cor).multiplyScalar(intensidade),
        side: THREE.DoubleSide,
      })
      const placa = new THREE.Mesh(geometria, material)
      placa.position.set(...posicao)
      placa.scale.set(largura, altura, 1)
      placa.lookAt(0, 0, 0)
      estudio.add(placa)
      return material
    })
    const gerador = new THREE.PMREMGenerator(gl)
    const reflexo = gerador.fromScene(estudio, 0.03)
    cena.environment = reflexo.texture
    return () => {
      cena.environment = null
      reflexo.dispose()
      gerador.dispose()
      geometria.dispose()
      geometriaCeu.dispose()
      materialCeu.dispose()
      texturaCeu.dispose()
      materiais.forEach((material) => material.dispose())
    }
  }, [gl, cena])
  return null
}

function Luzes() {
  return (
    <>
      <ambientLight intensity={0.15} />
      <directionalLight position={[4, 5, 6]} intensity={1.6} color={cores.ouroClaro} />
      <Estudio />
    </>
  )
}

// Avisa depois de alguns quadros, com os shaders já compilados: aí o pôster pode sair.
function AvisoPronta({ aoFicarPronta }: { aoFicarPronta: () => void }) {
  const quadros = useRef(0)
  useFrame(() => {
    quadros.current += 1
    if (quadros.current === 3) aoFicarPronta()
  })
  return null
}

function CenaDourada({ estreito, eventSource, aoFicarPronta, aoPerderContexto }: OpcoesCinema) {
  const [dpr, setDpr] = useState(estreito ? 1.5 : 1.75)
  // Fora da tela (a pessoa já rolou para os planos), a cena para de desenhar.
  const [visivel, setVisivel] = useState(true)
  useEffect(() => {
    const observador = new IntersectionObserver(([entrada]) => setVisivel(entrada.isIntersecting))
    observador.observe(eventSource)
    return () => observador.disconnect()
  }, [eventSource])

  return (
    <Canvas
      dpr={[1, dpr]}
      frameloop={visivel ? 'always' : 'never'}
      camera={{ position: [0, 0.2, estreito ? 7.4 : 6.4], fov: 35, near: 0.1, far: 50 }}
      gl={{ antialias: true, alpha: true, powerPreference: 'high-performance' }}
      eventSource={eventSource}
      eventPrefix="client"
      onCreated={({ gl }) => gl.domElement.addEventListener('webglcontextlost', aoPerderContexto)}
    >
      <PerformanceMonitor onDecline={() => setDpr(1)} />
      <Camera estreito={estreito} />
      <Luzes />
      <Conjunto estreito={estreito} />
      <AvisoPronta aoFicarPronta={aoFicarPronta} />
    </Canvas>
  )
}

export function montar(alvo: HTMLElement, opcoes: OpcoesCinema) {
  const raiz = createRoot(alvo)
  raiz.render(
    <StrictMode>
      <CenaDourada {...opcoes} />
    </StrictMode>,
  )
  return () => raiz.unmount()
}
