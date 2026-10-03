# Biblioteca no Figma

Arquivo: https://www.figma.com/design/zam95scFOGbSjkrdukfpse (plano Starter da equipe).

`estado.json` registra o que já existe no arquivo (IDs de coleções, páginas e componentes) e o que falta.
Os scripts rodam pela ferramenta `use_figma` do MCP do Figma, com `fileKey` acima, um de cada vez.

## Limites do plano Starter que moldaram o arquivo

- 1 modo por coleção: o tema escuro é a coleção **Cor no escuro**, com os mesmos nomes da coleção **Cor**.
- 3 páginas: Capa, Fundamentos e Componentes (uma seção por componente).
- Cota mensal de chamadas do MCP: acabou em 03/10/2026, no meio da Fase 3.

## Falta (ordem de retomada)

1. `fase3b.js`: Campo + Grupo de campo, Caixa, Interruptor + Linha do interruptor, Aviso e os rótulos
   de linha/coluna das grades de Botão e Selo. Pronto para rodar.
2. Avatar, Métrica, Cartão de seção e Cartão da lista (celular), na página Componentes.
3. Fundamentos: `clipsContent = true` no cartão "Foco/Anel no claro" (sem isso o Figma ignora o
   espalhamento da sombra e o anel não aparece).
4. Revisão final: contraste, alvos de 44px, nomes e cores sem variável.
