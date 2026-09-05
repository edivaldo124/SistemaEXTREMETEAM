from datetime import date, datetime, timedelta
from decimal import Decimal

from sqlalchemy import func, or_

from config import db
from modelos.matricula import Matricula
from modelos.pagamento import Pagamento
from modelos.pagamento_evento import PagamentoEvento
from modelos.solicitacao_plano import (
    STATUS_CANCELADA,
    STATUS_EFETIVADA,
    STATUS_PENDENTE,
    TIPO_DOWNGRADE,
    TIPO_UPGRADE,
    SolicitacaoMudancaPlano,
)
from modelos.usuario import Aluno
from servicos import planos as regras_plano

# Estados "fechados": não geram mais cobrança Pix nova nem esperam decisão de ninguém.
STATUS_FECHADOS = ('pago', 'cancelado', 'reembolsado')

# Estados "em aberto": ainda pedem alguma ação (do aluno ou de uma decisão pendente).
STATUS_ABERTOS = ('pendente', 'atrasado', 'em_processamento', 'em_analise', 'recusado')

# Rótulo humano de cada status interno - usado nos badges (nunca só a cor comunica o estado).
ROTULO_STATUS = {
    'pendente': 'Pendente',
    'atrasado': 'Vencida',
    'em_processamento': 'Processando',
    'em_analise': 'Em análise',
    'pago': 'Paga',
    'recusado': 'Recusada',
    'reembolsado': 'Reembolsada',
    'cancelado': 'Cancelada',
}

# Texto do botão principal do card "Minha mensalidade" para cada status.
ROTULO_ACAO_STATUS = {
    'pendente': 'Pagar agora',
    'atrasado': 'Regularizar',
    'em_processamento': 'Ver situação',
    'em_analise': 'Ver situação',
    'pago': 'Ver comprovante',
    'recusado': 'Tentar novamente',
    'reembolsado': 'Ver detalhes',
    'cancelado': 'Ver detalhes',
}


def rotulo_status(status):
    return ROTULO_STATUS.get(status, (status or '').capitalize())


def rotulo_acao(status):
    return ROTULO_ACAO_STATUS.get(status, 'Ver detalhes')


def mensalidade_destaque(pagamentos):
    """Escolhe a mensalidade mais relevante para o card 'Minha mensalidade':
    a mais próxima de vencer entre as em aberto ou, se não houver nenhuma em
    aberto, a mais recente já encerrada (paga/reembolsada/cancelada)."""
    abertos = [p for p in pagamentos if p.status in STATUS_ABERTOS]
    if abertos:
        return sorted(abertos, key=lambda p: p.vencimento)[0]

    fechados = [p for p in pagamentos if p.status not in STATUS_ABERTOS]
    if fechados:
        return sorted(fechados, key=lambda p: p.vencimento, reverse=True)[0]

    return None


# Códigos devolvidos por PagamentoDAO.contratar_plano - a rota traduz cada um numa
# mensagem para o aluno. Ter um código (em vez de só o pagamento) é o que permite a
# rota distinguir "já está pago" de "criei a cobrança" sem reinspecionar o banco.
CONTRATACAO_COBRANCA_CRIADA = 'cobranca_criada'
CONTRATACAO_COBRANCA_REUTILIZADA = 'cobranca_reutilizada'
CONTRATACAO_COBRANCA_REPLANEJADA = 'cobranca_replanejada'
CONTRATACAO_RENOVACAO_CRIADA = 'renovacao_criada'
CONTRATACAO_JA_ATIVO = 'ja_ativo'
CONTRATACAO_AGUARDANDO_DECISAO = 'aguardando_decisao'
CONTRATACAO_COBRANCA_EM_ANDAMENTO = 'cobranca_em_andamento'
CONTRATACAO_MUDANCA_AGENDADA = 'mudanca_agendada'
CONTRATACAO_MUDANCA_JA_EXISTE = 'mudanca_ja_existe'
CONTRATACAO_MUDANCA_CONFLITANTE = 'mudanca_conflitante'
CONTRATACAO_MUDANCA_SEM_VIGENCIA = 'mudanca_sem_vigencia'
CONTRATACAO_MESMO_PLANO = 'mesmo_plano'

ACAO_CONTRATAR = 'contratar'
ACAO_RENOVAR = 'renovar'
ACAO_AGENDAR_MUDANCA = 'agendar_mudanca'
ACOES_VALIDAS = (ACAO_CONTRATAR, ACAO_RENOVAR, ACAO_AGENDAR_MUDANCA)


class ResultadoContratacao:
    """O que aconteceu numa tentativa de contratar/renovar/trocar de plano."""

    def __init__(self, codigo, *, pagamento=None, solicitacao=None):
        self.codigo = codigo
        self.pagamento = pagamento
        self.solicitacao = solicitacao

    @property
    def gerou_cobranca(self):
        return self.pagamento is not None and self.codigo in (
            CONTRATACAO_COBRANCA_CRIADA,
            CONTRATACAO_COBRANCA_REUTILIZADA,
            CONTRATACAO_COBRANCA_REPLANEJADA,
            CONTRATACAO_RENOVACAO_CRIADA,
        )


class SolicitacaoPlanoDAO:
    """Persistência dos pedidos de troca de plano agendados para a próxima renovação."""

    @staticmethod
    def pendente_do_aluno(aluno_id):
        return (
            SolicitacaoMudancaPlano.query
            .filter_by(aluno_id=aluno_id, status=STATUS_PENDENTE)
            .order_by(SolicitacaoMudancaPlano.id.desc())
            .first()
        )

    @staticmethod
    def listar_do_aluno(aluno_id):
        return (
            SolicitacaoMudancaPlano.query
            .filter_by(aluno_id=aluno_id)
            .order_by(SolicitacaoMudancaPlano.id.desc())
            .all()
        )

    @staticmethod
    def buscar_por_id(solicitacao_id):
        return SolicitacaoMudancaPlano.query.filter_by(id=solicitacao_id).first()

    @staticmethod
    def bloquear_pendente_do_aluno(aluno_id):
        """Mesma trava de linha usada nas mensalidades: dois cliques simultâneos em
        "Agendar troca" são serializados e o segundo enxerga o pedido do primeiro."""
        return (
            SolicitacaoMudancaPlano.query
            .filter_by(aluno_id=aluno_id, status=STATUS_PENDENTE)
            .with_for_update()
            .order_by(SolicitacaoMudancaPlano.id.desc())
            .first()
        )

    @staticmethod
    def cancelar(solicitacao, *, ator, observacao=None):
        if solicitacao.status != STATUS_PENDENTE:
            return False
        solicitacao.status = STATUS_CANCELADA
        solicitacao.cancelado_em = datetime.utcnow()
        solicitacao.cancelado_por = ator
        if observacao:
            solicitacao.observacao = observacao[:255]
        db.session.commit()
        return True


class PagamentoDAO:
    # ---------------- Contratação, renovação e troca de plano ----------------

    @staticmethod
    def _cobranca_online_ativa(pagamento):
        """True se já existe um Pix ou um checkout válido emitido para esta cobrança.

        Enquanto existir, o valor da mensalidade não pode mudar: a conciliação compara o
        valor confirmado pelo provedor com o do banco e recusaria o pagamento por
        divergência - o aluno pagaria e não receberia a baixa.
        """
        return PagamentoDAO.pix_ainda_valido(pagamento) or PagamentoDAO.checkout_ainda_valido(pagamento)

    @staticmethod
    def _pagamentos_do_aluno(aluno_id):
        return Pagamento.query.filter_by(aluno_id=aluno_id).all()

    @staticmethod
    def _nova_cobranca(*, aluno, plano, pagamentos, hoje, ator, tipo_evento, detalhe):
        inicio, fim = regras_plano.periodo_para_nova_cobranca(pagamentos, plano, hoje=hoje)
        pagamento = Pagamento(
            aluno_id=aluno.id,
            plano_id=plano.id,
            # O preço vem sempre do plano persistido - o navegador não envia valor nenhum.
            valor=regras_plano.preco(plano),
            # Vence no primeiro dia do período que ela paga: uma renovação antecipada
            # nasce com vencimento futuro e por isso não entra como "Vencida".
            vencimento=inicio,
            status='pendente',
            competencia=inicio.strftime('%Y-%m'),
            vigencia_inicio=inicio,
            vigencia_fim=fim,
        )
        db.session.add(pagamento)
        db.session.flush()
        db.session.add(PagamentoEvento(
            pagamento_id=pagamento.id, tipo=tipo_evento, detalhe=detalhe, ator=ator,
        ))
        return pagamento

    @staticmethod
    def _replanejar_cobranca(pagamento, *, plano, pagamentos, hoje, ator):
        """Troca o plano de uma cobrança ainda não paga em vez de abrir uma segunda.

        O aluno mudou de ideia antes de pagar: reaproveitar a mesma linha evita deixar
        duas cobranças abertas disputando o mesmo período.
        """
        plano_antigo = pagamento.plano.nome_plano if pagamento.plano else '—'
        demais = [p for p in pagamentos if p.id != pagamento.id]
        inicio, fim = regras_plano.periodo_para_nova_cobranca(demais, plano, hoje=hoje)
        pagamento.plano_id = plano.id
        pagamento.valor = regras_plano.preco(plano)
        pagamento.vencimento = inicio
        pagamento.competencia = inicio.strftime('%Y-%m')
        pagamento.vigencia_inicio = inicio
        pagamento.vigencia_fim = fim
        db.session.add(PagamentoEvento(
            pagamento_id=pagamento.id, tipo='cobranca_replanejada',
            detalhe=f'Plano da cobrança em aberto alterado de {plano_antigo} para {plano.nome_plano}.',
            ator=ator,
        ))
        return pagamento

    @staticmethod
    def _efetivar_solicitacao(solicitacao, *, pagamento=None, aluno=None):
        solicitacao.status = STATUS_EFETIVADA
        solicitacao.efetivado_em = datetime.utcnow()
        if pagamento is not None:
            solicitacao.pagamento_efetivacao_id = pagamento.id
        if aluno is not None:
            aluno.plano_id = solicitacao.plano_destino_id

    @staticmethod
    def efetivar_mudancas_por_prazo(aluno, *, hoje=None):
        """Aplica um pedido agendado cujo período de origem já terminou sem renovação.

        Trocar o plano do cadastro aqui não libera nada: os benefícios do novo período
        continuam dependendo de uma mensalidade paga. Sem isto, um aluno que pediu a
        troca e deixou o plano vencer continuaria aparecendo no plano antigo.
        """
        hoje = hoje or date.today()
        solicitacao = SolicitacaoPlanoDAO.pendente_do_aluno(aluno.id)
        if not solicitacao or not solicitacao.vigencia_a_partir_de:
            return None
        if solicitacao.vigencia_a_partir_de > hoje:
            return None

        pagamentos = PagamentoDAO._pagamentos_do_aluno(aluno.id)
        if regras_plano.vigencia_ativa(pagamentos, hoje=hoje):
            # O aluno pagou outro período depois de pedir a troca: a mudança espera o
            # fim dessa vigência em vez de valer no meio de um período já pago.
            return None
        if regras_plano.cobranca_pendente(pagamentos):
            # Existe cobrança em aberto/em decisão: quem aplica a troca é ela.
            return None

        PagamentoDAO._efetivar_solicitacao(solicitacao, aluno=aluno)
        db.session.commit()
        return solicitacao

    @staticmethod
    def contratar_plano(*, aluno, plano, acao=ACAO_CONTRATAR, hoje=None, ator=None):
        """Único caminho pelo qual o aluno contrata, renova ou agenda a troca de plano.

        Todas as regras são reavaliadas aqui a partir do banco, com trava de linha no
        aluno: o que o formulário pediu é apenas uma intenção. Um clique repetido, dois
        envios do mesmo POST ou um `acao` forjado caem exatamente nas mesmas validações
        e nunca produzem uma segunda cobrança para um período já pago ou já em análise.
        """
        hoje = hoje or date.today()
        ator = ator or aluno.login

        # Serializa requisições concorrentes do mesmo aluno: a segunda espera a primeira
        # terminar e já enxerga a cobrança/solicitação recém-criada. (No SQLite dos
        # testes o SQLAlchemy não emite FOR UPDATE - o resultado continua correto.)
        aluno = Aluno.query.filter_by(id=aluno.id).with_for_update().first() or aluno

        pagamentos = PagamentoDAO._pagamentos_do_aluno(aluno.id)
        PagamentoDAO._promover_vencidos(pagamentos, hoje=hoje)
        solicitacao = SolicitacaoPlanoDAO.bloquear_pendente_do_aluno(aluno.id)
        situacao = regras_plano.situacao_plano(
            aluno, pagamentos, solicitacao_mudanca=solicitacao, hoje=hoje,
        )

        # 1. Alguém já está decidindo sobre um pagamento feito: nada de nova cobrança.
        if situacao.aguardando_decisao:
            return ResultadoContratacao(
                CONTRATACAO_AGUARDANDO_DECISAO, pagamento=situacao.cobranca, solicitacao=solicitacao,
            )

        if acao == ACAO_AGENDAR_MUDANCA:
            return PagamentoDAO._agendar_mudanca(
                aluno=aluno, plano=plano, situacao=situacao, solicitacao=solicitacao,
                pagamentos=pagamentos, hoje=hoje, ator=ator,
            )

        # 2. Já existe cobrança a pagar. Reaproveita em vez de abrir outra.
        cobranca = situacao.cobranca
        if cobranca:
            plano_alvo, solicitacao_aplicavel = PagamentoDAO._plano_da_proxima_cobranca(
                plano, solicitacao, cobranca_inicio=regras_plano.intervalo_vigencia(cobranca)[0], hoje=hoje,
            )
            if PagamentoDAO._conflita_com_agendamento(plano, solicitacao, situacao, cobranca):
                return ResultadoContratacao(CONTRATACAO_MUDANCA_CONFLITANTE, solicitacao=solicitacao)
            if cobranca.plano_id == plano_alvo.id:
                return ResultadoContratacao(
                    CONTRATACAO_COBRANCA_REUTILIZADA, pagamento=cobranca, solicitacao=solicitacao,
                )
            if PagamentoDAO._cobranca_online_ativa(cobranca):
                return ResultadoContratacao(
                    CONTRATACAO_COBRANCA_EM_ANDAMENTO, pagamento=cobranca, solicitacao=solicitacao,
                )
            PagamentoDAO._replanejar_cobranca(
                cobranca, plano=plano_alvo, pagamentos=pagamentos, hoje=hoje, ator=ator,
            )
            if solicitacao_aplicavel:
                PagamentoDAO._efetivar_solicitacao(solicitacao_aplicavel, pagamento=cobranca, aluno=aluno)
            aluno.plano_id = plano_alvo.id
            PagamentoDAO._sincronizar_situacao(aluno, hoje=hoje)
            db.session.commit()
            return ResultadoContratacao(
                CONTRATACAO_COBRANCA_REPLANEJADA, pagamento=cobranca, solicitacao=solicitacao,
            )

        # 3. Período pago e vigente: nada a cobrar agora. Só uma renovação explícita
        #    (do PRÓXIMO período) pode gerar cobrança - nunca um novo clique em "pagar".
        if situacao.ativo:
            if acao != ACAO_RENOVAR:
                # O período já está pago. Nem o mesmo plano nem outro geram cobrança
                # aqui: renovar exige a ação explícita, trocar de plano é agendamento.
                return ResultadoContratacao(CONTRATACAO_JA_ATIVO, solicitacao=solicitacao)

            inicio_renovacao = regras_plano.inicio_proximo_periodo(pagamentos, hoje=hoje)
            plano_alvo, solicitacao_aplicavel = PagamentoDAO._plano_da_proxima_cobranca(
                plano, solicitacao, cobranca_inicio=inicio_renovacao, hoje=hoje,
            )
            if PagamentoDAO._conflita_com_agendamento(plano, solicitacao, situacao, cobranca=None):
                return ResultadoContratacao(CONTRATACAO_MUDANCA_CONFLITANTE, solicitacao=solicitacao)

            pagamento = PagamentoDAO._nova_cobranca(
                aluno=aluno, plano=plano_alvo, pagamentos=pagamentos, hoje=hoje, ator=ator,
                tipo_evento='renovacao_antecipada',
                detalhe=(f'Cobrança do próximo período ({plano_alvo.nome_plano}) criada '
                         f'antes do fim da vigência atual.'),
            )
            if solicitacao_aplicavel:
                PagamentoDAO._efetivar_solicitacao(solicitacao_aplicavel, pagamento=pagamento, aluno=aluno)
                db.session.add(PagamentoEvento(
                    pagamento_id=pagamento.id, tipo='mudanca_plano_efetivada',
                    detalhe=(f'Mudança de plano solicitada em '
                             f'{solicitacao_aplicavel.criado_em.strftime("%d/%m/%Y")} aplicada a esta cobrança.'),
                    ator=ator,
                ))
            PagamentoDAO._sincronizar_situacao(aluno, hoje=hoje)
            db.session.commit()
            return ResultadoContratacao(
                CONTRATACAO_RENOVACAO_CRIADA, pagamento=pagamento, solicitacao=solicitacao,
            )

        # 4. Sem vigência e sem cobrança em aberto: contratação/renovação normal.
        plano_alvo, solicitacao_aplicavel = PagamentoDAO._plano_da_proxima_cobranca(
            plano, solicitacao, cobranca_inicio=hoje, hoje=hoje,
        )
        pagamento = PagamentoDAO._nova_cobranca(
            aluno=aluno, plano=plano_alvo, pagamentos=pagamentos, hoje=hoje, ator=ator,
            tipo_evento='plano_contratado',
            detalhe=f'Cobrança criada para contratação do plano {plano_alvo.nome_plano}.',
        )
        if solicitacao_aplicavel:
            PagamentoDAO._efetivar_solicitacao(solicitacao_aplicavel, pagamento=pagamento, aluno=aluno)
        aluno.plano_id = plano_alvo.id
        PagamentoDAO._sincronizar_situacao(aluno, hoje=hoje)
        db.session.commit()
        return ResultadoContratacao(
            CONTRATACAO_COBRANCA_CRIADA, pagamento=pagamento, solicitacao=solicitacao,
        )

    @staticmethod
    def _conflita_com_agendamento(plano_pedido, solicitacao, situacao, cobranca):
        """Com uma troca já agendada, só dois planos fazem sentido num pedido de
        renovação: o que está valendo (renovar "o meu plano", que a troca redireciona) e
        o destino agendado. Pedir um terceiro é conflitante - o aluno precisa cancelar a
        solicitação antes, para não ficar com dois planos futuros disputando o período."""
        if not solicitacao or not solicitacao.esta_pendente:
            return False
        aceitos = {solicitacao.plano_destino_id}
        if solicitacao.plano_origem_id:
            aceitos.add(solicitacao.plano_origem_id)
        if situacao.plano is not None:
            aceitos.add(situacao.plano.id)
        if cobranca is not None:
            aceitos.add(cobranca.plano_id)
        return plano_pedido.id not in aceitos

    @staticmethod
    def _plano_da_proxima_cobranca(plano_pedido, solicitacao, *, cobranca_inicio, hoje):
        """A cobrança do período seguinte tem de nascer no plano que o aluno agendou.

        Devolve `(plano, solicitacao_a_efetivar)`. A solicitação só é aplicada quando a
        cobrança cobre um período que começa em/depois da data agendada - uma cobrança
        de um período anterior continua no plano antigo, como contratado.
        """
        if not solicitacao or not solicitacao.esta_pendente:
            return plano_pedido, None
        a_partir_de = solicitacao.vigencia_a_partir_de
        if a_partir_de and cobranca_inicio and cobranca_inicio < a_partir_de:
            return plano_pedido, None
        destino = solicitacao.plano_destino
        if not destino:
            return plano_pedido, None
        return destino, solicitacao

    @staticmethod
    def _agendar_mudanca(*, aluno, plano, situacao, solicitacao, pagamentos, hoje, ator):
        if not situacao.ativo:
            # Sem período pago em curso não há o que preservar: escolher o plano já vale
            # como contratação, e agendar só adiaria o acesso sem motivo.
            return ResultadoContratacao(CONTRATACAO_MUDANCA_SEM_VIGENCIA)

        # Referência da troca é o plano que a PRÓXIMA renovação usaria: se o aluno já
        # pagou o período seguinte em outro plano, é dele que ele está saindo.
        plano_vigente = situacao.plano_proxima_renovacao
        if plano_vigente and plano.id == plano_vigente.id:
            return ResultadoContratacao(CONTRATACAO_MESMO_PLANO, solicitacao=solicitacao)

        if solicitacao:
            if solicitacao.plano_destino_id == plano.id:
                return ResultadoContratacao(CONTRATACAO_MUDANCA_JA_EXISTE, solicitacao=solicitacao)
            return ResultadoContratacao(CONTRATACAO_MUDANCA_CONFLITANTE, solicitacao=solicitacao)

        valor_origem = regras_plano.preco(plano_vigente) if plano_vigente else None
        valor_destino = regras_plano.preco(plano)
        tipo = TIPO_DOWNGRADE if valor_origem is not None and valor_destino < valor_origem else TIPO_UPGRADE

        nova = SolicitacaoMudancaPlano(
            aluno_id=aluno.id,
            plano_origem_id=plano_vigente.id if plano_vigente else None,
            plano_destino_id=plano.id,
            valor_origem=valor_origem,
            valor_destino=valor_destino,
            tipo=tipo,
            # Vale a partir do primeiro dia livre: tudo que já foi pago (ou está em
            # análise) continua valendo no plano contratado, sem reembolso nem perda.
            vigencia_a_partir_de=regras_plano.inicio_proximo_periodo(pagamentos, hoje=hoje),
            criado_por=ator,
        )
        db.session.add(nova)
        if situacao.mensalidade_vigente is not None:
            db.session.flush()
            db.session.add(PagamentoEvento(
                pagamento_id=situacao.mensalidade_vigente.id, tipo='mudanca_plano_solicitada',
                detalhe=(f'Aluno agendou mudança para o plano {plano.nome_plano} '
                         f'a partir de {nova.vigencia_a_partir_de.strftime("%d/%m/%Y")}. '
                         f'O plano atual segue valendo até o fim do período pago.'),
                ator=ator,
            ))
        db.session.commit()
        return ResultadoContratacao(CONTRATACAO_MUDANCA_AGENDADA, solicitacao=nova)

    # ---------------- Vigência e situação denormalizada do aluno ----------------

    @staticmethod
    def _promover_vencidos(pagamentos, hoje=None):
        """`pendente` vira `atrasado` depois do vencimento. Não altera nada além disso -
        uma cobrança de período futuro tem vencimento futuro e continua pendente."""
        hoje = hoje or date.today()
        mudou = False
        for pagamento in pagamentos:
            if pagamento.status == 'pendente' and pagamento.vencimento and pagamento.vencimento < hoje:
                pagamento.status = 'atrasado'
                mudou = True
        return mudou

    @staticmethod
    def _primeiro_dia_livre(pagamento, referencia):
        """Primeiro dia não coberto por outra mensalidade do mesmo aluno."""
        demais = [p for p in PagamentoDAO._pagamentos_do_aluno(pagamento.aluno_id) if p.id != pagamento.id]
        return regras_plano.inicio_proximo_periodo(demais, hoje=referencia)

    @staticmethod
    def garantir_vigencia(pagamento, *, referencia=None):
        """Define o período coberto por uma mensalidade que ainda não tem um (lançamento
        manual do admin ou linha anterior a este recurso), sem nunca sobrescrever o que
        já existe.

        Encadeia ao fim do que já está comprometido: registrar em dinheiro o mês seguinte
        de quem já pagou o atual precisa somar 30 dias, não sobrepor o período em curso.
        """
        if pagamento.vigencia_inicio and pagamento.vigencia_fim:
            return
        referencia = referencia or pagamento.data_pagamento or pagamento.vencimento or date.today()
        inicio = PagamentoDAO._primeiro_dia_livre(pagamento, referencia)
        pagamento.vigencia_inicio = inicio
        pagamento.vigencia_fim = inicio + timedelta(days=regras_plano.duracao_dias(pagamento.plano) - 1)

    @staticmethod
    def abrir_vigencia(pagamento, *, referencia=None):
        """Abre o período de acesso no momento em que o pagamento é confirmado.

        Se a janela planejada já tinha terminado antes da confirmação (cobrança antiga
        quitada com atraso), o período é reaberto a partir do primeiro dia livre com a
        mesma duração contratada - senão o aluno pagaria por dias que já passaram e
        continuaria sem acesso. Uma renovação antecipada (janela ainda futura) não é
        tocada: ela já nasceu no período certo.
        """
        referencia = referencia or pagamento.data_pagamento or date.today()
        PagamentoDAO.garantir_vigencia(pagamento, referencia=referencia)

        inicio, fim = pagamento.vigencia_inicio, pagamento.vigencia_fim
        if not inicio or not fim or fim >= referencia:
            return

        duracao = (fim - inicio).days + 1
        novo_inicio = PagamentoDAO._primeiro_dia_livre(pagamento, referencia)
        pagamento.vigencia_inicio = novo_inicio
        pagamento.vigencia_fim = novo_inicio + timedelta(days=duracao - 1)
        db.session.add(PagamentoEvento(
            pagamento_id=pagamento.id, tipo='vigencia_ajustada',
            detalhe=(f'Pagamento confirmado após o fim da janela original '
                     f'({inicio.strftime("%d/%m/%Y")} a {fim.strftime("%d/%m/%Y")}); '
                     f'período de {duracao} dias reaberto a partir de {novo_inicio.strftime("%d/%m/%Y")}.'),
            ator='sistema',
        ))

    @staticmethod
    def _sincronizar_situacao(aluno, *, hoje=None):
        """Reescreve os campos denormalizados do aluno a partir das mensalidades.

        `Aluno.mensalidade` e `Aluno.data_vencimento` passam a ser sempre derivados: era
        a divergência entre esses dois campos e o histórico financeiro que fazia a área
        do aluno pedir pagamento de um plano já pago.
        """
        if aluno is None:
            return
        hoje = hoje or date.today()
        pagamentos = PagamentoDAO._pagamentos_do_aluno(aluno.id)
        situacao = regras_plano.situacao_plano(aluno, pagamentos, hoje=hoje)

        validade = situacao.valido_ate
        aluno.data_vencimento = validade.strftime('%Y-%m-%d') if validade else None

        if situacao.ativo:
            aluno.mensalidade = 'Em Dia'
        elif situacao.aguardando_decisao:
            aluno.mensalidade = 'Em Análise'
        else:
            aluno.mensalidade = 'Pendente'

        # `plano_id` NÃO é reescrito aqui: ele é o plano do cadastro, que o admin edita.
        # O plano que vale de fato sai sempre de `situacao.plano` (derivado das
        # mensalidades) - sobrescrever esta coluna desfazia a escolha do admin em
        # silêncio no formulário de detalhes do aluno.

    @staticmethod
    def sincronizar_situacao_do_aluno(aluno, *, hoje=None):
        PagamentoDAO._sincronizar_situacao(aluno, hoje=hoje)
        db.session.commit()

    @staticmethod
    def salvar(pagamento):
        db.session.add(pagamento)
        db.session.commit()

    @staticmethod
    def listar_por_aluno(aluno_id):
        pagamentos = Pagamento.query.filter_by(aluno_id=aluno_id).order_by(Pagamento.vencimento.desc()).all()
        if PagamentoDAO._promover_vencidos(pagamentos):
            db.session.commit()
        return pagamentos

    @staticmethod
    def buscar_por_id(pagamento_id):
        return Pagamento.query.filter_by(id=pagamento_id).first()

    @staticmethod
    def mapa_por_aluno(aluno_ids=None):
        """Mensalidades agrupadas por aluno numa consulta só.

        Usado pelas telas que precisam da situação de MUITOS alunos (avisos e cobrança
        em massa): chamar `listar_por_aluno` num laço fazia um SELECT e um COMMIT por
        aluno.
        """
        consulta = Pagamento.query
        if aluno_ids is not None:
            consulta = consulta.filter(Pagamento.aluno_id.in_(list(aluno_ids) or [-1]))
        pagamentos = consulta.all()
        if PagamentoDAO._promover_vencidos(pagamentos):
            db.session.commit()

        mapa = {}
        for pagamento in pagamentos:
            mapa.setdefault(pagamento.aluno_id, []).append(pagamento)
        return mapa

    @staticmethod
    def atualizar_status(pagamento_id, status, forma_pagamento):
        pagamento = Pagamento.query.filter_by(id=pagamento_id).first()

        if pagamento:
            pagamento.status = status
            pagamento.forma_pagamento = forma_pagamento

            if status == 'pago':
                pagamento.data_pagamento = date.today()
                PagamentoDAO.abrir_vigencia(pagamento, referencia=pagamento.data_pagamento)
            else:
                pagamento.data_pagamento = None

            PagamentoDAO._sincronizar_situacao(pagamento.aluno)
            db.session.commit()
            return True

        return False

    @staticmethod
    def buscar_por_provider_payment_id(provider_payment_id):
        return Pagamento.query.filter_by(provider_payment_id=provider_payment_id).first()

    @staticmethod
    def buscar_por_external_reference(external_reference):
        """Acha a mensalidade por qualquer uma das duas referências persistidas.

        O Pix direto grava em `external_reference`; o Checkout Pro em
        `checkout_external_reference`. O webhook não sabe de antemão qual dos dois
        originou a notificação, então procura nas duas colunas.
        """
        if not external_reference:
            return None
        return Pagamento.query.filter(
            or_(
                Pagamento.external_reference == external_reference,
                Pagamento.checkout_external_reference == external_reference,
            )
        ).first()

    @staticmethod
    def bloquear_para_atualizacao(pagamento_id):
        """Relê a mensalidade com trava de linha (SELECT ... FOR UPDATE).

        Serializa cliques simultâneos em "Outras formas de pagamento": no Postgres de
        produção a segunda requisição espera a primeira terminar e então enxerga a
        preferência recém-criada, em vez de criar outra. No SQLite dos testes o SQLAlchemy
        simplesmente não emite a cláusula — o comportamento continua correto, só sem trava.
        """
        return Pagamento.query.filter_by(id=pagamento_id).with_for_update().first()

    @staticmethod
    def buscar_por_checkout_preference_id(preference_id):
        if not preference_id:
            return None
        return Pagamento.query.filter_by(checkout_preference_id=preference_id).first()

    @staticmethod
    def pix_ainda_valido(pagamento):
        """True se a cobrança Pix já gerada para este pagamento ainda pode ser
        reaproveitada (mesma idempotency_key), em vez de criar uma nova.

        Exige o copia-e-cola persistido: `provider_payment_id` também é preenchido por
        pagamentos do Checkout Pro (cartão/boleto), e reaproveitar um deles como se
        fosse Pix devolveria uma cobrança sem código nenhum para o aluno copiar.
        """
        if not pagamento.provider_payment_id or pagamento.status in STATUS_FECHADOS:
            return False
        if not pagamento.pix_copia_cola:
            return False
        if pagamento.data_expiracao and pagamento.data_expiracao <= datetime.utcnow():
            return False
        return True

    @staticmethod
    def checkout_ainda_valido(pagamento, *, ambiente_atual=None):
        """True se a preferência do Checkout Pro já criada pode ser reaproveitada.

        Só reutiliza quando tudo continua batendo: mensalidade ainda em aberto, URL
        gravada, preferência não expirada, ambiente igual ao atual (não devolve um
        checkout de sandbox para quem já migrou para produção) e, principalmente, valor
        idêntico ao da mensalidade — se o admin alterou o valor, a preferência antiga
        cobraria a quantia errada e o pagamento seria barrado na conferência.
        """
        if not pagamento.checkout_preference_id or not pagamento.checkout_url:
            return False
        if pagamento.status in STATUS_FECHADOS:
            return False
        if pagamento.checkout_expira_em and pagamento.checkout_expira_em <= datetime.utcnow():
            return False
        if ambiente_atual and pagamento.checkout_ambiente != ambiente_atual:
            return False
        if pagamento.checkout_valor is None or Decimal(str(pagamento.checkout_valor)) != Decimal(str(pagamento.valor)):
            return False
        return True

    @staticmethod
    def salvar_dados_checkout(pagamento, *, preference_id, external_reference, url_checkout,
                               ambiente, expira_em, ator='sistema'):
        pagamento.provider = 'mercado_pago'
        pagamento.checkout_preference_id = preference_id
        pagamento.checkout_external_reference = external_reference
        pagamento.checkout_url = url_checkout
        pagamento.checkout_ambiente = ambiente
        pagamento.checkout_valor = Decimal(str(pagamento.valor))
        pagamento.checkout_criado_em = datetime.utcnow()
        pagamento.checkout_expira_em = expira_em
        db.session.add(PagamentoEvento(
            pagamento_id=pagamento.id, tipo='checkout_criado',
            detalhe=f'Preferência do Checkout Pro criada ({ambiente}).', ator=ator,
        ))
        db.session.commit()

    @staticmethod
    def limpar_dados_checkout(pagamento):
        """Solta a preferência atual para que a próxima tentativa crie uma nova.

        Nunca mexe em status nem em provider_payment_id: descartar o link de checkout
        não pode alterar o que já foi confirmado sobre o pagamento.
        """
        pagamento.checkout_preference_id = None
        pagamento.checkout_external_reference = None
        pagamento.checkout_url = None
        pagamento.checkout_ambiente = None
        pagamento.checkout_valor = None
        pagamento.checkout_criado_em = None
        pagamento.checkout_expira_em = None
        db.session.commit()

    @staticmethod
    def registrar_evento(pagamento_id, tipo, detalhe=None, ator=None):
        db.session.add(PagamentoEvento(pagamento_id=pagamento_id, tipo=tipo, detalhe=detalhe, ator=ator))
        db.session.commit()

    @staticmethod
    def salvar_dados_pix(pagamento, *, provider_payment_id, external_reference, idempotency_key,
                          pix_copia_cola, ticket_url, data_expiracao):
        pagamento.provider = 'mercado_pago'
        pagamento.provider_payment_id = provider_payment_id
        pagamento.external_reference = external_reference
        pagamento.idempotency_key = idempotency_key
        pagamento.pix_copia_cola = pix_copia_cola
        pagamento.ticket_url = ticket_url
        pagamento.data_criacao_pix = datetime.utcnow()
        pagamento.data_expiracao = data_expiracao
        db.session.add(PagamentoEvento(
            pagamento_id=pagamento.id, tipo='pix_gerado',
            detalhe=f'Cobrança Pix criada (id provedor {provider_payment_id}).', ator='sistema',
        ))
        db.session.commit()

    @staticmethod
    def marcar_pago_via_webhook(pagamento, *, data_pagamento, forma_pagamento='pix'):
        """forma_pagamento vem do que o Mercado Pago confirmou na consulta à API
        ('pix', 'credit_card', 'boleto', 'account_money'...). O padrão continua 'pix'
        para não alterar o comportamento do fluxo Pix direto."""
        pagamento.status = 'pago'
        pagamento.data_pagamento = data_pagamento
        pagamento.forma_pagamento = (forma_pagamento or 'pix')[:30]
        pagamento.provider_status = 'approved'
        # O período só passa a valer agora: é a confirmação do pagamento que abre a
        # vigência, nunca a criação da cobrança.
        PagamentoDAO.abrir_vigencia(pagamento, referencia=data_pagamento)
        PagamentoDAO._sincronizar_situacao(pagamento.aluno)
        db.session.add(PagamentoEvento(
            pagamento_id=pagamento.id, tipo='webhook_aprovado',
            detalhe='Pagamento aprovado e confirmado pelo Mercado Pago.', ator='webhook_mercado_pago',
        ))
        db.session.commit()

    @staticmethod
    def marcar_reembolsado_via_webhook(pagamento):
        pagamento.status = 'reembolsado'
        pagamento.provider_status = 'refunded'
        PagamentoDAO._sincronizar_situacao(pagamento.aluno)
        db.session.add(PagamentoEvento(
            pagamento_id=pagamento.id, tipo='webhook_reembolso',
            detalhe='Pagamento reembolsado/estornado conforme notificação do Mercado Pago.',
            ator='webhook_mercado_pago',
        ))
        db.session.commit()

    @staticmethod
    def marcar_em_processamento_via_webhook(pagamento):
        if pagamento.status in STATUS_FECHADOS:
            return
        pagamento.status = 'em_processamento'
        pagamento.provider_status = 'in_process'
        PagamentoDAO._sincronizar_situacao(pagamento.aluno)
        db.session.add(PagamentoEvento(
            pagamento_id=pagamento.id, tipo='webhook_em_processamento',
            detalhe='Mercado Pago está analisando o pagamento.', ator='webhook_mercado_pago',
        ))
        db.session.commit()

    @staticmethod
    def marcar_recusado_via_webhook(pagamento, *, status_detail=None):
        if pagamento.status in STATUS_FECHADOS:
            return
        pagamento.status = 'recusado'
        pagamento.provider_status = 'rejected'
        pagamento.provider_status_detail = (status_detail or '')[:60] or None
        PagamentoDAO._sincronizar_situacao(pagamento.aluno)
        db.session.add(PagamentoEvento(
            pagamento_id=pagamento.id, tipo='webhook_recusado',
            detalhe='Pagamento recusado pelo Mercado Pago.', ator='webhook_mercado_pago',
        ))
        db.session.commit()

    # ---------------- Comprovante manual (dinheiro/transferência) ----------------

    @staticmethod
    def enviar_comprovante_manual(pagamento, *, arquivo_nome, ator):
        pagamento.comprovante_manual_arquivo = arquivo_nome
        pagamento.comprovante_manual_enviado_em = datetime.utcnow()
        pagamento.comprovante_manual_analisado_por = None
        pagamento.comprovante_manual_analisado_em = None
        pagamento.comprovante_manual_observacao = None
        pagamento.status = 'em_analise'
        PagamentoDAO._sincronizar_situacao(pagamento.aluno)
        db.session.add(PagamentoEvento(
            pagamento_id=pagamento.id, tipo='comprovante_enviado',
            detalhe='Aluno enviou comprovante manual para análise.', ator=ator,
        ))
        db.session.commit()

    @staticmethod
    def aprovar_comprovante_manual(pagamento, *, admin_login, observacao=None, data_pagamento=None,
                                    forma_pagamento='transferencia'):
        pagamento.status = 'pago'
        pagamento.data_pagamento = data_pagamento or date.today()
        pagamento.forma_pagamento = forma_pagamento
        pagamento.comprovante_manual_analisado_por = admin_login
        pagamento.comprovante_manual_analisado_em = datetime.utcnow()
        pagamento.comprovante_manual_observacao = observacao
        PagamentoDAO.abrir_vigencia(pagamento, referencia=pagamento.data_pagamento)
        PagamentoDAO._sincronizar_situacao(pagamento.aluno)
        db.session.add(PagamentoEvento(
            pagamento_id=pagamento.id, tipo='comprovante_aprovado',
            detalhe=observacao or 'Comprovante manual aprovado pela administração.', ator=admin_login,
        ))
        db.session.commit()

    @staticmethod
    def rejeitar_comprovante_manual(pagamento, *, admin_login, observacao=None):
        pagamento.status = 'atrasado' if pagamento.vencimento < date.today() else 'pendente'
        pagamento.comprovante_manual_analisado_por = admin_login
        pagamento.comprovante_manual_analisado_em = datetime.utcnow()
        pagamento.comprovante_manual_observacao = observacao
        PagamentoDAO._sincronizar_situacao(pagamento.aluno)
        db.session.add(PagamentoEvento(
            pagamento_id=pagamento.id, tipo='comprovante_rejeitado',
            detalhe=observacao or 'Comprovante manual rejeitado pela administração.', ator=admin_login,
        ))
        db.session.commit()

    @staticmethod
    def registrar_pagamento_manual(*, aluno_id, plano_id, valor, vencimento, competencia=None,
                                    data_pagamento=None, forma_pagamento='dinheiro', observacao=None, ator):
        """Lançamento manual de recebimento (dinheiro/transferência) feito pelo admin.
        Sempre nasce com provider='manual' e já fica 'pago' (o admin está confirmando
        um recebimento que já aconteceu, ao contrário do comprovante enviado pelo aluno,
        que fica 'em_analise' até ser revisado)."""
        pagamento = Pagamento(
            aluno_id=aluno_id, plano_id=plano_id, valor=valor, vencimento=vencimento,
            status='pago', data_pagamento=data_pagamento or date.today(),
            forma_pagamento=forma_pagamento, provider='manual', competencia=competencia,
        )
        db.session.add(pagamento)
        db.session.flush()
        PagamentoDAO.garantir_vigencia(pagamento)
        PagamentoDAO._sincronizar_situacao(pagamento.aluno)
        db.session.add(PagamentoEvento(
            pagamento_id=pagamento.id, tipo='manual_registrado',
            detalhe=observacao or f'Recebimento manual registrado ({forma_pagamento}).', ator=ator,
        ))
        db.session.commit()
        return pagamento

    # ---------------- Painel financeiro (admin) ----------------

    @staticmethod
    def _query_filtrada(*, inicio=None, fim=None, turma_id=None, plano_id=None, forma_pagamento=None,
                         status=None, busca_aluno=None):
        consulta = Pagamento.query.join(Aluno, Pagamento.aluno_id == Aluno.id)

        if inicio:
            consulta = consulta.filter(Pagamento.vencimento >= inicio)
        if fim:
            consulta = consulta.filter(Pagamento.vencimento <= fim)
        if turma_id:
            ids_alunos = [m.aluno_id for m in Matricula.query.filter_by(turma_id=turma_id).all()]
            consulta = consulta.filter(Pagamento.aluno_id.in_(ids_alunos or [-1]))
        if plano_id:
            consulta = consulta.filter(Pagamento.plano_id == plano_id)
        if forma_pagamento:
            consulta = consulta.filter(Pagamento.forma_pagamento == forma_pagamento)
        if status:
            consulta = consulta.filter(Pagamento.status == status)
        if busca_aluno:
            termo = busca_aluno.replace('\\', '\\\\').replace('%', '\\%').replace('_', '\\_')
            consulta = consulta.filter(Aluno.nome.ilike(f'%{termo}%', escape='\\'))

        return consulta

    @staticmethod
    def listar_filtrado(**filtros):
        # Reaproveita a mesma promoção pendente->atrasado usada na área do aluno.
        pendentes_vencidos = Pagamento.query.filter(Pagamento.status == 'pendente', Pagamento.vencimento < date.today()).all()
        for p in pendentes_vencidos:
            p.status = 'atrasado'
        if pendentes_vencidos:
            db.session.commit()

        return PagamentoDAO._query_filtrada(**filtros).order_by(Pagamento.vencimento.desc()).all()

    @staticmethod
    def totais_periodo(*, inicio=None, fim=None):
        """Totais do painel financeiro - sempre calculados no backend a partir do banco,
        nunca somados no front. `inicio`/`fim` filtram pelo vencimento da mensalidade."""
        base = PagamentoDAO._query_filtrada(inicio=inicio, fim=fim)

        def soma(status_lista):
            valor = base.filter(Pagamento.status.in_(status_lista)).with_entities(func.coalesce(func.sum(Pagamento.valor), 0)).scalar()
            return Decimal(valor or 0)

        def conta(status_lista):
            return base.filter(Pagamento.status.in_(status_lista)).count()

        alunos_inadimplentes = (
            base.filter(Pagamento.status == 'atrasado')
            .with_entities(Pagamento.aluno_id).distinct().count()
        )

        return {
            'total_recebido': soma(['pago']),
            'total_pendente': soma(['pendente']),
            'total_vencido': soma(['atrasado']),
            'total_em_analise': soma(['em_analise']),
            'qtd_pago': conta(['pago']),
            'qtd_pendente': conta(['pendente']),
            'qtd_vencido': conta(['atrasado']),
            'qtd_em_analise': conta(['em_analise']),
            'alunos_inadimplentes': alunos_inadimplentes,
        }
