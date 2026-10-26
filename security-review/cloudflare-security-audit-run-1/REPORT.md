# Auditoria de segurança — SistemaEXTREMETEAM (skill `security-audit` da Cloudflare, run-1)

## 1. Escopo, perfil e limites desta passada

- **Perfil:** `quick`. É uma **passada parcial**, não uma auditoria exaustiva: houve uma onda de caçadores e um crítico final, e as Fases 3 e 5 foram fundidas, com um verificador independente por candidato.
- **Escopo:** o repositório inteiro (`.`), exceto o build em `static/dist/`, `front/node_modules/`, `graphify-out/` e `.claude/`.
- **Revisão do código:** commit `dc6adb2`, na branch `claude/relatorio-seguranca-2026-10-26`. O código é idêntico ao da `main` em `14c78b4`; a branch só acrescenta um relatório em `security-review/`.
- **Orçamento:** não foi definido. Foram usados **14 agentes**: 4 de reconhecimento, 6 caçadores, 1 crítico final e 3 verificadores.
- **Como o código foi executado:** a política é `sandboxed-source-and-local-only`, ou seja, leitura do código e execução apenas local e isolada.
  - Nenhum serviço implantado foi acessado: nem produção, nem Mercado Pago, Gmail, Google, Supabase ou Sentry.
  - Toda execução de código do projeto rodou em sandbox: `unshare` sem rede, todos os mounts somente leitura exceto a `scratch` do agente, ambiente vazio (`env -i`) com allowlist, `prlimit` e timeout.
  - Os provedores externos foram simulados com *mocks*.
  - As evidências foram promovidas para `artifacts/` por um promotor confiável, que segue não-links simbólicos, exige arquivo regular com um link só e aplica limites de tamanho.
- **Execuções anteriores:** não havia `coverage-ledger.json` ou `findings.json` compatível. Os relatórios em prosa de `security-review/` não foram usados como exclusão nem como exemplo para os caçadores.
- **Cobertura adiada:** a unidade **u13** (cotas e chaves do limitador nas rotas pré-autenticação: login, segundo fator do admin, cadastro e recuperação de senha) foi apontada pelo crítico final e ficou `deferred` com o motivo `quick_profile_final_critic`. Ela não foi auditada nesta passada.
- **Fora de escopo:** código nativo, IA/LLM e IPC local, porque não há essas superfícies.

## 2. Postura geral

A base é madura:
- sessão revalidada no banco a cada requisição;
- checagem de dono em todos os recursos do aluno;
- webhook do Mercado Pago com HMAC e conciliação de referência, valor e moeda;
- uploads reprocessados com teto de pixels;
- CSP com nonce e nenhum `|safe`.

Os três achados abaixo estão nos **fluxos de identidade**: o ciclo de vida da sessão após o logout, a vinculação do login com Google e a entrega dos e-mails que provam a posse de um endereço. Nenhum é crítico ou alto.

## 3. Achados confirmados

| Severidade | Título | Fronteira afetada | Resultado observado (local) |
|---|---|---|---|
| **Média** | Cookie de sessão copiado sobrevive ao logout e volta a valer depois que a linha de revogação é apagada | Revogação de sessão no logout | Cópia do cookie renovada por página pública; após o expurgo, `GET /perfil` deu 200 com o perfil da vítima |
| **Baixa** | Sequestro prévio de conta: o login com Google verifica e abre uma conta cuja senha foi criada por quem nunca provou o e-mail | Vínculo identidade Google ↔ conta | A sessão Google da vítima e o login por senha do atacante caíram no mesmo `aluno_id` |

### 3.1 [Média] Cookie copiado sobrevive ao logout
`servicos/autorizacao.py:revogar_sessao_atual:revocation-row-purged-while-refreshable-cookie-lives`

- **Onde:** `servidor.py:412` (logout) → `servicos/autorizacao.py:58` (a linha de revogação expira 35 min depois) → `servidor.py:98` (`SESSION_REFRESH_EACH_REQUEST=True` renova o cookie em qualquer rota) → `servicos/autorizacao.py:55` (expurgo no próximo logout) → `servicos/autorizacao.py:82` (`_sessao_ativa` aceita o `sid` de novo).
- **Quem ataca:** quem já tem uma cópia do cookie da vítima, como num computador compartilhado, por extensão do navegador ou por log de proxy com inspeção TLS. É exatamente a ameaça para a qual a tabela `sessoes_revogadas` foi criada.
- **Como foi reproduzido:**
  - No sandbox, com SQLite e limitador em memória, o caçador e o verificador fizeram isso de forma independente.
  - A vítima fez login e logout, e a cópia do cookie passou a ser recusada.
  - Em T0+25 min, um `GET /` renovou a cópia com o mesmo `sid`.
  - Em T0+40 min, o logout de outro aluno apagou a linha de revogação.
  - Em T0+55 min, `GET /perfil` com a cópia renovada deu 200 com o nome da vítima. Um cliente de controle, sem renovação, recebeu 302.
- **Condições:** a vítima não troca a senha, o atacante faz uma requisição pública a cada 30 min e há algum logout de terceiro depois do vencimento da linha.
- **Impacto:** uso pleno da conta depois que a vítima acreditou ter saído. Aluno foi demonstrado; professor e admin usam o mesmo `_sessao_ativa`.
- **Prioridade:** probabilidade baixa (exige cookie já copiado) e impacto médio, o que dá severidade **média**.
- **Menor correção:**
  1. Um `before_request` que limpa a sessão quando `_sessao_ativa()` falha, para que um cookie revogado nunca seja reassinado.
  2. Um carimbo `emitida_em` com vida máxima absoluta (por exemplo 12 h), com as linhas de revogação retidas pelo menos por esse tempo.
  3. Teste de regressão: logout, renovação por página pública, expurgo e `/perfil`, que deve voltar `302 /login`.

### 3.2 [Baixa] Sequestro prévio de conta pelo login com Google
`blueprints/google_login.py:callback:login-binds-unverified-registrant-account`

- **Onde:** `blueprints/usuario_bp.py:403` (cadastro anônimo com e-mail qualquer) → `blueprints/google_login.py:144` (conta escolhida só pelo e-mail) → `:162` (marca `email_verificado=True` em conta pendente) → `blueprints/adm_bp.py:82` (aprovação pelo admin) → `blueprints/google_login.py:175` (abre a sessão).
- **Quem ataca:** visitante anônimo que se cadastra primeiro com o e-mail da vítima e uma senha escolhida por ele.
- **Como foi reproduzido:**
  - No sandbox, com as chamadas ao Google simuladas: o cadastro do atacante criou a linha `(1, False, 'pendente')`.
  - O cadastro da própria vítima não criou nada.
  - O login Google da vítima levou a linha a `(1, True, 'pendente')`, que então apareceu na lista de pendentes do admin.
  - Depois da aprovação, o Google da vítima abriu `aluno_id=1`, e a senha do atacante também. O `/perfil` do atacante mostrou o e-mail da vítima.
- **Condições:**
  - a vítima ainda não está cadastrada e entra com o Google enquanto a conta está pendente;
  - o admin aprova um cadastro com nome, CPF e telefone digitados pelo atacante;
  - a vítima continua usando a conta.
- **Impacto:** o atacante mantém acesso por senha à conta usada pela vítima (dados pessoais, pagamentos, comprovantes, foto). Fica restrito a uma conta e se resolve com "Esqueci minha senha" quando percebido.
- **Prioridade:** probabilidade baixa e impacto médio. O verificador fixou a severidade geral em **baixa** pela cadeia de condições.
- **Menor correção:**
  - No callback, recusar contas com `email_verificado=False` (mandar para o link do cadastro ou para "Esqueci minha senha") e remover a autoverificação.
  - Alternativa: quando o Google for a primeira prova do e-mail, apagar `senha_hash` e os tokens e exigir uma senha nova.

## 4. NEEDS VALIDATION (sem severidade, não é vulnerabilidade confirmada)

| Título | Rastro | Bloqueio exato | Próximo passo local | Checagem do dono |
|---|---|---|---|---|
| O nome do aluno, sem aspas, no cabeçalho `To` pode acrescentar um destinatário atacante aos links que provam posse de e-mail | `blueprints/usuario_bp.py:689` → `:805` → `servicos/email.py:65` → `servicos/gmail_conta.py:149` → `:153` | Não dá para observar offline se a Gmail API (`users.messages.send`) entrega a **todos** os endereços do `To` cru | Reexecutar `agents/v03-to-header/artifacts/evidence/check-01.txt`: confirmar 2 destinatários e, com `Address(...)`, só 1 | Com uma conta Gmail de teste e duas caixas próprias, pôr o nome `Test <caixa-2@...>, X` num aluno de teste, pedir troca de e-mail para a caixa-1 e ver se a caixa-2 recebe o link |

Localmente, o verificador e dois caçadores mostraram de forma independente que a mensagem crua sai com dois destinatários. O token tirado dela confirmou o e-mail da vítima na conta do atacante. Se a entrega se confirmar, esse caminho também alimenta o 3.2: a vítima que entrar com o Google cai na conta do atacante. Detalhes em `NEEDS-VALIDATION.md`.

## 5. Notas de endurecimento (não são achados)

- **Token em claro na fila de e-mail:** o link de verificação do cadastro (`blueprints/usuario_bp.py:421-432`) passa por `fila_email.enfileirar_transacional` e fica gravado em claro em `emails_pendentes.link_url`, contra a regra documentada em `servicos/fila_email.py:122-124`.
- **Token no Sentry:** `servicos/observabilidade.py:30` não mascara `/cadastro/verificar/<token>`.
- **Retenção:** as linhas de `emails_pendentes` (e-mail, nome, telefone em avisos ao admin) nunca são apagadas. Falta um job de retenção.
- **`confirmar_email` (`usuario_bp.py:849`):** não reconfere se o e-mail continua livre, e uma colisão vira `IntegrityError` (erro 500) em vez de uma recusa limpa.
- **Gmail OAuth sem PKCE:** diferente do login com Google e do Mercado Pago. O `state` é ligado à sessão e o callback é só para admin.
- **Segundo fator do admin:**
  - a proteção contra reuso do código falha aberta se o Redis cair (`usuario_bp.py:226-238`, troca deliberada);
  - o marcador pendente não guarda a credencial que passou na etapa da senha.
- **Paginação:** `templates/components/paginacao.html` espalha `request.args` em `url_for`. Chaves como `_scheme` e `_external` mudam o link, e `endpoint` dá erro 500. Não há XSS nem troca de host.
- **`_voltar_para_origem` (`servidor.py:281-287`):** não rejeita caminho iniciado por `//`.
- **Pagamentos:**
  - as rotas de status, retorno do checkout e sincronização do admin chamam `_processar_status_mp` sem trava de linha. Há uma janela de cerca de 3 s em que um reembolso pode ser sobrescrito por um `approved` antigo;
  - reembolso e chargeback não desfazem a matrícula criada automaticamente;
  - o preço promocional fica congelado em cobranças não pagas (comportamento documentado).
- **Build e deploy:**
  - `.dockerignore` não exclui `security-review/`, nem os scripts mortos `route_verificacao.py` e `update_model.py`;
  - no Render, `TRUST_PROXY_COUNT` padrão 0 junta todos os IPs num só balde de limite.
- **Autorização do admin:** a checagem é feita rota a rota. Um `before_request` no blueprint fecharia por padrão também as rotas futuras.
- **Unicidade de login:** é conferida só entre alunos, não contra professores nem o `ADMIN_USER`. Não há efeito entre principais diferentes.

### Padrões positivos confirmados
- Sessão com `sid` revogável e impressão da credencial revalidadas a cada requisição.
- CSRF global.
- Rotação da sessão em todo login.
- OAuth do Google e do Mercado Pago com `state` + PKCE e tokens cifrados com Fernet.
- Webhook com HMAC, janela de 300 s, marca contra reenvio e reconsulta à API.
- Valor sempre lido do banco.
- Uploads com lista fechada de formatos no Pillow, teto de pixels, nome UUID e rotas autenticadas.
- Exportação XLSX com todas as células forçadas a texto.
- CI com `contents: read` e actions fixadas por SHA.

## 6. Cobertura (do ledger)

- **13 unidades:** 9 `covered`, 3 `candidate` (com decisão final independente) e 1 `deferred` (u13, `quick_profile_final_critic`). Nenhuma `blocked`.
- **Crítico final:** aceitou 1 unidade ausente (u13) e nenhuma reatribuição. Por ser `quick`, não houve segunda onda, então **não há alegação de cobertura completa**.
- **Correções feitas pelo coordenador:**
  - no resultado do caçador h01, o campo `method` dos checks foi preenchido a partir do `artifact` (`null` vira `source`, arquivo vira `local`);
  - o fingerprint duplicado `servicos/gmail_conta.py:enviar:to-header-display-name-address-injection` (h05) foi consolidado no canônico do h01, por ser a mesma causa raiz.
- **Validadores:** `validate-findings.cjs` e `validate-coverage-ledger.cjs` passaram.
