// Cena do hero da home: o emblema do dragão feito de brasas. No topo do hero ele está
// meio formado, com brasas soltas em volta; com a rolagem elas se juntam, o emblema
// brilha nas últimas manchetes e sobe de novo como brasa quando o hero acaba. A cena não
// decide nada sozinha: a cada quadro lê o progresso da rolagem que static/js/cinema.js
// publica (ver estado.ts). Nenhum texto mora aqui; título, botões e SEO ficam no Jinja.
import { PerformanceMonitor } from '@react-three/drei'
import { Canvas, useFrame } from '@react-three/fiber'
import { easing } from 'maath'
import { StrictMode, Suspense, use, useEffect, useMemo, useRef, useState } from 'react'
import { createRoot } from 'react-dom/client'
import * as THREE from 'three'
import urlEmblema from './emblema.webp'
import { lerEstado, type OpcoesCinema } from './estado'
import { cores } from './tokens'

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

// Mancha radial macia, branca: vira o halo atrás do emblema (a cor vem do material).
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
// que faz as brasas do emblema saltarem.
function useGolpe() {
  const golpe = useRef({ indice: 0, inicio: -10 })
  return (indice: number, agora: number) => {
    if (indice !== golpe.current.indice) golpe.current = { indice, inicio: agora }
    const t = (agora - golpe.current.inicio) / 0.9
    return t >= 0 && t < 1 ? Math.sin(t * Math.PI) * (1 - t) : 0
  }
}

// Brasas que sobem em volta do emblema: cada uma com velocidade, tamanho e fase
// próprios, num único <points> com shader (uma chamada de desenho para todas). O
// deslocamento é acumulado na CPU (uDeslocamento), então acelerar com a rolagem não dá salto.
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
      // Coluna larga em volta do emblema, mais densa perto do eixo.
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

// Brilho dourado atrás do emblema: um sprite (sempre de frente para a câmera).
function Halo({ escala, opacidade }: { escala: number; opacidade: { current: number } }) {
  const material = useRef<THREE.SpriteMaterial>(null!)
  const textura = useMemo(criarTexturaHalo, [])
  useEffect(() => () => textura.dispose(), [textura])
  useFrame(() => {
    material.current.opacity = opacidade.current
  })
  return (
    <sprite scale={[escala, escala, 1]} position={[0, 0, -1.2]}>
      <spriteMaterial
        ref={material}
        map={textura}
        color={cores.ouro}
        transparent
        depthWrite={false}
        blending={THREE.AdditiveBlending}
        toneMapped={false}
      />
    </sprite>
  )
}

// --- Emblema de brasas ---------------------------------------------------------------

// Altura do emblema na cena; a largura sai da proporção da imagem (front/src/emblema.webp,
// gerada por front/scripts/emblema.py a partir do emblema oficial).
const ALTURA_EMBLEMA = 2.7

type AmostraEmblema = {
  alvos: Float32Array // onde cada brasa fica no emblema formado
  soltas: Float32Array // onde ela anda quando está solta
  cores: Float32Array
  atrasos: Float32Array // 0 a 1: ordem de chegada (e de saída, ao contrário)
  fases: Float32Array
  tamanho: number // diâmetro de uma brasa, para elas se tocarem sem amontoar
}

const BRONZE = new THREE.Color(cores.ouroEscuro)

// Sorteia as brasas entre os pixels opacos do emblema, com a cor de cada pixel. O dourado
// do X, o olho e a boca do dragão ficam como estão. As escamas seguem o brilho do pixel,
// puxadas para o bronze: o corpo fica quase preto e o contorno das escamas acende, que é
// como o dragão do logo se lê sobre o preto.
function amostrarEmblema(imagem: HTMLImageElement, quantidade: number): AmostraEmblema {
  const { naturalWidth: largura, naturalHeight: altura } = imagem
  const tela = document.createElement('canvas')
  tela.width = largura
  tela.height = altura
  const contexto = tela.getContext('2d', { willReadFrequently: true })!
  contexto.drawImage(imagem, 0, 0)
  const pixels = contexto.getImageData(0, 0, largura, altura).data

  // O dourado é o X, o olho e a boca; o resto é escama.
  const lerPixel = (indice: number) => {
    const [r, g, b] = [pixels[indice * 4] / 255, pixels[indice * 4 + 1] / 255, pixels[indice * 4 + 2] / 255]
    return { r, g, b, luz: 0.2126 * r + 0.7152 * g + 0.0722 * b, dourado: r > 0.5 && g > 0.3 && b < 0.35 && r - b > 0.3 }
  }

  // Sorteio com peso e sem repetição (Efraimidis-Spirakis): cada pixel opaco ganha a chave
  // sorteio^(1/peso) e ficam as maiores. O detalhe do dragão está nos brilhos, e o
  // dourado liso do X se lê bem com menos brasas. Tudo em arrays numéricos: com objetos e
  // função de comparação, o sorteio levava ~410 ms com a CPU 4x mais lenta (celular
  // médio); assim, ~100 ms.
  const aleatorio = sementeAleatoria(11)
  const indices = new Int32Array(largura * altura)
  const chaves = new Float32Array(largura * altura)
  let opacos = 0
  for (let indice = 0; indice < largura * altura; indice++) {
    if (pixels[indice * 4 + 3] < 128) continue
    const { luz, dourado } = lerPixel(indice)
    indices[opacos] = indice
    chaves[opacos] = Math.pow(aleatorio(), 1 / (dourado ? 0.5 : 0.15 + Math.min(1, 2 * luz)))
    opacos++
  }
  const total = Math.min(quantidade, opacos)
  const corte = chaves.slice(0, opacos).sort()[opacos - total]

  const escala = ALTURA_EMBLEMA / altura
  const alvos = new Float32Array(total * 3)
  const soltas = new Float32Array(total * 3)
  const coresBrasas = new Float32Array(total * 3)
  const atrasos = new Float32Array(total)
  const fases = new Float32Array(total)
  const cor = new THREE.Color()
  for (let k = 0, n = 0; k < opacos && n < total; k++) {
    if (chaves[k] < corte) continue
    const indice = indices[k]
    const { r, g, b, luz, dourado } = lerPixel(indice)
    const x = indice % largura
    const y = Math.floor(indice / largura)

    // Relevo: o X dourado fica um pouco atrás do dragão, e o brilho das escamas vem para a
    // frente. É o que dá volume quando o emblema gira.
    const z = (dourado ? -0.06 : 0.03 + 0.18 * luz) + (aleatorio() - 0.5) * 0.03
    alvos.set([(x + aleatorio() - largura / 2) * escala, (altura / 2 - y - aleatorio()) * escala, z], n * 3)

    cor.setRGB(r, g, b, THREE.SRGBColorSpace)
    if (dourado) cor.multiplyScalar(0.85)
    else cor.lerp(BRONZE, 0.35).multiplyScalar(Math.min(1.5, 2 * luz))
    coresBrasas.set([cor.r, cor.g, cor.b], n * 3)

    // Solta, a brasa fica perto do seu lugar, empurrada para fora do centro e para cima:
    // o emblema "explodido" continua com a forma dele, em vez de virar um céu de estrelas.
    const espalhamento = 0.25 + 0.7 * Math.pow(aleatorio(), 1.5)
    const [ax, ay] = [alvos[n * 3], alvos[n * 3 + 1]]
    const distancia = Math.hypot(ax, ay) || 1
    soltas.set(
      [
        ax + (ax / distancia * 0.5 + aleatorio() - 0.5) * espalhamento,
        ay + (ay / distancia * 0.5 + aleatorio() - 0.3) * espalhamento,
        (aleatorio() - 0.5) * 2 * espalhamento,
      ],
      n * 3,
    )

    // O dragão chega primeiro e o X depois: no topo do hero a cabeça do dragão já está
    // inteira, e o X, de forma grande e lisa, se lê mesmo ralo.
    atrasos[n] = dourado ? 0.3 + 0.7 * aleatorio() : 0.6 * aleatorio()
    fases[n] = aleatorio() * Math.PI * 2
    n++
  }

  const areaOpaca = opacos * escala * escala
  return { alvos, soltas, cores: coresBrasas, atrasos, fases, tamanho: 1.4 * Math.sqrt(areaOpaca / total) }
}

// A imagem é baixada e amostrada uma vez por quantidade (o StrictMode monta duas vezes).
const amostras = new Map<number, Promise<AmostraEmblema>>()

function carregarEmblema(quantidade: number) {
  let amostra = amostras.get(quantidade)
  if (!amostra) {
    const imagem = new Image()
    imagem.src = urlEmblema
    amostra = imagem.decode().then(() => amostrarEmblema(imagem, quantidade))
    amostras.set(quantidade, amostra)
  }
  return amostra
}

const verticeEmblema = /* glsl */ `
  uniform float uTempo;
  uniform float uEscalaPixel;
  uniform float uTamanho;
  uniform float uFormacao;
  uniform float uDesfazer;
  uniform float uImpulso;
  uniform float uBrilho;
  uniform vec3 uCorSolta;
  attribute vec3 aSolta;
  attribute vec3 aCor;
  attribute float aAtraso;
  attribute float aFase;
  varying vec3 vCor;
  varying float vAlfa;
  void main() {
    // 0 solta, 1 no lugar. Com uFormacao em 1, todas chegaram.
    float chegada = smoothstep(0.0, 0.12, uFormacao * 1.12 - aAtraso);

    // Solta, a brasa flutua devagar em volta do seu lugar.
    vec3 deriva = vec3(sin(uTempo * 0.3 + aFase), 0.6 * sin(uTempo * 0.4 + aFase * 1.7), cos(uTempo * 0.35 + aFase));
    vec3 solta = aSolta + deriva * 0.12;
    vec3 tremor = vec3(sin(uTempo * 1.3 + aFase * 7.0), cos(uTempo * 1.1 + aFase * 5.0), sin(uTempo * 0.9 + aFase * 3.0));
    vec3 p = mix(solta, position, chegada) + tremor * mix(0.04, 0.006, chegada);

    // Golpe da troca de manchete: as brasas saltam para fora do centro e voltam.
    p.xy += normalize(position.xy + 0.001) * uImpulso * (0.12 + 0.2 * fract(aFase));

    // Fim do hero: o emblema queima de cima para baixo e as brasas sobem.
    float ordem = clamp(0.5 + position.y / ${ALTURA_EMBLEMA.toFixed(2)}, 0.0, 1.0) * 0.8 + 0.2 * fract(aFase * 3.1);
    float saida = clamp((uDesfazer * 1.5 - (1.0 - ordem)) / 0.5, 0.0, 1.0);
    p.y += saida * saida * 1.8;
    p.x += sin(uTempo * 0.8 + aFase * 9.0) * saida * 0.3;

    vec4 vista = modelViewMatrix * vec4(p, 1.0);
    gl_Position = projectionMatrix * vista;
    gl_PointSize = uTamanho * (1.0 + 0.4 * (1.0 - chegada)) * uEscalaPixel / -vista.z;
    float cintila = 0.8 + 0.2 * sin(uTempo * 2.1 + aFase * 11.0);
    vCor = mix(aCor, uCorSolta, max(1.0 - chegada, saida)) * cintila * uBrilho;
    vAlfa = (1.0 - saida) * mix(0.7, 1.0, chegada);
  }
`

const fragmentoEmblema = /* glsl */ `
  varying vec3 vCor;
  varying float vAlfa;
  void main() {
    float alfa = smoothstep(0.5, 0.1, length(gl_PointCoord - 0.5)) * vAlfa;
    gl_FragColor = vec4(vCor, alfa);
    #include <colorspace_fragment>
  }
`

type Movimento = { formacao: number; desfazer: number; impulso: number; brilho: number }

type PropsEmblema = { quantidade: number; escala: number; movimento: { current: Movimento } }

function Emblema({ quantidade, escala, movimento }: PropsEmblema) {
  const amostra = use(carregarEmblema(quantidade))
  const material = useRef<THREE.ShaderMaterial>(null!)
  const uniformes = useMemo(
    () => ({
      uTempo: { value: 0 },
      uEscalaPixel: { value: 400 },
      uTamanho: { value: amostra.tamanho * escala },
      uFormacao: { value: 0 },
      uDesfazer: { value: 0 },
      uImpulso: { value: 0 },
      uBrilho: { value: 1 },
      uCorSolta: { value: new THREE.Color(cores.ouroClaro) },
    }),
    [amostra, escala],
  )

  useFrame((state) => {
    const u = material.current.uniforms
    const m = movimento.current
    u.uTempo.value = state.clock.elapsedTime
    // Pixels por unidade a 1 de distância: a brasa tem o mesmo tamanho na tela em qualquer resolução.
    const fov = THREE.MathUtils.degToRad((state.camera as THREE.PerspectiveCamera).fov)
    u.uEscalaPixel.value = (state.size.height * state.viewport.dpr) / (2 * Math.tan(fov / 2))
    u.uFormacao.value = m.formacao
    u.uDesfazer.value = m.desfazer
    u.uImpulso.value = m.impulso
    u.uBrilho.value = m.brilho
  })

  return (
    <points frustumCulled={false}>
      <bufferGeometry>
        <bufferAttribute attach="attributes-position" args={[amostra.alvos, 3]} />
        <bufferAttribute attach="attributes-aSolta" args={[amostra.soltas, 3]} />
        <bufferAttribute attach="attributes-aCor" args={[amostra.cores, 3]} />
        <bufferAttribute attach="attributes-aAtraso" args={[amostra.atrasos, 1]} />
        <bufferAttribute attach="attributes-aFase" args={[amostra.fases, 1]} />
      </bufferGeometry>
      <shaderMaterial
        ref={material}
        uniforms={uniformes}
        vertexShader={verticeEmblema}
        fragmentShader={fragmentoEmblema}
        transparent
        depthWrite={false}
        blending={THREE.AdditiveBlending}
      />
    </points>
  )
}

// No topo do hero o dragão e ~60% do X já estão no lugar: quem não rola vê a marca, e o
// pôster (que é esta cena parada no topo) também.
const FORMACAO_INICIAL = 0.75

function Conjunto({ estreito, leve }: { estreito: boolean; leve: boolean }) {
  const conjunto = useRef<THREE.Group>(null!)
  const giro = useRef<THREE.Group>(null!)
  const energia = useRef(0)
  const halo = useRef(0.16)
  const movimento = useRef<Movimento>({ formacao: FORMACAO_INICIAL, desfazer: 0, impulso: 0, brilho: 1 })
  const golpe = useGolpe()

  useFrame((state, delta) => {
    const { progresso: p, indice } = lerEstado()
    const impulso = golpe(indice, state.clock.elapsedTime)
    const m = movimento.current
    const { smoothstep } = THREE.MathUtils

    // Fecha durante a primeira manchete, brilha nas duas últimas e sobe como brasa
    // nos últimos 10% do hero, quando os planos já vêm entrando.
    easing.damp(m, 'formacao', FORMACAO_INICIAL + (1 - FORMACAO_INICIAL) * smoothstep(p, 0, 0.3), 0.25, delta)
    easing.damp(m, 'desfazer', 0.85 * smoothstep(p, 0.9, 1), 0.2, delta)
    easing.damp(m, 'brilho', 1 + 0.35 * smoothstep(p, 0.5, 0.8) + 0.6 * impulso, 0.15, delta)
    m.impulso = impulso
    halo.current = 0.12 + 0.12 * smoothstep(p, 0.5, 0.8) + 0.2 * impulso

    // Desktop: sempre à direita do título, sem invadir a coluna do texto.
    // Celular: no vão entre o texto e o rodapé do hero, subindo um pouco ao longo dele.
    const alvo: [number, number, number] = estreito
      ? [0, -1.05 + 0.2 * p, 0]
      : [1.95 - 0.25 * p, -0.05 - 0.1 * p, 0]
    easing.damp3(conjunto.current.position, alvo, 0.35, delta)
    // Vira devagar de um lado para o outro ao longo do hero; o mouse inclina um pouco.
    easing.dampE(
      giro.current.rotation,
      [0.05 - 0.08 * state.pointer.y, -0.16 + 0.32 * p + 0.14 * state.pointer.x, 0],
      0.5,
      delta,
    )

    // As brasas de fundo sobem mais rápido no meio do hero e disparam a cada golpe.
    energia.current = 0.6 * Math.sin(p * Math.PI) + 2.2 * impulso
  })

  const escala = estreito ? 0.66 : 0.94
  return (
    <group ref={conjunto} position={estreito ? [0, -1.05, 0] : [1.95, -0.05, 0]}>
      <Halo escala={estreito ? 3 : 4.6} opacidade={halo} />
      <group ref={giro} scale={escala}>
        <Emblema quantidade={estreito ? 18000 : 34000} escala={escala} movimento={movimento} />
      </group>
      <Brasas
        quantidade={leve ? 60 : estreito ? 110 : 240}
        espalhamento={estreito ? 1.6 : 2.4}
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
    // No celular a câmera quase não se aproxima: o emblema já ocupa a metade de baixo.
    const distancia = (estreito ? 7.4 - 0.25 * Math.sin(p * Math.PI) : 6.4 - 0.7 * Math.sin(p * Math.PI))
    easing.damp3(state.camera.position, [-0.6 * p, 0.2 - 0.4 * p, distancia], 0.4, delta)
    state.camera.lookAt(foco)
  })
  return null
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

function CenaDoEmblema({ estreito, leve, eventSource, aoFicarPronta, aoPerderContexto }: OpcoesCinema) {
  const [dpr, setDpr] = useState(leve ? 1 : estreito ? 1.5 : 1.75)
  // Fora da tela (a pessoa já rolou para os planos), a cena para de desenhar.
  const [visivel, setVisivel] = useState(true)
  // O iOS derruba o contexto WebGL quando o Safari vai para segundo plano ou falta memória.
  // O three.js recria tudo sozinho quando ele volta, mas o pôster que cobriu a cena na perda
  // ficava para sempre: a cada volta, o aviso conta de novo os quadros e tira o pôster.
  const [restauracoes, setRestauracoes] = useState(0)
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
      onCreated={({ gl }) => {
        gl.domElement.addEventListener('webglcontextlost', aoPerderContexto)
        gl.domElement.addEventListener('webglcontextrestored', () => setRestauracoes((n) => n + 1))
      }}
    >
      <PerformanceMonitor onDecline={() => setDpr(1)} />
      <Camera estreito={estreito} />
      {/* Até a imagem do emblema chegar não há o que mostrar: o pôster fica. */}
      <Suspense fallback={null}>
        <Conjunto estreito={estreito} leve={leve} />
        <AvisoPronta key={restauracoes} aoFicarPronta={aoFicarPronta} />
      </Suspense>
    </Canvas>
  )
}

export function montar(alvo: HTMLElement, opcoes: OpcoesCinema) {
  const raiz = createRoot(alvo)
  raiz.render(
    <StrictMode>
      <CenaDoEmblema {...opcoes} />
    </StrictMode>,
  )
  return () => raiz.unmount()
}
