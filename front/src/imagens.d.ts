// O Vite troca o import de uma imagem pela URL do arquivo no build (com hash no nome).
declare module '*.webp' {
  const url: string
  export default url
}
