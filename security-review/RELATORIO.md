# Relatório de segurança — Sistema Extreme Team

**Última atualização:** 22/09/2026
**Escopo:** aplicação Flask/Python completa (autenticação, autorização, acesso a dados,
injeção, XSS, CSRF, uploads, segredos, pagamentos, matrícula/turma, presença).
**Método:** leitura direta do código-fonte atual (não apenas dos relatórios anteriores),
consulta ao grafo do projeto, `grep`/varredura de sinks, Bandit, `pip-audit`, `compileall`
e testes locais. Nenhum segredo foi lido ou exibido. Nenhum serviço externo ou ambiente de
produção foi atacado.

> Este arquivo é o **único relatório de segurança mantido no repositório**. Ele substitui e
> incorpora quatro análises anteriores (05/09, 12/09, 17/09 e 21/09/2026), cada uma revalidando
> a anterior lendo o código diretamente. Os arquivos antigos foram removidos; o histórico
> resumido de cada rodada está na seção **Histórico de auditorias** no fim deste documento.

## Situação atual (22/09/2026)

**Nenhum achado aberto.** Os 9 pontos de atenção identificados na varredura de 21/09/2026
foram revisados de novo em 22/09/2026 e todos já estavam corrigidos no código atual da
branch `redesign-et` (working tree), sem necessidade de nova alteração.

| ID | Achado | Severidade original | Status em 22/09 | Evidência |
|---|---|---|---|---|
| SEC-01 | Matrícula criada antes da confirmação do pagamento | Média | **Corrigido** | `turma_id` fica pendurado na cobrança (`Pagamento.turma_id`); a `Matricula` só é criada em [`efetivar_turma_da_cobranca`](../dao/financeiroDAO.py#L729-L742), chamada por [`atualizar_status`](../dao/financeiroDAO.py#L715-L718) apenas quando `status == 'pago'`. Turma lotada gera evento `matricula_sem_vaga` em vez de estourar o limite. |
| SEC-02 | Professor recebe lista global de alunos ativos | Média (condicional) | **Não reproduz** | `alunos_disponiveis` só é montada `if eh_admin` em [turma_bp.py:242](../blueprints/turma_bp.py#L242); o template gate a mesma condição em [turma.html:60](../templates/turma.html#L60); a rota de matrícula usa `@admin_requerido` ([turma_bp.py:257](../blueprints/turma_bp.py#L257)), não decorator de professor. |
| SEC-03 | Verificação de lotação sujeita a corrida concorrente | Média | **Corrigido** | [`matricular_com_lotacao`](../dao/matriculaDAO.py#L21-L37) usa `.with_for_update()` na turma e checa a contagem dentro da mesma transação antes do insert. |
| SEC-04 | Estados e valores financeiros sem validação de domínio | Média | **Corrigido** | `Decimal` + `is_finite()` + limites de valor/duração + allowlist `STATUS_VALIDOS`/`FORMAS_PAGAMENTO_VALIDAS` em [adm_bp.py:148-155](../blueprints/adm_bp.py#L148-L155), [adm_bp.py:498-511](../blueprints/adm_bp.py#L498-L511) e [adm_bp.py:560-564](../blueprints/adm_bp.py#L560-L564). |
| SEC-05 | Confirmação de frequência não invalidada ao corrigir presença | Baixa | **Corrigido** | [`registrar_lote`](../dao/presencaDAO.py#L15-L23) zera `confirmada_aluno`/`confirmada_em` quando `presente` vira falso. |
| SEC-06 | `SECRET_KEY` sem requisito mínimo de força | Média (condicional) | **Corrigido** | [servidor.py:33-34](../servidor.py#L33-L34) exige `len(app.secret_key) >= 32`. |
| SEC-07 | Rate limiting com fallback em memória | Média (condicional) | **Corrigido** | [servidor.py:49-52](../servidor.py#L49-L52) falha no arranque se `APP_BASE_URL` for HTTPS e `RATELIMIT_STORAGE_URI` continuar `memory://`. |
| SEC-08 | Logs registram e-mails completos | Baixa | **Corrigido** | [`_destinatario_log`](../servicos/email.py#L15-L20) mascara (`ab***@dominio`) e é usado em todos os `logger.warning`/`logger.exception` com destinatário. |
| SEC-09 | Dependências sem lockfile/hash transitivo | Baixa | **Corrigido** (falta commitar) | `requirements.lock` existe (877 linhas, `pip-compile --generate-hashes`), mas ainda aparece como `??` no `git status` — só falta ser adicionado ao versionamento. |

### Pendências não relacionadas a segurança

- **`requirements.lock` não commitado** — gerado, mas fora do controle de versão ainda.
- **`tests/test_cadastro_publico_rejeita_cpf_invalido` falha por bug de teste**, não de
  produto: a asserção final consulta `Aluno.query` fora de um contexto de aplicação Flask
  (`RuntimeError: Working outside of application context`). Já era um dos dois "falsos
  positivos" documentados na rodada de 21/09.

## Controles verificados

- `CSRFProtect` inicializado e aplicado globalmente; única exceção é o webhook assinado do
  Mercado Pago em [pix_bp.py:328-329](../blueprints/pix_bp.py#L328-L329).
- Cookies com `HttpOnly`, `SameSite=Lax`, `Secure` configurável e lifetime limitado.
- Login limpa a sessão; sessões têm identificador e credencial revalidada; logout registra
  revogação no banco (`sessoes_revogadas`).
- Aluno, professor e administrador são revalidados no banco antes de acessar suas áreas.
- Acesso de professor à turma verifica o `professor_id` da turma.
- Pagamentos, comprovantes, fotos e presença do aluno têm verificação de propriedade.
- Webhook do Mercado Pago valida assinatura/tempo/referência e reconsulta a API — nunca
  confia apenas no status recebido no corpo do webhook.
- SQLAlchemy/ORM em todos os acessos revisados; nenhum sink de SQL injection confirmado.
- Curingas de `LIKE` escapados (`%`, `_`, `\`) em `financeiroDAO.py` e `usuarioDAO.py`.
- Uploads armazenados fora de `static/`, nome gerado por UUID, validação de conteúdo real
  (não apenas extensão/Content-Type) e limite de pixels.
- Jinja com autoescape; nenhum `|safe`, `render_template_string`, `innerHTML`, `eval` ou
  `document.write` em caminho explorável.
- Cabeçalhos de segurança (`CSP` com nonce, `X-Content-Type-Options`, `X-Frame-Options`,
  `Referrer-Policy`, `Permissions-Policy`, HSTS condicional) aplicados a toda resposta.
- Páginas autenticadas saem com `Cache-Control: no-store`.
- `pip-audit` sem vulnerabilidades conhecidas nas dependências declaradas.
- Bandit: 1 alerta médio (`app.run(host="0.0.0.0")`, protegido por `if __name__ == '__main__'`;
  produção usa Gunicorn) e alertas baixos, todos falsos positivos de constantes/`None`.

## Validação executada em 22/09/2026

- `pytest -q tests/test_contratacao_plano.py tests/test_datas_turma.py tests/test_seguranca.py
  tests/test_cadastro_administrativo.py tests/test_arranque_seguranca.py`: **127 passaram, 1
  falhou** (bug de teste descrito acima, não vulnerabilidade).
- Bandit sobre o projeto (excluindo testes/venv/graphify-out): mesma distribuição de alertas
  do relatório anterior (1 médio esperado, restante baixo/falso positivo).
- Nenhuma requisição foi enviada a Mercado Pago, Gmail, Redis ou PostgreSQL de produção.

## Histórico de auditorias

Resumo das rodadas anteriores — os arquivos originais foram removidos do repositório em
22/09/2026 para manter um único relatório vivo; o conteúdo relevante de cada um foi
revalidado e está refletido nas seções acima.

| Data | Escopo | Achados | Resultado |
|---|---|---|---|
| 05/09/2026 | Auditoria inicial completa (autenticação, autorização, CSRF, XSS, uploads, segredos) | 15 achados (F1–F15) | Todos corrigidos e revalidados nas rodadas seguintes. |
| 12/09/2026 | Reauditoria de segurança/desempenho | 1 achado médio (tempo de resposta em `/recuperar_senha`) + itens de desempenho | Achado de segurança corrigido em 19/09 (ver A1 abaixo); itens de desempenho tratados parcialmente por desenho. |
| 17/09/2026 (atualizado 19/09) | Revalidação de F1–F15 + novos achados A1–A4 + varredura independente S1–S2 + fluxo OAuth do Mercado Pago | A1–A4 (recuperação de senha vazando tempo, `/perfil/dados` sem limite de tentativas nem validação de tamanho, enumeração de usuário/e-mail) e S1–S2 (logout não revogava sessão, páginas autenticadas sem `Cache-Control`) | Todos corrigidos em 19/09/2026. |
| 21/09/2026 | Foco nos fluxos recentes de matrícula, turma, presença e permissões de professor | SEC-01 a SEC-09 (0 alto, 6 médio, 3 baixo) | Todos confirmados corrigidos (ou não reprodutíveis) em 22/09/2026 — ver tabela **Situação atual** acima. |

**Nenhuma injeção de SQL, XSS refletido/armazenado/DOM, path traversal, IDOR, SSRF ou
segredo exposto foi encontrado em nenhuma das rodadas.**
