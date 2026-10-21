import react from '@vitejs/plugin-react'
import { fileURLToPath } from 'node:url'
import { defineConfig } from 'vite'

const aqui = (caminho: string) => fileURLToPath(new URL(caminho, import.meta.url))

// Compila o hero da home para static/dist/cinema, que o Flask serve como qualquer
// arquivo estático. O Flask não versiona estáticos, então o hash do conteúdo vai no
// nome de cada arquivo e servicos/cinema.py acha as entradas pelo manifest.
// Rode `npm run build` nesta pasta e versione o resultado junto com o código.
export default defineConfig({
  plugins: [react()],
  base: './',
  build: {
    outDir: aqui('../static/dist/cinema'),
    emptyOutDir: true,
    manifest: 'manifest.json',
    target: 'es2022',
    modulePreload: { polyfill: false },
    // A cena leva o three.js inteiro (o R3F importa o pacote todo): ~1,15 MB, 316 KB
    // gzip. É baixada só depois que a página carregou, então o aviso padrão de 500 KB
    // não se aplica; o limite fica logo acima do tamanho atual para pegar regressão.
    chunkSizeWarningLimit: 1200,
    rolldownOptions: {
      // Duas entradas independentes: a cena 3D (React + three) e o vídeo
      // (scrolly-video). O visitante só baixa a que a página usar.
      input: { cena: aqui('src/cena.tsx'), video: aqui('src/video.ts') },
      preserveEntrySignatures: 'exports-only',
      output: {
        entryFileNames: '[name]-[hash].js',
        chunkFileNames: '[name]-[hash].js',
      },
    },
  },
})
