# Reavaliação de segurança e desempenho — 12/09/2026

Escopo: código atual do workspace, incluindo alterações preexistentes; testes em SQLite e uploads temporários, sem acessar banco de produção. Nenhum código da aplicação foi alterado nesta revisão.

## Achados

1. **Médio — recuperação de senha revela diferença de tempo.** Em `blueprints/usuario_bp.py:715`, somente pares CPF/e-mail existentes com acesso ativado persistem o token e chamam `enviar_email` de forma síncrona. A mensagem é igual, mas o tempo não. Reprodução com provedor simulado demorando 200 ms: par inexistente respondeu em 11,6 ms; existente em 206,1 ms, ambos HTTP 200. Isso permite inferir a existência do par informado; os limites de tentativas reduzem a exploração. Recomenda-se usar a fila persistente também para recuperação e verificar novamente a distribuição dos tempos. Não foi feita enumeração real.

2. **Médio — ferramenta de instalação local desatualizada.** `pip-audit` no ambiente virtual encontrou 12 entradas de alertas para `pip==25.1.1`, representando seis identificadores PYSEC distintos (há duplicatas). O comando indica correções até 26.2.0. Recomenda-se atualizar o pip local e repetir a auditoria. Isso não demonstra exploração de uma rota HTTP nem descreve o ambiente implantado. O [changelog oficial](https://pip.pypa.io/en/stable/news/) registra as correções das versões posteriores. A auditoria separada de `requirements.txt`, incluindo resolução de dependências transitivas, não encontrou vulnerabilidades conhecidas.

3. **Desempenho — avisos crescem com toda a base.** `blueprints/adm_bp.py:665` carrega todos os alunos, filtra os ativos em Python e carrega seus históricos completos por `PagamentoDAO.mapa_por_aluno`. A contagem de consultas é baixa, mas o volume de objetos cresce com alunos e mensalidades. Recomenda-se filtrar no SQL e processar os destinatários em lotes, preservando as regras de vigência e inadimplência.

4. **Desempenho — ainda há e-mails síncronos.** Aprovação de cadastro (`blueprints/adm_bp.py:77`) e diversos fluxos em `usuario_bp.py` chamam diretamente o provedor. `servicos/email.py:56` configura timeout de 10 segundos na requisição HTTP; não é um prazo total garantido. Enquanto aguardam, esses envios ocupam uma das duas threads HTTP configuradas no Dockerfile. Recomenda-se ampliar o uso da fila existente.

## Medições locais

SQLite descartável, 1.000 alunos aprovados, um plano e 12.000 mensalidades pendentes; cliente de teste Flask, aquecimento seguido de dez requisições por rota. Sem rede HTTP, navegador ou limites de CPU/memória do Compose. Não são medidas de capacidade de produção.

| Rota | Mediana | Máximo observado | SELECTs por requisição |
|---|---:|---:|---:|
| `/admin` | 5,0 ms | 5,7 ms | 6 |
| `/admin/financeiro` | 23,1 ms | 24,0 ms | 6 |
| `/admin/avisos` | 345,2 ms | 376,0 ms | 6 |

## Validação e limites

- `pytest -q --durations=10`: **512 aprovados, 7 ignorados, 553 avisos, 53,74 segundos**. Há avisos de APIs depreciadas; não são falhas de teste.
- Os sete testes ignorados exigem `TEST_POSTGRES_URL`; concorrência e travas reais do PostgreSQL não foram revalidadas nesta execução.
- `pip check`: nenhuma dependência quebrada.
- `pip-audit -r requirements.txt --progress-spinner off`: nenhuma vulnerabilidade conhecida encontrada.
- Revisados controles de sessão e revogação de credenciais, CSRF e cabeçalhos centrais, limites de upload, paginação e carregamento de dados. Os testes de regressão existentes passaram; isso não prova ausência de outras vulnerabilidades.
- Configuração efetiva de produção, versões das imagens em execução, HTTPS, consumo de memória e latência sob concorrência continuam fora desta validação local.

Prioridade sugerida: atualizar o pip local; colocar recuperação e outros e-mails transacionais na fila; reduzir o volume carregado em avisos; executar os testes PostgreSQL e uma medição sob concorrência em ambiente de homologação.
