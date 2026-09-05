"""Regras de vigência do plano do aluno.

Uma mensalidade paga cobre um intervalo fechado `[vigencia_inicio, vigencia_fim]`. É
esse intervalo - e não o texto livre de `Aluno.mensalidade`, nem a competência, nem a
simples existência de uma cobrança - que responde às três perguntas da área do aluno:

* o plano está ativo hoje e até quando?
* existe algo a pagar agora, ou o que existe é do PRÓXIMO período?
* há alguma decisão pendente (comprovante em análise, pagamento em processamento)?

Este módulo é só leitura: calcula e classifica, nunca escreve no banco. Quem persiste é
`dao.financeiroDAO.PagamentoDAO`.
"""

from datetime import date, timedelta
from decimal import Decimal

DURACAO_PADRAO_DIAS = 30

# Estados que exigem ação do próprio aluno para o período andar.
STATUS_A_PAGAR = ('pendente', 'atrasado', 'recusado')
# Estados que já estão nas mãos de outra pessoa/sistema: o aluno não deve ser
# incentivado a pagar de novo enquanto uma decisão está em curso.
STATUS_EM_DECISAO = ('em_analise', 'em_processamento')
# Períodos já comprometidos: ou foram pagos, ou aguardam decisão sobre um pagamento
# que já foi feito. Uma cobrança nova nunca pode sobrepor um destes.
STATUS_COMPROMETIDOS = ('pago',) + STATUS_EM_DECISAO

ESTADO_ATIVO = 'ativo'
ESTADO_AGUARDANDO_ANALISE = 'aguardando_analise'
ESTADO_EM_PROCESSAMENTO = 'em_processamento'
ESTADO_A_PAGAR = 'a_pagar'
ESTADO_RECUSADO = 'recusado'
ESTADO_VENCIDO = 'vencido'
ESTADO_SEM_PLANO = 'sem_plano'

ROTULO_ESTADO = {
    ESTADO_ATIVO: 'Plano ativo',
    ESTADO_AGUARDANDO_ANALISE: 'Aguardando análise',
    ESTADO_EM_PROCESSAMENTO: 'Pagamento em processamento',
    ESTADO_A_PAGAR: 'Pagamento pendente',
    ESTADO_RECUSADO: 'Pagamento recusado',
    ESTADO_VENCIDO: 'Plano vencido',
    ESTADO_SEM_PLANO: 'Sem plano',
}


def duracao_dias(plano):
    try:
        dias = int(getattr(plano, 'duracao_dias', None) or DURACAO_PADRAO_DIAS)
    except (TypeError, ValueError):
        dias = DURACAO_PADRAO_DIAS
    return max(dias, 1)


def preco(plano):
    return Decimal(str(getattr(plano, 'preco_plano', 0) or 0))


def intervalo_vigencia(pagamento):
    """Período coberto por uma mensalidade, em `(inicio, fim)`.

    Mensalidades lançadas antes deste recurso não têm as colunas preenchidas: para elas
    o intervalo é deduzido da data de pagamento (ou do vencimento) somada à duração do
    plano, para que o histórico antigo continue sendo lido corretamente.
    """
    inicio = pagamento.vigencia_inicio or pagamento.data_pagamento or pagamento.vencimento
    if not inicio:
        return None, None
    fim = pagamento.vigencia_fim
    if not fim:
        fim = inicio + timedelta(days=duracao_dias(pagamento.plano) - 1)
    return inicio, fim


def _ordenar_por_inicio(pagamentos):
    return sorted(pagamentos, key=lambda p: (intervalo_vigencia(p)[0] or date.min, p.id or 0))


def vigencia_ativa(pagamentos, hoje=None):
    """Mensalidade paga que cobre `hoje` - a de vigência mais longa, se houver várias."""
    hoje = hoje or date.today()
    candidatas = []
    for pagamento in pagamentos:
        if pagamento.status != 'pago':
            continue
        inicio, fim = intervalo_vigencia(pagamento)
        if inicio and fim and inicio <= hoje <= fim:
            candidatas.append((fim, pagamento.id or 0, pagamento))
    if not candidatas:
        return None
    return max(candidatas, key=lambda item: (item[0], item[1]))[2]


def cadeia_paga(pagamentos, hoje=None):
    """Sequência contínua de mensalidades pagas que começa na que cobre `hoje`.

    Renovar antecipadamente cria períodos encadeados (um começa no dia seguinte ao fim
    do anterior). A validade que interessa ao aluno é o fim de TODA essa corrente, não
    só do período em curso - senão quem já pagou a renovação vê uma data menor do que
    realmente comprou.
    """
    hoje = hoje or date.today()
    atual = vigencia_ativa(pagamentos, hoje=hoje)
    if not atual:
        return []

    pagos = {}
    for pagamento in pagamentos:
        if pagamento.status != 'pago':
            continue
        inicio, fim = intervalo_vigencia(pagamento)
        if inicio and fim:
            # Com dois períodos começando no mesmo dia, vale o que cobre mais tempo.
            atual_no_dia = pagos.get(inicio)
            if atual_no_dia is None or intervalo_vigencia(atual_no_dia)[1] < fim:
                pagos[inicio] = pagamento

    cadeia = [atual]
    fim_atual = intervalo_vigencia(atual)[1]
    while True:
        seguinte = pagos.get(fim_atual + timedelta(days=1))
        if not seguinte or seguinte in cadeia:
            break
        cadeia.append(seguinte)
        fim_atual = intervalo_vigencia(seguinte)[1]
    return cadeia


def fim_periodo_comprometido(pagamentos):
    """Último dia já comprometido (pago ou aguardando decisão). `None` se não houver."""
    fins = []
    for pagamento in pagamentos:
        if pagamento.status not in STATUS_COMPROMETIDOS:
            continue
        _, fim = intervalo_vigencia(pagamento)
        if fim:
            fins.append(fim)
    return max(fins) if fins else None


def plano_do_ultimo_periodo(pagamentos):
    """Plano do período comprometido mais distante - é ele que a próxima renovação
    repetiria. Com uma renovação antecipada já paga em outro plano, o "plano atual" para
    efeito de troca é esse, não o que está correndo hoje."""
    ultimo, fim_maior = None, None
    for pagamento in pagamentos:
        if pagamento.status not in STATUS_COMPROMETIDOS:
            continue
        _, fim = intervalo_vigencia(pagamento)
        if fim and (fim_maior is None or fim > fim_maior):
            ultimo, fim_maior = pagamento, fim
    return ultimo.plano if ultimo else None


def inicio_proximo_periodo(pagamentos, hoje=None):
    """Primeiro dia livre: encadeia ao fim do período comprometido para que renovar
    antes do vencimento não descarte os dias já pagos."""
    hoje = hoje or date.today()
    fim = fim_periodo_comprometido(pagamentos)
    if fim and fim >= hoje:
        return fim + timedelta(days=1)
    return hoje


def periodo_para_nova_cobranca(pagamentos, plano, hoje=None):
    inicio = inicio_proximo_periodo(pagamentos, hoje=hoje)
    return inicio, inicio + timedelta(days=duracao_dias(plano) - 1)


def cobranca_em_decisao(pagamentos):
    """Mensalidade com pagamento já enviado e aguardando decisão (análise/processamento)."""
    abertas = [p for p in pagamentos if p.status in STATUS_EM_DECISAO]
    return _ordenar_por_inicio(abertas)[0] if abertas else None


def cobranca_a_pagar(pagamentos):
    """Mensalidade que ainda depende de uma ação do aluno."""
    abertas = [p for p in pagamentos if p.status in STATUS_A_PAGAR]
    return _ordenar_por_inicio(abertas)[0] if abertas else None


def cobranca_pendente(pagamentos):
    """Qualquer cobrança que impeça abrir outra: a que aguarda decisão tem prioridade."""
    return cobranca_em_decisao(pagamentos) or cobranca_a_pagar(pagamentos)


class SituacaoPlano:
    """Retrato completo da situação do plano do aluno em uma data.

    Objeto de leitura, montado por `situacao_plano()` e consumido pelas telas e pelas
    validações de backend - as duas pontas olham exatamente para os mesmos campos, o
    que evita a tela oferecer um pagamento que a rota vai recusar (e vice-versa).
    """

    def __init__(self, *, estado, plano, mensalidade_vigente, cobranca, renovacao_antecipada,
                 proximo_periodo_inicio, solicitacao_mudanca, hoje, cadeia_paga=(),
                 plano_proxima_renovacao=None):
        self.estado = estado
        # Plano que vale HOJE.
        self.plano = plano
        # Plano que a PRÓXIMA renovação repetiria: normalmente o mesmo, mas difere quando
        # o aluno já pagou (ou está pagando) o período seguinte em outro plano. É esta a
        # referência para "trocar de plano" - a tela e o backend precisam usar a mesma.
        self.plano_proxima_renovacao = plano_proxima_renovacao or plano
        self.mensalidade_vigente = mensalidade_vigente
        self.cobranca = cobranca
        self.renovacao_antecipada = renovacao_antecipada
        self.proximo_periodo_inicio = proximo_periodo_inicio
        self.solicitacao_mudanca = solicitacao_mudanca
        self.hoje = hoje
        # Períodos pagos encadeados a partir de hoje (o primeiro é o em curso).
        self.cadeia_paga = list(cadeia_paga)

    @property
    def rotulo(self):
        return ROTULO_ESTADO.get(self.estado, 'Sem plano')

    @property
    def ativo(self):
        return self.estado == ESTADO_ATIVO

    @property
    def valido_ate(self):
        """Último dia de acesso já pago, somando as renovações antecipadas."""
        if not self.cadeia_paga:
            return None
        return intervalo_vigencia(self.cadeia_paga[-1])[1]

    @property
    def fim_periodo_atual(self):
        """Fim só do período em curso - o que a troca de plano tem de preservar."""
        if not self.mensalidade_vigente:
            return None
        return intervalo_vigencia(self.mensalidade_vigente)[1]

    @property
    def proximo_periodo_pago(self):
        """Renovação já paga que começa depois do período atual, quando existe."""
        return self.cadeia_paga[1] if len(self.cadeia_paga) > 1 else None

    @property
    def dias_restantes(self):
        if not self.valido_ate:
            return None
        return (self.valido_ate - self.hoje).days

    @property
    def aguardando_decisao(self):
        return bool(self.cobranca) and self.cobranca.status in STATUS_EM_DECISAO

    @property
    def pode_pagar(self):
        """Existe uma cobrança que o aluno pode quitar agora."""
        return bool(self.cobranca) and self.cobranca.status in STATUS_A_PAGAR

    @property
    def pode_renovar(self):
        """Pode antecipar o próximo período: só quando nada está em aberto nem em
        decisão - senão seria oferecer um segundo pagamento por cima de outro."""
        return self.cobranca is None

    def e_plano_da_proxima_renovacao(self, plano):
        return self.plano_proxima_renovacao is not None and plano.id == self.plano_proxima_renovacao.id

    @property
    def pode_solicitar_mudanca(self):
        """Só faz sentido agendar a troca quando existe um período pago correndo: sem
        vigência, trocar de plano é simplesmente contratar o novo."""
        return self.ativo and self.solicitacao_mudanca is None

    @property
    def descricao(self):
        if self.estado == ESTADO_ATIVO:
            if self.aguardando_decisao:
                return 'Seu plano está ativo. O comprovante do próximo período está em análise.'
            if self.renovacao_antecipada:
                return 'Seu plano está ativo. A cobrança em aberto é do próximo período.'
            return 'Seu plano está em dia. Nada a pagar neste período.'
        if self.estado == ESTADO_AGUARDANDO_ANALISE:
            return 'Recebemos seu comprovante. A administração vai analisar e confirmar - não é preciso pagar de novo.'
        if self.estado == ESTADO_EM_PROCESSAMENTO:
            return 'O pagamento está sendo processado pelo provedor. Aguarde a confirmação antes de pagar de novo.'
        if self.estado == ESTADO_RECUSADO:
            return 'O pagamento anterior foi recusado. Você pode tentar novamente por Pix ou outra forma.'
        if self.estado == ESTADO_A_PAGAR:
            return 'Conclua o pagamento para ativar seu plano.'
        if self.estado == ESTADO_VENCIDO:
            return 'Seu período de acesso terminou. Renove para voltar a treinar.'
        return 'Escolha um plano para começar.'


def situacao_plano(aluno, pagamentos, *, solicitacao_mudanca=None, hoje=None):
    hoje = hoje or date.today()
    vigente = vigencia_ativa(pagamentos, hoje=hoje)
    cadeia = cadeia_paga(pagamentos, hoje=hoje)
    cobranca = cobranca_pendente(pagamentos)

    renovacao_antecipada = False
    if cobranca and cadeia:
        inicio_cobranca, _ = intervalo_vigencia(cobranca)
        _, fim_pago = intervalo_vigencia(cadeia[-1])
        renovacao_antecipada = bool(inicio_cobranca and fim_pago and inicio_cobranca > fim_pago)

    if vigente:
        estado = ESTADO_ATIVO
    elif cobranca and cobranca.status == 'em_analise':
        estado = ESTADO_AGUARDANDO_ANALISE
    elif cobranca and cobranca.status == 'em_processamento':
        estado = ESTADO_EM_PROCESSAMENTO
    elif cobranca and cobranca.status == 'recusado':
        estado = ESTADO_RECUSADO
    elif cobranca:
        estado = ESTADO_A_PAGAR
    elif any(p.status == 'pago' for p in pagamentos):
        estado = ESTADO_VENCIDO
    else:
        estado = ESTADO_SEM_PLANO

    plano = (vigente.plano if vigente else None) or (cobranca.plano if cobranca else None) or aluno.plano

    return SituacaoPlano(
        estado=estado,
        plano=plano,
        mensalidade_vigente=vigente,
        cobranca=cobranca,
        renovacao_antecipada=renovacao_antecipada,
        proximo_periodo_inicio=inicio_proximo_periodo(pagamentos, hoje=hoje),
        solicitacao_mudanca=solicitacao_mudanca,
        hoje=hoje,
        cadeia_paga=cadeia,
        plano_proxima_renovacao=plano_do_ultimo_periodo(pagamentos) or plano,
    )


def esta_inadimplente(situacao):
    """Quem deve receber cobrança por e-mail: nem quem está com o plano ativo, nem quem
    já pagou e espera uma decisão - avisar essas pessoas seria cobrar duas vezes."""
    return not situacao.ativo and not situacao.aguardando_decisao
