// Ponte com static/js/cinema.js, o controle da rolagem do hero. Ele escreve o
// progresso em window.etCinema a cada rolagem; a cena só lê, uma vez por quadro,
// sem passar pelo React (setState a 60 quadros por segundo re-renderizaria tudo).

export type EstadoCinema = {
  progresso: number // 0 no topo do hero, 1 quando a última manchete termina
  indice: number // manchete ativa
  total: number
}

export type OpcoesCinema = {
  estreito: boolean // celular: emblema menor, centralizado abaixo do texto
  eventSource: HTMLElement // o ponteiro é lido no hero inteiro, não só no canvas
  aoFicarPronta: () => void
  aoPerderContexto: () => void
}

declare global {
  interface Window {
    etCinema?: EstadoCinema
  }
}

const PADRAO: EstadoCinema = { progresso: 0, indice: 0, total: 1 }

export function lerEstado(): EstadoCinema {
  return window.etCinema ?? PADRAO
}
