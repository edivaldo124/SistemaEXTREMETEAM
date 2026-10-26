# FINDINGS-DETAIL — achados confirmados de severidade média ou maior

Gerado a partir de `findings.json`. O achado confirmado de severidade **baixa** (`blueprints/google_login.py:callback:login-binds-unverified-registrant-account`) está descrito no REPORT.md, seção 3.2, e no próprio `findings.json`.

## [medium] Copied session cookie survives logout and becomes valid again after its revocation row is purged

**Fingerprint:** `servicos/autorizacao.py:revogar_sessao_atual:revocation-row-purged-while-refreshable-cookie-lives`

On logout, the session's sid is written to sessoes_revogadas with expira_em = now + PERMANENT_SESSION_LIFETIME (30 min) + 5 min. The model docstring states the assumption behind this: the row only has to outlive any copy of the cookie, because the last refresh came before logout. That assumption does not hold. The revocation table is checked only inside _sessao_ativa, which runs only from the protected-route helpers (aluno_autorizado, professor_autorizado, sessao_administrativa_valida). On any other request, such as GET / or GET /login, Flask's SESSION_REFRESH_EACH_REQUEST=True re-signs the permanent cookie with a fresh itsdangerous timestamp and the same sid, tipo_usuario and credential stamp. Someone holding a cookie copied before logout can keep it alive indefinitely by visiting public pages. Any later logout by any user deletes revocation rows whose expira_em has passed, including the victim's. After that, the revoked sid passes _sessao_ativa again. If the password is unchanged, the credential fingerprint still matches and the copied cookie regains full access to the victim's account. Professor and admin sessions use the same _sessao_ativa path.

### Causa raiz

Revocation is enforced only in the per-route authorization helpers, never before Flask refreshes the session cookie. The revocation row is kept for a fixed window based on the cookie lifetime, but a refreshable cookie has no absolute lifetime, so the row can be deleted while a refreshed copy of the revoked cookie is still valid.

### Comportamento esperado (invariante)

Once logout revokes a sid, no copy of that cookie should ever be accepted again or re-signed. Revoked sessions should be refused (cleared) before any refresh, or sessions should carry an absolute issue time that is enforced, so revocation rows can be purged once no copy can still be valid.

### Rastro ordenado

1. `entrypoint` — `servidor.py:412` (logout): POST /logout calls revogar_sessao_atual() and then session.clear() (lines 417-418). Only the victim's browser copy is cleared; a copy taken earlier still carries the same signed sid.
2. `propagation` — `servicos/autorizacao.py:58` (revogar_sessao_atual): The revocation row is created with expira_em = logout time + permanent_session_lifetime (30 min) + _FOLGA_REVOGACAO (5 min). This assumes no copy of the cookie can be refreshed after logout.
3. `propagation` — `servidor.py:98` (app.config.update): SESSION_REFRESH_EACH_REQUEST=True with a 30-minute permanent lifetime (line 94). Any request, including the public home route at servidor.py:374, which never consults sessoes_revogadas, re-signs the permanent cookie with a new timestamp and unchanged contents (same sid).
4. `propagation` — `servicos/autorizacao.py:55` (revogar_sessao_atual): The next logout by any user deletes every revocation row whose expira_em has passed, including the victim's row once logout + 35 min has elapsed.
5. `sink` — `servicos/autorizacao.py:82` (_sessao_ativa): With the row gone, db.session.get(SessaoRevogada, sid) returns None, so the revoked sid is accepted. aluno_autorizado (lines 129-137) then checks only esta_ativo and the credential fingerprint, both of which still match, and grants the session.

### Evidências

- `servicos/autorizacao.py:58` — expira_em = agora + current_app.permanent_session_lifetime + _FOLGA_REVOGACAO, a fixed retention of 35 minutes from logout.
- `servicos/autorizacao.py:55` — Every logout opportunistically deletes revocation rows where SessaoRevogada.expira_em < agora.
- `servidor.py:98` — SESSION_REFRESH_EACH_REQUEST=True, with PERMANENT_SESSION_LIFETIME=timedelta(minutes=30) at line 94; login sets session.permanent = True (blueprints/usuario_bp.py:196).
- `servicos/autorizacao.py:82` — The revocation lookup lives only in _sessao_ativa, which is called only from aluno_autorizado/professor_autorizado/sessao_administrativa_valida. No before_request hook in servidor.py (only preparar_nonce_csp at line 173) clears a revoked session.
- `servidor.py:374` — Public home route: it reads session but never calls an authorization helper, so a revoked cookie is refreshed there without any revocation check.

### Atacante e recurso afetado (fictícios)

- Atacante: Holder of a copied session cookie whose owner has since logged out.
- Recurso: sessão de um aluno fictício aprovado (o mesmo caminho vale para professor e admin).

### Entrada nativa e instruções limitadas (só local, em sandbox)

Entradas:
- `Cookie: session=<value copied before the victim's logout>; GET / at T0+25 min and T0+50 min; another user's login and logout at T0+40 min; GET /perfil at T0+55 min`

Passos:
1. In the approved sandbox, using the project test configuration (SQLite, memory:// limiter), create two approved dummy students without an outer app context.
2. Log in as the victim with POST /login, save the session cookie value, and confirm that GET /perfil returns 200.
3. Victim POSTs /logout (T0). Confirm the sessoes_revogadas row for the sid exists.
4. Install the copied cookie on two new clients: an attacker client and a control client that is never refreshed.
5. Shift the itsdangerous and autorizacao clocks to T0+25 min. The attacker sends GET / and receives a re-signed cookie carrying the same sid and tipo_usuario=aluno.
6. At T0+40 min, the other student logs in and logs out. Confirm the victim's revocation row has been purged.
7. At T0+50 min, the attacker sends GET / again.
8. At T0+55 min, send GET /perfil from the control client and then from the attacker client.

### Resultado observado e invariante que ele prova

T0: the revocation row exists. T0+25: attacker GET / returns 200 with a re-issued cookie carrying the same sid. T0+40: after another user's logout, the victim's revocation row no longer exists. T0+55: the control client with the unrefreshed copy gets 302 /login (expired by max age), while the attacker's refreshed copy gets GET /perfil 200 with the victim's name in the body. The revoked session regained full access to the victim's account (agents/v01-sessao/artifacts/evidence/check-01.txt).

### Condições e contenção

- **authentication_level:** The attacker already holds a copy of a victim's session cookie taken before logout, for example from a shared-computer browser profile, a browser extension, or a TLS-inspecting proxy log. This is the threat the sessoes_revogadas table was added to stop.
- **user_interaction:** The victim logs out to end the session and does not change their password afterwards. A password change alters the credential fingerprint and still invalidates the copy.
- **timing_dependency:** The attacker sends a request to any public page at least once every 30 minutes until the victim's revocation row has been purged.
- **data_state:** Some user logs out after the victim's row has expired (logout + 35 min), which triggers the purge. This is ordinary application traffic.

**Severidade:** probabilidade low (The attacker must already hold a copied session cookie, keep refreshing it through public pages at least every 30 minutes, and the victim must not change their password. The purge itself happens through any other user's ordinary logout.); impacto medium (Full use of the victim's account (student PII, payments, profile changes) after the victim believed logout had ended the session. Demonstrated for an aluno session; professor and admin sessions share the same _sessao_ativa path in source.); geral **medium**. Confiança: high (Every trace line was re-read in current source, and the result was reproduced independently in the sandbox with the project's own app and test configuration. The refresh went through a different public route (GET /) than the hunter used, and a control client showed that the unrefreshed copy expires, which isolates the refresh-then-purge mechanism.)

### Correção no código e caso de regressão

Enforce revocation before Flask can refresh the cookie, and give sessions an absolute lifetime so revocation rows can be purged safely. (1) Add a before_request hook that calls session.clear() whenever a session that claims an identity (tipo_usuario present) fails _sessao_ativa(). A revoked cookie is then never re-signed. (2) Store an issue timestamp in iniciar_sessao and reject sessions older than an absolute maximum (for example 12 h) in _sessao_ativa. Keep revocation rows at least that maximum plus a margin, so a row can only be purged once no copy can still be valid. Regression test: log out, refresh the copied cookie through a public page, purge the expired rows, and assert that /perfil still redirects to /login.

`servicos/autorizacao.py`:

```python
import time

VIDA_MAXIMA_SESSAO = timedelta(hours=12)
CHAVE_EMISSAO = 'emitida_em'

def iniciar_sessao():
    session[CHAVE_SESSAO] = secrets.token_urlsafe(16)
    session[CHAVE_EMISSAO] = int(time.time())

def _sessao_ativa():
    from config import db
    from modelos.sessao_revogada import SessaoRevogada

    sid = session.get(CHAVE_SESSAO)
    emitida = session.get(CHAVE_EMISSAO)
    if not sid or not isinstance(sid, str) or not isinstance(emitida, int):
        return False
    if time.time() - emitida > VIDA_MAXIMA_SESSAO.total_seconds():
        return False
    if g.get('_sessao_conferida') == sid:
        return True
    if db.session.get(SessaoRevogada, sid) is not None:
        return False
    g._sessao_conferida = sid
    return True

# in revogar_sessao_atual:
#     expira_em=agora + VIDA_MAXIMA_SESSAO + _FOLGA_REVOGACAO
```

`servidor.py`:

```python
from servicos import autorizacao

@app.before_request
def descartar_sessao_revogada():
    if session.get('tipo_usuario') and not autorizacao._sessao_ativa():
        session.clear()
```
