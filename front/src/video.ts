// Hero com vídeo: quando existe static/video/cinema.mp4, ele assume o lugar da cena
// 3D e avança com a rolagem (scrolly-video, como no template Framerate). Quem manda
// no progresso é static/js/cinema.js, pelo evento `cinema:progresso`.
import ScrollyVideo from 'scrolly-video/dist/ScrollyVideo.js'
import type { OpcoesCinema } from './estado'

export function montar(alvo: HTMLElement, src: string, opcoes: OpcoesCinema) {
  let avisou = false
  const pronto = () => {
    if (avisou) return
    avisou = true
    opcoes.aoFicarPronta()
  }
  const video = new ScrollyVideo({
    src,
    scrollyVideoContainer: alvo,
    cover: true,
    sticky: false,
    full: false,
    trackScroll: false,
    lockScroll: false,
    transitionSpeed: 8,
    frameThreshold: 0.02,
    useWebCodecs: true,
    onReady: pronto,
  })
  // Sem WebCodecs (caminho HTML5) o scrolly-video nunca chama onReady: o primeiro
  // quadro do <video> serve de aviso.
  video.video?.addEventListener('loadeddata', pronto, { once: true })

  const aoMudar = (evento: Event) => {
    const { progresso } = (evento as CustomEvent<{ progresso: number }>).detail
    video.setVideoPercentage(progresso)
  }
  window.addEventListener('cinema:progresso', aoMudar)
  return () => {
    window.removeEventListener('cinema:progresso', aoMudar)
    video.destroy()
  }
}
