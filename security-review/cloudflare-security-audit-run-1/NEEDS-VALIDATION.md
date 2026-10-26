# NEEDS-VALIDATION — pistas sem severidade

Pistas sustentadas pelo código, com um bloqueio exato fora do que dá para observar no código ou localmente. **Não** são vulnerabilidades confirmadas e não recebem severidade. Nenhum plano abaixo envolve tráfego contra produção.

## Unquoted student-controlled display name in the To header can add an attacker recipient to email-ownership token links

**Fingerprint:** `servicos/gmail_conta.py:enviar:to-header-unquoted-display-name`

gmail_conta.enviar builds the To header as f'{nome} <{destinatario}>' and never quotes or encodes the display name. The student controls nome at /cadastrar and at /perfil/dados, where the only check is length (at most 150). A name such as 'Ana <ana.atk@attacker.test>, Ana' therefore produces the raw header 'To: Ana <ana.atk@attacker.test>, Ana <victim@...>', which parses as two recipients. This happens on the /perfil/email confirmation message, which goes to an address the student only claims to own, and on the /cadastrar verification message. If the Gmail API delivers to every To address, the attacker receives the ownership-proof token for an address they do not control. The verifier reproduced this locally in a sandbox with the Gmail send call mocked. The token taken from the raw message confirmed dummy.victim@example.org onto the attacker's account. The signup verification message showed the same two-recipient To header. A follow-on effect is visible in source: Google login picks the Aluno only by email (google_login.py:144) and opens a session for an approved, active account (google_login.py:175-180). So if the victim later chooses 'Sign in with Google' with that address, they land in the attacker-controlled account. That step needs the victim to start a Google login. The address must also not already belong to another account, because solicitar_troca_email rejects duplicates at usuario_bp.py:787.

### Causa raiz alegada

servicos/gmail_conta.py:149 interpolates the raw, untrusted display name into an address-list header. It should build a single email.headerregistry.Address(display_name=nome, addr_spec=destinatario), which quotes the name, or strip address-list syntax from the name. The verifier checked locally that using Address leaves exactly one recipient.

### Rastro do código

1. `entrypoint` — `blueprints/usuario_bp.py:689` (atualizar_dados_perfil): An authenticated student sets aluno.nome to an arbitrary string. The name is only length-checked (at most 150), after a current-password check. /cadastrar (usuario_bp.py:317) takes the signup name the same way.
2. `propagation` — `blueprints/usuario_bp.py:805` (solicitar_troca_email): The confirmation link for novo_email is sent through _enviar_em_segundo_plano with nome_destinatario=aluno.nome.
3. `propagation` — `servicos/email.py:65` (enviar_email): The name is passed unchanged to gmail_conta.enviar.
4. `propagation` — `servicos/gmail_conta.py:149` (enviar): The To header is built by string interpolation, so address-list syntax in the name adds a second recipient.
5. `sink` — `servicos/gmail_conta.py:153` (enviar): The raw RFC 5322 message is POSTed to the Gmail users.messages.send endpoint (SEND_URL, gmail_conta.py:26), which takes recipients from the message headers.

### Evidências verificadas

- `servicos/gmail_conta.py:149` — mensagem['To'] = f'{nome} <{destinatario}>'. Verifier run (agents/v03-to-header/artifacts/evidence/check-01.txt): raw header 'Ana <ana.atk@attacker.test>, Ana <dummy.victim@example.org>', and getaddresses returns ['ana.atk@attacker.test', 'dummy.victim@example.org'].
- `blueprints/usuario_bp.py:849` — The token taken from that raw message was used on GET /perfil/confirmar_email/<token>, which set aluno.email = email_pendente. ACCOUNT_EMAIL_AFTER_CONFIRM: dummy.victim@example.org (check-01). The hunters' runs h01 check-01 and h05 check-03 match this.
- `blueprints/usuario_bp.py:423` — The signup verification e-mail is queued through fila_email with nome_destinatario=nome, the raw signup name. Verifier run: the 'Verifique seu e-mail' message had To 'Bob <bob.atk@attacker.test>, Bob <dummy.victim2@example.org>', which is two recipients.
- `blueprints/google_login.py:144` — Google login selects the account only by email. After the attacker binds the victim's address, a victim who signs in with Google using that address gets a session on the attacker's account at google_login.py:175-180, provided the account is approved and active. The victim has to start that Google login.

### Fronteira afetada

Prova de posse de e-mail por link com token (confirmação de troca de e-mail e verificação do cadastro); por consequência, a escolha de conta no login com Google, que é feita pelo e-mail.

### Bloqueio exato

- Whether Gmail API users.messages.send actually delivers to every address in the raw To header, including the injected attacker address, is provider behavior. It is not visible in source and cannot be tested offline. Local evidence ends at the raw message, which has two parsed To recipients, and at the server accepting that message's token.

### Planos de resolução

- **Local (limitado, em sandbox):** Run agents/v03-to-header/artifacts/evidence/check-01.txt (test_v03.py) in the sandbox with the Gmail send call mocked. Confirm EMAIL_CHANGE_RECIPIENTS and the signup RECIPIENTS each list two addresses. After the fix, which sets mensagem['To'] = Address(display_name=nome, addr_spec=destinatario), confirm that getaddresses returns only destinatario (FIXED_RECIPIENTS in the same file shows this).
- **Observado pelo dono (sem tráfego de auditoria):** Use a test Gmail sender account connected to a non-production instance, plus two mailboxes the owner controls. Set a test student's name to 'Test <owner-mailbox-2@...>, X' and request an e-mail change to owner-mailbox-1. Check whether owner-mailbox-2 receives the 'Confirme seu novo e-mail' message containing the confirmation link. Do not use real student accounts or third-party addresses.

**Correção sugerida, se a entrega se confirmar:** montar o cabeçalho com `email.headerregistry.Address(display_name=nome, addr_spec=destinatario)`, que põe o nome entre aspas, e recusar `<`, `>`, `,`, `"` e caracteres de controle no nome. Teste de regressão: um nome malicioso deve resultar em exatamente um destinatário no `To`.
